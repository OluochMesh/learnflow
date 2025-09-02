from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.models import Session, db
from datetime import datetime, timedelta
import json

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Homepage - public access"""
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard - requires login"""
    # Get user's recent sessions, newest first
    user_sessions = Session.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Session.created_at.desc()
    ).limit(20).all()
    
    return render_template('dashboard.html', sessions=user_sessions)

@main_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('profile.html', user=current_user)

@main_bp.route('/progress')
@login_required
def progress():
    """Progress tracking with charts"""
    # Get data for charts
    sessions = Session.query.filter_by(user_id=current_user.id).all()
    
    # Prepare data for line chart (entries per day)
    daily_counts = {}
    for session in sessions:
        date_str = session.created_at.strftime('%Y-%m-%d')
        daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
    
    line_data = {
        'labels': list(daily_counts.keys()),
        'data': list(daily_counts.values())
    }
    
    # Prepare data for pie chart (confidence scores)
    score_counts = {'SOLID': 0, 'PARTIAL': 0, 'NEEDS_REVIEW': 0}
    for session in sessions:
        if session.confidence_score in score_counts:
            score_counts[session.confidence_score] += 1
    
    pie_data = {
        'labels': list(score_counts.keys()),
        'data': list(score_counts.values()),
        'colors': ['#10B981', '#F59E0B', '#EF4444']  # green, yellow, red
    }
    
    return render_template('progress.html', 
                         line_data=json.dumps(line_data),
                         pie_data=json.dumps(pie_data))

@main_bp.route('/api/usage')
@login_required
def get_usage():
    """API endpoint to get current usage statistics"""
    # Calculate start of current week
    start_of_week = datetime.now() - timedelta(days=datetime.now().weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Count user's sessions this week
    weekly_sessions = Session.query.filter(
        Session.user_id == current_user.id,
        Session.created_at >= start_of_week
    ).count()
    
    # Total sessions
    total_sessions = Session.query.filter_by(user_id=current_user.id).count()
    
    return jsonify({
        'weekly_sessions': weekly_sessions,
        'total_sessions': total_sessions,
        'is_pro': current_user.subscription_status == 'pro',
        'limit_reached': weekly_sessions >= 5 and current_user.subscription_status == 'free'
    })
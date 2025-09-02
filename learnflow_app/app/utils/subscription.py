from datetime import datetime, timedelta
from app.models import Session

def check_usage_limit(user):
    # Calculate start of current week
    start_of_week = datetime.now() - timedelta(days=datetime.now().weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Count user's sessions this week
    weekly_sessions = Session.query.filter(
        Session.user_id == user.id,
        Session.created_at >= start_of_week
    ).count()
    
    return weekly_sessions < 5  # Free users get 5 sessions per week
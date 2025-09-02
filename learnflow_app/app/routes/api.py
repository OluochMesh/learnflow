from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from app.models import Session, db
from app.utils.ai_helper import analyze_with_ai
from app.utils.subscription import check_usage_limit

api_bp = Blueprint('api', __name__)

@api_bp.route('/analyze', methods=['POST'])
@login_required
def analyze_text():
    data = request.get_json()
    user_text = data.get('text')
    
    if not user_text:
        return jsonify({'error': 'No text provided'}), 400
    
    # Check free tier limit
    if current_user.subscription_status == 'free':
        if not check_usage_limit(current_user):
            return jsonify({'error': 'Free limit reached. Please upgrade to Pro.'}), 402
    
    # Call OpenAI
    try:
        ai_response = analyze_with_ai(user_text)
        
        # Save to database
        new_session = Session(
            user_id=current_user.id,
            input_text=user_text,
            ai_feedback=ai_response,
            confidence_score=ai_response.get('confidenceScore')
        )
        db.session.add(new_session)
        db.session.commit()
        
        return jsonify(ai_response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
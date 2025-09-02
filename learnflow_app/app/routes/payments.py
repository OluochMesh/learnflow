from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from app.models import User, db
from app.utils.intasend_helper import create_intasend_checkout, verify_payment

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/create-checkout', methods=['POST'])
@login_required
def create_checkout():
    try:
        checkout_data = create_intasend_checkout(
            email=current_user.email,
            amount=250,
            plan_name="LearnFlow Pro Monthly"
        )
        
        if checkout_data and 'invoice' in checkout_data:
            return jsonify({
                'checkout_url': checkout_data['invoice']['url'],
                'invoice_id': checkout_data['invoice']['invoice_id']
            })
        else:
            return jsonify({'error': 'Failed to create checkout'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payments_bp.route('/verify-payment/<invoice_id>')
@login_required
def verify_payment_status(invoice_id):
    try:
        is_complete = verify_payment(invoice_id)
        
        if is_complete:
            current_user.subscription_status = 'pro'
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Payment verified'})
        else:
            return jsonify({'status': 'pending', 'message': 'Payment not completed'})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
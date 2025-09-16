from flask import Blueprint, render_template, request, session
from flask_login import login_required, current_user
from models import db, Portfolio
from datetime import datetime, timedelta
from currency_utils import CurrencyConverter

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Get display currency from session or default to INR
    display_currency = session.get('display_currency', 'INR')

    portfolios = Portfolio.query.filter_by(user_id=current_user.id).all()

    # Calculate summary metrics in display currency
    total_value = sum(p.calculate_total_value(display_currency) for p in portfolios)
    total_invested = sum(p.calculate_total_cost(display_currency) for p in portfolios)
    total_gain_loss = total_value - total_invested
    total_return = ((total_value - total_invested) / total_invested * 100) if total_invested > 0 else 0
    total_holdings = sum(len(p.positions) for p in portfolios)

    # Prepare data for charts
    allocation_labels = []
    allocation_values = []

    for portfolio in portfolios:
        if portfolio.positions:
            allocation_labels.append(portfolio.name)
            allocation_values.append(portfolio.calculate_total_value(display_currency))

    # Mock performance data (in production, this would come from historical data)
    performance_dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30, 0, -1)]
    performance_values = [total_invested + (total_gain_loss * (i/30)) for i in range(30)]

    return render_template('dashboard.html',
                         portfolios=portfolios,
                         total_value=total_value,
                         total_invested=total_invested,
                         total_gain_loss=total_gain_loss,
                         total_return=total_return,
                         total_holdings=total_holdings,
                         allocation_labels=allocation_labels,
                         allocation_values=allocation_values,
                         performance_dates=performance_dates,
                         performance_values=performance_values,
                         display_currency=display_currency)

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/features')
def features():
    return render_template('features.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

@main_bp.route('/toggle_currency')
def toggle_currency():
    """Toggle between INR and USD display"""
    current_currency = session.get('display_currency', 'INR')
    new_currency = 'USD' if current_currency == 'INR' else 'INR'
    session['display_currency'] = new_currency

    # Redirect back to the referring page
    from flask import redirect, url_for
    return redirect(request.referrer or url_for('main.dashboard'))
from flask import Blueprint, render_template, session
from flask_login import login_required, current_user
from models import Portfolio
from stock_data import StockDataService
import json

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics')
@login_required
def view():
    display_currency = session.get('display_currency', 'INR')
    portfolios = Portfolio.query.filter_by(user_id=current_user.id).all()

    # Aggregate data across all portfolios
    total_value = 0
    total_invested = 0
    sector_allocation = {}
    country_allocation = {'US': 0, 'India': 0}
    stock_performance = []

    for portfolio in portfolios:
        # Update prices
        StockDataService.update_portfolio_prices(portfolio.positions)

        for position in portfolio.positions:
            market_value = position.calculate_market_value(display_currency)
            cost_basis = position.calculate_cost_basis(display_currency)
            total_value += market_value
            total_invested += cost_basis

            # Sector allocation
            sector = position.sector or 'Unknown'
            sector_allocation[sector] = sector_allocation.get(sector, 0) + market_value

            # Country allocation
            if position.exchange in ['NS', 'BO']:
                country_allocation['India'] += market_value
            else:
                country_allocation['US'] += market_value

            # Stock performance
            stock_performance.append({
                'ticker': position.ticker,
                'return': position.calculate_gain_loss_percentage(),
                'value': market_value
            })

    # Sort stocks by performance
    top_gainers = sorted(stock_performance, key=lambda x: x['return'], reverse=True)[:5]
    top_losers = sorted(stock_performance, key=lambda x: x['return'])[:5]

    # Calculate overall metrics
    total_gain_loss = total_value - total_invested
    total_return = ((total_value - total_invested) / total_invested * 100) if total_invested > 0 else 0

    return render_template('analytics.html',
                         portfolios=portfolios,
                         total_value=total_value,
                         total_invested=total_invested,
                         total_gain_loss=total_gain_loss,
                         total_return=total_return,
                         sector_allocation=json.dumps(sector_allocation),
                         country_allocation=json.dumps(country_allocation),
                         top_gainers=top_gainers,
                         top_losers=top_losers,
                         display_currency=display_currency)
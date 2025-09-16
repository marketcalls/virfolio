from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from models import db, Portfolio, Position
from forms import PortfolioForm, PositionForm
from stock_data import StockDataService
from datetime import datetime

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/portfolios')
@login_required
def list_portfolios():
    display_currency = session.get('display_currency', 'INR')
    portfolios = Portfolio.query.filter_by(user_id=current_user.id).all()
    return render_template('portfolios.html', portfolios=portfolios, display_currency=display_currency)

@portfolio_bp.route('/portfolio/<int:id>')
@login_required
def view(id):
    display_currency = session.get('display_currency', 'INR')
    portfolio = Portfolio.query.get_or_404(id)
    if portfolio.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('main.dashboard'))

    # Update position prices
    positions = StockDataService.update_portfolio_prices(portfolio.positions)
    db.session.commit()

    return render_template('portfolio_view.html', portfolio=portfolio, display_currency=display_currency)

@portfolio_bp.route('/portfolio/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PortfolioForm()
    if form.validate_on_submit():
        portfolio = Portfolio(
            user_id=current_user.id,
            name=form.name.data,
            description=form.description.data,
            base_currency=form.base_currency.data
        )
        db.session.add(portfolio)
        db.session.commit()
        flash('Portfolio created successfully!', 'success')
        return redirect(url_for('portfolio.view', id=portfolio.id))

    return render_template('portfolio_form.html', form=form, title='Create Portfolio')

@portfolio_bp.route('/portfolio/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    portfolio = Portfolio.query.get_or_404(id)
    if portfolio.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('main.dashboard'))

    form = PortfolioForm(obj=portfolio)
    if form.validate_on_submit():
        portfolio.name = form.name.data
        portfolio.description = form.description.data
        portfolio.base_currency = form.base_currency.data
        portfolio.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Portfolio updated successfully!', 'success')
        return redirect(url_for('portfolio.view', id=portfolio.id))

    return render_template('portfolio_form.html', form=form, title='Edit Portfolio')

@portfolio_bp.route('/portfolio/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    portfolio = Portfolio.query.get_or_404(id)
    if portfolio.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('main.dashboard'))

    db.session.delete(portfolio)
    db.session.commit()
    flash('Portfolio deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))

@portfolio_bp.route('/portfolio/<int:portfolio_id>/add_position', methods=['GET', 'POST'])
@login_required
def add_position(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    if portfolio.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('main.dashboard'))

    form = PositionForm()
    if form.validate_on_submit():
        # Get stock info
        stock_info = StockDataService.get_stock_info(form.ticker.data, form.exchange.data)

        position = Position(
            portfolio_id=portfolio.id,
            ticker=form.ticker.data.upper(),
            exchange=form.exchange.data,
            quantity=form.quantity.data,
            buy_price=form.buy_price.data,
            buy_date=form.buy_date.data,
            notes=form.notes.data,
            sector=stock_info.get('sector') if stock_info else None
        )

        # Get current price
        current_price = StockDataService.get_current_price(form.ticker.data, form.exchange.data)
        if current_price:
            position.current_price = current_price
            position.last_updated = datetime.now()

        db.session.add(position)
        db.session.commit()
        flash('Position added successfully!', 'success')
        return redirect(url_for('portfolio.view', id=portfolio.id))

    return render_template('position_form.html', form=form, portfolio=portfolio)

@portfolio_bp.route('/position/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_position(id):
    position = Position.query.get_or_404(id)
    portfolio = position.portfolio

    if portfolio.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('main.dashboard'))

    form = PositionForm(obj=position)
    if form.validate_on_submit():
        position.ticker = form.ticker.data.upper()
        position.exchange = form.exchange.data
        position.quantity = form.quantity.data
        position.buy_price = form.buy_price.data
        position.buy_date = form.buy_date.data
        position.notes = form.notes.data

        # Update stock info
        stock_info = StockDataService.get_stock_info(form.ticker.data, form.exchange.data)
        if stock_info:
            position.sector = stock_info.get('sector')

        # Update current price
        current_price = StockDataService.get_current_price(form.ticker.data, form.exchange.data)
        if current_price:
            position.current_price = current_price
            position.last_updated = datetime.now()

        db.session.commit()
        flash('Position updated successfully!', 'success')
        return redirect(url_for('portfolio.view', id=portfolio.id))

    return render_template('position_form.html', form=form, portfolio=portfolio, editing=True)

@portfolio_bp.route('/position/<int:id>/delete', methods=['POST'])
@login_required
def delete_position(id):
    position = Position.query.get_or_404(id)
    portfolio = position.portfolio

    if portfolio.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('main.dashboard'))

    db.session.delete(position)
    db.session.commit()
    flash('Position deleted successfully!', 'success')
    return redirect(url_for('portfolio.view', id=portfolio.id))
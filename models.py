from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from currency_utils import CurrencyConverter

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    portfolios = db.relationship('Portfolio', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Portfolio(db.Model):
    __tablename__ = 'portfolios'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    base_currency = db.Column(db.String(10), default='USD')
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', back_populates='portfolios')
    positions = db.relationship('Position', back_populates='portfolio', cascade='all, delete-orphan')

    def calculate_total_value(self, currency='INR'):
        """Calculate total portfolio value in specified currency"""
        total = sum(position.calculate_market_value() for position in self.positions)
        if self.base_currency == 'USD' and currency == 'INR':
            return CurrencyConverter.usd_to_inr(total)
        elif self.base_currency == 'INR' and currency == 'USD':
            return CurrencyConverter.inr_to_usd(total)
        return total

    def calculate_total_cost(self, currency='INR'):
        """Calculate total invested amount in specified currency"""
        total = sum(position.quantity * position.buy_price for position in self.positions)
        if self.base_currency == 'USD' and currency == 'INR':
            return CurrencyConverter.usd_to_inr(total)
        elif self.base_currency == 'INR' and currency == 'USD':
            return CurrencyConverter.inr_to_usd(total)
        return total

    def calculate_total_return(self):
        """Calculate percentage return"""
        total_value = self.calculate_total_value(self.base_currency)
        total_cost = self.calculate_total_cost(self.base_currency)
        if total_cost > 0:
            return ((total_value - total_cost) / total_cost) * 100
        return 0

    def calculate_gain_loss(self, currency='INR'):
        """Calculate absolute gain/loss in specified currency"""
        value = self.calculate_total_value(currency)
        cost = self.calculate_total_cost(currency)
        return value - cost

    def __repr__(self):
        return f'<Portfolio {self.name}>'

class Position(db.Model):
    __tablename__ = 'positions'

    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    ticker = db.Column(db.String(20), nullable=False, index=True)
    exchange = db.Column(db.String(20), default='US')
    quantity = db.Column(db.Float, nullable=False)
    buy_price = db.Column(db.Float, nullable=False)
    buy_date = db.Column(db.Date, nullable=False)
    current_price = db.Column(db.Float)
    last_updated = db.Column(db.DateTime)
    sector = db.Column(db.String(50))
    notes = db.Column(db.Text)

    portfolio = db.relationship('Portfolio', back_populates='positions')

    def get_position_currency(self):
        """Determine position currency based on exchange"""
        if self.exchange in ['NS', 'BO']:
            return 'INR'
        return 'USD'

    def calculate_market_value(self, currency='INR'):
        """Calculate market value in specified currency"""
        if self.current_price:
            value = self.quantity * self.current_price
        else:
            value = self.quantity * self.buy_price

        position_currency = self.get_position_currency()
        return CurrencyConverter.convert(value, position_currency, currency)

    def calculate_cost_basis(self, currency='INR'):
        """Calculate cost basis in specified currency"""
        value = self.quantity * self.buy_price
        position_currency = self.get_position_currency()
        return CurrencyConverter.convert(value, position_currency, currency)

    def calculate_gain_loss(self, currency='INR'):
        """Calculate gain/loss in specified currency"""
        if self.current_price:
            gain_loss = (self.current_price - self.buy_price) * self.quantity
        else:
            gain_loss = 0

        position_currency = self.get_position_currency()
        return CurrencyConverter.convert(gain_loss, position_currency, currency)

    def calculate_gain_loss_percentage(self):
        """Calculate percentage gain/loss"""
        if self.current_price and self.buy_price > 0:
            return ((self.current_price - self.buy_price) / self.buy_price) * 100
        return 0

    def __repr__(self):
        return f'<Position {self.ticker}>'
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, NumberRange
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                      validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PortfolioForm(FlaskForm):
    name = StringField('Portfolio Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    base_currency = SelectField('Base Currency',
                                choices=[('USD', 'USD'), ('INR', 'INR')],
                                default='USD')
    submit = SubmitField('Create Portfolio')

class PositionForm(FlaskForm):
    ticker = StringField('Stock Ticker', validators=[DataRequired(), Length(max=20)])
    exchange = SelectField('Exchange',
                          choices=[('US', 'US Markets'), ('NS', 'NSE India'), ('BO', 'BSE India')],
                          default='US')
    quantity = FloatField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    buy_price = FloatField('Buy Price', validators=[DataRequired(), NumberRange(min=0)])
    buy_date = DateField('Buy Date', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Add Position')
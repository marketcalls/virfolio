# VirFolio - Virtual Portfolio Tracker

A modern, feature-rich virtual portfolio tracking application for US and Indian stock markets built with Flask, featuring real-time market data, interactive analytics, and multi-currency support.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v3.1+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🌟 Features

### Core Functionality
- **Multi-Portfolio Management**: Create and manage multiple virtual portfolios
- **Real-Time Market Data**: Live stock prices via yfinance API for US and Indian markets
- **Multi-Currency Support**: Toggle between INR and USD display with automatic conversion
- **User Authentication**: Secure registration and login system
- **Responsive Design**: Modern UI with Tailwind CSS and DaisyUI components

### Analytics & Visualization
- **Interactive Charts**: Built with Plotly for dynamic data visualization
- **Portfolio Analytics**: Sector allocation, geographical distribution, performance metrics
- **Performance Tracking**: Monitor gains/losses, returns, and portfolio growth
- **Top Performers**: Track your best and worst performing stocks

### Market Coverage
- **US Markets**: NYSE, NASDAQ stocks
- **Indian Markets**: NSE and BSE stocks
- **Currency Conversion**: Automatic USD/INR conversion (1 USD = 88 INR default)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Basic knowledge of Flask and web development

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/marketcalls/virfolio.git
cd virfolio
```

### 2. Create a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`

## 📁 Project Structure

```
virfolio/
├── app.py                  # Main application file
├── config.py               # Configuration settings
├── models.py               # Database models (User, Portfolio, Position)
├── forms.py                # WTForms for user input
├── currency_utils.py       # Currency conversion utilities
├── stock_data.py          # Stock data fetching service
├── requirements.txt        # Python dependencies
├── virfolio.db            # SQLite database (created on first run)
│
├── routes/                 # Application routes
│   ├── auth.py            # Authentication routes
│   ├── main.py            # Main application routes
│   ├── portfolio.py       # Portfolio management routes
│   └── analytics.py       # Analytics routes
│
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Homepage
│   ├── dashboard.html     # User dashboard
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── portfolio_view.html    # Portfolio details
│   ├── portfolio_form.html    # Create/edit portfolio
│   ├── position_form.html     # Add/edit position
│   └── analytics.html         # Analytics dashboard
│
└── static/                 # Static files
    ├── css/               # CSS files
    └── js/                # JavaScript files
```

## 💻 Usage

### Getting Started

1. **Register an Account**
   - Navigate to the registration page
   - Create a new account with email and password

2. **Create Your First Portfolio**
   - Click "Create Portfolio" from the dashboard
   - Name your portfolio and select base currency (USD/INR)

3. **Add Stocks**
   - Click "Add Position" in your portfolio
   - Enter stock ticker (e.g., AAPL for Apple, RELIANCE for Reliance Industries)
   - Select exchange (US/NSE/BSE)
   - Enter quantity and purchase price

4. **View Analytics**
   - Navigate to the Analytics page
   - View portfolio allocation, sector distribution, and performance metrics
   - Track top gainers and losers

### Supported Stock Exchanges

- **US Stocks**: Use standard ticker symbols (AAPL, GOOGL, MSFT)
- **Indian Stocks (NSE)**: Use ticker without suffix (RELIANCE, TCS, INFY)
- **Indian Stocks (BSE)**: Use ticker without suffix

### Currency Toggle

Click the currency button (₹ INR / $ USD) in the navigation bar to switch display currency. All values will be automatically converted.

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///virfolio.db
```

### Currency Exchange Rate

To modify the default exchange rate, edit `currency_utils.py`:

```python
class CurrencyConverter:
    USD_TO_INR_RATE = 88.0  # Modify this value
```

## 📊 Database Schema

### Users Table
- `id`: Primary key
- `email`: Unique email address
- `username`: Unique username
- `password_hash`: Encrypted password

### Portfolios Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `name`: Portfolio name
- `base_currency`: USD or INR
- `description`: Optional description

### Positions Table
- `id`: Primary key
- `portfolio_id`: Foreign key to Portfolios
- `ticker`: Stock symbol
- `exchange`: Market exchange (US/NS/BO)
- `quantity`: Number of shares
- `buy_price`: Purchase price per share
- `buy_date`: Purchase date
- `current_price`: Latest market price
- `sector`: Stock sector

## 🛠️ Technologies Used

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: ORM for database operations
- **Flask-Login**: User session management
- **WTForms**: Form validation and rendering
- **yfinance**: Real-time stock data API

### Frontend
- **Tailwind CSS**: Utility-first CSS framework
- **DaisyUI**: Component library for Tailwind
- **Plotly.js**: Interactive charting library

### Database
- **SQLite**: Lightweight database for development
- Can be easily switched to PostgreSQL/MySQL for production

## 🔒 Security Features

- Password hashing with Werkzeug
- Session-based authentication
- CSRF protection with Flask-WTF
- Input validation and sanitization
- Secure cookie handling

## 🚦 API Limitations

- yfinance API has rate limits for frequent requests
- Some stock data may have delays (15-20 minutes for certain exchanges)
- Historical data availability varies by stock

## 🐛 Troubleshooting

### Common Issues

1. **Import Error for yfinance**
   ```bash
   pip install --upgrade yfinance
   ```

2. **Database Error**
   - Delete `virfolio.db` and restart the application
   - The database will be recreated automatically

3. **Stock Data Not Loading**
   - Check internet connection
   - Verify ticker symbol is correct
   - Some Indian stocks may need `.NS` or `.BO` suffix in yfinance

## 📝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

MarketCalls - [@marketcalls](https://twitter.com/marketcalls)

Project Link: [https://github.com/marketcalls/virfolio](https://github.com/marketcalls/virfolio)

## 🙏 Acknowledgments

Special thanks to these amazing projects that made VirFolio possible:

- [yfinance](https://github.com/ranaroussi/yfinance) - Reliable and free stock market data API that powers our real-time price updates
- [DaisyUI](https://daisyui.com/) - Beautiful and accessible UI components that give VirFolio its modern, clean interface
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework for rapid UI development
- [Plotly](https://plotly.com/) for interactive charts
- [Flask](https://flask.palletsprojects.com/) for the web framework

## 📈 Future Enhancements

- [ ] Historical portfolio performance tracking
- [ ] Email notifications for price alerts
- [ ] CSV/Excel import/export functionality
- [ ] Advanced portfolio optimization tools
- [ ] Mobile application
- [ ] Real-time WebSocket updates
- [ ] Social features for sharing portfolios
- [ ] AI-powered investment insights
- [ ] Integration with broker APIs
- [ ] Cryptocurrency support

## 💡 Tips

- Keep your portfolios organized with clear names and descriptions
- Regularly update stock prices for accurate tracking
- Use the analytics page to identify portfolio imbalances
- Export your data periodically for backup
- Monitor sector allocation to maintain diversification

---

**Note**: This is a virtual portfolio tracker for educational and tracking purposes only. It does not execute real trades or provide financial advice.
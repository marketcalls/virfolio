import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

class StockDataService:
    @staticmethod
    def get_ticker_suffix(ticker, exchange):
        """Add appropriate suffix based on exchange"""
        if exchange == 'NS':
            return f"{ticker}.NS"
        elif exchange == 'BO':
            return f"{ticker}.BO"
        return ticker

    @staticmethod
    def get_current_price(ticker, exchange='US'):
        """Fetch current price for a given ticker"""
        try:
            full_ticker = StockDataService.get_ticker_suffix(ticker, exchange)
            stock = yf.Ticker(full_ticker)
            hist = stock.history(period="1d")

            if not hist.empty:
                return hist['Close'].iloc[-1]
            return None
        except Exception as e:
            print(f"Error fetching price for {ticker}: {e}")
            return None

    @staticmethod
    def get_stock_info(ticker, exchange='US'):
        """Fetch detailed stock information"""
        try:
            full_ticker = StockDataService.get_ticker_suffix(ticker, exchange)
            stock = yf.Ticker(full_ticker)
            info = stock.info

            return {
                'symbol': ticker,
                'name': info.get('longName', ticker),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'currency': info.get('currency', 'USD'),
                'current_price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                'day_high': info.get('dayHigh', 0),
                'day_low': info.get('dayLow', 0),
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('forwardPE', info.get('trailingPE', 0)),
                '52_week_high': info.get('fiftyTwoWeekHigh', 0),
                '52_week_low': info.get('fiftyTwoWeekLow', 0)
            }
        except Exception as e:
            print(f"Error fetching info for {ticker}: {e}")
            return None

    @staticmethod
    def get_historical_data(ticker, exchange='US', period='1mo'):
        """Fetch historical price data"""
        try:
            full_ticker = StockDataService.get_ticker_suffix(ticker, exchange)
            stock = yf.Ticker(full_ticker)
            hist = stock.history(period=period)

            return hist
        except Exception as e:
            print(f"Error fetching historical data for {ticker}: {e}")
            return pd.DataFrame()

    @staticmethod
    def update_portfolio_prices(positions):
        """Update current prices for a list of positions"""
        updated_positions = []
        for position in positions:
            current_price = StockDataService.get_current_price(
                position.ticker, position.exchange
            )
            if current_price:
                position.current_price = current_price
                position.last_updated = datetime.now()
                updated_positions.append(position)

        return updated_positions

    @staticmethod
    def get_portfolio_chart_data(positions):
        """Prepare data for portfolio charts"""
        sectors = {}
        countries = {'US': 0, 'India': 0}
        total_value = 0

        for position in positions:
            market_value = position.calculate_market_value()
            total_value += market_value

            # Sector allocation
            sector = position.sector or 'Unknown'
            sectors[sector] = sectors.get(sector, 0) + market_value

            # Country allocation
            if position.exchange in ['NS', 'BO']:
                countries['India'] += market_value
            else:
                countries['US'] += market_value

        return {
            'sectors': sectors,
            'countries': countries,
            'total_value': total_value
        }
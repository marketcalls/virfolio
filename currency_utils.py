class CurrencyConverter:
    """Currency conversion utility for USD/INR"""

    # Default exchange rate (1 USD = 88 INR)
    USD_TO_INR_RATE = 88.0

    @staticmethod
    def usd_to_inr(amount):
        """Convert USD to INR"""
        return amount * CurrencyConverter.USD_TO_INR_RATE

    @staticmethod
    def inr_to_usd(amount):
        """Convert INR to USD"""
        return amount / CurrencyConverter.USD_TO_INR_RATE

    @staticmethod
    def convert(amount, from_currency, to_currency):
        """Convert between currencies"""
        if from_currency == to_currency:
            return amount

        if from_currency == 'USD' and to_currency == 'INR':
            return CurrencyConverter.usd_to_inr(amount)
        elif from_currency == 'INR' and to_currency == 'USD':
            return CurrencyConverter.inr_to_usd(amount)

        return amount

    @staticmethod
    def format_currency(amount, currency='INR'):
        """Format amount with currency symbol"""
        if currency == 'INR':
            return f"₹{amount:,.2f}"
        elif currency == 'USD':
            return f"${amount:,.2f}"
        return f"{amount:,.2f}"
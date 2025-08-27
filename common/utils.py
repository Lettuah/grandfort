# utils.py

def format_price(value):
    """
    Format a numeric value into human-readable currency/price format.
    Example: 1234567.89 -> 1,234,567.89
    """
    try:
        return None if value is None else f"{float(value):,.2f}"
    except (ValueError, TypeError):
        return None

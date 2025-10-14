"""
SellSysInsurance - Utility Functions
Common utility functions for the insurance sales system
"""

def format_currency(amount):
    """Format amount as currency"""
    return f"${amount:,.2f}"

def validate_email(email):
    """Basic email validation"""
    return "@" in email and "." in email

def calculate_premium(base_amount, risk_factor):
    """Calculate insurance premium based on base amount and risk factor"""
    return base_amount * risk_factor

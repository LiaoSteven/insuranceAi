"""
SellSysInsurance - Tests
Basic tests for the insurance sales system
"""

import sys
sys.path.insert(0, 'src')

from main import main
from utils import format_currency, validate_email, calculate_premium

def test_format_currency():
    """Test currency formatting"""
    assert format_currency(1000) == "$1,000.00"
    assert format_currency(1234.56) == "$1,234.56"

def test_validate_email():
    """Test email validation"""
    assert validate_email("test@example.com") == True
    assert validate_email("invalid") == False

def test_calculate_premium():
    """Test premium calculation"""
    assert calculate_premium(1000, 1.5) == 1500.0
    assert calculate_premium(500, 2.0) == 1000.0

if __name__ == "__main__":
    test_format_currency()
    test_validate_email()
    test_calculate_premium()
    print("All tests passed!")

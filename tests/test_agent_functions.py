import pytest
from agent_functions import (
    normalize_order_id,
    get_order_status,
    get_order_items,
    get_delivery_address,
    get_vendor_name,
    get_delivery_date,
)

def test_normalize_order_id_numeric():
    assert normalize_order_id("one zero four five one") == "10451"
    assert normalize_order_id("ten four five one") == "10451"
    assert normalize_order_id("one zero one two three") == "10123"

def test_get_order_status():
    assert "Shipped" in get_order_status("one zero four five one")
    assert "Processing" in get_order_status("one zero one two three")

def test_get_order_items():
    response = get_order_items("one zero four five one")
    
    assert "Wireless Ergonomic Mouse" in response
    assert "Fast Charging USB-C Adapter" in response

def test_get_delivery_address():
    assert "Springfield" in get_delivery_address("one zero four five one")
    assert "Columbus" in get_delivery_address("one zero one two three")

def test_get_vendor_name():
    assert "Tech Supplies Co." in get_vendor_name("one zero four five one")
    assert "AudioGear Inc." in get_vendor_name("one zero one two three")

def test_get_delivery_date():
    assert "2025-06-25" in get_delivery_date("one zero four five one")
    assert "2025-06-28" in get_delivery_date("one zero one two three")

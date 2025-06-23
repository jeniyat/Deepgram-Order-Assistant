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
    assert normalize_order_id("1 0 0 0 1") == "10001"


def test_get_order_status():
    assert "Shipped" in get_order_status("10001")


def test_get_order_items():
    response = get_order_items("10001")
    assert "Wireless Mouse" in response
    assert "USB-C Charger" in response


def test_get_delivery_address():
    assert "Springfield" in get_delivery_address("10001")


def test_get_vendor_name():
    assert "Tech Supplies Co." in get_vendor_name("10001")


def test_get_delivery_date():
    assert "2025-06-25" in get_delivery_date("10001")

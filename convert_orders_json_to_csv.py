import json
import csv

# Load JSON from file
with open('orders.json', 'r') as f:
    orders = json.load(f)

# Write orders.csv
with open('orders.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    # CSV header
    writer.writerow([
        "order_id", "store_location", "vendor_name", "status", "order_date", "delivery_date",
        "shipping_address_line1", "shipping_address_line2", "shipping_address_city",
        "shipping_address_state", "shipping_address_zip", "shipping_address_country"
    ])

    for order in orders:
        address = order.get("shipping_address", {})
        writer.writerow([
            order.get("order_id"),
            order.get("store_location"),
            order.get("vendor_name"),
            order.get("status"),
            order.get("order_date"),
            order.get("delivery_date"),
            address.get("line1"),
            address.get("line2", ""),  # Optional line2
            address.get("city"),
            address.get("state"),
            address.get("zip"),
            address.get("country")
        ])

# Write order_items.csv
with open('order_items.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    # CSV header
    writer.writerow([
        "order_id", "product_id", "product_name", "quantity", "unit_price"
    ])

    for order in orders:
        order_id = order.get("order_id")
        for item in order.get("items", []):
            writer.writerow([
                order_id,
                item.get("product_id"),
                item.get("product_name"),
                item.get("quantity"),
                item.get("unit_price")
            ])

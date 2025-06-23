import json

# Load orders once on import
with open("orders.json") as f:
    ORDERS = json.load(f)

ORDER_ID_MAP = {
    "a one two three": "10001",
    "one zero zero zero one": "10001",
    "b four five six": "10023",
    "one zero zero two three": "10023",
    "c seven eight nine": "10100",
    "one zero one zero zero": "10100",
}


def normalize_order_id(order_id: str) -> str:
    order_id_lower = order_id.lower()
    if order_id_lower in ORDER_ID_MAP:
        return ORDER_ID_MAP[order_id_lower]
    # fallback: remove spaces and check if numeric
    stripped = order_id_lower.replace(" ", "")
    if stripped.isdigit():
        return stripped
    return order_id


def get_order_status(order_id: str) -> str:
    order_id_normalized = normalize_order_id(order_id)
    for order in ORDERS:
        if order["order_id"].lower() == order_id_normalized.lower():
            return f"Order {order['order_id']} from vendor {order['vendor_name']} is currently {order['status']}."
    return f"Sorry, I could not find any order with ID {order_id}."


def get_order_items(order_id: str) -> str:
    order_id_normalized = normalize_order_id(order_id)
    for order in ORDERS:
        if order["order_id"].lower() == order_id_normalized.lower():
            if not order.get("items"):
                return f"Order {order['order_id']} has no items listed."
            items_list = []
            for item in order["items"]:
                qty = item.get("quantity", 1)
                name = item.get("product_name", "Unknown item")
                items_list.append(f"{qty} order of {name}")
            items_str = ", ".join(items_list)
            return f"Order {order['order_id']} contains: {items_str}."
    return f"Sorry, I could not find any order with ID {order_id}."


def get_delivery_address(order_id: str) -> str:
    order_id_normalized = normalize_order_id(order_id)
    for order in ORDERS:
        if order["order_id"].lower() == order_id_normalized.lower():
            addr = order.get("shipping_address")
            if addr:
                parts = [
                    addr.get("line1", ""),
                    addr.get("line2", ""),
                    f"{addr.get('city', '')}, {addr.get('state', '')} {addr.get('zip', '')}",
                    addr.get("country", ""),
                ]
                # Remove empty parts and join with commas
                address_str = ", ".join(filter(None, parts))
                return f"The delivery address for order {order['order_id']} is: {address_str}."
            else:
                return f"No delivery address found for order {order['order_id']}."
    return f"Sorry, I could not find any order with ID {order_id}."


def pick_author(author="Charles Dickens") -> str:
    return f"Tell a story in the same style as {author}. If you don't know the author, say 'I don't know who that is.'"


def end_story() -> str:
    return "Goodbye! Have a great day!"


def get_vendor_name(order_id: str) -> str:
    order_id_normalized = normalize_order_id(order_id)
    for order in ORDERS:
        if order["order_id"].lower() == order_id_normalized.lower():
            return (
                f"The vendor for order {order['order_id']} is {order['vendor_name']}."
            )
    return f"Sorry, I could not find any order with ID {order_id}."


def get_delivery_date(order_id: str) -> str:
    order_id_normalized = normalize_order_id(order_id)
    for order in ORDERS:
        if order["order_id"].lower() == order_id_normalized.lower():
            return f"The delivery date for order {order['order_id']} is {order['delivery_date']}."
    return f"Sorry, I could not find any order with ID {order_id}."


FUNCTION_MAP = {
    "get_order_status": get_order_status,
    "get_order_items": get_order_items,
    "get_delivery_address": get_delivery_address,
    "pick_author": pick_author,
    "end_story": end_story,
    "get_vendor_name": get_vendor_name,
    "get_delivery_date": get_delivery_date,
}

if __name__ == "__main__":
    # Quick test examples
    print(get_order_status("a one two three"))
    print(get_order_items("a one two three"))
    print(get_delivery_address("a one two three"))

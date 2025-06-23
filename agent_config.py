import os

AGENT_SETTINGS = {
    "type": "Settings",
    "audio": {
        "input": {"encoding": "linear16", "sample_rate": 44100},
        "output": {
            "encoding": "linear16",
            "sample_rate": 16000,
        },
    },
    "agent": {
        "listen": {"provider": {"model": "nova-3", "type": "deepgram"}},
        "think": {
            "provider": {"model": "gpt-4o-mini", "type": "open_ai"},
            "prompt": (
                "You are a helpful inventory manager assistant.\n"
                "- When asked about the status of an order, respond concisely with only the status.\n"
                "- When asked about the delivery address, respond concisely with only the shipping address.\n"
                "- When asked about the items, respond concisely with only the items and their quantities.\n"
                "- When asked about the vendor, respond concisely with only the vendor name.\n"
                "- When asked about the delivery date, respond concisely with only the delivery date.\n"
                "- When the user ends the conversation or says goodbye, respond only with: 'Bye and have a nice day.' Do not follow up or continue the conversation after that."
            ),
            "functions": [
                {
                    "name": "get_order_status",
                    "description": "Get the status of an order by its ID.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "order_id": {
                                "type": "string",
                                "description": "The order ID to look up",
                            }
                        },
                        "required": ["order_id"],
                    },
                },
                {
                    "name": "get_delivery_address",
                    "description": "Get the shipping address of an order by its ID.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "order_id": {
                                "type": "string",
                                "description": "The order ID to look up",
                            }
                        },
                        "required": ["order_id"],
                    },
                },
                {
                    "name": "get_order_items",
                    "description": "Get the list of items and quantities for an order by its ID.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "order_id": {
                                "type": "string",
                                "description": "The order ID to look up",
                            }
                        },
                        "required": ["order_id"],
                    },
                },
                {
                    "name": "get_vendor_name",
                    "description": "Get the vendor name of an order by its ID.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "order_id": {
                                "type": "string",
                                "description": "The order ID to look up",
                            }
                        },
                        "required": ["order_id"],
                    },
                },
                {
                    "name": "get_delivery_date",
                    "description": "Get the delivery date of an order by its ID.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "order_id": {
                                "type": "string",
                                "description": "The order ID to look up",
                            }
                        },
                        "required": ["order_id"],
                    },
                },
                {
                    "name": "end_story",
                    "description": "End the conversation.",
                    "parameters": {},
                },
            ],
        },
        "speak": {"provider": {"type": "deepgram", "model": "aura-2-thalia-en"}},
        "greeting": (
            "Hello! I’m your Deepgram inventory manager assistant. "
            "I can help you with order status, delivery schedule, items, shipping address, or vendor details. "
            "Please provide your order ID and your question to get started."
        ),
    },
}

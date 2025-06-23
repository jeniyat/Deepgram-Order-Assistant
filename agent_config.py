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
                "- When the user asks a specific question about an order detail, answer only that question concisely and precisely.\n"
                "  For example, if the user asks about order status, reply only with the status.\n"
                "  If asked about delivery address, reply only with the shipping address, etc.\n"
                "- If the user asks a general or summary question, such as 'Tell me about order {order_id}' or 'Give me details about order {order_id}', "
                "  provide a clear, concise, human-friendly summary combining key details like status, items, delivery date, vendor, and shipping address.\n"
                "- Always answer using complete sentences and a natural, conversational tone.\n"
                "- Do not add extra information beyond what was asked.\n"
                "- When the user ends the conversation or says goodbye, respond only with: 'Bye and have a nice day.' Do not continue the conversation after that."
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

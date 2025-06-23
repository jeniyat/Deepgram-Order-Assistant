# Deepgram Voice-Activated Order Assistant

A voice-enabled conversational assistant designed to help inventory managers manage and query orders across multiple store locations. This project combines Deepgram’s speech-to-text technology with OpenAI’s GPT-4 models to provide real-time, natural language responses about order statuses, delivery timelines, items, shipping addresses, and vendor information.



## Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [Getting Started](#getting-started)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Configuration](#configuration)  
- [Project Structure](#project-structure)  
- [Extending the Assistant](#extending-the-assistant)  
- [License](#license)



## Overview

Inventory managers often need quick access to order information spanning multiple stores. This voice assistant enables hands-free, conversational queries such as:

- "What is the status of order 10001?"  
- "When will order 10023 be delivered?"  
- "What items are in order 10100?"  
- "What is the shipping address for order 10001?"  
- "Who is the vendor for order 10023?"

The system listens to spoken input, transcribes it, processes the intent with GPT-4, calls backend functions to fetch relevant data from JSON-based order records, and responds via synthesized speech.



## Features

- Real-time speech recognition with Deepgram  
- Natural language understanding and generation powered by GPT-4  
- Multi-turn conversational context handling  
- Query order status, delivery date, items, shipping address, and vendor name  
- Graceful session termination with polite goodbyes  
- Supports multiple store orders with normalized order ID mapping



## Getting Started

### Prerequisites

- Python 3.10 or higher  
- [Deepgram API key](https://developers.deepgram.com)  




## Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/deepgram-order-assistant.git
cd deepgram-order-assistant
````

2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your API keys:

```env
DEEPGRAM_API_KEY=your_deepgram_api_key
```

---

## Usage

Start the voice assistant by running:

```bash
python main.py
```

Speak your queries naturally, for example:

* "What is the status of order 10001?"
* "Tell me the delivery address for order 10023."
* "List the items in order 10100."
* "Who is the vendor for order 10023?"
* "Goodbye."

The assistant will respond verbally and in the console log.

---

## Configuration

* `agent_config.py`: Contains agent settings including prompt instructions, models, and function definitions. Customize prompt or add new functions here.
* `agent_functions.py`: Backend logic to process order queries, load order data, and map spoken order IDs to actual IDs. Modify or extend this file to support new query types.
* `orders.json`: JSON data store with orders, vendors, items, delivery info, and shipping addresses. Update this to reflect your real inventory data.

---

## Project Structure

```
├── main.py              # Entry point, manages mic input, websockets, and interaction loop  
├── agent_config.py      # Agent settings and prompts  
├── agent_functions.py   # Backend functions for querying orders  
├── orders.json          # Sample order data  
├── speaker.py           # Audio playback utility  
├── requirements.txt     # Python dependencies  
├── README.md            # This file  
└── .env                 # Environment variables (not committed)
```

---

## Extending the Assistant

* Add new functions to `agent_functions.py` for other queries (e.g., payment status, invoice info)
* Update the `AGENT_SETTINGS` prompt in `agent_config.py` to instruct the assistant on handling new intents
* Enhance natural language understanding by fine-tuning prompt templates or leveraging additional NLP models
* Integrate with real databases or APIs instead of JSON files for dynamic data



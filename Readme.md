# Deepgram Voice-Activated Order Assistant Demo

A voice-enabled conversational assistant for inventory managers to query order status, delivery schedules, items, shipping addresses, and vendor information across multiple store locations. This demo showcases integration of Deepgram’s real-time speech-to-text API using GPT-4 for natural language understanding, providing a seamless voice interface accessible via both a terminal app and a Streamlit web app.



## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Getting Started](#getting-started)
* [Installation](#installation)
* [Usage](#usage)
* [Configuration](#configuration)
* [Directory Structure](#directory-structure)
* [Testing](#testing)
* [Docker Usage](#docker-usage)
* [Credits and Attribution](#credits-and-attribution)


## Overview

Inventory managers require quick, hands-free access to order-related information across multiple stores. This assistant listens to spoken queries, transcribes speech in real time via Deepgram, interprets intent with GPT-4, and fetches relevant data from order records, responding verbally and in text.

## Features

- Real-time speech recognition with Deepgram streaming API  
- Conversational AI powered by OpenAI GPT-4  
- Multi-turn dialogue context management  
- Query order status, delivery date, items, shipping address, and vendor details  
- Session control with start/end calls  
- Runs both as terminal CLI and interactive Streamlit web application


## Flow Diagram

```
+-----------------+        +------------------+          +--------------------+
|   User's Mic    |        |   App (async)    |          |  Deepgram Server   |
+-----------------+        +------------------+          +--------------------+
         |                           |                                |
         |   (1) Capture Audio       |                                |
         |==========================>                                 |
         |                           |                                |
         |                           |  (2) Send audio chunk over WS  |
         |                           |===============================>|
         |                           |                                |
         |                           |    (3) Server processes audio  |
         |                           |<===============================|
         |                           |    (4) Server sends messages   |
         |                           |        (text/audio)            |
         |                           |                                |
         |                           | (5) Receiver coroutine reads   |
         |                           |       incoming WS messages     |
         |                           |                                |
         |                           | (6) If message is a function   |
         |                           |     call request, invoke       |
         |                           |     backend functions to       |
         |                           |     query order data           |
         |                           |                                |
         |                           |     +----------------------------------+
         |                           |     |      Backend Query Layer         |
         |                           |     | (order lookup, normalize IDs,    |
         |                           |     |  fetch status, items, addresses) |
         |                           |     +----------------------------------+
         |                           |                      |
         |                           |<=====================+
         |                           |   (7) If audio bytes received,
         |                           |       enqueue to Speaker queue
         |                           |                              |
         |                           |          +-------------------+
         |                           |          |   Speaker class   |
         |                           |          +-------------------+
         |                           |                     |
         |                           |                     | (8) Background thread
         |                           |                     |     pulls audio from
         |                           |                     |     sync queue
         |                           |                     |====================>
         |                           |                     |                    |
         |                           |                     |        (9) Write to
         |                           |                     |        PyAudio output
         |                           |                     |====================>
         |                           |                     |                    |
         |                           |                     |        +------------------+
         |                           |                     |        | Machine Speakers |
         |                           |                     |        +------------------+
         |                           |                                |
         |                           | (10) Meanwhile, async app continues
         |                           |       sending/receiving messages
         |                           |                                |
+-----------------+        +------------------+          +--------------------+
|   User's Mic    |        |   App (async)    |          |  Deepgram Server   |
+-----------------+        +------------------+          +--------------------+

```

### Steps

1. User’s Mic captures audio — The user speaks a query, and the app captures this audio in real time.

2. App sends audio chunks over WebSocket (WS) — The captured audio data is sent asynchronously in small pieces to the Deepgram server via a WebSocket connection.

3. Deepgram server processes audio — The server performs speech-to-text transcription and natural language understanding.

4. Server sends back messages — These include transcribed text, audio responses, or instructions such as function call requests.

5. App’s receiver coroutine processes incoming messages — It listens continuously for incoming WebSocket messages.

6. Function call requests trigger backend queries — When the server requests data, the app calls local backend functions to fetch order information, normalize order IDs, and generate responses.

7. Audio bytes from server enqueue to the Speaker class — If the server sends audio output (e.g., spoken responses), it is queued for playback.

8. Speaker’s background thread pulls audio data — Running in a separate thread, it continuously retrieves audio chunks from a synchronous queue.

9. Audio is played through the machine’s speakers — The thread writes the audio data to the PyAudio output stream for the user to hear.

10. Meanwhile, the app continues streaming — The asynchronous event loop keeps capturing mic input and handling server responses concurrently, ensuring seamless, real-time conversation flow.




## Getting Started

### Prerequisites

- Python 3.10 or higher  
- Deepgram API Key ([Sign up here](https://developers.deepgram.com))  

## Installation

```bash
git clone https://github.com/yourusername/deepgram-order-assistant.git
cd deepgram-order-assistant

python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

pip install -r requirements.txt
````

Create a `.env` file in the root directory containing:

```env
DEEPGRAM_API_KEY=your_deepgram_api_key
```

## Usage

* **Terminal:**
  Run the voice assistant in the terminal with:

  ```bash
  python main.py
  ```

* **Web App (Streamlit):**
  Launch the interactive voice assistant web app:

  ```bash
  streamlit run app.py
  ```

* Speak naturally to ask questions like:

	* "What is the status of order 10001?"
	* "Tell me the delivery address for order 10023."
	* "List the items in order 10100."
	* "Who is the vendor for order 10023?"


## Configuration

* `agent_config.py`: Customize prompts, models, and function definitions.
* `agent_functions.py`: Backend logic to query orders and map spoken IDs to real data.
* `/data/`: Contains the CSV datasets (`orders.csv` and `order_items.csv`) with order and item data.




## Directory Structure

```
├── main.py              # Terminal app entry point with mic and streaming  
├── app.py               # Streamlit web app interface  
├── agent_config.py      # Agent settings and prompts  
├── agent_functions.py   # Backend query functions  
├── /data                # Folder containing CSV datasets (orders.csv, order_items.csv)  
├── speaker.py           # Audio playback utility  
├── requirements.txt     # Dependencies  
├── README.md            # This file  
└── .env                 # API keys (user needs to create this file)  

```

## Testing

Automated tests are included to verify the core backend functions such as order ID normalization and order data retrieval.

### Running Tests

Make sure you have `pytest` installed (it should be included in `requirements.txt`):

```bash
pip install pytest
```

Run the tests from the root project directory:

```bash
pytest tests/
```

The tests cover functions like:

* `normalize_order_id`: Converts spoken order IDs to normalized strings
* `get_order_status`: Retrieves order shipment status
* `get_order_items`: Lists items in an order
* `get_delivery_address`: Fetches shipping address
* `get_vendor_name`: Gets vendor information
* `get_delivery_date`: Returns estimated delivery date

This ensures your backend logic behaves as expected.



## Docker Usage

### Build and Run the Docker Container

1. Build the Docker image:

```bash
podman build -t deepgram-voice-assistant:latest .
# or with docker:
# docker build -t deepgram-voice-assistant:latest .
```

2. Run the container (map port 8501 and pass your `.env` file):

```bash
podman run -d -p 8501:8501 --env-file .env --name deepgram-voice-assistant deepgram-voice-assistant:latest
# or with docker:
# docker run -d -p 8501:8501 --env-file .env --name deepgram-voice-assistant deepgram-voice-assistant:latest
```

3. Access the app in your browser at [http://localhost:8501](http://localhost:8501).



### Important Note on macOS

Due to macOS architecture and container isolation, **Docker containers cannot access your Mac's microphone or speaker hardware**. This affects real-time audio features like speech input and output.

#### ⚠️ Why Real-Time Voice Doesn't Work in Docker on macOS

* **Docker on macOS uses a Linux VM**: Docker Desktop for Mac runs a lightweight Linux virtual machine (VM) to host the Docker daemon and containers.
* **Hardware Isolation**: This VM isolates containers from the Mac host’s hardware, including audio devices.
* **No Direct Sound Access**: Applications inside the container cannot access the host's sound card or `/dev/snd`, which are essential for audio input/output.

#### Workarounds (Advanced)

You *can* try setting up a **PulseAudio** server on the Mac host and configuring the container to use it. This involves:

* Installing and running a PulseAudio server on your Mac
* Exposing it to the Docker container over a TCP socket
* Configuring ALSA or PyAudio inside the container to route through PulseAudio

However, this approach is **not seamless**, requires manual setup, and is **outside the scope of this project**.

#### Recommendation

For full voice functionality (microphone and speaker access):

* **Run the app natively on your Mac** (outside Docker) using the instructions in the [Usage](#usage) section.
* Use Docker only for UI deployments in remote or cloud environments where audio devices are properly exposed.





## Credits and Attribution

This project is **inspired by** and **developed following guidelines from** the [Deepgram Voice Agent Python Client repository](https://github.com/deepgram/voice-agent-python-client/). Special thanks to the Deepgram team for providing this reference implementation of audio playback and voice agent components, which greatly informed the design and architecture of this demo.



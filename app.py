import streamlit as st
import threading
import asyncio
import logging
import queue
from streamlit_autorefresh import st_autorefresh

from main import start_stream, open_mic_stream, close_mic_stream
from agent_config import AGENT_SETTINGS
from agent_functions import FUNCTION_MAP
from speaker import Speaker

log_queue = queue.Queue()
transcript_queue = queue.Queue()


class QueueHandler(logging.Handler):
    def __init__(self, q):
        super().__init__()
        self.q = q

    def emit(self, record):
        try:
            msg = self.format(record)
            self.q.put(msg)
        except Exception:
            self.handleError(record)


root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

existing_console_handler = None
for handler in root_logger.handlers:
    if isinstance(handler, logging.StreamHandler):
        existing_console_handler = handler
        break

if existing_console_handler is None:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

queue_handler = QueueHandler(log_queue)
queue_handler.setLevel(logging.INFO)
queue_handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
root_logger.addHandler(queue_handler)

logger = logging.getLogger(__name__)


def voice_agent_runner(shared, transcript_queue):
    audio, mic_stream = None, None
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def run_stream():
        try:
            await start_stream(
                mic_stream, "wss://agent.deepgram.com/v1/agent/converse", shared
            )
        except asyncio.CancelledError:
            logger.info("Stream task cancelled.")
        finally:
            close_mic_stream(audio, mic_stream)
            logger.info("🎤 Microphone stream closed.")

    try:
        audio, mic_stream = open_mic_stream()
        task = loop.create_task(run_stream())

        # Poll for endstream flag, then cancel task if set
        while not shared.get("endstream", False):
            loop.run_until_complete(asyncio.sleep(0.1))

        # When endstream is True:
        task.cancel()
        loop.run_until_complete(task)
    except Exception as e:
        logger.error(f"Exception in voice agent: {e}")
    finally:
        loop.close()


def app():
    st.set_page_config(page_title="Deepgram Voice Agent", layout="wide")

    st.markdown(
        """
        <style>
        .stButton>button {
            font-size: 20px;
            height: 3em;
            width: 100%;
            margin-top: 0.5em;
        }
        .block-container {
            padding-top: 2rem;
        }
        .function-response {
            background-color: #f0f8ff;
            border-left: 4px solid #007acc;
            padding: 0.5em 1em;
            margin-bottom: 0.5em;
            font-style: italic;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("🧠🎙️ Deepgram Voice Agent")

    with st.expander("ℹ️ About this App", expanded=True):
        st.markdown(
            """
            This interface lets you interact with a voice agent using Deepgram's real-time transcription API.
            - Click 🟢📞 to start a call.
            - Press 🔴 to end the session.
        """
        )

    if "thread" not in st.session_state:
        st.session_state.thread = None
    if "shared" not in st.session_state:
        st.session_state.shared = {
            "endstream": False,
            "agent_ready": False,
            "goodbye_triggered": False,
            "mic_on": True,
        }
    if "function_responses" not in st.session_state:
        st.session_state.function_responses = []
    if "call_running" not in st.session_state:
        st.session_state.call_running = False
    if "call_ended" not in st.session_state:
        st.session_state.call_ended = False

    st.markdown("### 📞 Controls")

    start_disabled = st.session_state.call_running
    end_disabled = not st.session_state.call_running

    if st.button(
        "🟢 Start Call", disabled=start_disabled, key="start_call", help="Start Call"
    ):
        if st.session_state.thread and st.session_state.thread.is_alive():
            st.warning("Call already running")
        else:
            st.session_state.shared = {
                "endstream": False,
                "agent_ready": False,
                "goodbye_triggered": False,
                "mic_on": True,
            }
            st.session_state.function_responses.clear()

            while not transcript_queue.empty():
                try:
                    transcript_queue.get_nowait()
                except queue.Empty:
                    break

            st.session_state.thread = threading.Thread(
                target=voice_agent_runner,
                args=(st.session_state.shared, transcript_queue),
                daemon=True,
            )
            st.session_state.thread.start()
            st.session_state.call_running = True
            st.session_state.call_ended = False
            st.success("Call started")

    if st.button("🔴 End Call", disabled=end_disabled, key="end_call", help="End Call"):
        if st.session_state.thread and st.session_state.thread.is_alive():
            st.session_state.shared["endstream"] = True
            st.success("Ending call...")
        else:
            st.warning("No call is running")

    if st.session_state.call_running:
        if "last_function_response" in st.session_state.shared:
            resp = st.session_state.shared.pop("last_function_response", None)
            if resp:
                st.session_state.function_responses.append(resp)

    if (
        st.session_state.thread
        and not st.session_state.thread.is_alive()
        and st.session_state.call_running
    ):
        st.session_state.call_running = False
        st.session_state.call_ended = True

    if st.session_state.call_ended:
        st.info("📞 Call ended. You can start a new call.")

    if st.session_state.function_responses:
        st.markdown("### Function Call Responses")
        for resp in st.session_state.function_responses:
            st.markdown(
                f'<div class="function-response">{resp}</div>', unsafe_allow_html=True
            )

    st_autorefresh(interval=1000, key="refresh")


if __name__ == "__main__":
    app()

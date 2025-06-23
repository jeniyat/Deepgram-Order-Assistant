import os
import json
import asyncio
import logging
import argparse
import pyaudio
import websockets
from websockets.exceptions import ConnectionClosedOK

from agent_config import AGENT_SETTINGS
from agent_functions import FUNCTION_MAP
from speaker import Speaker

logger = logging.getLogger("__name__")

from dotenv import load_dotenv  # Ensure this import is here

# Load environment variables from .env
load_dotenv()


def configure_logger(loglevel):
    level = getattr(logging, loglevel.upper(), logging.DEBUG)
    logger.setLevel(level)
    formatter = logging.Formatter("%(levelname)-8s %(asctime)s %(name)-12s %(message)s")
    streamhandler = logging.StreamHandler()
    streamhandler.setFormatter(formatter)
    if not logger.hasHandlers():
        logger.addHandler(streamhandler)


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
FRAMES_PER_BUFFER = 1024


def _handle_task_result(task):
    try:
        task.result()
    except asyncio.CancelledError:
        pass
    except Exception:
        logger.error("Exception raised by task = %r", task)


async def start_stream(mic_stream, uri, shared):
    extra_headers = {"Authorization": f"Token {os.environ.get('DEEPGRAM_API_KEY')}"}
    logger.debug(f"Connecting to {uri}")

    try:
        async with websockets.connect(uri, additional_headers=extra_headers) as ws:

            async def sender(mic_stream, ws, shared):
                await ws.send(json.dumps(AGENT_SETTINGS))
                while True:
                    if shared.get("endstream", False):
                        await ws.send(b"")
                        break

                    if not shared.get("agent_ready", False):
                        await asyncio.sleep(0.1)
                        continue

                    # Mic is always on now; no mic_on check

                    try:
                        piece = mic_stream.read(
                            FRAMES_PER_BUFFER, exception_on_overflow=False
                        )
                        await ws.send(piece)
                    except ConnectionClosedOK:
                        logger.info("WebSocket closed normally, sender stopping.")
                        break
                    except Exception as e:
                        logger.error(f"Sender error: {e}")
                        break

                    await asyncio.sleep(0.01)

            async def receiver(ws, shared):
                speaker = Speaker(
                    AGENT_SETTINGS.get("audio", {})
                    .get("output", {})
                    .get("sample_rate", 16000)
                )
                with speaker:
                    async for msg in ws:
                        try:
                            if isinstance(msg, bytes):
                                await speaker.play(msg)
                                continue

                            msg = json.loads(msg)
                            msg_type = msg.get("type", "unknown")

                            if msg_type == "Welcome":
                                logger.info(
                                    f"Welcome received. Request id: {msg.get('request_id', '')}"
                                )

                            elif msg_type == "SettingsApplied":
                                logger.info("Settings applied, streaming microphone")
                                shared["agent_ready"] = True

                            elif msg_type == "ConversationText":
                                content = msg.get("content", "").strip()
                                logger.info(
                                    f"Role: {msg.get('role')} | Content: {content}"
                                )

                            elif msg_type == "UserStartedSpeaking":
                                logger.info("User started speaking. Stopping speaker")
                                speaker.stop()

                            elif msg_type == "AgentAudioDone":
                                logger.info("Agent finished speaking.")
                                if shared.get("goodbye_triggered", False):
                                    logger.info(
                                        "Farewell audio done, closing connection."
                                    )
                                    shared["endstream"] = True
                                    await ws.send(b"")
                                    await ws.close()
                                    break

                            elif msg_type == "FunctionCallRequest":
                                logger.info(
                                    f"Agent requested function call: {json.dumps(msg, indent=2)}"
                                )
                                for function_obj in msg.get("functions", []):
                                    fid = function_obj.get("id")
                                    name = function_obj.get("name")
                                    arguments = function_obj.get("arguments", "{}")
                                    func = FUNCTION_MAP.get(name)

                                    if name == "end_story":
                                        logger.info(
                                            "Received 'end_story' function call, shutting down."
                                        )
                                        response = {
                                            "type": "FunctionCallResponse",
                                            "id": fid,
                                            "name": name,
                                            "content": "Bye, it was nice talking to you! 👋",
                                        }
                                        await ws.send(json.dumps(response))
                                        shared["goodbye_triggered"] = True
                                        continue

                                    funcresponse = "Function not found."
                                    if func:
                                        try:
                                            kwargs = json.loads(arguments)
                                            logger.debug(f"Function args: {kwargs}")
                                            funcresponse = func(**kwargs)
                                        except Exception as e:
                                            logger.error(
                                                f"Error calling function {name}: {e}"
                                            )
                                            funcresponse = "Function execution failed."

                                    response = {
                                        "type": "FunctionCallResponse",
                                        "id": fid,
                                        "name": name,
                                        "content": funcresponse,
                                    }
                                    await ws.send(
                                        json.dumps(response, separators=(",", ":"))
                                    )

                            elif msg_type == "FunctionCallResponse":
                                content = msg.get("content", "").strip()
                                logger.info(
                                    f"Role: assistant | FunctionResponse: {content}"
                                )

                            elif msg_type in ["Error", "Warning"]:
                                logger.warning(f"{msg_type}: {msg}")
                            else:
                                logger.debug(f"Unhandled message type: {msg_type}")
                        except Exception as e:
                            logger.error(
                                f"Receiver exception on msg: {msg}, Error: {e}"
                            )

            loop = asyncio.get_event_loop()
            send_task = loop.create_task(sender(mic_stream, ws, shared))
            recv_task = loop.create_task(receiver(ws, shared))
            send_task.add_done_callback(_handle_task_result)
            recv_task.add_done_callback(_handle_task_result)
            await asyncio.wait([send_task, recv_task])

    except Exception as e:
        logger.error(f"Caught exception: {e}")


def open_mic_stream():
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER,
    )
    return audio, stream


def close_mic_stream(audio, stream):
    if stream:
        stream.stop_stream()
        stream.close()
    if audio:
        audio.terminate()


def run_voiceagent(uri):
    shared_data = {"endstream": False, "agent_ready": False, "goodbye_triggered": False}
    audio, mic_stream = open_mic_stream()
    try:
        asyncio.run(start_stream(mic_stream, uri, shared_data))
    except KeyboardInterrupt:
        logger.info(
            "👋 Shutting down gracefully on keyboard interrupt (Ctrl+C). Goodbye!"
        )
    finally:
        close_mic_stream(audio, mic_stream)
        logger.info("🎤 Microphone stream closed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("voice_agent")
    parser.add_argument(
        "url",
        help="WebSocket URL of Deepgram agent",
        type=str,
        nargs="?",
        default="wss://agent.deepgram.com/v1/agent/converse",
    )
    parser.add_argument(
        "--loglevel",
        help="Set logging level",
        type=str,
        default="DEBUG",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    )
    args = parser.parse_args()

    configure_logger(args.loglevel)
    run_voiceagent(args.url)

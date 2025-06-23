import janus
import threading
import pyaudio
import queue
import time
import asyncio


def _play(audio_out, stream, stop):
    while not stop.is_set():
        try:
            data = audio_out.sync_q.get(True, 0.05)
            stream.write(data)
        except queue.Empty:
            pass


class Speaker:
    def __init__(self, sample_rate):
        self._queue = None
        self._stream = None
        self._thread = None
        self._stop = None
        self.sample_rate = sample_rate

    def __enter__(self):
        audio = pyaudio.PyAudio()
        self._stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=False,
            output=True,
        )
        self._queue = janus.Queue()
        self._stop = threading.Event()
        self._thread = threading.Thread(
            target=_play, args=(self._queue, self._stream, self._stop), daemon=True
        )
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._stop.set()
        self._thread.join()
        self._stream.close()
        self._stream = None
        self._queue = None
        self._thread = None
        self._stop = None

    async def play(self, data):
        return await self._queue.async_q.put(data)

    def stop(self):
        if self._queue and self._queue.async_q:
            while not self._queue.async_q.empty():
                try:
                    self._queue.async_q.get_nowait()
                except janus.QueueEmpty:
                    break


if __name__ == "__main__":

    print("Testing Speaker playback with silence (no sound)...")
    with Speaker(sample_rate=16000) as speaker:
        loop = asyncio.get_event_loop()
        # Put 0.5 seconds of silence (32000 bytes of zeros for 16kHz 16-bit mono)
        silence = b"\x00" * 32000
        loop.run_until_complete(speaker.play(silence))
        print("Silence queued for playback. Waiting 1 sec...")
        time.sleep(1)
    print("Speaker test done.")

import asyncio

from loguru import logger


class AudioProcess(object):
    _instance = None
    _process = None
    _running = False

    def __new__(cls):
        # Singleton pattern to make sure we only create this instance once
        if cls._instance is None:
            cls._instance = super(AudioProcess, cls).__new__(cls)
        return cls._instance

    async def play(self, audio_file_path: str):
        self._running = True

        # Play audio file via `ffplay`
        self._process = await asyncio.create_subprocess_shell(
            " ".join([
                "ffplay",
                "-nodisp",  # Disable display
                "-loglevel quiet",  # Disable logging
                "-autoexit",  # Exit `ffplay` automatically after playing
                audio_file_path
            ])
        )

        # Wait for the subprocess to finish
        await self._process.wait()
        await self.stop()

    async def stop(self):
        if self._running:
            try:
                self._process.terminate()
                await self._process.wait()
            except Exception:
                # This might throw when process is already gone, silently fail
                pass
            self._running = False


player = AudioProcess()


async def play_audio(audio_file_path: str):
    # Make sure current process gets terminated first
    await player.stop()

    # Play audio file via `ffplay`
    logger.debug("Play audio file @ {}".format(audio_file_path))
    await player.play(audio_file_path)


async def stop_audio():
    await player.stop()

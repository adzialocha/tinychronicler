import asyncio
import datetime
import os
import time

from loguru import logger


class VideoProcess(object):
    _instance = None
    _process = None
    _timeout = None
    _running = False

    def __new__(cls):
        # Singleton pattern to make sure we only create this instance once
        if cls._instance is None:
            cls._instance = super(VideoProcess, cls).__new__(cls)
        return cls._instance

    async def show_image(
        self,
        image_file_path: str,
        monitor_id: int,
        duration: str,
    ):
        self._running = True

        # Play image file via `ffplay`
        self._process = await asyncio.create_subprocess_shell(
            " ".join([
                "ffplay",
                # "-fs",  # Enable fullscreen
                "-noborder",  # Borderless window
                "-loglevel",  # Disable logging
                "quiet",
                image_file_path,
            ]),
            env={
                **os.environ,
                "DISPLAY": ":{}.0".format(monitor_id)  # Select monitor
            }
        )

        # Convert duration string to seconds
        dur = time.strptime(duration, '%H:%M:%S')
        seconds = datetime.timedelta(hours=dur.tm_hour,
                                     minutes=dur.tm_min,
                                     seconds=dur.tm_sec).total_seconds()

        # Run `ffplay` for x seconds and then terminate process
        await asyncio.wait([
            asyncio.sleep(seconds),
            self._process.wait(),
        ], return_when=asyncio.FIRST_COMPLETED)
        await self.stop()

    async def play_video(
        self,
        video_file_path: str,
        monitor_id: int,
        duration: str,
        seek: str,
        muted: bool
    ):
        self._running = True

        # Play video file via `ffplay`
        self._process = await asyncio.create_subprocess_shell(
            " ".join([
                "ffplay",
                # "-fs",  # Enable fullscreen
                "-loop 0",  # Loop forever
                "-noborder",  # Borderless window
                "-sn",  # Disable subtitles
                "-loglevel quiet",  # Disable logging
                "-t {}".format(duration),  # Set duration of video
                # Start playing video from this position
                "-ss {}".format(seek),
                "-an" if muted else "",  # Disable audio
                "-autoexit",  # Exit `ffplay` automatically after playing
                video_file_path,
            ]),
            env={
                **os.environ,
                "DISPLAY": ":{}.0".format(monitor_id)  # Select monitor
            }
        )

        # Convert duration string to seconds
        dur = time.strptime(duration, '%H:%M:%S')
        seconds = datetime.timedelta(hours=dur.tm_hour,
                                     minutes=dur.tm_min,
                                     seconds=dur.tm_sec).total_seconds()

        # Run `ffplay` for x seconds and then terminate process
        await asyncio.wait([
            asyncio.sleep(seconds),
            self._process.wait(),
        ], return_when=asyncio.FIRST_COMPLETED)
        await self.stop()

    async def stop(self):
        if self._timeout is not None:
            self._timeout.cancel()
            self._timeout = None

        if self._running:
            try:
                self._process.kill()
                await self._process.wait()
            except Exception:
                # This might throw when process is already gone, silently fail
                pass
            self._running = False


player = VideoProcess()


async def play_video(
    video_file_path: str,
    monitor_id: int = 0,
    duration: str = "00:00:10",
    seek: str = "00:00:00",
    muted: bool = False
):
    # Make sure current process gets terminated first
    await player.stop()

    # Show video via `ffplay`
    logger.debug("Play video file @ {}".format(video_file_path))
    await player.play_video(
        video_file_path,
        monitor_id,
        duration,
        seek,
        muted
    )


async def show_image(
    image_file_path: str,
    monitor_id: int = 0,
    duration: str = "00:00:10"
):
    # Make sure current process gets terminated first
    await player.stop()

    # Show image via `ffplay`
    logger.debug("Show image file @ {}".format(image_file_path))
    await player.show_image(
        image_file_path,
        monitor_id,
        duration,
    )


async def stop_video_or_image():
    await player.stop()

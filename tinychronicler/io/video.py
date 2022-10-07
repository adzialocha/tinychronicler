import asyncio
import datetime
import time

process = None


async def stop_video_or_image():
    if process is not None:
        process.terminate()
        await process.wait()


async def play_video(
        video_file_path: str,
        monitor_id: int = 0,
        duration: str = "00:10:00",
        seek: str = "00:00:00",
        muted: bool = False):
    # Make sure current process gets terminated first
    await stop_video_or_image()

    # Show video via `ffplay`
    process = await asyncio.create_subprocess_exec(
        [
            "DISPLAY=:{}.0".format(monitor_id),  # Select monitor
            "ffplay",
            "-fs",  # Enable fullscreen
            "-loop 0",  # Loop forever
            "-noborder",  # Borderless window
            "-sn",  # Disable subtitles
            "-loglevel quiet",  # Disable logging
            "-t {}".format(duration),  # Set duration of video
            "-ss {}".format(seek),  # Start playing video from this position
            "-an" if muted else "",  # Disable audio
            "-autoexit",  # Exit `ffplay` automatically after playing
            video_file_path
        ],
    )

    # Wait for the subprocess to finish
    await process.wait()
    process = None


def show_image(
        image_file_path: str,
        monitor_id: int = 0,
        duration: str = "00:10:00"):
    # Make sure current process gets terminated first
    await stop_video_or_image()

    # Show image via `ffplay`
    process = await asyncio.create_subprocess_exec(
        [
            "DISPLAY=:{}.0".format(monitor_id),  # Select monitor
            "ffplay",
            "-fs",  # Enable fullscreen
            "-noborder",  # Borderless window
            "-loglevel quiet",  # Disable logging
            image_file_path
        ],
    )

    # Convert duration string to seconds
    dur = time.strptime(duration, '%H:%M:%S')
    seconds = datetime.timedelta(hours=dur.tm_hour,
                                 minutes=dur.tm_min,
                                 seconds=dur.tm_sec).total_seconds()

    # Run `ffplay` for x seconds and then terminate process
    time.sleep(seconds)
    process.terminate()
    await process.wait()
    process = None

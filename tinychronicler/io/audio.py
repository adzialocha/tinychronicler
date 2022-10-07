import asyncio

process = None


async def stop_audio():
    if process is not None:
        process.terminate()
        await process.wait()


async def play_audio(audio_file_path: str):
    # Make sure current process gets terminated first
    await stop_audio()

    # Play audio file via `ffplay`
    process = await asyncio.create_subprocess_exec(
        [
            "ffplay",
            "-nodisp",  # Disable display
            "-loglevel quiet",  # Disable logging
            "-autoexit",  # Exit `ffplay` automatically after playing
            audio_file_path
        ],
    )

    # Wait for the subprocess to finish
    await process.wait()
    process = None

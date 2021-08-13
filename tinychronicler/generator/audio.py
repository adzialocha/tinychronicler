import librosa

ONSET_THRESHOLD_DEFAULT = 0.2
ONSET_MIN_DURATION_DEFAULT = 0.1


def remove_close_onsets(
    onset_frames, onset_env_times, min_duration=ONSET_MIN_DURATION_DEFAULT
):
    # Convert frames to time
    onset_times = onset_env_times[onset_frames]

    # Always add the first onset to the array
    onset_cleaned = []

    # Remove onsets which are too close to each other
    start_index = 0
    while start_index <= len(onset_times) - 1:
        start_time = onset_times[start_index]
        found = False

        for index, end_time in enumerate(onset_times[start_index + 1 :]):
            end_index = index + start_index + 1
            end_time = onset_times[end_index]
            duration = end_time - start_time

            # Add onset when long enough duration or last event
            if duration >= min_duration or end_index == len(onset_times) - 2:
                onset_cleaned.append(onset_frames[start_index])
                start_index = end_index
                found = True
                break

        if not found:
            onset_cleaned.append(onset_frames[start_index])
            break

    return onset_cleaned


def detect_onsets(y, sr, threshold=ONSET_THRESHOLD_DEFAULT):
    # Get the frame->beat strength profile
    onset_envelope = librosa.onset.onset_strength(y=y, sr=sr)

    # Locate note onset events
    onset_frames = librosa.onset.onset_detect(
        y=y, sr=sr, onset_envelope=onset_envelope
    )

    # Remove onsets which signals are too low
    onset_frames = [o for o in onset_frames if onset_envelope[o] >= threshold]

    # Convert frames to time
    onset_env_times = librosa.times_like(onset_envelope, sr=sr)
    return onset_frames, onset_envelope, onset_env_times

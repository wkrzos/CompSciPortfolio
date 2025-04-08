from datetime import timedelta

def time_to_seconds(t_str):
    """Convert time string (HH:MM:SS or HH:MM) to seconds since midnight."""
    parts = t_str.split(':')
    if len(parts) == 3:
        h, m, s = map(int, parts)
    elif len(parts) == 2:
        h, m = map(int, parts)
        s = 0
    else:
        raise ValueError(f"Invalid time format: {t_str}. Expected HH:MM:SS or HH:MM")
    return h * 3600 + m * 60 + s

def seconds_to_time_str(seconds):
    """Convert seconds since midnight to HH:MM:SS format."""
    return str(timedelta(seconds=seconds))

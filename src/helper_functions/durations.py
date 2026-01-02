import re

def sum_durations_w_format(durations:list[str]):
        total_seconds = 0

        for duration in durations:
            total_seconds += parse_duration(duration)

        return format_duration(total_seconds)

def format_duration(total_seconds):
    days, rem = divmod(total_seconds, 86400)
    hrs, rem = divmod(rem, 3600)
    mins, secs = divmod(rem, 60)

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hrs > 0 or days > 0:  # show hours if any days or hours exist
        parts.append(f"{hrs}h")
    if mins > 0 or hrs > 0 or days > 0:  # show minutes if any larger units exist
        parts.append(f"{mins}m")
    parts.append(f"{secs}s")  # always show seconds

    return ":".join(parts)

def parse_duration(duration: int|str):
    if isinstance(duration, int):
        total_seconds = duration
    elif isinstance(duration, str):
        if not duration:
            raise ValueError(f"Duration str is len 0: {duration} | len:{len(duration)}")
        # Matches optional D,H,M,S parts
        pattern = r'(?:(\d+)d:)?(?:(\d+)h:)?(?:(\d+)m:)?(\d+)s'
        match = re.fullmatch(pattern, duration)
        if not match:
            raise ValueError(f"Invalid duration format: {duration}")
        total_seconds = None
        days, hrs, mins, secs = match.groups(default='0')
        total_seconds = int(days)*86400 + int(hrs)*3600 + int(mins)*60 + int(secs)
    else:
        raise ValueError(f"Invalid duration type: {type(duration)} -> {duration}")
    

    return total_seconds

def compare_prev_to_current(prev: int|str, current: int|str):
    prev_sec = parse_duration(prev)
    current_sec = parse_duration(current)
    
    diff_sec = current_sec - prev_sec

    return diff_sec
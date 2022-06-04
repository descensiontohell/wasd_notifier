import re


def is_valid_channel_name(channel_name: str) -> bool:
    some_weird_shit = re.match(r'([A-z\][\d])+', channel_name)
    if some_weird_shit and some_weird_shit[0] == channel_name:
        return True
    else:
        return False

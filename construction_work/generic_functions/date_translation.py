"""Date translation utils"""

from datetime import datetime


def translate_timezone(date_str, target_tz) -> str:
    """Translate timezone"""
    tmp_date = datetime.fromisoformat(date_str)
    tmp_date = tmp_date.astimezone(target_tz)
    return tmp_date.isoformat()

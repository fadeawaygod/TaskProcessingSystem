from datetime import datetime, timezone


def get_utc_now_without_timezone() -> datetime:
    """Return now with a datetime with timezone not aware and the timezone is set to UTC."""
    return datetime.now(timezone.utc).replace(tzinfo=None)

__all__ = [
    "datetime_from_utc_to_local"
]

from time import (
    time
)
from datetime import (
    datetime
)

fromtimestamp = datetime.fromtimestamp
utcfromtimestamp = datetime.utcfromtimestamp


# https://stackoverflow.com/a/19238551
def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time()
    offset = fromtimestamp(now_timestamp) - utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

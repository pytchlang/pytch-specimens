import hashlib
import unicodedata


def sha256hex(data_or_string):
    data = (
        unicodedata.normalize("NFC", data_or_string).encode("utf-8")
        if isinstance(data_or_string, str)
        else data_or_string
    )
    return hashlib.sha256(data).hexdigest()

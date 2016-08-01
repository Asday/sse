import re

prepathurl__protocol_host = re.compile(
    "^(https?://)(.*?)[:/]".encode()
)

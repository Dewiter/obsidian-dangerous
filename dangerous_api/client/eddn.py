import json
import logging
import zlib
from collections.abc import AsyncIterator

import zmq
import zmq.asyncio

log = logging.getLogger(__name__)


async def messages(url: str) -> AsyncIterator[dict]:
    """
    Yield decoded EDDN envelopes forever.
    """
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(url)
    socket.setsockopt_string(zmq.SUBSCRIBE, "")
    log.info("Connected to EDDN at %s", url)

    try:
        while True:
            raw = await socket.recv()
            try:
                yield json.loads(zlib.decompress(raw))
            except (zlib.error, json.JSONDecodeError) as error:
                log.warning("Could not decode EDDN message: %s", error)
    finally:
        socket.close()
        context.term()

"""
HTTP Client for connection to CKAN API from Chilean Open Data Portal
"""
import logging
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)

BASE_URL: str = os.getenv("CHILEAN_DATA_API_URL", "https://datos.gob.cl/api/3/action")
TIMEOUT: int = int(os.getenv("HTTP_API_TIMEOUT", "30"))


def _get(url: str, params: dict | None = None):
    """Method that execute a get call to an endpoint"""
    log.debug("GET %s params=%s", url, params)
    response = httpx.get(url, params=params or {}, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def download_bytes(url: str, max_bytes: int = 20 * 1024 * 1024) -> bytes:
    """
    Downloads the raw content of an URL with a size limit.
    Is used to download resource files (CSV/Excel) from an URL.
    """
    log.info("Descargando %s (limite %s bytes)", url, max_bytes)
    with httpx.stream("GET", url, timeout=TIMEOUT, follow_redirects=True) as response:
        response.raise_for_status()
        content = b""
        for chunk in response.iter_bytes():
            content += chunk
            # Safeguard: si se supera el limite, aborta.
            if len(content) > max_bytes:
                raise ValueError(
                    f"File size limit has been reached, max bytes {max_bytes}"
                )
        return content

"""Shared HTTP behavior: timeouts, user agent, and bounded retries."""

from collections.abc import Mapping
from typing import Any

import httpx

from .base import ProviderError


async def request_json(
    url: str,
    *,
    params: Mapping[str, Any],
    headers: Mapping[str, str] | None = None,
    timeout: float = 15.0,
) -> dict[str, Any]:
    """GET a JSON endpoint with a short, bounded retry policy."""
    merged_headers = {"User-Agent": "OpenLongevity/0.2.0 (research infrastructure)"}
    if headers:
        merged_headers.update(headers)
    for attempt in range(2):
        try:
            async with httpx.AsyncClient(timeout=timeout, follow_redirects=False) as client:
                response = await client.get(url, params=params, headers=merged_headers)
                response.raise_for_status()
                payload = response.json()
                if not isinstance(payload, dict):
                    raise ProviderError("provider returned a non-object JSON payload")
                return payload
        except (httpx.HTTPError, ValueError) as exc:
            if attempt == 1:
                raise ProviderError(f"provider request failed: {url}") from exc
    raise ProviderError("provider request failed")

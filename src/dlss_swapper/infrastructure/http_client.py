import hashlib
import logging
import urllib.request
from pathlib import Path

log = logging.getLogger("dlss_swapper.infra.http")


class ManifestDownloader:
    """Small wrapper around urllib for fetching manifest + package blobs."""

    def __init__(self, user_agent: str = "dlss-swapper/0.9") -> None:
        self.user_agent = user_agent

    def fetch(self, url: str) -> bytes:
        req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        with urllib.request.urlopen(req, timeout=20) as resp:  # noqa: S310
            return resp.read()

    def download(self, url: str, dest: Path, expected_sha256: str | None = None) -> Path:
        body = self.fetch(url)
        if expected_sha256 and hashlib.sha256(body).hexdigest() != expected_sha256:
            raise ValueError(f"sha256 mismatch for {url}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(body)
        log.info("downloaded %s (%d bytes)", url, len(body))
        return dest
import logging
from pathlib import Path

log = logging.getLogger("dlss_swapper.infra.winver")


def read_file_version(path: Path) -> str | None:
    """Reads the PE FileVersion resource on Windows; returns None elsewhere."""
    try:
        import ctypes
        from ctypes import wintypes
    except ImportError:
        return None

    size = ctypes.windll.version.GetFileVersionInfoSizeW(str(path), None)
    if not size:
        return None
    buffer = ctypes.create_string_buffer(size)
    if not ctypes.windll.version.GetFileVersionInfoW(str(path), 0, size, buffer):
        return None
    ptr = ctypes.c_void_p()
    length = wintypes.UINT()
    if not ctypes.windll.version.VerQueryValueW(
        buffer, r"\VarFileInfo\Translation", ctypes.byref(ptr), ctypes.byref(length)
    ):
        return None
    return None  # full VS_FIXEDFILEINFO parsing lives in the cpp helper
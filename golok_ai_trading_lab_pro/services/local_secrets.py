"""Windows DPAPI vault envelopes bound to the Odoo worker's user and purpose."""

import base64
import ctypes
import sys
from ctypes import wintypes


class VaultError(ValueError):
    pass


class _Blob(ctypes.Structure):
    _fields_ = [("size", wintypes.DWORD), ("data", ctypes.POINTER(ctypes.c_ubyte))]


def _transform(data, scope, *, decrypt):
    if sys.platform != "win32":
        raise VaultError("The Windows worker credential vault is unavailable.")
    crypt = ctypes.WinDLL("crypt32", use_last_error=True)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.LocalFree.argtypes = [ctypes.c_void_p]
    kernel.LocalFree.restype = ctypes.c_void_p
    content = (ctypes.c_ubyte * len(data)).from_buffer_copy(data)
    extra = (ctypes.c_ubyte * len(scope)).from_buffer_copy(scope)
    raw, entropy, output = _Blob(len(data), content), _Blob(len(scope), extra), _Blob()
    operation = crypt.CryptUnprotectData if decrypt else crypt.CryptProtectData
    operation.argtypes = [ctypes.POINTER(_Blob), ctypes.c_void_p, ctypes.POINTER(_Blob),
                          ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(_Blob)]
    operation.restype = wintypes.BOOL
    try:
        if not operation(ctypes.byref(raw), None, ctypes.byref(entropy), None, None, 1, ctypes.byref(output)):
            raise VaultError("The Windows worker credential vault is unavailable.")
        return ctypes.string_at(output.data, output.size)
    finally:
        ctypes.memset(content, 0, len(data))
        if output.data:
            ctypes.memset(output.data, 0, output.size)
            kernel.LocalFree(output.data)


def seal(value, scope):
    return base64.b64encode(_transform(value.encode("ascii"), scope, decrypt=False)).decode("ascii")


def open_secret(envelope, scope):
    try:
        return _transform(base64.b64decode(envelope, validate=True), scope, decrypt=True).decode("ascii")
    except (ValueError, UnicodeError):
        raise VaultError("The Windows worker cannot open this credential.") from None

"""Bounded, single-session NSE CM legacy Bhavcopy reader."""

import csv
import hashlib
import io
import re
from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal
from zipfile import BadZipFile, ZIP_DEFLATED, ZIP_STORED, ZipFile
from zlib import error as DeflateError

from . import market_data

LIMIT = 2 * 1024 * 1024
COLUMNS = "SYMBOL SERIES OPEN HIGH LOW CLOSE LAST PREVCLOSE TOTTRDQTY TOTTRDVAL TIMESTAMP TOTALTRADES ISIN".split()


@dataclass(frozen=True)
class DailyRow:
    symbol: str
    isin: str
    day: date
    opening: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int


def read(raw, day, *, today):
    if not isinstance(raw, bytes) or not 0 < len(raw) <= LIMIT or type(day) is not date or day > today:
        raise ValueError("Invalid historical date or file size.")
    digest = hashlib.sha256(raw).hexdigest()
    if raw.startswith(b"PK"):
        try:
            with ZipFile(io.BytesIO(raw)) as archive:
                members = archive.infolist()
                if len(members) != 1:
                    raise ValueError("Expected exactly one CSV member.")
                member = members[0]
                if (not re.fullmatch(r"[A-Za-z0-9_-]{1,120}\.csv", member.filename, re.I)
                        or member.file_size > LIMIT or member.file_size > 100 * max(1, member.compress_size)
                        or member.flag_bits & 1 or member.compress_type not in (ZIP_DEFLATED, ZIP_STORED)):
                    raise ValueError("Unsupported CSV archive member.")
                with archive.open(member) as stream:
                    raw = stream.read(LIMIT + 1)
        except (BadZipFile, OSError, EOFError, RuntimeError, DeflateError) as exc:
            raise ValueError("Invalid CSV archive.") from exc
    if len(raw) > LIMIT:
        raise ValueError("Uncompressed CSV exceeds limit.")
    rows = csv.reader(io.StringIO(raw.decode("utf-8-sig"), newline=""), strict=True)
    try:
        header = next(rows, [])
        if header not in (COLUMNS, COLUMNS + [""]):
            raise ValueError("Unsupported Bhavcopy schema.")
        result = {}
        for number, values in enumerate(rows, 2):
            if number > 10001 or len(values) != len(header) or (header[-1] == "" and values[-1]):
                raise ValueError("Invalid row width or count.")
            row = dict(zip(header, values))
            if datetime.strptime(row["TIMESTAMP"], "%d-%b-%Y").date() != day:
                raise ValueError("File contains a different trading date.")
            if row["SERIES"] != "EQ":
                continue
            symbol, isin = row["SYMBOL"], row["ISIN"]
            if (not re.fullmatch(r"[A-Z0-9][A-Z0-9&._-]{0,30}", symbol)
                    or not re.fullmatch(r"IN[A-Z0-9]{9}[0-9]", isin) or symbol in result):
                raise ValueError("Invalid or duplicate EQ identity.")
            bar = market_data.parse_bar(f"{day}T00:00:00Z", *(row[key] for key in ("OPEN", "HIGH", "LOW", "CLOSE", "TOTTRDQTY")),
                                        as_of=datetime.max.replace(tzinfo=timezone.utc))
            result[symbol] = DailyRow(symbol, isin, day, bar.open, bar.high, bar.low, bar.close, bar.volume)
    except csv.Error as exc:
        raise ValueError("Malformed CSV.") from exc
    if not result:
        raise ValueError("No EQ observations.")
    return digest, result

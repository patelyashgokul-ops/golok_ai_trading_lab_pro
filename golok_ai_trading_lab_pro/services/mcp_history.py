"""Pinned MCP handshake and tool schema for an injected historical fixture transport."""

import json
from datetime import date

VERSION = "2025-06-18"
SCHEMA = {"type": "object", "properties": {"date": {"type": "string"}},
          "required": ["date"], "additionalProperties": False}


def query_fixture(transport, day):
    if type(day) is not date:
        raise ValueError("Supply one fixture session date.")

    def request(number, method, params):
        raw = transport({"jsonrpc": "2.0", "id": number, "method": method, "params": params}, timeout=5)
        if not isinstance(raw, bytes) or len(raw) > 64 * 1024:
            raise ValueError("Invalid or oversized MCP reply.")
        message = json.loads(raw)
        if (not isinstance(message, dict) or message.get("jsonrpc") != "2.0"
                or type(message.get("id")) is not int or message["id"] != number or "error" in message
                or not isinstance(message.get("result"), dict)):
            raise ValueError("Invalid MCP response envelope.")
        return message["result"]

    hello = request(1, "initialize", {"protocolVersion": VERSION, "capabilities": {},
                                     "clientInfo": {"name": "golok-fixture", "version": "1"}})
    capabilities = hello.get("capabilities")
    if (hello.get("protocolVersion") != VERSION or not isinstance(capabilities, dict)
            or not isinstance(capabilities.get("tools"), dict)):
        raise ValueError("Unsupported MCP session.")
    transport({"jsonrpc": "2.0", "method": "notifications/initialized"}, timeout=5)
    listing = request(2, "tools/list", {})
    tools = listing.get("tools")
    if not isinstance(tools, list) or len(tools) > 32 or listing.get("nextCursor"):
        raise ValueError("Unsupported fixture tool inventory.")
    matched = [tool for tool in tools if isinstance(tool, dict) and tool.get("name") == "fixture_session"]
    if len(matched) != 1 or matched[0].get("inputSchema") != SCHEMA:
        raise ValueError("Fixture tool schema mismatch.")
    answer = request(3, "tools/call", {"name": "fixture_session", "arguments": {"date": day.isoformat()}})
    content = answer.get("structuredContent")
    if (answer.get("isError", False) is not False or not isinstance(content, dict)
            or content.get("date") != day.isoformat() or type(content.get("count")) is not int
            or not 0 <= content["count"] <= 10000):
        raise ValueError("Invalid historical fixture result.")
    return {"date": day, "count": content["count"], "origin": "synthetic"}

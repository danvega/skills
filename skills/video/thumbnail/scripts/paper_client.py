#!/usr/bin/env python3
"""Minimal MCP-over-HTTP client for the local Paper desktop server."""
import json, sys, urllib.request

URL = "http://127.0.0.1:29979/mcp"
SESSION_FILE = "/tmp/paper_session_id"

def _post(payload, session=None, timeout=60):
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json",
                 "Accept": "application/json, text/event-stream"})
    if session:
        req.add_header("mcp-session-id", session)
    resp = urllib.request.urlopen(req, timeout=timeout)
    sid = resp.headers.get("mcp-session-id")
    body = resp.read().decode()
    data = None
    for line in body.splitlines():
        if line.startswith("data: "):
            data = json.loads(line[6:])
    if data is None and body.strip():
        data = json.loads(body)
    return data, sid

def ensure_session():
    try:
        with open(SESSION_FILE) as f:
            return f.read().strip()
    except FileNotFoundError:
        pass
    data, sid = _post({"jsonrpc": "2.0", "id": 0, "method": "initialize",
        "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                   "clientInfo": {"name": "claude-code", "version": "1.0"}}})
    _post({"jsonrpc": "2.0", "method": "notifications/initialized"}, session=sid)
    with open(SESSION_FILE, "w") as f:
        f.write(sid)
    return sid

def call(tool, args=None, timeout=120):
    sid = ensure_session()
    data, _ = _post({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {"name": tool, "arguments": args or {}}}, session=sid, timeout=timeout)
    if data is None:
        return ""
    if "error" in data:
        return "RPC-ERROR: " + json.dumps(data["error"])
    out = []
    for c in data.get("result", {}).get("content", []):
        if c.get("type") == "text":
            out.append(c["text"])
        elif c.get("type") == "image":
            out.append("[image: %d b64 chars]" % len(c.get("data", "")))
    if data.get("result", {}).get("isError"):
        out.insert(0, "TOOL-ERROR:")
    return "\n".join(out)

if __name__ == "__main__":
    tool = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    print(call(tool, args))

#!/usr/bin/env python3
"""Minimal MCP-over-HTTP client for the remote Figma MCP server.
Auth: reuses the OAuth token Claude Code stored in the macOS keychain."""
import json, subprocess, sys, urllib.request

URL = "https://mcp.figma.com/mcp"
SESSION_FILE = "/tmp/figma_mcp_session"

def _token():
    r = subprocess.run(["security", "find-generic-password", "-s", "Claude Code-credentials", "-w"],
                       capture_output=True, text=True)
    creds = json.loads(r.stdout.strip())
    def find(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if "figma" in k.lower() and isinstance(v, dict):
                    for tk in ("accessToken", "access_token"):
                        if tk in v: return v[tk]
                r2 = find(v)
                if r2: return r2
        elif isinstance(o, list):
            for v in o:
                r2 = find(v)
                if r2: return r2
    return find(creds)

TOKEN = _token()

def _post(payload, session=None, timeout=120):
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json",
                 "Accept": "application/json, text/event-stream",
                 "Authorization": "Bearer " + TOKEN})
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
            sid = f.read().strip()
            if sid: return sid
    except FileNotFoundError:
        pass
    data, sid = _post({"jsonrpc": "2.0", "id": 0, "method": "initialize",
        "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                   "clientInfo": {"name": "claude-code", "version": "1.0"}}})
    _post({"jsonrpc": "2.0", "method": "notifications/initialized"}, session=sid)
    with open(SESSION_FILE, "w") as f:
        f.write(sid or "")
    return sid

def call(tool, args=None, timeout=300):
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
            out.append("IMAGE-B64:" + c.get("data", ""))
    if data.get("result", {}).get("isError"):
        out.insert(0, "TOOL-ERROR:")
    return "\n".join(out)

def schema(names):
    sid = ensure_session()
    data, _ = _post({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, session=sid)
    for t in data.get("result", {}).get("tools", []):
        if t["name"] in names:
            print("###", t["name"])
            print((t.get("description") or "")[:600])
            print(json.dumps(t.get("inputSchema", {}), indent=1)[:2200])
            print()

if __name__ == "__main__":
    tool = sys.argv[1]
    if tool == "--schema":
        schema(sys.argv[2].split(","))
    else:
        raw = sys.argv[2] if len(sys.argv) > 2 else "{}"
        if raw.startswith("@"):
            with open(raw[1:]) as f:
                raw = f.read()
        print(call(tool, json.loads(raw)))

import httpx, os, base64, pathlib

APPIUM = os.getenv("APPIUM_SERVER", "http://appium:4723/wd/hub")
ADB_HOST = os.getenv("ADB_HOST", "blissvm")
ADB_PORT = os.getenv("ADB_PORT", "5555")

def _post(url, data=None):
    return httpx.post(url, json=data).json()

def click(selector):
    return _post(f"{APPIUM}/click", {"selector": selector})

def type_text(text, selector):
    return _post(f"{APPIUM}/type", {"selector": selector, "text": text})

def wait(selector, timeout=10):
    return _post(f"{APPIUM}/wait", {"selector": selector, "timeout": timeout})

def swipe(start, end, duration_ms=500):
    return _post(f"{APPIUM}/swipe", {"start": start, "end": end, "duration": duration_ms})

def adb_shell(cmd):
    return httpx.get(f"http://{ADB_HOST}:{ADB_PORT}/shell", params={"cmd": cmd}).text

def screenshot():
    raw = httpx.get(f"{APPIUM}/screenshot").text
    path = pathlib.Path("/logs") / "shot.png"
    path.write_bytes(base64.b64decode(raw))
    return str(path)

"""
Butterfly - Local-First Visual ML Application

Main entry point that starts the backend and opens the browser.
"""
import sys
import webbrowser
import time
from pathlib import Path
from threading import Thread

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.server import start_server


def open_browser(url: str, delay: float = 2.0):
    """Open browser after delay"""
    time.sleep(delay)
    print(f"🦋 Opening Butterfly in your browser...")
    webbrowser.open(url)


def main():
    """
    Main entry point for Butterfly.
    
    Starts:
    1. Backend server (FastAPI)
    2. Browser pointing to frontend
    """
    host = "127.0.0.1"
    port = 8000
    url = f"http://{host}:{port}"
    
    print("=" * 60)
    print("🦋 Butterfly - Local-First Visual ML Application")
    print("=" * 60)
    print()
    print(f"Backend server: {url}")
    print(f"Frontend: {url}/index.html")
    print()
    print("Press Ctrl+C to stop")
    print()
    
    # Open browser in background thread
    browser_thread = Thread(target=open_browser, args=(url,), daemon=True)
    browser_thread.start()
    
    # Start server (blocking)
    try:
        start_server(host=host, port=port)
    except KeyboardInterrupt:
        print("\n🦋 Butterfly stopped")
        sys.exit(0)


if __name__ == "__main__":
    main()

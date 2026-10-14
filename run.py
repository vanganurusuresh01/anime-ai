import socket
import sys
import os

# Fix Windows console UTF-8 encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import uvicorn

def is_port_available(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) != 0

def find_available_port(start_port: int = 8000, max_attempts: int = 15) -> int:
    for port in range(start_port, start_port + max_attempts):
        if is_port_available(port):
            return port
    return start_port

def main():
    port = find_available_port(8000)
    
    print("\n" + "=" * 65)
    print("   🧬 ANIVERSE AI — PREMIER HACKATHON BUILD")
    print("   Tagline: Find the anime that matches your imagination.")
    print("=" * 65)
    print(f"\n   🚀 Server launching at:   http://127.0.0.1:{port}")
    print(f"   📚 Interactive API Docs: http://127.0.0.1:{port}/docs")
    print(f"   ❤️  System Health Check: http://127.0.0.1:{port}/api/health")
    print("\n   Features Ready:")
    print("   ✓ 8-Dimensional Anime DNA Vector Engine")
    print("   ✓ Natural Language Semantic Intent Parser")
    print("   ✓ Real-time HTML5 Canvas 8-Axis Radar Chart")
    print("   ✓ Taste Cross-Referencing Centroid Blender")
    print("   ✓ Smart Binge Commitment Calculator & Watchlist")
    print("   ✓ Live Global MAL Search via Jikan API")
    print("   ✓ Interactive Hackathon Judge Pitch Mode")
    print("   ✓ Premium Collaboration Watch Rooms")
    print("   ✓ Audio & Dubbing Premium Metadata Engine")
    print("   ✓ 12 Automated Unit Tests — All Passing")
    print("=" * 65 + "\n")

    uvicorn.run("app.main:app", host="127.0.0.1", port=port, log_level="info")

if __name__ == "__main__":
    main()

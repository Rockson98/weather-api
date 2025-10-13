import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tianqi_webtool.server import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

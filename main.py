from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import psutil
import uvicorn

app = FastAPI()

@app.get("/api/stats")
def get_stats():
    return {
        "cpu_percent": psutil.cpu_percent(interval=None),
        "ram_percent": psutil.virtual_memory().percent
    }

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SysPulse Web Dashboard</title>
        <style>
            body { font-family: sans-serif; background: #0e1117; color: white; text-align: center; padding: 50px; }
            .card { background: #1c2130; padding: 20px; border-radius: 10px; display: inline-block; margin: 15px; width: 200px; }
            .stat { font-size: 2.5em; font-weight: bold; color: #39d353; margin-top: 10px; }
        </style>
    </head>
    <body>
        <h1>SysPulse Web Dashboard</h1>
        <div class="card">
            <h3>CPU Usage</h3>
            <div id="cpu" class="stat">0%</div>
        </div>
        <div class="card">
            <h3>RAM Usage</h3>
            <div id="ram" class="stat">0%</div>
        </div>
        <script>
            async function update() {
                try {
                    const res = await fetch('/api/stats');
                    const data = await res.json();
                    document.getElementById('cpu').innerText = data.cpu_percent + '%';
                    document.getElementById('ram').innerText = data.ram_percent + '%';
                } catch(e) {
                    console.error(e);
                }
            }
            setInterval(update, 1000);
            update();
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    # We use a single-process worker here to prevent experimental 3.14 multiprocessing crashes
    uvicorn.run(app, host="127.0.0.1", port=8000, workers=1)
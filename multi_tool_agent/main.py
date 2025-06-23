from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from shared.root_agent import run  # ✅ FIXED

load_dotenv()

app = FastAPI()

class CityInput(BaseModel):
    city: str

@app.post("/webhook")
async def handle_city_query(city_input: CityInput):
    city = city_input.city.strip()
    if not city:
        return {"error": "City name cannot be empty."}
    
    try:
        response = run(city)  # ✅ FIXED
        return {"response": str(response)}
    except Exception as e:
        return {"error": str(e)}

@app.get("/ui", response_class=HTMLResponse)
def serve_form():
    return """
    <html>
        <body>
            <h2>Test Agent via City Name</h2>
            <form action="/ask" method="post">
                <input name="city" type="text" size="40" placeholder="Enter city name" />
                <button type="submit">Submit</button>
            </form>
        </body>
    </html>
    """

@app.post("/ask")
async def handle_ui_form(request: Request):
    form = await request.form()
    city = form.get("city", "").strip()
    
    if not city:
        return HTMLResponse(content="<p>City name cannot be empty.</p><a href='/ui'>Back</a>", status_code=400)

    try:
        response = run(city)  # ✅ FIXED
        return HTMLResponse(content=f"<p><strong>Response:</strong><br>{response.replace(chr(10), '<br>')}</p><a href='/ui'>Back</a>")
    except Exception as e:
        return HTMLResponse(content=f"<p>Error: {str(e)}</p><a href='/ui'>Back</a>", status_code=500)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("multi_tool_agent.main:app", host="0.0.0.0", port=port)

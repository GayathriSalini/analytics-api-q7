import secrets
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

API_KEY = "ak_eghdesoh70o0eqrcfkrrp3gk"
EMAIL = "24f3000207@ds.study.iitm.ac.in"

app = FastAPI()

# "*" is allowed for this endpoint. The preflight for the X-API-Key header is handled here too.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analytics")
async def analytics(request: Request, x_api_key: Optional[str] = Header(None)):
    # Auth first, before reading the body
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="invalid or missing API key")

    try:
        body = await request.json()
        events = body.get("events", [])
        if not isinstance(events, list):
            raise ValueError
    except Exception:
        raise HTTPException(status_code=400, detail="invalid body")

    users = set()
    positive_totals = {}
    revenue = 0.0

    for e in events:
        user = e.get("user")
        amount = float(e.get("amount", 0) or 0)
        users.add(user)
        if amount > 0:
            revenue += amount
            positive_totals[user] = positive_totals.get(user, 0.0) + amount

    top_user = max(positive_totals, key=positive_totals.get) if positive_totals else None

    return {
        "email": EMAIL,
        "total_events": len(events),
        "unique_users": len(users),
        "revenue": revenue,
        "top_user": top_user,
    }


@app.get("/")
def root():
    return {"status": "ok"}

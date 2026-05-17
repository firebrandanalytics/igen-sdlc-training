"""
main.py — Mileage Logbook web application.

Three routes:
  GET  /          — list all trips
  GET  /trips/new — show the add-trip form
  POST /trips     — create a new trip and redirect to the list
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(title="Mileage Logbook", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def list_trips(request: Request):
    conn = db.get_connection()
    try:
        trips = db.get_all_trips(conn)
    finally:
        conn.close()
    return templates.TemplateResponse(
        request, "trips_list.html", {"trips": trips}
    )


@app.get("/trips/new", response_class=HTMLResponse)
def new_trip_form(request: Request):
    return templates.TemplateResponse(
        request, "trip_form.html", {"errors": []}
    )


@app.post("/trips")
def create_trip(
    request: Request,
    trip_date: str = Form(...),
    vehicle: str = Form(...),
    start_location: str = Form(...),
    end_location: str = Form(...),
    miles: str = Form(...),
):
    errors = []
    if not trip_date:
        errors.append("Trip date is required.")
    if not vehicle.strip():
        errors.append("Vehicle is required.")
    if not start_location.strip():
        errors.append("Start location is required.")
    if not end_location.strip():
        errors.append("End location is required.")
    try:
        miles_float = float(miles)
        if miles_float <= 0:
            errors.append("Miles must be greater than zero.")
    except (ValueError, TypeError):
        miles_float = None
        errors.append("Miles must be a number.")

    if errors:
        return templates.TemplateResponse(
            request,
            "trip_form.html",
            {
                "errors": errors,
                "values": {
                    "trip_date": trip_date,
                    "vehicle": vehicle,
                    "start_location": start_location,
                    "end_location": end_location,
                    "miles": miles,
                },
            },
            status_code=422,
        )

    conn = db.get_connection()
    try:
        db.create_trip(
            conn,
            trip_date=trip_date,
            vehicle=vehicle.strip(),
            start_location=start_location.strip(),
            end_location=end_location.strip(),
            miles=miles_float,
        )
    finally:
        conn.close()

    return RedirectResponse(url="/", status_code=303)

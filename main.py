import logging
import os

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from starlette.responses import PlainTextResponse

from UnikinoParser import parse_unikino, download_unikino_page
from Model import create_calendar

unifilm_kino_url = os.getenv("UNIFILM_KINO_URL")
app = FastAPI()

calendar = ""


@app.get("/", response_class=PlainTextResponse)
async def root():
    return calendar


@app.on_event("startup")
@repeat_every(seconds=5)  # day
def parse_page():
    html = download_unikino_page(unifilm_kino_url)
    if html is None:
        pass  # dummykalender mit Fehlermeldung erstellen?
    movie_events = parse_unikino(html)
    global calendar
    calendar = create_calendar(movie_events).to_ical()

    logging.info("updated calendar")

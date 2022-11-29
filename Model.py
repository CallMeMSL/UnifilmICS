import datetime
from uuid import uuid1

from icalendar import Event, Calendar
from pydantic import BaseModel


class MovieEvent(BaseModel):
    title: str
    start: datetime.datetime
    movie_duration: int  # in m
    ads_duration: int = 30
    movie_descriptions: list[str]
    infos: list[str]
    awards: list[str]
    room: str
    img_url: str
    geo_location: str

    @property
    def end(self):
        return (self.start
                + datetime.timedelta(minutes=self.ads_duration)
                + datetime.timedelta(minutes=self.movie_duration))

    @property
    def cal_description(self):
        md_merged = ' '.join(self.movie_descriptions)
        infos_merged = ' '.join(self.infos)
        awards_merged = ' '.join(self.awards)
        return f" {md_merged} {infos_merged} {awards_merged} Laufzeit: {self.movie_duration} Minuten."

    @property
    def event(self):
        event = Event()
        event.add('name', self.title)
        event.add('summary', f"{self.title} - Unifilm")
        event.add('description', self.cal_description)
        event.add('dtstart', self.start)
        event.add('dtend', self.end)
        event.add('uid', uuid1())
        event['geo'] = self.geo_location
        event.add('location', self.room)
        event.add('image', self.img_url)
        event.add('dtstamp', datetime.datetime.now())
        return event


def create_calendar(movie_events: list[MovieEvent]) -> Calendar:
    cal = Calendar()
    cal.add('prodid', '-//Unikino ICS Kalender - NICHT OFFIZIELL//CallMeMSL@github//EN')
    cal.add('version', '2.0')
    for me in movie_events:
        cal.add_component(me.event)
    return cal

import logging
import re
from datetime import datetime

import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from Model import MovieEvent


def download_unikino_page(url: str) -> str | None:
    ua = UserAgent()
    with httpx.Client(headers={'User-Agent': ua.random}) as client:
        r = client.get(url)
        if r.status_code != 200:
            logging.error(f"couldn't reach unifilm page. Status code {r.status_code}")
            return
        soup = BeautifulSoup(r.content, "html.parser")
        request_token = soup.find('input', {'name': 'REQUEST_TOKEN'}).attrs['value']
        r = client.post(url, cookies=r.cookies, data={  # accept cookies for location data
            'FORM_SUBMIT': 'auto_form_dsgvo',
            'REQUEST_TOKEN': request_token,
            'google_analytics': '',
            'dlh_googlemaps': ['', 'ok'],
            'facebook': '',
            'cookie': ['', 'ok']})
        r = client.get(url, cookies=r.cookies)
        return r.text


def parse_unikino(html: str) -> list[MovieEvent] | None:
    soup = BeautifulSoup(html, "html.parser")
    film_section = soup.find("div", class_="anzeigebereich-film")
    if film_section is None:
        logging.error("Couldn't parse film section page")
        return
    movies = film_section.find_all("div", class_="film-showcase")
    if len(movies) == 0:
        logging.error("Couldn't find entries in film section")
        return
    geo_loc = get_unikino_lat_long(html)
    movie_events = []
    for movie in movies:
        name = movie.find("span", class_="").text
        date = movie.find("span", class_="film-info-text datum").text
        time = movie.find("span", class_="film-info-text uhrzeit").text
        room = movie.find("span", class_="film-info-text raum").text
        descriptions = [e.text for e in movie.find_all("p") if e.text != ""]
        info_html = movie.find("ul", class_="film-info-filmdaten")
        infos = [e.text for e in info_html.find_all("li", class_="vertical-divider") if e.text != ""]
        duration = info_html.find("li", class_="").text
        awards = [e.text for e in movie.find_all("li", class_="film-nominierungen") if e.text != ""]
        img_url = f"https://www.unifilm.de/{movie.find('img').attrs['src']}"
        date_time_iso = f"{'-'.join(date.split(' ')[1].split('.')[::-1])}T{time}:00+01:00"
        movie_events.append(MovieEvent(
            title=name,
            start=datetime.fromisoformat(date_time_iso),
            movie_duration=int(duration.split(' ')[0]),
            movie_descriptions=descriptions,
            infos=infos,
            awards=awards,
            room=room,
            img_url=img_url,
            geo_location=geo_loc
        ))
    return movie_events


def get_unikino_lat_long(html: str) -> str:
    result = re.search(r"gmap5\.center=new google\.maps\.LatLng\((\d+\.\d+),(\d+\.\d+)", html)
    if result is None:
        logging.error("Location couldn't be extracted")
    return f"{result.group(1)};{result.group(2)};"
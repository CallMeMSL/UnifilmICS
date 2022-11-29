# UnifilmICS - Infos zu deinem Unifilmkino direkt im Kalender

Dieses Programm stellt einen Server bereit,
mit dem Kalendereinträge im iCalender Format, für ein Kino des Betreibers [Unifilm](https://www.unifilm.de/startseite) deiner Wahl, generiert und abgerufen werden können.

Der Kalender aktualisiert sich täglich.

## Benutzung

Installiere Python 3.10 und die nötigen Abhänigkeiten in der ```requirements.txt``` mittels pip.

Nun muss das Kino per Umgebungvariable festgelegt werden.
Setze hierfür ```UNIFILM_KINO_URL``` mit der URL deines gewünschten Kinos.

Beispiel für Bielefeld:
```export UNIFILM_KINO_URL="https://www.unifilm.de/studentenkinos/Bielefeld_Uni"```

Anschließend starte den Server mit 
```uvicorn main:app```.

Lokal ist der Kalender nun unter ```http://localhost:8000``` verfügbar.

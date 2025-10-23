---
name: calendar
description: Workflow-Anleitung für Kalender-Operationen. Verwende bei Termine abrufen, Termine erstellen, Termine löschen, Kalender anzeigen, Events checken, Meeting planen, Terminkonflikt prüfen, diese Woche anzeigen, heute, morgen, nächste Woche. Kritisch für korrekte Kalender-Auswahl (Unternehmenskalender vs. Mitarbeiter-Kalender) und Konflikt-Vermeidung.
---

# Calendar Workflow

## Zwei Kalender

- **Unternehmenskalender**: Tools **ohne** `_personal` (kontakt@bold-projekte.com)
- **Mitarbeiter-Kalender**: Tools **mit** `_personal` (franke@bold-projekte.com)

## Termine abrufen

**STANDARD**: Immer **beide** Kalender abfragen, außer User nennt explizit einen.

```
1. searchEvent (Unternehmenskalender)
2. searchEvent_personal (Mitarbeiter-Kalender)
3. Ergebnisse getrennt anzeigen
```

## Termine erstellen

**PFLICHT vor Erstellung:**

1. **Konflikt-Prüfung**: Beide Kalender im Zeitraum abrufen, Überschneidungen melden
2. **Kalender-Auswahl**: Wenn nicht explizit genannt → User fragen welcher Kalender
3. Korrekte Tool-Version verwenden (`_personal` oder ohne)

**Zeitzonenbehandlung:**

- **Format**: `YYYY-MM-DDTHH:MM:SS` (OHNE Zeitzone-Offset wie +01:00 oder +02:00)
- Google Calendar verwendet dann automatisch die Kalender-Zeitzone (Europe/Berlin)
- **Beispiel**: `2025-10-23T18:00:00` für 18:00 Uhr
- **NICHT**: `2025-10-23T18:00:00+01:00` (führt zu Fehlern bei Sommerzeit/Winterzeit)

## Kern-Prinzipien

1. Beide Kalender prüfen (außer explizit anders)
2. Konflikt-Prüfung ist Pflicht vor Erstellung
3. Bei Unklarheit nachfragen welcher Kalender

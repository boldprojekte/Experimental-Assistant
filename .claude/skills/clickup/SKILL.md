---
name: ClickUp
description: Workflow-Anleitung für ClickUp-Operationen. Verwende bei Aufgaben erstellen, Aufgaben bearbeiten, Aufgaben suchen, alle Aufgaben in Projekt anzeigen, Kontakte verwalten, Dokumente erstellen, Listen organisieren, Ordner erstellen, Zeiterfassung starten, oder Zeiterfassung stoppen. Kritisch für korrekte Such-Strategie-Auswahl und Workspace-Struktur-Verständnis.
---

# ClickUp Workflow

Workflow-Anleitung für ClickUp-Operationen mit Fokus auf korrekte Such-Strategie und Workspace-Struktur.

## Workspace-Struktur

**KRITISCH** für die Bestimmung, wo Elemente erstellt oder gefunden werden.

### Spaces Übersicht

- **Personal List** (ID: `901208069739`) - Private Aufgaben. **VERSTECKTER** Space, nicht in Hierarchie-Abfragen sichtbar. Für alle persönlichen/privaten Aufgaben verwenden.
- **Privat** - Nur private Notizen und Dokumente (NICHT für Aufgaben!)
- **Operations** - Architekturprojekte (Format: Projektnummer + Ort + Straße)
- **Gut Gewohnt** - Bauträger-Projektentwicklung (mit Robert Crummenerl)
- **Backoffice** - Buchhaltung, Einkäufe, **Kontakte**, Urlaubskalender
- **Process Library** - ClickUp-Vorlagen (Projektordner mit vorkonfigurierten Aufgaben)
- **Growth** - Wachstums-Aufgaben/Dokumente (Webseite, Marketing, Akquise)
- **baumeet.ing** - Bauprotokoll-SaaS-Plattform

## Such-Strategie

**KRITISCH**: Wähle den korrekten Such-Ansatz basierend auf der Anfrage.

### Kontextbasierte Suche (alle Aufgaben in Projekt/Liste/Space)

Verwende wenn User nach "alle Aufgaben in X" oder "zeige Projekt Y Aufgaben" fragt:

1. Verwende `clickup_get_workspace_hierarchy` um Listen/Ordner-ID zu identifizieren
2. Verwende `clickup_get_workspace_tasks` mit `list_ids` oder `folder_ids`
3. **NIEMALS `clickup_search` verwenden** - durchsucht nur Titel, verpasst die meisten Aufgaben

**Beispiele:**
- "Zeige alle Aufgaben im Prozessionsweg" → `clickup_get_workspace_tasks` mit `list_ids`
- "Was gibt es in Gut Gewohnt zu tun?" → `clickup_get_workspace_tasks` mit `space_ids`

### Keyword-Suche (spezifische Aufgabe finden)

Verwende beim Suchen einer spezifischen Aufgabe nach Name/Keyword:

1. Verwende `clickup_search` mit Suchbegriffen
2. Identifiziere korrekte Aufgabe aus Ergebnissen

**Beispiele:**
- "Finde Aufgabe 'Kaya anrufen'" → `clickup_search` mit Keywords
- "Wo ist die Rechnung für Lieferant X?" → `clickup_search`

### Suchen vor Ändern

Suche immer nach existierendem Element vor Update/Bearbeitung:
- Verwende `clickup_search` für Aufgaben nach Name
- Verifiziere Existenz vor Update-Tool-Aufruf

## Aufgaben-Operationen

### Standard-Einstellungen

Anwenden außer explizit anders angegeben:
- **Priorität**: normal
- **Assignee**: "me" (der User)
- **Due Date**: nur wenn erwähnt
- **Tags**: nur wenn erwähnt
- **Custom Fields**: nur wenn erwähnt

### Aufgabe erstellen

1. Ziel-Liste aus Workspace-Struktur identifizieren
2. Verwende `clickup_create_task` mit `list_id` und `name`
3. Wende Defaults an, optionale Felder nur wenn spezifiziert
4. Gib Link aus: `https://app.clickup.com/t/{task_id}`

### Bulk-Operationen

Für mehrere Aufgaben in derselben Liste:
- Verwende `clickup_create_bulk_tasks` (effizienter als mehrere Einzelaufrufe)

## Weitere Operationen

### Kontakte
- Ort: Backoffice Space
- Erst mit `clickup_search` suchen

### Dokumente
- Ort basierend auf Kontext:
  - Privat → Privat Space
  - Projekt → Operations Space (spezifisches Projekt)
  - Vorlagen → Process Library
  - Wachstum → Growth Space
  - baumeet.ing → baumeet.ing Space
- Dokument-Link nach Erstellung bereitstellen

### Zeiterfassung
- Start: `clickup_start_time_tracking`
- Stop: `clickup_stop_time_tracking`
- Manuell: `clickup_add_time_entry`

## Kern-Prinzipien

1. **Korrekte Such-Strategie wählen** - Kontextbasiert vs. Keyword-Suche
2. **Geschwindigkeit vor Perfektion** - Defaults verwenden, nicht zu viel nachfragen
3. **Struktur-Bewusstsein** - Workspace-Struktur kennen vor Aktion
4. **Immer verlinken** - Direkte ClickUp-Links zu erstellten/geänderten Elementen bereitstellen
5. **Personal List für Privates** - ID `901208069739` für persönliche Aufgaben

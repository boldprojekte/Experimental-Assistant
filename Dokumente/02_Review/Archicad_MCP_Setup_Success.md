# Archicad MCP Setup - Erfolgreich abgeschlossen

**Datum:** 2025-10-24
**Status:** ✅ Verbunden und einsatzbereit

## Problem & Lösung

### Ausgangssituation
- Archicad 29 mit Tapir Add-On installiert
- MCP-Server installiert, aber Verbindung schlug fehl
- Fehlermeldung: "Failed to reconnect to archicad"

### Diagnose
1. ✅ Archicad läuft auf Port **19723**
2. ✅ JSON Interface funktioniert (getestet mit direktem API-Call)
3. ✅ Tapir Add-On ist aktiv
4. ❌ MCP-Server hatte keine Port-Konfiguration

### Root Cause
Der Archicad MCP-Server war im **local scope** (`~/.claude.json`) konfiguriert, aber ohne expliziten Port-Parameter. Der Auto-Discovery-Mechanismus funktionierte nicht.

### Lösung
```bash
# Alten Server entfernen
claude mcp remove --scope local archicad

# Neu hinzufügen mit Port-Parameter
claude mcp add --scope local --transport stdio archicad -- \
  uvx --from tapir-archicad-mcp archicad-server --port 19723
```

## Konfiguration

**Konfigurationsdatei:** `/Users/j.franke/.claude.json` (local scope)

**Server-Details:**
- **Name:** archicad
- **Transport:** stdio
- **Command:** `uvx --from tapir-archicad-mcp archicad-server --port 19723`
- **Port:** 19723 (Archicad JSON API)

## Archicad Setup

**Version:** Archicad 29 Build 3000
**Sprache:** Deutsch (GER)
**Add-Ons:**
- ✅ Tapir Add-On (installiert und aktiv)
- ✅ JSON Command Interface (eingebaut in Archicad 29)

## Verfügbare Tools

Der Tapir MCP-Server bietet **137 dynamisch generierte Tools** aus:
- Tapir Community API
- Official Archicad JSON API

**Semantic Tool Discovery:** Verwende natürliche Sprache, um Tools zu finden (z.B. "create a wall" statt exakte API-Namen).

## Nächste Schritte

1. **Instanzen entdecken:** Archicad-Instanzen mit ihren Port-Nummern auflisten
2. **Projekt-Informationen abfragen:** Layer, Views, Stories, etc.
3. **Elemente erstellen/bearbeiten:** Wände, Türen, Fenster, etc.
4. **Daten exportieren:** Projektdaten, Mengen, Pläne

## Wichtige Hinweise

- **Immer Archicad-Skill laden:** Vor MCP-Tool-Aufrufen die Skill laden (`archicad`)
- **Port-Spezifisch arbeiten:** Bei mehreren Instanzen immer Port angeben
- **Natürliche Sprache verwenden:** Für Tool-Discovery beschreibend formulieren
- **Lokal & Privat:** Alle Operationen laufen lokal, keine Cloud-Verbindung

## Fehlerbehebung

Falls die Verbindung erneut abbricht:
1. Prüfen, ob Archicad noch läuft: `lsof -i :19723`
2. MCP-Status prüfen: `/mcp` in Claude Code
3. Logs prüfen: `~/.tapir_mcp/logs/tapir_mcp_server.log`
4. Archicad neu starten bei Bedarf

---

**Setup durchgeführt von:** Claude Code
**Zeitaufwand:** ~30 Minuten (Diagnose + Lösung)

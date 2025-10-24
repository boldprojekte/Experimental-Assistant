# Archicad Integration Setup

Dokumentation zur Integration von Archicad-Steuerung in Ihren AI-Assistenten.

## Was wurde installiert?

### 1. Archicad MCP Server

**Repository**: [tapir-archicad-MCP](https://github.com/SzamosiMate/tapir-archicad-MCP)

Der MCP Server verbindet Claude Code mit laufenden Archicad-Instanzen und bietet:
- **137 Tools** aus Tapir API + offizieller Archicad JSON API
- **Semantische Suche** - Finden Sie Tools per natürlicher Sprache
- **Multi-Instanz-Unterstützung** - Steuern Sie mehrere Archicad-Projekte gleichzeitig
- **Offline & Privat** - Alle Daten bleiben auf Ihrem Computer

### 2. Konfigurationsdateien

**`.mcp.json`** (neu erstellt)
```json
{
  "mcpServers": {
    "archicad": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--from",
        "tapir-archicad-mcp",
        "archicad-server"
      ],
      "env": {}
    }
  }
}
```

**`.claude/skills/archicad/SKILL.md`** (neu erstellt)
- Vollständige Workflow-Anleitung
- Best Practices für Archicad-Steuerung
- Multi-Instanz-Management
- Fehlerbehebung

**`.claude/settings.local.json`** (aktualisiert)
- `Skill(archicad)` zu den erlaubten Skills hinzugefügt

**`CLAUDE.md`** (aktualisiert)
- Archicad zur Liste der Integrationen hinzugefügt
- Skills-Routing-Tabelle erweitert
- Archicad-spezifische Hinweise

## Was Sie noch tun müssen

### 1. Tapir Add-On aktivieren ✅ INSTALLIERT

Das Tapir Add-On wurde erfolgreich installiert unter:
```
/Applications/Graphisoft/Archicad 29/Add-Ons/TapirAddOn_AC29_Mac.bundle
```

**Nächste Schritte zur Aktivierung:**

1. **Starten Sie Archicad 29**
2. **Aktivieren Sie das Add-On:**
   - Gehen Sie zu **Optionen → Add-On Manager**
   - Sie sollten **TapirAddOn** in der Liste sehen
   - Stellen Sie sicher, dass es **aktiviert** ist (Häkchen gesetzt)
   - Falls nicht sichtbar, klicken Sie auf **"Liste verfügbarer Add-Ons bearbeiten"** → **"Hinzufügen"**
   - Navigieren Sie zu `/Applications/Graphisoft/Archicad 29/Add-Ons/TapirAddOn_AC29_Mac.bundle`
   - Klicken Sie **"OK"**
3. **Starten Sie Archicad neu**

**Überprüfung der Installation:**
Nach dem Neustart sollte das Tapir Add-On automatisch geladen werden. Sie können dies überprüfen, indem Sie:
- Zu **Optionen → Add-On Manager** gehen
- **TapirAddOn** in der Liste der geladenen Add-Ons sehen
- Status: **Geladen** ✓

### 2. Archicad API aktivieren

Stellen Sie sicher, dass die Archicad JSON API aktiviert ist:

1. Öffnen Sie Archicad
2. Gehen Sie zu **Optionen → Add-On Manager**
3. Aktivieren Sie **JSON Command Interface**
4. Starten Sie Archicad neu, wenn erforderlich

### 3. Claude Code neu starten

Damit die neue MCP-Server-Konfiguration geladen wird:

**Wichtig:** Schließen Sie diese Claude Code Session und starten Sie eine neue Session.

Die MCP-Konfiguration wird nur beim Start geladen.

## Erste Schritte

### Test der Installation

1. **Starten Sie Archicad** mit einem geöffneten Projekt
2. **In Claude Code** fragen Sie:
   ```
   Entdecke aktive Archicad-Instanzen
   ```
3. Claude sollte die laufenden Instanzen mit Port-Nummern anzeigen

### Beispiel-Workflows

**Projekt-Informationen abfragen:**
```
Zeige mir alle Ebenen im Archicad-Projekt auf Port 19723
```

**Elemente erstellen:**
```
Erstelle eine Wand mit 5m Länge und 3m Höhe im Projekt auf Port 19723
```

**Projekt-Daten exportieren:**
```
Exportiere alle Fenster mit ihren Eigenschaften aus dem Projekt
```

## Wichtige Hinweise

### Semantische Tool-Suche

Sie müssen **KEINE** exakten Tool-Namen kennen. Beschreiben Sie einfach, was Sie tun möchten:

❌ Nicht: "Verwende das Tool `archicad_create_wall_v2_json`"
✅ Besser: "Erstelle eine Wand in Archicad"

Der Server findet automatisch das passende Tool.

### Multi-Instanz-Management

Wenn mehrere Archicad-Instanzen laufen:
1. Claude wird Sie fragen, welche Instanz Sie verwenden möchten
2. Jede Instanz hat eine eindeutige Port-Nummer
3. Referenzieren Sie die Port-Nummer in Ihren Anfragen

### Alpha-Software

Der Archicad MCP Server ist in der **Alpha-Phase**:
- Erwarten Sie gelegentliche Probleme
- Speichern Sie Ihr Archicad-Projekt regelmäßig
- Testen Sie komplexe Operationen zuerst an Testprojekten
- Melden Sie Bugs an das [GitHub Repository](https://github.com/SzamosiMate/tapir-archicad-MCP/issues)

## Fehlerbehebung

### "Keine Instanzen gefunden"

**Lösung:**
- Überprüfen Sie, ob Archicad läuft
- Stellen Sie sicher, dass ein Projekt geöffnet ist
- Prüfen Sie, ob Tapir Add-On geladen ist
- Versuchen Sie, Archicad neu zu starten

### "Tool nicht gefunden"

**Lösung:**
- Formulieren Sie Ihre Anfrage anders
- Seien Sie spezifischer bei der Beschreibung
- Konsultieren Sie die Archicad API-Dokumentation
- Prüfen Sie, ob Tapir Add-On installiert ist

### "Verbindung verloren"

**Lösung:**
- Prüfen Sie, ob Archicad noch läuft
- Führen Sie erneut die Instanz-Erkennung durch
- Überprüfen Sie, ob sich die Port-Nummer geändert hat

## Integration mit bestehendem Workflow

### Dokumentation von Archicad-Änderungen

Nach Archicad-Operationen:
- Dokumentieren Sie Änderungen in `Dokumente/01_in Arbeit/`
- Erstellen Sie Task-Listen in `Aufgaben/` für komplexe Workflows
- Nutzen Sie ClickUp für Projekt-Tracking

### Kombination mit anderen Tools

Archicad funktioniert gut mit:
- **Browser** - Screenshots von Archicad für Dokumentation
- **ClickUp** - Tracking von Design-Aufgaben
- **Scripts** - Export/Konvertierung von Archicad-Daten
- **RAG** - Indexierung von Archicad-Dokumentation

## Installation Details

### Heruntergeladene Dateien

**Tapir Add-On für Archicad 29 (macOS):**
- **Quelle**: [ENZYME-APD/tapir-archicad-automation v1.2.3](https://github.com/ENZYME-APD/tapir-archicad-automation/releases/tag/1.2.3)
- **Datei**: `TapirAddOn_AC29_Mac.zip` (987 KB)
- **Download-Location**: `~/Downloads/Archicad-Addons/`
- **Extrahiert**: `TapirAddOn_AC29_Mac.bundle`
- **Installiert**: `/Applications/Graphisoft/Archicad 29/Add-Ons/TapirAddOn_AC29_Mac.bundle`
- **Datum**: 24. Oktober 2025

### Unterstützte Archicad-Versionen

Tapir 1.2.3 unterstützt:
- Archicad 25, 26, 27, 28, **29** ✓
- Windows und macOS

## Nächste Schritte

1. ✅ **Tapir Add-On installiert**
2. ⏳ **Tapir Add-On in Archicad aktivieren** (siehe Anleitung oben)
3. ⏳ **Claude Code neu starten**
4. ⏳ **Erste Tests durchführen** (siehe Beispiel-Workflows)
5. 📋 **Archicad-Dokumentation in RAG indexieren** (optional, für schnellen Zugriff)

## Ressourcen

### MCP Server & Integration
- [Archicad Tapir MCP Repository](https://github.com/SzamosiMate/tapir-archicad-MCP) - MCP Server für Claude Code
- [Skill-Datei](.claude/skills/archicad/SKILL.md) - Workflow-Anleitung

### Tapir Add-On
- [ENZYME-APD Tapir Repository](https://github.com/ENZYME-APD/tapir-archicad-automation) - Add-On Downloads & Dokumentation
- [Tapir Dokumentation](https://enzyme-apd.github.io/tapir-archicad-automation/archicad-addon) - JSON Commands
- [Discord Community](https://discord.gg/NAnSennmpY) - Support & Diskussionen

### Archicad API
- [Archicad API Dokumentation](https://archicadapi.graphisoft.com/) - Offizielle API-Referenz

---

**Erstellt am**: 24. Oktober 2025
**Letzte Aktualisierung**: 24. Oktober 2025
**Status**: ✅ Add-On installiert - Aktivierung in Archicad und Test ausstehend

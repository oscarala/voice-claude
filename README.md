# Voice Claude

Taste halten, sprechen, loslassen, und Claude Code setzt die Änderung im Projekt um.
Ein kleines Fenster auf dem zweiten Monitor zeigt den Verlauf.

## Aufbau

| Datei | Aufgabe |
|---|---|
| `teil1_aufnahme.py` | Hotkey + Mikrofon-Aufnahme -> WAV |
| `teil2_text.py` | WAV -> Text (faster-whisper, lokal) |
| `teil3_claude.py` | Text -> Claude Code -> Antwort |
| `teil4_fenster.py` | Fenster mit Status und Verlauf |
| `main.py` | verbindet alles |
| `config.py` | Einstellungen (Hotkey, Projektordner, Fensterposition) |

## Einrichten

```
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

## Reihenfolge

Jeder Teil lässt sich einzeln testen:

1. `.venv\Scripts\python teil1_aufnahme.py`: F9 halten, sprechen, loslassen, die Aufnahme wird abgespielt
2. `.venv\Scripts\python teil2_text.py`: zeigt den erkannten Text der letzten Aufnahme
3. `.venv\Scripts\python teil3_claude.py`: tippen statt sprechen, Claude antwortet
4. `.venv\Scripts\python teil4_fenster.py`: Fenster mit Beispieltext
5. `.venv\Scripts\python main.py`: alles zusammen

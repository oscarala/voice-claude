"""Teil 2: Sprache -> Text  —  DEIN TEIL

Wir benutzen faster-whisper. Das läuft komplett auf deinem PC, kostenlos.
Beim allerersten Start wird das Modell heruntergeladen (bei "small" ca. 500 MB).

Testen:  .venv\\Scripts\\python teil2_text.py
  -> nimmt die letzte Aufnahme aus Teil 1 und zeigt den erkannten Text.
"""
import os
import tempfile

from faster_whisper import WhisperModel

import config

_modell = None  # wird von lade_modell() gesetzt


def lade_modell():
    """Lädt das Whisper-Modell einmal in den Speicher."""
    global _modell
    # TODO 1: Erstelle ein WhisperModel und speichere es in _modell.
    #   Parameter: der Modellname (steht in config.WHISPER_MODELL),
    #              device="cpu", compute_type="int8"  (int8 = schneller auf normalen PCs)
    pass


def transkribiere(pfad):
    """Wandelt die WAV-Datei bei `pfad` in Text um und gibt ihn als String zurück."""
    # TODO 2:
    #   a) _modell.transcribe(pfad, language=config.SPRACHE) aufrufen.
    #      Das gibt ZWEI Dinge zurück: segmente, info
    #   b) `segmente` ist kein fertiger Text, sondern viele Stücke (ungefähr Sätze).
    #      Jedes Stück hat ein Attribut .text
    #      -> verbinde alle zu einem String (Tipp: " ".join(...))
    #   c) Leerzeichen am Anfang/Ende entfernen (.strip()) und zurückgeben
    pass


if __name__ == "__main__":
    pfad = os.path.join(tempfile.gettempdir(), "voice-claude.wav")
    if not os.path.exists(pfad):
        print("Keine Aufnahme gefunden. Mach zuerst eine mit teil1_aufnahme.py")
    else:
        print("Lade Modell (beim ersten Mal dauert's)...")
        lade_modell()
        print("Erkannt:", transkribiere(pfad))

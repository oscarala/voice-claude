"""Teil 1: Hotkey + Aufnahme  —  DEIN TEIL

Ziel: Solange der Hotkey gedrückt ist, nimmt das Mikrofon auf.
Beim Loslassen wird alles als WAV-Datei gespeichert.

Testen:  .venv\\Scripts\\python teil1_aufnahme.py
  -> F9 halten, etwas sagen, loslassen -> du hörst deine Aufnahme. ESC beendet.
"""
import os
import tempfile

import keyboard
import numpy as np
import sounddevice as sd
import soundfile as sf

SAMPLERATE = 16000  # Whisper arbeitet mit 16000 Messwerten pro Sekunde
KANAELE = 1         # Mono reicht für Sprache


class Aufnahme:
    def __init__(self):
        self.stuecke = []   # hier sammeln wir die Audio-Stückchen
        self.stream = None  # der laufende Mikrofon-Stream (oder None, wenn keiner läuft)

    def _neues_stueck(self, daten, frames, zeit, status):
        """Wird von sounddevice automatisch aufgerufen (viele Male pro Sekunde),
        jedes Mal mit einem neuen Stück Audio in `daten` (ein numpy-Array).
        Die anderen Parameter brauchst du nicht."""
        # TODO 1: Hänge eine KOPIE von `daten` an self.stuecke an.
        #   Warum Kopie? sounddevice benutzt dasselbe Array danach wieder und
        #   überschreibt es. Ohne Kopie hättest du am Ende lauter gleiche Stücke.
        pass

    def start(self):
        """Startet die Aufnahme."""
        # TODO 2:
        #   a) self.stuecke leeren (von der letzten Aufnahme könnte noch was drin sein)
        #   b) Einen Stream öffnen, der bei jedem neuen Stück self._neues_stueck aufruft:
        #        sd.InputStream(samplerate=..., channels=..., callback=...)
        #      und in self.stream speichern
        #   c) Den Stream starten (.start())
        pass

    def stop(self):
        """Stoppt die Aufnahme, speichert sie als WAV und gibt den Dateipfad zurück.
        Gibt None zurück, wenn nichts aufgenommen wurde."""
        # TODO 3:
        #   a) Stream stoppen und schließen (.stop() und .close()), danach self.stream = None
        #   b) Wenn self.stuecke leer ist: None zurückgeben
        #   c) Alle Stücke zu EINEM Array verbinden (Tipp: np.concatenate)
        #   d) Einen Pfad im Temp-Ordner bauen, z.B. "voice-claude.wav"
        #      (Tipp: tempfile.gettempdir() und os.path.join)
        #   e) Speichern mit sf.write(pfad, audio, samplerate)
        #   f) Pfad zurückgeben
        pass

    def laeuft(self):
        return self.stream is not None


def registriere_hotkey(taste, beim_druecken, beim_loslassen):
    """Ruft beim_druecken() auf, wenn `taste` gedrückt wird,
    und beim_loslassen(), wenn sie wieder losgelassen wird."""
    # TODO 4: Benutze keyboard.on_press_key(taste, funktion) und
    #   keyboard.on_release_key(taste, funktion).
    #   Beide rufen deine Funktion mit EINEM Argument auf (dem Tasten-Event),
    #   beim_druecken/beim_loslassen wollen aber KEINS -> du brauchst eine kleine
    #   Zwischen-Funktion (def ... oder lambda).
    #
    #   Falle: Wenn man eine Taste HÄLT, schickt Windows "gedrückt" immer wieder
    #   (wie wenn du "aaaaaaa" tippst, wenn du A hältst). beim_druecken() soll aber
    #   nur EINMAL pro Drücken laufen. Merk dir also, ob die Taste schon unten ist.
    #   Tipp: ein dict als Merkzettel, z.B. zustand = {"unten": False}
    pass


if __name__ == "__main__":
    # Selbsttest: Aufnahme machen und gleich wieder abspielen
    aufnahme = Aufnahme()

    def gedrueckt():
        print("Aufnahme läuft...")
        aufnahme.start()

    def losgelassen():
        pfad = aufnahme.stop()
        if pfad is None:
            print("Nichts aufgenommen.")
            return
        print("Gespeichert:", pfad, "- spiele ab...")
        audio, rate = sf.read(pfad)
        sd.play(audio, rate)
        sd.wait()

    registriere_hotkey("f9", gedrueckt, losgelassen)
    print("F9 halten zum Aufnehmen, ESC zum Beenden.")
    keyboard.wait("esc")

"""Steckt alle vier Teile zusammen.

Starten:  .venv\\Scripts\\python main.py
"""
import threading

import config
from teil1_aufnahme import Aufnahme, registriere_hotkey
from teil2_text import lade_modell, transkribiere
from teil3_claude import ClaudeVerbindung
from teil4_fenster import Fenster

BEREIT = f"Bereit - {config.HOTKEY.upper()} halten zum Sprechen"


def main():
    print("Lade Whisper-Modell...")
    lade_modell()

    fenster = Fenster()
    aufnahme = Aufnahme()
    claude = ClaudeVerbindung(config.PROJEKT_ORDNER)

    # Solange Claude an etwas arbeitet, ist dieses Schloss zu -> keine zweite Aufnahme
    beschaeftigt = threading.Lock()

    def verarbeite(pfad):
        # Läuft in einem eigenen Thread, damit das Fenster nicht einfriert
        try:
            fenster.sicher(fenster.zeige_status, "Verstehe...")
            text = transkribiere(pfad)
            if not text:
                fenster.sicher(fenster.fuege_nachricht_hinzu, "Fehler", "Nichts verstanden.")
                return
            fenster.sicher(fenster.fuege_nachricht_hinzu, "Du", text)
            fenster.sicher(fenster.zeige_status, "Claude arbeitet...")
            antwort = claude.frage(text)
            fenster.sicher(fenster.fuege_nachricht_hinzu, "Claude", antwort)
        except Exception as fehler:
            fenster.sicher(fenster.fuege_nachricht_hinzu, "Fehler", str(fehler))
        finally:
            beschaeftigt.release()
            fenster.sicher(fenster.zeige_status, BEREIT)

    def gedrueckt():
        if not beschaeftigt.acquire(blocking=False):
            return  # Claude arbeitet noch
        aufnahme.start()
        fenster.sicher(fenster.zeige_status, "Höre zu...")

    def losgelassen():
        if not aufnahme.laeuft():
            return
        pfad = aufnahme.stop()
        if pfad is None:
            beschaeftigt.release()
            fenster.sicher(fenster.zeige_status, BEREIT)
            return
        threading.Thread(target=verarbeite, args=(pfad,), daemon=True).start()

    registriere_hotkey(config.HOTKEY, gedrueckt, losgelassen)
    fenster.zeige_status(BEREIT)
    fenster.starten()


if __name__ == "__main__":
    main()

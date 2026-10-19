"""Teil 3: Text an Claude schicken und die Antwort zurückbekommen.

Wir starten dafür das `claude`-Programm (Claude Code), das schon installiert ist.
Das läuft über deinen normalen Claude-Login, du brauchst keinen extra API-Key.

Damit Claude sich an vorherige Befehle erinnert ("mach das nochmal größer"),
geben wir jedem Aufruf dieselbe Session-ID mit.

Testen:  .venv\\Scripts\\python teil3_claude.py
"""
import json
import shutil
import subprocess
import uuid

import config

ZUSATZ_ANWEISUNG = (
    "Der Nutzer spricht mit dir per Sprachsteuerung. Seine Nachricht wurde automatisch "
    "transkribiert und kann Erkennungsfehler enthalten. Antworte kurz auf Deutsch "
    "(2-4 Sätze), deine Antwort wird in einem kleinen Fenster angezeigt."
)


def finde_claude():
    # Auf Windows heißt das Programm meist claude.cmd (über npm installiert) oder claude.exe
    for name in ("claude.cmd", "claude.exe", "claude"):
        pfad = shutil.which(name)
        if pfad:
            return pfad
    raise RuntimeError("Das 'claude'-Programm wurde nicht gefunden. Ist Claude Code installiert?")


class ClaudeVerbindung:
    def __init__(self, projekt_ordner):
        self.projekt_ordner = projekt_ordner
        self.claude_pfad = finde_claude()
        self.session_id = str(uuid.uuid4())
        self.session_gestartet = False

    def frage(self, text):
        """Schickt `text` an Claude, wartet bis er fertig ist und gibt seine Antwort zurück."""
        befehl = [
            self.claude_pfad,
            "-p",                                   # nicht interaktiv: Antwort ausgeben und beenden
            "--output-format", "json",              # Antwort als JSON, leichter auszulesen
            "--permission-mode", "acceptEdits",     # Dateien ändern ohne jedes Mal nachzufragen
            "--append-system-prompt", ZUSATZ_ANWEISUNG,
        ]
        if self.session_gestartet:
            befehl += ["--resume", self.session_id]
        else:
            befehl += ["--session-id", self.session_id]

        # Den Text schicken wir über stdin statt als Argument, so machen Anführungszeichen
        # und Sonderzeichen im gesprochenen Text keine Probleme.
        ergebnis = subprocess.run(
            befehl,
            input=text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=self.projekt_ordner,
            timeout=15 * 60,
        )
        if ergebnis.returncode != 0:
            return "Fehler von Claude: " + (ergebnis.stderr.strip() or ergebnis.stdout.strip())

        self.session_gestartet = True
        daten = json.loads(ergebnis.stdout)
        return daten.get("result", "(keine Antwort)")


if __name__ == "__main__":
    # Selbsttest: tippen statt sprechen
    claude = ClaudeVerbindung(config.PROJEKT_ORDNER)
    print("Projekt:", config.PROJEKT_ORDNER)
    print("Schreib etwas an Claude (leere Zeile = Ende).")
    while True:
        text = input("\nDu: ").strip()
        if not text:
            break
        print("Claude denkt nach...")
        print("Claude:", claude.frage(text))

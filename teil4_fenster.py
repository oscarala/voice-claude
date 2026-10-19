"""Teil 4: Fenster für den zweiten Monitor  —  DEIN TEIL

Zeigt oben den Status ("Höre zu...", "Claude arbeitet...") und darunter den Verlauf.

Testen:  .venv\\Scripts\\python teil4_fenster.py
"""
import tkinter as tk

import config


class Fenster:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Voice Claude")
        self.root.geometry(config.FENSTER_GROESSE + config.FENSTER_POSITION)

        # TODO 1: Baue die Oberfläche.
        #   - Oben ein Label für den Status -> speichern in self.status_label
        #     (tk.Label(self.root, text="...")), Starttext z.B. "Bereit"
        #   - Darunter ein Textfeld für den Verlauf -> speichern in self.verlauf
        #     (tk.Text(self.root, ...)). Es soll den restlichen Platz ausfüllen.
        #     Tipp: .pack(fill="both", expand=True)
        #   - Bonus: dunkler Hintergrund (bg=...), Textfarbe (fg=...),
        #     größere Schrift (font=("Segoe UI", 12)), Zeilenumbruch bei Wörtern (wrap="word")
        pass

    def zeige_status(self, text):
        # TODO 2: Den Text vom Status-Label ändern. Tipp: .config(text=...)
        pass

    def fuege_nachricht_hinzu(self, wer, text):
        """`wer` ist "Du", "Claude" oder "Fehler"."""
        # TODO 3: Am Ende vom Verlauf einfügen, z.B.  "Du: mach den Button blau\n\n"
        #   Tipp: self.verlauf.insert("end", ...)
        #   Danach nach unten scrollen: self.verlauf.see("end")
        #   Bonus: "Du" und "Claude" in verschiedenen Farben (Stichwort: tag_config)
        pass

    # ----- ab hier fertig, nicht ändern -----

    def sicher(self, funktion, *args):
        """tkinter darf nur aus dem Haupt-Thread benutzt werden. main.py arbeitet aber
        in einem anderen Thread (damit das Fenster nicht einfriert, während Claude denkt).
        Deshalb ruft main.py deine Methoden über diese hier auf."""
        self.root.after(0, funktion, *args)

    def starten(self):
        self.root.mainloop()


if __name__ == "__main__":
    fenster = Fenster()
    fenster.zeige_status("Test-Status: Claude arbeitet...")
    fenster.fuege_nachricht_hinzu("Du", "Mach den Hero-Button blau.")
    fenster.fuege_nachricht_hinzu("Claude", "Erledigt, der Button in Hero.tsx ist jetzt blau.")
    fenster.starten()

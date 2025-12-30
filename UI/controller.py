import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self._anno = None


# A) popolo la dropdown iniziale con gli anni e gestisco l'handler con l'anno inserito
    def popola_dropdown(self):
        self._view.dd_anno.options = [ft.dropdown.Option(anno) for anno in self._model._anni]
        self._view.update()

    def dropdown_changed(self, e):
        # ricavo l'anno inserito dall'utente
        self._anno = e.control.value

        # richiamo al model per cercare le squadre relative a quell'anno
        self._lista_squadre = self._model.squadreAnno(self._anno)

        # implemento la view per la ListView
        self._view.txt_out_squadre.clean()
        self._view.txt_out_squadre.controls.append(ft.Text(f"Numero squadre: {len(self._lista_squadre)}"))
        for squadra in self._lista_squadre:
            self._view.txt_out_squadre.controls.append(ft.Text(f"{squadra.team_code} ({squadra.name})"))

        # popolo anche la dropdown relativa alle squadre
        self._view.dd_squadra.options = [ft.dropdown.Option(key = squadra.team_code,
                                                            text = f"{squadra.team_code} ({squadra.name})") for squadra in self._lista_squadre]
        self._view.update()


# B) funzione che gestisce la creazione del grafo
    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        self._model.build_graph(self._anno)
        self._view.update()


# C) funzione di handler che gestisce i dettagli
    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        self._view.txt_risultato.clean()
        utente = self._view.dd_squadra.value
        connessi = self._model.connessi(utente)
        for connesso in connessi:
            print(connesso)
            self._view.txt_risultato.controls.append(ft.Text(f"{connesso.team_code} ({connesso.name}) - peso: "))
        self._view.update()


# D) funzione di handler che gestisce il percorso
    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        self._view.txt_risultato.clean()
        self._view.update()
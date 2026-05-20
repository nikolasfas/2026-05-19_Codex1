import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choicePartenza = None
        self._choiceArtista = None

    def fillDDGenre(self):
        genre = self._model.getAllGenre()
        for g in genre:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(
                    data= g,  # Oggetto che stiamo inserendo
                    key= g.Name,  # Cosa verrà visualizzato
                    on_click=self._choiceDdPartenza, # Metodo che viene chiamato quando selezioniamo ciascuna voce ddel dropdown
                )
            )

    def _choiceDdPartenza(self, e):
        self._choicePartenza = e.control.data
        print(f"Hai selezionato '{self._choicePartenza.Name}' come genre.")
        self.fillDDArtist()

    def handleCreaGrafo(self, e):
        topI, top5 = self._model.buildGraph(self._choicePartenza.GenreId)
        nodes, edges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato correttamente: {nodes} nodi e {edges} archi")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Artista più influente: {topI[0]}, con influenza: {topI[1]}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Top 5 archi: ")
        )
        for a1, a2, data in top5:
            self._view.txt_result.controls.append(
                ft.Text(f"{a1.Name} -> {a2.Name}: {data["weight"]}")
            )

        self._view._ddArtist.disabled = False
        self._view.update_page()


    def fillDDArtist(self):
        for a in self._model.getAllArtists(self._choicePartenza.GenreId):
            self._view._ddArtist.options.append(
                ft.dropdown.Option(
                    data= a,  # Oggetto che stiamo inserendo
                    key= a.Name,  # Cosa verrà visualizzato
                    on_click=self._choiceDdArtista, # Metodo che viene chiamato quando selezioniamo ciascuna voce ddel dropdown
                )
            )

    def _choiceDdArtista(self, e):
        self._choiceArtista = e.control.data
        print(f"Hai selezionato '{self._choiceArtista.Name}' come genre.")

    def handleCammino(self,e):
        best_percorso = self._model.getPercorso(self._choiceArtista)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Il miglior percorso da {self._choiceArtista.Name} è:  ")
        )
        testo = " -> ".join(a.Name for a in best_percorso)
        self._view.txt_result.controls.append(ft.Text(testo))
        self._view.update_page()
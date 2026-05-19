import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choicePartenza = None

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

    def handleCreaGrafo(self, e):
        self._model.buildGraph(self._choicePartenza.GenreId)
        nodes, edges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato correttamente: {nodes} nodi e {edges} archi")
        )
        self._view.update_page()


    def handleCammino(self,e):
        pass
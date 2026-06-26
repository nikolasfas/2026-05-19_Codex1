import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        genres = self._model.getAllGenres()

        for genre in genres:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(
                    key = genre.GenreId,
                    text = genre.Name,
                )
            )


    def handleCreaGrafo(self, e):
        genreId =  self._view._ddGenre.value
        if not genreId:
            self._view.txt_result.controls.append(
                ft.Text("Selezionare un genre dal menù.", color="red")
            )
            self._view.update_page()
            return
        self._model.buildGraph(genreId)
        nodes, edges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato\nNumero di nodi: {len(nodes)}\nNumero di archi: {len(edges)}")
        )
        mostInfluent = self._model.getMostInfluent()
        self._view.txt_result.controls.append(
            ft.Text(f"Artistista più influente {mostInfluent[0]} con influenza: {mostInfluent[1]}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"ATop 5 archi:")
        )
        bestEdges = self._model.bestEdges()
        for u, v, data in bestEdges:
            self._view.txt_result.controls.append(
                ft.Text(f"{u} --> {v} | peso: {data['weight']}")
            )

        self._view._ddArtist.disabled = False
        for node in nodes:
            self._view._ddArtist.options.append(
                ft.dropdown.Option(
                    key=node.ArtistId,
                    text=node.Name,
                )
            )
        self._view.update_page()


    def handleCammino(self,e):
        start_id = self._view._ddArtist.value
        if not start_id:
            self._view.txt_result.controls.append(
                ft.Text("Selezionare un artista dal menù.", color="red")
            )
            self._view.update_page()
            return

        bestpath = self._model.handlePath(start_id)
        self._view.txt_result.controls.append(
            ft.Text(f"Cammino di lunghezza massima  trovato con lunghezza {len(bestpath)}: ")
        )
        for node in bestpath:
            self._view.txt_result.controls.append(
                ft.Text(node)
            )
        self._view.update_page()
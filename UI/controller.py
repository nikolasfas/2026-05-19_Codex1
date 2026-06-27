import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self, e):
        pass

    def fillDdCountires(self):
        countries = self._model.getCountires()
        for country in countries:
            self._view._ddCountry.options.append(
                ft.dropdown.Option(country)
            )


    def handleCammino(self,e):
        pass
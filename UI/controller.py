import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._selectedTeam = None



    def handleCreaGrafo(self, e):
        if self._view._ddAnno.value is None:
            self._view._txt_result.controls.append(ft.Text("Seleziona un anno dal menù"))
            return

        self._model.build_graph(self._view._ddAnno.value)
        self._view._txt_result.controls.clear()
        nodi,archi = self._model.getGraphDetails()
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo è fromato da {nodi} nodi e {archi} archi"))


        self._view._page.update()

    def handleDettagli(self, e):
        vicini = self._model.getSortedNeighbors(self._selectedTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Stampo i vicini di {self._selectedTeam}"))
        for v in vicini:
            self._view._txt_result.controls.append(ft.Text(f"{v[1]} - {v[0]}"))
        self._view._page.update()

    def handlePercorso(self, e):
        if self._selectedTeam == None:
            warnings.warn("Squadra non selezionata")
            self._view._txt_result.controls.append(ft.Text(f"Squadra non selezionata."))

        path = self._model.getPercorso(self._selectedTeam)

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Percorso trovato."))
        for p in path:
            self._view._txt_result.controls.append(ft.Text(f"{p[0]} -- {p[1]}"))

        self._view.update_page()


    def fillDDYear(self):
        anni = self._model.getALlYears()
        yearsDD = map(lambda x:ft.dropdown.Option(x), anni)
        self._view._ddAnno.options = yearsDD
        self._view._page.update()
        #questo corrisponde a fare :
        # yearsDD = []
        # for y in anni:
            # yearsDD.append(ft.dropdown.Option(y))

    def handleDDYearSelection(self, e):
        global intAnno
        self._view._txtOutSquadre.controls.clear()
        teams = self._model.getTeamsOfYear(self._view._ddAnno.value)
        self._view._txtOutSquadre.controls.append(ft.Text(f"Ho trovato {len(teams)} che hanno giocato nel {self._view._ddAnno.value}"))
        for team in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(f"{team.teamCode}"))
            self._view._ddSquadra.options.append(ft.dropdown.Option(data = team, text = team.teamCode, on_click=self.readDDTeams)),

        self._view._page.update()


    def readDDTeams(self, e):
        if e.control.data is None:
            self._selectedTeam = None
        else:
            self._selectedTeam = e.control.data
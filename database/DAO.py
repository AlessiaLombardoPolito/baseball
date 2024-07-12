from database.DB_connect import DBConnect
from model.team import Team


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(YEAR) 
                    from teams t 
                    where `year` >= 1985 
                    order by `year` desc"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["YEAR"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTeamsOfYear(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from teams t
                    where t.`year` = %s"""

        cursor.execute(query, (anno,))

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSalaryOfTeams(year, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t.teamCode , t.ID , sum(s.salary) as totSalary
                      FROM salaries s , teams t , appearances a 
                      WHERE s.`year` = t.`year` and t.`year` = a.`year` 
                      and a.`year` = %s
                      and t.ID = a.teamID 
                      and s.playerID = a.playerID 
                      GROUP by t.teamCode"""
        #Questa query SQL è progettata per calcolare il totale degli stipendi per ciascuna squadra in un determinato
        # anno. Funzionamento Generale:
        #
        # La query seleziona i codici delle squadre (t.teamCode) e i loro ID (t.ID), insieme alla somma totale degli
        # stipendi dei loro giocatori (sum(s.salary)).
        # Le tabelle salaries, teams e appearances sono unite implicitamente utilizzando condizioni che assicurano
        # che i dati corrispondano per lo stesso anno e per le stesse squadre e giocatori.
        # Viene filtrato solo per l'anno specificato (%s), e i risultati sono raggruppati per codice della squadra.
        # Alla fine, la query restituisce il totale degli stipendi per ciascuna squadra nell'anno specificato.

        cursor.execute(query, (year,))

        result = {}
        for row in cursor:
            # result.append( (idMap[row["ID"]], row["totSalary"]) )
            result[idMap[row["ID"]]] = row["totSalary"]

        cursor.close()
        conn.close()
        return result
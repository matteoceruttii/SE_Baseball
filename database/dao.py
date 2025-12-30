from database.DB_connect import DBConnect
from model.squadre import Squadre
from model.salario import Salario


class DAO:
# funzione che seleziona gli anni di campionato da inserire in seguito nel menu a tendina
    @staticmethod
    def selezionaAnno():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT year
                    FROM team
                    WHERE year >= 1980 """
        cursor.execute(query)

        # prendo gli anni dal database e filtro per non avere anni ripetuti
        for row in cursor:
            if row['year'] not in result:
                result.append(row['year'])

        cursor.close()
        conn.close()
        return result

# funzione che estrae le squadre che hanno giocato nell'anno selezionato (nodi del grafo)
    @staticmethod
    def getSquadreAnno(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select t.team_code, t.name
                    from team t
                    where t.year = %s """

        cursor.execute(query, (anno, ))

        for row in cursor:
            result.append(Squadre(**row))

        cursor.close()
        conn.close()
        return result


# funzione che ricava i pesi degli archi (somma dei salari dei vari giocatori)
    @staticmethod
    def getSalario(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select s.team_id, s.team_code , sum(s.salary) as somma_salario
                    from salary s
                    where s.year = %s
                    group by s.team_id, s.team_code  """

        cursor.execute(query, (anno,))

        for row in cursor:
            result.append(Salario(**row))

        cursor.close()
        conn.close()
        return result

if __name__ == '__main__':
    dao = DAO()
    for salario in dao.getSalario(2015):
        print(salario)
    print(dao.getSalario(2015))
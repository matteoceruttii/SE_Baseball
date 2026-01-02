from database.DB_connect import DBConnect
from model.squadre import Squadre


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
        query = """ select s.team_id, s.team_code, t.name, sum(s.salary) as somma_salario
                    from salary s, team t
                    where s.year = %s and t.team_code = s.team_code
                    group by s.team_id, s.team_code  """

        cursor.execute(query, (anno, ))

        for row in cursor:
            result.append(Squadre(**row))

        cursor.close()
        conn.close()
        return result

if __name__ == '__main__':
    dao = DAO()
    for salario in dao.getSquadreAnno(2015):
        print(salario)
    print(dao.getSquadreAnno(2015))
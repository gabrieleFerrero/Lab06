from database.DB_connect import get_connection
from model.strumento import Strumento
from model.prestito import Prestito

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self._nome = nome
        self._responsabile = responsabile

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self._responsabile = responsabile

    def get_strumenti(self) -> list[Strumento] | None:
        """
            Funzione che legge tutti gli strumenti nel database
            :return: una lista con tutti gli strumenti presenti oppure None
        """
        cnx = get_connection()
        if cnx is None:
            return None

        cursor = cnx.cursor()
        query = "SELECT codice, tipo, marca, anno_acquisto, valore, disponibile FROM strumento"
        try:
            cursor.execute(query)
            result = []
            for (codice, tipo, marca, anno_acquisto, valore, disponibile) in cursor:
                result.append(Strumento(codice, tipo, marca, anno_acquisto, valore, bool(disponibile)))
            return result
        except Exception as e:
            print(f"Errore nella lettura degli strumenti dal database: {e}")
            return None
        finally:
            cursor.close()
            cnx.close()

    def cerca_strumenti_per_tipo(self, tipo) -> list[Strumento] | None:
        """
            Funzione che recupera una lista con tutti gli strumenti presenti nel database di un certo tipo
            :param tipo: il tipo dello strumento (es. "Chitarra")
            :return: una lista con tutti gli strumenti del tipo indicato oppure None
        """
        cnx = get_connection()
        if cnx is None:
            return None

        cursor = cnx.cursor()
        query = "SELECT codice, tipo, marca, anno_acquisto, valore, disponibile FROM strumento WHERE tipo = %s"
        try:
            cursor.execute(query, (tipo,))
            result = []
            for (codice, tipo_str, marca, anno_acquisto, valore, disponibile) in cursor:
                result.append(Strumento(codice, tipo_str, marca, anno_acquisto, valore, bool(disponibile)))
            return result
        except Exception as e:
            print(f"Errore nella ricerca degli strumenti per tipo: {e}")
            return None
        finally:
            cursor.close()
            cnx.close()

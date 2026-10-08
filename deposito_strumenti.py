#in python prima devo importare
import csv
from operator import attrgetter
#creo gli oggetti->stesso file!
class Strumento:
    def __init__(self,id_strumento,tipo, marca, anno_acquisto, valore):
        self.id_strumento = id_strumento
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = int(anno_acquisto) #file csv-> in python devi dichiarare solo int e float
        self.valore = float(valore)

    #si descrive da sola
    def __str__(self):
        return f"{self.id_strumento}, {self.tipo}, {self.marca}, {self.anno_acquisto}, {self.valore}"


class Prestito:
    def __init__(self, id_prestito, data, id_strumento, cognome_allievo):
        self.id_prestito = id_prestito
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return f"{self.id_prestito}, {self.data}, {self.id_strumento}, {self.cognome_allievo}"


class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.responsabile = responsabile

        self.strumenti = {}
        self.prestiti = {}

        # per generare in automatico i nuovi codici
        self.ultimo_numero_strumento = 0
        self.ultimo_numero_prestito = 1

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        #carico file csv per lettura
        try:
            with open(file_path, mode='r', encoding='utf-8') as csvfile:
                reader= csv.reader(csvfile)
            for riga in reader:
            # controllo che la riga abbia tutti e 5 gli elementi
                if len(riga) == 5:
                    id_str, tipo, marca, anno, valore = riga

                # creo l'oggetto Strumento
                    nuovo_strumento = Strumento(id_str, tipo, marca, anno, valore)
                    #devo aggiungerlo in un dizionario che devo creare io per me quindi sarà un attributo dell'oggetto e
                    #non una componente-> tipo i figli di java
                    # lo inserisco nel dizionario-registro
                    self.strumenti[id_str] = nuovo_strumento

                    # aggiorno ID-> prendo il numero dell'ID attuale togliendo la S
                    numero_id = int(id_str.replace("S", ""))
                    if numero_id > self.ultimo_numero_strumento:
                        self.ultimo_numero_strumento = numero_id

        except FileNotFoundError:
        #se il file non esiste, scateniamo l'eccezione richiesta con raise che è proprio la funzione che
        #dice al main di vedersela lui per le eccezioni
            raise FileNotFoundError("Errore: Il file CSV degli strumenti non è stato trovato.")

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        #aumento di 1 il contatore per creare il nuovo id
        self.ultimo_numero_strumento += 1
        nuovo_id = f"S{self.ultimo_numero_strumento}"

        # creo lo strumento e lo salviamo nel dizionario
        nuovo_strumento = Strumento(nuovo_id, tipo, marca, anno_acquisto, valore)
        self.strumenti[nuovo_id] = nuovo_strumento

        return nuovo_strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        #ho gia importato sopra
        #creo  una lista degli strumenti-> alfabetico
        lista_strumenti= list(self.strumenti.values())
        lista_ordinata= sorted (lista_strumenti, key=attrgetter('marca'))
        return lista_ordinata

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        #se strumento non esiste
        if id_strumento not in self.strumenti:
            raise Exception(f"Errore: {id_strumento} non trovato")
        #se strumento è gia in prestito
        for prestito in self.strumenti.values():
            if prestito.id_strumento == id_strumento:
                raise Exception(f"Errore: {id_strumento} già prestato")
        #adesso posso procedere alla creazione dell'oggetto
        id_prestito= self.ultimo_numero_prestito + 1
        nuovo = Prestito(id_prestito, data, id_strumento, cognome_allievo)
        self.prestiti[id_prestito] = nuovo #non usi append perchè è un dizionario e non una lista
        return nuovo

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""

        def termina_prestito(self, id_prestito):
            # se il codice prestito non c'è scateno l'errore
            if id_prestito not in self.prestiti:
                raise Exception("Errore: Il codice prestito inserito non esiste.")

            # dizionario -> pop non remouve
            self.prestiti.pop(id_prestito)

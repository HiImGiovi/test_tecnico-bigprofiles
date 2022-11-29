![BigProfiles-Logo](https://bigprofiles.com/wp-content/uploads/2021/02/logo_multicolor.png)
# BigProfiles API

API ad alte performance per l’ingestion di informazioni. Sui dati 
salvati è possibile l’aggregazione temporale per minuto e sono 
restituite alcune statistiche (come, ad esempio, tempo totale di risposta, numero di errori, numero 
di richieste) aggregate sempre per minuto e la lista delle ultime 10 chiamate effettuate dell’ultima 
aggregazione.

## Prerequisiti
- Docker installato ed in esecuzione (https://docs.docker.com/get-docker/)

## Setup

- Una volta clonata la cartella, entrarci dentro, assicurandosi di essere allo stesso livello del file **docker-compose.yml** e lanciare il comando

    ```

    docker-compose up

    ```
- Finita la creazione delle immagini docker e del container, assicurarsi che l'api sia in funzione esposta in locale sulla porta 8000: <br />
**http://localhost:8000/docs** o **http://127.0.0.1:8000/docs**.<br />
Si dovrebbe accedere alla seguente schermata:

    ![APIDocs](/resources/APIDocs.png)

## Documentazione
### **Ingest**
Vengono eseguiti tutti i calcoli necessari per dare una response nel tempo atteso, 10-50ms ± 10%, senza andare a salvare subito i dati su db. <br />
Una volta deciso il tempo randomico di risposta e il rispettivo codice, 200 o 500, abbiamo tutti i dati per fare partire una post a database in **background** in modo di riuscire a controllare il tempo di risposta dell'endpoint (vedi funzione [write_enrich_input_to_db](/backend/src/routes/ingest.py#write_enrich_input_to_db)).<br />
**Punto di attenzione**: è possibile fare ciò, solo perché il codice di risposta viene definito a priori, a prescindere da ciò che succede dal salvataggio a db.

### **Retrieve**
Per la fase di retrieve è stata utilizzata aggregation pipeline. La logica seguita è stata quella di fare un unico filtro sui dati, andando a matchare l'intervallo temporale dei query parameter, e poi fare le successive operazioni per ottenere i risultati aggregati e i log.
E' stata eseguita prima una pipeline per ottenere i risultati aggregati, ed è poi stato utilizzato l'ultimo risultato aggregato per il recupero degli ultimi dieci log in quella finestra temporale.

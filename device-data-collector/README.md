# Device Data Collector

## Descrizione
Il microservizio `device-data-collector` riceve messaggi da dispositivi tramite il protocollo MQTT e li inserisce in un database MongoDB. Utilizza un pool di thread per gestire l'inserimento dei dati in modo efficiente.

## Funzionalità
- Connessione a un broker MQTT per ricevere messaggi dai dispositivi.
- Inserimento dei messaggi ricevuti in un database MongoDB.
- Gestione del multithreading per migliorare le prestazioni.

## Configurazione
Assicurati che MongoDB sia in esecuzione e accessibile. Configura il broker MQTT per inviare i messaggi ai topic desiderati.

## Esecuzione
1. Installa le dipendenze:
   ```bash
   pip install paho-mqtt pymongo

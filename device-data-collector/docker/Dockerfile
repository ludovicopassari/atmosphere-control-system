# Usa un'immagine base di Python
FROM python:3.9-slim

# Imposta la directory di lavoro all'interno del container.
WORKDIR /device-data-collector

# Copia il resto del codice nell'immagine
COPY ./app .

# Installa le dipendenze Python. Esegue quando si fa il buil dell'immagine
RUN pip install --upgrade -r requirements.txt

# Esegue il codice
CMD ["python", "device_data_collector.py"]
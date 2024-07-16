# Usa un'immagine base di Python
FROM python:3.9-slim

# Imposta la directory di lavoro all'interno del container.
WORKDIR /device-data-collector

# Copia il resto del codice nell'immagine
COPY . .

# Installa le dipendenze Python. Esegue quando si fa il buil dell'immagine
RUN pip install --no-cache-dir -r requirements.txt

# Esegue il codice
CMD ["python", "device_data_collector.py"]
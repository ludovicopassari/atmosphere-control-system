import logging
import queue
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from typing import List

import paho.mqtt.client as mqtt
from pymongo import MongoClient

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.debug("Creating Message Queue...")
# rappresenta la coda di messaggi in arrivo
message_queue = Queue(4)
mongo_client = MongoClient("mongodb://mongo:27017/", username='root', password='passwd')
db = mongo_client["testdb"]
collection = db["messages"]


# funzione di callback per gestire le connessioni
def on_connect(client, userdata, flags, reason_code, properties):
    logger.info("Connected with result code :  " + str(reason_code))
    client.subscribe("devices/data")


# funzione di callback per gestire l'arrivo di un messaggio
def on_message(client, userdata, msg):
    logger.info("Received a message on topic " + str(msg.topic))
    enqueue_message(message_queue, msg, 2, False)
    logger.debug("Message successfully enqueued ")


def process_message(msg_queue: Queue):
    while True:
        message = msg_queue.get()
        if message is None:
            break
        logger.debug(f"Working on  message: {message} thread {threading.current_thread()}")

        try:
            data = {
                "topic": "topic",
                "payload": message.payload.decode("utf-8"),
                "timestamp": time.time()
            }
            collection.insert_one(data)
            logger.debug("Message successfully stored ")

        except Exception as e:
            logger.error(f"Errore durante l'inserimento nel DB: {e}")
        message_queue.task_done()


# inserisce nella cosa di messaggi un messaggio assumendo che esso sia gia stato validato
def enqueue_message(msg_queue: Queue, message: str, timeout: int, block: bool):
    try:
        msg_queue.put(message, block=block, timeout=timeout)
    except KeyboardInterrupt:
        queue.put(None)
        exit(0)


def main():

    # numero di thread worker
    num_workers = 2
    logger.debug(f"Create successfully thread Queue with {num_workers} threads ")

    logger.debug("Create MQTT Client")
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqtt_client.enable_logger(logger=logger)
    # assegno le funzioni di call back
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    # Connessione al broker Mosquitto
    mqtt_client.connect("mosquitto", 1883, 60)
    logger.debug("Connected to MQTT Server")

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        logger.debug("Starting worker threads...")
        # lancia le istanze di thread che eseguiranno la funzione specificata come parametro
        futures = [executor.submit(process_message, message_queue) for _ in range(num_workers)]
        logger.debug("Worker threads started...")

        logger.debug("Starting thread to process network traffic")
        # lancia il thread che gestisce il traffico in arrivo dalla rete in modo tale da non bloccare il thread
        mqtt_client.loop_start()

        try:
            while True:
                pass
        except KeyboardInterrupt:

            mqtt_client.loop_stop()
            mqtt_client.disconnect()

            # aspetta che la coda di messaggi sia vuota
            message_queue.join()

            # fa in modo che i thread avviati terminino
            for i_thread in range(num_workers):
                message_queue.put(None)

            # aspetta che i thread siano terminati
            executor.shutdown(wait=True)


if __name__ == '__main__':
    main()

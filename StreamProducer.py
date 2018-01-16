#!/usr/bin/env python
import threading, logging, time
import multiprocessing
import msgpack
from kafka import KafkaConsumer, KafkaProducer

class TweeterFeedProducer:
    def pushData(self,msg):
        producer = KafkaProducer(bootstrap_servers='localhost:9092')
        producer.send('test', msg)
        #producer.send('test', b"\xc2Hola, mundo!")
        producer.close()

class JSONProducer:
    def publishJSONData(self,msg):
        producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=msgpack.dumps)
        producer.send('test', msg)
        producer.close()
         
class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        
    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092')

        while not self.stop_event.is_set():
            producer.send('test', b"test")
            producer.send('test', b"\xc2Hola, mundo!")
            time.sleep(1)

        producer.close()

def main():
    tasks = [
        Producer()
    ]

    for t in tasks:
        t.start()

    time.sleep(10)
    
    for task in tasks:
        task.stop()

    for task in tasks:
        task.join()
        
        
if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )
    main()

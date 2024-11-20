from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import pika

app = FastAPI()

# Legg til CORS-middleware for å håndtere OPTIONS forespørsler
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hei, im feeling good!"}

@app.get("/db")
def db_test():
    conn = psycopg2.connect(
        dbname="exampledb",
        user="exampleuser",
        password="examplepass",
        host="db"
    )
    cur = conn.cursor()
    cur.execute("SELECT 1")
    result = cur.fetchone()
    cur.close()
    conn.close()
    return {"Database connected": result}

@app.get("/mq")
def mq_test():
    connection = pika.BlockingConnection(pika.ConnectionParameters('broker'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='', routing_key='hello', body='Hei Verden!')
    connection.close()
    return {"Message sent to RabbitMQ!"}

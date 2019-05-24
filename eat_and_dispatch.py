import logging
import os
import threading
from json import loads

from flask import Flask
from flask import request
from kafka import KafkaConsumer

import send_colis as send_colis

# debug_level = os.environ["DEBUG_LEVEL"]
#
# if debug_level == "DEBUG":
#     logging.basicConfig(level=logging.DEBUG)
# elif debug_level == "INFO":
#     logging.basicConfig(level=logging.INFO)
# elif debug_level == "WARNING":
#     logging.basicConfig(level=logging.WARNING)
# elif debug_level == "ERROR":
#     logging.basicConfig(level=logging.ERROR)
# elif debug_level == "CRITICAL":
#     logging.basicConfig(level=logging.CRITICAL)
#
# topic_from_tweethon = os.environ["FROM_TWEETHON"]
# topic_from_comparathon = os.environ["FROM_COMPARATHON"]

# colissithon_port = os.environ["COLISSITHON_PORT"]
# kafka_endpoint = str(os.environ["KAFKA_IP"]) + ":" + str(os.environ["KAFKA_PORT"])

colissithon_port = 9876
kafka_endpoint = "0.0.0.0:8092"
topic_from_tweethon = "tweethon_out"
topic_from_comparathon = "comparathon_out"
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


@app.route('/create_bio', methods=['POST'])
def create_candidate_biographics():
    logging.info('create_bio service called')
    personJson = request.get_json()
    first_name = personJson['biographicsFirstName']
    name = personJson['biographicsName']
    picture = personJson['biographicsImage']
    picture_type = personJson['biographicsImageContentType']
    bio_id = send_colis.create_new_biographics(first_name, name, picture, picture_type)
    return str(bio_id)


@app.route('/bind_bio', methods=['POST'])
def create_related_biographics():
    logging.info('bind_bio service called')
    send_colis.bind_bio_to_bio(request.get_json())


@app.route('/create_minibio', methods=['POST'])
def prepare_mini_biographics():
    colis_json = request.get_json()
    first_name = colis_json['biographicsFirstName']
    name = colis_json['biographicsName']
    picture = None
    picture_type = None
    bio_id = send_colis.create_new_biographics(first_name, name, picture, picture_type)
    return str(bio_id)


def start_REST_server(port):
    app.run(host='0.0.0.0', port=port)


def start_tweets_consumer():
    consumer = KafkaConsumer(
        topic_from_tweethon,
        bootstrap_servers=[kafka_endpoint],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )
    logging.info('Kafka Consumer for Tweetopic started')
    for msg in consumer:
        logging.debug('Consume message from ##Tweetopic')
        tweet_json = msg.value[0]
        bio_id = msg.value[1]
        logging.debug("Tweet associated to bio_Id n° : " + str(bio_id))
        send_colis.link_tweet_to_bio(tweet_json, bio_id)


def start_pictures_consumer():
    consumer = KafkaConsumer(
        topic_from_comparathon,
        bootstrap_servers=[kafka_endpoint],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )
    logging.info('Kafka Consumer for Topictures started')
    for msg in consumer:
        logging.debug('Consume message from ##Topictures')
        picture_json = msg.value[0]
        bio_id = msg.value[1]
        logging.debug("Tweet associated to bio_Id n° : " + str(bio_id))
        send_colis.link_picture_to_bio(picture_json, bio_id)


if __name__ == '__main__':
    REST_thread = threading.Thread(target=start_REST_server, args=(colissithon_port,))
    rawdatas_thread = threading.Thread(target=start_tweets_consumer)
    pictures_thread = threading.Thread(target=start_pictures_consumer)

    REST_thread.start()
    logging.info('REST Thread started')
    rawdatas_thread.start()
    logging.info('Kafka Tweetopic Thread started')
    pictures_thread.start()
    logging.info('Kafka Topictures Thread started')

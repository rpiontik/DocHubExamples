import logging
import yaml
import time
import jwt
import requests

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

with open("bot_config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

service_account_id = config["service_account_id"]
api_key_id = config["api_key_id"]
service_account_private_key = config["service_account_private_key"]

def get_iam_token():
    now = int(time.time())
    payload = {
        'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
        'iss': service_account_id,
        'iat': now,
        'exp': now + 360}

    # Формирование JWT
    encoded_token = jwt.encode(
        payload,
        service_account_private_key,
        algorithm='PS256',
        headers={'kid': api_key_id})

    url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    x = requests.post(url,  
                  headers={'Content-Type': 'application/json'},
                  json = {'jwt': encoded_token}).json()
    token = x['iamToken']
    logging.info("Получил iam_token:")
    logging.info(token)
    return token
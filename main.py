import csv
import json
import time
import logging
import configparser
import requests
from dotenv import dotenv_values

logging.basicConfig(handlers=[
        logging.FileHandler(f'logs/{int(round(time.time() * 1000))}.log'),
        logging.StreamHandler()
    ],
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %I:%M:%S %p',
    level=logging.DEBUG
)

ENV = 'DEFAULT'

config = configparser.ConfigParser()
config.read('config.ini')
secrets = dotenv_values(config[ENV]['SECRETS_FILE'])


def read_csv(filename):
    logging.info(f'Reading input CSV file: {filename}')

    # Name,Email,Phone Number,Company,Survey Score,Title,Comments
    headers = {
        0: 'Name',
        1: 'Email',
        2: 'Phone Number',
        3: 'Company',
        4: 'Survey Score',
        5: 'Title',
        6: 'Comments'
    }

    data = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:
            if line_count > 0:
                record = {headers[i]: column for i, column in enumerate(row)}
                data.append(record)

            line_count += 1

    logging.info(f'Read {line_count} lines from the input CSV file.')

    return data


def create_payload(record):
    name_parts = record['Name'].split(' ')
    last_name = name_parts.pop()
    first_name = ' '.join(name_parts)

    survey_score = int(record['Survey Score'])
    if survey_score >= 90:
        priority = 'Very High'
    elif survey_score >= 85:
        priority = 'High'
    elif survey_score >= 80:
        priority = 'Medium'
    else:
        priority = 'Low'

    phone_number = record['Phone Number'].replace('(', '').replace(')', '').replace('-', '').replace(' ', '')

    return {
        "lead_status": {"label": "New Lead"},
        "priority__1": {"label": priority},
        "text__1": first_name,
        "text0__1": last_name,
        "lead_email": {"email": record['Email'], "text": record['Email']},
        "lead_phone": {"phone": phone_number},
        "lead_company": record['Company'],
        "text": record['Title'],
        "numbers__1": survey_score,
        "long_text": record['Comments']
    }


def create_items(data):
    logging.info('Creating items in Monday.com')

    api_url = config[ENV]['MDC_API_URL']
    headers = {
        "Authorization": secrets['MDC_API_KEY']
    }

    query = """
    mutation($board_id: ID!, $item_name: String!, $group_id: String, $column_values: JSON) {
          create_item (
            board_id: $board_id,
            item_name: $item_name,
            group_id: $group_id,
            column_values: $column_values,
            create_labels_if_missing :true
          ) {
            id
          }
    }
    """

    results = []
    for idx, record in enumerate(data):
        item_name = f"{record['Name']} ({record['Email']})"  # Name (Email)
        payload = create_payload(record)

        variables = {
            "board_id": config[ENV]['MDC_LEAD_BOARD_ID'],
            "item_name": item_name,
            "group_id": config[ENV]['MDC_LOAD_GROUP_ID'],
            "column_values": json.dumps(payload)
        }

        logging.info(f"Processing record No.:{idx} - Creating item {item_name}({record['Email']})")
        response = requests.post(api_url, json={'query': query, 'variables': variables}, headers=headers)
        logging.info(f"Response for record No.:{idx} - {response.json()}")

        result = {
            "name": item_name,
            "email": record['Email'],
            "response": response.json()
        }
        results.append(result)

    with open(f'output/MDC_item_creation_{int(round(time.time() * 1000))}.json', 'w') as f:
        f.write(json.dumps(results, indent=4))

    logging.info('Finished creating items in Monday.com')


def main():
    data = read_csv('input/sample_survey_data.csv')
    create_items(data)


if __name__ == '__main__':
    main()

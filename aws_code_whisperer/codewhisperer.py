import json
import boto3
import csv

# a function to convert a json file to a csv file
# keys in the json file are in the column names


def json_to_csv(json_file, csv_file):

    # open the json file
    with open(json_file) as f:
        data = json.load(f)

    # open the csv file
    with open(csv_file, 'w') as f:
        writer = csv.writer(f)

        # write the column names
        writer.writerow(data[0].keys())

        # write the data
        for row in data:
            writer.writerow(row.values())

# a function that reards a txt file from s3 and returns the text


def read_txt(bucket, key):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)
    return response['Body'].read().decode('utf-8')

# a function that writes a txt file to s3


def write_txt(bucket, key, text):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket, Key=key, Body=text)

# a function that calls a lambda function


def lambda_handler(event, context):
    # read the json file
    json_file = read_txt(event['bucket'], event['key'])

    # convert the json file to a csv file
    csv_file = '/tmp/converted_file.csv'
    json_to_csv(json_file, csv_file)

    # write the csv file to s3
    write_txt(event['bucket'], event['key'].replace('.json', '.csv'),
              open(csv_file, 'rb').read())
    return 'Success'

# a function that reads from a dynamoDB table


def read_dynamo(table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.scan()
    return response['Items']

# a function that writes to a dynamoDB table


def write_dynamo(table_name, item):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    table.put_item(Item=item)

# a functions that reads from a sqs queue


def read_sqs(queue_url):
    sqs = boto3.client('sqs')
    response = sqs.receive_message(QueueUrl=queue_url)
    return response['Messages']

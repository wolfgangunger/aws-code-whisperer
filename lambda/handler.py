import boto3
import json


def lambda_handler(event, context):
    """
    Lambda function to delete a file from an S3 bucket.
    """
    s3 = boto3.resource("s3")
    bucket = s3.Bucket("bucket-name")
    bucket.objects.filter(Prefix="folder/").delete()
    return {"statusCode": 200, "body": json.dumps("Files deleted from bucket!")}


# a function that reads a txt file from a s3 bucket    and returns the content


def read_file(bucket_name, file_name):
    s3 = boto3.resource("s3")
    obj = s3.Object(bucket_name, file_name)
    return obj.get()["Body"].read().decode("utf-8")


# a functions that writes a txt file to a s3 bucket


def write_file(bucket_name, file_name, content):
    s3 = boto3.resource("s3")
    obj = s3.Object(bucket_name, file_name)
    obj.put(Body=content)
    return "Success"


# a function that converts a json file to csv file
# keys in the json file should be the header of the csv file


def json_to_csv(json_file_name, csv_file_name):
    json_data = read_file("bucket-name", json_file_name)
    csv_data = json.loads(json_data)
    csv_data = json.dumps(csv_data)
    write_file("bucket-name", csv_file_name, csv_data)
    return "Success"

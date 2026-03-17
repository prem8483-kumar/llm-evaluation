from pathlib import Path

import boto3
from ragas.testset import Testset


def load_test_set_from_s3_bucket(bucket: str, test_set_key: str) -> Testset:

    session = boto3.Session(profile_name="246659685798_fi_DTPLQAUser", region_name="eu-west-1")
    s3_client = session.client(service_name='s3')

    # s3_client = boto3.client("s3", region_name='eu-west-1')

    local_path = Path.cwd() / test_set_key
    local_path.parent.mkdir(parents=True, exist_ok=True)

    s3_client.download_file(bucket, test_set_key, str(local_path))

    test_set = Testset.from_jsonl(str(local_path))

    return test_set


def upload_test_set_to_s3_bucket(test_set: Testset, bucket: str, test_set_key: str):

    print('Saving test set as jsonl file locally')
    test_set.to_jsonl(test_set_key)

    print("Uploading test set as jsonl file to s3 bucket")
    session = boto3.Session(profile_name="246659685798_fi_DTPLQAUser", region_name="eu-west-1")
    s3_client = session.client(service_name='s3')

    # s3_client = boto3.client("s3", region_name='eu-west-1')

    s3_client.upload_file(test_set_key, bucket, test_set_key)
    print(f"Uploaded to S3 as {test_set_key}")

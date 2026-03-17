from generate_testset import load_documents_from_s3_bucket, generate_test_set, upload_test_set_to_s3_bucket


def create_test_set():

    bucket = "dtpl-dls-s3-dev-cur-data-science-restricted"
    document_key = "smart_knowledge_assistant/source-pdfs/Hearings & Appeals.pdf"
    test_set_key = "smart_knowledge_assistant/test-sets/Hearings & Appeals.jsonl"

    print('Loading docs')
    documents = load_documents_from_s3_bucket(bucket, document_key)

    print('Generating test set')
    test_set = generate_test_set(documents, 40)

    print('Uploading test set json file to s3 bucket')
    upload_test_set_to_s3_bucket(test_set, bucket, test_set_key)

from evaluate_raga_metrics import evaluate_raga_metrics, load_test_set_from_s3_bucket, upload_result_to_s3_bucket

bucket = ""
test_set_key = ""
evaluation_result_key = ""


def evaluate_metrics():
    print("Loading test set from s3 bucket")
    eval_dataset = load_test_set_from_s3_bucket(bucket, test_set_key)

    print('Evaluating raga metrics using test set')
    evaluation_result = evaluate_raga_metrics(eval_dataset)

    print('Uploading result to s3 bucket')
    upload_result_to_s3_bucket(evaluation_result, bucket, evaluation_result_key)

    print(f"Metric score: {evaluation_result}")

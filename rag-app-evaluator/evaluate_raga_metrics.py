import boto3

from langchain_aws import ChatBedrockConverse
from langchain_aws import BedrockEmbeddings

from ragas import EvaluationDataset, evaluate
from ragas.dataset_schema import EvaluationResult

from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper

from ragas.metrics import ResponseRelevancy, FactualCorrectness, LLMContextPrecisionWithoutReference, LLMContextRecall

config = {
    "region_name": "eu-west-1",
    "llm": "eu.anthropic.claude-3-5-sonnet-20240620-v1:0",
    "embeddings": "cohere.embed-multilingual-v3",
    "temperature": 0,
}

evaluator_llm = LangchainLLMWrapper(ChatBedrockConverse(
    region_name=config["region_name"],
    base_url=f"https://bedrock-runtime.{config['region_name']}.amazonaws.com",
    model=config["llm"],
    temperature=config["temperature"],
))

evaluator_embeddings = LangchainEmbeddingsWrapper(BedrockEmbeddings(
    region_name=config["region_name"],
    model_id=config["embeddings"],
))


def load_test_set_from_s3_bucket(bucket: str, key: str) -> EvaluationDataset:
    s3_client = boto3.client("s3")
    local_test_set_path = '/tmp/test_set.jsonl'

    s3_client.download_file(bucket, key, local_test_set_path)
    eval_dataset = EvaluationDataset.from_jsonl(local_test_set_path)

    return eval_dataset


def evaluate_raga_metrics(eval_dataset: EvaluationDataset) -> EvaluationResult:

    metrics = [
        ResponseRelevancy(llm=evaluator_llm, embeddings=evaluator_embeddings),
        FactualCorrectness(llm=evaluator_llm),

        LLMContextPrecisionWithoutReference(llm=evaluator_llm),
        LLMContextRecall(llm=evaluator_llm),
    ]

    result = evaluate(dataset=eval_dataset, metrics=metrics)

    return result


def upload_result_to_s3_bucket(evaluation_result: EvaluationResult, bucket: str, key: str):

    print('Saving result as json file locally')
    local_output_path = '/tmp/evaluation_result.json'
    evaluation_result.to_pandas().to_json(local_output_path)

    print("Uploading result as json file to s3 bucket")
    s3_client = boto3.client("s3")
    s3_client.upload_file(local_output_path, bucket, key)
    print(f"Uploaded to S3 as {key}")

import boto3
from langchain_aws import ChatBedrockConverse
from langchain_aws import BedrockEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.testset import TestsetGenerator, Testset
from ragas.testset.persona import Persona

config = {
    "region_name": "eu-west-1",
    "llm": "eu.anthropic.claude-3-5-sonnet-20240620-v1:0",
    "embeddings": "cohere.embed-multilingual-v3",
    "temperature": 0,
}

generator_llm = LangchainLLMWrapper(ChatBedrockConverse(
    region_name=config["region_name"],
    base_url=f"https://bedrock-runtime.{config['region_name']}.amazonaws.com",
    model=config["llm"],
    temperature=config["temperature"],
))

generator_embeddings = LangchainEmbeddingsWrapper(BedrockEmbeddings(
    region_name=config["region_name"],
    model_id=config["embeddings"],
))

dummy_persona = Persona(
    name="Dummy-User",
    role_description="A dummy user asking questions."
)


def load_documents_from_s3_bucket(bucket: str, key: str) -> list[Document]:

    s3_client = boto3.client("s3")
    local_document_path = '/tmp/document.pdf'

    s3_client.download_file(bucket, key, local_document_path)

    loader = PyPDFLoader(local_document_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} documents from PDF")

    return documents


def generate_test_set(documents: list[Document], size: int) -> Testset:
    generator = TestsetGenerator(
        llm=generator_llm,
        embedding_model=generator_embeddings,
        persona_list=[dummy_persona]
    )
    test_set = generator.generate_with_langchain_docs(documents, testset_size=size)
    return test_set


def upload_test_set_to_s3_bucket(test_set: Testset, bucket: str, key: str):

    print('Saving test set as jsonl file locally')
    local_output_path = '/tmp/test_set.jsonl'
    test_set.to_jsonl(local_output_path)

    print("Uploading test set as jsonl file to s3 bucket")
    s3_client = boto3.client("s3")
    s3_client.upload_file(local_output_path, bucket, key)
    print(f"Uploaded to S3 as {key}")

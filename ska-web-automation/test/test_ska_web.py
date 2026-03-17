import time

from main.s3_helper import load_test_set_from_s3_bucket, upload_test_set_to_s3_bucket
from test.conftest import SKA_WEB_URL

use_case = "SharePoint"
bucket = "dtpl-dls-s3-dev-cur-data-science-restricted"
test_set_key = "smart_knowledge_assistant/rag-test-sets/Hearings & Appeals.jsonl"


def test_ska_app_with_saved_auth(browser_context):
    print("Loading test set from s3 bucket")
    test_set = load_test_set_from_s3_bucket(bucket, test_set_key)

    print("Login and select use case")
    page = login_chatbot_and_select_use_case(browser_context, use_case)

    print("Fetch chatbot response and update test set")
    test_set = update_test_set_with_chatbot_response(page, test_set)

    print("Uploading updated test set to s3 bucket")
    upload_test_set_to_s3_bucket(test_set, bucket, test_set_key)


def login_chatbot_and_select_use_case(browser_context, use_case):
    page = browser_context.new_page()
    page.goto(SKA_WEB_URL)

    page.get_by_text(use_case).click()
    page.get_by_text("Acknowledge").click()
    return page


def update_test_set_with_chatbot_response(page, test_set):
    for sample in test_set.samples:
        print("Entering question...")
        send_question(page, sample.eval_sample.user_input)

        print("Fetching response...")
        message = get_answer(page)
        sample.eval_sample.response = message
        sample.eval_sample.retrieved_contexts = message

    return test_set


def send_question(page, message: str):
    page.evaluate("""() => {
                const el = document.querySelector('#chat-input');
                if (el) el.focus();
            }""")

    time.sleep(5)
    page.keyboard.insert_text(message)
    page.keyboard.press("Enter")


def get_answer(page):
    wait_for_message_streaming_to_start(page)
    wait_for_message_streaming_to_stop(page)
    message = page.locator("div.message-content").last.inner_text()
    return message


def wait_for_message_streaming_to_start(page, timeout=10000):
    try:
        print("Waiting for message streaming to start")
        page.wait_for_selector("#stop-button", state="visible", timeout=timeout)
        print("Message streaming started")
    except TimeoutError:
        print("Timed out waiting for message streaming to start")


def wait_for_message_streaming_to_stop(page, timeout=60000):
    try:
        print("Waiting for message streaming to stop")
        page.wait_for_selector("#stop-button", state="hidden", timeout=timeout)
        print("Message streaming stopped")
    except TimeoutError:
        print("Timed out waiting for message streaming to stop")

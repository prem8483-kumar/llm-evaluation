import os
from pathlib import Path

from playwright.sync_api import sync_playwright
import pytest

AUTH_STATE_FILE = "okta_auth.json"
SKA_WEB_URL = "https://intg.smart-knowledge-assistant.starsaccount.com/"


@pytest.fixture(scope="session")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        if os.path.exists(Path.cwd() / AUTH_STATE_FILE):
            print("Reusing existing auth state")
            context = browser.new_context(storage_state=AUTH_STATE_FILE)
        else:
            print("Creating new auth state")
            context = browser.new_context()
            page = context.new_page()
            page.goto(SKA_WEB_URL)

            page.wait_for_selector("[id='chat-input']", timeout=120000)
            print("Logged in successfully!")

            context.storage_state(path=Path.cwd() / AUTH_STATE_FILE)
            print(f"Auth state saved to {AUTH_STATE_FILE}")

        yield context
        # browser.close()

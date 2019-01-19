from dotenv import load_dotenv
load_dotenv()

import os

from transferwise import TransferWise

# Environment variables
API_TOKEN = os.getenv("TRANSFERWISE_API_TOKEN")
SANDBOX_MODE = os.getenv("TRANSFERWISE_SANDBOX_MODE")

if __name__ == "__main__":
    transferwise = TransferWise(API_TOKEN, SANDBOX_MODE)

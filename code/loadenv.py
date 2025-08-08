import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# You can now use 'api_key' in your application
print(os.getenv("LANGEXTRACT_API_KEY"))

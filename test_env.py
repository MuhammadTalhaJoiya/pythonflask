from dotenv import load_dotenv
import os
from urllib.parse import quote

load_dotenv()

print("Testing environment variables:")
print(f"DB_USER: '{os.getenv('DB_USER')}'")
print(f"DB_PASSWORD: '{os.getenv('DB_PASSWORD')}'") 
print(f"DB_HOST: '{os.getenv('DB_HOST')}'")
print(f"DB_NAME: '{os.getenv('DB_NAME')}'")

# Test URI construction
if all([os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), os.getenv('DB_HOST'), os.getenv('DB_NAME')]):
    uri = f"mysql+pymysql://{os.getenv('DB_USER')}:{quote(os.getenv('DB_PASSWORD'))}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    print(f"\n✅ Database URI: {uri}")
else:
    print("\n❌ Some environment variables are missing!")
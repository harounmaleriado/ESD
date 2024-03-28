import time
from sqlalchemy.exc import OperationalError
from main.models.review_model import db  

def wait_for_mysql(retries=5, delay=5):
    """Wait for MySQL to become ready by attempting to query the database."""
    attempt = 0
    while attempt < retries:
        try:
            db.engine.execute('SELECT 1')
            print("MySQL is ready!")
            return True
        except OperationalError as e:
            print(f"MySQL not ready, retrying in {delay} seconds...")
            attempt += 1
            time.sleep(delay)
    print("MySQL was not ready after maximum retries. Exiting.")
    return False

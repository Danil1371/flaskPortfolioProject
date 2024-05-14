from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(join(dirname(__file__), '.env'))

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()

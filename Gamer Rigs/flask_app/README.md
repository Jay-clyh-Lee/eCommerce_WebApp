Edit .env

DEBUG_STATUS=""
SECRET_KEY=""
DB_USER=""
DB_PASSWORD=""
TEST=""
API=""

INSTALL under pipenv:
flask
PyMySQL
flask-bcrypt
python-dotenv

CMD:
pipenv shell
pipenv install flask PyMySQL flask-bcrypt python-dotenv
pipenv graph
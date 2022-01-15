from flask_app import app
from flask_app.controllers import users, trees
import os

if __name__ == '__main__':
    print(os.environ.get("TEST"))
    app.run(debug=bool(os.environ.get("DEBUG_STATUS")))
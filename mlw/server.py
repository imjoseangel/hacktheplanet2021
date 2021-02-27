"""
Main module of the server file
"""
from flask import render_template
from waitress import serve

# local modules
import config

# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")

# Create a URL route in our application for "/"


@connex_app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:8080/

    :return:        the rendered template "home.html"
    """
    return render_template("index.html")


@connex_app.route("/locations")
def locations():
    return render_template('locations.html')


if __name__ == "__main__":
    # connex_app.run(debug=True)
    serve(connex_app.app)

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
    return render_template("home.html")


@connex_app.route("/graph1")
def graph1():
    """
    This function just responds to the browser URL
    localhost:5000/people

    :return:        the rendered template "people.html"
    """
    return render_template("graph1.html")


if __name__ == "__main__":
    # connex_app.run(debug=True)
    serve(connex_app.app)

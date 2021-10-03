from flask import Flask, render_template


# GENERATES THE APP THAT ALL OTHER CODE USES
app = Flask(__name__)

# SECRET KEY FOR THE APP
app.config["SECRET_KEY"] = "39919f90eac849c3374896ba"

# ALLOWS THE PROGRAM TO CONNECT TO THE DIFFERENT ROUTES
from SustainabilityWebsite import routeHandler

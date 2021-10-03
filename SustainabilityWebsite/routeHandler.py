from flask import render_template, redirect, url_for, flash, request, jsonify, make_response
import json
from SustainabilityWebsite import app
from SustainabilityWebsite.buttonInputHandler import TripHandler
from SustainabilityWebsite.calculationHandler import getEmissions, getFlightData
from SustainabilityWebsite.audioRequestHandler import AudioFile
from SustainabilityWebsite.runML import runML

# EXTRA LOGGING FUNCTIONALITY
import logging

logging.basicConfig(level=logging.DEBUG)


# ADDS FUNCTIONALITY TO WHAT IS LOADED WHEN THE ROOTS ARE ADDED
@app.route('/', methods=["GET", "POST"], endpoint='home_page')
@app.route('/index.html')
def home_page():
    # CREATE THE FORM FOR ENTERING THE DEPARTURE AND DESTINATION AIRPORTS
    form = TripHandler()

    return render_template("index.html", form=form)


# LIST OUT THE AVAILABLE FLIGHTS IN BLOCKS
@app.route('/flights', methods=['POST'])
def flight_list(destination="JFK", departure="LAX", date="2021-10-02"):
    # GET THE VALUES PASSED FROM AJAX TO THE SERVER SIDE PYTHON FUNCTION
    destination = request.form.get("destination")
    departure = request.form.get("departure")
    date = f'{request.form.get("year")}-{request.form.get("month")}-{request.form.get("day")}'

    if request.form.get("economy"):
        seatClass = 1
    elif request.form.get("business"):
        seatClass = 2
    elif request.form.get("first_class"):
        seatClass = 3

    # GET ALL FLIGHT DETAILS FROM THE API
    all_flight_details = getFlightData(destination, departure, date, seatClass)

    # INITIALIZE A DICTIONARY TO HOLD ALL THE FLIGHT VALUES
    flight_dictionary = {}

    app.logger.info(all_flight_details)

    # ITERATE THROUGH ALL OF THE FLIGHTS FROM THE ARRAY
    for i in all_flight_details:
        distance = i[1]  # GET THE DISTANCES OF THE FLIGHTS

        # GET THE EMISSIONS OF THE FLIGHT AND APPEND TO I
        flightEmissions = getEmissions(distance, seatClass)
        i.append(round(flightEmissions, 2))

        # APPEND THE VALUES OF EMISSIONS TO THE DICTIONARY
        flight_dictionary[i[0]] = i

    app.logger.info(flight_dictionary)

    return jsonify(flight_dictionary)


# RECORD THE SPEECH OF THE USER
@app.route('/record', methods=['POST'])
def record():
    # INSTANTIATE AN A RECORDER CLASS
    newRecording = AudioFile()

    # BEGIN RECORDING
    newRecording.record()

    # MAKE THE API CALL TO THE SPEECH PARSER API
    spokenWordsText = newRecording.upload_file()
    newRecording.removeFile()
    app.logger.info(spokenWordsText)

    list_items = runML(r"C:\Users\Tal\PycharmProjects\FlaskSustainabilityProject\SustainabilityWebsite/", spokenWordsText)

    app.logger.info(list_items)


    dep_airport = list_items[-1][1][-3:].upper()
    dest_airport = list_items[-2][1][-3:].upper()
    dest_dep_dict = {}
    dest_dep_dict["dep"] = dep_airport
    dest_dep_dict["dest"] = dest_airport

    return jsonify(dest_dep_dict)


@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('404.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp

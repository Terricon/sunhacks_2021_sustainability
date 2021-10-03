from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class TripHandler(FlaskForm):
    # TWO CLASS VARIABLES TO HOLD THE INFORMATION REGARDING THE TRIP DATA
    departure_airport = StringField(label="Departure Airport:", validators=[DataRequired()])
    destination_airport = StringField(label="Destination Airport", validators=[DataRequired()])

    # DATE HANDLER
    # departure_date =

    # SUBMIT FIELD
    find_trips = SubmitField(label="Find me a trip!")

    # TWO BUTTONS FOR THE RENDERING
    startRecord = SubmitField(label="record")
    stopRecord = SubmitField(label="stop recording")

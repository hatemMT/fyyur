from datetime import datetime

from flask_wtf import Form
from wtforms import StringField, SelectField, \
    SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, URL, AnyOf, Regexp

from lookups import states, genres


class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )


class VenueForm(Form):
    selected_genres = ['Other']

    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            (state, state) for state in states
        ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone',
        validators=[
            Regexp(
                "\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|; 2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|; 4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}")
        ]
    )
    image_link = StringField(
        'image_link',
        validators=[URL()]
    )

    genres = SelectMultipleField(
        'genres[]', validators=[DataRequired()],
        choices=[(g, g) for g in genres]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )


class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            (state, state) for state in states
        ]
    )
    phone = StringField(
        'phone', validators=[
            Regexp(
                "\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|; 2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|; 4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}")
        ]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres[]', validators=[DataRequired(), AnyOf(
            (g, g) for g in genres
        )],
        choices=[(g, g) for g in genres]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )

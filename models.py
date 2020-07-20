from init import db
from sqlalchemy import or_


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())
    genres = db.Column(db.String())

    shows = db.relationship('Show', backref="venue")

    def __repr__(self):
        return f'''<Venue id={self.id} 
                    name={self.name} 
                >'''


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))

    genres = db.Column(db.String())


    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())

    shows = db.relationship('Show', backref="artist")

    def __repr__(self):
        return f'''<Artist id={self.id} 
                    name={self.name} 
                >'''


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    time = db.Column(db.DateTime)

    def __repr__(self):
        return f'''<Show id={self.id} 
                    artist_id={self.artist_id} 
                    artist_name={self.artist.name} 
                    venue_id={self.venue_id}
                    venue_name={self.venue.name}
                >'''

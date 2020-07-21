from flask import render_template, request, flash, redirect, url_for

from forms import *
from init import *
from models import *

HOME_TEMPLATE = 'pages/home.html'


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template(HOME_TEMPLATE)


#  Venues
#  ----------------------------------------------------------------

def map_to_vo(data):
    mapped = []
    for v in data:
        group_itr = filter(lambda i, city=v.city: i["city"] == city, mapped)
        try:
            group = next(group_itr)
            group["venues"].append(v)
        except StopIteration as e:
            group = {
                "city": v.city,
                "state": v.state
            }
            mapped.append(group)
            group["venues"] = []
            group["venues"].append(v)
    return mapped


def size(itr):
    return sum(1 for i in itr)


@app.route('/venues')
def venues():
    upcoming_query = db.session \
        .query(db.func.count(Show.id)) \
        .filter(Show.venue_id == Venue.id) \
        .filter(Show.time > db.func.now())

    venues_list = db.session \
        .query(Venue.id, Venue.city, Venue.state, Venue.name,
               upcoming_query.label("num_upcoming_shows")) \
        .order_by(Venue.id) \
        .all()

    data = map_to_vo(venues_list)
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    upcoming_query = db.session \
        .query(db.func.count(Show.id)) \
        .filter(Show.venue_id == Venue.id) \
        .filter(Show.time > db.func.now())

    search_term = request.form.get('search_term', '')
    response = {
        "count": db.session.query(Venue)
            .filter(Venue.name.ilike(f'%{search_term}%'))
            .count(),
        "data": db.session.query(Venue.id, Venue.name, upcoming_query.label('num_upcoming_shows'))
            .filter(Venue.name.ilike(f'%{search_term}%'))
            .all()
    }

    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    data = db.session.query(Venue).filter(Venue.id == venue_id).one()
    data.past_shows = db.session \
        .query(Artist.id.label('artist_id'), Artist.name.label('artist_name'),
               Artist.image_link.label('artist_image_link'),
               Show.time.label('start_time')) \
        .join(Artist) \
        .filter(Show.venue_id == venue_id) \
        .filter(Show.time <= db.func.now()).all()
    data.upcoming_shows = db.session \
        .query(Artist.id.label('artist_id'), Artist.name.label('artist_name'),
               Artist.image_link.label('artist_image_link'),
               Show.time.label('start_time')) \
        .join(Artist) \
        .filter(Show.venue_id == venue_id) \
        .filter(Show.time > db.func.now()).all()
    data.past_shows_count = len(data.past_shows)
    data.upcoming_shows_count = len(data.upcoming_shows)
    data.genres = data.genres.split(',')
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    data = {
        "name": request.form['name'],
        "city": request.form['city'],
        "state": request.form['state'],
        "address": request.form['address'],
        "phone": request.form['phone'],
        "facebook_link": request.form['facebook_link'],
        "genres": ','.join(request.form.getlist('genres'))
    }
    new_venue = Venue(**data)
    try:
        db.session.add(new_venue)
        db.session.commit()
        db.session.close()
        flash('Venue ' + request.form['name'] + ' was successfully listed')
    except:
        flash('An error occurred. Venue ' + data["name"] + ' could not be listed.')

    return render_template(HOME_TEMPLATE)


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    Venue.query.filter(Venue.id == venue_id).delete()
    return redirect(HOME_TEMPLATE)


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data = db.session.query(Artist.id, Artist.name).all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get("search_term", "")
    upcoming_query = db.session \
        .query(db.func.count(Show.id)) \
        .filter(Show.artist_id == Artist.id) \
        .filter(Show.time > db.func.now())

    response = {
        "count": db.session.query(Artist)
            .filter(Artist.name.ilike(f'%{search_term}%'))
            .count()
        ,
        "data": db.session.query(Artist.id, Artist.name, upcoming_query.label('num_upcoming_shows'))
            .filter(Artist.name.ilike(f'%{search_term}%'))
    }
    return render_template('pages/search_artists.html', results=response,
                           search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    data = db.session.query(Artist).filter(Artist.id == artist_id).one()
    data.past_shows = db.session \
        .query(Venue.id.label('venue_id'), Venue.name.label('venue_name'),
               Venue.image_link.label('venue_image_link'),
               Show.time.label('start_time')) \
        .join(Venue) \
        .filter(Show.artist_id == artist_id) \
        .filter(Show.time <= db.func.now()).all()
    data.upcoming_shows = db.session \
        .query(Venue.id.label('venue_id'), Venue.name.label('venue_name'),
               Venue.image_link.label('venue_image_link'),
               Show.time.label('start_time')) \
        .join(Venue) \
        .filter(Show.artist_id == artist_id) \
        .filter(Show.time > db.func.now()).all()
    data.past_shows_count = len(data.past_shows)
    data.upcoming_shows_count = len(data.upcoming_shows)
    data.genres = data.genres.split(',')
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist = Artist.query.get(artist_id)
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.phone = request.form['phone']
    artist.genres = ','.join(request.form.getlist('genres'))
    artist.facebook_link = request.form['facebook_link']
    db.session.commit()
    db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(selected_genres=venue.genres.split(','))
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.genres = ','.join(request.form.getlist('genres'))
    venue.facebook_link = request.form['facebook_link']
    db.session.commit()
    db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    data = {
        "name": request.form['name'],
        "city": request.form['city'],
        "state": request.form['state'],
        "phone": request.form['phone'],
        "facebook_link": request.form['facebook_link'],
        "genres": ','.join(request.form.getlist('genres'))
    }
    new_artist = Artist(**data)
    try:
        db.session.add(new_artist)
        db.session.commit()
        db.session.close()
        flash('Artist ' + request.form['name'] + ' was successfully listed')
    except:
        flash('An error occurred. Artist ' + data["name"] + ' could not be listed.')

    return render_template(HOME_TEMPLATE)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    data = db.session.query(Artist.id.label('artist_id'), Artist.name.label('artist_name'),
                            Artist.image_link.label('artist_image_link'),
                            Venue.id.label('venue_id'), Venue.name.label('venue_name'),
                            Show.time.label('start_time')) \
        .join(Artist).join(Venue).all()
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/search', methods=['POST'])
def search_shows():
    search_term = request.form.get('search_term', '')
    response = {
        "count": db.session.query(Show)
            .join(Artist).join(Venue)
            .filter(or_(Venue.name.ilike(f'%{search_term}%'), Artist.name.ilike(f'%{search_term}%')))
            .count(),
        "data": db.session.query(Show.id, Venue.name.label('venue_name'), Artist.name.label('artist_name'),
                                 Show.time.label('start_time'))
            .join(Artist).join(Venue)
            .filter(or_(Venue.name.ilike(f'%{search_term}%'), Artist.name.ilike(f'%{search_term}%')))
            .all()
    }

    return render_template('pages/search_shows.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    new_show = Show(artist_id=request.form['artist_id'],
                    venue_id=request.form['venue_id'],
                    time=datetime.strptime(request.form['start_time'], '%Y-%m-%d %H:%M:%S')
                    )
    try:
        db.session.add(new_show)
        db.session.commit()
        db.session.close()
        flash('Show was successfully listed!')
    except:
        flash('An error occurred. Show could not be listed.')
    return render_template(HOME_TEMPLATE)


# Errors Handling
# -----------------------------------

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URLForm
from .models import URL_map
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        short = form.custom_id.data or get_unique_short_id()
        url_map = URL_map(
            original=form.original_link.data,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        return render_template('index.html', form=form, short=short), 200
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def short_view(short):
    return redirect(
        URL_map.query.filter_by(short=short).first_or_404().original)

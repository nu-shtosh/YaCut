# yacut/models.py
from datetime import datetime

from flask import url_for

from . import db


class URL_map(db.Model):
    """id — поле для ID,
    original — поле для оригинальной длинной ссылки,
    short — поле для короткого идентификатора,
    timestamp — поле для временной метки."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(6), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('redirect_view', short=self.short, _external=True)
        )

    def only_url_to_dict(self):
        return dict(
            url=self.original,
        )
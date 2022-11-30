import json
from textwrap import shorten

from peewee import (Model, SqliteDatabase, FloatField, TextField, IntegerField, BooleanField, DateField,
                    TimestampField, ForeignKeyField, CompositeKey, BlobField, IntegrityError)

from books4 import config
import pendulum

database = SqliteDatabase(config.database)


class BaseModel(Model):
    """A base model that will use our Sqlite database."""

    class Meta:
        database = database


class Goodreads(BaseModel):
    author = TextField(null=True)
    average_rating = FloatField(null=True)
    best_book_id = TextField(null=True)
    description = TextField(null=True)
    goodreads_id = TextField(null=True)
    image_url = TextField(null=True)
    image_url2 = TextField(null=True)
    ratings_count = IntegerField(null=True)
    title = TextField(null=True)
    url = TextField(null=True)
    publication_year = IntegerField(null=True)
    num_pages = IntegerField(null=True)
    isbns = TextField(null=True)
    ratings_count5 = IntegerField(null=True)
    ratings_count4 = IntegerField(null=True)
    ratings_count3 = IntegerField(null=True)
    ratings_count2 = IntegerField(null=True)
    ratings_count1 = IntegerField(null=True)
    ratings_count5_pct = IntegerField(null=True)
    ratings_count4_pct = IntegerField(null=True)
    ratings_count3_pct = IntegerField(null=True)
    ratings_count2_pct = IntegerField(null=True)
    ratings_count1_pct = IntegerField(null=True)

    class Meta:
        table_name = 'goodreads'

    def __str__(self):
        return f'{shorten(str(self.title), 30)} by {shorten(str(self.author), 20)}'

    def __repr__(self):
        return f'{self.id}: {shorten(str(self.title), 30)} by {shorten(str(self.author), 20)}'

    def isbns_list(self):
        isbns = []
        if self.isbns:
            isbns = json.loads(str(self.isbns))
        return isbns

    def rating_dist(self):
        if not self.ratings_count:
            return
        dist = [
            ('5', self.ratings_count5, self.ratings_count5_pct),
            ('4', self.ratings_count4, self.ratings_count4_pct),
            ('3', self.ratings_count3, self.ratings_count3_pct),
            ('2', self.ratings_count2, self.ratings_count2_pct),
            ('1', self.ratings_count1, self.ratings_count1_pct),
        ]
        return dist


class Book(BaseModel):
    goodreads = ForeignKeyField(model=Goodreads, backref='books', null=True)
    author = TextField(null=True)
    best_image = TextField(null=True)
    category_str = TextField(null=True)
    file_format = TextField(null=True)
    goodreads_searched = IntegerField(null=True)
    hidden = BooleanField(null=True)
    image_url = TextField(null=True)
    keywords_str = TextField(null=True)
    language = TextField(null=True)
    post_date = DateField()
    post_title = TextField(null=True)
    recommended = BooleanField(null=True)
    timestamp = TimestampField()
    title = TextField(null=True)
    url = TextField(unique=True)

    class Meta:
        table_name = 'books'

    def __str__(self):
        return f'{shorten(str(self.title), 30)} by {shorten(str(self.author), 20)}'

    def __repr__(self):
        return f'<Book2: {self.id}> {shorten(str(self.title), 30)} by {shorten(str(self.author), 20)}'

    @property
    def post_date_p(self):
        return pendulum.parse(str(self.post_date))

    @property
    def post_date_short(self):
        s = self.post_date_p.diff_for_humans(absolute=True)
        split = s.split(' ')
        if len(split) > 1:
            s = split[0] + split[1][0]

        return s

    @property
    def date_added(self) -> pendulum.DateTime:
        return pendulum.from_timestamp(self.timestamp.timestamp(), tz=pendulum.tz.get_local_timezone())

    @property
    def keywords_list(self):
        if self.keywords_str:
            return json.loads(str(self.keywords_str))
        else:
            return []

    @property
    def category_list(self):
        if self.category_str:
            return json.loads(str(self.category_str))
        else:
            return []

    @property
    def category_text(self):
        if self.category_str:
            return ', '.join(json.loads(str(self.category_str)))
        else:
            return ''

    @property
    def keywords_text(self):
        if self.keywords_str:
            return ', '.join(json.loads(str(self.keywords_str)))
        else:
            return ''

    def title_author(self, short=False):
        t, a = self.title or '', self.author or ''
        if short:
            t = shorten(t, 30)
            a = shorten(a, 20)
        return f'{t} - {a}'

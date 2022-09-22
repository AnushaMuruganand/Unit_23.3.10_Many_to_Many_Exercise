"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8Pe2gx8Z68Cs0vGplXvVBmSSKiA7yfijA4A&usqp=CAU"


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """ User. """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False, unique=True)

    last_name = db.Column(db.String(50), nullable=False, unique=True)

    image_url = db.Column(db.Text, nullable=False, default = DEFAULT_IMAGE_URL)

    # ADDING RELATIONSHIP BETWEEN "User" and "Post" MODELS
    # We set "casade" as When a user is deleted, the related posts should be deleted, too. or elese an "Integrity Error" occurs because of FOREIGB-KEY constraint we set up on "posts" table
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    # Adding a "property" class, which allows us to create a property for this class so we can access as "User.propertyname". "propertyname" is same as the function name we define here. Here we access this as "User.full_name"
    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """ POST. """

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    title = db.Column(db.Text, nullable = False)

    content = db.Column(db.Text, nullable = False)

    # date+time automatically default to the when the post is created
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def formatted_date(self):
        """Return nicely-formatted date."""

        # %a is The abbreviated weekday name according to the current locale.
        # %b is The abbreviated month name according to the current locale.
        # %d is The day of the month(range 01 to 31).
        # %Y is The year 
        # %I is The hour using a 12-hour clock (range 01 to 12).
        # %M is The minute(range 00 to 59).
        # %p is Either `AM' or `PM'. Noon is treated as `pm' and midnight as `am'.
        return self.created_at.strftime("%a %b %d  %Y, %I:%M %p")

class Tag(db.Model):
    """ Tag """

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text, nullable = False, unique = True)

    posts = db.relationship('Post', secondary = "posts_tags", backref = "tags")
    

class PostTag(db.Model):
    """ PostTag """

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True)




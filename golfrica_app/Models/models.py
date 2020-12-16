from golfrica_app import db, ma, bcrypt
from flask_serialize import FlaskSerializeMixin
from datetime import datetime
from random import random
from sqlalchemy.orm import class_mapper
import sqlalchemy
import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy_serializer import SerializerMixin

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and not x.startswith('query')]:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    email_verified_at = db.Column(db.String(150), nullable=True)
    password = db.Column(db.String(200), nullable=False)
    profile_image = db.Column(db.String(200), nullable=True)
    profile_description = db.Column(db.Text, nullable=True)
    login_type = db.Column(db.Integer, default=0)
    created_at = db.Column(db.String(50), nullable=True)
    updated_at = db.Column(db.String(50), nullable=True)

    def __init__(self, first_name, last_name, email, password, login_type):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.login_type = login_type



class UserSchema(ma.Schema):
    class Meta:
        fields = [prop.key for prop in class_mapper(User).iterate_properties
        if isinstance(prop, sqlalchemy.orm.ColumnProperty)]

class LoginDevice(db.Model):
    __tablename__ = "login_devices"
    login_id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(200), nullable=False)
    device_name = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, default=0)
    created_at = db.Column(db.String(50), nullable=True)
    updated_at = db.Column(db.String(50), nullable=True)

    def __init__(self, device_name, token, user_id, updated_at):
        # token = str(datetime.now())+random(0,1000)+str(datetime.now())
        self.token = bcrypt.generate_password_hash(token)
        self.device_name = device_name
        self.user_id = user_id
        self.created_at = str(datetime.now())
        self.updated_at = updated_at

class LoginDeviceSchema(ma.Schema):
    class Meta:
        fields = [prop.key for prop in class_mapper(LoginDevice).iterate_properties
        if isinstance(prop, sqlalchemy.orm.ColumnProperty)]



class Status(db.Model):
    __tablename__ = "statuses"
    status_id = db.Column(db.Integer, primary_key=True)
    status_description = db.Column(db.Text, nullable=False)
    status_media = db.Column(db.Text, nullable=True)
    status_link = db.Column(db.String(200), nullable=True)
    status_sm_id = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, default=0)
    club_id = db.Column(db.Integer, default=0)
    player_id = db.Column(db.Integer, default=0)
    is_app_status = db.Column(db.Integer, default=0)
    is_sm_status = db.Column(db.Integer, default=0)
    is_club_status = db.Column(db.Integer, default=0)
    is_player_status = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Float, default=0.0)
    status_sm_likes = db.Column(db.Integer, default=0)
    status_sm_comments = db.Column(db.Integer, default=0)
    status_sm_shares = db.Column(db.Integer, default=0)
    created_at = db.Column(db.String(50), nullable=True)
    updated_at = db.Column(db.String(50), nullable=True)


class Club(db.Model):
    __tablename__ = "clubs"
    club_id = db.Column(db.Integer, primary_key=True)
    club_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    club_country = db.Column(db.String(100), nullable=False)
    club_union_federation = db.Column(db.String(100), nullable=False)
    club_profile_pic = db.Column(db.Text, nullable=True)
    club_cover_pic = db.Column(db.Text, nullable=True)
    web_link = db.Column(db.Text, nullable=True)
    fb_link = db.Column(db.Text, nullable=True)
    twitter_link = db.Column(db.Text, nullable=True)
    instagram_link = db.Column(db.Text, nullable=True)
    whatsapp_number = db.Column(db.String(50), nullable=True)
    address = db.Column(db.Text, nullable=True)
    postal_address = db.Column(db.String(100), nullable=True)
    holes_9_or_18 = db.Column(db.Integer, nullable=True)
    public_or_private = db.Column(db.String(50), nullable=True)
    fb_followers = db.Column(db.Integer, nullable=True)
    twitter_followers = db.Column(db.Integer, nullable=True)
    insta_followers = db.Column(db.Integer, nullable=True)
    coordinates = db.Column(db.String(200), nullable=True) #longitude and latitude

    ##not part of the model

class ClubDescription(db.Model):
    __tablename__ = "club_description"
    des_id = db.Column(db.Integer, primary_key=True)
    des_text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, default=0)
    club_id = db.Column(db.Integer, default=0)
    des_media = db.Column(db.Text, nullable=True)

class ClubDesSchema(ma.Schema):
    class Meta:
        fields = [prop.key for prop in class_mapper(ClubDescription).iterate_properties
        if isinstance(prop, sqlalchemy.orm.ColumnProperty)]
        fields = fields + ['first_name', 'last_name', 'profile_image']

class StatusSchema(ma.Schema):
    class Meta:
        fields = [prop.key for prop in class_mapper(Status).iterate_properties
        if isinstance(prop, sqlalchemy.orm.ColumnProperty)]
        fields = fields + [prop.key for prop in class_mapper(Club).iterate_properties
        if isinstance(prop, sqlalchemy.orm.ColumnProperty)]
        fields = fields + ['total_likes', 'total_swaps', 'total_comments','avg_rating']


class Country(db.Model):
    __tablename__ = "countries"
    country_id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.String(50), nullable=True)
    updated_at = db.Column(db.String(50), nullable=True)

class CountrySchema(ma.Schema):
    class Meta:
        fields = [prop.key for prop in class_mapper(Country).iterate_properties
        if isinstance(prop, sqlalchemy.orm.ColumnProperty)]



class ClubSchema(ma.Schema):
    class Meta:
        fields = [prop.key for prop in class_mapper(Club).iterate_properties
        if isinstance(prop, sqlalchemy.orm.ColumnProperty)]
        fields = fields + ['followers','total_reviews','avg_rating','followers','is_followed']


class Like(db.Model):
    __tablename__ = "likes"
    like_id = db.Column(db.Integer, primary_key=True)
    is_status = db.Column(db.Integer, default=0)
    is_player = db.Column(db.Integer, default=0)
    is_club = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, default=0)
    status_id = db.Column(db.Integer, default=0)
    player_id = db.Column(db.Integer, default=0)
    club_id = db.Column(db.Integer, default=0)
    created_at = db.Column(db.String(50), nullable=True)
    updated_at = db.Column(db.String(50), nullable=True)

class LikeSchema(ma.Schema):
    class Meta:
        fields = [prop.key for prop in class_mapper(Like).iterate_properties
        if isinstance(prop, sqlalchemy.orm.ColumnProperty)]

class Comment(db.Model):
    __tablename__ = "comments"
    comment_id = db.Column(db.Integer, primary_key=True)
    is_status = db.Column(db.Integer, default=0)
    is_player = db.Column(db.Integer, default=0)
    is_club = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, default=0)
    status_id = db.Column(db.Integer, default=0)
    player_id = db.Column(db.Integer, default=0)
    club_id = db.Column(db.Integer, default=0)
    comment = db.Column(db.Text, default=0)
    rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.String(50), nullable=True)
    updated_at = db.Column(db.String(50), nullable=True)

class CommentSchema(ma.Schema):
    class Meta:
        fields = [prop.key for prop in class_mapper(Comment).iterate_properties
        if isinstance(prop, sqlalchemy.orm.ColumnProperty)]

        fields = fields + ['user_id','profile_image', 'first_name','last_name']

class Swap(db.Model):
    __tablename__ = "swaps"
    swap_id = db.Column(db.Integer, primary_key=True)
    is_status = db.Column(db.Integer, default=0)
    is_player = db.Column(db.Integer, default=0)
    is_club = db.Column(db.Integer, default=0)

    swaper_id = db.Column(db.Integer, default=0)
    swaped_with_id = db.Column(db.Integer, default=0)

    status_id = db.Column(db.Integer, default=0)
    player_id = db.Column(db.Integer, default=0)
    club_id = db.Column(db.Integer, default=0)

    is_accepted = db.Column(db.Integer, default=0)
    is_rejected = db.Column(db.Integer, default=0)
    is_expired = db.Column(db.Integer, default=0)
    is_reviewed = db.Column(db.Integer, default=0)
    review_rating = db.Column(db.Integer, default=0)
    review_desc = db.Column(db.Text, default=0)
    created_at = db.Column(db.String(50), nullable=True)
    updated_at = db.Column(db.String(50), nullable=True)

class SwapSchema(ma.Schema):
    class Meta:
        fields = [prop.key for prop in class_mapper(Swap).iterate_properties
        if isinstance(prop, sqlalchemy.orm.ColumnProperty)]

class Rating(db.Model):
    __tablename__ = "ratings"
    rating_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, default=0)
    is_club_rating = db.Column(db.Integer, default=0)
    is_player_rating = db.Column(db.Integer, default=0)
    club_id = db.Column(db.Integer, default=0)
    player_id = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    review = db.Column(db.Text, nullable=True)

class RatingSchema(ma.Schema):
    class Meta:
        fields = [prop.key for prop in class_mapper(Rating).iterate_properties
        if isinstance(prop, sqlalchemy.orm.ColumnProperty)]

class Follow(db.Model):
    __tablename__ = "follows"
    f_id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, default=0)
    followed_id = db.Column(db.Integer, default=0)
    is_club_followed = db.Column(db.Integer, default=0)
    is_player_followed = db.Column(db.Integer, default=0)
    is_user_followed = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)

class FollowSchema(ma.Schema):
    class Meta:
        fields = [prop.key for prop in class_mapper(Follow).iterate_properties
        if isinstance(prop, sqlalchemy.orm.ColumnProperty)]
        fields = fields + ['user_id','profile_image', 'first_name','last_name','is_followed','user_followers','users_followed']


class Player(db.Model):
    __tablename__ = "players"
    player_id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(200), nullable=False)
    club_id = db.Column(db.Integer, default=0)
    email = db.Column(db.String(200), nullable=False)
    player_profile_pic = db.Column(db.Text, nullable=True)
    player_cover_pic = db.Column(db.Text, nullable=True)
    web_link = db.Column(db.Text, nullable=True)
    fb_link = db.Column(db.Text, nullable=True)
    twitter_link = db.Column(db.Text, nullable=True)
    instagram_link = db.Column(db.Text, nullable=True)
    whatsapp_number = db.Column(db.String(50), nullable=True)
    address = db.Column(db.Text, nullable=True)
    postal_address = db.Column(db.String(100), nullable=True)
    fb_followers = db.Column(db.Integer, nullable=True)
    twitter_followers = db.Column(db.Integer, nullable=True)
    insta_followers = db.Column(db.Integer, nullable=True)

class PlayerSchema(ma.Schema):
    class Meta:
        fields = [prop.key for prop in class_mapper(Player).iterate_properties
        if isinstance(prop, sqlalchemy.orm.ColumnProperty)]
        fields = fields + ['user_id','profile_image', 'first_name','last_name','is_followed','followers']









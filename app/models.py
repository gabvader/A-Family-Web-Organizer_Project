from app import db, login_manager
from sqlalchemy import or_, and_
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


event_participants = db.Table(
    "event_users",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("event_id", db.Integer, db.ForeignKey("event.id"), primary_key=True),
)

class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    budget = db.Column(db.Float, default=0)
    # db.relationship() is a function relating two SQL classes, eg Family and User
    # User is the first argument of function, the target class of the relationship
    # backref creates back-reference from User class to Familiy
    # Now for any User object, I can access it associated Family by using family attribute, like user.family
    users = db.relationship('User', backref='family', lazy='dynamic')
    # Same for Event. Now I can access the Family of the event by event.family
    events = db.relationship('Event', backref='family', lazy='dynamic')
    shopping_list_items = db.relationship('ShoppingListItem', backref='family', lazy='dynamic')
    

    def __repr__(self):
        return f'<Family {self.name}>'

# UserMixin class provides  properties that are necessary for Flask-login
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    alias = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'))
    created_events = db.relationship('Event', backref='creator', lazy='dynamic')
    added_items = db.relationship('ShoppingListItem', backref='added_by_user', lazy='dynamic', foreign_keys='ShoppingListItem.added_by_user_id')
    purchased_items = db.relationship('ShoppingListItem', backref='purchased_by_user', lazy='dynamic', foreign_keys='ShoppingListItem.purchased_by_user_id')
    
    # Here we implement a few methods for the User class 
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
       return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User name={self.username}, email={self.email}>'
    
    def get_events_for_day(self, date):
        # Here I use the SQLalchemy or_ / and_ objects
        return self.participating_events.filter(
            or_(
                # This is the case if the event spans through more days
                and_(Event.start_date <= date, Event.end_date > date),
                # This is the case if the event starts and ends at the same day
                and_(Event.start_date == date, Event.end_date == date)
            )
        )
    
    
    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('event_type.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    whole_family= db.Column(db.Boolean, default=True)
    participants = db.relationship('User', secondary=event_participants, backref=db.backref('participating_events', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Event {self.title}>'


class ShoppingListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    is_purchased = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float, nullable=True)
    # foreign key column that stores the user ID of the person who added the item to the shopping list. 
    # It is a direct reference to the User table's id column.
    added_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    purchased_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'))
    


class EventType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    events = db.relationship('Event', backref='event_type', lazy='dynamic')
    

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
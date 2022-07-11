import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    isAdmin = db.Column(db.Boolean(), nullable=False, default=False) 
    webshops = db.relationship('WebShop', secondary='user_webshops', back_populates='users')

class WebShop(db.Model):
    __tablename__ = 'webshops'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    users = db.relationship('User', secondary='user_webshops', back_populates='webshops')

class UserWebShop(db.Model):
    __tablename__ = 'user_webshops'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    webshop_id = db.Column(db.Integer, db.ForeignKey('webshops.id'))


class Screenshot(db.Model):
    __tablename__ = 'screenshots'

    id = db.Column(db.Integer, primary_key=True)
    screenshot_file = db.Column(db.Text, nullable=False) 


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price_current = db.Column(db.Float, nullable=False)
    price_reference = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime(), nullable=False)

    webshop_id = db.Column(db.Integer, db.ForeignKey('webshops.id'),
        nullable=False)

    webshop = db.relationship('Webshop',
        backref=db.backref('webshops', useList=False))

    screenshot_id = db.Column(db.Integer, db.ForeignKey('screenshots.id'),
        nullable=False)

    screenshot = db.relationship('Screenshot',
        backref=db.backref('screenshots', useList=False))
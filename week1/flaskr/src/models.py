from enum import unique
import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    username = db.Column(db.String(50), nullable=False, unique=True)
    isAdmin = db.Column(db.Boolean(), nullable=False, default=False) 
    webshops = db.relationship('WebShop', secondary='user_webshops', back_populates='users')

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class WebShop(db.Model): 
    __tablename__ = 'webshops'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    users = db.relationship('User', secondary='user_webshops', back_populates='webshops')

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class UserWebShop(db.Model):
    __tablename__ = 'user_webshops'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    webshop_id = db.Column(db.Integer, db.ForeignKey('webshops.id'))


class Screenshot(db.Model):
    __tablename__ = 'screenshots'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    screenshot_file = db.Column(db.Text, nullable=False)

    
    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    article_number = db.Column(db.String(255), nullable=True)
    price_current = db.Column(db.Float, nullable=False)
    price_reference = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime(), nullable=False)

    webshop_id = db.Column(db.Integer, db.ForeignKey('webshops.id'),
        nullable=False)

    webshop = db.relationship('WebShop')

    screenshot_id = db.Column(db.Integer, db.ForeignKey('screenshots.id'),
        nullable=False)

    screenshot = db.relationship('Screenshot')

    scraper_id = db.Column(db.Integer, db.ForeignKey('scrapers.id'),
        nullable=True)

    scraper = db.relationship('Scraper')

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    def serialize(self):
       return {
            'id': self.id,
            'name': self.name,
            'article_number': self.article_number,
            'price_current': self.price_current,
            'price_reference': self.price_reference,
            'screenshot': self.screenshot.name,
            'webshop': self.webshop.name,
            'date': self.date.strftime("%d-%m-%Y, %H:%M:%S")
       }

class Scraper(db.Model):
    __tablename__ = 'scrapers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(), nullable=False, unique=True)
    start_date = db.Column(db.DateTime(), nullable=False)
    end_date = db.Column(db.DateTime(), nullable=False)
    last_scanned = db.Column(db.DateTime(), nullable=True)


    webshop_id = db.Column(db.Integer, db.ForeignKey('webshops.id'),
        nullable=False)

    webshop = db.relationship('WebShop')

    products = db.relationship("Product")

    @classmethod
    def find_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    def serialize(self):
       return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'start_date': self.start_date.strftime("%d-%m-%Y, %H:%M:%S"),
            'end_date': self.end_date.strftime("%d-%m-%Y, %H:%M:%S"),
            'last_scanned': self.last_scanned,
            'webshop': self.webshop.name
       }
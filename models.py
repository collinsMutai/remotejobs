from sqlalchemy import Column, String, Integer,  create_engine
from flask_sqlalchemy import SQLAlchemy


database_name = "jobs"
database_path = "postgresql://{}:{}@{}/{}".format(
    "postgres", "7749", "localhost:5432", database_name
)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Jobs(db.Model):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    city = Column(String)
    # date = db.Column(db.DateTime())

    def __init__(self, title, city):
        self.title = title
        self.city = city
        # self.date = date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "city": self.city
            # "date": self.date
        }



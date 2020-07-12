from flask_sqlalchemy import SQLAlchemy

# Create Db instance
Db = SQLAlchemy()


class User(Db.Model):
    # Fields
    __tablename__ = 'users'

    user_id = Db.Column(Db.Integer, primary_key=True, autoincrement=True)
    first_name = Db.Column(Db.String(64), nullable=False)
    age = Db.Column(Db.Integer, nullable=False)
    passhash = Db.Column(Db.String(64), nullable=False)
    # toString
    def toString(self):
        print(f"{self.user_id}: {self.first_name} ({self.age}) {self.passhash}")
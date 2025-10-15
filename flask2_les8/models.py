from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()



class user:
    # __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    quizes = db.relationship('quiez', 
                             backref = 'user',
                             cascade = "all, delete, delete-orphan", 
                             lazy = 'select')
    
class quiz:
    # __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

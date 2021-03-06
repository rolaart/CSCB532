from app import db
from app.models import User

def commit_db_transaction():
    db.session.commit()

def persist_model(object, commit_transaction=True):
    db.session.add(object)
    if commit_transaction:
        commit_db_transaction()


def delete_model(object):
    db.session.delete(object)
    commit_db_transaction()


def find_user_by_email(email):
    return User.query.filter_by(email=email).first()
    
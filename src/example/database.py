from .models import db


def get_all(model):
    data = model.query.all()
    return data


def add_instance(model, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)
    commit_changes()


def delete_instance(model, id):
    model.query.filter_by(id=id).delete()
    commit_changes()


def edit_instance(model, id, **kwargs):
    instance = model.query.filter_by(id=id).all()[0]
    for attr, new_value in kwargs.items():
        setattr(instance, attr, new_value)
    commit_changes()


def get_by_id(model, id):
    data = model.query.filter_by(id=id).first()
    return data


def get_by_email(model, email):
    data = model.query.filter_by(email=email).first()
    return data


def commit_changes():
    db.session.commit()

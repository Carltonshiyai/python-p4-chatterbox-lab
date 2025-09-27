#!/usr/bin/env python3

import pytest
from app import app, db
from models import Message
from faker import Faker

fake = Faker()

@pytest.fixture(autouse=True)
def setup_database():
    with app.app_context():
        db.create_all()
        if Message.query.count() == 0:
            for i in range(5):
                message = Message(
                    body=fake.sentence(),
                    username=fake.first_name()
                )
                db.session.add(message)
            db.session.commit()
        yield

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))
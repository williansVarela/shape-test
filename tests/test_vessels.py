import os
import sys

import pytest
from flask_migrate import Migrate

sys.path.append(os.path.join(os.path.dirname(__file__),'../'))

from sqlalchemy import func

from api.app import create_app
from api.models.vessel import Vessel
from config import db


@pytest.fixture(scope="module")
def app():
    app = create_app(test_config=True)
    
    with app.app_context():
        db.create_all()
        Migrate(app, db)

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_insert_clean_db(app):
    result = app.test_client().post('/vessel', json={'code':'MV102'})
    assert result.get_json().get('message') == 'OK'
    assert result.status_code == 201
    with app.app_context():
        query = db.session.query(Vessel.code)
        query_results = db.session.execute(query).all()
        assert query_results[0][0] == 'MV102'

def test_insert_replicated(app):
    result = app.test_client().post('/vessel', json={'code':'MV102'})
    assert result.get_json().get('message') == 'FAIL'
    assert result.status_code == 409
    with app.app_context():
        query = db.session.query(func.count(Vessel.code))
        query_results = db.session.execute(query).all()
        assert query_results[0][0] == 1

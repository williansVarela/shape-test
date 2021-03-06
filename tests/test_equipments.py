import os
import sys

import pytest
from flask_migrate import Migrate

sys.path.append(os.path.join(os.path.dirname(__file__),'../'))

from sqlalchemy import func, or_

from api.app import create_app
from api.models.equipment import Equipment, Operation
from api.models.vessel import Vessel
from config import db


@pytest.fixture(scope="module")
def app():
    app = create_app(test_config=True)
    
    with app.app_context():
        db.create_all()
        Migrate(app, db)
        vessel_obj1 = Vessel(code='MV102')
        vessel_obj2 = Vessel(code='MV101')
        db.session.add(vessel_obj1)
        db.session.add(vessel_obj2)
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_insert_clean_db(app):
    result = app.test_client().post('/equipment', json={'vessel_code':'MV102', 'code':'5310B9D7', 'location':'brazil', 'name':'compressor'})
    assert result.get_json().get('message') == 'OK'
    assert result.status_code == 201
    with app.app_context():
        query = db.session.query(Equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 1
        assert query_results[0][0].vessel_id == 1
        assert query_results[0][0].code == '5310B9D7'
        assert query_results[0][0].location == 'brazil'
        assert query_results[0][0].active
        assert query_results[0][0].name == 'compressor'

def test_insert_without_vessel_code(app):
    result = app.test_client().post('/equipment', json={'code':'5310B9D7', 'location':'brazil', 'name':'compressor'})
    assert result.get_json().get('message') == 'ERROR'
    assert result.status_code == 400
    with app.app_context():
        query = db.session.query(Equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 1

def test_insert_without_code(app):
    result = app.test_client().post('/equipment', json={'vessel_code':'MV102', 'location':'brazil', 'name':'compressor'})
    assert result.get_json().get('message') == 'ERROR'
    assert result.status_code == 400
    with app.app_context():
        query = db.session.query(Equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 1

def test_insert_without_location(app):
    result = app.test_client().post('/equipment', json={'vessel_code':'MV102', 'code':'5310B9D7', 'name':'compressor'})
    assert result.get_json().get('message') == 'ERROR'
    assert result.status_code == 400
    with app.app_context():
        query = db.session.query(Equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 1

def test_insert_without_name(app):
    result = app.test_client().post('/equipment', json={'vessel_code':'MV102', 'code':'5310B9D7', 'location':'brazil'})
    assert result.get_json().get('message') == 'ERROR'
    assert result.status_code == 400
    with app.app_context():
        query = db.session.query(Equipment)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 1

def test_status_active(app):
    result = app.test_client().get('/equipment/active')
    assert result.status_code == 200

def test_status_inactive(app):
    result = app.test_client().put('/equipment/inactive', json={"equipments": ["5310B9D7"]})
    assert result.get_json().get('message') == 'OK'
    assert result.status_code == 201

def test_insert_operation(app):
    result = app.test_client().post('/equipment/operation', json={"code": "5310B9D7", "type": "replacement", "cost": "1000"})
    assert result.get_json().get('message') == 'OK'
    assert result.status_code == 201
    with app.app_context():
        query = db.session.query(Operation)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 1

def test_operation_by_name(app):
    result = app.test_client().post('/equipment/operation/costs', json={'name': 'compressor'})
    assert result.status_code == 200

def test_operation_by_code(app):
    result = app.test_client().post('/equipment/operation/costs', json={'code': '5310B9D7'})
    assert result.status_code == 200

def test_operation_without_filter(app):
    result = app.test_client().post('/equipment/operation/costs', json={})
    assert result.status_code == 400

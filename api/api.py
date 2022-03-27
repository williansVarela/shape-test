from flask import Blueprint, request, jsonify

from api.models.equipment import equipment
from config import db

import logging


def log_info(message):
    pass


healthcheck_blueprint = Blueprint('healthcheck', __name__)
equipments_blueprint = Blueprint('equipments', __name__)


@healthcheck_blueprint.route('/', methods=['GET'])
def healthcheck():

    """Checks if the system is alive
        ---
        responses:
          200:
            description: OK if the system is alive
    """
    logging.basicConfig(format='%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Test the health of the system')
    return 'OK', 200


@equipments_blueprint.route('/insert_equipment', methods=['POST'])
def insert_equipment():
    """insert_equipment
        ---
        parameters:
            - name: vessel_code
              in: body
              type: string
              required: true
            - name: code
              in: body
              type: string
              required: true
            - name: name
              in: body
              type: string
              required: true
            - name: location
              in: body
              type: string
              required: true
        responses:
          201:
            description: returns OK if the equipment was correctly inserted
          400:
            description: Error
    """
    logging.basicConfig(format='%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Runing')
    return {'message':'OK'}, 201

@equipments_blueprint.route('/update_equipment_status', methods=['PUT'])
def update_equipment_status():
    """update_equipment_status
        ---
        parameters:
            - name: code
              in: body
              type: string
              required: true
        responses:
          201:
            description: returns OK if the equipments were correctly updated
          400:
            description: Error
    """
    logging.basicConfig(format='%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Runing')
    return {'message':'OK'}, 201

@equipments_blueprint.route('/active_equipments', methods=['GET'])
def active_equipment():
    """active_equipments
        ---
        parameters:
            - name: vessel_code
              in: query
              type: string
              required: true
        responses:
          200:
            description: returns a json with equipments key and a list of equipments
          400:
            description: error
    """
    logging.basicConfig(format='%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Runing')
    return {'message':'OK'}, 200

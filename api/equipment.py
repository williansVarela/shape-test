import logging

from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from api.models.equipment import Equipment, Operation
from api.models.vessel import Vessel
from config import db

equipments_blueprint = Blueprint('equipments', __name__)

@equipments_blueprint.route('', methods=['GET'])
def list_equipments():
    """List all existing equipments.
        ---
        responses:
          200:
            description: OK
    """
    logging.basicConfig(format='%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('list of equipments endpoint')

    equipment = Equipment.query.all()
    return jsonify([obj.to_dict() for obj in equipment]), 200


@equipments_blueprint.route('/<int:equipment_id>', methods=['GET'])
def view_equipment(equipment_id):
    """Retrieve information about one equipment, specified in the URL.
        ---
        parameters:
            - name: equipment_id
              in: body
              type: int
              required: true

        responses:
          200:
            description: OK
          404:
            description: Not found
    """
    logging.basicConfig(format='%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('View vessel endpoint')
    
    equipment = Equipment.query.get_or_404(equipment_id)
    return equipment.to_dict(), 200


@equipments_blueprint.route('', methods=['POST'])
def insert_equipment():
    """Create a new equipment.
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
            description: There was a parsing or validation error in the request.
          409:
            description: An equipment with that code already exists 
          500:
            description: Error
    """
    logging.basicConfig(format='%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Insert equipment endpoint')

    try:
        data = request.get_json()
        vessel = Vessel.query.filter_by(code=data['vessel_code']).first()
        
        if not vessel:
            logger.info(f"Vessel code {data['vessel_code']} not found")
            return {'message': 'ERROR'}, 400

        equipment = Equipment(
            vessel_id = vessel.id,
            name = data['name'],
            code = data['code'],
            location = data['location'],
            active = True
        )
        db.session.add(equipment)
        db.session.commit()
    except KeyError:
        return {'message': 'ERROR'}, 400
    except exc.IntegrityError:
        message = f"Code {data['code']} already exists"
        logger.info(message)
        return {'message': 'FAIL'}, 409
    except:
        message = 'An unhandled exception occurred.'
        logger.info(message)
        return {'message': 'ERROR'}, 500

    logger.info('Equipment created successfully')

    return {'message':'OK'}, 201


@equipments_blueprint.route('/status/inactive', methods=['PUT'])
def update_equipment_status():
    """update_equipment_status
        ---
        parameters:
            - name: equipments
              in: body
              type: list
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

    data = request.get_json()
    equipments = data['equipments']
    # equipments = Equipment.query.filter(Equipment.id.in_(equipment_list)).all()

    logger.info(f'List of equipments: {equipments}')
    
    for equipment_code in equipments:
        equipment = Equipment.query.filter_by(code=equipment_code).first()
        if equipment:
            equipment.active = False
            db.session.commit()
        else:
            message_error = f'Equipment {equipment_code} not found.'
            logger.info(message_error)
            return {'message': message_error}, 400
    
    message = 'All equipments set to inactive'
    logger.info(message)
    return {'message': 'OK'}, 201


@equipments_blueprint.route('/active', methods=['GET'])
def active_equipment():
    """List all active equipments.
        ---
        responses:
          200:
            description: OK
    """
    logging.basicConfig(format='%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('list of active equipments endpoint')

    equipments = Equipment.query.filter_by(active=True).all()
    return jsonify([equipment.to_dict() for equipment in equipments]), 200


@equipments_blueprint.route('/<int:equipment_id>', methods=['DELETE'])
def delete_equipment(equipment_id):
    """Delete an equipment.
        ---
        parameters:
            - name: equipment_id
              in: body
              type: int
              required: true

        responses:
          200:
            description: OK
          404:
            description: Not found
    """
    logging.basicConfig(format='%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('View equipment endpoint')
    
    equipment = Equipment.query.get_or_404(equipment_id)
    db.session.delete(equipment)
    db.session.commit()
    return {'message': f'OK'}, 200


@equipments_blueprint.route('/operation', methods=['GET'])
def list_operations():
    """List all existing operations.
        ---
        responses:
          200:
            description: OK
    """
    logging.basicConfig(format='%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('list of operation endpoint')

    operations = Operation.query.all()
    return jsonify([obj.to_dict() for obj in operations]), 200


@equipments_blueprint.route('/operation', methods=['POST'])
def operation_equipment():
    """Add an operation order related to a equipment.
        ---
        parameters:
            - name: code
              in: body
              type: string
              required: true
            - name: replacement
              in: body
              type: string
              required: true
            - name: cost
              in: body
              type: float
              required: true
        responses:
          201:
            description: returns OK if the operation was correctly created.
          400:
            description: There was a parsing or validation error in the request.
          500:
            description: Error
    """
    logging.basicConfig(format='%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Operation endpoint')

    data = request.get_json()

    try:
        equipment = Equipment.query.filter_by(code=data['code']).first()
        logger.info(f"Equipment: {equipment}")
        
        if not equipment:
            logger.info('Equipment code is not valid')
            return {'message': 'ERROR'}, 400

        operation = Operation(
            equipment_id = equipment.id,
            type = data['type'],
            cost = data['cost']
        )
        db.session.add(operation)
        db.session.commit()
    except KeyError:
        return {'message': 'Invalid body'}, 400
    except:
        message = 'An unhandled exception occurred.'
        return {'message': message}, 500

    logger.info('Operation added successfully')

    return {'message':'OK'}, 201


@equipments_blueprint.route('/operation/costs', methods=['POST'])
def costs_operations():
    """Returns the total cost in operation of an equipment.
        ---
        parameters:
            - name: code
              in: body
              type: string
              required: false
            - name: name
              in: body
              type: string
              required: false
        responses:
          200:
            description: OK
          400:
            description: There was a parsing or validation error in the request.
    """
    logging.basicConfig(format='%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Total cost in operation endpoint')

    data = request.get_json()
    
    if 'code' in data.keys():
        operations = Operation.query.join(Equipment).filter(Equipment.code==data['code']).all()
        costs = [operation.cost for operation in operations]
        return {'message': f'Total cost: {sum(costs)}'}, 200
    elif 'name' in data.keys():
        operations = Operation.query.join(Equipment).filter(Equipment.name==data['name']).all()
        costs = [operation.cost for operation in operations]
        return {'message': f'Total cost: {sum(costs)}'}, 200

    logger.info('Code or Name not found in the request')
    return 'ERROR', 400
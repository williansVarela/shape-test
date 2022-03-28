from api.models.equipment import Equipment, Operation
from api.models.vessel import Vessel
from flask import Blueprint, request, jsonify
from config import db
from sqlalchemy import exc
import logging


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

    data = request.get_json()
    vessel_id = Vessel.query.get(data['vessel_id'])
    
    if not vessel_id:
        return {'message': 'Vessel ID is not valid'}, 400

    try:
        equipment = Equipment(
            vessel_id = data['vessel_id'],
            name = data['name'],
            code = data['code'],
            location = data['location'],
            active = True
        )
        db.session.add(equipment)
        db.session.commit()
    except KeyError:
        return {'message': 'Invalid body'}, 400
    except exc.IntegrityError:
        message = f"Code {data['code']} already exists"
        logger.info(message)
        return {'message': message}, 409
    except:
        message = 'An unhandled exception occurred.'
        return {'message': message}, 500

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
    return {'message': message}, 201


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
    return {'message': f'Equipment {equipment.code} removed successfully!'}, 200


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
    equipment = Equipment.query.filter_by(code=data['code']).first()
    logger.info(f"Equipment: {equipment}")
    
    if not equipment:
        return {'message': 'Equipment code is not valid'}, 400

    try:
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
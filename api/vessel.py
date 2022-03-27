from api.models.vessel import Vessel
from flask import Blueprint, request, jsonify
from config import db
from sqlalchemy import exc
import logging


vessels_blueprint = Blueprint('vessels', __name__)

@vessels_blueprint.route('', methods=['GET'])
def list_vessel():
    """List all existing vessels.
        ---

        responses:
          200:
            description: OK
    """
    logging.basicConfig(format='%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('list vessels endpoint')

    vessel = Vessel.query.all()
    return jsonify([obj.to_dict() for obj in vessel]), 200


@vessels_blueprint.route('/<int:vessel_id>', methods=['GET'])
def view_vessel(vessel_id):
    """Retrieve information about one vessel, specified in the URL.
        ---
        parameters:
            - name: vessel_id
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
    
    vessel = Vessel.query.get_or_404(vessel_id)
    return vessel.to_dict(), 200


@vessels_blueprint.route('', methods=['POST'])
def insert_vessel():
    """Create a new vessel.
        ---
        parameters:
            - name: code
              in: body
              type: string
              required: true
        responses:
          201:
            description: OK
          400:
            description: There was a parsing or validation error in the request.
          409:
            description: A vessel with that code already exists 
          500:
            description: Error
    """
    logging.basicConfig(format='%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Insert vessel endpoint')

    data = request.get_json()
    try:
        vessel = Vessel(
            code = data['code']
        )
        db.session.add(vessel)
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

    logger.info('Vessel created successfully')

    return {'message': 'OK'}, 201


@vessels_blueprint.route('/<int:vessel_id>', methods=['DELETE'])
def delete_vessel(vessel_id):
    """Delete a vessel.
        ---
        parameters:
            - name: vessel_id
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
    logger.info('Delete  vessel endpoint')
    
    vessel = Vessel.query.get_or_404(vessel_id)
    db.session.delete(vessel)
    db.session.commit()
    return {'message': f'Vessel {vessel.code} removed successfully!'}, 200
import logging

from flask import Blueprint


healthcheck_blueprint = Blueprint('healthcheck', __name__)

@healthcheck_blueprint.route('/', methods=['GET'])
def healthcheck():

    """Checks if the system is alive.
        ---
        responses:
          200:
            description: OK if the system is alive
    """
    logging.basicConfig(format='%(levelname)s - %(asctime)s (%(filename)s:%(funcName)s): %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Test the health of the system')
    return 'OK', 200

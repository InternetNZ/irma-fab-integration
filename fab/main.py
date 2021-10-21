"""
IRMA - FAB integration main module
"""
import traceback

from http import HTTPStatus
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from fab import fab, logger, InternalServerError

app = Flask(__name__)
CORS(app)


@app.errorhandler(401)
@app.errorhandler(InternalServerError)
@app.errorhandler(HTTPException)
def error_handler(error):
    """
    Handles registered errors by returning code and description in
    JSON format
    """
    response = jsonify({
        "code": error.code,
        "name": error.name,
        "description": error.description,
    })
    return response, error.code


@app.route('/fab/vc', methods=['POST'])
def save_fab_vc():
    """
    This API is called by FAB to send back the requested VC.
    """
    try:
        fab.save_fab_vc(request.json)

        return jsonify(''), HTTPStatus.OK
    except Exception as exc:
        logger.error('Internal error: %s - %s', str(exc),
                     traceback.format_exc())
        raise InternalServerError() from exc


@app.route('/fab/vc/<vc_id>', methods=['GET'])
def get_fab_vc(vc_id):
    """
    Fetches a stored FAB verifiable credential by given (session) id.

    :param vc_id: challenge ID in FAB context
    :return: VC
    """
    try:
        verifiable_credential = fab.get_fab_vc(vc_id)

        if verifiable_credential:
            return jsonify(verifiable_credential), HTTPStatus.OK

        return '', HTTPStatus.NO_CONTENT
    except Exception as exc:
        logger.error('Internal error: %s - %s', str(exc),
                     traceback.format_exc())
        raise InternalServerError() from exc

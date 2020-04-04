from flask import Flask, jsonify
from flask_cors import CORS
from .auth.auth import requires_auth, AuthError
from .database.models import setup_db, Drink, Ingredient

app = Flask(__name__)
setup_db(app)
CORS(app)


@app.after_request
def after_request(response):
    """Adds response headers after request

    Args:
        response: The response object to add headers to

    Returns:
        response: The response object that the headers were added to
    """

    response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type, Authorization, true'
    )
    response.headers.add(
        'Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS'
    )

    return response


@app.route('/drinks')
def get_drinks():
    """Route handler for endpoint showing all drinks in short form

    Returns:
        response: A json object representing all drinks
    """

    drinks = Drink.query.order_by(Drink.id).all()
    drinks = [drink.short_format() for drink in drinks]

    response = jsonify({
        'success': True,
        'drinks': drinks,
    })

    return response


@requires_auth('get:drinks-detail')
@app.route('/drinks-detail')
def get_drinks_detail():
    """Route handler for endpoint showing all drinks in long form

    Requires 'get:drinks-detail' permission

    Returns:
        response: A json object representing all drinks
    """

    drinks = Drink.query.order_by(Drink.id).all()
    drinks = [drink.long_format() for drink in drinks]

    response = jsonify({
        'success': True,
        'drinks': drinks,
    })

    return response


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where
        drink an array containing only the newly created drink or appropriate
        status code indicating reason for failure
'''


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where
        drink an array containing only the updated drink or appropriate status
        code indicating reason for failure
'''


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id
        is the id of the deleted record or appropriate status code indicating
        reason for failure
'''


@app.errorhandler(400)
def bad_request(error):  # pylint: disable=unused-argument
    """Error handler for 400 bad request

    Args:
        error: unused

    Returns:
        Response: A json object with the error code and message
    """
    response = jsonify({
        'success': False,
        'error_code': 400,
        'message': 'Bad Request',
    })
    return response, 400


@app.errorhandler(404)
def not_found(error):  # pylint: disable=unused-argument
    """Error handler for 404 not found

    Args:
        error: unused

    Returns:
        Response: A json object with the error code and message
    """
    response = jsonify({
        'success': False,
        'error_code': 404,
        'message': 'Not Found',
    })
    return response, 404


@app.errorhandler(405)
def method_not_allowed(error):  # pylint: disable=unused-argument
    """Error handler for 405 method not allowed

    Args:
        error: unused

    Returns:
        Response: A json object with the error code and message
    """
    response = jsonify({
        'success': False,
        'error_code': 405,
        'message': 'Method Not Allowed',
    })
    return response, 405


@app.errorhandler(422)
def unprocessable_entity(error):  # pylint: disable=unused-argument
    """Error handler for 422 unprocessable entity

    Args:
        error: unused

    Returns:
        Response: A json object with the error code and message
    """
    response = jsonify({
        'success': False,
        'error_code': 422,
        'message': 'Unprocessable Entity',
    })
    return response, 422


@app.errorhandler(500)
def internal_server_error(error):  # pylint: disable=unused-argument
    """Error handler for 500 internal server error

    Args:
        error: unused

    Returns:
        Response: A json object with the error code and message
    """
    response = jsonify({
        'success': False,
        'error_code': 500,
        'message': 'Internal Server Error',
    })
    return response, 500


@app.errorhandler(AuthError)
def authorization_error(error):
    """Error handler for authorization error

    Args:
        error: A dict representing the authorization error

    Returns:
        Response: A json object with the error code and message
    """
    response = jsonify(error.error)
    response.status_code = error.status_code

    return response

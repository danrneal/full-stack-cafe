from flask import Flask, jsonify
from flask_cors import CORS
from .auth.auth import requires_auth
from .database.models import setup_db, Drink

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


# Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''

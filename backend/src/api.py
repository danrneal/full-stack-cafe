from flask import Flask, jsonify, request, abort
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


@app.route('/drinks', methods=['GET'])
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


@requires_auth('post:drinks')
@app.route('/drinks', methods=['POST'])
def create_drink():
    """Route handler for endpoint to create a drink

    Returns:
        response: A json object containing the id of the drink that was created
    """

    try:

        drink = Drink(title=request.json.get('title'))
        drink.insert()

        for ingredient in request.json.get('recipe'):

            ingredient = Ingredient(
                name=ingredient.get('name'),
                parts=ingredient.get('parts'),
                color=ingredient.get('color'),
                drink_id=drink.id,
            )

            ingredient.insert()

        response = jsonify({
            'success': True,
            'created_drink_id': drink.id,
        })

    except AttributeError:
        abort(400)

    return response


@requires_auth('patch:drinks')
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
def patch_book_rating(drink_id):
    """Route handler for endpoint updating the a single drink

    Args:
        drink_id: An int representing the identifier for the drink to update

    Returns:
        response: A json object stating if the request was successful
    """

    drink = Drink.query.get(drink_id)

    if drink is None:
        abort(422)

    try:

        old_drink = drink.long_format()
        title = request.json.get('title')
        recipe = request.json.get('recipe')

        if title is not None:
            drink.title = title

        if recipe is not None:

            for ingredient in drink.recipe:
                ingredient.delete()

            for ingredient in request.json.get('recipe'):

                ingredient = Ingredient(
                    name=ingredient.get('name'),
                    parts=ingredient.get('parts'),
                    color=ingredient.get('color'),
                    drink_id=drink.id,
                )

                ingredient.insert()

        drink.update()

    except AttributeError:
        abort(400)

    response = jsonify({
        'success': True,
        'updated_drink_id': drink_id,
        'old_drink': old_drink,
        'new_drink': drink.long_format(),
    })

    return response


@requires_auth('delete:drinks')
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
def delete_drink(drink_id):
    """Route handler for endpoint to delete a single drink

    Args:
        drink_id: An int representing the identifier for a drink to delete

    Returns:
        response: A json object containing the id of the drink that was deleted
    """

    drink = Drink.query.get(drink_id)

    if drink is None:
        abort(422)

    drink.delete()

    response = jsonify({
        'success': True,
        'deleted_drink_id': drink_id,
    })

    return response


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

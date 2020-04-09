# Full Stack Cafe

This is a coffee shop app with a flask-based API and an Auth0 authorization and authentication backend. Full Stack Cafe uses role based access control to limit the actions of users. Users with the barista role can view the recipes for various drinks and users with the manager role can create, edit, or delete drinks. This app also utilizes an ionic front end. You will need python3, nodejs, and ionic installed to run the app.

## Set-up

Set-up a virtual environment and activate it:

```bash
python3 -m venv env
source env/bin/activate
```

You should see (env) before your command prompt now. (You can type `deactivate` to exit the virtual environment any time.)

### Backend

Navigate to the backend folder

Install the requirements:

```bash
pip install -r requirements.txt
```

Set up your environment variables:

```bash
touch .env
echo FLASK_APP=src/api.py >> .env
echo FLASK_ENV=development >> .env
```

### Frontend

Navigate to the frontend folder

Install the requirements:

```bash
npm install -g @ionic/cli
npm install
```

## Usage

To start the backend, run the following command from the backend folder:

```bash
flask run
```

To start the frontend, run the following command in another terminal from the frontend folder:

```bash
ionic serve
```

Navigate to `http://127.0.0.1:8100/` to see the app in action!

## Screenshots

![Full Stack Cafe Homepage](https://i.imgur.com/5Pimf3I.png)
![Full Stack Cafe Drink Editor](https://i.imgur.com/KXWqWze.png)
![Full Stack Cafe User Page](https://i.imgur.com/MVPYWgc.png)

## API Reference

### Base URL

When running locally with the built in flask server, the base url is as follows:

```bash
http://127.0.0.1:5000/
```

### Error Handling

Below are a list of errors that may be raised as part of the api

#### 400: Bad Request

This is returned when the requested is malformed in some way. (i.e. Required info is missing)

#### 401: Unauthorized

This is returned when accessing a non-public endpoint while unauthenticated. (i.e. User is not logged in)

##### authorization_header_missing

This is the error when there is no header for authorization included with the request.

##### invalid_header

This is the error when the authorization header is malformed in some way. (i.e. The token is in the incorrect format)

##### token_expired

This is the error when the provided token is expired and the user must re-login

##### invalid_claims

This is error if the token is invalid in any other way. (i.e. The token has been modified or the permissions object is missing)

#### 403: Forbidden

This is returned when accessing a resource you are not authorized to access. (i.e. User is logged in but does not have sufficient permissions to access the requested resource)

#### 404: Not Found

This is returned when the requested resource does not exist.

#### 405: Method Not Allowed

This is returned when the incorrect request method is specified at an endpoint. (i.e. Attempting to delete without specifying a specific drink to delete)

#### 422: Unprocessable Entity

This is returned when the request is unable to be fulfilled in some way. (i.e. Attempting to update a drink that has previously been deleted)

#### 500: Internal Server Error

This is returned when something there is a problem with the server.

### Endpoints

Drinks

#### GET /drinks

```bash
curl http://127.0.0.1:5000/drinks
```

```bash
{
  "success": true,
  "drinks": [
    {
      "id": 1,
      "title": "Mocha",
      "recipe": [
        {
          "parts": 1,
          "color": "#e8ddb8"
        },
        {
          "parts": 2,
          "color": "#743315"
        },
        {
          "parts": 1,
          "color": "#371808"
        }
      ]
    }
  ]
}
```

#### GET /drinks-details

Required Permissions: get:drinks-detail

```bash
curl -H "Authorization: Bearer <token>" http://127.0.0.1:5000/drinks-detail
```

```bash
{
  "success": true,
  "drinks": [
    {
      "id": 1,
      "title": "Mocha",
      "recipe": [
        {
          "name": "Milk",
          "parts": 1,
          "color": "#e8ddb8"
        },
        {
          "name": "Chocolate",
          "parts": 2,
          "color": "#743315"
        },
        {
          "name": "Espresso",
          "parts": 1,
          "color": "#371808"
        }
      ]
    }
  ]
}
```

#### POST /drinks

Required Permissions: post:drinks

```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{"title": "Water", "recipe": [{"name": "Water", "parts": "1", "color": "blue"}]}' http://127.0.0.1:5000/drinks
```

- title (str): Title of the drink
- recipe (list): A list of ingredient objects
  - name (str): Name of the ingredient in the recipe
  - parts (int): Number of parts of the recipe the ingredient comprises
  - color (int): Color of the ingredient

```bash
{
  "success": true,
  "created_drink_id": 2,
  "old_drink": null,
  "new_drink": {
    "id": 2,
    "title": "Water",
    "recipe": [
      {
        "name": "Water",
        "parts": 1,
        "color": "blue"
      }
    ]
  }
}
```

#### PATCH /drinks/<drink_id>

Required Permissions: patch:drinks

```bash
curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{"title": "Whiskey", "recipe": [{"name": "Whiskey", "parts": "1", "color": "brown"}]}' http://127.0.0.1:5000/drinks/2
```

- title (str) [optional]: Title of the drink
- recipe (list) [optional]: A list of ingredient objects
  - name (str): Name of the ingredient in the recipe
  - parts (int): Number of parts of the recipe the ingredient comprises
  - color (int): Color of the ingredient

```bash
{
  "success": true,
  "updated_drink_id": 2,
  "new_drink": {
    "id": 6,
    "title": "Whiskey",
    "recipe": [
      {
        "name": "Whiskey",
        "parts": 1,
        "color": "brown"
      }
    ]
  },
  "old_drink": {
    "id": 6,
    "title": "Water",
    "recipe": [
      {
        "name": "Water",
        "parts": 1,
        "color": "blue"
      }
    ]
  }
}
```

#### DELETE /drinks/<drink_id>

Required Permissions: delete:drinks

```bash
curl -X DELETE -H "Authorization: Bearer <token>" http://127.0.0.1:5000/drinks/1
```

```bash
{
  "success": true,
  "deleted_drink_id": 1,
  "old_drink": {
    "id": 1,
    "title": "Mocha",
    "recipe": [
      {
        "name": "Milk",
        "parts": 1,
        "color": "#e8ddb8"
      },
      {
        "name": "Chocolate",
        "parts": 2,
        "color": "#743315"
      },
      {
        "name": "Espresso",
        "parts": 1,
        "color": "#371808"
      }
    ]
  },
  "new_drink": null
}
```

## Testing Suite

The backend has a testing suite to test all of the API endpoints from both Postman and from unit tests.

To set up the test database:

```bash
cp starter.db test.db
```

### Postman Tests

From Postman import the postman collection (full-stack-cafe.postman_collection.json) into Postman and use a runner to run the entire collection.

#### _Note: Postman tests need to be done with a fresh copy of the starter database or some of the test will fail. Specifically any drinks that have been deleted in previous tests will no longer be available causing all tests referencing those drinks to fail_

### Unit Tests

Set a barista and manager token from Auth0 in your environment variables:

```bash
echo BARISTA_TOKEN="XXX" >> .env
echo MANAGER_TOKEN="XXX" >> .env
set -a; source .env; set +a
```

To run all the unit tests:

```bash
usage: test_api.py
```

## Credit

[Udacity's Full Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044)

## License

Full Stack Cafe is licensed under the [MIT license](https://github.com/danrneal/full-stakc-api/blob/master/LICENSE).

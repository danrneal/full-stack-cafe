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

The API reference documentation is available [here](https://documenter.getpostman.com/view/10868159/SzfDxQzs?version=latest)

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

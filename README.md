# Full Stack Cafe

This is a coffee shop app with a flask-based API and an Auth0 authorization and authentication backend. Full Stack Cafe uses role based access control to limit the actions of users. Users with the barista role can view the recipes for various drinks and users with the manager role can create, edit, or delete drinks. This app also utilizes an ionic front end. You will need python3, nodejs, and ionic installed to run the app.

## Set-up

### Backend

Navigate to the backend folder

Set-up a virtual environment and activate it:

```bash
python3 -m venv env
source env/bin/activate
```

You should see (env) before your command prompt now. (You can type `deactivate` to exit the virtual environment any time.)

Install the requirements:

```bash
pip install -U pip
pip install -r requirements.txt
```

Set up an Auth0 domain at [Auth0](https://auth0.com/).

- Create a single page app
- Set "Allowed Callback URLs", "Allowed Logout URLs", and "Allowed Web Origins" to `http://127.0.0.1:5000`
- Create an API
- Check the options "Enable RBAC" and "Add Permissions in the Access Token"

Set up the global `AUTH0_DOMAIN` variable in `src/auth/auth.py` to your own Auth0 domain.

Set up your environment variables:

```bash
touch .env
echo FLASK_APP=src/api.py >> .env
```

Initialize and set up the database:

```bash
cp src/database/starter.db src/database/database.db
```

### Frontend

Navigate to the frontend folder

Install the requirements:

```bash
npm install -g @ionic/cli
npm install
```

## Usage

To start the backend, navigate to the backend folder and make sure you are in the virtual environment (you should see (env) before your command prompt). If not `source /env/bin/activate` to enter it.

```bash
Usage: flask run
```

To start the frontend, run the following command in another terminal from the frontend folder:

```bash
Usage: ionic serve
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
cd backend
cp src/database/starter.db src/database/test.db
```

### Postman Tests

From Postman import the postman collection (full-stack-cafe.postman_collection.json) into Postman and use a runner to run the entire collection. Then you will need to edit the barista and manager folders in postman to have a valid barista and manager tokens from Auth0 in the Authorization tab.

#### _Note: Postman tests are run against production and need to be done with a fresh copy of the starter database or some of the tests will fail. Specifically any drinks that have been deleted in previous tests will no longer be available causing all tests referencing those drinks to fail._

### Unit Tests

Set a barista and manager token from Auth0 in your environment variables:

```bash
echo BARISTA_TOKEN="XXX" >> .env
echo MANAGER_TOKEN="XXX" >> .env
set -a; source .env; set +a
```

To run all the unit tests:

```bash
Usage: test_api.py
```

## Credit

[Udacity's Full Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044)

## License

Full Stack Cafe is licensed under the [MIT license](https://github.com/danrneal/full-stack-cafe/blob/master/LICENSE).

# Flask-FirebaseAuth

Flask-FirebaseAuth is a Flask extension that provides an easy way to
protect certain views or your whole application with HTTP [Bearer token access
authentication](https://datatracker.ietf.org/doc/html/rfc6750) using a Firebase 
Auth **idToken** as the token.

## Installation

This package is not yet available on [PyPI](http://pypi.org), so you will have 
to install and use it locally by doing the following:
```shell
python setup.py sdist bdist_wheel
pip install -e .
```

This document will be updated whent it is available, first on [TestPyPI](https://test.pypi.org/),
and then [PyPI](http://pypi.org)

## Usage

Usage of Flask-FirebaseAuth is simple:

    from flask import Flask, render_template
    from flask_firebaseauth import FirebasedAuth

    app = Flask(__name__)

    # Initialize the Firebase Admin Module with either a path to
    # a service account JSON file or project id (the latter is the
    # better approach if you are, say deploying to Cloud Run or some
    # similar Google service).
    service_account_creds = os.environ.get("SERVICE_ACCOUNT_CREDS")
    if service_account_creds is not None:
        cred = credentials.Certificate(service_account_creds)
        initialize_app(cred)
    else:
        project_id = os.environ.get("PROJECT_ID")
        if project_id is None:
            print("Must specify either PROJECT_ID or SERVICE_ACCOUNT_CREDS environment variable.")
            exit(1)
        cred = credentials.ApplicationDefault()
        initialize_app(cred, {'projectId': project_id})

    firebase_auth = FirebaseAuth(auth=auth, app=app)

    @app.route('/secret')
    @firebase_auth.required
    def secret_view():
        return render_template('secret.html')

You might find this useful, for example, if you would like to protect
your staging server from uninvited guests.


## License
[LICENSE](./LICENSE)
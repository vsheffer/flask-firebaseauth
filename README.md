Flask-FirebaseAuth
==================

[![Build Status](https://github.com/vsheffer/flask_firebaseauth/actions/workflows/ci.yaml/badge.svg?branch=main)](https://travis-ci.org/vsheffer/flask-firebaseauth)

[![Coverage Status](https://coveralls.io/repos/vsheffer/flask-fiebaseauth/badge.png)](https://coveralls.io/r/vsheffer/flask-firebaseauth)

Flask-FirebaseAuth is a Flask extension that provides an easy way to
protect your RESTful API requests with bearer token access
authentication that verifies the bearer token with Firebase Auth.

It uses the Firebase Auth idToken as the bearer token. FirebaseAuth then
verifies that the token is valid and hasn't expired. To use:

1.  In the client login to Firebase Auth using any of the supported
    methods,
2.  Obtain the idToken from the authenticated user,
3.  Add an HTTP Authorization header (<span
    class="title-ref">Authorization: Bearer \<idToken\></span>) to your
    request,
4.  In your Flask based RESTful service endpoints add
    @firebase_auth.required to each request.

# Testing Locally

The current version no longer supports Github actions for testing/deployment.
But, you can test locally using a Docker container.  To test, first build a 
local image:
```shell
docker build . -t local/test-flask-firebase-auth -f Dockerfile.test
```
then run the container:
```shell
docker run  local/test-flask-firebase-auth
```

# Build and Use as Local Package

To use this version of the package you will need to build it locally and then
use it to build your local project.  I do all of my RESTful deployments in a
Docker container, so this is not a burden if that is your use case.

Set up a **venv** in the local directory:
```shell
python3 -m venv ./venv
```

Activate the newly created **venv**:
```shell
source venv/bin/activate
```

Install the **wheel** package in the **venv**:
```shell
pip install wheel
```

Build the package:
```shell
python setup.py bdist_wheel
```

Copy the resulting wheel file:
```shell
cp cp dist/Flask_FirebaseAuth-0.1.1-py3-none-any.whl  <your desired path>
```

Again, I normally build my RESTFul APIs into Docker images and deploy the
containers, usually, to a Kubernetes cluster.  As such, I actually commit
this file to my Git repos, add the following line to my **requirements.txt**
file:

`file:Flask_FirebaseAuth-0.1.1-py3-none-any.whl`

then, from inside the Dockerfile install the image's Python required packages
using pip.

# Links

-   [Documentation](https://flask-firebaseauth.readthedocs.io/)
-   [Issue
    Tracker](http://github.com/vsheffer/flask-firebaseauth/issues)
-   [Code](http://github.com/vsheffer/flask-firebaseauth/)
-   [Development
    Version](http://github.com/vsheffer/flask-firebaseauth/zipball/master#egg=Flask-FirebaseAuth-dev)

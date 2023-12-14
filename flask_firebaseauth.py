"""
    flask.ext.firebaseauth
    ~~~~~~~~~~~~~~~~~~~

    Flask-FirebaseAuth is a Flask extension that provides an easy way to protect
    access to your RESTful APIs using Fir
    :copyright: (c) 2023 Vincent Sheffer.
    :license: MIT, see LICENSE for more details.
"""
import logging
import traceback
from functools import wraps

import firebase_admin.auth
from firebase_admin import auth as firebase_auth
from flask import request, Response, json

__version__ = '0.1.1'


log = logging.getLogger("flask-firebaseauth")


class FirebaseAuth(object):
    firebase_auth_api: firebase_auth
    user_info: dict

    """
    A Flask extension for adding HTTP bearer token access authentication to the
    application.

    :param app: a :class:`~flask.Flask` instance. Defaults to `None`. If no
        application is provided on creation, then it can be provided later on
        via :meth:`init_app`.
    """

    def __init__(self, auth: firebase_auth, app=None):
        self.firebase_auth_api = auth
        if app is not None:
            self.app = app
            self.init_app(app)
        else:
            self.app = None

    @staticmethod
    def init_app(app):
        """
        Initialize this FirebaseAuth extension for the given application.

        :param app: a :class:`~flask.Flask` instance
        """
        app.config.setdefault('FIREBASE_AUTH_FORCE', False)
        app.config.setdefault('FIREBASE_AUTH_REALM', '')

        # @app.before_request
        # def require_firebaseauth():
        #     if not current_app.config['FIREBASE_AUTH_FORCE']:
        #         return
        #     if not self.authenticate():
        #         return self._return_error("Invalid access token.", 401)

    def _return_error(self, message: str, code: int) -> Response:
        err_dict = {
            "code": code,
            "message": message
        }
        realm = self.app.config['FIREBASE_AUTH_REALM']
        return self.app.response_class(response=json.dumps(err_dict),
                                       status=code,
                                       headers={'WWW-Authenticate': f'Bearer realm="{realm}"'},
                                       mimetype='application/json')

    def authenticate(self, id_token: str) -> str(None):
        """
        Check the request for HTTP bearer access authentication header and try
        to authenticate the user.

        :returns: `None` if the user is authorized, or a `str` with and error
                   message otherwise.
        """
        try:
            value = self.firebase_auth_api.verify_id_token(id_token)
            log.debug(f"value = {value}")
            self.app.firebase_user = value
            self.user_info = value
            return None
        except firebase_admin.auth.ExpiredIdTokenError:
            return "Firebase auth id token has expired"
        except firebase_admin.auth.RevokedIdTokenError:
            return "Firebase auth id token has been revoked."
        except firebase_admin.auth.InvalidIdTokenError:
            return "Invalid Firebase Auth id token"
        except Exception as e:
            traceback.print_exc()
            return f"Some unknown error has occurred verifying the token: {e}"

    def required(self, view_func):
        """
        A decorator that can be used to protect specific views with HTTP
        bearer access authentication using Firebase Auth idToken as the
        bearer token.
        """

        @wraps(view_func)
        def wrapper(*args, **kwargs) -> Response:
            log.debug(f"kwargs = {kwargs}")
            auth_header = request.headers.get('Authorization')
            if auth_header is None:
                return self._return_error("Missing Authorization: Bearer header", 401)

            if not auth_header.startswith("Bearer"):
                return self._return_error("Malformed Authorization header.", 401)

            try:
                token = auth_header.split(" ")[1]
                retstr = self.authenticate(token)
                if retstr is None:
                    # args = (self.user_info,) + args
                    #                kwargs['firebase_user'] = self.user_info
                    return view_func(*args, **kwargs)
                else:
                    return self._return_error(retstr, 401)
            except IndexError:
                return self._return_error(
                    "Malformed Authorization header, should be 'Authorization: Bearer <idToken>'.", 401)

        return wrapper

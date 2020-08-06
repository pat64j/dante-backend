from flask_restful import HTTPException

class ValidationError(ValueError):
    pass

class TokenNotFound(HTTPException):
    """ Indicates that a token could not be found in the DB """
    pass


class InternalServerError(HTTPException):
    pass


class SchemaValidationError(HTTPException):
    pass


class AccountNotFoundError(HTTPException):
    pass


class UpdatingAccountError(HTTPException):
    pass


class FreshTokenRequiredError(HTTPException):
    pass


class MissingTokenError(HTTPException):
    pass


class EmailAlreadyExistsError(HTTPException):
    pass


class UnauthorizedError(HTTPException):
    pass


class NoInputReceivedError(HTTPException):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400
    },
    "FreshTokenRequiredError": {
        "message": "Only fresh tokens are allowed",
        "status": 401
    },
    "AccountNotFoundError": {
        "message": "Could not find this account.",
        "status": 404
    },
    "UpdatingAccountError": {
        "message": "An error occured while updating this account.",
        "status": 404
    },
    "TokenNotFound": {
        "message": "Could not find the request token.",
        "status": 404
    },
    "EmailAlreadyExistsError": {
        "message": "User with given email address already exists",
        "status": 400
    },
    "UnauthorizedError": {
        "message": "Invalid username or password",
        "status": 401
    },
    "NoInputReceivedError": {
        "message": "No input data provided",
        "status": 400
    }
}

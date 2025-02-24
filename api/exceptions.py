import json
import traceback
from logging_config import logger


class BaseAPIException(Exception):
    def __init__(self, message: str, error_code: str = "VITAL_SYNC_API_ERROR"):
        self.error_code = error_code

        logger.error(
            json.dumps(
                {
                    "error_code": self.error_code,
                    "message": message,
                    "trace": traceback.format_exc(),
                }
            )
        )

        super().__init__(message)


class UserNotFoundError(BaseAPIException):
    pass


class ValidationError(BaseAPIException):
    pass


class UserAlreadyExistsError(BaseAPIException):
    pass

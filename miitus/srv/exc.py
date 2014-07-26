class ConflictError(Exception):
    status = 409
    message = ''

class RevokeChainRequested(Exception):
    pass

class BrokenToken(Exception):
    pass

class PasswordWrong(Exception):
    pass

class WorkerIdInitFailed(Exception):
    pass

class UserNotFound(Exception):
    pass


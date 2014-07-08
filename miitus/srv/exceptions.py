class AlreadyExists(Exception):
    pass

class DBGenericError(RuntimeError):
    pass

class NotExists(Exception):
    pass

class RevokeChainRequested(Exception):
    pass

class BrokenToken(Exception):
    pass

class PasswordWrong(Exception):
    pass

class WorkerIdInitFailed(Exception):
    pass


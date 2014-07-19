class Conflict(Exception):
    status = 409
    message = ''

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

class ParellelInsertionDetected(Exception):
    pass


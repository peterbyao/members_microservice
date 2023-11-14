class MemberException(Exception):
    ...


class MemberNotFoundError(MemberException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Member Not Found"


class MemberAlreadyExistError(MemberException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Member Already Exists"

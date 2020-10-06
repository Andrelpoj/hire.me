class AliasNotFound(Exception):
    def __init__(self, alias):
        self.alias = alias 

class AliasAlreadyExists(Exception):
    def __init__(self, alias):
        self.alias = alias 

class UnexpectedServerResponse(Exception):
    def __init__(self, response):
        self.response = response

from msilib.schema import Error


class LimitExceeded(Exception):
    def __init__(self, limit):
        self.limit = limit
        self.message = f"limit of {limit} has been exceeded"

        super().__init__(self.message)

class FastFlowException(Exception):
    def __init__(self, message: str = "Error while processing request"):

        super().__init__(message)


class ApiValidationError(FastFlowException):
    def __init__(self, message: str = "Error while processing request to Provider API"):

        super().__init__(message)


class FlowNotFound(FastFlowException):
    def __init__(self, message: str = "Flow was not found"):
        super().__init__(message)

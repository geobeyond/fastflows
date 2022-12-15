class FastFlowsError(Exception):
    def __init__(self, message: str = "Error while processing request"):

        super().__init__(message)


class ApiValidationError(FastFlowsError):
    def __init__(self, message: str = "Error while processing request to Provider API"):

        super().__init__(message)


class FlowNotFoundError(FastFlowsError):
    def __init__(self, message: str = "Flow was not found"):
        super().__init__(message)

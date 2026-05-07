class ApplicationError(Exception):
    pass


class InvalidDateRangeError(ApplicationError):
    pass


class EventProcessingError(ApplicationError):
    pass


class RepositoryError(ApplicationError):
    pass


class PublisherError(ApplicationError):
    pass

from app.src.business_logic.services.logger_service import Logger


class ParserMeta(type):
    """A Parser metaclass that will be used for GenericTestService class creation.
    """
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return (hasattr(subclass, 'dummy_function') and
                callable(subclass.dummy_function))


class GenericTestService(metaclass=ParserMeta):
    def __init__(self, logger: Logger):
        self.logger = logger

    def dummy_function(self):
        pass

class SingletonMeta(type):
    """
    Metaclase que implementa el patrón Singleton.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SingletonBase(metaclass=SingletonMeta):
    """
    Clase base que utiliza la metaclase SingletonMeta para implementar el patrón Singleton.
    """
    def __init__(self):
        pass

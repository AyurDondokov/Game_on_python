"""Реализация  сохранений"""


class Memento:
    def __init__(self, state, name):
        self._state = state
        self._name = name

    @property
    def name(self):
        return self._name

    def __str__(self):
        """Только для отладки"""
        return f"{self.name}{self._state}"


class toDictMixin:
    def save(self):
        return Memento(self._trase_dict(self.__dict__), " self.__name__")

    def _trase_dict(self, attributes):
        result = {}
        for key, value in attributes.items():
            if key.endswith("_s"):
                result[key] = self._trase(key, value)
        return result

    def _trase(self, key, value):
        if isinstance(value, toDictMixin):
            return value.save()
        elif isinstance(value, dict):
            return self._trase_dict(value)
        elif isinstance(value, list):
            return [self._trase(key, v) for v in value]
        elif hasattr(value, '__dict__'):
            return self._trase_dict(value.__dict__)
        else:
            return value

class IdGenerator:
    _counter = 0

    @classmethod
    def generate(cls):
        cls._counter += 1
        return cls._counter

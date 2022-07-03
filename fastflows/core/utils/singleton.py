class Singleton(type):
    # singleton implementation for Catalog and Providers
    _instance = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instance:
            self._instance[self] = super().__call__(*args, **kwargs)
        return self._instance[self]

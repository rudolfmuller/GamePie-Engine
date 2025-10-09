
class Objects:
    def __init__(self, *items):
        self._items = items 

    def draw(self):
        for obj in self._items:
            obj.draw()

    def set(self, name, *values):
        if not values:
            return
        for i, item in enumerate(self._items):
            value = values[i] if i < len(values) else values[0]
            setattr(item, name, value)

    def all(self):
        for obj in self._items:
            yield obj

    def call(self, name, *args, **kwargs):
        results = []
        for item in self._items:
            attr = getattr(item, name, None)
            if callable(attr):
                results.append(attr(*args, **kwargs))
            elif attr is not None:
                results.append(attr) 
            else:
                raise AttributeError(f"object '{item}' does not have '{name}'")
        return results

    @property
    def objects(self):
        return list(self._items)

    def __call__(self):
        return list(self._items)

class Namespace:
    def __init__(self,dict):
        self._dict = dict
    
    def set(self,name, value=None):
        self._dict[name] = value
    def get(self,name):
        return self._dict[name]
    def getaslist(self, index):
        return [list(self._dict.values())[index],list(self._dict.keys())[index]]

    
    def __call__(self):
        return dict(self._dict)
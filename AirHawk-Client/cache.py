import json

class Cache:
    path: str
    data: dict

    def __init__(self, path: str) -> None:
        self.path = path
        try:
            self.load()
        except:
            self.data = {}
    
    def save(self) -> None:
        with open(self.path, 'w') as f:
            json.dump(self.data, f)
    
    def load(self) -> None:
        with open(self.path, 'r') as f:
            self.data = json.load(f)

    def get(self, key: str, default=None):
        if not key in self.data:
            return default
        return self.data[key]
    
    def set(self, key: str, value):
        self.data[key] = value
        self.save()
    
    def delete(self, key: str):
        del self.data[key]
        self.save()
    
    def clear(self):
        self.data = {}
        self.save()
    
    def __getitem__(self, key: str):
        return self.get(key)
    
    def __setitem__(self, key: str, value):
        self.set(key, value)
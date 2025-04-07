class ImageObject:
    def __init__(self, name="", path="", size=0, orig_name="", points=None):
        self.name = name
        self.path = path
        self.size = size
        self.orig_name = orig_name
        self.points = points or []

    def to_dict(self):
        return {
            "name": self.name,
            "path": self.path,
            "size": self.size,
            "orig_name": self.orig_name,
            "points": self.points
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", ""),
            path=data.get("path", ""),
            size=data.get("size", 0),
            orig_name=data.get("orig_name", ""),
            points=data.get("points", [])
        )


class ResultObject:
    def __init__(self, id=0, count=0):
        self.id = id
        self.count = count

    def to_dict(self):
        return {
            "id": self.id,
            "count": self.count
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", 0),
            count=data.get("count", 0)
        )

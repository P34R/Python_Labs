class Manufacturer:
    id: int
    name: str

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __repr__(self):
        return str(self)
    def __str__(self):
        return str(self.id) + " " + self.name
    def toString(self):
        return str(self.id) + " " + self.name


class Software:
    id: int
    name: str
    version: float
    manufacturer: Manufacturer

    def __init__(self, id: int, name: str, version: float, manufacturer: Manufacturer):
        self.id = id
        self.name = name
        self.version = version
        self.manufacturer = manufacturer

    def setManufacturer(self, manufacturer: Manufacturer):
        self.manufacturer = manufacturer
    def __repr__(self):
        return str(self)
    def __str__(self):
        return str(self.id) + " " + self.name + " " + str(self.version) + " " + self.manufacturer.toString()
    def toString(self):
        return str(self.id) + " " + self.name + " " + str(self.version) + " " + self.manufacturer.toString()
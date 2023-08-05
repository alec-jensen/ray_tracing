from vector import Vector3

class Ray:
    def __init__(self, origin: Vector3, direction: Vector3):
        self.origin: Vector3 = origin
        self.direction: Vector3 = direction
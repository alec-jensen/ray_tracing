from vector import Vector3
from rgb import rgb

class Light:
    def __init__(self, position: Vector3, color: rgb, intensity: float):
        self.position: Vector3 = position
        self.color: rgb = color
        self.intensity: float = intensity

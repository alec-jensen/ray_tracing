# Raytracing in Python with Numba
# Author: Alec Jensen

class rgb:
    def __init__(self, r: int, g: int, b: int):
        self.r: int = r
        self.g: int = g
        self.b: int = b
    
    def __str__(self):
        return f'rgb({self.r}, {self.g}, {self.b})'
    
    def __repr__(self):
        return self.__str__()
    
    def __add__(self, other):
        return rgb(self.r + other.r, self.g + other.g, self.b + other.b)
    
    def __sub__(self, other):
        return rgb(self.r - other.r, self.g - other.g, self.b - other.b)
    
    def __mul__(self, other):
        return rgb(self.r * other.r, self.g * other.g, self.b * other.b)
    
    def __truediv__(self, other):
        return rgb(self.r / other.r, self.g / other.g, self.b / other.b)
    
class Vertex:
    def __init__(self, x: int, y: int, z: int):
        self.x: int = x
        self.y: int = y
        self.z: int = z
    
    def __str__(self):
        return f'Vertex({self.x}, {self.y}, {self.z})'
    
    def __repr__(self):
        return self.__str__()

class _3DObject:
    def __init__(self, vertices: list, color: rgb):
        self.vertices: list[Vertex] = vertices
        self.color: rgb = color
    
    def __str__(self):
        return f'3DObject({self.vertices}, {self.color})'
    
    def __repr__(self):
        return self.__str__()

class Box(_3DObject):
    def __init__(self, x: int, y: int, z: int, width: int, height: int, depth: int, color: rgb):
        vertices = [
            Vertex(x, y, z),
            Vertex(x + width, y, z),
            Vertex(x + width, y + height, z),
            Vertex(x, y + height, z),
            Vertex(x, y, z + depth),
            Vertex(x + width, y, z + depth),
        ]
        super().__init__(vertices, color)

class Scene:
    def __init__(self):
        self.objects: list[_3DObject] = []

    def register(self, obj: _3DObject):
        self.objects.append(obj)

class Camera:
    def __init__(self, x: int, y: int, z: int, pitch: int, yaw: int, roll: int, fov: int):
        self.x: int = x
        self.y: int = y
        self.z: int = z
        self.pitch: int = pitch
        self.yaw: int = yaw
        self.roll: int = roll
        self.fov: int = fov

class Renderer:
    def __init__(self, scene: Scene, camera: Camera):
        self.scene: Scene = scene
        self.camera: Camera = camera

    def render(self):
        pass

def main():
    scene = Scene()

    box = Box(0, 0, 0, 100, 100, 100, rgb(255, 0, 0))
    print(box)
    scene.register(box)

if __name__ == '__main__':
    main()

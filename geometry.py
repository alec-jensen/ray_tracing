from material import Material
from vector import Vector2, Vector3
from ray import Ray
import math

class _3DObject:
    def __init__(self, material: Material):
        self.material: Material = material

class Sphere(_3DObject):
    def __init__(self, center: Vector3, radius: int, material: Material):
        super().__init__(material)
        self.center: Vector3 = center
        if type(radius) != int:
            raise TypeError(f'radius must be an integer, not {type(radius)}')
        self.radius: int = radius
    
    def intersect(self, ray: Ray):
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c

        if discriminant > 0:
            # Ray intersects the sphere
            root1 = (-b - math.sqrt(discriminant)) / (2 * a)
            root2 = (-b + math.sqrt(discriminant)) / (2 * a)
            hit_point = ray.origin + min(root1, root2) * ray.direction
            normal = (hit_point - self.center).normalized()
            return hit_point, normal
        else:
            # Ray doesn't intersect the sphere
            return None, None

class Box(_3DObject):
    def __init__(self, position: Vector3, size: Vector3, material: Material):
        super().__init__(material)
        self.position: Vector3 = position
        self.size: Vector3 = size

    def intersect(self, ray: Ray):
        tmin = (self.position.x - ray.origin.x) / ray.direction.x
        tmax = (self.position.x + self.size.x - ray.origin.x) / ray.direction.x

        if tmin > tmax:
            tmin, tmax = tmax, tmin

        tymin = (self.position.y - ray.origin.y) / ray.direction.y
        tymax = (self.position.y + self.size.y - ray.origin.y) / ray.direction.y

        if tymin > tymax:
            tymin, tymax = tymax, tymin

        if (tmin > tymax) or (tymin > tmax):
            return None, None

        if tymin > tmin:
            tmin = tymin

        if tymax < tmax:
            tmax = tymax

        tzmin = (self.position.z - ray.origin.z) / ray.direction.z
        tzmax = (self.position.z + self.size.z - ray.origin.z) / ray.direction.z

        if tzmin > tzmax:
            tzmin, tzmax = tzmax, tzmin

        if (tmin > tzmax) or (tzmin > tmax):
            return None, None

        if tzmin > tmin:
            tmin = tzmin

        if tzmax < tmax:
            tmax = tzmax

        hit_point = ray.origin + tmin * ray.direction
        normal = self.calculate_normal(hit_point)
        return hit_point, normal

class Plane(_3DObject):
    def __init__(self, position: Vector3, normal: Vector3, size: Vector2, material: Material):
        super().__init__(material)
        self.position: Vector3 = position
        self.normal: Vector3 = normal.normalized()
        self.size: Vector2 = size

    def intersect(self, ray: Ray):
        denominator = self.normal.dot(ray.direction)

        if abs(denominator) > 1e-6:
            hit_point = self.position - ray.origin
            t = hit_point.dot(self.normal) / denominator

            if t > 0:
                hit_point = ray.origin + t * ray.direction
                return hit_point, self.normal

        return None, None
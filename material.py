from rgb import rgb

class Material:
    def __init__(self, color: rgb, ambient: float, diffuse: float, specular: float, shininess: float, roughness: float):
        self.color: rgb = color
        self.ambient: float = ambient
        self.diffuse: float = diffuse
        self.specular: float = specular
        self.shininess: float = shininess
        self.roughness: float = roughness
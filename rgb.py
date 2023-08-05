class rgb:
    def __init__(self, r: int, g: int, b: int):
        for val in [r, g, b]:
            if not isinstance(val, int):
                raise TypeError(f'rgb values must be integers, not {type(val)}')
        self.r: int = r
        self.g: int = g
        self.b: int = b
        self.clamp()
    
    def __str__(self):
        return f'rgb({self.r}, {self.g}, {self.b})'
    
    def __repr__(self):
        return self.__str__()
    
    def __add__(self, other):
        return rgb(self.r + other.r, self.g + other.g, self.b + other.b)
    
    def __sub__(self, other):
        return rgb(self.r - other.r, self.g - other.g, self.b - other.b)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return rgb(int(self.r * other), int(self.g * other), int(self.b * other))
        elif isinstance(other, rgb):
            return rgb(self.r * other.r, self.g * other.g, self.b * other.b)
        else:
            raise TypeError("Unsupported type for multiplication with rgb")
        
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        return rgb(self.r / other.r, self.g / other.g, self.b / other.b)
    
    def as_tuple(self):
        return (self.r, self.g, self.b)
    
    def clamp(self):
        self.r = min(max(self.r, 0), 255)
        self.g = min(max(self.g, 0), 255)
        self.b = min(max(self.b, 0), 255)
    
    @classmethod
    def from_tuple(cls, tup: tuple):
        return cls(tup[0], tup[1], tup[2])
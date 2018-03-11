import math

class Vec3:
	X=0.0
	Y=0.0
	Z=0.0

	def __init__(self, x, y, z):
		self.X=x
		self.Y=y
		self.Z=z

	def __add__(self, other):
		return Vec3(self.X+other.X, self.Y+other.Y, self.Z+other.Z)

	def __sub__(self, other):
		return Vec3(self.X-other.X, self.Y-other.Y, self.Z-other.Z)

	def __mul__(self, other):
		return Vec3(self.X*other.X, self.Y*other.Y, self.Z*other.Z)

	def Mul(self, value):
		return Vec3(self.X*value, self.Y*value, self.Z*value)

	def __div__(self, other):
		return Vec3(self.X/other.X, self.Y/other.Y, self.Z/other.Z)

	def Dot(self,other):
		return self.X*other.X + self.Y*other.Y + self.Z*other.Z

	def Length(self):
		return math.sqrt(self.X*self.X + self.Y*self.Y + self.Z*self.Z)

	def Lerp(self,other, t):
		return self.Mul(1.0-t) + other.Mul(t)

def UnitVector(myVector):
	result = Vec3(0.0,0.0,0.0)
	length = myVector.Length()
	if length > 0.0 :
		result = myVector.Mul(1.0/length)
	return result


class Ray : 
	Origin = Vec3(0.0,0.0,0.0)
	Direction = Vec3(0.0,0.0,0.0)

	def __init__(self, origin, direction):
		Origin = origin
		Direction = direction

	def PointAtParameter(t):
		return Origin + direction.Mul(t) #TODO : probably not the right way to multiply a vec3 with a float


#def Color(Ray ray):






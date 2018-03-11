import math

class Vec3:
	X=0.0
	Y=0.0
	Z=0.0

	def __init__(self, x=0.0, y=0.0, z=0.0):
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

	def Dot(value0, value1):
		return value0.X*value1.X + value0.Y*value1.Y + value0.Z*value1.Z

	def Length(self):
		return math.sqrt(self.X*self.X + self.Y*self.Y + self.Z*self.Z)

	def Lerp(self,other, t):
		return self.Mul(1.0-t) + other.Mul(t)

	def PrintDesc(self):
		print("X:",self.X,"Y:",self.Y,"Z:",self.Z)


##################################################################################

def UnitVector(myVector):
	result = Vec3()
	length = myVector.Length()
	if length > 0.0 :
		result = myVector.Mul(1.0/length)
	return result

##################################################################################

class Ray : 
	Origin = Vec3()
	Direction = Vec3()

	def __init__(self, origin, direction):
		self.Origin = origin
		self.Direction = direction

	def PointAtParameter(self,t):
		return self.Origin + self.Direction.Mul(t)

##################################################################################

class HitRecord:
	ParamT = 0.0
	Point = Vec3()
	Normal = Vec3()


##################################################################################

class Sphere:
	Center = Vec3()
	radius = 1.0

	def __init__(self, center = Vec3(), radius=1.0):
		self.Center = center
		self.Radius = radius

	def Hit(self, ray, tMin, tMax, hitRecord):
		centerToOrigin = ray.Origin - self.Center
		a = Vec3.Dot(ray.Direction, ray.Direction)
		b = Vec3.Dot(centerToOrigin, ray.Direction) #there should be a *2.f here but simplifies the equation later
		c = Vec3.Dot(centerToOrigin, centerToOrigin) - self.Radius*self.Radius
		discriminant = b*b-a*c
		if discriminant > 0.0:
			tmp = (-b - math.sqrt(discriminant) ) / a
			if tMin<=tmp and tmp<=tMax :
				hitRecord.ParamT = tmp
				hitRecord.Point = ray.PointAtParameter(tmp)
				hitRecord.Normal = (hitRecord.Point - self.Center).Mul(1.0/self.Radius)
				return True
			
			tmp = (-b + math.sqrt(discriminant) ) / a
			if tMin<=tmp and tmp<=tMax : #maybe some code to put in common here
				hitRecord.ParamT = tmp
				hitRecord.Point = ray.PointAtParameter(tmp)
				hitRecord.Normal = (hitRecord.Point - self.Center).Mul(1.0/self.Radius)
				return True
		return False

##################################################################################

class HitableList:
	Elems = []
	def Hit(self, ray, tMin, tMax, hitRecord):
		hitSomething = False
		closestSoFar = tMax
		for curElem in self.Elems:
			if curElem.Hit(ray, tMin, closestSoFar, hitRecord):
				hitSomething = True
				closestSoFar = hitRecord.ParamT
		return hitSomething
	
##################################################################################
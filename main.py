import array
import rt
import sys
import random
import math
import pdb

def ColorToGammaSpaceToPPM(color, maxValue):
	tmp = rt.Vec3(math.sqrt(color.X),math.sqrt(color.Y), math.sqrt(color.Z))
	return tmp.Mul(maxValue)

#High quality Option
MAX_RECURSION_ALLOWED = 50 #TODO port that code into something iterative rather than recursive that's poorly performing
nsample = 10 #for aliasing# PPM header

#Comment for high quality
#MAX_RECURSION_ALLOWED = 50
#nsample = 1 #for aliasing# PPM header

nx = 200 #image resolution
ny = 100 #image resolution

EPSILON = 0.001

def Color2(ray, world, recursionLevel):	
	tmp = rt.HitRecord() 	
	if world.Hit(ray, EPSILON, sys.float_info.max, tmp) and recursionLevel < MAX_RECURSION_ALLOWED :
		target = tmp.Point + tmp.Normal + rt.RandomInUnitSphere()
		recursionLevel += 1
		return tmp.Material.Albedo * Color2(rt.Ray(tmp.Point, target-tmp.Point) ,world, recursionLevel)
	else: #background
		unitDirection = rt.UnitVector(ray.Direction)
		t = 0.5 * (unitDirection.Y + 1.0)
		return rt.Vec3(1.0,1.0,1.0).Lerp(rt.Vec3(0.5,0.7,1.0),t)

def Color(ray, world, recursionLevel):
	tmp = rt.HitRecord()
	if world.Hit(ray, EPSILON, sys.float_info.max, tmp) :
		scattered = rt.Ray()		
		attenuation = rt.Vec3()		
		if  recursionLevel < MAX_RECURSION_ALLOWED and tmp.Material.Scatter(ray, tmp, attenuation, scattered):							
			recursionLevel += 1						
			return attenuation * Color(scattered, world, recursionLevel)
		else :		
			return rt.Vec3()
	else: #background
		unitDirection = rt.UnitVector(ray.Direction)
		t = 0.5 * (unitDirection.Y + 1.0)
		return rt.Vec3(1.0,1.0,1.0).Lerp(rt.Vec3(0.5,0.7,1.0),t)

maxval = 255
ppm_header = f'P6 {nx} {ny} {maxval}\n'

# PPM image data
image = array.array('B', [0, 0, 0] * nx * ny)

lowerLeftCorner = rt.Vec3(-2.0,-1.0,-1.0)
horizontal = rt.Vec3(4.0,0.0,0.0)
vertical = rt.Vec3(0.0,2.0,0.0)
origin = rt.Vec3()
scale = 255.9

scene = rt.HitableList()
scene.Elems.append(rt.Sphere(rt.Vec3(0.0,0.0,-1.0), 0.5, rt.Lambertian(rt.Vec3(0.8,0.3,0.3))))
scene.Elems.append(rt.Sphere(rt.Vec3(0.0,-100.5,-1.0), 100.0, rt.Lambertian(rt.Vec3(0.8,0.8,0.0))))
scene.Elems.append(rt.Sphere(rt.Vec3(1.0,0.0,-1.0), 0.5, rt.Metal(rt.Vec3(0.8,0.6,0.2))))
scene.Elems.append(rt.Sphere(rt.Vec3(-1.0,-0.0,-1.0), 0.5, rt.Metal(rt.Vec3(0.8,0.8,0.8))))

mainCamera = rt.Camera()
curPurcentComplete = 0

for i in range(0, nx):
	for j in range(0, ny):
		color = rt.Vec3()		
		for k in range(0, nsample):
			u = ( float(i) + random.random() ) / float(nx)
			v = ( float(j) + random.random() ) / float(ny)		
			ray = mainCamera.GetRay(u,v)			
			color += Color(ray,scene,0)			
		color = color.Mul(1.0/float(nsample))
		color = ColorToGammaSpaceToPPM(color, scale)
		index = 3 * ((ny-1-j) * nx + i) #matching what is in the book
		image[index] = int(color.X)
		image[index + 1] = int(color.Y)
		image[index + 2] = int(color.Z)
		print("Cur Pixel, ", i+1, ", ", j+1, "complete ")		

print("Saving Image")
# Save the PPM image as a binary file
with open('raytracing.ppm', 'wb') as f:
	f.write(bytearray(ppm_header, 'ascii'))
	image.tofile(f)
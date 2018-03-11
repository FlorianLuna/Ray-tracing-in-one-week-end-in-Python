import array
import rt
import sys
import random
import math

def ColorToGammaSpaceToPPM(color, maxValue):
	tmp = rt.Vec3(math.sqrt(color.X),math.sqrt(color.Y), math.sqrt(color.Z))
	return tmp.Mul(maxValue)

#QUALITY Option
MAX_RECURSION_ALLOWED = 500 #TODO port that code into something iterative rather than recursive that's poorly performing
nsample = 100 #for aliasing# PPM header
nx = 200 #image resolution
ny = 100 #image resolution

def Color(ray, world, recursionLevel):
	tmp = rt.HitRecord()
	if world.Hit(ray, 0.0, sys.float_info.max, tmp) and recursionLevel < MAX_RECURSION_ALLOWED:
		#return rt.Vec3(tmp.Normal.X + 1.0, tmp.Normal.Y + 1.0, tmp.Normal.Z + 1.0).Mul(0.5) #NORMAL VISUALIZATION
		target = tmp.Point + tmp.Normal + rt.RandomInUnitSphere()
		recursionLevel += 1
		return Color(rt.Ray(tmp.Point, target-tmp.Point) ,world, recursionLevel).Mul(0.5)
	else: #background
		unitDirection = rt.UnitVector(ray.Direction)
		t = 0.5 * (unitDirection.Y + 1.0)
		return rt.Vec3(1.0,1.0,1.0).Lerp(rt.Vec3(0.5,0.7,1.0),t)

#nsample = 100 #as in book
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
scene.Elems.append(rt.Sphere(rt.Vec3(0.0,0.0,-1.0), 0.5))
scene.Elems.append(rt.Sphere(rt.Vec3(0.0,-100.5,-1.0), 100.0))

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
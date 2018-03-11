import array
import rt



def RescaleColorToPPM(color, maxValue):
	return color.Mul(maxValue)

# PPM header
nx = 200
ny = 100
maxval = 255
ppm_header = f'P6 {nx} {ny} {maxval}\n'

# PPM image data
image = array.array('B', [0, 0, 0] * nx * ny)

lowerLeftCorner = rt.Vec3(-2.0,-1.0,-1.0)
horizontal = rt.Vec3(4.0,0.0,0.0)
vertical = rt.Vec3(0.0,2.0,0.0)
origin = rt.Vec3()
scale = 255.9

for i in range(0, nx-1):
	for j in range(0, ny-1):
		u = float(i) / float(nx)
		v = float(j) / float(ny)
		direction = lowerLeftCorner + horizontal.Mul(u) + vertical.Mul(v)					
		ray = rt.Ray(origin, direction)
		color = rt.Color(ray)
		color = RescaleColorToPPM(color, scale)
		index = 3 * ((ny-1-j) * nx + i) #matching what is in the book
		image[index] = int(color.X)
		image[index + 1] = int(color.Y)
		image[index + 2] = int(color.Z)

# Save the PPM image as a binary file
with open('raytracing.ppm', 'wb') as f:
	f.write(bytearray(ppm_header, 'ascii'))
	image.tofile(f)
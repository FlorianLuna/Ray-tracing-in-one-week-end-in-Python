import array
import rt

# PPM header
width = 200
height = 100
maxval = 255
ppm_header = f'P6 {width} {height} {maxval}\n'

# PPM image data (filled with blue)
image = array.array('B', [0, 0, 0] * width * height)

# Fill with red the rectangle with origin at (10, 10) and width x height = 50 x 80 pixels
for i in range(0, width-1):
	for j in range(0, height-1):
		index = 3 * ((height-1-j) * width + i) #matching what is in the book
		image[index] = int(float(i)/float(width)*255.0)
		image[index + 1] = int(float(j)/float(height)*255.0)
		image[index + 2] = int(0.2*255.0)

test = rt.Vec3(1.0, 2.0, 3.0)

# Save the PPM image as a binary file
with open('blue_red_example.ppm', 'wb') as f:
	f.write(bytearray(ppm_header, 'ascii'))
	image.tofile(f)
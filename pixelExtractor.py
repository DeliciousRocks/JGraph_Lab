import os
import sys
from PIL import Image


if len(sys.argv) == 3:
	file_in_path = sys.argv[1]
	file_in_parts = file_in_path.split("/")
	file_in = file_in_parts[len(file_in_parts)-1]
	just_name = file_in[:-3]
	file_out = sys.argv[2]+just_name+"eps"
else: 
	file_in = "{0}.png"
	file_out = file_in[:-3]+"eps"

if not(os.path.exists(file_out)):
	#print(sys.argv)
	im = Image.open(file_in_path.replace("\r",""), 'r')
	output = "newgraph\n"
	width = im.width
	output += "xaxis min 0 max "+ str(width) +" nodraw\n"
	height = im.height
	output += "yaxis min 0 max "+ str(height) +" nodraw\n"

	mark_size = "marksize "+ str(1/width) + " " + str(1/height) + " "

	colors_used = {}
	pix_val = list(im.getdata())
	for h in range(height):
		for w in range(width):
			current_pixel = pix_val[(h * width)+ w]
			#print(current_pixel)
			if (type(current_pixel) == type(0)):
				pass
			elif ((len(current_pixel) == 3) or ((len(current_pixel) == 4) and (current_pixel[3] != 0))):
				color = str(current_pixel[0]/255) + " " + str(current_pixel[1]/255) + " " + str(current_pixel[2]/255)
				if color in colors_used.keys():
					colors_used[color].append(str(w) +" " + str(height - h) + " ")
				else:
					colors_used[color] = [str(w) + " " + str(height - h) + " "]
	for color in colors_used.items():
		output += "newcurve marktype box "+ mark_size +"linetype none color " + color[0] + " pts "
		for pixel in color[1]:
			output += pixel 
		output += "\n"
	f = open(file_out.replace("\r",""),"w")
	f.write(output)
	f.close()

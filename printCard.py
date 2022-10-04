from PIL import Image
import json, os, re, sys
def main():
	#Provide instructions on proper usage
	if len(sys.argv) == 1:
		print("usage: printCard.py card_data.json (optional: artwork_asset.jpg")

	if len(sys.argv) == 2:
		card_data_file_path = sys.argv[1]
		art_asset_path = ""

	if len(sys.argv) == 3:
		card_data_file_path = sys.argv[1]
		art_asset_path = sys.argv[2]

	#Read the JSON file
	card_file = open(card_data_file_path,"r")
	card_data = json.loads(card_file.read())

	symbol_size = 10
	art_height = 150
	art_width = 202
	card_output_file = card_data["Card_Name"].replace(" ","_")+".jgr"

	output = "newgraph\n"
	output += "xaxis min 0 max 240 nodraw\n"
	output += "yaxis min 0 max 336 nodraw\n"



	#Select the correct frame
	if (card_data["Color"] == "W"):
		if("Creature" in card_data["Type_Line"]["Type"]):
			output += "newcurve eps Frames_EPS/w_creature.eps "
		else:
			output += "newcurve eps Frames_EPS/w_noncreature.eps "
	elif (card_data["Color"] == "U"):
		if("Creature" in card_data["Type_Line"]["Type"]):
			output += "newcurve eps Frames_EPS/u_creature.eps "
		else:
			output += "newcurve eps Frames_EPS/u_noncreature.eps "
	elif (card_data["Color"] == "B"):
		if("Creature" in card_data["Type_Line"]["Type"]):
			output += "newcurve eps Frames_EPS/b_creature.eps "
		else:
			output += "newcurve eps Frames_EPS/b_noncreature.eps "
	elif (card_data["Color"] == "R"):
		if("Creature" in card_data["Type_Line"]["Type"]):
			output += "newcurve eps Frames_EPS/r_creature.eps "
		else:
			output += "newcurve eps Frames_EPS/r_noncreature.eps "
	elif (card_data["Color"] == "G"):
		if("Creature" in card_data["Type_Line"]["Type"]):
			output += "newcurve eps Frames_EPS/g_creature.eps "
		else:
			output += "newcurve eps Frames_EPS/g_noncreature.eps "
	elif (card_data["Color"] == "M"):
		if("Creature" in card_data["Type_Line"]["Type"]):
			output += "newcurve eps Frames_EPS/m_creature.eps "
		else:
			output += "newcurve eps Frames_EPS/m_noncreature.eps "
	elif (card_data["Color"] == "L"):
		output += "newcurve eps Frames_EPS/l_border.eps marksize "
	elif (card_data["Color"] == "A"):
		if (card_data["Type_Line"]["Subtype"] == "Vehicle"):
			output += "newcurve eps Frames_EPS/v_border.eps "
		else:
			if("Creature" in card_data["Type_Line"]["Type"]):
				output += "newcurve eps Frames_EPS/a_creature.eps "
			else:
				output += "newcurve eps Frames_EPS/a_noncreature.eps "
	output += "marksize 240 336 pts 120 168\n"

#Add the art, if provided
	if len(art_asset_path) > 0:
		art_asset_path_split = art_asset_path.split("/")
		art_asset_name = art_asset_path_split[len(art_asset_path_split)-1].replace(" ","_")
		art_asset_jgr = art_asset_name[0:len(art_asset_name)-3]+"jgr"
		art_asset_eps = art_asset_name[0:len(art_asset_name)-3]+"eps"
		art_asset_jgr_path = "Art_Assets_EPS/"+art_asset_jgr
		art_asset_eps_path = "Art_Assets_EPS/"+art_asset_eps
		f = open(art_asset_jgr_path,"w")
		f.write(imageToEPS(art_asset_path))
		f.close()
		os.system("jgraph "+art_asset_jgr_path+ " > "+art_asset_eps_path)
		output += "newcurve eps " + art_asset_eps_path + " marksize " + str(art_width) + " " + str(art_height) + " pts 120 224 \n"	

	#Add the mana value
	if len(card_data["Mana_Value"]) > 0:
		symbols = card_data["Mana_Value"].split("{")
		symbols=symbols[1:]
		symbols.reverse()
		location = 215
		for symbol in symbols:
			clean = symbol.split("}")[0]
			output += "newcurve eps Symbols_EPS/{"+clean+"}.eps marksize "+str(symbol_size)+" "+str(symbol_size)+" pts "+str(location)+" 310 \n"
			location -= 10
	#Add the card name	
	output += "newstring hjl vjc x 20 y 310 : "+card_data["Card_Name"]+"\n"

	#Add all of the types to the type line
	types = ""
	for t in card_data["Type_Line"]["Type"]:
		types += t +" "
	output += "newstring hjl vjc x 20 y 138 : "+card_data["Type_Line"]["Super_Type"]+types
	if len(card_data["Type_Line"]["Subtype"]) > 0:
		output += "- "+card_data["Type_Line"]["Subtype"]+"\n"
	else:
		output +="\n"		

	#Put all of the cards abilities into the text box
	ability_starting_height = 117
	for ability in card_data["Text_Box"]["Abilities"]:
		symbols = ability.find("{")
		if symbols == -1:

			output += "newstring hjl vjc x 20 y "+str(ability_starting_height)+" : " + ability + "\n"	
		else:

			current_x = 20
			index = 0
			while(index < len(ability)):
				if symbols >= 0:
					print(ability[index:])
					output += "newstring hjl vjc x " + str(current_x) + " y "+str(ability_starting_height)+" : " + ability[index:symbols] + "\n"	
					current_x += len(ability[index:symbols])
					symbol = ability[symbols+1:].split("}")[0]
					end_point = ability[index:].find("}") 
					print(end_point)
					output += "newcurve eps Symbols_EPS/{"+symbol+"}.eps marksize "+str(symbol_size)+" "+str(symbol_size)+" pts "+str(current_x + (symbol_size/2 ))+" "+str(ability_starting_height)+" \n"
					current_x += 10
					index += end_point + 1
					symbols = ability[index:].find("{")
				else:
					output += "newstring hjl vjc x " + str(current_x) + " y "+str(ability_starting_height)+" : " + ability[index:] + "\n"	
					index = len(ability)
		ability_starting_height -= 13

	#Add the flavor text, if present
	if len(card_data["Text_Box"]["Flavor_Text"]) > 0:
		output += "newstring hjl vjc fontsize 8 x 20 y 50 font Helvetica-Italic : " + card_data["Text_Box"]["Flavor_Text"] + "\n"	

	#If the card has power and toughness, add it to the card here
	if("Creature" in card_data["Type_Line"]["Type"]) or (card_data["Type_Line"]["Subtype"] == "Vehicle"):
		output += "newstring hjl vjc x 195 y 30 : "+card_data["Text_Box"]["Power"]+" / "+card_data["Text_Box"]["Toughness"]+"\n"		



				
			
	f = open(card_output_file.replace("\r",""),"w")
	f.write(output)
	f.close()

def imageToEPS(path):
	im = Image.open(path.replace("\r",""), 'r')
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
	return output
	
main()
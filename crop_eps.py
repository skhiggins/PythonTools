def crop_eps(filename, outfile = [], l = -1, b = -1, r = -1, t = -1):
	
	# Read the lines of the .eps file:
	with open(filename, 'r') as eps_infile:
		lines = eps_infile.readlines() 
	
	# Open the file to write to
	if outfile == []:
		toopen = filename
	else:
		toopen = outfile
	
	# Write lines, replacing the lines setting bounding box
	dim_args = [l, b, r, t]
	with open(toopen, 'w') as eps_outfile:
		for line in lines:
			if "BoundingBox" not in line:
				eps_outfile.write(line)
			else:
				# need to extract each number
				# note the order is l, b, r, t
				dimensions = line.split()
				new_dimensions = [dimensions[0]]
					# dimensions[0] is %%BoundingBox: or %%HiResBoundingBox:	
					
				counter = 0
				for arg in dim_args:
					counter = counter + 1
					if arg == -1:
						new_dimensions.append(dimensions[counter])
					else:
						if "HiRes" not in line:
							new_dimensions.append(str(arg))
						else:
							new_dimensions.append(str(arg) + ".000")
				new_dim_join = " ".join(new_dimensions)
				eps_outfile.write(new_dim_join + "\n")


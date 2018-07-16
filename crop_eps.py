def crop_eps(filename, outfile = [], l = -1, b = -1, r = -1, t = -1):
	
	# Read the lines of the .eps file:
	eps_infile = open(filename, 'r')
	lines = eps_infile.readlines() 
		# now that it's saved in lines we can close the file
	eps_infile.close()
	
	# Open the file to write to
	if outfile == []:
		eps_outfile = open(filename, 'w')
	else:
		eps_outfile = open(outfile, 'w')
	
	# Write lines, replacing the lines setting bounding box
	dim_args = [l, b, r, t]
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

	# Close new eps file		
	eps_outfile.close()

import os
main = os.path.join("C:/Dropbox", "FinancialInclusion", "POS")

# Store type 04 (corner stores)
myfile = "quint_income_pc_05_tot"
myinfile = os.path.join(main, "graphs", myfile + ".eps")
myoutfile = os.path.join(main, "graphs", myfile + "_cropped.eps")

crop_eps(myinfile, myoutfile, l = 64, r = 337)


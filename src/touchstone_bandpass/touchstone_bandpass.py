INFILE  = 'example.s1p'
OUTFILE = 'bp_LTE.s1p'

freqs = [(880e6, 960e6), (1710e6, 1880e6)]

LOW_MAG = -15 #dB

output = []
unit_line = ''
with open(INFILE, 'r') as f:
	for line in f:

		if line[0] == '!':
			continue
		if line[0] == '#':
			unit_line = line
			continue

		floats_list = []
		for item in line.split():
  			floats_list.append(float(item))

		ff = floats_list[0]

		phase = 0
		mag   = 0
		for freq in freqs:
			if (ff >= freq[0] and ff <= freq[1]):
				mag = LOW_MAG

		output.append(str(ff) + " " + str(mag) + " " + str(phase) + "\n")

with open(OUTFILE, 'w') as f:
	f.write(unit_line)

	for line in output:
		f.write(line)

import pygal


def parse_fasta_to_dict(FASTA_file):
	seq_dict = {}
	nt = ''
	idline = ''
	with open(FASTA_file, 'r') as fin:  # Read the input file
		for line in f:
			if line.startswith('>'):  # Save the sequences in a dictionary,
				if nt:
					seq_dict[idline] = nt
				idline = line.lstrip('>').rstrip()
				nt = ''
			else:
				sequence = line.rstrip('\n').upper()
				nt = nt + sequence
		seq_dict[idline] = nt
	return seq_dict


def fastq_to_fasta(fastq_file, fasta_file):
	with open(fastq_file, 'r') as f_in, \
			open(fasta_file, 'w')as f_out:
		counter = 0
		for line in f_in:
			counter += 1
			if counter % 4 == 1:
				line = line.rstrip()
				line = line.lstrip('@')
				idcode = '>' + line
			if counter % 4 == 2:
				line = line.rstrip()
				seq = line
			if counter % 4 == 0:
				print('{}\n{}'.format(idcode, seq), file=f_out)


def oneline_fasta(FASTA_file, fileout):
	with open(FASTA_file, 'r') as f, \
			open(fileout, 'w') as fout:  # Read the input file
		nt = ''
		idline = ''
		for line in f:
			if line.startswith('>'):  # Save the sequences in a dictionary,
				if nt:
					print('{}\n{}'.format(idline, nt), file=fout)
				idline = line.rstrip()  # taking away the newlines
				idline = idline.lstrip('>')
				nt = ''
			if not line.startswith('>'):
				sequence = line.rstrip().rstrip('\n').upper()
				nt = nt + sequence
		print('{}\n{}'.format(idline, nt), file=fout)


def plot_nucleotides(fastasequence, windowsize=100, step=50):
	'''
	This function takes a fasta sequence, joins all the sequences into 1 and slides a window over it and counts %
	Nucleotides across the window and plots it
	'''
	sequence_dict = parse_fasta_to_dict(fastasequence)
	nucleotides = 'ACTGN'  # Just so we can have everything in 1 dict
	nuc = {'A': [], 'C': [], 'T': [], 'G': [], 'N': [], 'midle_pos': []}

	allN = []
	for key in sequence_dict:  # this part takes the dictionary and makes it a string
		allN.append(sequence_dict[key])
	allN = ''.join(allN)

	upper_window = windowsize
	lower_window = 0
	while upper_window < len(allN):  # Count the nucleotides and append them alongside the windos into de dict list
		working_seq = allN[lower_window:upper_window]
		for Nuc in nucleotides:
			nuc[Nuc].append((working_seq.count(Nuc)/(upper_window-lower_window))*100)
			nuc['midle_pos'].append(upper_window - step)
		upper_window += step
		lower_window += step
	working_seq = allN[lower_window:]
	for Nuc in nucleotides:
		nuc[Nuc].append((working_seq.count(Nuc)/(upper_window-lower_window))*100)
		nuc['midle_pos'].append(upper_window - step)

	line_chart = pygal.Line()  # Lets plot
	line_chart.title = 'Nucleotide % across the file'
	line_chart.x_labels = nuc['midle_pos']
	for Nuc in nucleotides:
		line_chart.add(Nuc, nuc[Nuc])
	line_chart.render()

with open('gc.txt','r') as fin:
	plot_nucleotides(fin)
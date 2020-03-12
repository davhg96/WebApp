from matplotlib import pyplot as plt
import os

plt.style.use('ggplot')
def parse_fasta_to_dict(FASTA_file):
	seq_dict = {}
	nt = []
	idline = ''
	with open(FASTA_file, 'r') as fin:  # Read the input file
		for line in fin:
			if line.startswith('>'):  # Save the sequences in a dictionary,
				if nt:
					nt=''.join(nt)
					seq_dict[idline] = nt
				idline = line.lstrip('>').rstrip()
				nt = []
			else:
				sequence = line.rstrip('\n').upper()
				nt.append(sequence)
		nt = ''.join(nt)
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
		return 'done'

def oneline_fasta(FASTA_file, fileout):
	'''
	This function takes a fasta file and outputs a one line fasta file
	'''
	with open(FASTA_file, 'r') as f, \
			open(fileout, 'w') as fout:  # Read the input file
		nt = [] #Using lists makes it faster but needs some joining later
		idline = ''
		for line in f:
			if line.startswith('>'):  # Save the sequences in a dictionary,
				if nt:
					nt=''.join(nt)
					print('{}\n{}'.format(idline, nt), file=fout)
				idline = line.rstrip()  # taking away the newlines

				nt = []
			if not line.startswith('>'):
				sequence = line.rstrip().rstrip('\n').upper()
				nt.append(sequence)
		nt = ''.join(nt)
		print('{}\n{}'.format(idline, nt), file=fout)


def plot_nucleotides(fastasequence, windowsize=100, step=50, GC=False):
	'''
	This function takes a fasta sequence, joins all the sequences into 1 and slides a window over it and counts %
	Nucleotides across the window and plots it, Added functionality to choose if the user want s GC% or overall N freqs.
	'''
	sequence_dict = parse_fasta_to_dict(fastasequence)
	nuc={'midle_pos':[]}
	if GC:
		nucleotides=['GC','N']
		for Nuc in nucleotides:
			nuc[Nuc]=[]
		allN = []
		for key in sequence_dict:  # this part takes the dictionary and makes it a string
			allN.append(sequence_dict[key])
		allN = ''.join(allN)
		upper_window = windowsize#Start the window
		lower_window = 0
		while upper_window <= len(allN):  # Count the nucleotides and append them alongside the windos into de dict list
			working_seq = allN[lower_window:upper_window]
			nuc['GC'].append(((working_seq.count('G')+working_seq.count('C')) / (upper_window - lower_window)) * 100)
			if (upper_window - step) not in nuc['midle_pos']:  # Check if the middle pso is already added,
				# only add it if the previous is different
				nuc['midle_pos'].append(upper_window - step)
			upper_window += step  # move the window
			lower_window += step

		working_seq = allN[lower_window:]  # Take the end if th ewindow falls over the edge
		for Nuc in nucleotides:
			nuc[Nuc].append((working_seq.count(Nuc) / (len(allN) - lower_window)) * 100)
			if (lower_window + (len(working_seq) / 2)) not in nuc['midle_pos']:  # Check if the middle pso is already
				# added, only add it if the  previous is different
				nuc['midle_pos'].append(lower_window + (len(working_seq) / 2))

		for Nuc in nucleotides:
			if not any(nuc[Nuc]) == 0:  # Check if there are values, if not ignore that nucleotide
				plt.plot(nuc['midle_pos'], nuc[Nuc], label=Nuc)

		plt.title('GC% in Fasta file')
		plt.xlabel('Window middle position')
		plt.ylabel('GC%')
		plt.legend()

		plt.savefig('test')
		return
	# General plot code, similar to the GC code but changes the dictionary
	else:
		nucleotides = 'ACTGN'  # Just so we can have everything in 1 dict
		for Nuc in nucleotides:
			nuc[Nuc]=[]
		allN = []
		for key in sequence_dict:  # this part takes the dictionary and makes it a string
			allN.append(sequence_dict[key])
		allN = ''.join(allN)
		upper_window = windowsize
		lower_window = 0
		while upper_window <= len(allN):  # Count the nucleotides and append them alongside the windos into de dict list
			working_seq = allN[lower_window:upper_window]
			for Nuc in nucleotides:

				nuc[Nuc].append((working_seq.count(Nuc) / (upper_window - lower_window)) * 100)
				if (upper_window - step) not in nuc['midle_pos']:  # Check if the middle pso is already added,
																	# only add it if the previous is different
					nuc['midle_pos'].append(upper_window - step)
			upper_window += step  # move the window
			lower_window += step

		working_seq = allN[lower_window:] # Take the end if th ewindow falls over the edge
		for Nuc in nucleotides:
			nuc[Nuc].append((working_seq.count(Nuc) / (len(allN) - lower_window)) * 100)
			if (lower_window + (len(working_seq)/2)) not in nuc['midle_pos']:  # Check if the middle position is already
																			# added, only add it if the  previous is different
				nuc['midle_pos'].append(lower_window + (len(working_seq)/2))


		for Nuc in nucleotides:
			if not any(nuc[Nuc])==0: #Check if there are values, if not ignore that nucleotide
				plt.plot(nuc['midle_pos'], nuc[Nuc], label=Nuc)

		plt.title('Nucleotide abundance in Fasta file')
		plt.xlabel('Window middle position')
		plt.ylabel('Nucleotide abundance (%)')
		plt.legend()

		plt.savefig('test')
		return


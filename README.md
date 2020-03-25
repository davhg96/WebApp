#### **Description**
This is an in development web application designed to perform basic bioinformatics tasks.
The users can upload their files and perform file transformations such as mutate multiline fasta files into 
oneline fasta files, transform fastq files into fasta files or plot the nucleotide abundance across the input file


#### **Usage:**
##### Run these commands in your linux console:

First clone the project to the desired location:

`git clone https://github.com/davhg96/WebApp.git ./`

#### If you don't have conda installed on your computer please install it from here:

https://www.anaconda.com/distribution/

###### Import and activate the attached conda environment.

`conda env create -f Flask.yml`

`conda activate Flask`

###### Check that it was instaleld propperly:

`conda list`



Once the environmen is active run the web script

`python web.py`

And access the address that pops up in your comand line.
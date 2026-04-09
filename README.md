# BINF6112_ContigBinningChallenge
**UNCC BINF6112 - Programming II April 7th Challenges**

Given mulitple *Bothrops insularis* BLAST result TSV files and a contig TXT file containing contig ids and contig lengths, contigs are filtered by bin priority, bit score, and a coverage threshold. Summary statistics are generated for each bin, as well as two bar plots displaying the number of contigs per bin and the total base pairs per bin. Default coverage threshold is set to 0.9 to ensure that the highest-quality contigs are being used for assembly at a later point. 


## License: 
**GNU General Public License Version 3**

The GNU GPL is a license that ensures code is open-source. GNU GPL allows others to utilize, modify, or distribute code. If other users modify the code, then these users are expected to share their changes to the code under a GNU GPL to maintain the open-source integrity of the code.

I chose to use the GNU GPL to make the code easily accessible for anyone to use, or to further build upon. 

[Project URL](https://github.com/bluker17/BINF6112_ContigBinningChallenge)

## Author:
**Bobby Luker**
rluker@charlotte.edu
UNCC ID: 801484356

## Project File Structure:
```
└── 📁data
    ├── Binsularis_BLAST_Apicomplexa.tsv
    ├── Binsularis_BLAST_Hepatozoon.tsv
    ├── Binsularis_BLAST_Mitochondrion.tsv
    ├── Binsularis_BLAST_SexualChromosomes.tsv
    ├── Binsularis_contig_sizes.txt
└── 📁example_runs
    └── 📁0.25
    └── 📁0.50
    └── 📁0.75
    └── 📁0.90
└── 📁output
└── 📁src
    └── 📁prioritization
        ├── __init__.py
        ├── priority.py
    └── 📁reader
        ├── __init__.py
        ├── read_files.py
    └── 📁summary_statistics
        ├── __init__.py
        ├── summary.py
├── environment-alternative.yml
├── environment.yml
├── LICENSE
├── main.py
├── README.md
└── run_test.sh
```

## Testing Instructions:
04/08/2026

### Installation

For MacOS:
```bash
conda env create -f environment.yml
```
For Windows/Linux:
```bash
conda env create -f environment-alternative.yml
```
Conda will automatically create an environment named bin_chal with all the specified packages and versions.

### Usage

1. Activate the environment:
```bash
conda activate bin_chal
```
2. Run following command to test:
```bash
bash run_test.sh
```

#### Command-Line Arguments:
| Argument                          | Description                                  | Default               |
| --------------------------------- | -------------------------------------------- | --------------------- |
| `-i`, `--input_blast_files`       | BLAST results as TSV files |[data/Binsularis_BLAST_Apicomplexa.tsv,<br> data/Binsularis_BLAST_Hepatozoon.tsv,<br> data/Binsularis_BLAST_Mitochondrion.tsv,<br> data/Binsularis_BLAST_SexualChromosomes.tsv]|
| `-c`, `--contig_file` | TXT file containing contig ids and contig lengths                           | data/Binsularis_contig_sizes.txt|
| `-t`, `--threshold` | Coverage threshold float                           | 0.9|
| `-s`, `--summary_stats_file`       | TSV ouput file containing summary statistics             | output/summary_stats.tsv|
| `-d`, `--data_frame_file` | TSV output file containing contig classification data frame. This frame is used for summary statistics                    | output/data_frame.tsv|
| `--contigs_barplot` | PNG output file containing a barplot of contigs per bin                    | output/contigs_per_bin.png|
| `--bps_barplot` | PNG output file containing a barpolot of toal base pairs per bin                    | output/total_bps_per_bin.png|



Expected Output:

- Runs the program with multiple coverage thresholds. 
- Prints output locations of each example run.
- Prints completion statement upon all runs. 

## Overview:
`data`: Contains the BLAST result TSV files and the contig size TXT file.

`src`: Contains multiple subdirectories leading to modules handling the input and output data. 
1. `reader` contains module `read_files.py` which reads in the BLAST result TSV files and contig size TXT file to merge all files into one main data frame for further analysis.
2. `prioritization` contains module `priority.py` which adds a bin column to the data frame. The data frame is then filtered by the highest priority bin and bitscore for each contig id. 
3. `summary_statistics` contains module `summary.py` which writes output TSV files of the data frame used for statistical analysis, a data frame containing summary statistics, a barplot of total base pairs per bin, and a barplot of contigs per bin.

`main.py` executes all modules to produce results. 

`run_test.sh`: Bash script that executes multiple test runs at different coverage threshold values for the user.

`example_runs`: Contains output file directories for different coverage threshold values when `run_test.sh` is executed.

## References
OpenAI's ChatGPT model GPT-5.3 was used to guide coding decisions in:

`reader.py`: how to convert pandas columns into numpy arrays for coverage threshold analysis, how to use .concat() to combine two pandas table as one.

`priority.py`: how to use .sort_values() and .drop_duplicates() to effetively filter a data frame.

`summary.py`: how to use .groupby(), .agg(), and pd.NamedAgg() when generating the summary statistics data frame.

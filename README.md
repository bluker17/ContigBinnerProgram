# Contig Binner Program
**UNCC BINF6112 - Programming II April 7th Challenges**

For a draft genome assembly, when given multiple BLAST result TSV files and a contig TXT file containing contig IDs and lengths, the contigs are filtered by bin priority, bitscore, coverage threshold, and contig size threshold. Summary statistics are generated for each bin, along with two bar plots showing the number of contigs per bin and the total base pairs per bin. The default coverage threshold is set to 0.9 to ensure that only the highest-quality contigs are used. However, the user can adjust the coverage threshold to relax this restriction if needed.

[Project URL](https://github.com/bluker17/BINF6112_ContigBinningChallenge)

## License: 
**GNU General Public License Version 3**

Review `LICENSE` for more information. 

## Author:
**Bobby Luker**
rluker@charlotte.edu
UNCC ID: 801484356

## Project File Structure:
```
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
└── 📁testing_materials
    └── 📁example_data
        └── 📁blast_files
            ├── Binsularis_BLAST_Apicomplexa.tsv
            ├── Binsularis_BLAST_Hepatozoon.tsv
            ├── Binsularis_BLAST_Mitochondrion.tsv
            ├── Binsularis_BLAST_SexualChromosomes.tsv
        ├── Binsularis_contig_sizes.txt
        ├── prioritization.tsv
    └── 📁example_outputs
        └── 📁0.25
        └── 📁0.50
        └── 📁0.75
        └── 📁0.90
    └── 📁expected_example_outputs
        └── 📁0.25
        └── 📁0.50
        └── 📁0.75
        └── 📁0.90
    ├── run_test.sh
├── .gitattributes
├── .gitignore
├── environment.yml
├── LICENSE
├── main.py
└── README.md
```

## Testing Instructions:
### Installation

1. Download or clone the repository:
```bash
git clone https://github.com/bluker17/ContigBinnerProgram.git
```
2. Create the conda environment. Conda will automatically create an environment named `bin_chal` with all the specified packages and versions.
```bash
conda env create -f environment.yml
```

### Usage
1. Activate the environment:
```bash
conda activate bin_chal
```
2. Run following command to test:
```bash
testing_materials/run_test.sh
```
3. Example single-line terminal command to execute the program:
```bash
./main.py -i data/blast_files -c contig_sizes.txt -p priority_file.tsv --coverage_threshold 0.5
```
4. If the above commands do not work, then please make `main.py` and `run_test.sh` executuable with the following command and retry executing the program.
```bash
chmod +x main.py
chomd +x testing_materials/run_test.sh
```

#### Command-Line Arguments:
| Argument                          | Description                                  | Default               |
| --------------------------------- | -------------------------------------------- | --------------------- |
| `-i`, `--input_blast_files`       | BLAST results as TSV files |example_data/blast_files/|
| `-c`, `--contig_file` | TXT file containing contig ids and contig lengths                           | example_data/Binsularis_contig_sizes.txt|
| `-p`, `--priority_file` | TSV file containing bins and priority. 'Bin' corresponds to files assigned to contigs. 'priority' corresponds to numerical priority classification for each bin. The lowest numerical value roeesponds to the highest priority bin.                           | example_data/prioritization.tsv|
| `--coverage_threshold` | Coverage threshold float. Used to filter out contigs less than the threshold.                           | 0.9|
| `--contig_size_threshold` | Coverage threshold int. Used to filter out contigs less than a specific bp size.                           | 3000|
| `-s`, `--summary_stats_file`       | TSV ouput file containing summary statistics             | output/summary_stats.tsv|
| `-d`, `--data_frame_file` | TSV output file containing contig classification data frame. This frame is used for summary statistics                    | output/data_frame.tsv|
| `--contigs_barplot` | PNG output file containing a barplot of contigs per bin                    | output/contigs_per_bin.png|
| `--bps_barplot` | PNG output file containing a barpolot of toal base pairs per | `--verbose` | Enables detailed logging and displays warnings during execution for debugging. Default behavior is silent (no extra logs or warnings). | False |


Expected Output:

- Classifies BLAST contigs into bins based upon contig size, coverage, bitscore, and provided priority.
    - Data frame that has contigs binned is used to create summary statistics and visualizations. This data frame is saved to a TSV file.
- Summary statistics and visualizations are generated:
    - Summary statistics saved to TSV file.
    - Bar chart displaying the total base pairs per bin
    - Bar chart showing the count of contigs per bin.
- Prints output locations of each example run.
- Prints completion statement upon successful execution of run(s).

## Overview:
`example_data`: Contains the example BLAST result TSV files and the contig size TXT file.

`src`: Contains multiple subdirectories leading to modules handling the input and output data. 
1. `reader` contains module `read_files.py` which reads in the BLAST result TSV files and contig size TXT file to merge all files into one main data frame for further analysis.
2. `prioritization` contains module `priority.py` which adds a bin column to the data frame. The data frame is then filtered by the highest priority bin and bitscore for each contig id. 
3. `summary_statistics` contains module `summary.py` which writes output TSV files of the data frame used for statistical analysis, a data frame containing summary statistics, a barplot of total base pairs per bin, and a barplot of contigs per bin.

`main.py` executes all modules to produce results. 

`run_test.sh`: Bash script that executes multiple test runs at different coverage threshold values for the user.

`example_runs`: Contains output file directories for different coverage threshold values when `run_test.sh` is executed.

## References
### Python Standard Library

**`argparse`**  
Python Software Foundation. (2024). *argparse — Parser for command-line options, arguments and sub-commands*. Python 3 Documentation.
https://docs.python.org/3/library/argparse.html

Used for parsing command-line arguments and handling CLI input configuration.

---

**`matplotlib`**
Hunter, J. D., Droettboom, M., & the Matplotlib development team. (2025). *Matplotlib documentation*. Matplotlib.
https://matplotlib.org/stable/contents.html

Used for creating data visualizations, charts, graphs, and plotting analytical results.

---

**`pandas`**
The pandas development team. (2025). *pandas documentation*. pandas.
https://pandas.pydata.org/docs/

Used for data manipulation, tabular data processing, and CSV file handling.

---

**`pathlib`**
Python Software Foundation. (2024). *pathlib — Object-oriented filesystem paths*. Python 3 Documentation.
https://docs.python.org/3/library/pathlib.html

Used for file and directory path handling.

---

**`sys`**
Python Software Foundation. (2024). *sys — System-specific parameters and functions*. Python 3 Documentation.
https://docs.python.org/3/library/sys.html

Used for interacting with interpreter-level functionality such as command-line arguments and program exit handling.

---

**`warnings`**
Python Software Foundation. (2024). *warnings — Warning control*. Python 3 Documentation.
https://docs.python.org/3/library/warnings.html

Used to control how warning messages are handled in Python programs, including filtering, suppressing, or escalating warnings such as deprecation notices during runtime.

---

### AI Assistance
This project was developed with the help of [ChatGPT-5.3](https://chatgpt.com) and [ChatGPT-5.5](https://chatgpt.com) by [OpenAI](https://openai.com).

ChatGPT assisted with:
- pandas code architecture and implementation
- Debugging and code review

# 20260407 — Contig Binning Challenge

## Background

You are working with a draft genome assembly of *Bothrops insularis*, a venomous pit viper endemic to Queimada Grande island off the coast of Brazil. The assembly contains **6,427 contigs** of varying sizes. Not all contigs belong to the snake's nuclear genome — some may originate from mitochondrial DNA, from an intracellular Apicomplexa parasite, or from the sex chromosomes (chromosome W), which in snakes behave very differently from autosomes.

To help classify contigs, four BLAST searches were run against curated reference databases. Your job is to use these results, together with contig size information, to **bin each contig** into a putative category.

## Data

All data files are in the `data/` directory.

### BLAST result tables

Each `.tsv` file contains tab-separated BLAST output produced with:

```
blastn -outfmt "6 qseqid staxids bitscore std"
```

Only the **top 5 hits** per query were retained. The 14 columns are:

| # | Column    | Description                          |
|---|-----------|--------------------------------------|
| 1 | qseqid    | Query contig name                    |
| 2 | staxids   | Subject taxonomy ID(s)               |
| 3 | bitscore  | Bit score of the alignment           |
| 4 | qseqid    | Query contig name (repeated by `std`)|
| 5 | sseqid    | Subject sequence accession           |
| 6 | pident    | Percentage identity                  |
| 7 | length    | Alignment length (bp)                |
| 8 | mismatch  | Number of mismatches                 |
| 9 | gapopen   | Number of gap openings               |
|10 | qstart    | Query start position                 |
|11 | qend      | Query end position                   |
|12 | sstart    | Subject start position               |
|13 | send      | Subject end position                 |
|14 | evalue    | E-value                              |

The four BLAST tables are:

- `Binsularis_BLAST_Mitochondrion.tsv` — hits against a mitochondrial DNA database
- `Binsularis_BLAST_Apicomplexa.tsv` — hits against an Apicomplexa (parasite) database
- `Binsularis_BLAST_Hepatozoon.tsv` — hits against a Hepatozoon (a specific Apicomplexa genus) database
- `Binsularis_BLAST_SexualChromosomes.tsv` — hits against a chromosome W database

### Contig sizes

- `Binsularis_contig_sizes.txt` — two whitespace-separated columns: `contig_name` and `size_bp`.

## Your Task

Write a Python script (or a small pipeline of scripts) that produces a **classification table** assigning each contig to one of the following bins:

| Bin                     | Meaning                                      |
|-------------------------|----------------------------------------------|
| Mitochondrion           | Putative mitochondrial DNA                   |
| Apicomplexa             | Putative Apicomplexa parasite sequence        |
| Sexual Chromosome       | Putative chromosome W                        |
| Diploid Chromosome      | Putative autosomal (nuclear, non-W) sequence |


### Rules

1. **Ignore contigs smaller than 3,000 bp.** They are too short to classify reliably. Exclude them from the analysis entirely.

2. **Coverage matters.** A contig that has a hit covering only 200 bp out of a 500,000 bp contig should not be treated the same as one where the hit spans a substantial fraction of the contig. For each contig, compute the **total aligned query length** (using `qstart` and `qend` from the BLAST hits) as a fraction of the contig's total size. Use this alignment coverage to inform your classification — you are free to decide on a reasonable threshold, but you must justify your choice.

3. **Priority rule.** If a contig appears in more than one BLAST table, apply this priority order for classification:

   **Mitochondrion > Apicomplexa > Sexual Chromosome > Diploid Chromosome**

   That is, if a contig has hits in both the Mitochondrion and the Sexual Chromosome tables, classify it as Mitochondrion (the mtDNA is the most distinctive signal).

   *Note:* Hepatozoon is a genus within Apicomplexa. Hits from the Hepatozoon table should reinforce (not override) Apicomplexa classification — use your judgment on how to integrate this.

4. **Retain the best hit.** In your final output table, include the **single most informative hit** (highest bitscore) from the database that determined the classification. The output should contain at minimum: contig name, contig size, bin, best-hit accession, bitscore, e-value, percent identity, and alignment coverage of the contig.

5. **Summary statistics.** After classification, produce a brief report with:
   - Number and total base pairs in each bin.
   - Number of contigs that had no hit in any database (Unclassified).
   - A bar chart showing the number of contigs per bin.
   - A bar chart showing the total base pairs per bin.

## Deliverables

- A Python script (or scripts) that reads the data files and produces the classification table and summary.
- The classification table saved as a `.tsv` file.
- The summary charts saved as `.png` files.
- A brief written explanation (in comments or a companion `.md` file) of any thresholds you chose and why.

## Tips: Libraries You Should Use

This challenge is an opportunity to practice with **Pandas**, **NumPy**, and **Matplotlib**. Below are some hints on where each library fits in — we are deliberately not giving you the code. Figuring out the exact syntax and function calls is part of the exercise.

### Pandas

Pandas is your primary tool here. Think about how to use it for:

- **Reading the data.** The BLAST tables are tab-separated with no header row. Pandas can read these directly if you tell it the separator and provide column names yourself. The contig sizes file is similar.
- **Merging tables.** You will need to combine information from multiple BLAST files and the contig sizes table into a single working DataFrame. Think about which column they share and what kind of join makes sense (inner? outer? left?).
- **Filtering.** Removing contigs below the size threshold is a one-liner once the data is in a DataFrame.
- **Grouping and aggregating.** Computing summary statistics per bin (count, total bp) is exactly what `groupby` was designed for.
- **Sorting.** To pick the best hit per contig (highest bitscore), think about how sorting followed by dropping duplicates — or, alternatively, using `groupby` with an aggregation that selects the top row — could help.

### NumPy

NumPy operates underneath Pandas, but it is useful to call on directly when you need:

- **Vectorized arithmetic.** Computing alignment coverage for every row at once (aligned length divided by contig size) is much faster and cleaner as a vector operation than as a loop.
- **Conditional logic on arrays.** Assigning bins based on multiple conditions can be approached with `numpy.select` or `numpy.where`, which evaluate conditions across entire columns simultaneously.
- **Thresholding.** Filtering rows that meet a minimum coverage or bitscore threshold is natural with NumPy boolean arrays.

### Matplotlib

Matplotlib will handle your summary visualizations:

- **Bar charts.** Think about `plt.bar()` or the Pandas `.plot(kind="bar")` shortcut for showing counts or totals per bin.
- **Labeling.** Your charts should have axis labels, a title, and (optionally) value annotations on each bar so the reader can see exact numbers at a glance.
- **Saving figures.** Use `savefig()` with an appropriate DPI so the output is publication-quality.
- **Subplots.** If you want both charts (contig count and total bp) side by side, look into `plt.subplots(1, 2, ...)`.

### General Python

- **Argparse.** As always, use `argparse` to handle input file paths so your script is not hard-coded to specific locations.
- **Docstrings and type hints.** Document your functions.
- **Guard clause.** Wrap your entry point with `if __name__ == "__main__":`.

## Suggested AI Prompt (If You Use AI)

You are welcome to use generative AI tools. If you do, **you must document your usage** — state which tool, what prompts you used, and how the output was incorporated. Failing to disclose AI use is a violation of academic integrity policy.

A starting prompt you might adapt:

> "Write a Python 3 script that reads multiple BLAST output tables (tab-separated, outfmt 6 with extra columns for qseqid, staxids, and bitscore prepended to the standard columns) and a contig sizes file. The script should classify each contig into bins based on which database produced the best hit, using a priority system. Use Pandas for data manipulation, NumPy for vectorized operations, and Matplotlib for bar charts. Include argparse, docstrings, and type hints."

Remember: **you are responsible for understanding and verifying any code an AI generates.**

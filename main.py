#!/bin/usr/env python3
# -*- coding: utf-8 -*-
import argparse, sys
from pathlib import Path

from src.reader.read_files import Reader
from src.prioritization.priority import Prioritizer
from src.summary_statistics.summary import SummaryStatistics


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for the program.

    Returns
    -------
    argparse.Namespace
    Object containing parsed arguments.
    """
    parser = argparse.ArgumentParser(description="File paths for input and output files.")

    parser.add_argument(
        "-i", "--input_blast_files",
        required=True,
        default=["example_data/blast_files/",
                    "data/Binsularis_BLAST_Hepatozoon.tsv",
                    "data/Binsularis_BLAST_Mitochondrion.tsv",
                    "data/Binsularis_BLAST_SexualChromosomes.tsv"],
        type=str,
        help="Path to input files containing BLAST results."
    )
    parser.add_argument(
        "-c", "--contig_file",
        required=True,
        default="example_data/Binsularis_contig_sizes.txt",
        type=str,
        help="Path to input file containing contig sizes."
    )
    parser.add_argument(
        "-p", "--priority_file",
        required=True,
        default="example_data/prioritization.tsv",
        type=str,
        help="Path to input TSV file for the prioritization labels."
    )
    parser.add_argument(
        "-s", "--summary_stats_file",
        required=False,
        default="output/summary_stats.tsv",
        type=str,
        help="Path to output file for a summary statistics TSV file. Default is output/summary_stats.tsv."
    )
    parser.add_argument(
        "-d", "--data_frame_file",
        required=False,
        default="output/data_frame.tsv",
        type=str,
        help="Path to output TSV file for the final data frame used to generate summary statistics and visualizations. Default is output/data_frame.tsv."
    )
    parser.add_argument(
        "--contigs_barplot",
        required=False,
        default="output/contigs_barplot.png",
        type=str,
        help="Path to output file for summary bar plot of contigs per bin. Default is output/contigs_barplot.png."
    )
    parser.add_argument(
        "--bps_barplot",
        required=False,
        default="output/bps_barplot.png",
        type=str,
        help="Path to output file for summary bar plot of total base pairs per bin. Default is output/bps_barplot.png."
    )
    parser.add_argument(
        "--coverage_threshold",
        required=False,
        default=0.9,
        type=float,
        help="Threshold for coverage to classify contigs. Default is 0.9."
    )
    parser.add_argument(
        "--contig_size_threshold",
        required=False,
        default=3000,
        type=int,
        help="Threshold for contig size to classify contigs. Default is 3000."
    )

    return parser.parse_args()

def validate_args(args: argparse.Namespace):
    """
    Validate the parsed command-line arguments.

    Parameters
    ----------
    args : argparse.Namespace
    Object containing parsed arguments.

    Raises
    ------
    ValueError
    If any of the arguments are invalid.
    """

# Checking blast directory path and contained file paths
    directory = Path(args.input_blast_files)

    if not directory.is_dir():
        raise ValueError("Input BLAST files path must be a directory containing TSV files.")

    bins = set()
    with Path(args.priority_file).open() as f:
        next(f)
        for line in f:
            parts = line.strip().split("\t")
            try:
                value = int(parts[1])
            except ValueError:
                raise ValueError("Bin labels in the priority file must be integers.")
            bins.add(parts[0])

    for file in directory.iterdir():
        if not file.name.endswith(".tsv"):
            raise ValueError("Input files must be TSV files with .tsv extension.")
        filepath = Path(file)
        if not filepath.is_file():
            raise ValueError(f"Input file {file} does not exist.")
        if file.name not in bins:
            raise ValueError(f"Input file {file} is not listed in the priority file.")
        
# Checking the files for appropriate extensions and existence.
    if not args.contig_file.endswith(".txt"):
        raise ValueError("Contig file must be a text file with .txt extension.")
    
    if not args.contigs_barplot.endswith(".png"):
        raise ValueError("Contigs bar plot file must be a PNG file with .png extension.")

    if not args.bps_barplot.endswith(".png"):
        raise ValueError("Base pairs bar plot file must be a PNG file with .png extension.")
    
    if not args.summary_stats_file.endswith(".tsv"):
        raise ValueError("Summary statistics file must be a TSV file with .tsv extension.")
    
    if not args.data_frame_file.endswith(".tsv"):
        raise ValueError("Data frame file must be a TSV file with .tsv extension.")
    
# Checking the thresholds.
    if not 0 <= args.coverage_threshold <= 1:
        raise ValueError("Coverage threshold must be a float between 0 and 1.")
    if args.contig_size_threshold <= 0:
        raise ValueError("Contig size threshold must be a positive integer.")
    if not isinstance(args.contig_size_threshold, int):
        raise ValueError("Contig size threshold must be an integer.")

def main() -> int: 
    args = parse_args()

    sys.stdout.write("""
    Arguments received:
        Contig File Path: {contig_file}
        Input BLAST File Paths: {input_blast_files}
        Priority File Path: {priority_file}
        Coverage Threshold: {coverage_threshold}
        Contig Size Threshold: {contig_size_threshold}
        Output Data Frame File Path: {data_frame_file}
        Output Summary Statistics File Path: {summary_stats_file}
        Contigs Bar Plot File Path: {contigs_barplot}
        Base Pairs Bar Plot File Path: {bps_barplot}
    """.format(
        contig_file=args.contig_file,
        input_blast_files=args.input_blast_files,
        priority_file=args.priority_file,
        coverage_threshold=args.coverage_threshold,
        contig_size_threshold=args.contig_size_threshold,
        summary_stats_file=args.summary_stats_file,
        data_frame_file=args.data_frame_file,
        contigs_barplot=args.contigs_barplot,
        bps_barplot=args.bps_barplot
    ))

    validate_args(args)

# Reading in the input files to create the main BLAST data frame.
    reader = Reader(args.input_blast_files, args.contig_file, args.coverage_threshold, args.contig_size_threshold)
    BLAST_df = reader.read_main()

# Filtering the BLAST data frame to include priorities based upon the coverage threshold and the bins assigned to each contig.  
    prioritizer = Prioritizer(BLAST_df, args.priority_file)
    priority_df = prioritizer.priority_main()

# Generate summary statistics, visualizations, and ouput files from the priority data frame. 
    summary_stats = SummaryStatistics(priority_df, args.summary_stats_file, args.contigs_barplot, args.bps_barplot, args.data_frame_file)
    summary_stats.summary_main()

    sys.stdout.write("""
    Program executed successfully.
        Output Data Frame File Path: {data_frame_file}
        Output Summary Statistics File Path: {summary_stats_file}
        Contigs Bar Plot generated at: {contigs_barplot}
        Base Pairs Bar Plot generated at: {bps_barplot}
    """.format(
        data_frame_file=args.data_frame_file,
        summary_stats_file=args.summary_stats_file,
        contigs_barplot=args.contigs_barplot,
        bps_barplot=args.bps_barplot
    ))

    return 0

if __name__ == "__main__":
    sys.exit(main())
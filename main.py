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
        nargs="+",
        required=False,
        default=["data/Binsularis_BLAST_Apicomplexa.tsv",
                    "data/Binsularis_BLAST_Hepatozoon.tsv",
                    "data/Binsularis_BLAST_Mitochondrion.tsv",
                    "data/Binsularis_BLAST_SexualChromosomes.tsv"],
        type=str,
        help="Path to input files containing BLAST results"
    )
    parser.add_argument(
        "-c", "--contig_file",
        required=False,
        default="data/Binsularis_contig_sizes.txt",
        type=str,
        help="Path to input file containing contig sizes"
    )
    parser.add_argument(
        "-s", "--summary_stats_file",
        required=False,
        default="output/summary_stats.tsv",
        type=str,
        help="Path to output file for a summary statistics TSV file"
    )
    parser.add_argument(
        "-d", "--data_frame_file",
        required=False,
        default="output/data_frame.tsv",
        type=str,
        help="Path to output TSV file for the final data frame used to generate summary statistics and visualizations."
    )
    parser.add_argument(
        "--contigs_barplot",
        required=False,
        default="output/contigs_barplot.png",
        type=str,
        help="Path to output file for summary bar plot of contigs per bin"
    )
    parser.add_argument(
        "--bps_barplot",
        required=False,
        default="output/bps_barplot.png",
        type=str,
        help="Path to output file for summary bar plot of total base pairs per bin"
    )
    parser.add_argument(
        "-t", "--threshold",
        required=False,
        default=0.9,
        type=float,
        help="Threshold for coverage to classify contigs"
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
    for file in args.input_blast_files:
        if not file.endswith(".tsv"):
            raise ValueError("Input files must be TSV files with .tsv extension.")
        path = Path(file)
        if not path.is_file():
            raise ValueError(f"Input file {file} does not exist.")
        
    if len(args.input_blast_files) != 4:
        raise ValueError("Exactly 4 input files must be provided.")

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
    
    if not args.threshold >= 0 and args.threshold <= 1:
        raise ValueError("Threshold must be a float between 0 and 1.")

def main() -> int: 
    args = parse_args()

    sys.stdout.write("""
    Arguments received:
        Contig File Path: {contig_file}
        Input BLAST File Paths: {input_blast_files}
        Coverage Threshold: {threshold}
        Output Data Frame File Path: {data_frame_file}
        Output Summary Statistics File Path: {summary_stats_file}
        Contigs Bar Plot File Path: {contigs_barplot}
        Base Pairs Bar Plot File Path: {bps_barplot}
    """.format(
        contig_file=args.contig_file,
        input_blast_files=args.input_blast_files,
        threshold=args.threshold,
        summary_stats_file=args.summary_stats_file,
        data_frame_file=args.data_frame_file,
        contigs_barplot=args.contigs_barplot,
        bps_barplot=args.bps_barplot
    ))

    validate_args(args)

# Reading in the input files to create the main BLAST data frame.
    reader = Reader(args.input_blast_files, args.contig_file, args.threshold)
    BLAST_df = reader.read_main()

# Filtering the BLAST data frame to include priorities based upon the coverage threshold and the bins assigned to each contig.  
    prioritizer = Prioritizer(BLAST_df)
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
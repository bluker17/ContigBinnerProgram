#!/bin/usr/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import re

class Reader:
    """
    A class that reads in TSV files containing BLAST results and a teb-delimited text file.
    """
    def __init__(self, tsv_files: list[str], contigs_file: str, threshold: float = 0.1):
        self.tsv_files = tsv_files
        self.tsv_df_name = None
        self.data_frame = None
        self.col_headers = ["qseqid", "staxids", "bitscore", "sseqid", "pident", "length", "mismatch", "gapopen", "qstart", "qend", "sstart", "send", "evalue"]
        self.threshold = threshold

        self.main_df = None
        self.priority_df = None

        self.contigs_file = contigs_file
        self.contigs_df = None

    def read_contigs(self):
        """
        Reads in contigs from a tab-delimited text file as a data frame. Then, filters out contigs that are less than or equal to 3000 bp in length. 
        """
        self.contigs_df = pd.read_csv(self.contigs_file, sep= "\t", header=None, names=["contig_name", "size_bp"])
        self.contigs_df = self.contigs_df.query("size_bp >= 3000")
    
    def get_df_name(self, tsv_file:str):
        """
        Gets the name of the data frame based on the input file name.

        Inputs
        ------
        tsv_file: str - Path to the TSV file
        """
        self.tsv_df_name = re.search(r'_([^_]+)\.', tsv_file).group(1) + "_df"


    def read_blast_results(self, tsv_file: str):
        """
        Reads in BLAST results from a TSV file as a data frame. Then, filters out duplicate columns and names the columns according to the BLAST output format. Adds a column to the data frame that contains the name of the data frame.

        Inputs
        ------
        tsv_file: str - Path to the TSV file
        """
        self.data_frame = self.tsv_df_name

        self.data_frame = pd.read_csv(tsv_file, sep="\t", index_col=False, header=None)
        self.data_frame = self.data_frame.drop(self.data_frame.columns[3], axis=1)
        self.data_frame.columns = self.col_headers
        self.data_frame.insert(0, "bin", self.tsv_df_name)
        #print(self.data_frame["bin"].unique())

    def generate_main_df(self):
        """
        Generates a main data frame that contains all the BLAST results from the input TSV files. 
        """
        for file in self.tsv_files:
            self.get_df_name(file)
            self.read_blast_results(file)
            self.main_df = pd.concat([self.main_df, self.data_frame], ignore_index=True) if self.main_df is not None else self.data_frame


    def merge_main_df(self):
        """
        Merges the main data frame with the contigs data frame based on the contig names.
        """
        self.main_df = pd.merge(self.contigs_df, self.main_df, left_on = "contig_name", right_on = "qseqid", how = "inner")

    def add_coverage(self):
        """
        Uses numpy to calculate the coverage for each contig. Adds a column to the main data frame that contains the coverage of the BLAST hits. The coverage is calculated as the length of the BLAST hit divided by the size of the contig.
        """
        qend = self.main_df["qend"].to_numpy()
        qstart = self.main_df["qstart"].to_numpy()
        size_bp = self.main_df["size_bp"].to_numpy()

        coverage = (qend - qstart) / size_bp

        self.main_df["coverage"] = coverage

    def coverage_threshold(self):
        """
        Filters the main data frame based on a coverage threshold. Only retains rows where the coverage is greater than or equal to the threshold.
        """
        self.main_df = self.main_df.query("coverage >= @self.threshold")

    def priority_classification(self):
        """
        Classifies contigs based on their coverage.
        """
        self.priority_df = self.main_df.sort_values(by=["coverage"], ascending=[True])


    def read_main(self) -> pd.DataFrame:
        """
        Executes the functions needed to generate the main data frame that contains all the BLAST results from the input TSV files and the filtered contigs data frame.
        """
        self.read_contigs()
        self.generate_main_df()
        self.merge_main_df()
        self.add_coverage()
        self.coverage_threshold()
        self.priority_classification()
        return self.priority_df


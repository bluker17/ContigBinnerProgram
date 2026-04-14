#!/bin/usr/env python3
# -*- coding: utf-8 -*-

import pandas as pd

class Prioritizer:
    """
    A class that filters a data frame by prioritizing contigs based on BLAST results.
    """
    def __init__(self, main_df: pd.DataFrame, priority_file: str):
        self.main_df = main_df
        self.priority_df = None
        self.priority_file = priority_file
        self.priority_map = {}

    def load_priority_map(self):
        """
        Loads the priority map from the input TSV file. 

        Parameters
        ----------
        priority_file : str
            Path to the input TSV file containing the priority map.
        """
        prioritization_df = pd.read_csv(self.priority_file, sep="\t")
        self.priority_map = dict(zip(prioritization_df["bin"], prioritization_df["priority"]))

    def prioritize_bin(self):
        """
        Filters the main data frame by prioritizing contigs based upon their bin. Priority is as follows: Mitochondrion > Apicomplexa > Sexual Chromosome > Diploid Chromosome
        """
        self.priority_df = self.main_df.copy()
        self.priority_df["priority"] = self.priority_df["bin"].map(self.priority_map)
        self.priority_df["priority"] = self.priority_df["priority"].fillna("Unclassified")


        self.priority_df = self.priority_df.sort_values(by=["priority"], ascending=[True]).drop_duplicates(subset=["qseqid"], keep="first")

    def filter_by_bitscore(self):
        """
        Filters the priority data frame by removing the same contig ids within the same bin based upon the highest bitscore.
        """
        self.priority_df = self.priority_df.sort_values(by=["bitscore"], ascending=[False]).drop_duplicates(subset=["qseqid"], keep="first")
    
    def priority_main(self):
        """
        Runs the prioritization pipeline by first generating the main data frame and then filtering it based on priority.
        """
        self.load_priority_map()
        self.prioritize_bin()
        self.filter_by_bitscore()
        return self.priority_df
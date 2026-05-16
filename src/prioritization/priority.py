#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import warnings

class Prioritizer:
    """
    A class that filters a data frame by prioritizing contigs based on BLAST results.
    """
    def __init__(self, main_df: pd.DataFrame, contigs_df: pd.DataFrame, raw_main_df: pd.DataFrame, priority_file: str, verbose: bool = False):
        self.main_df = main_df
        self.contigs_df = contigs_df
        self.raw_main_df = raw_main_df

        self.priority_df = None
        self.priority_file = priority_file
        self.priority_map = {}

        self.verbose = verbose

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
        self.priority_df["priority"] = self.priority_df["priority"].fillna(999)


        self.priority_df = self.priority_df.sort_values(by=["priority"], ascending=[True])

    def filter_by_bitscore(self):
        """
        Filters the priority data frame by removing the same contig ids within the same bin based upon the highest bitscore.
        """
        # self.priority_df = self.priority_df.sort_values(by=["bitscore"], ascending=[False]).drop_duplicates(subset=["qseqid"], keep="first")
        self.priority_df = (self.priority_df.sort_values(by=["bitscore"], ascending=[False]).drop_duplicates(subset=["qseqid", "bin"], keep="first"))

    def apply_priority_filter(self):
        """
        Applies the final priority filtering across bins.
        """
        self.priority_df = (self.priority_df.sort_values(by=["priority"], ascending=[True]).drop_duplicates(subset=["qseqid"], keep="first"))

    def assign_remaining_contigs(self):
        """
        Assigns remaining contigs as Diploid Chromosome or Unclassified.

        Diploid Chromosome:
            Contigs that had BLAST hits but did not pass prioritization filters.

        Unclassified:
            Contigs that had no BLAST hits in any database.
        """

        # Contigs already confidently classified
        classified_contigs = set(self.priority_df["qseqid"])

        # All contigs that passed size filtering
        all_contigs = set(self.contigs_df["contig_name"])

        # Contigs with any BLAST hit before coverage filtering
        raw_hit_contigs = set(self.raw_main_df["qseqid"].dropna())

        # Remaining contigs after classification
        remaining_contigs = all_contigs - classified_contigs

        diploid_contigs = remaining_contigs.intersection(raw_hit_contigs)

        unclassified_contigs = remaining_contigs - raw_hit_contigs

        diploid_df = self.contigs_df[
            self.contigs_df["contig_name"].isin(diploid_contigs)
        ].copy()

        diploid_df["bin"] = "Diploid Chromosome"

        unclassified_df = self.contigs_df[
            self.contigs_df["contig_name"].isin(unclassified_contigs)
        ].copy()

        unclassified_df["bin"] = "Unclassified"

        # Standardize columns
        for dataframe in [diploid_df, unclassified_df]:

            dataframe["qseqid"] = dataframe["contig_name"]
            dataframe["bitscore"] = pd.NA
            dataframe["sseqid"] = pd.NA
            dataframe["pident"] = pd.NA
            dataframe["evalue"] = pd.NA
            dataframe["coverage"] = pd.NA
            dataframe["priority"] = pd.NA

        frames_to_concat = [self.priority_df, diploid_df, unclassified_df]

        self.priority_df = pd.concat(
            [df for df in frames_to_concat if df is not None and not df.isna().all().all()],
            ignore_index=True
        )

    def priority_main(self):
        """
        Runs the prioritization pipeline by first generating the main data frame and then filtering it based on priority.
        """
        if not self.verbose:
            warnings.filterwarnings(
                "ignore",
                category=FutureWarning,
                message=r".*DataFrame concatenation with empty or all-NA entries.*"
            )

        self.load_priority_map()
        self.prioritize_bin()
        self.filter_by_bitscore()
        self.apply_priority_filter()
        self.assign_remaining_contigs()
        return self.priority_df
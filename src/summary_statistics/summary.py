#!/bin/usr/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

class SummaryStatistics:
    """
    A class that generates summary statistics and visualizations for the contig classification results.
    """
    def __init__(self, priority_df: pd.DataFrame, summary_stats_file: str, contigs_bin_file: str, total_bps_bin_file: str, data_frame_file: str):
        self.priority_df = priority_df
        self.summary_stats_file = summary_stats_file
        self.contigs_bin_file = contigs_bin_file
        self.total_bps_bin_file = total_bps_bin_file
        self.data_frame_file = data_frame_file

        self.contig_stats = None
        self.bp_stats = None

        self.summary_stats = None

    def generate_output_file(self):
        """
        Genertates the outpute TSV file conatining the priority data frame as is.
        """
        self.priority_df.to_csv(self.data_frame_file, sep='\t', index=False)
    
    def generate_summary_stats(self):
        """
        Generates summary statistics for the priority data frame, including:
            Number and total base pairs in each bin.
            Number of contigs in each bin.
            Maximum bitscore for each bin
            Mean bitscore for each bin
            Maximum contig coverage for each bin
            Mean contig coverage for each bin
        """
        self.contig_stats = self.priority_df['bin'].value_counts()
        self.bp_stats = self.priority_df.groupby('bin')['size_bp'].sum()
        
        self.summary_stats = self.priority_df.groupby('bin').agg(
            total_bp=pd.NamedAgg(column='size_bp', aggfunc='sum'),
            contig_count=pd.NamedAgg(column='qseqid', aggfunc='count'),
            max_bitscore=pd.NamedAgg(column='bitscore', aggfunc='max'),
            median_bitscore=pd.NamedAgg(column='bitscore', aggfunc='median'),
            mean_bitscore=pd.NamedAgg(column='bitscore', aggfunc='mean'),
            max_coverage=pd.NamedAgg(column='coverage', aggfunc='max'),
            median_coverage=pd.NamedAgg(column='coverage', aggfunc='median'),
            mean_coverage=pd.NamedAgg(column='coverage', aggfunc='mean')
        ).reset_index()

    def generate_summary_stats_file(self):
        """
        Generates a TSV file containing the summary statistics for each bin.
        """
        self.summary_stats.to_csv(self.summary_stats_file, sep='\t', index=False)

    def generate_contig_png(self):
        """
        Generates a bar chart showing the count of contigs per bin.
        """

        plt.figure(figsize=(10, 6))
        self.contig_stats.plot(kind='bar')
        plt.xlabel('Bin')
        plt.xticks(rotation=45)
        plt.ylabel('Contig Counts')
        plt.title('Contig Classification')
        plt.tight_layout()
        plt.savefig(self.contigs_bin_file)
    
    def generate_bps_png(self):
        """
        Generates a bar chart showing the total base pairs per bin.
        """
        plt.figure(figsize=(10, 6))
        self.bp_stats.plot(kind='bar')
        plt.xlabel('Bin')
        plt.xticks(rotation=45)
        plt.ylabel('Total Base Pairs')
        plt.title('Total Base Pairs per Bin')
        plt.tight_layout()
        plt.savefig(self.total_bps_bin_file)

    def summary_main(self):
        """
        Executes the functions needed to generate the output and summary files.
        """
        self.generate_output_file()
        self.generate_summary_stats()
        self.generate_summary_stats_file()
        self.generate_contig_png()
        self.generate_bps_png()
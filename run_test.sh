#!/bin/bash

thresholds=(0.25 0.50 0.75 0.90)

for t in "${thresholds[@]}" ; do
    echo -e "\nRunning threshold: $t"
    python3 main.py \
        -i example_data/blast_files/ \
        -c example_data/Binsularis_contig_sizes.txt \
        -p example_data/prioritization.tsv \
        --summary_stats_file example_runs/${t}/${t}_summary_stats.tsv \
        --contigs_barplot example_runs/${t}/${t}_contigs_barplot.png \
        --bps_barplot example_runs/${t}/${t}_bps_barplot.png \
        --data_frame_file example_runs/${t}/${t}_data_frame.tsv \
        -t $t
done

echo -e "\nAll runs completed."
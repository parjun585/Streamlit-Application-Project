import streamlit as st
import numpy as np
from PIL import Image
import time
import pandas as pd
import altair as alt

def reverse(seq):
    """Reverses a DNA sequence."""
    return seq[::-1]

def complement(seq):
    """Complements a DNA sequence."""
    complement_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement_map.get(base, base) for base in seq)

def reverse_complement(seq):
    """Returns the reverse complement of a DNA sequence."""
    return complement(reverse(seq))

def length(seq):
    """Returns the length of the sequence."""
    return len(seq)

def dna_stats(sequence):
    """Calculates DNA statistics and returns them."""
    # Initialize counters
    base_counts = {'A': 0, 'T': 0, 'C': 0, 'G': 0}

    # Calculate base frequencies
    for base in sequence:
        if base in base_counts:
            base_counts[base] += 1

    # Calculate individual nucleotide content percentages
    total_bases = len(sequence)
    a_content = (base_counts['A'] / total_bases * 100) if total_bases > 0 else 0
    t_content = (base_counts['T'] / total_bases * 100) if total_bases > 0 else 0
    g_content = (base_counts['G'] / total_bases * 100) if total_bases > 0 else 0
    c_content = (base_counts['C'] / total_bases * 100) if total_bases > 0 else 0

    # Calculate AT and GC content percentages
    at_content_percent = (base_counts['A'] + base_counts['T']) / total_bases * 100 if total_bases > 0 else 0
    gc_content_percent = (base_counts['G'] + base_counts['C']) / total_bases * 100 if total_bases > 0 else 0

    # Calculate dinucleotide counts
    at_count = base_counts['A'] + base_counts['T']
    gc_count = base_counts['G'] + base_counts['C']

    # Return the calculated statistics
    return base_counts, a_content, t_content, g_content, c_content, at_count, gc_count, at_content_percent, gc_content_percent


    # total_bases = len(sequence)
    # a_content = (base_counts['A']) / total_bases * 100
    # t_content = (base_counts['T']) / total_bases * 100
    # g_content = (base_counts['G']) / total_bases * 100
    # c_content = (base_counts['C']) / total_bases * 100
    # at_content = (base_counts['A'] + base_counts['T']) / total_bases * 100
    # gc_content = (base_counts['G'] + base_counts['C']) / total_bases * 100

    # # Calculate dinucleotide frequencies
    # at_count = base_counts['A'] + base_counts['T']
    # gc_count = base_counts['G'] + base_counts['C']
    # at_content_percent = at_content
    # gc_content_percent = gc_content

    # # Return the calculated statistics
    # return base_counts, at_content, gc_content, at_count, gc_count, at_content_percent, gc_content_percent

# Page Title
image = Image.open('image.jpg')
st.image(image, use_column_width=True)

st.write("""
# DNA Sequence Analyzer

***This web application empowers users to efficiently manipulate and analyze DNA sequences. Key features include:***
- Reverse complement: Generate the reverse, complement and reverse complement of a DNA sequence, essential for identifying potential open reading frames (ORFs) on the reverse strand.
- Base composition: Calculate the frequency of each nucleotide (A, T, C, G) within a sequence.
- Sequence analysis: Determine the AT and GC content for comprehensive sequence characterization.
""")

dna_input = st.text_input("Enter a DNA sequence:")
dna_sequence=dna_input.upper()
progress_text = "Operation in progress. Please wait."
my_bar = st.progress(0, text=progress_text)

for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
time.sleep(1)
my_bar.empty()

st.button("Run")

if dna_input:
    dna_sequence = dna_input.upper()
    
    # Check for invalid characters
    valid_bases = {'A', 'T', 'C', 'G'}
    invalid_characters = set(dna_sequence) - valid_bases

    if invalid_characters:
        st.warning(f"The sequence contains non-DNA characters ({', '.join(invalid_characters)}), which will be omitted.Please check your sequence carefully.")
    else:
        # Filter out non-DNA characters
        dna_sequence = ''.join(base for base in dna_sequence if base in valid_bases)

        st.subheader("Manipulation Results")
        st.write("Original:", dna_input.upper())
        # st.write("Filtered:", dna_sequence)
        st.write("Reverse:", reverse(dna_sequence))
        st.write("Complement:", complement(dna_sequence))
        st.write("Reverse complement:", reverse_complement(dna_sequence))
        st.write("Length of Sequence:", length(dna_sequence))

        # DNA stats
        base_counts, a_content, t_content, g_content, c_content, at_count, gc_count, at_content_percent, gc_content_percent = dna_stats(dna_sequence)
        st.subheader("DNA Sequence Analysis")
        # Creating a table
        table_data = {
            "Base": ["A", "T", "C", "G", "A/T", "G/C"],
            "Count": [base_counts["A"], base_counts["T"], base_counts["C"], base_counts["G"], at_count, gc_count],
            "Content": [
                f"{a_content:.2f}%", f"{t_content:.2f}%", f"{c_content:.2f}%", f"{g_content:.2f}%", f"{at_content_percent:.2f}%", f"{gc_content_percent:.2f}%"
            ]
        }
        st.table(pd.DataFrame(table_data))

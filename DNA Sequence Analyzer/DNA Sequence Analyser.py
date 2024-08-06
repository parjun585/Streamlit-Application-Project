import streamlit as st
import numpy as np
from PIL import Image
import time

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
    """Returns the length of the sequence """
    return len(seq)

def dna_stats(sequence):
    """Calculates DNA statistics and returns them."""
    # Initialize counters
    base_counts = {'A': 0, 'T': 0, 'C': 0, 'G': 0}

    # Calculate base frequencies
    for base in sequence:
        if base in base_counts:
            base_counts[base] += 1

    # Calculate AT and GC content
    total_bases = len(sequence)
    at_content = (base_counts['A'] + base_counts['T']) / total_bases * 100
    gc_content = (base_counts['G'] + base_counts['C']) / total_bases * 100

    # Return the calculated statistics
    return base_counts, at_content, gc_content

######################
# Page Title
######################
image = Image.open('image.jpg')
st.image(image, use_column_width=True)

st.write("""
# Reverse Complement and DNA Stats App

***Reverse Complement converts a DNA sequence into its reverse, complement, or reverse-complement counterpart. You may want to work with the reverse-complement of a sequence if it contains an ORF on the reverse strand.***
""")

dna_input = st.text_input("Enter a DNA sequence:")

progress_text = "Operation in progress. Please wait."
my_bar = st.progress(0, text=progress_text)

for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
time.sleep(1)
my_bar.empty()

st.button("Rerun")

def main():
    """Main function for Streamlit app."""
    if dna_input:
        dna_sequence = dna_input.upper()
        
        # Check for invalid characters
        valid_bases = {'A', 'T', 'C', 'G'}
        invalid_characters = set(dna_sequence) - valid_bases

        if invalid_characters:
            st.warning(f"The sequence contains non-DNA characters ({', '.join(invalid_characters)}), which will be omitted. Please check your DNA sequence.")
            return  # Stop further execution

        # Filter out non-DNA characters
        dna_sequence = ''.join(base for base in dna_sequence if base in valid_bases)

        st.subheader("Manipulation Results")
        st.write("Original:", dna_input.upper())
        st.write("Filtered:", dna_sequence)
        st.write("Reverse:", reverse(dna_sequence))
        st.write("Complement:", complement(dna_sequence))
        st.write("Reverse complement:", reverse_complement(dna_sequence))
        st.write("Length of Sequence:", length(dna_sequence))

        # DNA stats
        base_counts, at_content, gc_content = dna_stats(dna_sequence)

        st.subheader("DNA Sequence Analysis")
        # Creating a table
        table_data = {
            "Base": ["A", "T", "C", "G"],
            "Count": [base_counts["A"], base_counts["T"], base_counts["C"], base_counts["G"]],
            "Content": [
                f"{at_content if base in ['A', 'T'] else gc_content:.2f}%" for base in ["A", "T", "C", "G"]
            ]
        }
        st.table(table_data)

if __name__ == "__main__":
    main()

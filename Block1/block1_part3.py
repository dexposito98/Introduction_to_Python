# 1)
from collections import Counter # Use Counter module

def calculate_proportion(fasta_filename, subsequences_filename, number_of_repetitions, output_filename):
    # Create a Counter to store the count of each subsequence
    sub_sequence_count = Counter()
    # Open the subsequences file and count each sub-sequence
    with open(subsequences_filename, "r") as f:
        for line in f:
            line = line.strip() # Remove whitespaces
            sub_sequence_count[line] = 0 # Each sub-sequence is being added to the Counter(as keys) and its count is being set to 0.
    # Open the FASTA file and check for the presence of each subsequence in each protein
    proteins_with_subsequence = set() # To store proteins with number_of_repetitions of the subsequence
    total_proteins = 0
    with open(fasta_filename, "r") as f:
        seq = ""
        for line in f:
            if line.startswith(">"): 
                total_proteins += 1
                # To count when changing the protein
                for sub_sequence in sub_sequence_count: 
                    count = seq.count(sub_sequence) # Check how many times the subsequence appears
                    if count >= number_of_repetitions:
                        sub_sequence_count[sub_sequence] += 1
                        proteins_with_subsequence.add(line) # Added to the previous set
                seq = ""
            else:
                seq += line.strip()
    # Seq has the whole sequence of the protein, so now it will check how many times the subsequence appears there
    if seq: 
        for sub_sequence in sub_sequence_count:
            count = seq.count(sub_sequence)
            if count >= number_of_repetitions:
                sub_sequence_count[sub_sequence] += 1
                proteins_with_subsequence.add(line)

    # Save the results to the output file
    with open(output_filename, "w") as f:
        total_proteins_subsequence = len(proteins_with_subsequence)
        total_subsequences = len(sub_sequence_count)
        f.write(f"# Number of proteins: {total_proteins:>{len(str(total_proteins))}}\n") # Total number of proteins from the fasta file (> to right align)
        f.write(f"# Number of subsequences: {total_subsequences:>{len(str(total_subsequences))}}\n") # Total number of subsequences
        f.write("# Subsequence proportions:\n")
        for sub_sequence, count in sorted(sub_sequence_count.items(), key=lambda x: x[1], reverse=True):
            if total_proteins_subsequence > 0: # To avoid dividing by 0
                prop = count / total_proteins_subsequence
                f.write(sub_sequence.ljust(20) + str(count).ljust(20) +  "{:.4f}".format(prop) + '\n')

# An example to try: calculate_proportion("example.fa","sequence_fragments.txt",5, "result.txt")
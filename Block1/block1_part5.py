#Let's first define again the FASTA_iterator function
def FASTA_iterator(fasta_filename): 
    with open(fasta_filename, 'r') as fasta_file: 
        identifier = "" 
        sequence = "" 

        for line in fasta_file: 
            line = line.strip() 
            if line.startswith(">"): 
                if identifier and sequence: 
                    yield (identifier, sequence) 
                identifier = line[1:] 
                sequence = "" 
            else: 
                sequence += line 

        if identifier and sequence: 
            yield identifier, sequence

################################################
# 1) Repeat the same exercises proposed in session 2 but using the FASTA_Iterator function created in session 4 to read the FASTA ﬁles:
# a)
def get_proteins_ratio_by_residue_threshold(filename, residue, relative_threshold=0.03, absolute_threshold=10):
    true_prot = 0
    all_prot = 0
    relative_freq = 0
    absolute_freq = 0
    residue_num = 0
    total_residues = 0
    
    fasta_generator = FASTA_iterator(filename)
    for identifier, sequence in fasta_generator:
        residue_num = sequence.count(residue)
        total_residues = len(sequence)
        relative_freq = residue_num / total_residues
        absolute_freq = residue_num
        if relative_freq >= relative_threshold and absolute_freq >= absolute_threshold:
            true_prot += 1
        all_prot += 1

    print(true_prot/all_prot)

# b)
def print_sequence_summary(filename, output_filename, first_n=10, last_n=10):
    def FASTA_generator(filename):
        with open(filename, "r") as f:
            prot_id = ""
            seq = ""
            for line in f:
                if line.startswith(">"):
                    if prot_id:
                        yield prot_id, seq
                    prot_id = line.strip()[1:]
                    seq = ""
                else:
                    seq += line.strip()
            if prot_id:
                yield prot_id, seq
    
    with open(output_filename, "w") as f_out:
        for prot_id, seq in FASTA_generator(filename):
            frequency = {}
            for aa in seq:
                if aa not in frequency:
                    frequency[aa] = seq.count(aa)
            first_N = seq[:first_n]
            last_N = seq[-last_n:]
            out_str = f'{prot_id}\t{first_N}\t{last_N}\t'
            for aa in frequency:
                out_str += f'{aa}:{frequency[aa]},'
            f_out.write(out_str.rstrip(',') + '\n')

############################################################
# 2) A function that, given a multiline FASTA ﬁle, returns the length of the sequence with the maximum length: 
# get_max_sequence_length_from_FASTA_file(fasta_filename)
def get_max_sequence_length_from_FASTA_file(fasta_filename):
    max_length = 0
    for identifier, sequence in FASTA_iterator(fasta_filename):
        max_length = max(max_length, len(sequence))
    return max_length

############################################################
# 3) A function that, given a multiline FASTA ﬁle, returns the length of the sequencewith the minimum length: 
# get_min_sequence_length_from_FASTA_file ( fasta_filename )
def get_min_sequence_length_from_FASTA_file(fasta_filename):
    min_length = float('inf')
    for identifier, sequence in FASTA_iterator(fasta_filename):
        min_length = min(min_length, len(sequence))
    return min_length

############################################################
# 4) A function that, given a FASTA ﬁle, returns a list of tuples (identiﬁer, sequence) corresponding to the sequence(s) with maximum length. The list must be sorted by the identiﬁer (case insensitive sorted).¶
# get_longest_sequences_from_FASTA_file( fasta_filename )
def get_longest_sequences_from_FASTA_file(fasta_filename):
    max_length = 0
    longest_sequences = []
    for identifier, sequence in FASTA_iterator(fasta_filename):
        length = len(sequence)
        if length > max_length:
            max_length = length
            longest_sequences = [(identifier, sequence)]
        elif length == max_length:
            longest_sequences.append((identifier, sequence))
    return sorted(longest_sequences, key=lambda x: x[0].lower())

############################################################
# 5) A function that, given a FASTA ﬁle, returns a list of tuples (identiﬁer, sequence) corresponding to the sequence(s) with minimum length. The list must be sorted by the identiﬁer (case insensitive sorted).¶
# get_shortest_sequences_from_FASTA_file( fasta_filename )
def get_shortest_sequences_from_FASTA_file(fasta_filename):
    min_length = float('inf')
    shortest_sequences = []
    for identifier, sequence in FASTA_iterator(fasta_filename):
        length = len(sequence)
        if length < min_length:
            min_length = length
            shortest_sequences = [(identifier, sequence)]
        elif length == min_length:
            shortest_sequences.append((identifier, sequence))
    return sorted(shortest_sequences, key=lambda x: x[0].lower())

############################################################
# 6) A function that, given a protein FASTA ﬁle, returns a dictionary with the molecular weights of all the proteins in the ﬁle. The dictionary keys must be the protein identiﬁers and the associated values must be a ﬂoat corresponding to the molecular weight.¶
# get_molecular_weights( fasta_filename )
from molecular_weights import aminoacid_mw # Import the dictionary

def get_molecular_weights(fasta_filename):
    weights = {}

    for identifier, sequence in FASTA_iterator(fasta_filename):
        weight = 0.0
        for amino_acid in sequence:
            weight += aminoacid_mw.get(amino_acid, 0)
        weights[identifier] = weight
    return weights

############################################################
# 7) A function that, given a protein FASTA ﬁle, returns a tuple with (identiﬁer, sequence) of the protein with the lowest molecular weight. If there are two or moreproteins having the minimum molecular weight, just return the ﬁrst one.¶
# get_sequence_with_min_molecular_weight( fasta_filename )

def get_sequence_with_min_molecular_weight(fasta_filename):
    weights = get_molecular_weights(fasta_filename) # Reusing the function from ex 6)
    min_weight = float('inf')
    min_identifier = None
    min_sequence = None
    for identifier, sequence in FASTA_iterator(fasta_filename):
        if weights[identifier] < min_weight:
            min_weight = weights[identifier]
            min_identifier = identifier
            min_sequence = sequence
    return min_identifier, min_sequence

###########################################################
# 8) A function that, given a protein FASTA ﬁle, returns the mean of the molecular weights of all the proteins¶
# get_mean_molecular_weight( fasta_filename )
def get_mean_molecular_weight(fasta_filename):
    weights = get_molecular_weights(fasta_filename)
    total_weight = 0
    count = 0
    for identifier in weights:
        total_weight += weights[identifier]
        count += 1
    mean_weight = total_weight / count
    return mean_weight
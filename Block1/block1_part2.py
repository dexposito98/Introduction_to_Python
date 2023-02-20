# 1) 
def get_proteins_ratio_by_residue_threshold(filename,
    residue, relative_threshold=0.03, absolute_threshold=10):
    true_prot = 0
    all_prot = 0
    relative_freq = 0
    absolute_freq = 0
    residue_num = 0
    total_residues = 0

    with open(filename, "r") as f:
        for line in f:
            if line.startswith(">"): # New protein
                if relative_freq >= relative_threshold and absolute_freq >= absolute_threshold:
                    true_prot += 1
                relative_freq = 0
                absolute_freq = 0
                residue_num = 0
                total_residues = 0
                all_prot += 1
            else: # Aminoacid line
                residue_num += line.count(residue)
                total_residues += len(line)
                relative_freq = residue_num / total_residues
                absolute_freq = residue_num
    if relative_freq >= relative_threshold and absolute_freq >= absolute_threshold: # For the last protein
        true_prot += 1
    print(true_prot/all_prot)


# 2)
def print_sequence_summary(filename, output_filename, first_n=10, last_n=10):
    # Open input file
    with open(filename, "r") as f_in:
        # Open output file
        with open(output_filename, "w") as f_out:
            prot_id = ""
            seq = ""
            for line in f_in:
                if line.startswith(">"):
                    # If we already have stored information for a protein, write it to the output file
                    if prot_id:
                        frequency = {}
                        for aa in seq:
                            if aa not in frequency:
                                frequency[aa] = seq.count(aa)
                        first_N = seq[:first_n]
                        last_N = seq[-last_n:]
                        out_str = f'{prot_id}\t{first_N}\t{last_N}\t'
                        for aa in frequency:
                            out_str += f'{aa}:{frequency[aa]},'
                        f_out.write(out_str.rstrip(',') + '\n') # Remove last comma
                    # Update the current protein's identifier
                    prot_id = line.strip()[1:]
                    seq = ""
                else:
                    # Otherwise, add the line to the current protein's sequence
                    seq += line.strip()
            # Write the last protein's information to the output file
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
  

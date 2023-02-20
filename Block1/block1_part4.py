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

# To test it:
#fasta_file = 'uniprot_sprot_sample.fasta' 

#fasta_generator = FASTA_iterator(fasta_file) 

# for identifier, sequence in fasta_generator: 
#   print("Identifier:", identifier) 
#    print("Sequence:", sequence) 
#    print("\n")

####################################################################

def compare_fasta_file_identifiers(fasta_filenames_list): 
    union = set() 
    intersection = set() 
    frequency = dict() 
    specific = dict() 

    for fasta_filename in fasta_filenames_list: 
        specific[fasta_filename] = set() 
        fasta_generator = FASTA_iterator(fasta_filename) 
        file_identifiers = set() 

        for identifier, _ in fasta_generator:  #_ to discard the sequence and take only the identifier
            file_identifiers.add(identifier.upper()) # Upper to convert to uppercase
            union.add(identifier.upper()) 

        if not intersection: 
            intersection = file_identifiers 
        else: 
            intersection &= file_identifiers 

        for identifier in file_identifiers: 
            if identifier.upper() in frequency: 
                frequency[identifier.upper()] += 1 
            else: 
                frequency[identifier.upper()] = 1 

    for fasta_filename in fasta_filenames_list:
        fasta_generator = FASTA_iterator(fasta_filename)
        file_identifiers = set() 

        for identifier, _ in fasta_generator: 
            identifier = identifier.upper()
            file_identifiers.add(identifier) 

        for identifier in file_identifiers:
            if frequency[identifier] == 1:
                specific[fasta_filename].add(identifier) 

    return { 
        "intersection": intersection, 
        "union": union, 
        "frequency": frequency, 
        "specific": specific 
    } 

#To test it
#fasta_filenames_list= ["input.fasta","input2.fasta","input3.fasta"]
#result = compare_fasta_file_identifiers(fasta_filenames_list) 

#print(result)

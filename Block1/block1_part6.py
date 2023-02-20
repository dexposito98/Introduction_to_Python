## EX6 ##

import math
import sys

# calculate minimum distance between two lists of coordinates
def calculate_min_distance(coords1, coords2):
    dists = (math.sqrt(sum((c1[i]-c2[i])**2 for i in range(3))) for c1 in coords1 for c2 in coords2)
    # return minimum distance found
    return min(dists)

# calculate mean minimum distance for each chain in a given pdb file
def calculate_pdb_chain_mean_minimum_distances(pdb_file_path):
    # open pdb file or use standard input if no file provided
    if pdb_file_path:
        pdb = open(pdb_file_path, "r")
    else:
        pdb = sys.stdin

    # create empty set to hold chain information
    chains = set()

    # loop through each line in the pdb file and extract coordinates for each chain and residue
    for line in pdb:
        if line.startswith("ATOM"):
            chain = line[21]
            residue = line[22:26]
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])

            # add chain to set
            chains.add(chain)

    # reset file pointer to beginning of file
    pdb.seek(0)

    # create empty dictionary to hold mean minimum distances for each chain
    mean_min = {}

    # loop through each chain in the set and extract coordinates for each residue
    for chain in chains:
        residues = {}

        for line in pdb:
            if line.startswith("ATOM") and line[21] == chain:
                residue = line[22:26]
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])

                # add residue coordinates to list for the residue it belongs to
                if residue not in residues:
                    residues[residue] = []

                residues[residue].append([x, y, z])

        distances = []
        # loop through each pair of residues in the chain and calculate minimum distance between them
        for residue1, coords1 in residues.items():
            for residue2, coords2 in residues.items():
                if residue1 < residue2:
                    distances.append(calculate_min_distance(coords1, coords2))

        # calculate mean of all minimum distances for the chain
        mean_distance = sum(distances) / len(distances)

        # add mean minimum distance to the dictionary for the chain
        mean_min[chain] = f"{mean_distance:.4f}"

        # reset file pointer to beginning of file
        pdb.seek(0)

    return mean_min


if __name__ == "__main__":
    # call calculate_pdb_chain_mean_minimum_distances function with filename provided as command line argument
    if len(sys.argv) > 1:
        results = calculate_pdb_chain_mean_minimum_distances(sys.argv[1])
    # call function with no arguments if no filename provided
    else:
        results = calculate_pdb_chain_mean_minimum_distances(None)

    # sort dictionary by chain and print mean minimum distances for each chain in the dictionary
    for chain, value in sorted(results.items()):
        print(f"{chain} : {value}")



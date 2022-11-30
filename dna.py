import csv
import sys

def main():

    # Check for proper command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # Initialize lists
    list_sequences = []
    people = []

    # Read database file into a variable
    with open(sys.argv[1]) as f:
        database = csv.DictReader(f)

        # Get first row of database to create list of DNA sequences
        first_row = next(database)

        # Iterate through keys and populate list of DNA sequences if key value not equal to name
        for key in first_row.keys():
            if key != "name":
                list_sequences.append(key)

        # Return to top of database
        f.seek(0)

        # Iterate through rows of database
        for row in database:

            # Iterate through number of DNA sequences
            for item in list_sequences:

                # Attempt to convert count of DNA sequence to integer
                try:
                    row[item] = int(row[item])

                # If not valid, continue to next key
                except ValueError:
                    continue

            # Append each row of database to people list
            people.append(row)

        # Calculate number of DNA sequences to compare
        number_sequences = len(list_sequences)

    # Read DNA sequence file into a variable
    with open(sys.argv[2]) as f:
        dna_file = csv.reader(f)

        # Get DNA sequence as a string
        dna_sequence = next(dna_file)[0]

    # Iterate through DNA sequences
    for i in range(number_sequences):

        # Find longest match of each STR in DNA sequence
        count = longest_match(dna_sequence, list_sequences[i])

        # Update list of DNA sequences to be a list of dictionaries with sequence length counts
        list_sequences[i] = {list_sequences[i]:count}

    # Initialize dictionary of DNA sequence counts
    dict_sequences = {}

    # Convert list of DNA sequences to be a dictionary of DNA sequences
    for dictionary in list_sequences:
        dict_sequences.update(dictionary)

    # Set default profile to no match
    profile = "No match"

    # Check database for matching profiles
    for person in people:

        # Splice dictionary to get DNA sequence counts
        current_sequence = dict(list(person.items())[1:])

        # Compare DNA sequence counts and get name of person if there is a match
        if current_sequence == dict_sequences:
            profile = person["name"]

    print(profile)


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()

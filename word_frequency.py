def word_frequency(file_path):
    """Calculates the frequency of each word in a given file."""
    frequency = {}
    try:
        with open(file_path, 'r') as file:
            text = file.read()
            words = text.split()
            for word in words:
                word = word.lower()  # Convert to lowercase to count "Word" and "word" as the same
                if word in frequency:
                    frequency[word] += 1
                else:
                    frequency[word] = 1
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    return frequency

# Example usage:
# print(word_frequency('example.txt'))
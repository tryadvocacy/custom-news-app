from collections import Counter
import re
from typing import Dict

def analyze_word_frequency(file_path: str) -> Dict[str, int]:
    """
    Analyze word frequency from a given file.
    
    Args:
        file_path (str): Path to the file to analyze
        
    Returns:
        Dict[str, int]: Dictionary with words as keys and their frequencies as values,
                       sorted by frequency in descending order
                       
    Raises:
        FileNotFoundError: If the specified file does not exist
        IOError: If there's an error reading the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().lower()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except IOError as e:
        raise IOError(f"Error reading file: {e}")
    
    # Remove punctuation and split into words
    words = re.findall(r'\b[a-z]+\b', content)
    
    # Count word frequencies
    word_counts = Counter(words)
    
    # Return sorted by frequency (descending)
    return dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True))


def analyze_word_frequency_with_limit(file_path: str, limit: int = 10) -> Dict[str, int]:
    """
    Analyze word frequency from a file and return top N most frequent words.
    
    Args:
        file_path (str): Path to the file to analyze
        limit (int): Number of top words to return (default: 10)
        
    Returns:
        Dict[str, int]: Dictionary with top N words and their frequencies
    """
    all_frequencies = analyze_word_frequency(file_path)
    return dict(list(all_frequencies.items())[:limit])


if __name__ == "__main__":
    # Example usage
    example_file = "sample.txt"
    
    try:
        frequencies = analyze_word_frequency(example_file)
        print("Word Frequencies:")
        for word, count in frequencies.items():
            print(f"{word}: {count}")
        
        print("\n--- Top 10 Words ---")
        top_frequencies = analyze_word_frequency_with_limit(example_file, limit=10)
        for word, count in top_frequencies.items():
            print(f"{word}: {count}")
    except (FileNotFoundError, IOError) as e:
        print(f"Error: {e}")
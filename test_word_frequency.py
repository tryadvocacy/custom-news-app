from word_frequency import word_frequency
import os
import pytest

def test_word_frequency():
    # Create a temporary file to test
    with open('test_file.txt', 'w') as f:
        f.write('hello world hello')

    # Get the frequency
    frequency = word_frequency('test_file.txt')

    # check if the frequency is correct
    assert frequency['hello'] == 2
    assert frequency['world'] == 1

    # delete the temporary file
    os.remove('test_file.txt')

def test_word_frequency_file_not_found():
    frequency = word_frequency('non_existent_file.txt')
    assert frequency == {}

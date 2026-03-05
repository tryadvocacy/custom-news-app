
import os
import json
from unittest.mock import patch
from word_cloud_generator import main

def test_main_generates_output():
    # Create a dummy word frequencies file
    dummy_data = {"hello": 5, "world": 10}
    input_filename = "test_frequencies.json"
    with open(input_filename, "w") as f:
        json.dump(dummy_data, f)

    output_filename = "test_wordcloud.png"

    # Patch sys.argv to simulate command-line arguments
    with patch("sys.argv", ["word_cloud_generator.py", input_filename, "--output", output_filename]):
        main()

    # Check if the output file was created
    assert os.path.exists(output_filename)

    # Clean up created files
    os.remove(input_filename)
    os.remove(output_filename)

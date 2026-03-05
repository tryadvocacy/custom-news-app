import argparse
import json
from wordcloud import WordCloud

def main():
    parser = argparse.ArgumentParser(description="Generate a word cloud from a JSON file of word frequencies.")
    parser.add_argument("input_filename", help="The name of the input JSON file.")
    parser.add_argument("--output", dest="output_filename", help="The name of the output PNG file.")
    args = parser.parse_args()

    with open(args.input_filename, "r") as f:
        frequencies = json.load(f)

    wc = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(frequencies)

    if args.output_filename:
        wc.to_file(args.output_filename)
    else:
        # Display the word cloud if no output file is specified
        import matplotlib.pyplot as plt
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.show()

if __name__ == "__main__":
    main()

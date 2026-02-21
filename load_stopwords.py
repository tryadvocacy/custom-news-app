with open('stopwords.txt', 'r') as f:
    stop_words = set(word.strip() for word in f.readlines())
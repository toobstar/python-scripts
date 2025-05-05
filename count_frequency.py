import os.path
import sys, getopt

def parse_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at {file_path} does not exist.")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")
    

def replace_non_alphanumeric_with_space(text):
    alpha_numeric = ''.join(char if char.isalnum() else ' ' for char in text)
    return alpha_numeric.lower()

def main():     
    # "static/sample-html.txt"
    print(len(sys.argv))
    if len(sys.argv) > 1: 
        file_path = sys.argv[1] 
    else:
        file_path = input("Enter the path to the file: ")

    try:
        content = parse_file(file_path)
        print("checking ", file_path)
        content = replace_non_alphanumeric_with_space(content)

        word_count_map = {}
        for word in content.split(' '):
            clean = word.strip()
            if len(clean) > 1:
                word_count_map[clean] = word_count_map.get(clean, 0) + 1
        
        words_as_list = list(word_count_map.items())
        words_as_list.sort(key=lambda x: x[1], reverse=True)
        
        print("Top 20 Words:")
        for idx, word_pair in enumerate(words_as_list):
            if idx < 5:
                print(f"{word_pair[0]}: {word_pair[1]}")

    except (FileNotFoundError, IOError) as e:
        print(e)

if __name__ == "__main__":
    main()
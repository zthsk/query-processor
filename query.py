import argparse
import subprocess
from queryProcessor import QueryProcessor
from nltk.stem import PorterStemmer

def main():
    parser = argparse.ArgumentParser(description="Retrieve data based on query and directory")
    parser.add_argument("-q", "--query", nargs='+', required=True, help="List of queries")
    parser.add_argument("-d", "--directory", required=True, help="Directory path")

    args = parser.parse_args()

    stemmer = PorterStemmer()
    queries = args.query
    try:
        command = f'./tokenizer_string \"{queries}\"'

        #print(f'Tokenizing {html_docs}!!!')
        # Run the C++ command and capture its output
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    

        # Check if the execution was successful
        if result.returncode == 0:
            tokens = result.stdout.decode('utf-8').splitlines()  # Decode the binary output to text
        else:
            print("Error while running C++ script:")
            print(result.stderr.decode('utf-8'))  # Decode the binary error to text

    except Exception as e:
        print(f"An error occurred: {e}")

    directory = args.directory
    tokens = [stemmer.stem(token) for token in tokens]
    obj = QueryProcessor(tokens, directory)
    obj.runQueryProcessor()
    acm = obj.getAccumulator()
    top_10_records = dict(list(acm.items())[:10])
    if top_10_records:
        for doc, wt in top_10_records.items():
            print(f'DocID: {doc} \t FileName: {obj.getFileName(doc)} \t Weight: {wt}') 
    else:
        query = " ".join(queries)


if __name__ == "__main__":
    main()










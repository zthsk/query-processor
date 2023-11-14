import string
import sys
import os
import subprocess
from Inverter import HTMLInverter
from nltk.stem import PorterStemmer
import time
import shutil

if __name__ == "__main__":

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    files = os.listdir(input_dir)
    total_docs = len(files)

    stemmer = PorterStemmer()
    m = HTMLInverter(total_docs)

    #delete and then create the directory for our tokenized files
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # with open(os.path.join(output_dir, "map.txt"), 'w') as f:
    #             f.write("DocID,FileName\n")

    doc_id = 0
    #Loop over all files and tokenize them
    print("building global hashtable..")
    for file in files:
        if file.endswith(".html"):
            input_file = os.path.join(input_dir,file)

            try:
                command = f'./tokenizer_files {input_file}'
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

            tokens = [stemmer.stem(token) for token in tokens]
            m.processTokens(tokens, doc_id)


            with open(os.path.join(output_dir, "map.txt"), 'a') as f:
                id = str(doc_id).ljust(4)
                fname = str(file).ljust(12)
                rec = id + '|' + fname + '\n'
                f.write(rec)

            doc_id += 1   


    print("finished table..")    
    print(f"writing files to {output_dir}..") 

    m.finish(output_dir)
    
    print("finished writing output..")
    print("complete!!")
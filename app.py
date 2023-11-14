from flask import Flask, render_template, request, send_from_directory
import subprocess
import os

app = Flask(__name__)

html_directory = 'files'
def search_results(matching_documents):
    docs_data = []
    for document in matching_documents[:-1]:
        split1 = document.split('\t')
        split2 = [a.split(':') for a in split1]
        data = [a[1].strip() for a in split2]
        docs_data.append(data)
    return docs_data

@app.route('/')
def index():
    return render_template('index.html')
  
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    searched = False
    try:
        #calling query processor script and capture its output
        result = subprocess.check_output(['python3', 'query.py', '-q', query, '-d', 'invertedfiles'])
        matching_documents = result.decode('utf-8').split('\n')
        matching_documents = search_results(matching_documents)
        searched = True
    except Exception as e:
        print(f'Error: {str(e)}')
        matching_documents = []

    return render_template('index.html',query=query, matching_documents=matching_documents, searched = searched)

@app.route('/open_file/<filename>')
def open_file(filename):
    # Ensure the requested file exists in the "files" directory
    file_path = os.path.join(html_directory,filename)

    if os.path.isfile(file_path):
        return send_from_directory(html_directory, filename)
    else:
        return "File not found"
    
if __name__ == '__main__':
    app.run()

# @brief Web service which accepts a POST upload of an archive zip returns a JSON object representing a sorted list of
#    the top 10 words found within text files contained in the zipfile, and their counts.
# @returns JSON payload containing status string, and nested words list such as:
# {"status": "success", "words": [["foo", 1000], ["bar", 999], ["etc", 998]]}
# @author Adam Daughterson
import os
import shutil
from flask import Flask, request
from Worder import Worder
from FileUtils import FileUtils
import json

# TODO: This should be changed to reflect your actual upload folder
upload_folder = '/tmp/worder'
extension = set(['zip'])
response = dict()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_folder

# We only want to allow zip files to be uploaded.
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in extension

# This creates the URL path http://<host:port>/worder, and runs the associated method (upload()) below.
@app.route('/worder', methods=['POST'])
def upload():
    file = request.files['file']
    try:
        os.makedirs(upload_folder)
    except Exception as e:
        handle_failure(e)

    if file and allowed_file(file.filename):
        try:
            file.save(os.path.join(upload_folder, file.filename))
        except Exception as e:
            handle_failure(e)
    else:
        handle_failure("Invalid file. Check file type, and integrity.")

    # Create an instance of Worder
    worder = Worder(max_threads=3, tmpdir=upload_folder)
    try:
        words = worder.get_words(os.path.join(upload_folder, file.filename))
        if words and len(words) > 0:
            response['status'] = 'success'
            response['words'] = words
        else:
            raise Exception("Word list is malformed.")
    except Exception as e:
        handle_failure(e)
    try:
        shutil.rmtree(upload_folder)
    except Exception as e:
        handle_failure(e)
    return json.dumps(response,sort_keys=True)

def handle_failure(e):
    response = dict()
    response['status'] = 'failed'
    response['message'] = e
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
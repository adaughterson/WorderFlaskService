SYNOPSIS
    python WorderService.py

OVERVIEW
    The WorderService is a lightweight HTTP service which listens on port 5001 for an upload of a zip file.
    When it receives the zip file, it then hands processing off to Worder which returns a list of tuples of the top ten words
        discovered in the text files contained within the uploaded zip file, and the count of each word.
    WorderService then returns a status JSON object containing the result of the search, and the list of discovered words,
        or in a failing case, the failing status and the error message returned.

DEPENDANCIES
    Install python modules:
        Flask
    Change hard-coded path to upload folder in WorderService.py. This would ideally be configuration based, but I ran out of time.

EXAMPLE USAGE
    Issue a POST such as the following:
        $ curl -X POST -H "Content-Type: multipart/form-data" -F file=@your.zip http://<host>:5001/worder
        {"status": "success", "words": [["self", 121], ["0", 69], ["1", 54], ["e", 51], ["file", 35], ["9", 34], ["n", 32], ["words", 30], ["to", 30], ["for", 29]]}

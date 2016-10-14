# @class Count the number of words delimited by non-word characters.
# @author Adam Daughterson
from Queue import Queue
import threading
import operator
import mimetypes
import os
from FileUtils import FileUtils
from SearchWorker import SearchWorker
from AdamD import AdamD

class Worder(AdamD):
    def __init__(self,max_threads=3,tmpdir=None):
        AdamD.__init__(self)
        self.fileU = FileUtils()
        self.qlock = threading.Lock()
        self.queue = Queue(max_threads)
        self.files = list()
        self.threads = list()
        self.words = dict()
        self.tmpdir = tmpdir

    # @brief Public getter of words in text files contained within a zipfile.
    # @param string zipfile The archive with text files to scan for words.
    # @returns list result_words The list of tuples containing words and counts.
    def get_words(self,zipfile):
        result_words = []
        try:
            # Unzip the archive to self.tmpdir, and populate the file list
            self.fileU.unzip(zipfile,self.tmpdir)
            self.files = self.fileU.get_file_list(self.tmpdir)
        except Exception as e:
            self.log("Unable to retrieve file list from {}\n{}".format(file,e))
        # We presumably have a list of files now
        if len(self.files) > 0:
            try:
                result_words = self._get_words()
            except Exception as e:
                self.log("Unable to get words, see detailed error messages\n{0}".format(e))
        return result_words

    # @brief Private class method for implementation of word search.
    #     Creates thread pool of <max_threads> breadth.
    #     Spawns SearchWorker thread instances for each file in self.files
    #     Adds threads to queue
    #     Waits for queue to empty
    #  @returns list sliced First 10 elements of sorted_words.
    def _get_words(self):
        thread_id = 0
        # For passing a reference to the current context to the worker thread.
        me = self
        # Create threads
        for filename in self.files:
            if os.path.isfile(filename):
                filetype, enc = mimetypes.guess_type(filename)
                if filetype and filetype.startswith('text'):
                    thread = SearchWorker(me,thread_id, filename, self.queue, self.qlock)
                    thread.start()
                    self.threads.append(thread)
                    thread_id += 1
                    self.qlock.acquire()
                    self.queue.put(filename)
                    self.qlock.release()

        # wait for queue to empty
        while not self.queue.empty():
            pass

        # Wait for all threads to complete
        for t in self.threads:
            t.join()

        # Get top 10 words
        sorted_words = sorted(self.words.items(),key=operator.itemgetter(1))
        sorted_words.reverse()
        sliced = sorted_words[:10]
        return sliced

    # @brief Setter of words.
    #    Adds words to self.words.
    # @param string word The word to add.
    # @returns bool result True of False
    def add_word(self,word):
        result = False
        try:
            if self.words.has_key(word):
                self.log("Incrementing pre-existing word {}".format(word))
                self.words[word] += 1
            else:
                self.log("Creating new word {}".format(word))
                self.words[word] = 1
            result = True
        except Exception as e:
            self.log("Issue encountered attempting to add a word: {}".format(e))
        return result
# @class Extension of threading.Thread which allows for abstracting away the implementation of searching for words
#    in files, and adding them to local Worder instance.
import threading
from FileUtils import FileUtils

# @param Worder worder A local instance of the Worder who spawned us.
# @param int threadID ID of this thread.
# @param string filename The filename to search.
# @param Queue q The instance of Queue we are adding this thread to.
# @param threading.Lock qlock The lock to use when we want to write.
class SearchWorker(threading.Thread):
    def __init__(self, worder, threadID, filename, q,qlock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.filename = filename
        self.q = q
        self.qlock = qlock
        self.worder = worder
        self.fileU = FileUtils()

    # @brief Overridden threading.thread.run() method. Calls self._process_data()
    def run(self):
        self._process_data()

    # @brief Handles getting a slot in execution queue, and executing the search once queued.
    def _process_data(self):
        result = False
        while not result:
            if not self.q.empty():
                qpos = self.q.get()
                try:
                    # Pass the search of the file to FileUtils instance
                    words = self.fileU.find_words(self.filename)
                    fwords = [word for word in words if word != '']
                    for word in fwords:
                        self.qlock.acquire()
                        result = self.worder.add_word(word)
                        self.qlock.release()
                except Exception as e:
                    self.worder.log("Failed to add word to list\n{}".format(e))
                    result = True
            else:
                pass
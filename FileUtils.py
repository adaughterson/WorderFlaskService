# @class File system interaction convenience methods.
# @author Adam Daughterson
import os
import re
import zipfile
import os.path
import shutil
from AdamD import AdamD

class FileUtils(AdamD):
    def __init__(self):
        AdamD.__init__(self)
        word_reg = r"[^a-zA-Z0-9]"
        self.word_reg = re.compile(word_reg)

    # @brief Get the list of files in a directory.
    # @param string dir The absolute path of the directory to list.
    # @returns list file_list Array of paths
    def get_file_list(self,dir):
        file_list = list()
        try:
            files = os.listdir(dir)
            for fname in files:
                file_list.append(os.path.join(dir,fname))
        except Exception as e:
            self.log("Unable to get file list from {}\n{}".format(dir,e))
        return file_list

    # @brief Convenience method for unzipping archives.
    # @param string archive Absolute path to zipfile to unzip.
    # @param string outdir Absolute path to ouput dir.
    def unzip(self,archive,outdir):
        zip = zipfile.ZipFile(archive)
        try:
            zip.extractall(outdir)
        except Exception as e:
            self.log("Unable to unzip {}\n{}".format(archive,e))

    # @brief Searches file for words delimited by non-words.
    # @param string filepath The absolute path to the file to search.
    # @returns list words Array containing all words found in file.
    def find_words(self,filepath):
        wordlists = list()
        words = list()
        with open(filepath) as infile:
            for line in infile:
                wordlists.append(re.split(r"[^a-zA-Z0-9]",line))
        for wlist in wordlists:
            for word in wlist:
                words.append(word)
        return words

    # @brief Create temp dirs
    def create_temps(self,abs_path):
        self.log("Creating temp dir")
        try:
            os.makedirs(abs_path)
        except Exception as e:
            self.log("Errors encountered creating temp dir {}. Message: {}".format(abs_path,e))

    # @brief Cleanup temp dirs
    def cleanup_temps(self,abs_path):
        self.log("Cleaning up...")
        try:
            shutil.rmtree(abs_path)
        except Exception as e:
            self.log("Error cleaning up {}. You will need to manually delete the temporary files.\nError message: {}".format(abs_path,e))
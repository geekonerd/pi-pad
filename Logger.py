from time import time
from datetime import datetime

# Logger Utility
class Logger :

    # initialize
    def __init__(self, devel):
        self.devel = devel
        self.debug("Logger init done!")

    # get current timestamp in "YYYY-MM-DD HH:MM:SS" format
    def getTS(self) :
        ts = time()
        return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    # log a debug msg
    def debug(self, mex) :
        if (self.devel) : print("::", self.getTS(), ">>DEBUG<< ::", mex)

    # log an error msg
    def error(self, mex) :
        print ("::", self.getTS(), "!!ERROR!! ::", mex)

    # log a generic message
    def log(self, mex) :
        print ("::", self.getTS(), "::", mex)

# DEBUG
if __name__ == "__main__" :
    # instantiate
    log = Logger(True)

    # test methods
    log.log("Welcome! Testing Logger:")
    log.debug("Debug message")
    log.error("Error message")
    log.log("Generic message")

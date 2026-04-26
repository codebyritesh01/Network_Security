import sys
# sys module is used to access system-level information.
# Here we use sys.exc_info() to get details of the current exception:
# error type, error object, and traceback information.

from logging import Logger;

# Custom exception class
# It inherits from Python's built-in Exception class
class NetworkSecurityException(Exception):

    # Constructor runs when object is created
    # error_message = original error message
    # error_detail = sys module, used to extract traceback info
    def __init__(self, error_message, error_detail: sys):

        # Store original error message
        self.error_message = error_message

        # sys.exc_info() returns:
        # type of error, actual error, traceback object
        _, _, exc_tb = error_detail.exc_info()

        # Line number where error happened
        self.lineno = exc_tb.tb_lineno

        # File name where error happened
        self.file_name = exc_tb.tb_frame.f_code.co_filename


    # __str__ runs when we print exception object
    # It returns user-friendly error message
    def __str__(self):

        return "Error occured in python script name [{0}] linenumber [{1}] error message [{2}]".format(
            self.file_name,              # Python file name
            self.lineno,                # Error line number
            str(self.error_message)     # Original error message
        )
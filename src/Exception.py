import sys
import logging
from src.logger import logging

def error_messsage_details(error,error_details:sys):
    _,_,exc_tb = error_details.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = 'Error occurred in python script name [{0}] line [{1}] error message [{2}]'.format(file_name,exc_tb.tb_lineno,str(error))
    return error_message

class CustomException(Exception):
    def __init__(self,error_message,error_details:sys):
        super().__init__(error_message)
        self.error_message = error_messsage_details(error_message,error_details=error_details)
        logging.info(self.error_message)
        
    def __str__(self):
        return self.error_message
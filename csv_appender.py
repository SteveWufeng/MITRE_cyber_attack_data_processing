# 
# file: csv_appender.py
# @Author: Steve Wufeng
import pandas as pd
import csv
import numpy as np

class csv_appender:
    """processes a csv file and appends each line to another
        csv file.
    """
    # all possible states of the class
    __slots__ = ["__source_csv", "__destination_csv", "__buffer",
                 "__row_read_progress"]
    
    def __init__(self, source_csv: str, destination_csv: str, 
                 progress: int = 0) -> None:
        """constructor for a csv_appender object.
        
        Args:
            source_csv (str): source of the csv file to be processed.
            destination_csv (str): destination csv file to append to.
        """
        # progress of reading the source csv file
        self.__row_read_progress = progress 
        # open the source csv file and
        # extract only columns 'C' and 'H'
        self.__source_csv = pd.read_csv(source_csv, 
                                        header=0,
                                        usecols=["description", "tactics"],
                                        skiprows=range(progress))
        # turn the dataframe into a numpy array
        self.__source_csv = self.__source_csv.to_numpy()
        
        # save the destination csv file
        self.__destination_csv = destination_csv
        
        try:
            self.process_source() # process the source csv file
        except:
            self.save_progress() # save progress if error occurs
            raise Exception(
                "An error occur while processing the source csv file.")
        try:
            # append the processed data to the destination csv file
            self.append_to_destination()
        except:
            raise Exception(
                "An error occur while appending to the destination csv file.")

    def process_source(self) -> None:
        """process one line of data in the source csv file.
        """
        # # get the description of from the source csv file
        # description = self.__source_csv[self.__row_read_progress][0]
        # # get the Tactics from the source csv file
        # tactics = self.__source_csv[self.__row_read_progress][1]
        self.__buffer = "testing 123, 456"
        # print(self.__source_csv[self.__row_read_progress][0])
        # print(self.__source_csv[self.__row_read_progress][1])
    
    def append_to_destination(self) -> None:
        """simply append the buffer to the destination csv file.
        """
        with open(self.__destination_csv, "a") as file:
            file.write(self.__buffer)
        
    def save_progress(self) -> None:
        """save a file that contains the progress of the
            source csv file.
        """
        with open("progress.txt", "w") as file:
            file.write(f"{self.__source_csv}: {self.__row_read_progress}")

if __name__ == "__main__":
    csv_appender("enterprise-attack-v11.3.csv", "MITRE_Dataset.csv")
    
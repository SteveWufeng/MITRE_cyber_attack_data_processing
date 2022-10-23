# 
# file: csv_appender.py
# description: Appends a csv file to another csv file line by line
#              specifically, it finds two desired columns in the source file
#              column 1 will be the paragraph, and column 2 will be the label.
#              appends each line of the paragraph followed by their labels to
#              the destination file.
#              Note: this script will also filter out unwanted content in the 
#              paragraph column. It will citations, web links, "</code><code>"
# @Author: Steve Wufeng
from pickle import NONE
import pandas as pd
import numpy as np
import re

class csv_appender:
    """processes a csv file and appends each line to another
        csv file.
    """
    # all possible states of the class
    __slots__ = ["__source_csv","__source_data", "__destination_csv", "__buffer",
                 "__row_read_progress"]
    
    def __init__(self, source_csv: str, destination_csv: str) -> None:
        """constructor for a csv_appender object.
        
        Args:
            source_csv (str): source of the csv file to be processed.
            destination_csv (str): destination csv file to append to.
        """
        # progress of reading the source csv file  
        # check if the a previous progress file exists
        try:    
            with open(f"{source_csv[:-3]}_progress.txt", 'r') as file:
                # continue from the progress
                self.__row_read_progress = int(file.readline()) 
        except:
            print("no previous progress found")
            self.__row_read_progress = 0 
        
        self.__row_read_progress = 0 # uncomment this line will start from the beginning
        # open the source csv file and
        # extract only columns 'C'(description) and 'H'(tactics)
        self.__source_csv = source_csv
        
        try: # try to open the source csv file
            self.__source_data = pd.read_csv(source_csv, 
                                            header=0,
                                            usecols=["description", "tactics"])
        except FileNotFoundError: # if the file is not found
            raise FileNotFoundError(f"file {source_csv} not found!")
        
        # turn the dataframe into a numpy array
        self.__source_data = self.__source_data.to_numpy()
        
        # save the destination csv file
        self.__destination_csv = destination_csv
        
        # buffer to store the processed data
        self.__buffer = []
        # start the parse and append process
        
        while(self.__row_read_progress < len(self.__source_data)):
            self.parse_and_append()
            self.__buffer = [] # clear the buffer after each iteration
        
    def parse_and_append(self):
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

        self.__row_read_progress += 1 # update progress
        self.save_progress() # save progress

    def process_source(self) -> None:
        """process one line of data in the source csv file.
            this method updates the __buffer attribute. 
        """
        # first check if we have reached the end of the database
        if (self.__row_read_progress > len(self.__source_data)):
            print("Process complete! Nothing else to do!")
            
        # get the description of from the source csv file
        description = str(self.__source_data[self.__row_read_progress][0])
        description = description.replace("\n", " ") # remove new line characters to better apply regular expression
        
        # apply regular expression to remove unwanted stuff 
        # filter out citation, and web link string in the sentense         
                # ex. (Citation: RIT library)
                # ex. (https://www.rit.edu)
                # ex. <code>
                # ex. </code>
        description = self.filter("(\(Citation:.*\))|(\(https://[\w\s\./]*\))|(</code>)|(<code>)", description)
        description = description.split(".")
        
        # get the Tactics from the source csv file
        tactics = str(self.__source_data[self.__row_read_progress][1])
        tactics = tactics.replace(" ", "_") # replace spaces with underscores
        tactics = tactics.upper()   # upper case the tactics
        
        # format description and tactics and append to buffer
        for sentense in description:
            # each element in the buffer represents a line in the csv file
            # they will be appended in the destination csv file later
            if not((sentense in ["", " ", "\n", NONE])): # ignore any empty sentenses       
                self.__buffer.append(f"\"{sentense.strip()}.\",{tactics}")
    
    def append_to_destination(self) -> None:
        """simply append the buffer to the destination csv file.
        """
        with open(self.__destination_csv, "a") as file:
            for csv_line in self.__buffer:
                file.write(csv_line+"\n")
        
    def save_progress(self) -> None:
        """save a file that contains the progress of the
            source csv file.
        """
        with open(f"{self.__source_csv[:-3]}_progress.txt", "w") as file:
            file.write(f"{self.__row_read_progress}\n")

    def filter(self, regEx: str, sentense: str) -> str:
        """filter out stuff we don't want from the string
        Args:
            sentense (str): the string to be filtered
            regEx (str): the regular expression pattern to be removed
            
        """
        matches = re.findall(regEx, sentense)
        for match in matches:
            for token in match:
                if token != "":
                    sentense = sentense.replace(token, "")
        return sentense

if __name__ == "__main__":
    # csv_appender("enterprise-attack-v11.3.csv", "MITRE_Dataset.csv")
    # csv_appender("enterprise-attack-v11.3.csv", "testout2.csv")
    csv_appender("testin.csv", "testout.csv")
#from root_pandas import read_root
from progressbar import ProgressBar
import pandas as pd
import fastparquet
import pyarrow.feather as feather
import sys
import traceback
import logging
import time
import numpy as np


## Gloval parameters
fileLocation = '/eos/user/r/rkamalie/'

def root2disk(fileName, chunkSize=1000000):
    """
    A function to convert input ROOT file into parquet and feather formats for later 
    faster input/output from disk.

    Parameters
    ----------
    - fileName : string
       Specifies location and name of the file

    - chunkSize : int
       A part of the whole sample that is read and processed at a time. 
    
    Raises
    ------
    - Nothing. Used to have TypeError if no parameters are given. 
    
    Returns
    -------
    - Void

    """

    if not isinstance(fileName, str) and not isinstance(chunkSize, int):
        raise TypeError("Please specify both fileName and chunkSize parameters! Exiting.")


    #pbar = ProgressBar()
    count = 1
    #for df in pbar(read_root(filename, chunksize=oneMillion)):
    print 'Processing >>'
    for df in read_root(paths=fileName, chunksize=chunkSize):
        print '>>'*count
        feather.write_feather(df, 'ndf_{0}.feather'.format(count))
        df.to_parquet('ndf_{0}.parquet'.format(count), engine='fastparquet', compression='gzip')
        count +=1
        if count >100:
            break
    
    


def readFilesIntoDataFrame(nameTemplate, numOfFiles):
    #https://www.kaggle.com/arjanso/reducing-dataframe-memory-size-by-65
    """                                                                                                                                               
    A function to convert parquet or feather data files into the pandas dataframe.
    
    Parameters                                                                                                                                        
    ----------                                                                                                                                        
    - nameTemplate : string                                                                                                                               
      Template that describes name pattern of existing data files.
                                                                                                                                                      
    - numOfFiles : int                                                                                                                                 
      Number of files to process, should be equal to the total number of data files if one aims to load the full sample.
                                                                                                                                                      
    Raises                                                                                                                                            
    ------                                                                                                                                            
    - Nothing.                                                       
                                                                                                                                                      
    Returns                                                                                                                                           
    -------                                                                                                                                           
    - Final dataframe made of individual data files.                                                                                                                                          
                                                                                                                                                      
    """

    list_of_dfs = []
    for i in range(numOfFiles):
        print ('Processing {0} out of {1} files'.format(i, numOfFiles))

        fileToProcess = fileLocation + nameTemplate.format(i)
        print 'fileToProcess=', fileToProcess
        
        if 'feather' in nameTemplate:
            read_df = feather.read_feather(fileToProcess)
        elif 'parquet' in nameTemplate:
            read_df = pd.read_parquet(fileToProcess)
        else:
            print 'This should not happen, nameTemplate is wrong, please check it is in parquet or feather format or that the template correctly describes the existing files, exiting...'
            sys.exit(1)

        print read_df.info(memory_usage='deep')
        print '-'*50
        print read_df.describe()
        list_of_dfs.append(read_df)
    
    print 'Start concatenating dataframes, it may take some time'
    comb_df = pd.concat(list_of_dfs, ignore_index=True)
    return comb_df

def main():

    try:
        filename = "/eos/cms/store/group/phys_egamma/ReleaseInputsArchive/2017UL_ElePhoReg/input_trees/DoubleElectron_FlatPt-1To300_2017ConditionsFlatPU0to70ECALGT_105X_mc2017_realistic_IdealEcalIC_v5-v2_AODSIM_EgRegTreeV5Refined.root"
        twentyMillion = 20000000
        #root2disk(filename, twentyMillion)
    

        parquetStringIn = 'df_{:d}.parquet'
        featherStringIn = 'df_{:d}.feather'

        readFilesIntoDataFrame(featherStringIn, 1)

    except Exception as e:
        logging.error(traceback.format_exc())



if __name__ == '__main__':
    start_time = time.time()

    main()
    #sys.exit(main())




    end_time = time.time()
    time_taken = end_time - start_time # time_taken is in seconds                                                           
                                                                                                                         
    hours, rest = divmod(time_taken,3600)
    minutes, seconds = divmod(rest, 60)
    print
    print "---It took {hours} hours, {minutes} minutes, and {seconds:.1f} seconds to run this script ---".format (hours=hours, minutes=minutes, seconds=seconds) 








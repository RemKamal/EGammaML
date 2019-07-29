import re, io, sys
import subprocess

fullRun = False


def skim():
    sampleRe = re.compile(r'comb_listOf_([A-Za-z0-9_-]*)_trees(\w*)')
    files_txt = '../dataAndBackgroundSamplesFinal.txt' if fullRun else '../signalSamplesFinal_GluGluToRadionToHHTo2B2ZTo2L2Nu.txt'#signalSamplesFinal_test.txt'
    print 'files_txt was', files_txt
    with io.open(files_txt, mode="rt", encoding="utf-8") as f:
        listOfFiles = f.read().split('\n')[:-1]
    for fil in listOfFiles:

        if fil.startswith('./'):
            fil = fil[2:]
        print 'fil is ', fil
        matchObj = sampleRe.search(fil)
        sampleName = matchObj.group(1)
        if sampleName not in fil:
            print 'An error happened, list of samples and sample name do NOT coincide, please check. See top of the script for the hint.'
            exit(1)
        print ' file is ', fil
        print 'sample name is ', sampleName
        command = 'python submit_v5.py ../' + fil + ' ' + sampleName
        print 'command is',command
        subprocess.call(command, shell=True)



def main():

    import traceback
    import logging

    try:
        skim()
    #skimData()
    #skimBackground()
    
    except Exception as e:
        logging.error(traceback.format_exc())
    # Logs the error appropriately. 



if __name__ == '__main__':
    sys.exit(main())








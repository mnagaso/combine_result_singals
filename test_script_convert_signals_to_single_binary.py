import subprocess, glob
import re
from optparse import OptionParser


# some functions for sorting signal files take from -> https://nedbatchelder.com/blog/200712/human_sorting.html
def tryint(s):
    try:
        return int(s)
    except ValueError:
        return s
 

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]


def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)


def main():
    """
    """
    
    parser = OptionParser()
    parser.add_option("-d", "--dir", dest="dpath", help="directory path where *semp files are placed", metavar="DIR_PATH", default="OUTPUT_FILES")
    parser.add_option("-o", "--outfile", dest="fname", help="output filename", metavar="OUTFILE",default="out.h5")

    options, args = parser.parse_args()
    file_directory_path    = options.dpath
    output_file_name        = options.fname

    # make a list of .semp files
    sig_files = glob.glob(file_directory_path+"/*semp")
    
    # reorder
    sort_nicely(sig_files)
    #print(sig_files)

    # read the last timestep number
    last_timestep = sum(1 for line in open(sig_files[0]))
    #print(last_timestep)

    # time window for limited extraction of timesteps
    time_window = [0, last_timestep-1]  

    # writeout a file list as an text file
    fname = "signal_file_list.txt"
    with open(fname, "w") as f:
        for i, path in enumerate(sig_files):
            f.write("./"+path+"\n")

    # binarize_signals
    cmd = './combine ' + fname + ' ' + output_file_name + ' ' + str(len(sig_files)) + \
                   ' ' + str(time_window[0]) + ' ' +  str(time_window[1]) + ' ' + str(last_timestep)
    subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    main()   

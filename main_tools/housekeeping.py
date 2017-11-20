import argparse
import psutil

from main_tools import global_vars
from main_tools.my_random import MY_RANDOM as random
import sys


def prettyPrintSet(level, prefix, element, dictionary=None):
    if dictionary:
        print("{}{}{} --> {}".format(prefix, "  "*level, element, dictionary[element]))
    else:
        print("{}{}{}".format(prefix, "  "*level, element))
    if type(element) == type({}):
        for item in element:
            prettyPrintSet(level + 1, prefix, item, dictionary)
    elif type(element) == type([]):
        for item in element:
            prettyPrintSet(level + 1, prefix, item)

def debugPrint(verbosLevel, string, dictionary=None):
    if global_vars.verbos >= verbosLevel: 
        spacing = "  "*(verbosLevel-1)
        BLUE_START = "\033[94m"
        COLOR_END = "\033[0m"
        prefix = "{}{}debug-{}: {}".format(spacing,BLUE_START,verbosLevel,COLOR_END)
        print("{}{}".format(prefix,string))
        if dictionary:
            for element in dictionary:
                if type(dictionary) == type({}):
                    prettyPrintSet(1, prefix, element, dictionary)
                else:
                    prettyPrintSet(1, prefix, element)

def process_args(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--param",help="REQUIRED!: The location of the parameter file",required=True)
    parser.add_argument("-m","--model",help="REQUIRED!: The location of the model file",required=True)
    parser.add_argument("-i","--id", help="REQUIRED!: The unique identifier of the job",required=True)
    parser.add_argument("-o","--out", help="REQUIRED!: The location of the output dir",required=True)
    parser.add_argument("-g","--map", help="The location of the genetic map file")
    parser.add_argument("-a","--array", help="The location of the array template file, in bed form")
    parser.add_argument("-v", help="increase output verbosity", action="count",default=0)
    parser.add_argument('--profile', action='store_true', default=False, help="Print a log file containing the time in seconds and memory use in Mb for main functions")
    tmpArgs = parser.parse_args()

    args = {
            'param file':tmpArgs.param,
            'model file':tmpArgs.model,
            'genetic map':tmpArgs.map,
            'SNP file':tmpArgs.array,
            'job':tmpArgs.id,
            'path':tmpArgs.out,
            'profile':tmpArgs.profile
        }
    model_args = argsFromModelCSV(tmpArgs.model)
    args['sim option'] = model_args['sim option']
    args['germline'] = model_args['germline']
    args['pedmap'] = model_args['pedmap']
    args['random discovery'] = model_args['random discovery']


    global_vars.init()
    global_vars.verbos = tmpArgs.v
    debugPrint(1,"Debug on: Level " + str(global_vars.verbos))

    return args

def set_seed(seed_option):
    seed_option = int(seed_option)
    if seed_option == 0:
        random.seed()
    if seed_option > int(0):
        random.seed(seed_option)

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def argsFromModelCSV(filename):
    #Reads arguments from model_file.csv
    #returns model_args dictionary
    f=open(filename, 'r')
    model_args=dict()
    for line in f:
        if line.startswith("-macs") or line.startswith("-macs_file"):
            x = line.strip().split(",")
            model_args['sim option']= x[0][1:]
        if line.startswith("-macsswig"):
            x = line.strip().split(",")
            model_args['sim option']= x[0][1:]
        if line.startswith("-germline"):
            model_args['germline']= True
        if line.startswith("-nonrandom_discovery"):
            model_args['random discovery'] = False
        if line.startswith("-random_discovery"):
            x = line.strip().split(",")
            # model_args['random discovery'] = str2bool(x[1])
            model_args['random discovery'] = x[1]
        if line.startswith("-pedmap"):
            model_args['pedmap'] = True
        
    if 'sim option' not in model_args:
        print("Sim option not provided in model_file.csv")
        sys.exit(1)
    if 'germline' not in model_args:
        model_args['germline'] = False
    if 'random discovery' not in model_args:
        model_args['random discovery'] = True
    if 'pedmap' not in model_args:
        model_args['pedmap'] = False
    return model_args


def profile(prof_option, path, job, func):
    if(prof_option == True):
        fprof = open(str(path) + '/profile' + str(job) + '.log', 'a')
        p = psutil.Process()
        with p.oneshot():
            p.cpu_times()  # return cached value
            p.memory_full_info()

        time = p.cpu_times().user
        mem = (float(p.memory_full_info().uss) / 1048576)
        fprof.write(str(func) + '\t' + str(time) + '\t' + str(mem) + '\t' + str(job) + '\n')
    return

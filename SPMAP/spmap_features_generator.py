import sys, os
#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math
import multiprocessing as mp
import fileinput
import sys, getopt
from os import listdir
from os.path import isfile, join
import re
import numpy as np
from fasta import readFasta
MAX_NUMBER = sys.maxsize
MIN_NUMBER = (-1) * MAX_NUMBER -1

def usage():
    print ("spmap_features_generator.py usage:")
    print ("python spmap_features_generator.py <options> <source files> ")
    print ("-i,--input: input a file in fasta format.")
    print ("-o,--ouput: output a file of the generated feature.")
    print ("-p,--profile: specify the profile file.")
    print ("-h,--help: show the help information.")



opts, args = getopt.getopt(sys.argv[1:], 'i:o:p:a:b:h', ['input=','output=','profile=','argument=','veriable=','help'])
inputFile=""
outputFile=""
profile=""
argument=""
veriable=""

for opt, arg in opts:
    if opt in ('-i','--input'):
        inputFile = arg
    elif opt in ('-o','--output'):
        outputFile = arg
    elif opt in ('-p','--profile'):
        profile = arg
    elif opt in ('-a','--argument'):
        argument = int(arg)
    elif opt in ('-b','--veriable'):
        veriable = int(arg)
    elif opt in ('-h', '--help'):
        usage()
        sys.exit(2)
    else:
        usage()
        sys.exit(2)
check_head = re.compile(r'\>')



def parse_profile_values(item):
    item = item.replace("[","").replace("]","")
    values_list = item.split(",")
    new_list_values = list()
    for value in values_list:
        new_list_values.append(float(value.strip()))
    return new_list_values

def read_profiles(filename_profile):
    alphabet = "ARNDCQEGHILKMFPSTWYV"
    file = open(filename_profile,"r")
    profile_dict = dict()
    for line in file:
        if line == "\n":
            continue
        item_list = line.split(":")
        if item_list[0].strip() == "NUMBER OF CLUSTER":
            cluster_id = item_list[1].strip()
            profile_dict[cluster_id] = dict()
        if item_list[0].strip() in alphabet:
            letter = item_list[0].strip()
            profile_dict[cluster_id][letter] = parse_profile_values(item_list[1].strip())
    file.close()
    return profile_dict



def extract_subsequences(sequence):
    subsequence_list = [sequence[i:i+5] for i in range(len(sequence)-4)]
    return subsequence_list
def calculate_fv(subsequence_list, profile_dict):
    list_fv = list()
    for cluster_id in profile_dict:
        max_value = MIN_NUMBER
        for subsequence in subsequence_list:
            if "X" in subsequence or "B" in subsequence or "Z" in subsequence:
                continue
            sum_values = 0
            for i in range(len(subsequence)):
                letter = subsequence[i]
                sum_values += profile_dict[cluster_id][letter][i]
            if sum_values > max_value:
                max_value = sum_values
        if max_value < -15:
            max_value = 0
        else:
            max_value = math.exp(max_value)
        list_fv.append(max_value)
    return list_fv


def form_feature_vector(prot_id, sequence, profile_dict):
    subsequence_list = extract_subsequences(sequence)
    return prot_id, calculate_fv(subsequence_list, profile_dict)

def write_feature_vector(filename_fv,fv_dict):
    file = open(filename_fv, "w")
    for prot_id in fv_dict:
        file.write(">"+prot_id)
        for value in fv_dict[prot_id]:
            file.writelines(["\t",str(value)])
        file.write("\n")
    file.close()
    return

def create_fv_files():
    filename_fasta = inputFile
    filename_profile = profile
    filename_fv = outputFile
    fasta_dict = readFasta(filename_fasta)
    profile_dict = read_profiles(filename_profile)
    pool = mp.Pool(processes=8)
    results = [pool.apply_async(form_feature_vector, args=(prot_id, fasta_dict[prot_id], profile_dict)) for prot_id in fasta_dict]

    fv_dict_raw = dict()
    for p in results:
      (prot_id, fv) = p.get()
      fv_dict_raw[prot_id] = fv
    write_feature_vector(filename_fv, fv_dict_raw)
    return


#DATA = "_golden_trust_negative"
#create_fv_files(SETNAME, DATA)
create_fv_files()


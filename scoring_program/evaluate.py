#!/usr/bin/env python
import sys
from sys import argv
from os import listdir
from os.path import isfile, join
import os.path
from glob import glob
import re
import subprocess
import shlex
import json

__author__ = 'sopankhosla'

root_dir = "/Users/sopank/Documents/CMU/Work/Coref/SharedTask/codi2021/"
default_input_dir = root_dir + "scoring_input_1_2"
default_output_dir = root_dir + "scoring_output"

# Debug flag 0: no debug, 1: show all scores, 2: also show version amd listing of dir
debug_mode = False

# Version number
scoring_version = 1.0

def run_command(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    return p.stdout.read()

def get_results_from_scorer(submit_dir, truth_dir, options):

    if debug_mode:
        print(submit_dir)
        print(truth_dir)

    if debug_mode:
        with open(truth_dir, "r") as f:
            t = f.read()

        with open(submit_dir, "r") as f:
            s = f.read()

        try:
            assert t == s
            print("Assertion passed!!")
            print(t[:100])
            print(s[:100])
        except:
            print("Assertion failed!!")
            print(t[:100])
            print(s[:100])

    if local_mode:
        scoring_file = os.getcwd() + "/ua-scorer/ua-scorer.py"
    else:
        scoring_file = os.getcwd() + "/program/ua-scorer/ua-scorer.py"

    cmd = "python " + scoring_file + " " + truth_dir + " " + submit_dir + " " + " ".join(options) + " shared_task" 

    print("Command:")
    print(cmd)
    
    output = run_command(cmd.split()).decode("utf-8")

    if debug_mode:
        print("Output: ", output.split("\n"))

    result_json = json.loads(output.split("\n")[-2])

    return result_json

def output_to_dict(result_json, output_dict, result_type, dataset, selected_score):

    if debug_mode:
        print(result_json[result_type].keys())
    for metric in result_json[result_type]:
        for name, val in result_json[result_type][metric].items():
            output_dict[dataset + "_" + result_type + "_" + metric + "_" + name] = val

    output_dict[dataset + "_" + result_type] = output_dict[dataset + "_" + result_type + "_" + selected_score]

    return output_dict

def scorer(submit_dir, truth_dir, result_type, options, selected_score):

    submitted_datasets = [x.split("/")[-2] for x in glob(os.path.join(submit_dir, "*", ""))]
    truth_datasets = [x.split("/")[-2] for x in glob(os.path.join(truth_dir, "*", ""))]

    print('\nSubmitted dataset folders')
    print(submitted_datasets)

    print('\nTruth datasets folders')
    print(truth_datasets)
    output_dict = {}
    try:
        for d in data_map:
            dataset = data_map[d]
            if d not in truth_datasets:
                print("\nSorry, " + d + " is not available right now!")
                output_dict[dataset + "_" + result_type] = 0.0
                continue
            if d not in submitted_datasets or len(os.listdir(os.path.join(submit_dir, d))) == 0:
                print("You did not submit results for " + d)
                output_dict[dataset + "_" + result_type] = 0.0           
                continue
            
            submit_file = [f for f in os.listdir(os.path.join(submit_dir, d)) if f[0] != "."][0]           
            truth_file = [f for f in os.listdir(os.path.join(truth_dir, d)) if f[0] != "."][0]
            
            print("\n=======================\n")
            print("Calculating scores for " + d + "\n")

            print("Submitted filename: " + submit_file)
            print("Truth filename: " + truth_file + "\n")

            result_json = get_results_from_scorer(
                            os.path.join(os.path.join(submit_dir, d), submit_file), 
                            os.path.join(os.path.join(truth_dir, d), truth_file), 
                            options
                        )

            if debug_mode:
                print("result json ", result_json)
            
            output_to_dict(
                result_json, output_dict, 
                result_type, dataset, 
                selected_score
            )

            print("\n=======================\n")

        # Unfortunate Fallback 
        if "Lgt_AR" not in output_dict:
            output_dict["Lgt_AR"] = 0.0
        
        return output_dict

    except Exception as e:
        exception_printed = False
        if result_type == "AR":
            if not exception_printed:
                print("Coreference scorer not working properly!!")
            output_dict = {
                "Lgt_AR": 0,
                "AMI_AR": 0,
                "Per_AR": 0,
                "Swbd_AR": 0,
                "ARR_AR": 0
            }
        elif result_type == "Br":
            if not exception_printed:
                print("Bridging scorer not working properly!!")
            output_dict = {
                "Lgt_AR": 0,
                "Lgt_Br": 0,
                "AMI_Br": 0,
                "Per_Br": 0,
                "Swbd_Br": 0,
                "ARR_Br": 0
            }
        else:
            if not exception_printed:
                print("Discourse Deixis scorer not working properly!!")
            output_dict = {
                "Lgt_AR": 0,
                "Lgt_DD": 0,
                "AMI_DD": 0,
                "Per_DD": 0,
                "Swbd_DD": 0,
                "ARR_DD": 0
            }
        return output_dict

def scoring_router(submit_dir, truth_dir, comp_phase):

    result_type = comp_phase.split("-")[1]
    if comp_phase.split("-")[1] == 'AR':
        options = []
        selected_score = "CoNLL_F1"

    elif comp_phase.split("-")[1] == 'Br':
        options = ["keep_bridging"]
        selected_score = "fbe_F1"

    elif comp_phase.split("-")[1] == 'DD':
        options = ["evaluate_discourse_deixis"]
        selected_score = "CoNLL_F1"
    else:
        raise NotImplementedError

    if debug_mode:
        print("Options: ", options)
        print("selected_score: ", selected_score)

    output_dict = scorer(submit_dir, truth_dir, result_type, options, selected_score)
    
    return output_dict


# =============================== MAIN ========================================

if __name__ == "__main__":

    #### INPUT/OUTPUT: Get input and output directory names
    # print(argv[1], argv[2])
    if len(argv) == 1:  # Use the default input and output directories if no arguments are provided
        input_dir = default_input_dir
        output_dir = default_output_dir
    else:
        input_dir = argv[1]
        output_dir = argv[2]

    if root_dir in os.getcwd():
        local_mode = True
        debug_mode = True
    else:
        local_mode = False
        debug_mode = False

    debug_mode = True

    print("Local Mode:", local_mode)
    # if not local_mode:
    #     print("Program directory: ", [f for f in os.listdir('./program')])
    #     print("Temp directory: ", [f for f in os.listdir('./temp')])

    submit_dir = os.path.join(input_dir, 'res')
    try:
        submit_dir = os.path.join(submit_dir, [f for f in listdir(submit_dir)][0])
    except:
        print("Incorrect directory structure!")
        raise Exception("Incorrect directory structure!")
    truth_dir = os.path.join(input_dir, 'ref/reference_data_test')

    print("Input metadata")
    metadata = {}
    if not local_mode:
        with open(os.path.join(input_dir, 'metadata')) as f:
            for r in f.readlines():
                spl = r.strip().split(": ")
                metadata[spl[0]] = ": ".join(spl[1:])
    
    if debug_mode:
        print(metadata)

    data_map = {
        'Light': 'Lgt', 
        'AMI': 'AMI', 
        'Persuasion': 'Per', 
        'Switchboard': 'Swbd', 
        'ARRAU': 'ARR'
    }

    phase_map = {
        "1": "Dev-AR", 
        "2": "Dev-Br",
        "3": "Dev-DD",
        "4": "Eval-AR",
        "5": "Eval-Br-(Gold)",
        "6": "Eval-Br-(Pred)",
        "7": "Eval-DD-(Gold)",
        "8": "Eval-DD-(Pred)"
    }

    if not os.path.isdir(submit_dir):
        print("{} doesn't exist".format(submit_dir))

    if os.path.isdir(submit_dir) and os.path.isdir(truth_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        score_file = open(os.path.join(output_dir, 'scores.txt'), 'w')
        # html_file = open(os.path.join(output_dir, 'scores.html'), 'w')

        if not local_mode:
            comp_phase = phase_map[metadata['competition-phase']]
        else:
            comp_phase = 'Dev-Br'

        if debug_mode:
            print(submit_dir)
            print(truth_dir)
            print(metadata)
            
        print("Competition Phase:", comp_phase)

        output_dict = scoring_router(submit_dir, truth_dir, comp_phase)
        if debug_mode:
            print(output_dict)

        for key, val in output_dict.items():
            score_file.write(str(key) + ":" + str(val) + '\n')

        score_file.close()
    else:
        print("Incorrect directory structure!")
        raise Exception("Incorrect directory structure!")

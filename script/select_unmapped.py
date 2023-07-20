#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 13:46:52 2023

@author: Zhang Xinyue
"""

import argparse
import sys
import os
import random
from argparse import RawTextHelpFormatter

def parser_args(args):
    parser = argparse.ArgumentParser(
    description="This script is used for select unmapped ID",
    formatter_class=argparse.RawTextHelpFormatter,
    usage="python select_uid_unmapped.py [options]",
    )
    parser.add_argument(
        "-N",
        "--unmapped_id",
        type=str,
        default=False,
        help="The unmapped id file.",
        required=True,
    )
    parser.add_argument(
        "-B",
        "--bam_stat",
        type=str,
        default=False,
        help="The bam stat file.",
        required=True,
    )
    parser.add_argument(
        "-U",
        "--uid",
        type=str,
        default=False,
        help="The uid file.",
        required=False,
    )
    parser.add_argument(
        "-S",
        "--star",
        type=str,
        default=True,
        help="Use star mapping.",
        required=False,
    )
    parser.add_argument(
        "-O",
        "--out",
        type=str,
        default="./Unmapped.id.xls",
        help="Output file.",
        required=True,
    )
    return parser.parse_args(args)

args = parser_args(sys.argv[1:])
unmapped_id = args.unmapped_id
bam_stat = args.bam_stat
uid_file = args.uid
Is_STAR = args.star
out_file = args.out
sample = os.path.split(unmapped_id)[0].split('/')[-1]
unmapped_id_set = set()
true_unmapped_id_set = set()
expect_ratio = 0.99

with open(str(unmapped_id), 'r') as fi:
    for line in fi:
        if(line[0] == '@'):
            unmapped_id_set.add(line.split()[0])
            if(Is_STAR):
                next(fi)
                next(fi)
                next(fi)
                
with open(str(bam_stat), 'r') as fi:
    for line in fi:
        lines = line.strip().split('\t')
        if(lines[0] == sample):
            old_ratio = float(lines[2].split('(')[1].split(')')[0])/100

remove_ratio = 1 - (old_ratio/expect_ratio - old_ratio)/(1 - old_ratio)

if(uid_file):
    with open(str(uid_file), 'r') as fi:
        for line in fi:
            lines = line.strip().split('\t')
            if(lines[0] in unmapped_id_set):
                for i in lines[1:]:
                    true_unmapped_id_set.add(i)
    final_set=set(random.sample(list(true_unmapped_id_set),int(len(true_unmapped_id_set)*remove_ratio)))
else:
    final_set=set(random.sample(list(unmapped_id_set),int(len(unmapped_id_set)*remove_ratio)))
    
with open(str(out_file),'w') as fo:
    for i in final_set:
          fo.write(i[1:] + '\n')

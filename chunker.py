#!/usr/bin/env python3
import sys
import os
import random
import linecache
import math
import argparse
from tqdm import tqdm
from pint import UnitRegistry

ureg = UnitRegistry()

def process(source,dest,target):

   source_filename = source.name
   lines = sum(1 for _ in tqdm(source,unit='lines'))
   size = os.stat(source_filename).st_size
   lineSize = size / (lines - 2)
   targetLines = math.ceil( target/lineSize)

   #print("Found {} lines {} bytes {} len".format(lines,size,targetLines))

   choices  = random.sample(range(2,lines-1), k=targetLines)

   with dest as out:
      out.write('[\n'.encode('utf-8'))
      for choice in tqdm(choices,unit='entries'):
         line = linecache.getline(source_filename,choice)
         out.write(line.encode('utf-8'))
         if not line.endswith(',\n'):
            print(choice)
      out.seek(-2, os.SEEK_CUR)
      out.write(']'.encode('utf-8'))

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description='Process some integers.')
   parser.add_argument('infile', nargs='?', type=argparse.FileType('r'))
   parser.add_argument('outfile', nargs='?', type=argparse.FileType('wb'))
   parser.add_argument('--size')
   params = parser.parse_args()
   print(params)
   print("Input = {}".format(params.infile.name))
   print("Output = {}".format(params.outfile.name))
   print("Size = {} ".format(ureg.parse_expression(params.size).to(ureg.bytes)))
   size = ureg.parse_expression(params.size).to(ureg.bytes)
   process(params.infile,params.outfile,size)

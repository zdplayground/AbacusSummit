"""

This script transforms a table of cosmological parameters into ini files which can be passed
as input to the Boltzmann code CLASS.

Example
=======
>>> python table_to_ini.py --help
>>> python table_to_ini.py --table README.md

Notes
=====

The table with different parameter values should follow the following format:

                       Table
------------------------------------------------------
Comments: The first line after the comments refers to the first set of cosmological params; the second
to the next, etc.
| param1 |  param2 |  param3 |  ...  |  notes  |
| ------ |  ------ |  -----  |  ---  |  ------ | 
|val1-1  |  val1-2 |  val1-3 |  ...  |LCDM base|
|val2-1  |  val2-2 |  val2-3 |  ...  |neutriono|
|  ...   |    ...  |   ...   |  ...  |   ...   |
"""
import numpy as np
import re
import sys
import argparse
import os

stringNames = ['notes','root','omega_ncdm']
commentedParam = ['notes']
rootParam = 'root'
cosmo_dir = '../Cosmologies/'
cosmology_table = cosmo_dir+'README.txt'
sigma8 = ['sigma8_m','sigma8_cb']
h = 'h'
As = 'A_s'
h_def = 0.700001
As_def = 2.00001e-9
args = {'table':cosmology_table}

def main(table=args['table']):
    # parameter names and row where they can be found
    paramNames, namesRow = list_param_names(table)
    # Create a numpy array with all entries in the table and names taken from it
    Params, numCosm = read_table(paramNames,table,namesRow)
    write_ini(Params, numCosm)
    
def list_param_names(fn,output_s8=False):
    # count total number of commented rows
    parRow = 0
    for line in open(fn):
        # if this is the start of the table, exit and parse the parameter names
        if line[:1] == '|':
            paramLine = line
            break
        parRow += 1
    # Assuming that the first line in the table has the parameter names
    try:
        paramLine
    except NameError:
        print("The table should have a line '| par1 | par2 | par3' at the beginning to extract column names!"); exit()
    paramLine = re.sub('^\|\s*', '', paramLine)
    paramLine = re.sub('\s*\|\s*$', '', paramLine)
    paramNames = re.split('\s*\|\s*',paramLine)
    
    assert rootParam in paramNames, "You are either lacking a column with the root name or it is not called "+rootParam
    # ignore the sigma8 columns as they cannot be given as input to class
    if output_s8 == False:
        for s8 in sigma8: paramNames.remove(s8)
    return paramNames, parRow

def read_table(paramNames,fn,namesRow):
    # for parameter name row and the horizontal line row
    extraRows = 2
    # This is where the sim numbers start
    startRow = namesRow + extraRows # since next row is |---|...|---|
    numRows = sum([1 for line in open(fn) if line[:1]=='|'])
    # number of parameters and cosmologies
    numParams = len(paramNames)
    numCosm = numRows-extraRows
    paramTypes = np.zeros(numParams,dtype=type)
    for i in range(numParams):
        paramTypes[i] = np.float32 if paramNames[i] not in stringNames else '<U256'

    paramsDt = np.dtype([(paramNames[i],paramTypes[i]) for i in range(numParams)])
    
    # array with all param values for all cosmologies
    Params = np.empty(numCosm,dtype=paramsDt)

    iCosm = 0
    for i,line in enumerate(open(fn)):
        if i < startRow or line[:1] != '|': continue
        # separating the individual row entries in 'line'
        line = re.sub('^\|\s*', '', line)
        line = re.sub('\s*\|\s*$', '', line)
        line = re.split('\s*\|\s*',line)
        for p,parName in enumerate(Params.dtype.names):
            if parName == h and 'TBD' in line[p]: Params[parName][iCosm] = h_def;
            elif parName == As and 'TBD' in line[p]: Params[parName][iCosm] = As_def;
            else: Params[parName][iCosm] = (line[p]);
        iCosm += 1
    return Params, numCosm

def write_ini(Params,numCosm):
    # Write files
    for iCosm in range(numCosm):
        # Create file with name root
        paramNames = Params.dtype.names
        if Params[rootParam][iCosm][-1:] != '.': Params[rootParam][iCosm] += '.'
        dir_fn = cosmo_dir
        wfn = os.path.join(dir_fn,Params[rootParam][iCosm]+'ini')
        # record all cosmologies as separate files
        with open(wfn, 'w') as f:
            for p,parName in enumerate(paramNames):
                # write the notes as a comment at the end of the file and TBD if TBD
                TBD_string = 'With A_s calibration, ' if np.abs(As_def-Params[As][iCosm]) < 1.e-16 else ''
                if parName in commentedParam: line = '# '+TBD_string+str(Params[parName][iCosm])+'\n'
                # write all the other parameter values
                else: line = parName+' = '+str(Params[parName][iCosm])+'\n'
                f.write(line)

class ArgParseFormatter(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=ArgParseFormatter)
    parser.add_argument('--table', help='table name to read from', default=cosmology_table)
    args = parser.parse_args()
    args = vars(args)
    #print(args['table'])
    exit(main(**args))

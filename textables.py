from __future__ import print_function
import __future__
import os
import sys
import time
import warnings

import numpy as np
import argparse

from astropy.stats import sigma_clip
from astropy.coordinates import SkyCoord, Angle
import astropy.units as u
from astropy.table import Table, Column, MaskedColumn
from astropy.io import ascii

import sci_utils as su
from astroML.stats import sigmaG
from astropy import constants as c
from astropy.io import ascii
from uncertainties import ufloat
from termcolor import colored

import warnings
warnings.filterwarnings('ignore')


def cli():
    """command line inputs

    Get parameters from command line

    Returns
    -------
    Arguments passed by command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Table file name to be converted to tex format with appropiriate decimal figures")
    parser.add_argument("-n", "--nsig", help="Significant figures by default", default=4, type=int)
    parser.add_argument("-j", "--JOIN", help="Join value and uncertainties in single column", action="store_true")
    args = parser.parse_args()
    return args


def formatNumber(n, digits):
    formatter = '{:.' + '{}'.format(digits) + 'f}'
    x = round(n, digits)
    return formatter.format(x)


# ==========================================
#	Get string to be printed
# ==========================================
def toprint(vv,el,eu, return_indiv=False):
    """ Transform the values into strings with appropriate number of significant figures
        according to the uncertainty in the measurement.

        Input
        -----
        vv      # Value
        el      # Lower confidence uncertainty (if assymetric)
        eu      # Upper confidence uncertainty (if assymetric)

        Optional
        --------
        return_indiv    # Boolean. True:  if you want to get individual values for the value and errors
                                   False: if you want a string with $XX \pm YY$ or $XX^{+YY}_{-ZZ}$
    """

    vv, el, eu = float(vv), float(el), float(eu)

    xl = ufloat(vv,el)
    xu = ufloat(vv,eu)
    xx = ufloat(vv,np.min([el,eu]))

    xx_str = '{:.2f}'.format(xx)[0:'{:.2f}'.format(xx).index('+/-')]
    xl_str = '{:.2f}'.format(xl)['{:.2f}'.format(xl).index('+/-')+3:]
    xu_str = '{:.2f}'.format(xu)['{:.2f}'.format(xu).index('+/-')+3:]

    error = np.min([el,eu])
    nsig = -int(np.floor(np.log10(abs(error))))+1

    xx = round(vv,nsig)
    xx_str = formatNumber(vv,nsig)

    xl = round(el,nsig)
    xl_str = formatNumber(el,nsig)

    xu = round(eu,nsig)
    xu_str = formatNumber(eu,nsig)

    if el == eu:
        value = "$"+xx_str+" \pm "+xl_str+"$"+" \t"
    else:
        value = "$"+xx_str+"^{+"+xu_str+"}_{-"+xl_str+"}$"+" \t"

    if return_indiv:
        return xx_str,xl_str,xu_str

    return value


# ======================================
# 	        MAIN
# ======================================

if __name__ == "__main__":

    """textables

    Input
    -----
    File       # Path to the CSV file that you want to convert. The file must be comma-separated
                 with column headers indicating the name of the parameter. Columns corresponding to 
                 uncertainties of each parameter (e.g., named "Param") should be named as follows:
                 - Symetric uncertainties: "eParam"
                 - Assymetric uncertainties: "elParam", "euParam" 
                 If no uncertainty colum is found matching this nomenclature, then the number of 
                 significant decimal figures used for the Param values will correspond to that specified
                 in the --nsig option (default=6 for "BJD" columns and 4 for any other).

    Optional
    --------
    --nsig      # Integer. Number of significant figures by default for columns with no corresponding uncertainties
    --join      # Boolean. Join the values and uncertainties in a single column like  $XX \pm YY$ (symetric uncertainties)
                  or $XX^{+YY}_{-ZZ}$ (asymetric uncertainties).

    Output      
    -------
    texTable    # LaTeX table obtained from the original CSV but this time including the latex format and 
                  appropriate number of significant decimal figures. The table will be written int he same 
                  directory as the original file and with the same filename but ending with ".tex" 
    """

    print("\n")
    print("======================")
    print("     TeXtables       ")
    print("======================\n")
    print("\n")

    args = cli()
    if args.JOIN == True:
        return_indiv = False
    else:
        return_indiv = True

    # Reading the file
    root,file = os.path.split(args.file)
    file_name = file.split('.')[0]
    tab = np.genfromtxt(args.file,encoding='utf-8',names=True,dtype=None,delimiter=',')
    colnames = tab.dtype.names

    # Initialize arrays
    done = []
    tab_to_print = []
    tab_to_print_colnames = []


    for col in colnames:
        if col in done: continue

        value = tab[col]
        value_str = []
        # SYMMETRIC uncertainties
        if 'e'+col in colnames:
            evalue = tab['e'+col]
            done.append('e'+col)

            evalue_str = []
            for vv,el in zip(value,evalue):
                result = toprint(vv,el,el,return_indiv=return_indiv)
                if args.JOIN:
                    xx_str = result
                    value_str.append(xx_str)
                else:
                    xx_str,el_str,_ = result
                    value_str.append(xx_str)
                    evalue_str.append(el_str)

            if args.JOIN:
                tab_to_print.append(value_str)
                tab_to_print_colnames.append(col)
            else:
                tab_to_print.append(value_str)
                tab_to_print.append(evalue_str)
                tab_to_print_colnames.append(col)
                tab_to_print_colnames.append('$\sigma_{\\rm '+col+'}$')

        # ASSYMETRIC uncertainties
        elif 'el'+col in colnames:
            elow = tab['el'+col]
            eupp = tab['eu'+col]
            done.append('el'+col)
            done.append('eu'+col)

            elow_str = []
            eupp_str = []
            for vv,el,eu in zip(value,elow,eupp):
                result = toprint(vv,el,eu,return_indiv=return_indiv)
                if args.JOIN:
                    xx_str = result
                    value_str.append(xx_str)
                else:
                    xx_str,el_str,eu_str = result
                    value_str.append(xx_str)
                    elow_str.append(el_str)
                    eupp_str.append(el_str)

            if args.JOIN:
                tab_to_print.append(value_str)
                tab_to_print_colnames.append(col)
            else:
                tab_to_print.append(value_str)
                tab_to_print.append(elow_str)
                tab_to_print.append(eupp_str)

                tab_to_print_colnames.append(col)
                tab_to_print_colnames.append('$\sigma^{\\rm l}_{\\rm '+col+'}$')
                tab_to_print_colnames.append('$\sigma^{\\rm u}_{\\rm '+col+'}$')

        # NO uncertainties
        else:
            for vv in value:
                xx = round(vv,args.nsig)
                nsig = args.nsig
                if col == 'BJD': nsig=6
                xx_str = formatNumber(vv,nsig)
                value_str.append(xx_str)
            tab_to_print.append(value_str)
            tab_to_print_colnames.append(col)


    # OUTPUT table file
    print(tab_to_print_colnames)
    t = Table(tab_to_print,names=tab_to_print_colnames)
    ascii.write(t,os.path.join(root,file_name+'.tex'),format='latex',overwrite=True)




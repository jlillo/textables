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
    vv, el, eu = float(vv), float(el), float(eu)

    xl = ufloat(vv,el)
    xu = ufloat(vv,eu)
    xx = ufloat(vv,np.min([el,eu]))

    xx_str = '{:.2f}'.format(xx)[0:'{:.2f}'.format(xx).index('+/-')]
    xl_str = '{:.2f}'.format(xl)['{:.2f}'.format(xl).index('+/-')+3:]
    xu_str = '{:.2f}'.format(xu)['{:.2f}'.format(xu).index('+/-')+3:]

    error = np.min([el,eu])
    nsig = -int(np.floor(np.log10(abs(error))))+1

    print(xx_str,xl_str,nsig)

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
    print(value)
    print('\n')

    if return_indiv:
        return xx_str,xl_str,xu_str

    return value


# ======================================
# 	        MAIN
# ======================================

if __name__ == "__main__":
    args = cli()

    root,file = os.path.split(args.file)
    file_name = file.split('.')[0]

    print("\n")
    print("======================")
    print("     TeXtables       ")
    print("======================\n")
    print("\n")

    tab = np.genfromtxt(args.file,encoding='utf-8',names=True,dtype=None,delimiter=',')

    colnames = tab.dtype.names

    done = []

    tab_to_print = []
    tab_to_print_colnames = []


    for col in colnames:
        if col in done: continue

        value = tab[col]
        value_str = []
        if 'e'+col in colnames:
            evalue = tab['e'+col]
            done = 'e'+col

            evalue_str = []

            for vv,el in zip(value,evalue):
                xx_str,el_str,_ = toprint(vv,el,el,return_indiv=True)
                value_str.append(xx_str)
                evalue_str.append(el_str)

            tab_to_print.append(value_str)
            tab_to_print.append(evalue_str)

            tab_to_print_colnames.append(col)
            tab_to_print_colnames.append('$\sigma_{\rm '+col+'}$')
        else:
            for vv in value:
                xx = round(vv,args.nsig)
                nsig = args.nsig
                if col == 'BJD': nsig=6
                xx_str = formatNumber(vv,nsig)
                value_str.append(xx_str)
            tab_to_print.append(value_str)
            tab_to_print_colnames.append(col)


    print(tab_to_print_colnames)
    t = Table(tab_to_print,names=tab_to_print_colnames)
    ascii.write(t,os.path.join(root,file_name+'.tex'),format='latex',overwrite=True)




#!/usr/bin/env python
# written spring '21 by ian k. bania
# a tuya is a type of distinctive, flat-topped, steep-sided volcano formed when
# lava erupts through a thick glacier or ice sheet, producing an object of
# similar appearence to a mesa, e.g. see hogg rock in oregon

####################
# IMPORT LIBRARIES #
####################
import mesa_reader as mr
import sys
import argparse
import numpy as np
import mpmath as mp
import math
from decimal import Decimal as D
import scipy.special as sc
from scipy.integrate import quad
from scipy.optimize import fsolve
from scipy.interpolate import interpolate
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib
import matplotlib.animation as an
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
from random import randrange
import time
import csv
import copy
import os.path
from os import path

##################
# DEFINE CLASSES #
##################
class PopIIIStar:
    '''Describes important parameters of a population III star,
    Units:
            M - Solar
            R - Solar
            L - Solar
            Tc - Kelvin (K)
            rhoc - g/cm^3
            life_star - years'''

    def __init__(self, M = 0, R = 0, L = 0, Tc = 0, rhoc = 0, life_star = 0):
        self.mass = M
        self.radius = R
        self.lum = L
        self.core_temp = Tc
        self.core_density = rhoc
        self.lifetime = life_star

    # calculates stellar volume
    def get_vol(self):
        vol = (4/3) * np.pi * (self.radius*6.96e10)**3 #in cm^3
        return vol

    def get_num_density(self):
        mn_grams = 1.6726e-24
        M = 1.9885e33 * self.mass
        n_baryon = 0.75*M/mn_grams * 1/(self.get_vol())
        return n_baryon

    def get_mass_grams(self):
        M_gram = 1.9885e33 * self.mass
        return M_gram

    def get_radius_cm(self):
        R_cm = self.radius*6.96e10
        return R_cm

    def get_vesc_surf(self):
        G  = 6.6743*10**(-8) #cgs units
        M = self.get_mass_grams()
        R = self.get_radius_cm()
        Vesc = np.sqrt(2*G*M/R) # escape velocity(cm/s) 
        return Vesc

####################
# DEFINE FUNCTIONS #
####################
def read_in_T_chi(name):
    '''reads T_chi vs M_chi data from CSV files'''
    # read DM temp from csv
    T_chi_csv = []
    m_chi_csv = []
    with open(name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            T_chi_csv.append(float(row[1]))
            m_chi_csv.append(float(row[0])*g_per_GeV)

    # now fit interpolation functions to T_chi w.r.t m_chi
    T_chi_fit = interp(m_chi_csv, T_chi_csv)
    return (m_chi_csv, T_chi_csv, T_chi_fit)

def read_in_evap(name):
    '''reads T_chi vs M_chi data from CSV files'''
    # read DM temp from csv
    m_chi_csv = []
    evap_csv = []
    with open(name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            evap_csv.append(float(row[1]))
            m_chi_csv.append(float(row[0]))

    # now fit interpolation functions to T_chi w.r.t m_chi
    return (m_chi_csv, evap_csv)

def assign_const():
    '''sets up physical constants as global parameters'''
    global m_p
    m_p = 1.6726231 * 10 ** (-24) # grams
    global g_per_GeV
    g_per_GeV = 1.783 *10 ** (-24)
    global G_cgs
    G_cgs = 6.6743*10**(-8) #cgs
    global k_cgs
    k_cgs = 1.3807 * 10 ** (-16) # cm2 g s-2 K-1
    global g_per_Msun
    g_per_Msun = 1.988*10**33
    global cm_per_Rsun
    cm_per_Rsun = 6.957*10**10 
    global eps_per_Lsun
    eps_per_Lsun = 2.599*10*-34

def mesa_dir(direc):
    arg1 = direc
    arg = arg1.split('_')
    hist= "history_" + arg[0] + ".data"
    direc = mr.MesaLogDir(log_path=arg1, history_file=hist)
    return direc

def mesa_prof(direc, profile):
    '''gets profile numbers for a MESA run'''
    # use mesa_reader to get our profile data
    prof = direc.profile_data(int(profile))

    # read info about this specific profile
    lab_mass = str(round(prof.star_mass, 3))
    year = str(round(prof.star_age, 3))
    model = str(round(prof.model_number, 3))
    mesa_lab = year + " yr, " + lab_mass + " $M_{\\odot}$, " + model
    return (prof, mesa_lab, lab_mass)

def gen_hist_labels(history):
    '''generate labels corresponding to history files'''
    labels = []
    for i in range(len(history)):
        mass = str(round(history[i].star_mass[0], 2))
        # check to see if its a DM star
        # if history[i].DM == 'True':
        #     DM = 'DM'
        # else:
        #     DM = 'no DM'

        # combine the elements
        # labels.append(mass + " $M_{\\odot}$, " + DM)
        labels.append(mass + " $M_{\\odot}$, DM")

    # return our list of labels
    return labels

def gen_profs(dirs):
    '''get the indices of profiles during various interesting points in the stars evolution '''
    # 2d array
    profs = []

    # run thru each star we want to plot
    for i in range(len(dirs)):
        index = mr.MesaProfileIndex(file_name=dirs[i] + '/profiles.index')
        prof_nums = index.model_numbers

        # data for this profile
        profs.append(prof_nums)
    return profs

def progbarinit(barlen = 20):
    '''prints a simple progress bar'''
    # sys.stdout.write("[%s]" % (" " * barlen))
    # sys.stdout.flush()
    # # return to start of line, after '['
    # sys.stdout.write("\b" * (barlen+1))

def progbar():
    '''update the bar'''
    # sys.stdout.write("-")
    # sys.stdout.flush()

def progbarend():
    '''this ends the progress bar'''
    # sys.stdout.write("]\n")

def save_plt(plt, name, args):
    '''makes modifications to plot with any of the force options, and saves it'''
    # tight margins
    plt.tight_layout()

    # check axes params
    if args.xlog:
        plt.xscale('log')
    if args.ylog:
        plt.yscale('log')
    if args.xlin:
        plt.xscale('linear')
    if args.ylin:
        plt.yscale('linear')

    # have we forced any axes?
    if 'args.xaxis' in globals():
        btm = args.xaxis[0]
        top = args.xaxis[1]
        plt.xlin(xbtm, xtop)

    if 'args.yaxis' in globals():
        btm = args.yaxis[0]
        top = args.yaxis[1]
        plt.xlin(btm, top)

    # check file type params
    if args.PDF:
        plt.savefig(name+ ".pdf")
    else:
        plt.savefig(name + ".png", dpi = 400)
    plt.clf()

def aninit():
    line.set_data([], [])
    return line,

########
# MAIN #
########
def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.MetavarTypeHelpFormatter)
    parser.add_argument("-D", "--dir", nargs='+', help="directory or directories containing data files", type=str)
    parser.add_argument("--DMevo", help="plot DM params over time", action='store_true')
    parser.add_argument("--DMheat", help="plot radial DM heating profile", action='store_true')
    parser.add_argument("--DMprof", help="plot radial DM profile", action='store_true')
    parser.add_argument("--cpu", help="plot star time versus wall time", action='store_true')
    parser.add_argument("--HR", help="plot an HR diagram", action='store_true')
    parser.add_argument("--dMdt", help="plot total mass over time", action='store_true')
    parser.add_argument("--dRdt", help="plot total radius over time", action='store_true')
    parser.add_argument("--dLdt", help="plot total luminosity over time, by source", action='store_true')
    parser.add_argument("--dEddMaxdt", help="plot maximum Eddington factor over time", action='store_true')
    parser.add_argument("--rho", help="plot radial density profile", action='store_true')
    parser.add_argument("--P", help="plot radial pressure profile", action='store_true')
    parser.add_argument("--T", help="plot radial temperature profile", action='store_true')
    parser.add_argument("--L", help="plot radial luminosity profile, by source", action='store_true')
    parser.add_argument("--Edd", help="plot radial Eddington factor profile", action='store_true')
    parser.add_argument("--beta", help="plot radial beta (P_gas/P) profile", action='store_true')
    parser.add_argument("--XYZ", help="plot radial composition profile", action='store_true')
    parser.add_argument("-n", "--number", help="how many profiles to plot, equispaced by interest", type=int, default=0)
    # parser.add_argument("--range", nargs=2, help="time range of profiles to plot, min and max in [yr]", type=float)
    parser.add_argument("--Arho", help="animate radial density profile", action='store_true')
    parser.add_argument("--AP", help="animate radial pressure profile", action='store_true')
    parser.add_argument("--AT", help="animate radial temperature profile", action='store_true')
    parser.add_argument("--AL", help="animate radial luminosity profile, by source", action='store_true')
    parser.add_argument("--AEdd", help="animate radial Eddington factor profile", action='store_true')
    parser.add_argument("--Abeta", help="animate radial beta (P_gas/P) profile", action='store_true')
    parser.add_argument("--AXYZ", help="animate radial composition profile", action='store_true')
    parser.add_argument("--poly", help="add a polytrope with specified index to plots", type=float)
    parser.add_argument("--Rnorm", help="normalize all radial profiles to R_star", action='store_true')
    parser.add_argument("--dM", help="use enclosed mass instead of radius for all profiles", action='store_true')
    parser.add_argument("--Mnorm", help="use with --dM, normalize all profiles to M_star", action='store_true')
    parser.add_argument("--dMstar", help="use M_star instead of time for evolution plots", action='store_true')
    parser.add_argument("--no-annotate", help="turn all anotations off", action='store_true')
    parser.add_argument("-f", "--filename", help="filename for the plots to be produced", type=str)
    parser.add_argument("-d", "--dark", help="use dark theme for plots", action='store_true')
    parser.add_argument("-p", "--plain", help="use plain theme for plots", action='store_true')
    parser.add_argument("-x", "--xaxis", nargs=2, help="manually set x axis, min and max", type=float)
    parser.add_argument("-y", "--yaxis", nargs=2, help="manually set y axis, min and max", type=float)
    parser.add_argument("--xlog", help="force log scale on x axis", action='store_true')
    parser.add_argument("--ylog", help="force log scale on y axis", action='store_true')
    parser.add_argument("--xlin", help="force lin scale on x axis", action='store_true')
    parser.add_argument("--ylin", help="force lin scale on y axis", action='store_true')
    parser.add_argument("--PDF", help="produce PDFs of the plots", action='store_true')
    args = parser.parse_args()

    # print
    readouts = ["adding hidden agendas...",
        "dispatching feral hogs...",
        "compressing fish files...",
        "depositing slush funds...",
        "increasing magmafacation...",
        "reticulating splines...",
        "iterating cellular automata...",
        "graphing whale migration...",
        "calculating llama expectoration trajectory...",
        "constructing additional pylons..."]
    rand = randrange(10)
    print(readouts[rand])

    # assign various physical constants as global variables
    assign_const()

    # set up some plotting stuff
    # fig = plt.figure()
    fig = plt.figure(figsize = (24,16))
    # plt.style.use('fast')
    palette = plt.get_cmap('magma')
    vir = plt.get_cmap('viridis')
    fig = plt.figure()
    ax = plt.axes()
    global line
    line, = ax.plot([], [], lw=3)

    # theme
    if args.dark:
        plt.style.use('dark_background')
        if args.plain:
            print("cannot plot two themes at once...")
            exit
    elif args.plain:
        plt.style.use('default')
    else:
        plt.style.use('Solarize_Light2')

    # filename handling
    if args.filename:
        # custom file name
        filename = args.filename
    else:
        # or just concatinate all the directory names
        filename = ''.join(args.dir)

    # make our history list
    if args.dir:
        print("fetching history files...")
        history = []
        mrdirs = []
        progbarinit(len(args.dir))
        for i in range(len(args.dir)):
            # progress bar
            progbar()

            # pick up the data from history files
            history.append(mr.MesaData(args.dir[i] + '/history_' + args.dir[i] + '.data'))

            # generate all the mesa reader objects we need
            mrdirs.append(mesa_dir(args.dir[i]))
        progbarend()

        # create our legend labels
        print("generating history labels...")
        hist_lab = gen_hist_labels(history)

        # find the interesting profile indices
        print("fetching profile indices...")
        profs = gen_profs(args.dir)

    # hamburger and rustal
    if args.HR:
        progbarinit(len(history))
        for i in range(len(history)):
            # make actual plot
            plt.plot(history[i].log_Teff, history[i].log_L,
                    color=vir(i / len(history)),
                    ls = '-',
                    linewidth=2,
                    label=hist_lab[i])
            progbar()
        progbarend()

        # add ZAMS anotation
        hit_ZAMS = False
        mass100 = False
        mass200 = False
        mass300 = False
        mass400 = False
        mass500 = False
        mass600 = False
        mass700 = False
        mass800 = False
        mass900 = False
        mass950 = False
        mass1000 = False

        # for all timesteps in a star
        for j in range(len(history[i].star_age)):
            # write to stdout
            l = len(history[i].star_age)
            a = j
            progbar()

            # annotations
            nucpercent = 10**(history[i].log_Lnuc[j]) / 10**(history[i].log_L[j])
            if nucpercent > 0.900 and hit_ZAMS == False and history[i].star_age[j] > 50.0:
                plt.scatter(history[i].log_Teff[j], history[i].log_L[j], c="#E0115F", s=10)
                plt.annotate(str(round(history[i].star_age[j]))+" yr " + str(round(history[i].radius[j],2))+" $R_{\odot}$", (history[i].log_Teff[j], history[i].log_L[j]))
                hit_ZAMS = True

            if abs(history[i].star_mass[j] - 100.0) < 0.1 and mass100 == False:
                plt.scatter(history[i].log_Teff[j], history[i].log_L[j], color=palette(2/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].log_Teff[j], history[i].log_L[j]))
                mass100 = True

            if abs(history[i].star_mass[j] - 200.0) < 0.1 and mass200 == False:
                plt.scatter(history[i].log_Teff[j], history[i].log_L[j], color=palette(3/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].log_Teff[j], history[i].log_L[j]))
                mass200 = True

            if abs(history[i].star_mass[j] - 300.0) < 0.1 and mass300 == False:
                plt.scatter(history[i].log_Teff[j], history[i].log_L[j], color=palette(4/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].log_Teff[j], history[i].log_L[j]))
                mass300 = True

            if abs(history[i].star_mass[j] - 400.0) < 0.1 and mass400 == False:
                plt.scatter(history[i].log_Teff[j], history[i].log_L[j], color=palette(5/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].log_Teff[j], history[i].log_L[j]))
                mass400 = True

            if abs(history[i].star_mass[j] - 500.0) < 0.1 and mass500 == False:
                plt.scatter(history[i].log_Teff[j], history[i].log_L[j], color=palette(6/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].log_Teff[j], history[i].log_L[j]))
                mass500 = True

            if abs(history[i].star_mass[j] - 600.0) < 0.1 and mass600 == False:
                plt.scatter(history[i].log_Teff[j], history[i].log_L[j], color=palette(7/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].log_Teff[j], history[i].log_L[j]))
                mass600 = True

            if abs(history[i].star_mass[j] - 700.0) < 0.1 and mass700 == False:
                plt.scatter(history[i].log_Teff[j], history[i].log_L[j], color=palette(8/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].log_Teff[j], history[i].log_L[j]))
                mass700 = True

            if abs(history[i].star_mass[j] - 800.0) < 0.1 and mass800 == False:
                plt.scatter(history[i].log_Teff[j], history[i].log_L[j], color=palette(9/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].log_Teff[j], history[i].log_L[j]))
                mass800 = True

            if abs(history[i].star_mass[j] - 900.0) < 0.1 and mass900 == False:
                plt.scatter(history[i].log_Teff[j], history[i].log_L[j], color=palette(10/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].log_Teff[j], history[i].log_L[j]))
                mass900 = True

            if abs(history[i].star_mass[j] - 950.0) < 0.1 and mass950 == False:
                plt.scatter(history[i].log_Teff[j], history[i].log_L[j], color=palette(10/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].log_Teff[j], history[i].log_L[j]))
                mass950 = True

            if abs(history[i].star_mass[j] - 1000.0) < 0.1 and mass1000 == False:
                plt.scatter(history[i].log_Teff[j], history[i].log_L[j], color=palette(11/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].log_Teff[j], history[i].log_L[j]))
                mass1000 = True

        # make the plot
        plt.title("HR Diagram: " + filename)
        plt.legend()
        plt.gca().invert_xaxis()
        plt.ylabel('log($L$) [$L_{\odot}$]')
        plt.xlabel('log($T_{eff}$) [K]')
        name = filename + "_HR" 
        save_plt(plt, name, args)

    # radical
    if args.dRdt:
        progbarinit(len(history))
        for i in range(len(history)):
            # make actual plot
            plt.plot(history[i].star_age, history[i].radius, color=vir(i / len(history)), ls = '-', linewidth=2, label=hist_lab[i])
            progbar()
        progbarend()

        # add ZAMS anotation
        mass100 = False
        mass200 = False
        mass300 = False
        mass400 = False
        mass500 = False
        mass600 = False
        mass700 = False
        mass800 = False
        mass900 = False
        mass1000 = False

        # for all timesteps in a star
        progbarinit(len(history))
        for j in range(len(history[i].star_age)):
            # write to stdout
            l = len(history[i].star_age)
            a = j
            progbar()

            # annotations
            if abs(history[i].star_mass[j] - 100.0) < 0.1 and mass100 == False:
                plt.scatter(history[i].star_age[j], history[i].radius[j], color=palette(2/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].radius[j]))
                mass100 = True

            if abs(history[i].star_mass[j] - 200.0) < 0.1 and mass200 == False:
                plt.scatter(history[i].star_age[j], history[i].radius[j], color=palette(3/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].radius[j]))
                mass200 = True

            if abs(history[i].star_mass[j] - 300.0) < 0.1 and mass300 == False:
                plt.scatter(history[i].star_age[j], history[i].radius[j], color=palette(4/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].radius[j]))
                mass300 = True

            if abs(history[i].star_mass[j] - 400.0) < 0.1 and mass400 == False:
                plt.scatter(history[i].star_age[j], history[i].radius[j], color=palette(5/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].radius[j]))
                mass400 = True

            if abs(history[i].star_mass[j] - 500.0) < 0.1 and mass500 == False:
                plt.scatter(history[i].star_age[j], history[i].radius[j], color=palette(6/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].radius[j]))
                mass500 = True

            if abs(history[i].star_mass[j] - 600.0) < 0.1 and mass600 == False:
                plt.scatter(history[i].star_age[j], history[i].radius[j], color=palette(7/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].radius[j]))
                mass600 = True

            if abs(history[i].star_mass[j] - 700.0) < 0.1 and mass700 == False:
                plt.scatter(history[i].star_age[j], history[i].radius[j], color=palette(8/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].radius[j]))
                mass700 = True

            if abs(history[i].star_mass[j] - 800.0) < 0.1 and mass800 == False:
                plt.scatter(history[i].star_age[j], history[i].radius[j], color=palette(9/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].radius[j]))
                mass800 = True

            if abs(history[i].star_mass[j] - 900.0) < 0.1 and mass900 == False:
                plt.scatter(history[i].star_age[j], history[i].radius[j], color=palette(10/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].radius[j]))
                mass900 = True

            if abs(history[i].star_mass[j] - 1000.0) < 0.1 and mass1000 == False:
                plt.scatter(history[i].star_age[j], history[i].radius[j], color=palette(11/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].radius[j]))
                mass1000 = True

        # make the plot
        progbarend()
        plt.title("Radius Over Time: " + filename)
        plt.legend()
        plt.ylabel('Radius [$R_{\odot}$]')
        plt.yscale('log')
        plt.xlabel('Age [yr]')
        name = filename + "_dRdt" 
        save_plt(plt, name, args)

    # luminary
    if args.dLdt:
        progbarinit(len(history))
        for i in range(len(history)):
            # make actual plot
            plt.plot(history[i].star_age, history[i].luminosity,
                    color=vir(i / len(history)),
                    ls = '-',
                    linewidth=2,
                    label=hist_lab[i])
            plt.plot(history[i].star_age, 10**history[i].log_Lnuc,
                    color=vir(i / len(history)),
                    ls = ':',
                    linewidth=2,
                    label='nuclear')
            plt.plot(history[i].star_age, history[i].DM_energy_rate/eps_per_Lsun,
                    color=vir(i / len(history)),
                    ls = '--',
                    linewidth=2,
                    label='DM')
            progbar()
        progbarend()

        # add ZAMS anotation
        mass100 = False
        mass200 = False
        mass300 = False
        mass400 = False
        mass500 = False
        mass600 = False
        mass700 = False
        mass800 = False
        mass900 = False
        mass1000 = False

        # for all timesteps in a star
        progbarinit(len(history))
        for j in range(len(history[i].star_age)):
            # write to stdout
            l = len(history[i].star_age)
            a = j
            progbar()

            # annotations
            if abs(history[i].star_mass[j] - 100.0) < 0.1 and mass100 == False:
                plt.scatter(history[i].star_age[j], history[i].luminosity[j], color=palette(2/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].luminosity[j]))
                mass100 = True

            if abs(history[i].star_mass[j] - 200.0) < 0.1 and mass200 == False:
                plt.scatter(history[i].star_age[j], history[i].luminosity[j], color=palette(3/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].luminosity[j]))
                mass200 = True

            if abs(history[i].star_mass[j] - 300.0) < 0.1 and mass300 == False:
                plt.scatter(history[i].star_age[j], history[i].luminosity[j], color=palette(4/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].luminosity[j]))
                mass300 = True

            if abs(history[i].star_mass[j] - 400.0) < 0.1 and mass400 == False:
                plt.scatter(history[i].star_age[j], history[i].luminosity[j], color=palette(5/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].luminosity[j]))
                mass400 = True

            if abs(history[i].star_mass[j] - 500.0) < 0.1 and mass500 == False:
                plt.scatter(history[i].star_age[j], history[i].luminosity[j], color=palette(6/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].luminosity[j]))
                mass500 = True

            if abs(history[i].star_mass[j] - 600.0) < 0.1 and mass600 == False:
                plt.scatter(history[i].star_age[j], history[i].luminosity[j], color=palette(7/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].luminosity[j]))
                mass600 = True

            if abs(history[i].star_mass[j] - 700.0) < 0.1 and mass700 == False:
                plt.scatter(history[i].star_age[j], history[i].luminosity[j], color=palette(8/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].luminosity[j]))
                mass700 = True

            if abs(history[i].star_mass[j] - 800.0) < 0.1 and mass800 == False:
                plt.scatter(history[i].star_age[j], history[i].luminosity[j], color=palette(9/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].luminosity[j]))
                mass800 = True

            if abs(history[i].star_mass[j] - 900.0) < 0.1 and mass900 == False:
                plt.scatter(history[i].star_age[j], history[i].luminosity[j], color=palette(10/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].luminosity[j]))
                mass900 = True

            if abs(history[i].star_mass[j] - 1000.0) < 0.1 and mass1000 == False:
                plt.scatter(history[i].star_age[j], history[i].luminosity[j], color=palette(11/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].luminosity[j]))
                mass1000 = True

        # make the plot
        progbarend()
        plt.title("Luminosity Over Time: " + filename)
        plt.legend()
        plt.ylabel('Luminosity [$L_{\odot}$]')
        plt.yscale('log')
        plt.xlabel('Age [yr]')
        name = filename + "_dLdt" 
        save_plt(plt, name, args)

    # massif
    if args.dMdt:
        progbarinit(len(history))
        for i in range(len(history)):
            # make actual plot
            plt.plot(history[i].star_age, history[i].star_mass, color=vir(i / len(history)), ls = '-', linewidth=2, label=hist_lab[i])
            progbar()
        progbarend()

        # add ZAMS anotation
        rad1 = False
        rad3 = False
        rad5 = False
        rad10 = False
        rad30 = False
        rad50 = False
        rad100 = False
        rad300 = False
        rad500 = False
        rad1000 = False

        # for all timesteps in a star
        progbarinit(len(history))
        for j in range(len(history[i].star_age)):
            # write to stdout
            l = len(history[i].star_age)
            a = j
            progbar()

            # annotations
            if abs(history[i].radius[j] - 1.0) < 0.1 and rad1 == False:
                plt.scatter(history[i].star_age[j], history[i].star_mass[j], color=palette(2/12), s=20)
                plt.annotate(str(round(history[i].radius[j])) + " $R_{\odot}$", (history[i].star_age[j], history[i].star_mass[j]))
                rad1 = True

            if abs(history[i].radius[j] - 3.0) < 0.1 and rad3 == False:
                plt.scatter(history[i].star_age[j], history[i].star_mass[j], color=palette(3/12), s=20)
                plt.annotate(str(round(history[i].radius[j])) + " $R_{\odot}$", (history[i].star_age[j], history[i].star_mass[j]))
                rad1 = True

            if abs(history[i].radius[j] - 5.0) < 0.1 and rad5 == False:
                plt.scatter(history[i].star_age[j], history[i].star_mass[j], color=palette(4/12), s=20)
                plt.annotate(str(round(history[i].radius[j])) + " $R_{\odot}$", (history[i].star_age[j], history[i].star_mass[j]))
                rad5 = True

            if abs(history[i].radius[j] - 10.0) < 0.1 and rad10 == False:
                plt.scatter(history[i].star_age[j], history[i].star_mass[j], color=palette(5/12), s=20)
                plt.annotate(str(round(history[i].radius[j])) + " $R_{\odot}$", (history[i].star_age[j], history[i].star_mass[j]))
                rad10 = True

            if abs(history[i].radius[j] - 30.0) < 0.1 and rad30 == False:
                plt.scatter(history[i].star_age[j], history[i].star_mass[j], color=palette(6/12), s=20)
                plt.annotate(str(round(history[i].radius[j])) + " $R_{\odot}$", (history[i].star_age[j], history[i].star_mass[j]))
                rad30 = True

            if abs(history[i].radius[j] - 50.0) < 0.1 and rad50 == False:
                plt.scatter(history[i].star_age[j], history[i].star_mass[j], color=palette(7/12), s=20)
                plt.annotate(str(round(history[i].radius[j])) + " $R_{\odot}$", (history[i].star_age[j], history[i].star_mass[j]))
                rad50 = True

            if abs(history[i].radius[j] - 100.0) < 0.1 and rad100 == False:
                plt.scatter(history[i].star_age[j], history[i].star_mass[j], color=palette(8/12), s=20)
                plt.annotate(str(round(history[i].radius[j])) + " $R_{\odot}$", (history[i].star_age[j], history[i].star_mass[j]))
                rad100 = True

            if abs(history[i].radius[j] - 300.0) < 0.1 and rad300 == False:
                plt.scatter(history[i].star_age[j], history[i].star_mass[j], color=palette(9/12), s=20)
                plt.annotate(str(round(history[i].radius[j])) + " $R_{\odot}$", (history[i].star_age[j], history[i].star_mass[j]))
                rad300 = True

            if abs(history[i].radius[j] - 500.0) < 0.1 and rad500 == False:
                plt.scatter(history[i].star_age[j], history[i].star_mass[j], color=palette(10/12), s=20)
                plt.annotate(str(round(history[i].radius[j])) + " $R_{\odot}$", (history[i].star_age[j], history[i].star_mass[j]))
                rad500 = True

            if abs(history[i].radius[j] - 1000.0) < 0.1 and rad1000 == False:
                plt.scatter(history[i].star_age[j], history[i].star_mass[j], color=palette(11/12), s=20)
                plt.annotate(str(round(history[i].radius[j])) + " $R_{\odot}$", (history[i].star_age[j], history[i].star_mass[j]))
                rad1000 = True

        # make the plot
        progbarend()
        plt.title("Mass Over Time: " + filename)
        plt.legend()
        plt.ylabel('Mass [$M_{\odot}$]')
        plt.yscale('log')
        plt.xlabel('Age [yr]')
        name = filename + "_dMdt" 
        save_plt(plt, name, args)

    # dense
    if args.rho:
        for j in range(len(mrdirs)):
            # how many profiles do we want to plot
            if args.number == 0:
                num = len(profs[j])
            else:
                num = args.number

            # loop thru different profile files
            progbarinit(len(profs[j]))
            for i in range(len(profs[j])):
                # progress bar
                progbar()

                # is this one we want to plot?
                spacing = round(len(profs[j])/num)

                # modulo
                if i % spacing == 0:
                    # get profile info from MESA reader
                    dat, lab, mmm = mesa_prof(mrdirs[j], profs[j][i])

                    # make actual plot
                    plt.plot(dat.radius, 10**(dat.logRho),
                            color=vir(i / len(profs)),
                            ls = '-',
                            linewidth=1,
                            label=lab)

                    # make progress bar

        # plot the plot
        progbarend()
        plt.title("Density Profile: " + filename)
        plt.legend()
        plt.ylabel('Density [g cm$^{-3}$]')
        plt.yscale('log')
        plt.xlabel('Radius [$R_{\odot}$]')
        name = filename + "_rho" 
        save_plt(plt, name, args)

    # crock pot
    if args.P:
        for j in range(len(mrdirs)):
            # how many profiles do we want to plot
            if args.number == 0:
                num = len(profs[j])
            else:
                num = args.number

            # loop thru different profile files
            progbarinit(len(profs[j]))
            for i in range(len(profs[j])):
                # is this one we want to plot?
                spacing = round(len(profs[j])/num)

                # modulo
                if i % spacing == 0:
                    # get profile info from MESA reader
                    dat, lab, mmm = mesa_prof(mrdirs[j], profs[j][i])

                    # make actual plot
                    plt.plot(dat.radius, dat.pressure,
                            color=vir(i / len(profs)),
                            ls = '-',
                            linewidth=1,
                            label=lab)

                    # make progress bar
                    progbar()

        # plot the plot
        progbarend()
        plt.title("Pressure Profile: " + filename)
        plt.legend()
        plt.ylabel('Pressure [g cm$^{-1}$ s$^{-2}$]')
        plt.yscale('log')
        plt.xlabel('Radius [$R_{\odot}$]')
        name = filename + "_P" 
        save_plt(plt, name, args)

    # temp
    if args.T:
        for j in range(len(mrdirs)):
            # how many profiles do we want to plot
            if args.number == 0:
                num = len(profs[j])
            else:
                num = args.number

            # loop thru different profile files
            progbarinit(len(profs[j]))
            for i in range(len(profs[j])):
                # is this one we want to plot?
                spacing = round(len(profs[j])/num)

                # modulo
                if i % spacing == 0:
                    # get profile info from MESA reader
                    dat, lab, mmm = mesa_prof(mrdirs[j], profs[j][i])

                    # make actual plot
                    plt.plot(dat.radius, dat.temperature,
                            color=vir(i / len(profs)),
                            ls = '-',
                            linewidth=1,
                            label=lab)

                    # make progress bar
                    progbar()

        # plot the plot
        progbarend()
        plt.title("Temperature Profile: " + filename)
        plt.legend()
        plt.ylabel('Temperature [K]')
        plt.yscale('log')
        plt.xlabel('Radius [$R_{\odot}$]')
        name = filename + "_T" 
        save_plt(plt, name, args)

    # lums
    if args.L:
        for j in range(len(mrdirs)):
            # how many profiles do we want to plot
            if args.number == 0:
                num = len(profs[j])
            else:
                num = args.number

            # loop thru different profile files
            progbarinit(len(profs[j]))
            for i in range(len(profs[j])):
                # is this one we want to plot?
                spacing = round(len(profs[j])/num)

                # modulo
                if i % spacing == 0:
                    # get profile info from MESA reader
                    dat, lab, mmm = mesa_prof(mrdirs[j], profs[j][i])

                    # make actual plot
                    plt.plot(dat.radius, dat.luminosity,
                            color=vir(i / len(profs)),
                            ls = '-',
                            linewidth=1,
                            label=lab)
                    plt.plot(dat.radius, dat.extra_L,
                            color=vir(i / len(profs)),
                            ls = '--',
                            linewidth=1,
                            label="extra")
                    plt.plot(dat.radius, dat.luminosity - dat.extra_L,
                            color=vir(i / len(profs)),
                            ls = ':',
                            linewidth=1,
                            label="other")

                    # make progress bar
                    progbar()

        # plot the plot
        progbarend()
        plt.title("Luminosity Profile: " + filename)
        plt.legend()
        plt.ylabel('Luminosity [$L_{\odot}$]')
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('Radius [$R_{\odot}$]')
        name = filename + "_L" 
        save_plt(plt, name, args)

    # edd
    if args.Edd:
        for j in range(len(mrdirs)):
            # how many profiles do we want to plot
            if args.number == 0:
                num = len(profs[j])
            else:
                num = args.number

            # loop thru different profile files
            progbarinit(len(profs[j]))
            for i in range(len(profs[j])):
                # is this one we want to plot?
                spacing = round(len(profs[j])/num)

                # modulo
                if i % spacing == 0:
                    # get profile info from MESA reader
                    dat, lab, mmm = mesa_prof(mrdirs[j], profs[j][i])

                    # make actual plot
                    plt.plot(dat.radius, dat.luminosity/(10**(dat.log_L_div_Ledd)),
                            color=vir(i / len(profs)),
                            ls = '-',
                            linewidth=1,
                            label=lab)

                    # make progress bar
                    progbar()

        # plot the plot
        progbarend()
        plt.title("Eddintgon Factor Profile: " + filename)
        plt.legend()
        plt.ylabel('Eddington Factor $(\\frac{L(r)}{L_{edd}(r)})$')
        plt.yscale('log')
        plt.xlabel('Radius [$R_{\odot}$]')
        name = filename + "_Edd" 
        save_plt(plt, name, args)

    # beta
    if args.beta:
        for j in range(len(mrdirs)):
            # how many profiles do we want to plot
            if args.number == 0:
                num = len(profs[j])
            else:
                num = args.number

            # loop thru different profile files
            progbarinit(len(profs[j]))
            for i in range(len(profs[j])):
                # is this one we want to plot?
                spacing = round(len(profs[j])/num)

                # modulo
                if i % spacing == 0:
                    # get profile info from MESA reader
                    dat, lab, mmm = mesa_prof(mrdirs[j], profs[j][i])

                    # make actual plot
                    plt.plot(dat.radius, dat.pgas/dat.pressure,
                            color=vir(i / len(profs)),
                            ls = '-',
                            linewidth=1,
                            label=lab)

                    # make progress bar
                    progbar()

        # plot the plot
        progbarend()
        plt.title("Beta Profile: " + filename)
        plt.legend()
        plt.ylabel('$\\beta ~ (\\frac{P_{gas}(r)}{P(r)})$')
        plt.xlabel('Radius [$R_{\odot}$]')
        name = filename + "_beta" 
        save_plt(plt, name, args)

    # composition
    if args.XYZ:
        for j in range(len(mrdirs)):
            # how many profiles do we want to plot
            if args.number == 0:
                num = len(profs[j])
            else:
                num = args.number

            # loop thru different profile files
            progbarinit(len(profs[j]))
            for i in range(len(profs[j])):
                # is this one we want to plot?
                spacing = round(len(profs[j])/num)

                # modulo
                if i % spacing == 0:
                    # get profile info from MESA reader
                    dat, lab, mmm = mesa_prof(mrdirs[j], profs[j][i])

                    # make actual plot
                    plt.plot(dat.radius, dat.x_mass_fraction_H,
                            color=vir(i / len(profs)),
                            ls = '-',
                            linewidth=1,
                            label="H, " + lab)
                    plt.plot(dat.radius, dat.y_mass_fraction_He,
                            color=vir(i / len(profs)),
                            ls = '--',
                            linewidth=1,
                            label="He")
                    plt.plot(dat.radius, dat.z_mass_fraction_metals,
                            color=vir(i / len(profs)),
                            ls = ':',
                            linewidth=1,
                            label="Z")

                    # make progress bar
                    progbar()

        # plot the plot
        progbarend()
        plt.title("Composition Profile: " + filename)
        plt.legend()
        plt.ylabel('Composition Fraction')
        plt.yscale('log')
        plt.xlabel('Radius [$R_{\odot}$]')
        plt.ylim(bottom=10**(-10))
        name = filename + "_XYZ" 
        save_plt(plt, name, args)

    # DM evolution
    if args.DMevo:
        progbarinit(len(history))
        for i in range(len(history)):
            # make actual plot
            plt.plot(history[i].star_age, history[i].DM_energy_rate,
                    color=vir(i / len(history)),
                    ls = '-',
                    linewidth=2,
                    label=hist_lab[i] + ' $L_\\chi$ [ergs/s]')
            plt.plot(history[i].star_age, history[i].C_tot,
                    color=vir(i / len(history)),
                    ls = '--',
                    linewidth=2,
                    label='$C_{tot}$ [s$^{-1}$]')
            plt.plot(history[i].star_age, history[i].N_chi,
                    color=vir(i / len(history)),
                    ls = ':',
                    linewidth=2,
                    label='$N_\\chi$')
            progbar()

        # add ZAMS anotation
        progbarend()
        mass100 = False
        mass200 = False
        mass300 = False
        mass400 = False
        mass500 = False
        mass600 = False
        mass700 = False
        mass800 = False
        mass900 = False
        mass1000 = False

        # for all timesteps in a star
        progbarinit(len(history))
        for j in range(len(history[i].star_age)):
            # write to stdout
            l = len(history[i].star_age)
            a = j
            progbar()

            # annotations
            if abs(history[i].star_mass[j] - 100.0) < 0.1 and mass100 == False:
                plt.scatter(history[i].star_age[j], history[i].C_tot[j], color=palette(2/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].C_tot[j]))
                mass100 = True

            if abs(history[i].star_mass[j] - 200.0) < 0.1 and mass200 == False:
                plt.scatter(history[i].star_age[j], history[i].C_tot[j], color=palette(3/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].C_tot[j]))
                mass200 = True

            if abs(history[i].star_mass[j] - 300.0) < 0.1 and mass300 == False:
                plt.scatter(history[i].star_age[j], history[i].C_tot[j], color=palette(4/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].C_tot[j]))
                mass300 = True

            if abs(history[i].star_mass[j] - 400.0) < 0.1 and mass400 == False:
                plt.scatter(history[i].star_age[j], history[i].C_tot[j], color=palette(5/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].C_tot[j]))
                mass400 = True

            if abs(history[i].star_mass[j] - 500.0) < 0.1 and mass500 == False:
                plt.scatter(history[i].star_age[j], history[i].C_tot[j], color=palette(6/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].C_tot[j]))
                mass500 = True

            if abs(history[i].star_mass[j] - 600.0) < 0.1 and mass600 == False:
                plt.scatter(history[i].star_age[j], history[i].C_tot[j], color=palette(7/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].C_tot[j]))
                mass600 = True

            if abs(history[i].star_mass[j] - 700.0) < 0.1 and mass700 == False:
                plt.scatter(history[i].star_age[j], history[i].C_tot[j], color=palette(8/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].C_tot[j]))
                mass700 = True

            if abs(history[i].star_mass[j] - 800.0) < 0.1 and mass800 == False:
                plt.scatter(history[i].star_age[j], history[i].C_tot[j], color=palette(9/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].C_tot[j]))
                mass800 = True

            if abs(history[i].star_mass[j] - 900.0) < 0.1 and mass900 == False:
                plt.scatter(history[i].star_age[j], history[i].C_tot[j], color=palette(10/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].C_tot[j]))
                mass900 = True

            if abs(history[i].star_mass[j] - 1000.0) < 0.1 and mass1000 == False:
                plt.scatter(history[i].star_age[j], history[i].C_tot[j], color=palette(11/12), s=20)
                plt.annotate(str(round(history[i].star_mass[j])) + " $M_{\odot}$", (history[i].star_age[j], history[i].C_tot[j]))
                mass1000 = True

        # make the plot
        progbarend()
        plt.title("Dark Matter Over Time: " + filename)
        plt.legend()
        plt.yscale('log')
        plt.xlabel('Age [yr]')
        name = filename + "_DMevo" 
        save_plt(plt, name, args)

    # DM profile
    if args.DMheat:
        for j in range(len(mrdirs)):
            # how many profiles do we want to plot
            if args.number == 0:
                num = len(profs[j])
            else:
                num = args.number

            # loop thru different profile files
            progbarinit(len(profs[j]))
            for i in range(len(profs[j])):
                # is this one we want to plot?
                spacing = round(len(profs[j])/num)

                # modulo
                if i % spacing == 0:
                    # get profile info from MESA reader
                    dat, lab, mmm = mesa_prof(mrdirs[j], profs[j][i])

                    # make actual plot
                    plt.plot(dat.radius, dat.extra_heat,
                            color=vir(i / len(profs)),
                            ls = '-',
                            linewidth=1,
                            label=lab)

                    # make progress bar
                    progbar()

        # plot the plot
        progbarend()
        plt.title("DM Heat Profile: " + filename)
        plt.legend()
        plt.yscale('log')
        plt.xscale('log')
        plt.ylabel('$Q_{\\chi}(r)$ [ergs/s/g]')
        plt.xlabel('Radius [$R_{\odot}$]')
        plt.ylim(bottom=10**(-14))
        name = filename + "_DMheat" 
        save_plt(plt, name, args)

    if args.DMprof:
        for j in range(len(mrdirs)):
            # how many profiles do we want to plot
            if args.number == 0:
                num = len(profs[j])
            else:
                num = args.number

            # loop thru different profile files
            progbarinit(len(profs[j]))
            for i in range(len(profs[j])):
                # is this one we want to plot?
                spacing = round(len(profs[j])/num)

                # modulo
                if i % spacing == 0:
                    # get profile info from MESA reader
                    dat, lab, mmm = mesa_prof(mrdirs[j], profs[j][i])

                    # make actual plot
                    plt.plot(dat.radius, np.sqrt(dat.n_chi2),
                            color=vir(i / len(profs)),
                            ls = ':',
                            linewidth=1,
                            label=lab)

                    # make progress bar
                    progbar()

        # plot the plot
        progbarend()
        plt.title("DM profile: " + filename)
        plt.legend()
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('Radius [$R_{\odot}$]')
        plt.ylabel('$\int_{cell} n_{\\chi}(r)~ dV$')
        plt.ylim(bottom=10**(-14))
        name = filename + "_DMprof" 
        save_plt(plt, name, args)

    # time 
    if args.cpu:
        progbarinit(len(history))
        for i in range(len(history)):
            plt.plot(history[i].star_age, history[i].elapsed_time,
                    color=vir(i / len(history)),
                    ls = '-',
                    linewidth=2,
                    label=hist_lab[i])
            progbar()

        # make the plot
        progbarend()
        plt.title("MESA Computation Time " + filename)
        plt.legend()
        plt.ylabel('Ellapsed Wall Time')
        plt.xlabel('Age [yr]')
        name = filename + "_cpu" 
        save_plt(plt, name, args)

    # dense
    if args.Arho:
        def animate(k):
            # get profile info from MESA reader
            dat, lab, mmm = mesa_prof(mrdirs[0], profs[0][k])

            # set our data
            x = dat.radius
            y = 10**(dat.logRho) 
            line.set_data(x, y)

            # return to animation 
            return line,

        # plot the plot
        # fig.plt.title("Density Profile: " + filename)
        # fig.plt.legend()
        # fig.plt.ylabel('Density [g cm$^{-3}$]')
        # fig.plt.yscale('log')
        # fig.plt.xlabel('Radius [$R_{\odot}$]')
        name = filename + "_rho" 
        anim = an.FuncAnimation(fig, animate, init_func=aninit, frames=200, interval=20, blit=True)
        anim.save(name + '.gif', writer='imagemagick')

###########
# EXECUTE #
###########
if __name__ == "__main__":
    # execute only if run as a script
    main()

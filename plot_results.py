##############################################
# Quick script to read in pin readings file 
# for a given board.
#
# Author: Ed Leming <e.leming@sussex.ac.uk>
# Date: 29/07/2016
##############################################
import argparse
#import ROOT
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

def check_dir(dname):
    """Check if directory exists, create it if it doesn't"""
    direc = os.path.dirname(dname)
    try:
        os.stat(direc)
    except:
        os.makedirs(direc)
        print "Made directory %s...." % dname
    return dname    

def read_data_file(fname):
    '''Function to read in data file
    '''
    fin = file(fname,'r')
    results = [[],[],[],[]]
    for line in fin.readlines():
        if line[0]=="#":
            continue
        bits = line.split()
        # Correct for indexing offset
        chan = int(bits[0])
        if chan < 5:
            chan = chan - 1
        else:
            chan = chan - 5
        # Fill dict with values
        results[chan].append({"channel":int(bits[0]),"width":int(bits[1]), "master_pin":int(bits[2]), "master_rms":float(bits[3]), "slave_pin":int(bits[4]), "slave_rms":float(bits[5])})
    return results

def plot(chan, data):
    '''Function to plot variables from data format
    '''
    x = [i['width'] for i in data[chan][:]]
    master = [i['master_pin'] for i in data[chan][:]]
    master_err = [i['master_rms'] for i in data[chan][:]]
    slave = [i['slave_pin'] for i in data[chan][:]]
    slave_err = [i['slave_rms'] for i in data[chan][:]]

    plt.figure()
    plt.errorbar(x, master, yerr=master_err, fmt='.', color='r', label='Master mode')
    plt.errorbar(x, slave, yerr=slave_err, fmt='.', color='b', label='Slave mode')
    plt.title("PIN response as a function of IPW: Channel %i" % data[chan][0]["channel"])
    plt.xlabel("IPW [12 bit]")
    plt.ylabel("PIN response [14 bit]")
    legend = plt.legend()

def plot_all(data, board_name):
    '''Function to plot all 4 channels response
    '''
    
    fig = plt.figure(num=None, figsize=(16, 10), dpi=80)
    fig.suptitle('Response for board: %s' % (board_name), fontsize=16)
    for chan in range(4):
        x = [i['width'] for i in data[chan][:]]
        master = [i['master_pin'] for i in data[chan][:]]
        master_err = [i['master_rms'] for i in data[chan][:]]
        slave = [i['slave_pin'] for i in data[chan][:]]
        slave_err = [i['slave_rms'] for i in data[chan][:]]
        
        plt.subplot(int("22%i" % (chan + 1)))
        plt.errorbar(x, master, yerr=master_err/np.sqrt(500), fmt='.', color='r', label='Master mode')
        plt.errorbar(x, slave, yerr=slave_err/np.sqrt(500), fmt='.', color='b', label='Slave mode')
        #plt.title("PIN response as a function of IPW: Channel %i" % data[chan][0]["channel"])
        plt.title("Channel %i" % data[chan][0]["channel"])
        plt.xlabel("IPW [12 bit]")
        plt.ylabel("PIN response [14 bit]")
        legend = plt.legend()
    return fig

def plot_low(data, board_name):
    '''Function to plot all 4 channels response
    '''
    fig = plt.figure(num=None, figsize=(16, 10), dpi=80)
    fig.suptitle('Response for board: %s' % (board_name), fontsize=16)
    for chan in range(4):
        x = [i['width'] for i in data[chan][:]]
        master = [i['master_pin'] for i in data[chan][:]]
        master_err = [i['master_rms'] for i in data[chan][:]]
        slave = [i['slave_pin'] for i in data[chan][:]]
        slave_err = [i['slave_rms'] for i in data[chan][:]]
        
        plt.subplot(int("22%i" % (chan + 1)))
        plt.errorbar(x[:110], master[:110], yerr=master_err[:110]/np.sqrt(500), fmt='.', color='r', label='Master mode')
        plt.errorbar(x[:110], slave[:110], yerr=slave_err[:110]/np.sqrt(500), fmt='.', color='b', label='Slave mode')
        #plt.title("PIN response as a function of IPW: Channel %i" % data[chan][0]["channel"])
        plt.title("Channel %i" % data[chan][0]["channel"])
        plt.xlabel("IPW [12 bit]")
        plt.ylabel("PIN response [14 bit]")
        legend = plt.legend()
    return fig

if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='file', help='path to data file')
    args = parser.parse_args()    
    
    results = read_data_file(args.file)
    
    board_name = args.file[8:-17]
    broad_sweep = plot_all(results, board_name)
    low_sweep = plot_low(results, board_name)

    plot_path = check_dir("plots/%s/" % board_name)
    broad_sweep.savefig("%s/full_sweep.png" % plot_path)
    low_sweep.savefig("%s/low_sweep.png" % plot_path)

    plt.show()
    #os.system("open %s/low_sweep.png" % plot_path)
    #os.system("open %s/full_sweep.png" % plot_path)


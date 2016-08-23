#!/usr/bin/env python
##############################
# run_readout_test.py
#
# Script to acquire a set of 
# pin readings over the full 
# operational range of a PIN 
# board.
##############################

import time
import argparse
import numpy as np
from core import serial_command

def read_pin():
    '''Wait keep looking for pin. It will be retuned when the sequence ends
    '''
    pin, rms = None, None
    try:
        while (pin == None):
            pin, rms, channel = sc.read_pin_sequence()
    except KeyboardInterrupt:
        print "Keyboard interrupt"
    return int(pin), float(rms)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', dest='board_name', help='Board identifier')
    parser.add_argument('-n', dest='pulses', type=int,
                        help='Number of pulses to average in a sequence [500]',
                        default = 500)
    parser.add_argument('-c', dest='channels', 
                        help='Argument is true if this board is for channels 1-4, false for channels 5-8 [False]',
                        default = False)
    args = parser.parse_args()
    if args.channels:
        channels = [1,2,3,4]
    else:
        channels = [5,6,7,8]

    # Connect to tellie
    sc = serial_command.SerialCommand("/dev/tty.usbserial-FTGA2OCZ")
    sc.select_channel(channels[0]) # Lets us set up other inputs 
    sc.set_pulse_height(16383)
    sc.set_fibre_delay(0)
    sc.set_pulse_delay(1.0)
    sc.set_trigger_delay(0)    
    sc.set_pulse_number(args.pulses)

    # What do we want to run over?
    widths = {}
    widths[channels[3]] =  np.concatenate( (np.arange(7700,6500,-10), np.arange(6500,0,-50)) )
    widths[channels[2]] =  np.concatenate( (np.arange(7700,6500,-10), np.arange(6500,0,-50)) )
    widths[channels[1]] =  np.concatenate( (np.arange(8350,7200,-10), np.arange(7200,0,-50)) )
    widths[channels[0]] =  np.concatenate( (np.arange(7250,6100,-10), np.arange(6100,0,-50)) )

    # Make output file
    timestamp = time.strftime("%H.%M_%y%m%d",time.gmtime())
    filename = "./results/%s_%s.txt" % (args.board_name, timestamp)
    out_file = file(filename, 'w')
    out_file.write("#Pulses per measurement = %i\n" % args.pulses)
    out_file.write("#Channel\tIPW\tmaster_pin\tmaster_rms\tslave_pin\tslave_rms\n")

    for chan in channels:
        sc.select_channel(chan)
        for width in widths[chan]:
            sc.set_pulse_width(width)
            
            # Fire master mode
            sc.fire_sequence()
            master_pin, master_rms = read_pin()

            # Fire slave mode
            sc.trigger_averaged()
            slave_pin, slave_rms = read_pin()

            out_file.write("%i\t%i\t%i\t%1.2f\t%i\t%1.2f\n" % (chan,width,master_pin, master_rms, slave_pin, slave_rms))
            print "---------------"
            print "Channel %i" % chan
            print "---"
            print "IPW: %i\nMaster: %i +/- %1.2f\nSlave: %i +/- %1.2f" % (width, master_pin, master_rms, slave_pin, slave_rms)
            if (slave_pin == master_pin == 65535):
                break
            
    out_file.close()

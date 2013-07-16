# Import libraries
from argparse import ArgumentParser
from serial import Serial
from serial import SerialException
import struct
from sys import exit
from time import sleep
from xbee import ZigBee
from ZBDispatch import ZBDispatch

# Import different uploaders
import uploaders.xively
import uploaders.nimbits
#import uploaders.sense

# Comment those services that you don't want to make use of
VERSION = '1.0.0'


def hex(bindata):
    '''Transforms binary information into useful, readable
    data.

    Keyword arguments:
    bindata -- string that holds binary information
    '''

    return ''.join('%02x' % ord(byte) for byte in bindata)

def decode(m):
    '''Decodes the integer that contains useful metadata
    in order to correctly unpack information from the
    XBee packet.

    Keyword arguments:
    i -- metadata integer
    '''

    # The function will return this variable
    result = []

    # Holds all valid data types
    # http://docs.python.org/2/library/struct.html
    data_types = [{'?': 1}, {'c': 1}, {'B': 1}, {'i': 4},\
            {'I': 4}, {'l': 4}, {'L': 4}, {'h': 2},\
            {'f': 4}, {'d': 8}]

    for i in range(0, len(str(m))):
        result.append(data_types[int(str(m)[i]) - 1])

    return result



def direct_io_handler(name, packet, debug):
    '''Takes an incoming packet and extracts the useful
    information and creates a ready-to-serialize
    object (dict). Used when XBee Direct I/O is enabled.

    Keyword arguments:
    name -- ID of the packet, i.e. 'rx_io_data_long_addr'
    packet -- The packet itself
    debug -- Wether the content should be printed or not
    '''

    if debug:
        print packet

    sa = hex(packet['source_addr'])
    data = []

    for d in packet['samples'][0].keys():
        data.append(packet['samples'][0][d])

    print 'PACKET RECEIVED FROM: ' + sa
    print 'DATA: ' + str(data) + '\n'
    uploaders.xively.upload(sa, data)
    #uploaders.nimbits.upload(sa, data)



def xbee_arduino_handler(name, packet, debug):
    '''Takes an incoming packet and extracts the useful
    information and creates a ready-to-serialize
    object (dict). The packets come from an Arduino
    with an XBee module attached.

    Keyword arguments:
    name -- ID of the packet, i.e. 'rx'
    packet -- The packet itself
    debug -- Wether the content should be printed or not
    '''

    if debug:
        print packet

    # Get source address and actual data
    sa = hex(packet['source_addr_long'][4:])
    rf = hex(packet['rf_data'])

    # Check what data types are going to be unpacked
    h = struct.unpack('i',packet['rf_data'][0:4])[0]
    decoded_h = decode(h)

    # Will contain unpacked info.
    data = []

    counter = 4
    for dt in decoded_h:
        data.append(struct.unpack(dt.keys()[0],
            packet['rf_data'][counter:counter+dt.values()[0]])[0])
        counter = counter + dt.values()[0]

    print 'PACKET RECEIVED FROM: ' + sa
    print 'DATA: ' + str(data) + '\n'
    uploaders.xively.upload(sa, data)
    #uploaders.nimbits.upload(sa, data)


def main():
    '''After parsing arguments , it instantiates an
    asynchronous dispatcher which creates a new thread
    for every packet that arrives.
    '''

    # Argument parsing
    parser = ArgumentParser(description='Receives data from any number or XBee routers in API mode using Direct I/O and then uploads this information to Cosm.')
    parser.add_argument('--debug', help='prints everything that the coordinator receives', action='store_true', default=False)
    parser.add_argument('device_file', help='where the zigbee cordinator is connected', action='store')
    parser.add_argument('baud_rate', action='store', type=int)
    args = vars(parser.parse_args())


    # Serial connection with the XBee
    try:
        ser = Serial(args['device_file'], args['baud_rate'])
    except SerialException as s:
        print 'Connection with the XBee could not be established... Exiting.'
        exit()
    print 'Listening on', args['device_file'], '...\n'


    # Asynchronous dispatcher
    dispatch = ZBDispatch(ser)
    dispatch.register(
        'direct_io',
        direct_io_handler,
        lambda packet: packet['id']=='rx_io_data_long_addr',
        args['debug']
    )
    dispatch.register(
        'io_data',
        xbee_arduino_handler,
        lambda packet: packet['id']=='rx',
        args['debug']
    )

    zb = ZigBee(ser, callback=dispatch.dispatch, escaped=True)


    # Main loop
    while True:
        try:
            sleep(.1)
        except KeyboardInterrupt as k:
            print '\nCTRL+C received. Exiting.'
            break


    # Close XBee connection
    zb.halt()
    ser.close()


if __name__ == '__main__':
    main()
else:
    pass

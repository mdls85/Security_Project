import socket
import argparse
import sys

def setup_args_to_script():
    # sets up command line help options and passing filename as argument
    about = 'This program reads the IP addresses found in a file passed via cmd line and determines whether the address is vulnerable to the Java Desrialization Bug by way of running versions of Oracle WebLogic that are vulnerable.'

    parser = argparse.ArgumentParser(description=about)
    parser.add_argument('filename', help="filename of file containing ip addresses")
    parser.parse_args()

def read_addresses(filename):
    # open file named 'filename' for reading and returns a list the IP addresses found in that file
    file_handler = open(filename,'r')

    # using list comprehension to read each line in file and storing each in list minus end of line character
    addresses = [line.rstrip() for line in file_handler]

    # close file
    file_handler.close()

    return addresses

if __name__ == '__main__':
    setup_args_to_script()
    TARGET_PORT = 7001

    # access filename passed via cmd line (args set for script so try block not necessary
    arg1 = sys.argv[1]

    addresses = read_addresses(arg1)
    t3_header = 't3 12.2.1\nAS:255\nHL:19\nMS:10000000\nPU:t3://us-l-breens:7001\n\n'

    for ip in addresses:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3.0)

        try:
            sock.connect((ip, TARGET_PORT))
            sock.sendall(t3_header)
        except Exception as e:
            print e.message

        try:
            data = sock.recv(1024)
        except socket.timeout:
            data = ''

        sock.close()

        if 'HELO' in data:
            print ip + " is vulnerable."
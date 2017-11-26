from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException
import argparse
import sys

def setup_args_to_script():
    # sets up command line help options and passing filename as argument
    about = 'This program determines whether ip address(es) passed to it is/are vulnerable to the Java Deserialization Bug by way of running versions of Oracle WebLogic that are vulnerable.'

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
    args = setup_args_to_script()

    # potential ports - [7001 - 9000, 5556]

    TARGET_PORT = 7001
    START_PORT = 7001
    END_PORT = 9000
    OTHER_PORT = 5556
    TARGET_PROTOCOL = 't3'

    # access filename passed via cmd line (args set for script so try block not necessary
    arg1 = sys.argv[1]

    addresses = read_addresses(arg1)

    # LOOK INTO SUBNET SCENE (-sn ip/24) which disables ping scan so add discovered addresses to list and proceed with port scan

    for ip in addresses:
        # instantiate nmap prcoess

        # -p7001 port to scan
        # -sV - probe open ports to detect service and version info
        options = "-p" + str(START_PORT) + "-" + str(END_PORT) + "," + str(OTHER_PORT) + " -sV"
        n_map_proc = NmapProcess(ip, options=options)
        n_map_proc.run()

        # GET REPORT IF SUCCESSFUL THEN TRY TO DETERMINE SERVICE ON PORT 7001

        if n_map_proc.rc == 0:
            # nmap task completed successfully
            # try to parse the XML output into a report
            try:
                # expecting NmapReport since passing complete xml output
                report = NmapParser.parse(n_map_proc.stdout)

                # fetch the scanned hosts from report (single ip address = 0 but subnet maybe more (or if a range given)
                hosts = report.hosts

                for host in hosts:
                    # check for service running on port 7001 with t3 protocol
                    services = host.services

                    for service in services:
                        # the service exists so use banner grabbing to try to determine application name and version
                        # search string for weblogic name and version
                        print service.banner
                        print service.servicefp
                        print service.service


            except NmapParserException as e:
                print e.msg
        else:
            print 'error performing nmap on ' + ip
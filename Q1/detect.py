import socket
import argparse
import sys
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException

OUTPUT_FILE = 'report.txt'
# START_PORT = 7001
# END_PORT = 9001
START_PORT = 8001
END_PORT = 8001
VERSIONS = ['10.3.6.0', '12.1.2.0', '12.1.3.0', '12.2.1.0']

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

def get_output_handler():
    file_handler = open(OUTPUT_FILE, 'w')

    return file_handler

def build_t3_header(ip, port):
    t3_header = 't3 '
    t3_header += '12.2.1'                                   # noticed that regardless of version passed, the real version provided the version is not below 10. Since versions below 10 not vulnerable. we do not vary this
    t3_header += '\nAS:255\nHL:19\nMS:10000000\nPU:t3://'
    t3_header += str(ip)
    t3_header += ':'
    t3_header += str(port)
    t3_header += '\n\n'

    return t3_header

def fetch_version(data):
    # returns the version from the data received from sockets in response to the t3 protocol message sent
    # known that the string 'HELO' is in data
    index = data.find('O', 0, len(data))

    # extract slice of string after string 'HELO'
    version = data[index+2:13]

    return version

def get_subnet_hosts(subnet):

    host_list = []
    n_map_proc = NmapProcess(subnet, options="-sn")
    n_map_proc.run()

    if n_map_proc.rc == 0:
        # nmap task completed successfully
        # try to parse the XML output into a report
        try:
            # expecting NmapReport since passing complete xml output
            report = NmapParser.parse(n_map_proc.stdout)

            # fetch the scanned hosts from report (single ip address = 0 but subnet maybe more (or if a range given)
            hosts = report.hosts

            for host in hosts:
                if host.is_up():
                    host_list.append(host)
        except NmapParserException as e:
            print e.msg

    return host_list

def scan_ip(ip, output):
    for port in range(START_PORT, END_PORT + 1):
        t3_header = build_t3_header(ip,port)
        data = ''
        try:
            # connect and send headers
            print 'Connecting to ' + ip + ':' + str(port) + ' ...'
            sock = socket.create_connection((ip,port), 4)
            sock.settimeout(2.0)

            print 'Sending header message ...'
            sock.sendall(t3_header)

            try:
                # listen for received response from socket
                data = sock.recv(1024)
            except socket.timeout:
                # connected but received no response
                print 'No response'

            sock.close()

            if "HELO" in data:
                # known that server is running an instance of oracle weblogic on tested port

                version = fetch_version(data)

                if version:
                    # a version was returned
                    if version in VERSIONS:
                        # the version returned is vulnerable
                        output.write('Oracle Weblogic ' + version + ' found running on ' + ip + ':' + str(port) + ' is vulnerable')

                        # don't bother checking other versions or ports as we have found vulnerability
                        return True
                    else:
                        # non-vulnerable version of weblogic running
                        print 'Oracle Weblogic running on ' + ip + ':' + str(port) + ' is not vulnerable (version ' + version + ').'

                        # assuming that since there is a non-vulnerable version on this port, if instances exist on other ports at this IP then they too are not vulnerable
                        return False
                else:
                    print 'Oracle Weblogic version is unknown. Vulnerability cannot be determined.'
            else:
                print 'Either weblogic not running or old (and safe from bug) version Weblogic running.'

        except Exception:
            print 'Connection failed'

if __name__ == '__main__':
    setup_args_to_script()

    # CHANGE TO MUTUALLY EXCLUSIVE COMMAND LINE ARGS THAT SET WHETHER IP OR SUBNET PASSED
    # access filename passed via cmd line (args set for script so try block not necessary
    arg1 = sys.argv[1]

    addresses = read_addresses(arg1)
    output_handler = get_output_handler()

    for ip in addresses:
        scan_ip(ip,output_handler)
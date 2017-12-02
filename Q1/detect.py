import socket
import argparse
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException

OUTPUT_FILE = 'report.txt'
START_PORT = 9001
END_PORT = 9002
VERSIONS = ['10.3.6.0', '12.1.2.0', '12.1.3.0', '12.2.1.0']

def setup_args_to_script():
    # sets up command line argument options
    about = 'This program detects whether a server is vulnerable to the Java Desrialization Bug.'

    parser = argparse.ArgumentParser(description=about)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', help="filename of file containing ip addresses")
    group.add_argument('--ip', help="a single ip address to test")
    group.add_argument('--sub', help="a subnet address to test")
    parsed = parser.parse_args()
    return parsed

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

            # fetch the scanned hosts from report
            hosts = report.hosts

            for host in hosts:
                if host.is_up():
                    host_list.append(host.address)
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
                        print 'Oracle Weblogic ' + version + ' found running on ' + ip + ':' + str(port) + ' is vulnerable'

                        # don't bother checking other versions or ports as we have found vulnerability
                        return
                    else:
                        # non-vulnerable version of weblogic running
                        print 'Oracle Weblogic running on ' + ip + ':' + str(port) + ' is not vulnerable (version ' + version + ').'

                        # assuming that since there is a non-vulnerable version on this port, if instances exist on other ports at this IP then they too are not vulnerable
                        return
                else:
                    print 'Oracle Weblogic version is unknown. Vulnerability cannot be determined.'
            else:
                print 'WebLogic may not be running on this on ' + ip + ':' + str(port)

        except Exception:
            print 'Connection failed'

if __name__ == '__main__':
    args = setup_args_to_script()

    # determine argument passed via cmd

    if args.file:
        # a filename was passed with a list of IPs
        addresses = read_addresses(args.file)
    elif args.sub:
        # a subnet was passed
        addresses = get_subnet_hosts(args.sub)
    else:
        # a single IP was passed
        addresses = []
        addresses.append(args.ip)

    output_handler = get_output_handler()

    for ip in addresses:
        scan_ip(ip,output_handler)
        print '\n'

    # closing file
    output_handler.close()
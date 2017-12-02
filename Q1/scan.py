from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException
import argparse
import sys

if __name__ == '__main__':
    # declaring ip and port of known server running vulnerable version of Oracle WebLogic
    VERSIONS = ['10.3.6.0', '12.1.2.0', '12.1.3.0', '12.2.1.0']
    TARGET_PORT = 9001
    TARGET_IP = '54.202.208.189'


    # instantiate nmap prcoess
    # -p9001 port to scan
    # -sV - probe open ports to detect service and version info
    # --version-all - try every single probe (intensity 9)
    # -Pn - treat all hosts as online (get around blocking of probe)
    options = "-p" + str(TARGET_PORT) + " -sV --version-all -Pn"
    n_map_proc = NmapProcess(TARGET_IP, options=options)
    n_map_proc.run()

    # GET REPORT IF SUCCESSFUL THEN TRY TO DETERMINE SERVICE ON PORT 7001

    if n_map_proc.rc == 0:
        print 'Successfully scanned ' + TARGET_IP + ':' + str(TARGET_PORT) + '...'
        # nmap task completed successfully
        # try to parse the XML output into a report
        try:
            print 'Parsing results ...'
            # expecting NmapReport since passing complete xml output
            report = NmapParser.parse(n_map_proc.stdout)

            # fetch the scanned hosts from report
            hosts = report.hosts

            for host in hosts:
                # check for service running on port 9001
                services = host.services

                if services:
                    print 'Services running...'
                else:
                    print 'No services detected'
                for service in services:
                    # a service exists so use banner grabbing to try to determine application name and version
                    if 'Oracle WebLogic Server' in service.banner:
                        # oracle weblogic running... try to get version
                        if 'version' in service.banner:
                            # a version was returned
                            for vers in VERSIONS:
                                if vers in service.banner:
                                    print 'Oracle Weblogic ' + vers + ' found running on ' + TARGET_IP + ':' + str(TARGET_PORT) + ' is vulnerable'
                        else:
                            print 'Oracle WebLogic is running but version is unknown'
        except NmapParserException as e:
            print e.msg
    else:
        print 'error performing nmap on ' + TARGET_IP + ':' + str(TARGET_PORT)
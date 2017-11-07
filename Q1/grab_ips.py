from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException

if __name__ == '__main__':
    TARGET_PORT = 7001
    TARGET_PROTOCOL = 't3'

    ip = '192.65.160.2/24'

    n_map_proc = NmapProcess(ip, options="-sn")
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
                if host.is_up():
                    print host.address
        except NmapParserException as e:
            print e.msg

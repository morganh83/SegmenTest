```
usage: segmentationTest.py [-h] \[-i IP] [-c CIDR] \[-f FILE] [-s] \[-v]

Perform a network segmentation test against a client network or networks

optional arguments:
  -h, --help            show this help message and exit
  -i IP, --ip IP        Test a Single IP
  -c CIDR, --cidr CIDR  CIDR address to test
  -f FILE, --file FILE  File containing IP addresses in CIDR or single format
  -s, --stop            Stop the script after the first failed test
  -v, --verbose         Display the IP addresses of the hosts that responded to the tests
```

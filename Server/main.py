import sys
import multiThreadSocketServer

arg = None
verbose = False

try:
    arg = sys.argv[1]
    if(arg) == "-v":
        verbose = True
    else:
        raise SystemExit(f"This script only takes the argument \"-v\", not {arg}.Run with \"-v\" to see verbose output.")
except IndexError:
    pass
if(len(sys.argv)>2):
    raise SystemExit(f"This script only takes the argument \"-v\", not {arg}. Run with \"-v\" to see verbose output.")

def main():
    s = multiThreadSocketServer.Server("127.0.0.1",65432,1024,True) 



if __name__ == "__main__":
    main()

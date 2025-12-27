#!/usr/bin/env python3
import sys
import byond.topic as Topic

def print_help():
    print("BYOND Status Query test\n")
    print("Usage: " + sys.argv[0] + " [hostname] [port] [query]\n")
    sys.exit(1)

def main():
    if(len(sys.argv) < 3):
        print_help()

    host = sys.argv[1]
    port = sys.argv[2]
    if(len(sys.argv) > 3):
        query = sys.argv[3]
    else:
        query = 'status'

    response_type,response_data = Topic.send(host, port, '?{}'.format(query))
    print("Response:")
    print(response_data)
    print("Response size: {}".format(len(str(response_data))))


if __name__ == "__main__":
    main()

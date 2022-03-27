#!/usr/bin/env python3
import sys
import byond.topic as Topic

def print_help():
    print("BYOND Status Query test\n")
    print("Usage: " + sys.argv[0] + " [hostname] [port]\n")
    sys.exit(1)

def main():
    if(len(sys.argv) < 3):
        print_help()

    host = sys.argv[1]
    port = sys.argv[2]

    response_type,response_data = Topic.send(host, port, '?status')
    print("Status:")
    print(response_data)

    response_type,response_data = Topic.send(host, port, '?playing')

    print("Current players from '?playing': " + str(int(response_data)))


if __name__ == "__main__":
    main()

'''
Crapy stego
'''

import sys
import os
import getpass
import argparse
import imghdr
import struct

desc = """
Do you want to hide data in files and maybe break the files 
and also not hide the data really good at all?. Then this is 
the tool for you!
"""

def sxor(s1, s2):
    # convert strings to a list of character pair tuples
    # go through each tuple, converting them to ASCII code (ord)
    # perform exclusive or on the ASCII code
    # then convert the result back to ASCII (chr)
    # merge the resulting array of characters as a string
    return bytes([(ord(a) ^ ord(b)) for a, b in zip(s1, s2)])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-f", "--file", action="store", help="File to add/get secrets to/from", 
                        type=str, required=True)
    parser.add_argument("-d", "--dest", action="store", help="Destination file", type=str)
    parser.add_argument("-m", "--message", action="store", help="The message to hide in the file", type=str)
    parser.add_argument("-u", "--un_steg", action="store_true", help="Undo stego and get message", default=False)
    parser.add_argument("-e", "--extra_sec", action="store_true", help="Adds extra secrurity", default=False)

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print("File {} does not exist dingus!".format(args.file))
        sys.exit(1)

    if not args.un_steg and not args.dest:
        print("Destination file is required")
        sys.exit(1)
    elif not args.un_steg and os.path.exists(args.dest):
        print("Destination file {} exists and would be overwritten.".format(args.dest))
        sys.exit(1)

    if not args.message and not args.un_steg:
        print("A message is required dingus!")
        sys.exit(1)

    if args.extra_sec:
        password = None
        try:
            while 1:
                password = getpass.getpass(prompt="password: ")
                if not password or len(password) < 5:
                    print("A password is required (minimum length 5)!")
                    continue
                check = getpass.getpass(prompt="again: ")
                if check != password:
                    print("Passwords don't match dingus!")
                    continue
                else:
                    break
        except KeyboardInterrupt:
            print("exiting...")
            sys.exit(1)

        if not password:
            sys.exit(1)

        print("Sweet password!")

    img_type = imghdr.what(args.file)
    if img_type == "bmp":
        BMP_FILE_HEADER_SIZE = 50 # 14 + 1 bytes
        if not args.un_steg:
            source_file = None
            with open(args.file, 'rb') as f:
                source_file = bytearray(f.read())

            if args.extra_sec:
                if len(password) > len(args.message):
                    password = password[:len(args.message)]
                elif len(password) < len(args.message):
                    diff = len(args.message) - len(password)
                    password = password + "*" * diff
                message = sxor(args.message, password)
            else:
                message = args.message
                message = message.encode('utf-8')

            l = struct.pack("I", len(message))
            for i, b in enumerate(l):
                loc = BMP_FILE_HEADER_SIZE + i
                source_file[loc] = b

            start = BMP_FILE_HEADER_SIZE + struct.calcsize("I")
            for i, b in enumerate(message):
                loc = start + i
                source_file[loc] = b

            with open(args.dest, 'wb') as f:
                f.write(source_file)
        else:
            file_contents = None
            with open(args.file, 'rb') as f:
                file_contents = f.read()
            s = struct.calcsize("I")
            l = file_contents[BMP_FILE_HEADER_SIZE:BMP_FILE_HEADER_SIZE+s]
            l = struct.unpack("I", l)[0]
            loc = BMP_FILE_HEADER_SIZE + s
            end = loc + l
            message = file_contents[loc:end]

            if args.extra_sec:
                if len(password) > l:
                    password = password[:l]
                elif len(password) < l:
                    diff = l - len(password)
                    password = password + "*" * diff
                message = sxor(password, message.decode('utf-8')).decode('utf-8')
            print("Message:", message)
    else:
        if not args.un_steg:
            source_file = None
            with open(args.file, 'rb') as f:
                source_file = f.read()
            with open(args.dest, 'wb') as f:
                f.write(source_file)
                l = struct.pack("I", len(args.message))
                f.write(args.message.encode('utf-8'))
                f.write(l)
        else:
            file_contents = None
            with open(args.file, 'rb') as f:
                file_contents = f.read()
            s = struct.calcsize("I") * -1
            l = struct.unpack("I", file_contents[s:])[0]
            loc = s - l
            end = loc + l
            print("Message:", file_contents[loc:end].decode('utf-8'))

    print("Done!")

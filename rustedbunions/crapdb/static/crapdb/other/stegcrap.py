'''
Crapy stego
'''

import sys
import os
import getpass
import argparse
import imghdr
import struct
import string

DESC = """
Do you want to hide data in files and maybe break the files 
and also not hide the data really good at all?. Then this is 
the tool for you!
"""

ALPHABET = string.ascii_lowercase

# This gets us past the header...idk how big it is
# If it's not fixed length then maybe I break some BMP files...whatever
BMP_FILE_HEADER_SIZE = 50

def sxor(str1, str2):
    '''
    convert strings to a list of character pair tuples
    go through each tuple, converting them to ASCII code (ord)
    perform exclusive or on the ASCII code
    then convert the result back to ASCII (chr)
    merge the resulting array of characters as a string
    '''
    return bytes([(ord(a) ^ ord(b)) for a, b in zip(str1, str2)])

def shifttext(shift, msg):
    '''
    Perform ROT
    '''
    msg = msg.strip().lower()
    data = []
    for char in msg:
        if char.strip() and char in ALPHABET:
            data.append(ALPHABET[(ALPHABET.index(char) + shift) % 26])
        else:
            data.append(char)

    output = ''.join(data)
    return output.encode('utf-8')

def get_rot_constant():
    '''
    Get the user's ROT constant
    '''
    rot = 1
    try:
        while 1:
            try:
                rot = int(input("How much to ROT?"))
                if rot <= 0:
                    print("Must be more than 0")
                    continue
                else:
                    break
            except ValueError:
                print("Bad input")
                continue
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(1)

    return rot

def get_password():
    '''
    Get the user's password
    '''
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
    return password

def main(args):
    '''
    Do all the main stuff for the program
    '''

    # Check all the arguments
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

    apply_sec = 0
    if args.extra_sec:
        apply_sec += 1
    if args.some_sec:
        apply_sec += 1
    if args.Xtreme_sec:
        apply_sec += 1

    if apply_sec > 1:
        print("You can't do more than 1 sec at a time")
        sys.exit(1)

    password = None
    rot = 1
    message = None

    if args.message:
        message = args.message.encode('utf-8')

    if args.extra_sec:
        password = get_password()

        if args.message:
            if len(password) > len(args.message):
                password = password[:len(args.message)] # Truncate password. Too long
            elif len(password) < len(args.message):
                diff = len(args.message) - len(password) # How much longer do we need to be
                password = password + ("*" * diff) # Pad with '*' characters

            # Do XOR crypto on the message
            message = sxor(args.message, password)
    elif args.some_sec:
        rot = get_rot_constant()

        if args.message:
            # Do ROT on the message
            message = shifttext(rot, args.message)
    elif args.Xtreme_sec:
        # TODO
        print("TODO")
        sys.exit(1)

    # get the image type based on the image header
    img_type = imghdr.what(args.file)
    if img_type == "bmp":
        if not args.un_steg:
            '''
            Adding sego
            '''
            source_file = None
            with open(args.file, 'rb') as file:
                source_file = bytearray(file.read())

            # Write the length of the message to the header first
            length_bytes = struct.pack("I", len(message))
            for i, byte in enumerate(length_bytes):
                loc = BMP_FILE_HEADER_SIZE + i
                source_file[loc] = byte

            # Write the message after the length
            start = BMP_FILE_HEADER_SIZE + struct.calcsize("I")
            for i, byte in enumerate(message):
                loc = start + i
                source_file[loc] = byte

            # Write to the destination file
            with open(args.dest, 'wb') as file:
                file.write(source_file)
        else:
            '''
            Undoing stego
            '''
            file_contents = None
            with open(args.file, 'rb') as file:
                file_contents = file.read()

            # Fist get the size of the length (4 bytes for 'I' I think...)
            len_size = struct.calcsize("I") # Number of bytes used to store the length

            # Then get those bytes
            msg_len_bytes = file_contents[BMP_FILE_HEADER_SIZE:BMP_FILE_HEADER_SIZE + len_size]

            # Then convert those bytes to an actual number representing the message length
            msg_len = struct.unpack("I", msg_len_bytes)[0]

            # Pull out the message
            loc = BMP_FILE_HEADER_SIZE + len_size
            end = loc + msg_len
            message = file_contents[loc:end].decode('utf-8')

            # Decrypt
            if args.extra_sec:
                if len(password) > len(message):
                    password = password[:len(message)] # Truncate password. Too long
                elif len(password) < len(message):
                    diff = len(message) - len(password) # How much longer do we need to be
                    password = password + ("*" * diff) # Pad with '*' characters

                message = sxor(password, message).decode('utf-8')
            elif args.some_sec:
                message = shifttext((rot * -1), message).decode('utf-8')

            print("Message:", message)
    else:
        if not args.un_steg:
            '''
            Adding stego
            '''
            source_file = None
            with open(args.file, 'rb') as file:
                source_file = file.read()

            with open(args.dest, 'wb') as file:
                file.write(source_file)
                length = struct.pack("I", len(message))
                file.write(message)
                file.write(length)
        else:
            '''
            Undoing stego
            '''
            file_contents = None
            with open(args.file, 'rb') as file:
                file_contents = file.read()

            struct_len = struct.calcsize("I") * -1 # Need as negative to rev idx the file contents
            msg_len = struct.unpack("I", file_contents[struct_len:])[0]
            loc = struct_len - msg_len
            end = loc + msg_len
            message = file_contents[loc:end].decode('utf-8')

            # Decrypt
            if args.extra_sec:
                if len(password) > len(message):
                    password = password[:len(message)] # Truncate password. Too long
                elif len(password) < len(message):
                    diff = len(message) - len(password) # How much longer do we need to be
                    password = password + ("*" * diff) # Pad with '*' characters

                message = sxor(password, message).decode('utf-8')
            elif args.some_sec:
                message = shifttext((rot * -1), message).decode('utf-8')

            print("Message:", message)

    print("Done!")

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description=DESC)

    PARSER.add_argument("-f", "--file", action="store", help="File to add/get secrets to/from",
                        type=str, required=True)

    PARSER.add_argument("-d", "--dest", action="store", help="Destination file", type=str)

    PARSER.add_argument("-m", "--message", action="store",
                        help="The message to hide in the file", type=str)

    PARSER.add_argument("-u", "--un_steg", action="store_true",
                        help="Undo stego and get message", default=False)

    PARSER.add_argument("-e", "--extra_sec", action="store_true",
                        help="Adds extra security", default=False)

    PARSER.add_argument("-s", "--some_sec", action="store_true",
                        help="Adds some security", default=False)

    PARSER.add_argument("-X", "--Xtreme_sec", action="store_true",
                        help="Adds extreme security", default=False)

    # Start the things
    main(PARSER.parse_args())

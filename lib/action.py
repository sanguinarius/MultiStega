#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PIL import Image
from Crypto.Cipher import AES
import base64
from stegano import slsb


DEFAULT_SEPARATOR=":"

def check_image(path):
    try:
        i=Image.open(path)
        if i.format=='PNG':
            return path
        else:
            raise ValueError
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except ValueError:
        print "Source file isn't a PNG"
    except:
        print "Unexpected error:", sys.exc_info()[0]
    exit()

class Messages(object):
    def __init__(self, filesrc, filedst = None, blocksize=32, padding="{"):
        self.blocksize = blocksize
        self.padding = padding
        # one-liner to sufficiently pad the text to be encrypted
        pad = lambda s: s + (self.blocksize - len(s) % self.blocksize) * self.padding
        self.pad = pad
        self.filesrc = filesrc
        self.filedst = filedst
        self.separator= DEFAULT_SEPARATOR


class Write_Messages(Messages):
    def create_message(self, nmbmess):
        try:
            mess=[]
            key=[]
            for i in xrange(nmbmess):
                i +=1
                mess.append(raw_input("Enter message number %s : " % i))
                key.append(raw_input("Enter pass number %s : " %i))
            message = self.__encrypt_message(mess, key)
            self.__stega_in_png(message)
            print 'Finish'
        except:
            print "Unexpected error in Creation module:", sys.exc_info()[0]


    def __encrypt_message(self, mess, key):
        # one-liners to encrypt/encode and decrypt/decode a string
        # encrypt with AES, encode with base64
        EncodeAES = lambda c, s: base64.b64encode(c.encrypt(self.pad(s)))
        encoded=[]
        for position, item in enumerate(mess):
            try:
                cipherkey = AES.new(key[position].ljust(self.blocksize, self.padding))
                encoded.append(EncodeAES(cipherkey, item))
            except:
                print "Unexpected error in Encrypt message:", sys.exc_info()[0]
        return encoded

    def __stega_in_png(self, mess):
        try:
            full_string = self.separator.join(mess)
            print full_string
            secret = slsb.hide(self.filesrc, full_string)
            secret.save(self.filedst)
        except:
            print "Unexpected error in Stegano module:", sys.exc_info()[0]

class Reveal_Messages(Messages):
    def detect_message(self):
        #detect message in image same block and padding in parameter
        full_mess = slsb.reveal(self.filesrc)
        full_mess_parse = self.__parse_message(full_mess)
        while 1:
            self.pass_key = raw_input("Enter your key : ")
            if self.pass_key: break
        result = self.__decrypt_message(full_mess_parse, self.pass_key)
        return result

    def __parse_message(self, full_mess):
        list_mess = full_mess.split(self.separator)
        return list_mess


    def __decrypt_message(self, mess, key):
         # one-liners to encrypt/encode and decrypt/decode a string
        # encrypt with AES, encode with base64
        DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(self.padding)
        decoded=[]
        for position, item in enumerate(mess):
            try:
                cipherkey = AES.new(key.ljust(self.blocksize, self.padding))
                decoded.append(DecodeAES(cipherkey, item))
            except:
                print "Unexpected error in Decrypt module:", sys.exc_info()[0]

        result = []
        def is_ascii(s):
            return all(ord(c) < 128 for c in s)
        for str in decoded:
            if is_ascii(str):
                result.append(str)
        return result


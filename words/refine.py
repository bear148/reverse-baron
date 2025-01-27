import os
from pathlib import Path
import re

# Word list refinement functions

ROOT_DIR = Path(__file__).parent
wordFile = ROOT_DIR / 'words-o.txt'
newWordFile = ROOT_DIR / 'words-n.txt'
newWordMD5File = ROOT_DIR / 'words-n-md5.txt'

# Gets all possible words that do not have numbers, special characters, and are between the lengths of 4 and 8.
def condenseToAllPossibleWords():
    with open(wordFile, 'r') as wFile, open(newWordFile, 'w') as oFile:
        for line in wFile:
            #if bool(re.search(r"[^a-zA-Z]", line)) and (len(line) > 3 and len(line) < 9):
            if line.strip().isalpha() and (3 < len(line.strip()) < 9):
                oFile.write(line)

# Translate condensed word list into md5
def translateCondensedIntoMD5():
    with open(newWordFile, 'r') as nWFile, open(newWordMD5File, 'w') as oFile:
        for line in nWFile:
            # This is very important because the MD5 values stored on the wordtwist website are of the words all Uppercase
            temp = line.strip().upper() 
            oFile.write(md5(temp) + "\n") 
            
# Get location of word, location, and the same for the md5 version
def getWordInfo(word):
    print(f"Getting word: {word}")
    with open(newWordFile) as nWFile, open(newWordMD5File) as nWMD5File:
        for ln, line in enumerate(nWFile, 1):
            if word == line.strip():
                print(f"The word ({word}) was on line: {ln}")
    
    print(f"The MD5 code for {word} is {md5(word.upper())}")
                
    
            
        

#############################################################
# EXACT REPLICATION OF WORDTWIST MD5 ENCRYPTION IN PYTHON   #
# MAIN FUNCTION IS `md5(string)` STRING IS ALWAYS UPPERCASE #
############################################################# 

# Example Usage of MD5 hashing function: MD5("HELLO")
#                                               ^- Always upper case!
# The capitalization of the word in the translateCondensedIntoMD5 is handled automatically, but manual usage of the
# md5 function required you type in the word in all capitals.

def rotate_left(value, shift_bits):
    return (value << shift_bits) | (value >> (32 - shift_bits))

def add_unsigned(x, y):
    x8 = x & 0x80000000
    y8 = y & 0x80000000
    x4 = x & 0x40000000
    y4 = y & 0x40000000
    result = (x & 0x3FFFFFFF) + (y & 0x3FFFFFFF)

    if x4 & y4:
        return (result ^ 0x80000000 ^ x8 ^ y8)
    if x4 | y4:
        if result & 0x40000000:
            return (result ^ 0xC0000000 ^ x8 ^ y8)
        else:
            return (result ^ 0x40000000 ^ x8 ^ y8)
    else:
        return (result ^ x8 ^ y8)

def f(x, y, z): return (x & y) | (~x & z)
def g(x, y, z): return (x & z) | (y & ~z)
def h(x, y, z): return x ^ y ^ z
def i(x, y, z): return y ^ (x | ~z)

def ff(a, b, c, d, x, s, ac):
    a = add_unsigned(a, add_unsigned(add_unsigned(f(b, c, d), x), ac))
    return add_unsigned(rotate_left(a, s), b)

def gg(a, b, c, d, x, s, ac):
    a = add_unsigned(a, add_unsigned(add_unsigned(g(b, c, d), x), ac))
    return add_unsigned(rotate_left(a, s), b)

def hh(a, b, c, d, x, s, ac):
    a = add_unsigned(a, add_unsigned(add_unsigned(h(b, c, d), x), ac))
    return add_unsigned(rotate_left(a, s), b)

def ii(a, b, c, d, x, s, ac):
    a = add_unsigned(a, add_unsigned(add_unsigned(i(b, c, d), x), ac))
    return add_unsigned(rotate_left(a, s), b)

def convert_to_word_array(string):
    message_length = len(string)
    number_of_words_temp1 = message_length + 8
    number_of_words_temp2 = (number_of_words_temp1 - (number_of_words_temp1 % 64)) // 64
    number_of_words = (number_of_words_temp2 + 1) * 16
    word_array = [0] * number_of_words

    byte_position = 0
    byte_count = 0

    while byte_count < message_length:
        word_count = byte_count // 4
        byte_position = (byte_count % 4) * 8
        word_array[word_count] |= ord(string[byte_count]) << byte_position
        byte_count += 1

    word_count = byte_count // 4
    byte_position = (byte_count % 4) * 8
    word_array[word_count] |= 0x80 << byte_position
    word_array[number_of_words - 2] = message_length * 8
    word_array[number_of_words - 1] = message_length >> 29

    return word_array

def word_to_hex(value):
    hex_value = ""
    for i in range(4):
        byte = (value >> (i * 8)) & 255
        hex_value += "{:02x}".format(byte)
    return hex_value

def utf8_encode(string):
    return string.encode('utf-8').decode('latin-1')

def md5(string):
    string = utf8_encode(string)
    x = convert_to_word_array(string)

    a = 0x67452301
    b = 0xEFCDAB89
    c = 0x98BADCFE
    d = 0x10325476

    s11, s12, s13, s14 = 7, 12, 17, 22
    s21, s22, s23, s24 = 5, 9, 14, 20
    s31, s32, s33, s34 = 4, 11, 16, 23
    s41, s42, s43, s44 = 6, 10, 15, 21

    for k in range(0, len(x), 16):
        aa, bb, cc, dd = a, b, c, d

        a = ff(a, b, c, d, x[k + 0], s11, 0xD76AA478)
        d = ff(d, a, b, c, x[k + 1], s12, 0xE8C7B756)
        c = ff(c, d, a, b, x[k + 2], s13, 0x242070DB)
        b = ff(b, c, d, a, x[k + 3], s14, 0xC1BDCEEE)
        a = ff(a, b, c, d, x[k + 4], s11, 0xF57C0FAF)
        d = ff(d, a, b, c, x[k + 5], s12, 0x4787C62A)
        c = ff(c, d, a, b, x[k + 6], s13, 0xA8304613)
        b = ff(b, c, d, a, x[k + 7], s14, 0xFD469501)
        a = ff(a, b, c, d, x[k + 8], s11, 0x698098D8)
        d = ff(d, a, b, c, x[k + 9], s12, 0x8B44F7AF)
        c = ff(c, d, a, b, x[k + 10], s13, 0xFFFF5BB1)
        b = ff(b, c, d, a, x[k + 11], s14, 0x895CD7BE)
        a = ff(a, b, c, d, x[k + 12], s11, 0x6B901122)
        d = ff(d, a, b, c, x[k + 13], s12, 0xFD987193)
        c = ff(c, d, a, b, x[k + 14], s13, 0xA679438E)
        b = ff(b, c, d, a, x[k + 15], s14, 0x49B40821)
        a=gg(a,b,c,d,x[k+1], s21,0xF61E2562);
        d=gg(d,a,b,c,x[k+6], s22,0xC040B340);
        c=gg(c,d,a,b,x[k+11],s23,0x265E5A51);
        b=gg(b,c,d,a,x[k+0], s24,0xE9B6C7AA);
        a=gg(a,b,c,d,x[k+5], s21,0xD62F105D);
        d=gg(d,a,b,c,x[k+10],s22,0x2441453);
        c=gg(c,d,a,b,x[k+15],s23,0xD8A1E681);
        b=gg(b,c,d,a,x[k+4], s24,0xE7D3FBC8);
        a=gg(a,b,c,d,x[k+9], s21,0x21E1CDE6);
        d=gg(d,a,b,c,x[k+14],s22,0xC33707D6);
        c=gg(c,d,a,b,x[k+3], s23,0xF4D50D87);
        b=gg(b,c,d,a,x[k+8], s24,0x455A14ED);
        a=gg(a,b,c,d,x[k+13],s21,0xA9E3E905);
        d=gg(d,a,b,c,x[k+2], s22,0xFCEFA3F8);
        c=gg(c,d,a,b,x[k+7], s23,0x676F02D9);
        b=gg(b,c,d,a,x[k+12],s24,0x8D2A4C8A);
        a=hh(a,b,c,d,x[k+5], s31,0xFFFA3942);
        d=hh(d,a,b,c,x[k+8], s32,0x8771F681);
        c=hh(c,d,a,b,x[k+11],s33,0x6D9D6122);
        b=hh(b,c,d,a,x[k+14],s34,0xFDE5380C);
        a=hh(a,b,c,d,x[k+1], s31,0xA4BEEA44);
        d=hh(d,a,b,c,x[k+4], s32,0x4BDECFA9);
        c=hh(c,d,a,b,x[k+7], s33,0xF6BB4B60);
        b=hh(b,c,d,a,x[k+10],s34,0xBEBFBC70);
        a=hh(a,b,c,d,x[k+13],s31,0x289B7EC6);
        d=hh(d,a,b,c,x[k+0], s32,0xEAA127FA);
        c=hh(c,d,a,b,x[k+3], s33,0xD4EF3085);
        b=hh(b,c,d,a,x[k+6], s34,0x4881D05);
        a=hh(a,b,c,d,x[k+9], s31,0xD9D4D039);
        d=hh(d,a,b,c,x[k+12],s32,0xE6DB99E5);
        c=hh(c,d,a,b,x[k+15],s33,0x1FA27CF8);
        b=hh(b,c,d,a,x[k+2], s34,0xC4AC5665);
        a=ii(a,b,c,d,x[k+0], s41,0xF4292244);
        d=ii(d,a,b,c,x[k+7], s42,0x432AFF97);
        c=ii(c,d,a,b,x[k+14],s43,0xAB9423A7);
        b=ii(b,c,d,a,x[k+5], s44,0xFC93A039);
        a=ii(a,b,c,d,x[k+12],s41,0x655B59C3);
        d=ii(d,a,b,c,x[k+3], s42,0x8F0CCC92);
        c=ii(c,d,a,b,x[k+10],s43,0xFFEFF47D);
        b=ii(b,c,d,a,x[k+1], s44,0x85845DD1);
        a=ii(a,b,c,d,x[k+8], s41,0x6FA87E4F);
        d=ii(d,a,b,c,x[k+15],s42,0xFE2CE6E0);
        c=ii(c,d,a,b,x[k+6], s43,0xA3014314);
        b=ii(b,c,d,a,x[k+13],s44,0x4E0811A1);
        a=ii(a,b,c,d,x[k+4], s41,0xF7537E82);
        d=ii(d,a,b,c,x[k+11],s42,0xBD3AF235);
        c=ii(c,d,a,b,x[k+2], s43,0x2AD7D2BB);
        b=ii(b,c,d,a,x[k+9], s44,0xEB86D391);

        a = add_unsigned(a, aa)
        b = add_unsigned(b, bb)
        c = add_unsigned(c, cc)
        d = add_unsigned(d, dd)

    return (word_to_hex(a) + word_to_hex(b) + word_to_hex(c) + word_to_hex(d)).lower()
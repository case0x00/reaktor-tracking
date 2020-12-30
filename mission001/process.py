#!/usr/bin/env python3

import base64

with open("data") as f:
    content = f.read()

def string_to_list(word):
    return [char for char in word]

def window(seq):
    for i in range(0, len(seq)-16):
        sub_seq = seq[i:i+16]
        # check if sub_seq has uniq chars
        sub_seq_uniq = set(sub_seq)
        # if lens are same, sub_seq is unique
        if len(sub_seq_uniq) == len(sub_seq):
            return sub_seq

# finding uniq as a string
uniq_content_str = ''.join(window(string_to_list(content)))

# decoding b64
decoded_bytes = base64.b64decode(uniq_content_str)
decoded_str = str(decoded_bytes, "utf-8")
print(f"b64 decoded string is: {decoded_str}")
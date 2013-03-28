#!/usr/bin/env python

# used for printing more debuging messages if app runs in verbose mode

__verbose_mode = False


def debug_message(text):
    global __verbose_mode
    if __verbose_mode:
        print text + '\n'
    return

def set_verbose_mode(mode):
    global __verbose_mode
    __verbose_mode = mode
    return

#!/usr/bin/python
'''
per ora provo un semplice menu
'''

def comando():
    pass

def add_manga():
    pass

dmenu={
        1 : ['Prima scelta',comando],
        2 : ['Seconda scelta', comando]
        }

def display_menu(choices):
    for key in choices:
        print "%s : %s" % (key, choices[key][0])



if __name__ == "__main__":
    display_menu(dmenu)


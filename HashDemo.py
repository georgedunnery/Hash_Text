# George Dunnery - CS 5800

from Hash import *

# GLOBAL variable for output file
FILE = "hash_text_output.txt"
URL = "http://www.ccs.neu.edu/home/vip/teach/Algorithms/" \
      "7_hash_RBtree_simpleDS/hw_hash_RBtree/alice_in_wonderland.txt"


def main():
    t = TextHash(17, 701)
    t.process_web_text(URL)
    t.save(FILE)

    print(t.chain_lengths())
    print(t.average_collisions())


main()

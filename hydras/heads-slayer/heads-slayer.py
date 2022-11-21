# Head Slayer
#
# Author: Guillaume Michel
#
# Description: This script takes as input a list of peerids (one per line) from a text file,
# and creates text files with a fraction of the shallowest peerids from the input list. It
# builds a binary trie to determine the depth of each peerid, and orders them by depth.
# The PERCENTILE variable can be edited to generate list with different numbers of peerids.

from random import shuffle

import multihash as mh
import hashlib as hl

from binary_trie import Trie, bytes_to_bitstring

PERCENTILES = [25, 50, 75]
HEADS_FILENAME = "heads.list"

# turn a peer_id (e.g 12D3KooWEZXjE41uU4EL2gpkAQeDXYok6wghN7wwNVPF5bwkaNfS) to its
# sha256 hash representation (256 bits), used as kademlia identifier
def multihash_to_kad_id(peer_id: str) -> bytes:
    multi_hash = mh.from_b58_string(peer_id)
    return hl.sha256(multi_hash).digest()


if __name__ == "__main__":
    f = open(HEADS_FILENAME, "r")
    heads = [s[:-1] for s in f.readlines()]  # remove trailing '\n'
    f.close()

    keys = []

    # create the binary trie
    t = Trie()
    for h in heads:
        bitstring = bytes_to_bitstring(multihash_to_kad_id(h))
        keys.append(bitstring)
        t.add(bitstring, h)

    # get the depth of all nodes in the binary trie
    depth_map = {}
    for k in keys:
        d = t.depth(k)
        if d not in depth_map:
            depth_map[d] = []
        else:
            depth_map[d].append(t.find(k))

    # number of peerids for each truncated list
    limits = [int(len(heads) * n / 100) for n in PERCENTILES]

    # truncated lists of peerids
    # e.g list with 25%, 50% and 75% of the shallowest peerids
    lists = []
    for i in PERCENTILES:
        lists.append([])

    # iterate on the depths
    for i in range(len(keys[0])):
        # if no peerid is at depth i, continue
        if i not in depth_map:
            continue

        # iterate on the lists of peerids, and complete them
        for n in range(len(PERCENTILES)):
            if len(depth_map[i]) + len(lists[n]) > limits[n]:
                # there are more peerids with depth i, than spots left in the list of peerids,
                # the right number of peerids is randomly selected

                # randomize list
                shuffle(depth_map[i])
                # take the first elements until the number of heads is reached
                lists[n] += depth_map[i][: limits[n] - len(lists[n])]
            else:
                # If all peers at depth i fit the list, add all peerids to lists[n]
                lists[n] += depth_map[i]

    # write the peerids lists to files "heads-slayed-XX.list"
    for i in range(len(PERCENTILES)):
        f = open("heads-slayed-" + str(PERCENTILES[i]) + ".list", "w")
        f.writelines([peerid + "\n" for peerid in lists[i]])
        f.close()

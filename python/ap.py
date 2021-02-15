import sys

import general
from hashmap import hashmap_t
import airports

def msg0(s):
    general.msg(0, s)
def msg1(s):
    general.msg(1, s)

def count_reachable(code):
    #
    # Print out the  number of airports reachable from airport code
    # Also count the start airport itself!
    #
    
    # Use this format!
    count = -1
    print("%d airports reachable from %s" % (count, code))
    
def compute_route(algo, scode, dcode):
    s = airports.ap_get_id(scode)
    d = airports.ap_get_id(dcode)
    g = airports.ap_get_graph()
    
    # Computer a shortest route between s and d, using the specified algorithm!
    # "bfs" should compute a route with minimal hops, all other algorithms compute a route with minimal milage
    #
    
    if (algo == "bellman-ford"):
        pass
    elif (algo == "dijkstra"):
        pass
    elif (algo == "astar"):
        pass
    elif (algo == "bfs"):
        pass
    else:
        general.error("Invalid algorithm name: %s" % algo)
        
    # Output one line per hop, indicating source, destination, and length
    # Finally, output the total length
    print("%s to %s (%dkm)" % ("MAN", "HEL", 1812))
    print("%s to %s (%dkm)" % ("HEL", "HKG", 7810))
    print("%s to %s (%dkm)" % ("HKG", "SYD", 7394))
    print("Total = %dkm" % 17016)
    
    # If there is no route ...
    print("No route from %s to %s" % (scode, dcode))
    
    # And, in any case, log the number of relaxed/explored edges
    msg0("relaxed %d edges\n" % 1896)
    
airports.ap_std_init()

if (len(sys.argv) == 5 and sys.argv[1] == "route"):
    compute_route(sys.argv[2], sys.argv[3], sys.argv[4])
elif (len(sys.argv) == 3 and sys.argv[1] == "count"):
    count_reachable(sys.argv[2])
else:
    general.error("Invalid command line")
    
    

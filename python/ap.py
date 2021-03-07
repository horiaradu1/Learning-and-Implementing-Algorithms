import sys

import general
from hashmap import hashmap_t
import airports

from sp_algorithms import bfs, bellman_ford, dijkstra, astar_search
from shortest_path import sssp_result_t, sp_result_t
import graph
import weight
from math import sqrt
import random

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
    s = airports.ap_get_id(code)
    d = graph.INVALID_NODE
    g = airports.ap_get_graph()

    sssp = bfs(g, s ,d)
    count += 1
    for i in sssp.dist:
        if not weight.weight_eq(i , weight.weight_inf()):
            count += 1

    print("%d airports reachable from %s" % (count, code))
    
def compute_route(algo, scode, dcode):
    s = airports.ap_get_id(scode)
    d = airports.ap_get_id(dcode)
    g = airports.ap_get_graph()

    stat_edges_explored = -1
    
    # Computer a shortest route between s and d, using the specified algorithm!
    # "bfs" should compute a route with minimal hops, all other algorithms compute a route with minimal milage
    #

    def heuristic(g, d):

        class point_t:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        def coords_dist(coords, u, v):
            dx = coords[u].x - coords[v].x
            dy = coords[u].y - coords[v].y
    
            return weight.weight_t(round(sqrt(dx*dx + dy*dy)))

        N = g.graph_get_num_nodes()
        h = [weight.weight_zero()] * N
        coords = [point_t(0, 0)]*N

        for key, code in enumerate(airports.airports):
            if code is not None:
                coords[key].u = code.lat
                coords[key].v = code.lng

        for u in range(0, N):
            h[u] = coords_dist(coords, u, d)

        return h

    h = heuristic(g, d)

    def print_algo_path(algorithm, algo_name):
        #print("Using algo: %a" % algo_name)
        if algo_name == "astar":
            sp = algorithm
            stat_edges_explored = sp.relax_count
            if sp.path != None:
                total = sp.dist.weight_to_int()
        else:
            sssp = algorithm
            stat_edges_explored = sssp.relax_count
            sp = sssp.sssp_to_sp_result(d)
            if sp.path != None:
                total = sssp.dist[d].weight_to_int()

        #if sssp.pred[d] is graph.INVALID_NODE or sssp.dist[d] is weight.weight_inf():
        if sp.path == None:
            print("No route from %s to %s" % (scode, dcode))
        else:
            path = sp.path.nodes
            airport_id = s
            airport_code = scode
            for i in path[1:]:
                km = -1
                for edge in g.get_graph_succs(airport_id):
                    v = edge.v
                    if v == i:
                        km = edge.w.weight_to_int()
                next_airport_code = airports.ap_get_code(i)
                print("%s to %s (%dkm)" % (airport_code, next_airport_code, km))
                airport_id = i
                airport_code = next_airport_code
            print("Total = %dkm" % total)
        
        msg0("relaxed %d edges\n" % stat_edges_explored)
    
    
    if (algo == "bellman-ford"):
        print_algo_path(bellman_ford(g, s), algo)
        
    elif (algo == "dijkstra"):
        print_algo_path(dijkstra(g, s, d), algo)
        
    elif (algo == "astar"):
        print_algo_path(astar_search(g, s, d, h), algo)
        
    elif (algo == "bfs"):
        print_algo_path(bfs(g, s, d), algo)
    
    else:
        general.error("Invalid algorithm name: %s" % algo)
        
    # # Output one line per hop, indicating source, destination, and length
    # # Finally, output the total length
    # print("%s to %s (%dkm)" % ("MAN", "HEL", 1812))
    # print("%s to %s (%dkm)" % ("HEL", "HKG", 7810))
    # print("%s to %s (%dkm)" % ("HKG", "SYD", 7394))
    # print("Total = %dkm" % 17016)
    
    # # If there is no route ...
    # print("No route from %s to %s" % (scode, dcode))
    
    # # And, in any case, log the number of relaxed/explored edges
    #msg0("relaxed %d edges\n" % stat_edges_explored)

    #print("\n----END----")
    
airports.ap_std_init()

if (len(sys.argv) == 5 and sys.argv[1] == "route"):
    compute_route(sys.argv[2], sys.argv[3], sys.argv[4])
elif (len(sys.argv) == 3 and sys.argv[1] == "count"):
    count_reachable(sys.argv[2])
else:
    general.error("Invalid command line")
    
    

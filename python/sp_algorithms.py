import graph
import pq
import general
from shortest_path import sssp_result_t, sp_result_t
import weight

from queue import Queue
from hashmap import hashmap_t, HashingModes

def bfs(g, src, dst):
    # Breadth-first search algorithm

    # Declaration of the main variables
    stat_edges_explored = 0
    N = g.graph_get_num_nodes()
    pred = [graph.INVALID_NODE]*N
    dist = [weight.weight_inf()]*N
    
    D = Queue()
    F = hashmap_t(N, HashingModes.HASH_1_LINEAR_PROBING)
    D.put(src)
    pred[src] = src
    dist[src] = weight.weight_zero()
    # Does the first node (src) count towards stat_edges_explored
    #stat_edges_explored += 1

    # While the searching queue is not empty
    while not D.empty():
        u = D.get(0)
        # Can break after finding the dst node, as this algorithm already is looking first for the shortest paths, node wise
        # if u == dst:
        #     break
        F.hashmap_insert(str(u), u)
        for edge in g.get_graph_succs(u):
            v = edge.v
            if F.hashmap_lookup(str(v)) is None and pred[v] is graph.INVALID_NODE:
                # and pred[v] is graph.INVALID_NODE -- not been through the node already
                # F.hashmap_lookup(str(v)) is None -- check if node v already in finished
                D.put(v)
                pred[v] = u
                dist[v] = weight.weight_add(dist[u], edge.w)
                stat_edges_explored += 1

    return sssp_result_t(N, src, dst, False, pred, dist, stat_edges_explored)
    
def bellman_ford(g, src):
    # Bellman Ford algorithm + its negative cycle posibility

    # Function to initiate the queue
    def init_estimate(g, s):
        N = g.graph_get_num_nodes()
        D = [weight.weight_inf()]*N
        D[s] = weight.weight_zero()
        return D

    # Function for the relaxation of a node and edge
    # That returns True if the node was able to be relaxed
    def relax(g, D, u, v):
        w_u_v = weight.weight_inf()
        for edge in g.get_graph_succs(u):
            if edge.v == v:
                w_u_v = edge.w  #w(u,v)
        if weight.weight_less((weight.weight_add(D[u], w_u_v)), D[v]):
            D[v] = weight.weight_add(D[u], w_u_v)
            return True
        return False

    stat_edges_explored = 0
    N = g.graph_get_num_nodes()
    pred = [graph.INVALID_NODE]*N
    has_negative_cycle = False
    negative = False

    D = init_estimate(g, src)
    pred[src] = src
    # Does the first node (src) count towards stat_edges_explored
    #stat_edges_explored += 1

    for i in range(N-1):
        # Guilty until proven innocent :)
        negative = True
        for u in range(N):
            for edge in g.get_graph_succs(u):
                v = edge.v
                if not edge.w.weight_is_inf() and relax(g, D, u, v):
                    pred[v] = u
                    stat_edges_explored += 1
                    negative = False
        # If it iterated D and did not change anything
        # Go then and check for a negative cycle
        if negative is True:
            break

    for u in range(N):
        for edge in g.get_graph_succs(u):
            v = edge.v
            # If it still works to change D in the new iteration
            # Then it is a negative cycle
            if relax(g, D, u, v):
                stat_edges_explored += 1
                has_negative_cycle = True
                D[v] = weight.weight_neg_inf()


    return sssp_result_t(N, src, graph.INVALID_NODE, has_negative_cycle, pred, D, stat_edges_explored)
    
def dijkstra(g, src, dst):

    # Function to initiate the priority queue
    def init_estimate(g, s):
        N = g.graph_get_num_nodes()
        D = pq.DPQ_t(N)
        for i in range(N):
            if i == s:
                D.DPQ_insert(s, weight.weight_zero())
            else:
                D.DPQ_insert(i, weight.weight_inf())
        return D

    # Relax function
    def relax(g, D, u, pred):
        for edge in g.get_graph_succs(u):
            v = edge.v
            w_v = edge.w
            if D.DPQ_contains(v):
                w_u_v = weight.weight_add(D.DPQ_prio(u), w_v)
                if weight.weight_less(w_u_v, D.DPQ_prio(v)) and not w_u_v.weight_is_inf():
                    D.DPQ_decrease_key(v, w_u_v)
                    pred[v] = u

    # Init variables
    stat_edges_explored = 0
    N = g.graph_get_num_nodes()
    pred = [graph.INVALID_NODE]*N
    #dist = [weight.weight_neg_inf()]*N
    dist = []
    
    D = init_estimate(g, src)
    pred[src] = src
    # Does the first node (src) count towards stat_edges_explored
    #stat_edges_explored += 1
    
    # Relax each node while the queue is not empty
    while D.DPQ_is_empty() is False:
        u = D.DPQ_pop_min()
        relax(g, D, u, pred)
        stat_edges_explored += 1

    # Could put D.DPQ_dist_free() directly in return
    # Add each element from the DPQ in the dist list
    for i in D.DPQ_dist_free():
        dist.append(i)

    return sssp_result_t(N, src, dst, False, pred, dist, stat_edges_explored)
    
def astar_search(g, src, dst, h):

    global stat_edges_explored

    # Function to initiate the priority queue
    def init_estimate(g, s, h):
        N = g.graph_get_num_nodes()
        D = pq.DPQ_t(N)
        for i in range(N):
            if i == s:
                D.DPQ_insert(s, h[s])
            else:
                D.DPQ_insert(i, weight.weight_inf())
        return D

    # Relax function with heuristics included
    # That also goes through the edge and checks each statement
    def relax(g, D, u, pred, dist, h):
        global stat_edges_explored
        w_u = D.DPQ_prio(u)
        for edge in g.get_graph_succs(u):
            v = edge.v
            w_v = edge.w
            if D.DPQ_contains(v):
                # Calculate with the heuristics into a new weight
                w_u_v = weight.weight_add(w_u, w_v)
                h_v_minus_h_u = weight.weight_sub(h[v], h[u])
                new_w_u_v = weight.weight_add(w_u_v, h_v_minus_h_u)
                if weight.weight_less(new_w_u_v, D.DPQ_prio(v)) and not new_w_u_v.weight_is_inf():
                    # Then relax the node and go to the next
                    stat_edges_explored += 1
                    D.DPQ_decrease_key(v, new_w_u_v)
                    pred[v] = u
                    #dist[v] = weight.weight_add(w_u, w_u_v)
        
    stat_edges_explored = 0
    N = g.graph_get_num_nodes()
    pred = [graph.INVALID_NODE]*N
    dist = [weight.weight_inf()]*N

    D = init_estimate(g, src, h)
    pred[src] = src
    #dist[src] = weight.weight_zero()
    # Does the first node (src) count towards stat_edges_explored
    #stat_edges_explored += 1

    # Relax each node while the queue is not empty
    while D.DPQ_is_empty() is False:
        u = D.DPQ_pop_min()

        # If the dst is reached
        if u == dst:
            # Then return D[dst] and exit loop
            break

        relax(g, D, u, pred, dist, h)

    # Make sure the dst in dist is assigned after exiting while loop
    # dist = D.DPQ_dist_free()
    # dist[dst] = weight.weight_sub(dist[dst], h[dst])
    # There is no need for dist in the A*, as the dst is returned directly

    # Return just the dst
    return sssp_result_t(N, src, dst, False, pred, D.DPQ_dist_free(), stat_edges_explored).sssp_to_sp_result(dst)

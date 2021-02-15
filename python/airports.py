import math

from hashmap import hashmap_t, HashingModes
import general
from graph import graph_t
import weight

R = 6371
TO_RAD = (3.1415926536 / 180)

def dist(lat1, lng1, lat2, lng2):
    lng1 = lng1 - lng2
    lng1 = lng1 * TO_RAD
    lat1 = lat1 * TO_RAD
    lat2 = lat2 * TO_RAD
    
    dz = math.sin(lat1) - math.sin(lat2)
    dx = math.cos(lng1) * math.cos(lat1) - math.cos(lat2)
    dy = math.sin(lng1) * math.cos(lat1)
    return math.asin(math.sqrt(dx * dx + dy * dy + dz * dz) / 2) * 2 * R
    
class airport_t:
    def __init__(self, code, lat, lng):
        self.code = code
        self.lat = lat
        self.lng = lng
        
num_apids = 0
airports = None
code_id_map = None

route_g = None

def ap_get_num_ids():
    return num_apids
    
def ap_read(f):
    global airports, code_id_map, num_apids
    
    assert (airports == None and code_id_map == None)
    
    num_apids = int(f.readline())
    n = int(f.readline())
    
    airports = [None]*num_apids
    
    code_id_map = hashmap_t(num_apids, HashingModes.HASH_1_LINEAR_PROBING)
    
    for i in range(0, n):
        (id_string, code, lat_string, lng_string) = f.readline().split()
        
        id = int(id_string)
        
        if (not id < num_apids):
            general.error("Invalid airport ID: %d", id)
            
        airports[id] = airport_t(code, float(lat_string), float(lng_string))
        
        code_id_map.hashmap_insert(code, id)
        
def ap_read_routes(f):
    global route_g
    
    num_edges = int(f.readline())
    
    assert (route_g == None)
    
    route_g = graph_t(ap_get_num_ids())
    
    for i in range(0, num_edges):
        (id1_string, id2_string) = f.readline().split()
        id1 = ap_check_id(int(id1_string))
        id2 = ap_check_id(int(id2_string))
        
        dist = ap_get_dist(id1, id2)
        
        route_g.graph_add_edge(id1, dist, id2)
        
def fopenchk(name, mode):
    try:
        f = open(name, mode)
        return f
    except:
        general.error("Error opeining %s for %s" % (name, mode))
        
def ap_std_init():
    f = fopenchk("../data/airports.txt", "r")
    ap_read(f)
    f.close()
    
    f = fopenchk("../data/routes.txt", "r")
    ap_read_routes(f)
    f.close()
    
def ap_get_graph():
    return route_g
    
def ap_get_dist(id1, id2):
    return weight.weight_t(round(ap_get_dist_dbl(id1, id2)))
    
def ap_is_valid_id(id):
    return id < num_apids and airports[id] != None and airports[id].code != "0"
    
def ap_invalidate_id(id):
    assert(id < num_apids)
    # Note: As our hashtables do not support delete, we insert a validity check after retrieving a code
    airports[id].code = "0"
    
def ap_check_id(id):
    if (not ap_is_valid_id(id)):
        general.error("Invalid aiport id: %d" % id)
    return id
    
def ap_get_code(id):
    assert (ap_is_valid_id(id))
    return airports[id].code
    
def ap_get_lat(id):
    assert (ap_is_valid_id(id))
    return airports[id].lat
    
def ap_get_lng(id):
    assert (ap_is_valid_id(id))
    return airports[id].lng
    
def ap_get_id_aux(code):
    return code_id_map.hashmap_lookup(code)
    
def ap_is_valid_code(code):
    res = None
    res = ap_get_id_aux(code)
    return res != None and ap_is_valid_id(res)
    
def ap_get_id(code):
    res = ap_get_id_aux(code)
    if (res == None or not (ap_is_valid_id(res))):
        general.error("Unknown airport ID: %s" % code)
    return res

def ap_get_dist_dbl(id1, id2):
    return dist(ap_get_lat(id1), ap_get_lng(id1), ap_get_lat(id2), ap_get_lng(id2))

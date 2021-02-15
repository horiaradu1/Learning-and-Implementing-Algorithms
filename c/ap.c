#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <stdbool.h>
#include <assert.h>
#include <math.h>

#include "general.h"
#include "sp_algorithms.h"
#include "hashmap.h"
#include "airports.h"


void count_reachable(char const *code) {
  /**
   * Print out the number of airports reachable from airport code.
   * Also count the start airport itself!
   */

  // Use this format!
  size_t count = -1;
  printf("%zu airports reachable from %s\n",count,code);


}

void compute_route(char const *algo, char const *scode, char const *dcode) {
  node_t s=ap_get_id(scode);
  node_t d=ap_get_id(dcode);
  graph_t const *g = ap_get_graph();

  /** Compute a shortest route between s and d, using the specified algorithm!
   *  "bfs" should compute a route with minimal hops, all other algorithms compute a route with minimal mileage
   */

  if (strcmp(algo,"bellman-ford")==0) ;
  else if (strcmp(algo,"dijkstra")==0) ;
  else if (strcmp(algo,"astar")==0) ;
  else if (strcmp(algo,"bfs")==0) ;
  else error("Invalid algorithm name: %s", algo);

  /**
   * Output one line per hop, indicating source, destination, and length.
   * Finally, output the total length
   */
  printf("%s to %s (%ldkm)\n","MAN","HEL",(long)1812);
  printf("%s to %s (%ldkm)\n","HEL","HKG",(long)7810);
  printf("%s to %s (%ldkm)\n","HKG","SYD",(long)7394);
  printf("Total = %ldkm\n",(long)17016);

  /// If there is no route ...
  printf("No route from %s to %s\n",scode,dcode);


  /// And, in any case, log the number of relaxed/explored edges
  msg0("relaxed %llu edges\n", (unsigned long long)1896);

}


int main(int argc, char **argv)
{

  ap_std_init();

  if (argc==5 && strcmp(argv[1],"route")==0) compute_route(argv[2],argv[3],argv[4]);
  else if (argc==3 && strcmp(argv[1],"count")==0) count_reachable(argv[2]);
  else error("Invalid command line");

  ap_delete();

  return 0;
}


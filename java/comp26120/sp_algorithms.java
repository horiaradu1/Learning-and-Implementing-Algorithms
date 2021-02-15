package comp26120;

import java.util.ArrayList;

public class sp_algorithms {

    public static final void error (String msg) {
	System.err.println(msg);
	System.exit(1);
    }

    public static sssp_result_t bfs(graph_t g, node_t src, node_t dst) {
	long stat_edges_explored=0;

	int N = g.graph_get_num_nodes();

	ArrayList<node_t> pred = new ArrayList<node_t>();
	ArrayList<weight_t> dist = new ArrayList<weight_t>();

	error("Not implemented");

	return new sssp_result_t(N, src, dst, false, pred, dist, stat_edges_explored);
    }

    public static sssp_result_t bellman_ford(graph_t g, node_t src) {
	error("Not implemented");

	return null;
    }

    public static sssp_result_t dijkstra(graph_t g, node_t src, node_t dst) {
	error("Not implemented");

	return null;
    }

    public static sp_result_t astar_search(graph_t g, node_t src, node_t dst, weight_t[] h) {
	error("Not implemented");

	return null;
    }

}

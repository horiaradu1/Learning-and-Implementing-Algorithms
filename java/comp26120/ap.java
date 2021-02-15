package comp26120;

public class ap {
    airports airport_info = new airports();
    general settings;

    public ap(general settings) {
        this.settings = settings;
    }

    private static char[] code_string_to_code(String code_string) {
	char [] code = new char[4];
	for (int i = 0; i < 3; i++) {
	    code[i] = code_string.charAt(i);
	}
	code[3] = 0;
	return code;
    }
    
    public static void count_reachable(String code_string) {
	char[] code = code_string_to_code(code_string);
	
	/**
	 * Print out the number of airports reachalbe from airport code.
	 * Also count the start airport itself!
	 */

	// Use this format!
	int count = -1;
	System.out.format("%d airports reachable from %s\n",count,code);
    }

    public void compute_route(String algo, String scode_string, String dcode_string) {
	char[] scode = code_string_to_code(scode_string);
	char[] dcode = code_string_to_code(dcode_string);
	
	airports.apid_t s = airport_info.ap_get_id(scode);
	airports.apid_t d = airport_info.ap_get_id(dcode);
	graph_t g = airport_info.ap_get_graph();

	/** Compute the shortest route between s and d, using the specified algorithms!
	 * "bfs" should compute a route with minimal hops, all other algorithms compute a route with minimal mileage
	 */

	if (algo.equals("bellman-ford")) {
	} else if (algo.equals("dijkstra")) {
	} else if (algo.equals("astar")) {
	} else if (algo.equals("bfs")) {
	} else {
	    sp_algorithms.error ("Invalid algorithm name: " + algo);
	}

	/**
	 * Output one line per hop, indicating source, destination, and lenght
	 * Finally, output the total lenght
	 */

	System.out.format("%s to %s (%dkm)\n", "MAN", "HEL", 1812);
	System.out.format("%s to %s (%dkm)\n", "HEL", "HKG", 7810);
	System.out.format("%s to %s (%dkm)\n", "HKG", "SYD", 7394);
	System.out.format("Total = %dkm\n",17016);

	/// If there is no route ...
	System.out.format("No route from %s to %s\n",scode,dcode);

	/// And, in any case, log the number of relaxed/explored edges
	System.out.format("LOG: relaxed %d edges\n\n", 1896);
    }

    public static void main(String[] args) {
	general general_settings = new general();
        general_settings.set_msg_verb(-1);

        ap ap = new ap(general_settings);
        ap.airport_info.ap_std_init();

	if (args.length == 5 && args[0].equals("route")) {
	    ap.compute_route(args[1],args[2],args[3]);
	} else if (args.length == 3 && args[0].equals("count")) {
	    ap.count_reachable(args[1]);
	} else {
	    sp_algorithms.error("Invalid command line");
	}
    }
}

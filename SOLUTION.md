
|       Method 	    |   Local  	|   Same-Zone  	|   Different Region 	|
| ----------------- | --------- | ------------- | --------------------- |
| REST add	        |   2.599ms |    3.5ms      |  	       345.100ms    |
| gRPC add	        |   1.577ms	|   1.343ms     |    	   184.253ms    |
| REST rawimg	    |   7.445ms	|    7.780ms    |   	  1411.830ms    |
| gRPC rawimg	    |  15.689ms |   16.207ms    |   	  204.406ms     |
| REST dotproduct	|   4.819ms	|    3.924ms    |  	      343.393ms     |
| gRPC dotproduct	|   1.496ms	|   1.535ms     |    	  165.322ms     |
| REST jsonimg	    |  49.397ms |   41.310ms    |   	  1634.208ms    |
| gRPC jsonimg	    |  37.955ms |   44.357ms    |   	   231.326ms    |
| PING              |  0.045ms  |   0.438ms     |           141ms       |

You should measure the basic latency  using the `ping` command - this can be construed to be the latency without any RPC or python overhead.

You should examine your results and provide a short paragraph with your observations of the performance difference between REST and gRPC. You should explicitly comment on the role that network latency plays -- it's useful to know that REST makes a new TCP connection for each query while gRPC makes a single TCP connection that is used for all the queries.
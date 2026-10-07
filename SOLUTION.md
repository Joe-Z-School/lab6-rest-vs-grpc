
|       Method 	    |   Local  	|   Same-Zone  	|   Different Region 	|
| ----------------- | --------- | ------------- | --------------------- |
| REST add	        |   2.599ms |   	        |  	                    |
| gRPC add	        |   1.577ms	|   	        |    	                |
| REST rawimg	    |   7.445ms	|   	        |   	                |
| gRPC rawimg	    |  15.689ms |   	        |   	                |
| REST dotproduct	|   4.819ms	|   	        |  	                    |
| gRPC dotproduct	|   1.496ms	|   	        |    	                |
| REST jsonimg	    |  49.397ms |   	        |   	                |
| gRPC jsonimg	    |  37.955ms |   	        |   	                |
| PING              |  0.045ms  |               |                       |

You should measure the basic latency  using the `ping` command - this can be construed to be the latency without any RPC or python overhead.

You should examine your results and provide a short paragraph with your observations of the performance difference between REST and gRPC. You should explicitly comment on the role that network latency plays -- it's useful to know that REST makes a new TCP connection for each query while gRPC makes a single TCP connection that is used for all the queries.

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

## Observations
- Some interesting observations I made is that even though grpc uses protobufs methods and technology to compress, full-duplex communicate, and multiplex, the local timings of the raw image sending took longer than the REST application. Other than the raw image however, all other timings show that the gRPC method will send data slightly faster than a REST method. Moving to the same zone setup, I notice that the sending of image data appears to be quicker using the REST application over the gRPC application. My thought on this is because when you send images via REST, the network layer handles the transmission as raw stream of I/O bytes without serialization and parsing. Using gRPC however requires all the data to pass through protobufs serialization. Meaning the raw bytes are wrapped into a protobuf message field, causing much more overhead and time. As for the other features, the gRPC method transports the data in roughly have the time. The last but most important timings that entail different zone transporting, the gRPC method significantly outpreforms the REST method in all aspects. The important aspect is noticing that as base latency increases, the better gRPC will preform over applications like REST. Because of RESTs head of line blocking and creation of a new connection each request, REST suffers from severe bottlenecks. While the multiplexing, TCP reuse, and header compression for gRPC at first caused extra time, those features now become very efficient and offest the serialization costs.
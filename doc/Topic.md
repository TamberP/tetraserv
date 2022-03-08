# byond.topic

A python module for sending packets to BYOND servers, for calling
`/world/Topic()`

## Exports
### `send(address, port, query)`

Sends a Topic() packet to the specified server, and (ideally) returns
the response from the server.
* `address`: The address (IP, or DNS) of the target DreamDaemon
  instance to send the Topic() packet to.
* `port`: Port that the DreamDaemon instance is serving the world on
* `query`: Query string to be sent.

Returns: A tuple containing the response-type, and the response from the server.

If the response-type is `TOPIC_RESPONSE_STRING`, the response will be
a dict of key-value pairs, parsed out from the URL query-format string
returned from the server.

The actual data returned from the server depends on the codebase that
the server is running, and the query that was sent.

If the response-type is `TOPIC_RESPONSE_FLOAT`, the response will be a
floating point numeric value.

(`send` automatically opens a socket, transmits the packet, receives
the reply, and then closes the socket again.)

### Constants

* `TOPIC_PACKET_ID`: The signature that identifies a Topic() packet.
* `TOPIC_RESPONSE_STRING`: Response-type: string
* `TOPIC_RESPONSE_FLOAT`: Response-type: float/numeric

## Examples

### Requesting World Status

```python

import byond.topic as Topic

responseType, responseData = Topic.send("localhost", 26200, '?status')
if(responseType == Topic.TOPIC_RESPONSE_STRING):
    print(f"We're currently playing a {responseData['mode'][0]} round on {responseData['map_name'][0]}, with {responseData['players'][0]} players!")
```

(The values available in your status response data depend on the
codebase you're querying. Try it and see, first!)

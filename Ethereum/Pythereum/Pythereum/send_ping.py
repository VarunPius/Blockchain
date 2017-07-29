from discovery import EndPoint, PingNode, PingServer

my_endpt = EndPoint(u'52.4.20.183', 30303, 30303)
their_endpt = EndPoint(u'127.0.0.1', 30303, 30303)  # Can use the IP from Ethereum list 

server = PingServer(my_endpt)

listen_thread = server.udp_listen()
listen_thread.start()

server.ping(their_endpt)

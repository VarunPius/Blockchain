import socket
import threading
import time
import struct
import rlp
from crypto import keccak256
from secp256k1 import PrivateKey
from ipaddress import ip_address

class EndPoint(obj):
    def __init__(self, address, udp_port, tcp_port):
        self.address = ip_address(address)
        self.udp_port = udp_port
        self.tcp_port = tcp_port

    def pack(self):
        return [self.address.packed, struct.pack(">H", self.udp_port), struct.pack(">H", self.tcp_port)]

class PingNode(obj):
    packet_type = '\x01'
    version = '\x03'
    def __init__(self, endpt_from. endpt_to):
        self.endpt_from = endpt_from
        self.endpt_to = endpt_to

    def pack(self):
        return [self.version, self.endpt_from.pack(), self.endpt_to.pack(), struct.pack(">I", time.time() + 60)]

class PingServer(obj):
    def __init__(self, my_endpt):
        self.endpt = my_endpt

        #Obtain Private Key
        pri8_key_file = open('priv_key', 'r')
        pri8_key_serialized = pri8_key_file.read()
        pri8_key_file.close()
        self.priv_key = PrivateKey()
        self.priv_key.deserialize(pri8_key_serialized)

        # initialize socket
        sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sck.bind('0.0.0.0', self.endpt.udp_port)

    def wrap_packet(self, packet):
        payload = packet.packet_type + rlp.encode(packet.pack())
        sig = self.priv_key.ecdsa_sign_recoverable(keccak256(payload), raw = True)
        sig_serialized = self.priv_key.ecdsa_recoverable_serialize(sig)
        payload = sig_serialized[0] + chr(sig_serialized[1]) + payload

        hashed_payload = keccak256(payload)
        return hashed_payload + payload

    def udp_listen(self):
        def receive_ping():
            print "Listening..."
            data, addr = sck.recvfrom(1024)
            print "Received message[", addr, "]"

        return threading.Thread(target = receive_ping)

    def ping(self, endpt):
        ping = PingNode(self.endpt, endpt)
        msg = self.wrap_packet(ping)
        print "Sending ping."
        sck.sendto(msg, (endpt.address.exploded, endpt.udp_port))

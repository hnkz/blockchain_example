import random
import socket

class DNSFlags():
    def __init__(self, qr, opcode, aa, tc, rd, ra, z, ad, cd, rcode):
        self.qr = qr # 1bit
        self.opcode = opcode # 4bit
        self.aa = aa # 1bit
        self.tc = tc # 1bit
        self.rd = rd # 1bit
        self.ra = ra # 1bit
        self.z = z # 1bit
        self.ad = ad # 1bit
        self.cd = cd # 1bit
        self.rcode = rcode # 4bit
    
    def to_bytes(self):
        result = bytearray()
        result.append(
            self.qr << 7 | 
            (self.opcode >> 3 & 0x1) << 6 |
            (self.opcode >> 2 & 0x1) << 5 |
            (self.opcode >> 1 & 0x1) << 4 |
            (self.opcode >> 0 & 0x1) << 3 |
            self.aa << 2 |
            self.tc << 1 |
            self.rd << 0
        )
        result.append(
            self.ra << 7 |
            self.z << 6 |
            self.ad << 5 |
            self.cd << 4 |
            (self.rcode >> 3 & 0x1) << 3 |
            (self.rcode >> 2 & 0x1) << 2 |
            (self.rcode >> 1 & 0x1) << 1 |
            (self.rcode >> 0 & 0x1) << 0
        )
        return bytes(result)

class DNSHeader():
    def __init__(self, flags, qdcount, ancount, nscount, arcount):
        self.id = random.randint(0, 10000)
        self.flags = flags
        self.qdcount = qdcount
        self.ancount = ancount
        self.nscount = nscount
        self.arcount = arcount
    
    def to_bytes(self):
        result = bytearray()
        result.append(self.id >> 8 & 0xff)
        result.append(self.id & 0xff)
        for b in self.flags.to_bytes():
            result.append(b)
        result.append(self.qdcount >> 8 & 0xff)
        result.append(self.qdcount & 0xff)
        result.append(self.ancount >> 8 & 0xff)
        result.append(self.ancount & 0xff)
        result.append(self.nscount >> 8 & 0xff)
        result.append(self.nscount & 0xff)
        result.append(self.arcount >> 8 & 0xff)
        result.append(self.arcount & 0xff)
        return bytes(result)

class QuestionSection():
    def __init__(self, domain, dtype, dclass):
        self.domains = domain.split(".")
        self.dtype = dtype
        self.dclass = dclass
    
    def to_bytes(self):
        result = bytearray()
        # 未実装
        return bytes(result)

class DNS():
    def __init__(self, header, sections, ip="127.0.0.1", port=53):
        self.header = header
        self.sections = sections
        self.address = (ip, port)

    def to_bytes(self):
        result = bytearray()
        for b in self.header.to_bytes():
            result.append(b)
        for section in self.sections:
            for b in section.to_bytes():
                result.append(b)
        return bytes(result)

    @staticmethod
    def domain_to_ip(domain):
        raise Exception('not implmented')

    @staticmethod
    def ip_to_domain():
        raise Exception('not implemented')

def communicate(query, address):
    """
    クエリの送信と応答結果の受信
    :param query バイト配列
    :param address (送信先のアドレス, ポート番号)
    :return 受信したバイト配列
    """
    BUFFER = 1024
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # internet, udp
    try:
        client.settimeout(2)
        client.sendto(query, address)
        data, address = client.recvfrom(BUFFER)
        client.close()
        return data
    except socket.timeout:
        client.close()
        raise Exception('DNS timeout.')


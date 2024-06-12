
import logging
from basic import BaseDataObject
from pathlib import Path
import dpkt

class PcapReader():
    """Reads pcap raw data and convert it to a list of raw data packets"""
  
    def __init__(self, path :Path) -> None:
        """
        Args:
            path (Path): path to pcap file
        """
        
        self.pcap_file = path
        self.pcap_data= self.read_pcap()


    def read_pcap(self):
        pcap_data =[]
        try:
            # save pcap file as list of packets
            with open(self.pcap_file, 'rb') as file:               
                    pcap = dpkt.pcap.Reader(file)
                    pcap_data = [packet for packet in pcap]
                    # for packet in pcap:
                    #     pcap_data.append(packet)
                    #self.pcap_data = [buf for _, buf in pcap]

        except Exception as exception:
                logging.error("error while reading pcap data")
                logging.error("Exception: {}".format(type(exception).__name__))
                logging.error("Exception message: {}".format(exception))
        return pcap_data
                
    def __repr__(self) -> str:
         return f"Number of read packtets: {len(self.pcap_data)}\n"
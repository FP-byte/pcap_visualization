
import logging
import os
from pathlib import Path

from basic import BaseDataObject
from pcap_parsing.parser import PcapReader, PacketParser
from data_processing.pcap_cleaner import DataFrameCleaner
from data_processing.data_processor import DataProcessor
from data_visualization.pcap_plotter import GraphPlotter

logging.basicConfig(filename = "packet_parser.log", format="%(asctime)s:%(name)s:%(levelname)s:%(message)s")


if __name__ == "__main__":
    curr_folder = os.path.dirname(os.path.abspath(__file__))
    filename = "testtraffic_0806"
    
    path = Path(f"{curr_folder}/data/pcaps/{filename}.pcap").absolute()  

    #read pcap data to file
    reader = PcapReader(path)

    #save filtered data
    save_path =  Path(f"{curr_folder}/data/csv/{filename}.csv").absolute()

    #parse packets
    packet_parser = PacketParser(filename, reader.pcap_data)
    packet_parser.parse_packet_data()
    clean_df = packet_parser.save_df(packet_parser.pcap_cleandata)
    print(clean_df.head())
    #process filtered data
    #create clusters
    data_cleaner = DataFrameCleaner(clean_df)
    data_processor = DataProcessor(data_cleaner.df_data, data_cleaner.urls) #creates clusters and timelines
    # cluster urls
    data_processor.create_dns_clusters()
    # add categorization
    data_processor.add_lable_to_cluster()
    data_processor.print_clusers()

    # visualizations
    data_plotter = GraphPlotter(data_processor)
    # alle clusters 
    data_plotter.plot_all_clusters()
    # top 10 clusters
    data_plotter.plot_top10_clusters()

    data_plotter.plot_category_detail('social media')
    data_plotter.plot_category_distribution()

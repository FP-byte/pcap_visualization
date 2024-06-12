import pandas as pd

import matplotlib.pyplot as plt

from data_processing.data_processor import DataProcessor

class GraphPlotter():

    def __init__(self, data_processor: DataProcessor) -> None:
        self.clusters = data_processor.clusters
        self.data_processor= data_processor
        self.labeled_clusters = data_processor.labeled_clusters

    def plot_clusters (self, cluster_names, cluster_sizes, title, xlabel, ylabel='Link count'):
        plt.figure(figsize=(10, 6))
        plt.bar(cluster_names, cluster_sizes, color='skyblue')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()


    def plot_top10_clusters(self):
        # Visualize the clusters        
        cluster_names = self.data_processor.get_cluster_names()
        # remove category other
        cluster_names.remove('other')
        cluster_sizes = [len(self.clusters[name]) for name in cluster_names if name != 'other']
        self.plot_clusters(cluster_names[:10], cluster_sizes[:10], "Top 10 clusters", 'Top 10 URL Clusters')
        

    def plot_all_clusters(self):
        # Visualize the clusters
        cluster_names = self.data_processor.get_cluster_names()
        #print(cluster_names)        
        cluster_names.remove('other')
        cluster_sizes = [len(self.clusters[name]) for name in cluster_names if name != 'other']
        self.plot_clusters(cluster_names, cluster_sizes, "All clusters", 'URL Clusters Based on Regular Expressions')

    
    def plot_category_distribution(self):
            
            """ Plot the number of domains for each category
            """

            categories = list(self.labeled_clusters.keys())
            counts = [sum(len(domains) for domains in category.values()) for category in self.labeled_clusters.values()]

            # Combine categories and counts, then sort them based on counts
            sorted_data = sorted(zip(categories, counts), key=lambda x: x[1], reverse=True)
            sorted_categories, sorted_counts = zip(*sorted_data)

            # Define a list of colors from color map tab20 (one color per category)
            colors = plt.cm.get_cmap('tab20', len(sorted_categories)).colors

            plt.figure(figsize=(10, 6))
            plt.bar(sorted_categories, sorted_counts, color=colors)
            plt.xlabel('Category')
            plt.ylabel('Number of Domains')
            plt.title('Number of Domains per Category')
            plt.xticks(rotation=90)
            plt.tight_layout()
            plt.show()


            
    def plot_category_detail(self, category_name):
            """
            Plot distribution of domains within a specific category

            Args:
                category_name (str): name of category from the given categories
            """

            if category_name not in self.labeled_clusters:
                print(f"Category '{category_name}' not found in data.")
                return

            subcategories = self.labeled_clusters[category_name]
            labels = list(subcategories.keys())
            sizes = [len(domains) for domains in subcategories.values()]

            plt.figure(figsize=(10, 6))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.title(f'Domain Distribution in Category: {category_name}')
            plt.show()     

        

    
        

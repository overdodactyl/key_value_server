import pandas as pd
import matplotlib.pyplot as plt

def read_locust_results(file_path):
    """
    Read the locust results csv file into a pandas dataframe.
    :param file_path: path to the csv file
    :return: pandas dataframe
    """
    locust_results = pd.read_csv(file_path)

    # Remove the first 10 columns as burn-in
    locust_results = locust_results.iloc[5:]

    # order by the requests per second
    # locust_results = locust_results.sort_values(by=["Requests/s"])

    throughput = locust_results["Requests/s"]
    latency = locust_results["Total Average Response Time"]
    
    return throughput, latency

def plot_locust_results(file_path):
    one_server = read_locust_results("locust_results/one_server_stats_history.csv")
    two_servers = read_locust_results("locust_results/two_servers_stats_history.csv")
    three_servers = read_locust_results("locust_results/three_servers_stats_history.csv")

    plt.plot(one_server[0], one_server[1], label="1 server")
    plt.plot(two_servers[0], two_servers[1], label="2 servers")
    plt.plot(three_servers[0], three_servers[1], label="3 servers")

    # Add a legend
    plt.legend()

    # Add axis labels
    plt.xlabel("Throughput (RPS)")
    plt.ylabel("Latency (ms)")

    # Add a title
    plt.title("Throughput vs Latency")

    # Save the plot
    plt.savefig(file_path)

    # Reset the plot
    plt.clf()


plot_locust_results("locust_results/throughput_vs_latency.png")



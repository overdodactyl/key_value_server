import subprocess
import time
import pandas as pd
import matplotlib.pyplot as plt


def run_locust(num_users, spawn_rate, run_time="1m"):
    # Start the test with the specified number of users and hatch rate
    subprocess.run([
        "locust",
        "-f", "locustfile.py",
        "--headless",
        "--host", "http://localhost:8081"
        "--users", str(num_users),
        "--spawn-rate", str(spawn_rate),
        "--run-time", run_time,
        "--csv", f"locust_{num_users}_users"
    ])

    # Parse the CSV files to get RPS and latency
    stats_df = pd.read_csv(f"locust_{num_users}_users_requests.csv")
    rps = stats_df['Requests/s'].mean()
    latency = stats_df['Median Response Time'].mean()

    return rps, latency


def plot_data(data):
    df = pd.DataFrame(data)
    plt.plot(df['rps'], df['latency'])
    plt.xlabel('Throughput (RPS)')
    plt.ylabel('Latency (ms)')
    plt.title('Throughput vs Latency')
    plt.show()


if __name__ == "__main__":
    results = []
    user_counts = [10, 50, 100, 200]  # Example user counts
    spawn_rate = 10  # Users spawned per second

    for user_count in user_counts:
        # Start the KV server setup for the current test
        # start_kv_servers(count=number_of_kv_servers)  # This would be a custom function to start your servers

        # Run the locust test
        rps, latency = run_locust(num_users=user_count, spawn_rate=spawn_rate)

        # Store the result
        results.append({'users': user_count, 'rps': rps, 'latency': latency})

        # Stop the KV server setup after the test
        # stop_kv_servers()  # Another custom function to stop your servers

        # Wait a bit before the next test
        time.sleep(10)

    # Now, plot the results
    plot_data(results)

from locust import HttpUser, task, between
import random
import string
import locust.stats


locust.stats.CSV_STATS_INTERVAL_SEC = 1

def generate_random_string(length=10):
    """Generate a random string of fixed length."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))

class KeyValueStoreUser(HttpUser):
    wait_time = between(.1, .2)
    key_store = []

    @task(10)
    def put_key_value(self):
        key = generate_random_string()
        value = generate_random_string(1202)
        # value = generate_large_random_string()
        self.client.post("/put?key={key}".format(key=key), json={"value": value})
        KeyValueStoreUser.key_store.append(key)

    @task(1)
    def get_value(self):
        if KeyValueStoreUser.key_store:
            key = random.choice(KeyValueStoreUser.key_store)
            self.client.get(f"/get?key={key}")

package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"sync"
	"time"
)

// KeyValue store structure
type KeyValue struct {
	mu   sync.RWMutex
	data map[string]string
}

var kvStore = &KeyValue{data: make(map[string]string)}

// Handlers
func putHandler(w http.ResponseWriter, r *http.Request) {
	key := r.URL.Query().Get("key")
	if key == "" {
		http.Error(w, "Missing key", http.StatusBadRequest)
		return
	}

	var item struct {
		Value string `json:"value"`
	}
	err := json.NewDecoder(r.Body).Decode(&item)
	if err != nil {
		http.Error(w, "Invalid request", http.StatusBadRequest)
		return
	}

	kvStore.mu.Lock()
	kvStore.data[key] = item.Value
	kvStore.mu.Unlock()

	json.NewEncoder(w).Encode(struct{ Status string }{Status: "success"})
}

func getHandler(w http.ResponseWriter, r *http.Request) {
	key := r.URL.Query().Get("key")
	if key == "" {
		http.Error(w, "Missing key", http.StatusBadRequest)
		return
	}

	kvStore.mu.RLock()
	value, exists := kvStore.data[key]
	kvStore.mu.RUnlock()

	if !exists {
		http.Error(w, "Key not found", http.StatusNotFound)
		return
	}

	json.NewEncoder(w).Encode(struct {
		Status string
		Value  string
	}{Status: "success", Value: value})
}

func deleteHandler(w http.ResponseWriter, r *http.Request) {
	key := r.URL.Query().Get("key")
	if key == "" {
		http.Error(w, "Missing key", http.StatusBadRequest)
		return
	}

	kvStore.mu.Lock()
	delete(kvStore.data, key)
	kvStore.mu.Unlock()

	json.NewEncoder(w).Encode(struct{ Status string }{Status: "success"})
}

// Persistence
func saveDataPeriodically(interval time.Duration) {
	for {
		time.Sleep(interval)
		saveDataNow()
	}
}

func saveDataNow() {
	kvStore.mu.RLock()
	defer kvStore.mu.RUnlock()

	file, err := json.MarshalIndent(kvStore.data, "", " ")
	if err != nil {
		log.Println("Error marshalling data:", err)
		return
	}

	err = ioutil.WriteFile("data/key_value_data.json", file, 0644)
	if err != nil {
		log.Println("Error writing file:", err)
	}
}

func main() {
	// Load initial data
	data, err := ioutil.ReadFile("data/key_value_data.json")
	if err == nil {
		json.Unmarshal(data, &kvStore.data)
	}

	// Setup HTTP server
	http.HandleFunc("/put", putHandler)
	http.HandleFunc("/get", getHandler)
	http.HandleFunc("/del", deleteHandler)

	// Start persistence goroutine
	go saveDataPeriodically(600 * time.Second)

	// Start HTTP server
	log.Fatal(http.ListenAndServe(":8080", nil))
}

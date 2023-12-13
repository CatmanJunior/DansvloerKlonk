const source = new EventSource("http://127.0.0.1:5000/stream-data");


//streams the data

source.onmessage = function (event) {
    console.log(event.data);
};
source.onerror = function (error) {
    console.error("EventSource failed:", error);
    source.close(); // Consider closing the connection in case of an error
};
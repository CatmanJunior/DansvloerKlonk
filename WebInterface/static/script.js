document.addEventListener('DOMContentLoaded', (event) => {
    // Select all tiles
    const tiles = document.querySelectorAll('.tile');

    tiles.forEach(tile => {
        tile.addEventListener('click', () => {
            // Toggle tile color between two states
            if (tile.style.backgroundColor === 'rgb(221, 221, 221)') { // default color
                tile.style.backgroundColor = '#444'; // new color
            } else {
                tile.style.backgroundColor = '#ddd'; // back to default color
            }
        });
    });
});

//open bootstrap modal
function openModal() {
    document.getElementById('mqttMessages').style.display = "block";
}

//close modal
function closeModal() {
    document.getElementById('myModal').style.display = "none";
}
//open modal when clicked on button
document.getElementById('modalBtn').addEventListener('click', openModal);
//close modal when clicked outside of modal
window.addEventListener('click', outsideClick);
//close modal when clicked outside of modal
function outsideClick(e) {
    if (e.target != document.getElementById('mqttMessages') && e.target != document.getElementById('modalBtn')) {
        document.getElementById('mqttMessages').style.display = "none";
    }
    console.log(e.target);
}

// if (!!window.EventSource) {
//     console.log("starting event source");

//     var source = new EventSource('/stream_updates', );

//     source.addEventListener('open', function(e) {
//         console.log("open");
//     }, false);  

//     source.addEventListener('error', function(e) {
//         if (e.target.readyState != EventSource.OPEN) {
//             console.log(e.target.readyState);
//         }
//     }, false);

//     source.addEventListener('message', function(e) {
//         console.log("message");
//         console.log(e.data);
//     }, false);
// }

function fetchUpdate() {
    fetch('/get_update')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Process the data received from Flask
            // data contains current beat, light up the corresponding tile
            const tiles = document.querySelectorAll('.tile');

            tiles.forEach(tile => {
                if (tile.id == data['current_beat']) {
                    tile.style.backgroundColor = '#444';
                } else {
                    tile.style.backgroundColor = '#ddd';
                }
            })
            updateModal(data['message_list']);

        }).catch(error => console.error('Error:', error));
}

// Poll the server every 5 seconds
setInterval(fetchUpdate, 300);

//update the modal with the latest mqtt messages



function updateModal(data) {
    const messages = document.getElementById('msgList');
    messages.innerHTML = "";

    data.forEach(message => {
        const messageDiv = document.createElement('div');
        messageDiv.className = "message";

        const messageHeaderDiv = document.createElement('div');
        messageHeaderDiv.className = "message-header";

        const messageTopicSpan = document.createElement('span');
        messageTopicSpan.className = "message-topic";
        messageTopicSpan.innerHTML = message['topic'];

        const messageTimeSpan = document.createElement('span');
        messageTimeSpan.className = "message-time";
        messageTimeSpan.innerHTML = message['time'];

        const messageBodyDiv = document.createElement('div');
        messageBodyDiv.className = "message-body";
        messageBodyDiv.innerHTML = message['body'];

        messageHeaderDiv.appendChild(messageTopicSpan);
        messageHeaderDiv.appendChild(messageTimeSpan);

        messageDiv.appendChild(messageHeaderDiv);
        messageDiv.appendChild(messageBodyDiv);

        messages.appendChild(messageDiv);
    });
};

//add button function to reset-button to get /send-message
document.getElementById('reset-button').addEventListener('click', () => {
    fetch('/send-message')
        .then(response => response.json())
        .then(data => {
            console.log(data);
        }).catch(error => console.error('Error:', error));
});
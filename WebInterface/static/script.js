document.addEventListener('DOMContentLoaded', (event) => {
    // Select all tiles
    const tiles = document.querySelectorAll('.tile');

    tiles.forEach(tile => {
        tile.addEventListener('click', () => {
            // Toggle tile color between two states
            if(tile.style.backgroundColor === 'rgb(221, 221, 221)') { // default color
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
    if(e.target != document.getElementById('mqttMessages') && e.target != document.getElementById('modalBtn')) {
        document.getElementById('mqttMessages').style.display = "none";
    }
    console.log(e.target);
}

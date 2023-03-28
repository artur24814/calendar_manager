// chat/static/room.js

console.log("Sanity check from room.js.");

const roomName = JSON.parse(document.getElementById('roomName').textContent);

let body_chat = document.querySelector(".chat-body")


body_chat.scrollTo(0, body_chat.scrollHeight);

let chatLog = document.querySelector("#chatLog");
let request_user = chatLog.dataset.user
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
// let onlineUsersSelector = document.querySelector("#onlineUsersSelector");

// // adds a new option to 'onlineUsersSelector'
// function onlineUsersSelectorAdd(value) {
//     if (document.querySelector("option[value='" + value + "']")) return;
//     let newOption = document.createElement("option");
//     newOption.value = value;
//     newOption.innerHTML = value;
//     onlineUsersSelector.appendChild(newOption);
// }

// removes an option from 'onlineUsersSelector'
function onlineUsersSelectorRemove(value) {
    let oldOption = document.querySelector("option[value='" + value + "']");
    if (oldOption !== null) oldOption.remove();
}

// focus 'chatMessageInput' when user opens the page
chatMessageInput.focus();

// submit if the user presses the enter key
chatMessageInput.onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter key
        chatMessageSend.click();
    }
};

// clear the 'chatMessageInput' and forward the message
chatMessageSend.onclick = function() {
    if (chatMessageInput.value.length === 0) return;
    //forward the message to the WebSocket
    chatSocket.send(JSON.stringify({
        "message": chatMessageInput.value,
    }));
};

let chatSocket = null;

function connect() {

    let loc = window.location
    let wsStart = 'ws://'

    // for productions
    if (loc.protocol == 'https:') {
        wsStart = 'wss://'
    }

    chatSocket = new WebSocket(wsStart + window.location.host + "/ws/chat/" + roomName + "/");

    console.log(chatSocket)

    chatSocket.onopen = function(e) {
        console.log("Successfully connected to the WebSocket.");
    }

    chatSocket.onclose = function(e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data);
    
        switch (data.type) {
            case "chat_message":
                if (request_user == data.user){
                    chatLog.innerHTML +=`
                    <div class="d-flex flex-row justify-content-start">
                        <img src=" ${data.img}" class="rounded-circle"
                        alt="avatar 1" style="width: 45px; height: 100%;">
                        <div>
                        <p class="small p-2 ms-3 mb-1 rounded-3" style="background-color: #f5f6f7;">
                            ${data.message}</p>
                        <p class="small ms-3 mb-3 rounded-3 text-muted">${data.date}</p>
                        </div>
                    </div>`
                } else {
                    chatLog.innerHTML += `
                        <div class="d-flex flex-row justify-content-end mb-4 pt-1">
                            <img src="${data.img}" class="rounded-circle"
                            alt="avatar 1" style="width: 45px; height: 100%;">
                            <div>
                                <p class="small p-2 me-3 mb-1 text-white rounded-3 bg-primary">
                                ${data.message}</p>
                                <p class="small ms-3 mb-3 rounded-3 text-muted">${data.date}</p>
                            </div>
                        </div>
                    `
                }
                chatMessageInput.value=''
                body_chat.scrollTo(0, body_chat.scrollHeight);
                break;
        }
    
        // scroll 'chatLog' to the bottom
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    chatSocket.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    }
}
connect();

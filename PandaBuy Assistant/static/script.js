function openNav() {
    document.getElementById("sidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
    document.getElementById("sidebar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
}

function createNewChat() {
    const chatContainer = document.getElementById('chat-container');
    const sentMessages = chatContainer.querySelectorAll('.sent-message'); // Select all messages sent by the user

    // Remove each sent message
    sentMessages.forEach(message => {
        message.remove();
    });

    alert("Creating a new chat...");
}

async function sendMessage() {
    const userInput = document.getElementById('question-input').value;
    if (userInput) {
        // Display the user's message
        const chatContainer = document.getElementById('chat-container');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message';

        const profilePic = document.createElement('img');
        profilePic.src = 'https://cdn.discordapp.com/attachments/1233228314949451786/1256695243521134622/shopping_bag_icon.jpg?ex=6681b426&is=668062a6&hm=524058020bab37003277d6a61db50846898e29294f664f72b9bac71a4f823c6d&';
        profilePic.alt = 'Profile Picture';
        profilePic.className = 'profile-pic';

        const text = document.createElement('span');
        text.textContent = userInput;
        text.className = 'message-text';

        messageDiv.appendChild(profilePic);
        messageDiv.appendChild(text);
        chatContainer.appendChild(messageDiv);

        // Send the user's message to the server
        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: userInput })
            });

            const data = await response.json();

            // Display the response from the server
            const responseDiv = document.createElement('div');
            responseDiv.className = 'message';

            const responseProfilePic = document.createElement('img');
            responseProfilePic.src = 'https://th.bing.com/th/id/OIP.XmdHUOdIXaEnkq4XCjnNsAHaHa?rs=1&pid=ImgDetMain';
            responseProfilePic.alt = 'Profile Picture';
            responseProfilePic.className = 'profile-pic';

            const responseText = document.createElement('span');
            responseText.textContent = data.answer;
            responseText.className = 'message-text';

            responseDiv.appendChild(responseProfilePic);
            responseDiv.appendChild(responseText);
            chatContainer.appendChild(responseDiv);
        } catch (error) {
            console.error('Error:', error);
        }

        // Clear the input
        document.getElementById('question-input').value = '';
    }
}

document.getElementById('question-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

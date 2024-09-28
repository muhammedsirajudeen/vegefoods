

document.addEventListener('DOMContentLoaded', function () {
    const chatIcon = document.getElementById('chatbot-icon');
    const chatSection = document.getElementById('chat-section');
    const closeChatButton = document.getElementById('close-chat');

    // Show chat section on icon click
    chatIcon.addEventListener('click', function () {
        chatSection.style.display = chatSection.style.display === 'none' ? 'block' : 'none';
    });

    // Hide chat section on close button click
    closeChatButton.addEventListener('click', function () {
        chatSection.style.display = 'none';
    });
});

// Function to display user's selected message
function showUserMessage(message) {
    const responseDiv = document.getElementById('response');
    const userMessageHTML = `
        <div class="d-flex flex-row justify-content-end mb-4">
            <div class="me-3">
                <p class="small p-2 mb-1 rounded-3 bg-primary text-white" style="font-size: 1rem;">${message}</p>
            </div>
            <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava2-bg.webp" alt="user avatar" style="width: 45px; height: 100%;">
        </div>
        
    `;
    responseDiv.insertAdjacentHTML('beforeend', userMessageHTML);
    responseDiv.scrollTop = responseDiv.scrollHeight; // Scroll to the latest message
}

function fetchWalletBalance() {
    showUserMessage("Wallet Balance"); // Display the user's selection as a user-side message

    fetch('/user/api/wallet-balance/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const responseDiv = document.getElementById('response');
            const botMessageHTML = `
                <div class="d-flex flex-row justify-content-start mb-4">
                    <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3-bg.webp" alt="bot avatar" style="width: 45px; height: 100%;">
                    <div class="ms-3">
                        <p class="small p-2 mb-1 rounded-3 bg-body-tertiary" style="font-size: 1rem;">Your current wallet balance is: $${data.balance}</p>
                         <!-- Feedback buttons -->
        <div class="d-flex">
            <button class="btn btn-outline-success me-2" onclick="handleFeedback('helpful')">👍 Helpful</button>
            <button class="btn btn-outline-danger" onclick="handleFeedback('dislike')">👎 Dislike</button>
        </div>
                    </div>
                </div>
            `;
            responseDiv.insertAdjacentHTML('beforeend', botMessageHTML);
            responseDiv.scrollTop = responseDiv.scrollHeight; // Scroll to the latest message
        })
        .catch(error => console.error('Error fetching wallet balance:', error));
}

function fetchLatestComplaintStatus() {
    showUserMessage("Latest Complaint Status"); // Display the user's selection as a user-side message

    fetch('/user/api/latest-complaint-status/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const responseDiv = document.getElementById('response');
            const botMessageHTML = `
                <div class="d-flex flex-row justify-content-start mb-4">
                    <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3-bg.webp" alt="bot avatar" style="width: 45px; height: 100%;">
                    <div class="ms-3">
                        <p class="small p-2 mb-1 rounded-3 bg-body-tertiary">Your latest complaint: ${data.subject} - Status: ${data.status}</p>
                         <!-- Feedback buttons -->
        <div class="d-flex">
            <button class="btn btn-outline-success me-2" onclick="handleFeedback('helpful')">👍 Helpful</button>
            <button class="btn btn-outline-danger" onclick="handleFeedback('dislike')">👎 Dislike</button>
        </div>
                    </div>
                </div>
            `;
            responseDiv.insertAdjacentHTML('beforeend', botMessageHTML);
            responseDiv.scrollTop = responseDiv.scrollHeight; // Scroll to the latest message
        })
        .catch(error => console.error('Error fetching latest complaint status:', error));
}

function showCustomerCareMessage() {
    showUserMessage("Customer Care Support"); // Display the user's selection

    const responseDiv = document.getElementById('response');
    const botMessageHTML = `
        <div class="d-flex flex-row justify-content-start mb-4">
            <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3-bg.webp" alt="bot avatar" style="width: 45px; height: 100%;">
            <div class="ms-3">
                <p class="small p-2 mb-1 rounded-3 bg-body-tertiary" style="font-size: 1.1rem;">Our customer care executives are busy right now. They will get back to you within 10 minutes. You can also give a missed call at 79943556519.</p>
                <!-- Feedback buttons -->
        <div class="d-flex">
            <button class="btn btn-outline-success me-2" onclick="handleFeedback('helpful')">👍 Helpful</button>
            <button class="btn btn-outline-danger" onclick="handleFeedback('dislike')">👎 Dislike</button>
        </div>
            </div>
        </div>
    `;
    responseDiv.insertAdjacentHTML('beforeend', botMessageHTML);
    responseDiv.scrollTop = responseDiv.scrollHeight;
}

function showReturnPolicy() {
    showUserMessage("Return Policy"); // Display the user's selection

    const responseDiv = document.getElementById('response');
    const botMessageHTML = `
     <div class="d-flex flex-row justify-content-start mb-4">
    <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3-bg.webp" alt="bot avatar" style="width: 45px; height: 100%;">
    <div class="ms-3">
        <p class="small p-2 mb-1 rounded-3 bg-body-tertiary" style="font-size: 1.1rem;">📦 Return Policy: You can request a return within 24 hours of receiving your product. If approved by our admin within 2 hours, we will arrange for a pickup within 1 hour. Please make sure the product is in its original condition. 🔄</p>
        
        <!-- Feedback buttons -->
        <div class="d-flex">
            <button class="btn btn-outline-success me-2" onclick="handleFeedback('helpful')">👍 Helpful</button>
            <button class="btn btn-outline-danger" onclick="handleFeedback('dislike')">👎 Dislike</button>
        </div>
    </div>
</div>

    `;
    responseDiv.insertAdjacentHTML('beforeend', botMessageHTML);
    responseDiv.scrollTop = responseDiv.scrollHeight;
}
function handleFeedback(type) {
    
    let message;
    if (type === 'helpful') {
        showUserMessage("👍 Helpful"); 
        message = "Thank you for your feedback! We're glad you found it helpful. Happy shopping! 🛒";
    } else if (type === 'dislike') {
        showUserMessage("👎 Dislike");
        message = "Thank you for your feedback! We're sorry that you didn't find it helpful. If you have any more questions, feel free to ask! 🙁";
    }


    displayFeedbackMessage(message);
}

// Function to display feedback message
function displayFeedbackMessage(message) {
    const feedbackContainer = document.createElement('div');
    feedbackContainer.className = 'd-flex flex-row justify-content-start mb-4';
    feedbackContainer.innerHTML = `
        <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3-bg.webp" alt="user avatar" style="width: 45px; height: 100%;">
        <div class="ms-3">
            <p class="small p-2 mb-1 rounded-3 bg-body-tertiary" style="font-size: 1.1rem;">${message}</p>
        </div>
    `;

    // Append the feedback message to the chat container
    document.querySelector('#chat2 .card-body').appendChild(feedbackContainer);
}
document.getElementById('close-chat').addEventListener('click', function() {
    window.location.reload()
    
    
});



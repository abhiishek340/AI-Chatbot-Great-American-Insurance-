function addMessage(message, isUser = false) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
    
    const content = `
        <div class="message-content">
            ${isUser ? '' : '<div class="bot-avatar"><i class="fas fa-robot"></i></div>'}
            <div class="message-text">${message}</div>
        </div>
    `;
    
    messageDiv.innerHTML = content;
    chatMessages.appendChild(messageDiv);
    messageDiv.scrollIntoView({ behavior: 'smooth' });
}

function addTypingIndicator() {
    const chatMessages = document.getElementById('chat-messages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot typing-message';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = `
        <div class="message-content">
            <div class="bot-avatar"><i class="fas fa-robot"></i></div>
            <div class="message-text">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    `;
    chatMessages.appendChild(typingDiv);
    typingDiv.scrollIntoView({ behavior: 'smooth' });
}

function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

function askQuestion(question) {
    if (question === 'Get a Quote') {
        const quoteInfo = `
            <div class='formatted-response quote-info'>
                <h2>GreatQuoter - Online Quote System</h2>
                
                <h3>Available Products for Online Quotes:</h3>
                <ul>
                    <li>Directors & Officers Liability</li>
                    <li>Employment Practices Liability</li>
                    <li>Fiduciary Liability</li>
                    <li>Crime Coverage</li>
                </ul>

                <h3>Key Features of GreatQuoter:</h3>
                <ul>
                    <li>Quick and easy online quoting process</li>
                    <li>Real-time pricing and coverage options</li>
                    <li>Instant quote generation</li>
                    <li>Ability to bind coverage online</li>
                    <li>Access to policy forms and endorsements</li>
                </ul>

                <h3>How to Get Started:</h3>
                <ul>
                    <li>Visit GreatQuoter at <a href="https://www.greatquoter.com" target="_blank">www.greatquoter.com</a></li>
                    <li>Register for a new account or log in</li>
                    <li>Select your desired product</li>
                    <li>Complete the application form</li>
                    <li>Review and select coverage options</li>
                    <li>Generate and bind your quote</li>
                </ul>

                <h3>Need Assistance?</h3>
                <ul>
                    <li>Contact our Support Team: 1-800-869-9965</li>
                    <li>Email: executiveliability@gaig.com</li>
                    <li>Hours: Monday-Friday, 8:00 AM - 5:00 PM ET</li>
                </ul>
            </div>
        `;
        addMessage(quoteInfo, false);
        return;
    }
    
    if (question === 'How do I file a claim?') {
        const modal = document.getElementById('fileUploadModal');
        modal.style.display = 'block';
        setTimeout(() => {
            modal.classList.add('show');
        }, 10);
        return;
    }
    
    const inputElement = document.getElementById('user-input');
    inputElement.value = question;
    sendMessage();
    
    const buttons = document.querySelectorAll('.suggested-questions button');
    buttons.forEach(btn => {
        if (btn.textContent === question) {
            btn.style.background = '#003087';
            btn.style.color = 'white';
            setTimeout(() => {
                btn.style.background = '';
                btn.style.color = '';
            }, 500);
        }
    });
}

async function sendMessage() {
    const inputElement = document.getElementById('user-input');
    const message = inputElement.value.trim();
    
    if (message === '') return;
    
    addMessage(message, true);
    inputElement.value = '';
    
    addTypingIndicator();
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        removeTypingIndicator();
        
        if (response.ok) {
            addMessage(data.response, false);
        } else {
            addMessage('❌ Sorry, something went wrong. Please try again.');
        }
    } catch (error) {
        removeTypingIndicator();
        addMessage('🔌 Error: Could not connect to the server.');
    }
}

function handleGetQuote() {
    const quoteInfo = `
        <div class='formatted-response quote-info'>
            <h2>GreatQuoter - Online Quote System</h2>
            
            <h3>Available Products for Online Quotes:</h3>
            <ul>
                <li>Directors & Officers Liability</li>
                <li>Employment Practices Liability</li>
                <li>Fiduciary Liability</li>
                <li>Crime Coverage</li>
            </ul>

            <h3>Key Features:</h3>
            <ul>
                <li>Quick and easy online quoting process</li>
                <li>Real-time pricing and coverage options</li>
                <li>Instant quote generation</li>
                <li>Ability to bind coverage online</li>
                <li>Access to policy forms and endorsements</li>
            </ul>

            <h3>How to Get Started:</h3>
            <ul>
                <li>Visit GreatQuoter at <a href="https://www.greatquoter.com" target="_blank">www.greatquoter.com</a></li>
                <li>Register for a new account or log in</li>
                <li>Select your desired product</li>
                <li>Complete the application form</li>
                <li>Review and select coverage options</li>
                <li>Generate and bind your quote</li>
            </ul>

            <h3>Need Assistance?</h3>
            <ul>
                <li>Contact our Support Team: 1-800-869-9965</li>
                <li>Email: executiveliability@gaig.com</li>
                <li>Hours: Monday-Friday, 8:00 AM - 5:00 PM ET</li>
            </ul>
        </div>
    `;
    addMessage(quoteInfo, false);
}

// Add these functions for file upload handling
function showFileUploadModal() {
    const modal = document.getElementById('fileUploadModal');
    modal.style.display = 'block';
}

function hideFileUploadModal() {
    const modal = document.getElementById('fileUploadModal');
    modal.classList.remove('show');
    setTimeout(() => {
        modal.style.display = 'none';
        document.getElementById('claimForm').reset();
        document.getElementById('fileList').innerHTML = '';
    }, 300);
}

function handleFileUpload(event) {
    const files = event.target.files;
    const fileList = document.getElementById('fileList');
    fileList.innerHTML = '';

    Array.from(files).forEach(file => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
            <span><i class="fas fa-file"></i>${file.name}</span>
            <i class="fas fa-times remove-file" onclick="removeFile(this)"></i>
        `;
        fileList.appendChild(fileItem);
    });
}

function removeFile(element) {
    element.parentElement.remove();
}

async function handleClaimSubmission(event) {
    event.preventDefault();
    
    const description = document.getElementById('claimDescription').value;
    const files = document.getElementById('fileUpload').files;
    
    if (!description.trim()) {
        alert('Please provide a claim description');
        return;
    }
    
    const formData = new FormData();
    formData.append('description', description);
    
    if (files.length > 0) {
        Array.from(files).forEach(file => {
            formData.append('files', file);
        });
    }
    
    try {
        addMessage('Submitting your claim...', false);
        
        const response = await fetch('/submit-claim', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const result = await response.json();
            addMessage(`
                <div class="success-message">
                    <h3>✅ Claim Submitted Successfully</h3>
                    <p>Our team will review your claim and contact you soon.</p>
                    <p>Reference Number: ${result.claim_id || 'N/A'}</p>
                </div>
            `, false);
            hideFileUploadModal();
        } else {
            throw new Error('Failed to submit claim');
        }
    } catch (error) {
        addMessage(`
            <div class="error-message">
                <h3>❌ Error Submitting Claim</h3>
                <p>Please try again or contact support at 1-800-545-4269.</p>
            </div>
        `, false);
    }
}

// Add these functions for voice input
let recognition;

function initializeSpeechRecognition() {
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = function() {
            const voiceBtn = document.querySelector('.voice-btn');
            voiceBtn.style.background = '#e31837'; // Change color when recording
            voiceBtn.innerHTML = '<i class="fas fa-microphone-slash"></i>';
        };

        recognition.onend = function() {
            const voiceBtn = document.querySelector('.voice-btn');
            voiceBtn.style.background = '';
            voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
        };

        recognition.onresult = function(event) {
            const voiceText = event.results[0][0].transcript;
            document.getElementById('user-input').value = voiceText;
            sendMessage();
        };

        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            addMessage('Sorry, I could not understand that. Please try again or type your question.', false);
        };
    }
}

function startVoiceInput() {
    if (!recognition) {
        initializeSpeechRecognition();
    }
    
    if (recognition) {
        try {
            recognition.start();
        } catch (e) {
            recognition.stop();
        }
    } else {
        addMessage('Speech recognition is not supported in your browser. Please type your question.', false);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const inputElement = document.getElementById('user-input');
    const sendButton = document.querySelector('.send-btn');
    
    inputElement.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    sendButton.addEventListener('click', sendMessage);
    
    inputElement.focus();
    
    sendButton.addEventListener('mousedown', function() {
        this.style.transform = 'scale(0.95)';
    });
    
    sendButton.addEventListener('mouseup', function() {
        this.style.transform = '';
    });

    // Add new event listeners for file upload
    document.querySelector('.close-modal').addEventListener('click', hideFileUploadModal);
    document.querySelector('.cancel-btn').addEventListener('click', hideFileUploadModal);
    document.getElementById('fileUpload').addEventListener('change', handleFileUpload);
    document.getElementById('claimForm').addEventListener('submit', handleClaimSubmission);

    // Initialize speech recognition
    initializeSpeechRecognition();
});

// Add this CSS for success and error messages
const style = document.createElement('style');
style.textContent = `
    .success-message, .error-message {
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .success-message {
        background: #e6ffe6;
        border: 1px solid #00cc00;
    }
    
    .error-message {
        background: #ffe6e6;
        border: 1px solid #cc0000;
    }
    
    .success-message h3, .error-message h3 {
        margin: 0 0 10px 0;
    }
`;
document.head.appendChild(style);

document.addEventListener('click', function(event) {
    const modal = document.getElementById('fileUploadModal');
    if (event.target === modal) {
        hideFileUploadModal();
    }
});
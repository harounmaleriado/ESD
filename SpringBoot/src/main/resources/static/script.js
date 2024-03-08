document.getElementById('send-button').addEventListener('click', function() {
    var input = document.getElementById('message-input');
    var message = input.value.trim();
    if (message) {
      var messagesContainer = document.getElementById('messages');
      var messageElement = document.createElement('div');
      messageElement.textContent = message;
      messagesContainer.appendChild(messageElement);
      input.value = ''; // Clear input field
    }
  });
  
import {v4 as uuidv4} from 'uuid';

export function createMessageElement(message) {
    const messageElement = document.createElement('div');
    messageElement.setAttribute("data-message-id", message.msg_id);
    messageElement.classList.add('message');
    messageElement.classList.add(`message-${message.user}`);
    messageElement.innerHTML = message.message;
    const iconElement = document.createElement('div');
    iconElement.classList.add('icon');
    iconElement.classList.add(`icon-${message.user}`);
    const finalElement = document.createElement('div');
    finalElement.classList.add('message-container');
    if (message.user === 'human') {
        iconElement.innerHTML = '🧑';
        finalElement.appendChild(iconElement);
        finalElement.appendChild(messageElement);
    } else if (message.user === 'ai') {
        iconElement.innerHTML = '🤖';
        finalElement.appendChild(messageElement);
        finalElement.appendChild(iconElement);
    }
    return finalElement;
}

function messageNotDisplayed(messageId) {
    return document.querySelector('[data-message-id="' + messageId + '"]') === null;
}


export function updateChatHistory(localMemory) {
    const chatHistoryContainer = document.querySelector('#chat-history-container');
    localMemory.forEach((message) => {
        if (messageNotDisplayed(message.msg_id)) {
            const newMessageElement = createMessageElement(message);
            chatHistoryContainer.appendChild(newMessageElement);
        }
    });
    chatHistoryContainer.scrollTop = chatHistoryContainer.scrollHeight;
}


export function inputIsValid(textElement) {
    const validityState = textElement.validity;
    if (validityState.valueMissing) {
        document.querySelector('#text-input')
            .setCustomValidity('You cant send an empty message!');
        textElement.reportValidity();
        return false;
    }
    return true;
}

export async function sendToChatBot(url, userText) {
    const headers = {"Content-Type": "application/json"}
    const requestJson = {
        method: "POST",
        mode: "cors",
        headers: headers,
        body: JSON.stringify({message: userText}),
        credentials: 'include',
    }
    return await fetch(url, requestJson);
}

export function createMessageJson(sessionId, message, user) {
    return {
        msg_id: uuidv4(),
        sessionId: sessionId,
        user: user,
        message: message,
        timestamp: new Date().getTime()
    };
}

function clearUserInputBox(textElement) {
    textElement.value = '';
}

function handleUserMessage(userMessage) {
    if (userMessage.validator(userMessage.textElement) === false) {
        return;
    }
    const userMsgJson = createMessageJson(userMessage.sessionId, userMessage.textElement.value, "human");
    userMessage.localMemory.push(userMsgJson);
    updateChatHistory(userMessage.localMemory);
    clearUserInputBox(userMessage.textElement);
    sendToChatBot(userMessage.url, userMsgJson.message).then(
        async (response) => {
            storeAiMessage(userMessage, await response.json());
        }
    );
}

function storeAiMessage(userMessage, aiJson) {
    const aiMsgJson = createMessageJson(userMessage.sessionId, aiJson, "ai");
    userMessage.localMemory.push(aiMsgJson);
    updateChatHistory(userMessage.localMemory);
}

export function sendMessage(userMessage) {
    handleUserMessage(userMessage);
}

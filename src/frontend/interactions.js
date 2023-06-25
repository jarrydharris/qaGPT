import {updateProducts} from "./products.js";

const togglePollingButton = document.getElementById('polling-toggle');

function updatePollingButtonValue(state) {
    togglePollingButton.value = 'Polling: ' + state;
}

let polling = (function () {
    let state = false;
    let public_state = {};
    let paused = false;
    public_state.getState = () => state;
    public_state.toggle = () => {
        if (paused) return;
        state = !state;
        updatePollingButtonValue(state);
    };
    public_state.setState = (newState) => {
        if (paused) return;
        state = newState;
        updatePollingButtonValue(state);
    };
    public_state.pausePolling = () => {
        // if the state was false, but we didn't pause it, then we don't need to do anything
        if (!state && !paused) return;
        // if the state was false, but we paused it, then we need to set the state to true and unpause it
        if (!state && paused) {
            state = true;
            paused = false;
            updatePollingButtonValue(state);
        } else if (state) {
            // Otherwise we need to pause it
            state = false;
            paused = true;
            updatePollingButtonValue("Paused");
        }
    };
    return public_state;
})();

togglePollingButton.addEventListener('click', polling.toggle);


function compareJson(a, b) {
    return JSON.stringify(a, Object.keys(a).sort()) === JSON.stringify(b, Object.keys(b).sort());
}

export async function setState(currentState) {
    polling.pausePolling();
    const headers = {"Content-Type": "application/json"}
    const requestJson = {
        method: "POST",
        mode: "cors",
        headers: headers,
        body: JSON.stringify(currentState),
        credentials: 'include',
    }
    await fetch('http://localhost:5000/api/set_input_state', requestJson).then((response) => {
        if (!response.ok) {
            throw new Error('Failed to update backend with state');
        }
    });
    polling.pausePolling();
}

export function initInteractionStates(interactionElements) {
    polling.pausePolling();
    const interactionsState = {}
    interactionElements.forEach((interactionElement) => {
        if (interactionElement.type === "checkbox") {
            interactionsState[interactionElement.id] = {
                id: interactionElement.id,
                checked: interactionElement.checked,
                type: interactionElement.type,
            };
        } else {
            interactionsState[interactionElement.id] = {
                id: interactionElement.id,
                value: interactionElement.value,
                type: interactionElement.type,
            };
        }

    });

    polling.setState(true)
    return interactionsState;
}

export function updateInteractionStates(currentState, newState) {
    Object.entries(currentState).forEach(([key, value]) => {
        if (value.type === "checkbox") {
            value.checked = newState[key].checked;
        } else {
            value.value = newState[key].value;
        }
    });
}

export function updateInteractionDisplay(newState, interactionElements) {
    interactionElements.forEach((interaction) => {
        if (interaction.type === "checkbox") {
            interaction.checked = newState[interaction.id].checked;
        } else if (interaction.type === "range") {
            interaction.value = newState[interaction.id].value;
            const event = new Event('input', {bubbles: true});
            interaction.dispatchEvent(event);
        } else {
            interaction.value = newState[interaction.id].value;
        }
    });
}

export async function pollBackendInteractionStates(interactionStateUrl, currentState, interactionElements, interval) {
    async function getInteractionStates() {
        if (polling.getState()) {
            try {
                const response = await fetch(interactionStateUrl, {credentials: 'include'});
                const newState = await response.json();
                if (compareJson(currentState, newState)) {
                    updateInteractionStates(currentState, newState);
                    updateInteractionDisplay(currentState, interactionElements);
                }

            } catch (e) {
                console.log(e.message);
            }
            try {
                const requestInit = {
                    method: "GET",
                    mode: "cors",
                    credentials: "include"
                }
                const response = await fetch('http://localhost:5000/api/products', requestInit);
                const products = await response.json().then((products) => {
                    if (products.length > 0) {
                        updateProducts(products);
                    }
                });


            } catch (e) {
                console.log(e.message);
            }
        }
    }

    await getInteractionStates();
    setInterval(getInteractionStates, interval);
}

export function handleInteractionChange(url, interaction, currentState) {
    polling.pausePolling();
    const newState = currentState;
    if (interaction.type === "checkbox") {
        newState[interaction.id].checked = interaction.checked;
    } else {
        newState[interaction.id].value = interaction.value;
    }
    updateInteractionStates(currentState, newState);
    setState(currentState);
    polling.pausePolling();
}

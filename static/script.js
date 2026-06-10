let currentSessionId = null;

async function loadSessions() {

    const response = await fetch("/sessions");
    const sessions = await response.json();

    const sessionsDiv =
        document.getElementById("sessions");

    sessionsDiv.innerHTML = "";

    sessions.forEach(session => {

        const div = document.createElement("div");

        div.className = "session-item";

        const title =
            document.createElement("span");

        title.innerText =
            session.title;

        title.onclick = () => {

            currentSessionId =
                session.id;

            loadMessages(session.id);
        };

        const renameBtn =
            document.createElement("button");

        renameBtn.innerText = "✏️";

        renameBtn.onclick = (event) => {

            event.stopPropagation();

            renameSession(session.id);
        };

        const deleteBtn =
            document.createElement("button");

        deleteBtn.innerText = "X";

        deleteBtn.onclick = (event) => {

            event.stopPropagation();

            deleteSession(session.id);
        };

        div.appendChild(title);
        div.appendChild(renameBtn);
        div.appendChild(deleteBtn);

        sessionsDiv.appendChild(div);
    });
}

async function loadMessages(sessionId) {

    const response =
        await fetch(`/messages/${sessionId}`);

    const messages =
        await response.json();

    const chatBox =
        document.getElementById("chat-box");

    chatBox.innerHTML = "";

    messages.forEach(message => {

        const div =
            document.createElement("div");

        div.className = message.role;

        div.innerHTML = message.content;

        div.style.marginBottom = "10px";

        chatBox.appendChild(div);
    });
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {

    if (!currentSessionId) {
        alert("Select a chat first");
        return;
    }

    const input =
        document.getElementById("message");

    const message =
        input.value;
    const model =
        document.getElementById("model").value;

    if (!message.trim()) return;

    input.value = "";

    const chatBox =
        document.getElementById("chat-box");

    const loading =
        document.createElement("div");

    loading.id = "loading";

    loading.innerHTML =
        "<i>AI is thinking...</i>";

    chatBox.appendChild(loading);

    chatBox.scrollTop =
        chatBox.scrollHeight;

    const response =
        await fetch(
            `/chat/${currentSessionId}`,
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify({
                    message: message,
                    model: model
                })
            }
        );

    await response.json();

    document
        .getElementById("loading")
        ?.remove();

    loadMessages(currentSessionId);
}
window.onload = () => {
    loadSessions();
};

async function createSession() {

    const title =
        prompt("Enter chat title");

    if (!title) return;

    const response =
        await fetch(
            "/session",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify({
                    title: title
                })
            }
        );

    const session =
        await response.json();

    loadSessions();

    currentSessionId =
        session.session_id;
}




window.onload = () => {

    loadSessions();

    loadModels();

    document
        .getElementById(
            "new-chat-btn"
        )
        .onclick =
            createSession;
};

document.addEventListener(
    "DOMContentLoaded",
    () => {

        document
            .getElementById("message")
            .addEventListener(
                "keydown",
                function(event) {

                    if (
                        event.key === "Enter"
                    ) {
                        sendMessage();
                    }
                }
            );
    }
);

async function deleteSession(sessionId) {

    await fetch(
        `/session/${sessionId}`,
        {
            method: "DELETE"
        }
    );

    loadSessions();

    document.getElementById(
        "chat-box"
    ).innerHTML = "";
}

async function loadModels() {

    const response =
        await fetch("/models");

    const models =
        await response.json();

    const modelSelect =
        document.getElementById("model");

    modelSelect.innerHTML = "";

    models.forEach(model => {

        const option =
            document.createElement("option");

        option.value = model.id;

        option.textContent =
            model.name;

        modelSelect.appendChild(option);
    });
}

async function renameSession(sessionId) {

    const newTitle =
        prompt("Enter new title");

    if (!newTitle) return;

    await fetch(
        `/session/${sessionId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify({
                title: newTitle
            })
        }
    );

    loadSessions();
}
document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("chatForm");
    const input = document.getElementById("id_question");
    const typingIndicator = document.getElementById("typingIndicator");
    const chatMessages = document.getElementById("chatMessages");

    if (!form) return;

    form.addEventListener("submit", async (e) => {

        e.preventDefault();

        const question = input.value.trim();

        if (!question) return;

        
        const formData = new FormData(form);

    
        addUserMessage(question);
        
        input.value = "";

        typingIndicator.style.display = "flex";

        scrollToBottom();

        try {

            const response = await fetch("/chat/", {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error("Server Error: " + response.status);
            }

            const data = await response.json();

            await new Promise(resolve => setTimeout(resolve, 1000));

            typingIndicator.style.display = "none";

            addAIMessage(data.answer);

            scrollToBottom();

        }
        catch (err) {

            typingIndicator.style.display = "none";

            console.error(err);

            alert(err.message);

        }

    });

    function addUserMessage(question) {

        const html = `
            <div class="user-message">
                <div class="message-card">
                    ${question}
                </div>
            </div>
        `;

        typingIndicator.insertAdjacentHTML("beforebegin", html);
    }

    function addAIMessage(answer) {

        const html = `
            <div class="ai-message">

                <div class="ai-avatar">
                    🤖
                </div>

                <div class="message-card">
                    ${answer.replace(/\n/g, "<br>")}
                </div>

            </div>
        `;

        typingIndicator.insertAdjacentHTML("beforebegin", html);
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

});
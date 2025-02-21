function sendMessage() {
    let userInput = document.getElementById("user-input").value.trim();
    if (userInput === "") return;

    let chatBox = document.getElementById("chat-box");

    // แสดงข้อความของผู้ใช้
    let userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.textContent = userInput;
    chatBox.appendChild(userMessage);

    // เรียก API ไปยัง Flask Server
    fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ faculty: userInput })
    })
    .then(response => response.json())
    .then(data => {
        let botMessage = document.createElement("div");
        botMessage.className = "bot-message";
        botMessage.textContent = data.response;
        chatBox.appendChild(botMessage);

        // เลื่อนลงอัตโนมัติ
        chatBox.scrollTop = chatBox.scrollHeight;
    });

    // ล้างช่อง input
    document.getElementById("user-input").value = "";
}

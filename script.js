const startBtn = document.getElementById("startBtn");
const sendBtn = document.getElementById("sendBtn");
const transcriptBox = document.getElementById("transcript");
const departmentSelect = document.getElementById("department");

let recognition;
if ("webkitSpeechRecognition" in window) {
  recognition = new webkitSpeechRecognition();
} else {
  alert("Your browser does not support Speech Recognition");
}

recognition.continuous = false;
recognition.lang = "en-US";

startBtn.onclick = () => {
  transcriptBox.value = "";
  recognition.start();

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    transcriptBox.value = transcript;
  };

  recognition.onerror = (event) => {
    alert("Speech recognition error: " + event.error);
  };
};

sendBtn.onclick = () => {
  const webhook = departmentSelect.value;
  const message = transcriptBox.value.trim();

  if (!message) return alert("No message to send.");
  if (!webhook.startsWith("https://discord.com/api/webhooks/")) return alert("Invalid webhook URL.");

  fetch(webhook, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ content: "```\n" + message + "\n```" })
  })
    .then(res => {
      if (res.ok) {
        alert("✅ Message sent!");
        transcriptBox.value = "";
      } else {
        alert("❌ Failed to send message.");
      }
    });
};

function appendMessage(text, sender) {
  const container = document.getElementById("messages");
  const div = document.createElement("div");
  div.className = `message ${sender}`;
  div.textContent = text;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

async function sendMessage(event) {
  event.preventDefault();
  const input = document.getElementById("chat-input");
  const text = input.value.trim();
  if (!text) return;
  appendMessage(text, "user");
  input.value = "";
  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text }),
  });
  const data = await res.json();
  appendMessage(data.response || "", "bot");
}

async function loadGoals() {
  const res = await fetch("/goals");
  const data = await res.json();
  const container = document.getElementById("goal-cards");
  container.innerHTML = "";
  data.goals.forEach((g) => {
    const card = document.createElement("div");
    card.className = "goal-card";
    card.textContent = g.description;
    container.appendChild(card);
  });
}

async function addGoal(event) {
  event.preventDefault();
  const input = document.getElementById("goal-input");
  const text = input.value.trim();
  if (!text) return;
  await fetch("/goals", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ description: text }),
  });
  input.value = "";
  loadGoals();
}

document.getElementById("chat-form").addEventListener("submit", sendMessage);
document.getElementById("goal-form").addEventListener("submit", addGoal);

window.addEventListener("DOMContentLoaded", loadGoals);

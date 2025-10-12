// University Chat Frontend - با قابلیت ذخیره تاریخچه و دکمه پاک‌سازی

const API_BASE_URL = 'https://hadisadoghiyazdi.loca.lt'; // برای LocalTunnel
//const API_BASE_URL = 'http://localhost:8000';  // برای LocalTunnel، به URL تولیدشده تغییر دهید (مثل https://hadisadoghiyazdi.loca.lt)
const CHAT_API_URL = `${API_BASE_URL}/api/chat`;

// بارگذاری تاریخچه گفتگو از localStorage
let chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];

// المنت‌های صفحه
const chatContainer = document.getElementById('chat-container');
const inputBox = document.getElementById('user-input');
const sendButton = document.getElementById('send-btn');
const clearButton = document.getElementById('clear-btn'); // دکمه جدید
const statusIndicator = document.getElementById('status-indicator');

// بررسی وضعیت سرور بک‌اند
async function checkBackendStatus() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/status`);
    if (res.ok) {
      statusIndicator.textContent = '🟢 متصل به بک‌اند';
    } else {
      statusIndicator.textContent = '🟠 خطای پاسخ سرور';
    }
  } catch (err) {
    statusIndicator.textContent = '🔴 عدم اتصال به بک‌اند';
  }
}

// افزودن پیام به صفحه و ذخیره در localStorage
function appendMessage(sender, text) {
  const msgDiv = document.createElement('div');
  msgDiv.className = sender === 'user' ? 'msg user' : 'msg bot';
  msgDiv.textContent = text;
  chatContainer.appendChild(msgDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  // ذخیره پیام در تاریخچه
  chatHistory.push({ sender, text });
  localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
}

// بارگذاری پیام‌های قبلی هنگام ورود
function loadChatHistory() {
  chatContainer.innerHTML = '';
  chatHistory.forEach(msg => appendMessage(msg.sender, msg.text));
}

// ارسال پیام به بک‌اند
async function sendMessage() {
  const userText = inputBox.value.trim();
  if (!userText) return;

  appendMessage('user', userText);
  inputBox.value = '';

  try {
    const response = await fetch(CHAT_API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userText })
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const data = await response.json();
    appendMessage('bot', data.reply || 'پاسخی دریافت نشد');
  } catch (err) {
    appendMessage('bot', `❌ خطا در ارتباط با بک‌اند: ${err.message}`);
  }
}

// پاک کردن تاریخچه گفتگو
function clearChatHistory() {
  if (!confirm('آیا از حذف کامل تاریخچه گفتگو اطمینان دارید؟')) return;
  localStorage.removeItem('chatHistory');
  chatHistory = [];
  chatContainer.innerHTML = '';
  appendMessage('bot', '🧹 تاریخچه گفتگو پاک شد.');
}

// رویدادها
sendButton.addEventListener('click', sendMessage);
clearButton.addEventListener('click', clearChatHistory);
inputBox.addEventListener('keypress', e => {
  if (e.key === 'Enter') sendMessage();
});

// مقداردهی اولیه
loadChatHistory();
checkBackendStatus();
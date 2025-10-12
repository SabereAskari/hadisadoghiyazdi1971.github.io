// University Chat Frontend - با قابلیت ذخیره تاریخچه و دکمه پاک‌سازی
const API_BASE_URL = 'https://hadisadoghiyazdi.loca.lt';
//const API_BASE_URL = 'http://localhost:8000'; // برای تست محلی
const CHAT_API_URL = `${API_BASE_URL}/api/chat`;

// بارگذاری تاریخچه گفتگو از localStorage
let chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];

// المنت‌های صفحه
const chatContainer = document.getElementById('chatMessages');
const inputBox = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const clearButton = document.getElementById('clearButton');
const statusIndicator = document.getElementById('connectionStatus');
const statusText = document.getElementById('statusText');

// جلوگیری از ارسال مکرر
let isSending = false;

// بررسی وضعیت سرور بک‌اند
async function checkBackendStatus() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/health`);
    if (res.ok) {
      statusIndicator.className = 'status-dot';
      statusText.textContent = '🟢 متصل به بک‌اند';
    } else {
      statusIndicator.className = 'status-dot error';
      statusText.textContent = '🟠 خطای پاسخ سرور';
    }
  } catch (err) {
    statusIndicator.className = 'status-dot error';
    statusText.textContent = '🔴 عدم اتصال به بک‌اند';
  }
}

// افزودن پیام به صفحه و ذخیره در localStorage
function appendMessage(sender, text) {
  const msgDiv = document.createElement('div');
  msgDiv.className = sender === 'user' ? 'message-user' : 'message-bot';
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

// نمایش loading indicator
function showLoading() {
  const loadingIndicator = document.getElementById('loadingIndicator');
  loadingIndicator.classList.remove('d-none');
}

// مخفی کردن loading indicator
function hideLoading() {
  const loadingIndicator = document.getElementById('loadingIndicator');
  loadingIndicator.classList.add('d-none');
}

// ارسال پیام به بک‌اند
async function sendMessage(e) {
  if (e) e.preventDefault(); // جلوگیری از رفتار پیش‌فرض فرم
  if (isSending) return; // جلوگیری از ارسال مکرر
  isSending = true;

  const userText = inputBox.value.trim();
  if (!userText) {
    isSending = false;
    return;
  }

  appendMessage('user', userText);
  inputBox.value = '';
  showLoading();

  try {
    const response = await fetch(CHAT_API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userText, max_sources: 5 })
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const data = await response.json();
    appendMessage('bot', data.answer || 'پاسخی دریافت نشد');
  } catch (err) {
    appendMessage('bot', `❌ خطا در ارتباط با بک‌اند: ${err.message}`);
    console.error('Fetch error:', err);
  } finally {
    hideLoading();
    isSending = false;
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
sendButton.removeEventListener('click', sendMessage); // حذف listenerهای قبلی
sendButton.addEventListener('click', sendMessage);
inputBox.removeEventListener('keypress', sendMessage); // حذف listenerهای قبلی
inputBox.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') sendMessage(e);
});
document.getElementById('chatForm').addEventListener('submit', sendMessage); // اضافه کردن listener برای فرم
clearButton.addEventListener('click', clearChatHistory);

// مقداردهی اولیه
loadChatHistory();
checkBackendStatus();
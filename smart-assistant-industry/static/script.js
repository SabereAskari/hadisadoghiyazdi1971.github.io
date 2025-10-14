// University Chat Frontend - با markdown rendering و UI بهبود یافته
const API_BASE_URL = 'https://hadisadoghiyazdi.loca.lt'; // برای تونل
//const API_BASE_URL = 'http://localhost:8000'; // برای تست محلی
const CHAT_API_URL = `${API_BASE_URL}/api/chat`;

// بارگذاری تاریخچه گفتگو از localStorage
let chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];

// Import marked library for markdown rendering (loaded from CDN in HTML)

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
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${sender === 'user' ? 'message-user' : 'message-bot'}`;
  
  const contentDiv = document.createElement('div');
  contentDiv.className = 'message-content';
  
  // Create header with copy button
  const headerDiv = document.createElement('div');
  headerDiv.className = 'message-header';
  
  const leftSide = document.createElement('div');
  leftSide.className = 'left-side';
  
  const icon = document.createElement('span');
  icon.className = 'message-icon';
  icon.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
  
  const copyBtn = document.createElement('button');
  copyBtn.className = 'copy-btn';
  copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
  copyBtn.onclick = () => copyToClipboard(text);
  copyBtn.title = 'کپی متن';
  
  leftSide.appendChild(icon);
  leftSide.appendChild(copyBtn);
  headerDiv.appendChild(leftSide);
  
  // Create message text
  const textDiv = document.createElement('div');
  textDiv.className = 'message-text';
  
  // Render markdown for bot messages
  if (sender === 'bot' && typeof marked !== 'undefined') {
    // Configure marked for RTL and Persian
    marked.setOptions({
      breaks: true,
      gfm: true
    });
    textDiv.innerHTML = marked.parse(text);
  } else {
    textDiv.textContent = text;
  }
  
  contentDiv.appendChild(headerDiv);
  contentDiv.appendChild(textDiv);
  messageDiv.appendChild(contentDiv);
  
  chatContainer.appendChild(messageDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  // ذخیره پیام در تاریخچه
  chatHistory.push({ sender, text });
  localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
}

// Copy to clipboard function
function copyToClipboard(text) {
  // Remove markdown formatting for plain text copy
  const plainText = text.replace(/\*\*/g, '').replace(/\*/g, '').replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
  
  navigator.clipboard.writeText(plainText).then(() => {
    showNotification('✓ متن کپی شد', 'success');
  }).catch(err => {
    showNotification('✗ خطا در کپی کردن', 'error');
  });
}

// Show notification
function showNotification(message, type) {
  const notification = document.createElement('div');
  notification.className = `copy-notification ${type}`;
  notification.textContent = message;
  notification.style.animation = 'slideInFade 0.3s ease-out';
  
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.style.animation = 'slideOutFade 0.3s ease-out';
    setTimeout(() => {
      document.body.removeChild(notification);
    }, 300);
  }, 2000);
}

// بارگذاری پیام‌های قبلی هنگام ورود
function loadChatHistory() {
  chatContainer.innerHTML = '';
  
  // Filter out error messages from history
  chatHistory = chatHistory.filter(msg => 
    !msg.text.includes('خطا در ارتباط با بک‌اند') && 
    !msg.text.includes('Failed to fetch')
  );
  
  // Save cleaned history
  localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
  
  // Load messages
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
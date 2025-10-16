// University Chat Frontend
const API_BASE_URL = window.location.origin;
const CHAT_API_URL = `${API_BASE_URL}/api/chat`;
const HEALTH_API_URL = `${API_BASE_URL}/api/health`;

// متغیرهای سراسری
let chatHistory = [];
let isConnectedToBackend = false;
let isSending = false;

// المنت‌های DOM
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const clearButton = document.getElementById('clearButton');
const statusIndicator = document.getElementById('connectionStatus');
const statusText = document.getElementById('statusText');

// بررسی وضعیت سرور
async function checkBackendStatus() {
  try {
    const res = await fetch(HEALTH_API_URL);
    if (res.ok) {
      isConnectedToBackend = true;
      statusIndicator.style.backgroundColor = '#27ae60';
      statusText.textContent = '🟢 متصل و آماده';
      return true;
    } else {
      throw new Error(`HTTP ${res.status}`);
    }
  } catch (err) {
    isConnectedToBackend = false;
    statusIndicator.style.backgroundColor = '#e74c3c';
    statusText.textContent = '🔴 عدم اتصال';
    console.error('Backend connection error:', err);
    return false;
  }
}

// اضافه کردن پیام به چت
function appendMessage(sender, text) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message message-${sender}`;
  
  const contentDiv = document.createElement('div');
  contentDiv.className = 'message-content';
  
  // اگر پیام ربات است، از marked استفاده کن
  if (sender === 'bot' && typeof marked !== 'undefined') {
    marked.setOptions({ 
      breaks: true, 
      gfm: true,
      pedantic: false
    });
    contentDiv.innerHTML = marked.parse(text);
  } else {
    contentDiv.textContent = text;
  }
  
  messageDiv.appendChild(contentDiv);
  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  
  // ذخیره پیام
  chatHistory.push({ 
    sender, 
    text, 
    timestamp: new Date().toISOString() 
  });
}

// ارسال پیام
async function sendMessage() {
  if (isSending) return;
  if (!isConnectedToBackend) {
    alert('سرور متصل نیست. لطفا بعدا دوباره تلاش کنید.');
    return;
  }
  
  isSending = true;
  
  const userText = messageInput.value.trim();
  if (!userText) {
    isSending = false;
    return;
  }
  
  // نمایش پیام کاربر
  appendMessage('user', userText);
  messageInput.value = '';
  
  try {
    const response = await fetch(CHAT_API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        message: userText, 
        max_sources: 5 
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    
    const data = await response.json();
    appendMessage('bot', data.answer || 'پاسخی دریافت نشد');
    
  } catch (err) {
    console.error('Send error:', err);
    appendMessage('bot', `❌ خطا: ${err.message}`);
  } finally {
    isSending = false;
  }
}

// پاک کردن گفتگو
function clearChatHistory() {
  if (!confirm('آیا از حذف کامل گفتگو اطمینان دارید؟')) return;
  
  chatHistory = [];
  chatMessages.innerHTML = '';
  appendMessage('bot', '🧹 گفتگو پاک شد. آماده پاسخگویی به سؤالات جدید هستم.');
}

// رویدادها
sendButton.addEventListener('click', sendMessage);
clearButton.addEventListener('click', clearChatHistory);

messageInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// مقداردهی اولیه
async function initializeApp() {
  const status = await checkBackendStatus();
  
  if (status) {
    appendMessage('bot', 'سلام! من دستیار هوشمند شرکت توزیع برق ایران هستم.\n\nمی‌توانید هر سؤالی درباره موضوعات بالا بپرسید.');
  } else {
    appendMessage('bot', '⚠️ سرور متصل نیست. لطفا بعدا دوباره تلاش کنید.');
  }
}

// شروع برنامه
document.addEventListener('DOMContentLoaded', initializeApp);

// بررسی وضعیت هر ۳۰ ثانیه
setInterval(checkBackendStatus, 30000);
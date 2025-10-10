---
layout: persian
classes: wide rtl-layout
dir: rtl
title: "چگونه تونل بسازیم و سرور با ادرس  ثابت  راه اندازی کنیم"
permalink: /teaching//studenteffort/toolkit/localtunneling/
author_profile: true

header:
  overlay_image: "/assets/images/background.jpg"
  overlay_filter: 0.3
  overlay_color: "#5e616c"
  caption: "Photo credit: [**Unsplash**](https://unsplash.com)"
---

## 📋 فهرست مطالب
- [PM2 چیست؟](#pm2-چیست)
- [توضیحات tunnel.js](#توضیحات-tunneljs)
- [روش اجرا](#روش-اجرا)
- [عیب‌یابی](#عیب‌یابی)
- [FAISS چیست؟ یک راهنمای کامل](#faiss-چیست-یک-راهنمای-کامل)


## PM2 چیست؟

**PM2 (Process Manager 2)** یک مدیریت‌کننده process برای برنامه‌های Node.js است که:

### 🎯 مزایای PM2:
- **ریستارت خودکار** اگر برنامه crash کند
- **مانیتورینگ** وضعیت processes
- **لاگ‌گیری** متمرکز
- **شروع خودکار** پس از ریبوت سیستم
- **مدیریت حافظه** و CPU


### 🔧 دستورات مهم PM2:
```bash
# شروع برنامه
pm2 start tunnel.js --name "tunnel"

# مشاهده وضعیت
pm2 status

# مشاهده لاگ‌ها
pm2 logs tunnel

# توقف برنامه
pm2 stop tunnel

# ریستارت
pm2 restart tunnel

# حذف از لیست
pm2 delete tunnel

# ذخیره configuration
pm2 save
```

### ⚙️ چرا از PM2 استفاده کردیم؟
- وقتی LocalTunnel قطع می‌شود، PM2 به طور خودکار آن را ریستارت می‌کند
- مدیریت بهتر لاگ‌ها و خطاها
- امکان مانیتورینگ از راه دور

## توضیحات tunnel.js

### 📜 کد کامل:
```javascript
// tunnel.js
const { exec } = require('child_process');

console.log('🚀 Starting localtunnel...');

const child = exec('npx localtunnel --port 5000 --subdomain hadisadoghiyazdi');

child.stdout.on('data', (data) => {
  const output = data.toString().trim();
  console.log(`[LT] ${output}`);
  
  if (output.includes('your url is:')) {
    console.log('✅ Tunnel is ready! No password required.');
  }
});

child.stderr.on('data', (data) => {
  console.error(`[LT-ERROR] ${data.toString().trim()}`);
});

child.on('close', (code) => {
  console.log(`❌ Tunnel exited with code ${code}`);
  process.exit(code || 1);
});
```

### 🔍 توضیح خط به خط:

1. **وارد کردن ماژول‌ها**:
   ```javascript
   const { exec } = require('child_process');
   ```
   - برای اجرای دستورات سیستم عامل

2. **اجرای LocalTunnel**:
   ```javascript
   const child = exec('npx localtunnel --port 5000 --subdomain hadisadoghiyazdi');
   ```
   - ایجاد تونل روی پورت 5000
   - استفاده از subdomain ثابت

3. **مدیریت خروجی**:
   ```javascript
   child.stdout.on('data', (data) => {
     console.log(`[LT] ${output}`);
   });
   ```
   - نمایش خروجی استاندارد

4. **مدیریت خطاها**:
   ```javascript
   child.stderr.on('data', (data) => {
     console.error(`[LT-ERROR] ${data.toString().trim()}`);
   });
   ```
   - نمایش خطاهای سیستم

5. **مدیریت بسته شدن**:
   ```javascript
   child.on('close', (code) => {
     console.log(`❌ Tunnel exited with code ${code}`);
     process.exit(code || 1);
   });
   ```
   - وقتی تونل بسته می‌شود، PM2 آن را ریستارت می‌کند

## روش اجرا

### 🚀 راه‌اندازی سریع:
1. **فایل `main.bat` را اجرا کنید**
2. **صبر کنید تا همه سرویس‌ها راه‌اندازی شوند**
3. **پسورد نمایش داده شده را کپی کنید**
4. **به آدرس `https://hadisadoghiyazdi.loca.lt` بروید**
5. **پسورد را وارد کنید**

### 📝 فایل main.bat:
```batch
@echo off
cd /d "H:\HadiSadoghiYazdi\hadisadoghiyazdi1971.github.io\hadisadoghiyazdi1971.github.io\smart-repair-api"
title Smart Repair System

echo ========================================
echo 🚀 Starting System
echo ========================================

echo Step 1: Starting Flask...
start "Flask Server" python app.py
timeout /t 3 >nul

echo Step 2: Stopping old tunnel (if exists)...
call pm2 delete tunnel >nul 2>&1
timeout /t 2 >nul

echo Step 3: Starting new tunnel with pm2...
call pm2 start tunnel.js --name "tunnel" --restart-delay 3000
timeout /t 8 >nul

echo Step 4: Getting password...
powershell -Command "(Invoke-WebRequest -Uri 'https://loca.lt/mytunnelpassword' -UseBasicParsing).Content.Trim()" > password.txt
set /p TUNNEL_PASSWORD=<password.txt

echo.
echo ✅ SYSTEM READY!
echo 📍 Flask: http://localhost:5000
echo 🌐 Tunnel: https://hadisadoghiyazdi.loca.lt
echo 🔑 Password: %TUNNEL_PASSWORD%
echo.
echo To view tunnel logs: pm2 logs tunnel
echo To stop tunnel: pm2 stop tunnel
echo.
pause
```

## عیب‌یابی

### 🔧 مشکلات رایج و راه‌حل‌ها:

1. **تونل قطع می‌شود**:
   - PM2 به طور خودکار ریستارت می‌کند
   - دستی: `pm2 restart tunnel`

2. **پسورد کار نمی‌کند**:
   - جدید بگیرید: `https://loca.lt/mytunnelpassword`
   - در فایل `password.txt` ذخیره می‌شود

3. **PM2 کار نمی‌کند**:
   - از `node tunnel.js` مستقیم استفاده کنید
   - یا از `npx pm2` استفاده کنید

4. **پورت 5000 ت است**:
   - برنامه‌های دیگر را ببندید
   - یا پورت را در `app.py` تغییر دهید

### 📞 دستورات مفید برای دیباگ:
```bash
# بررسی processes
pm2 status

# مشاهده لاگ‌های زنده
pm2 logs tunnel

# بررسی پورت
netstat -ano | findstr :5000

# بررسی سرویس Flask
curl http://localhost:5000/health
```

## 🎯 نکات نهایی

- سیستم با **دیتابیس فایل‌محل** کار می‌کند
- **اتصال اینترنتی** با LocalTunnel برقرار می‌شود
- **مدیریت خطا** با PM2 انجام می‌شود
- **پسورد** هر 7 روز یکبار تغییر می‌کند


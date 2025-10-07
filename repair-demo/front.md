---
layout: persian
classes: wide rtl-layout
dir: rtl
title: "سیستم هوشمند تخصیص کارهای تعمیراتی"
permalink: /repair-demo/front/
author_profile: true

header:
  overlay_image: "/assets/images/background.jpg"
  overlay_filter: 0.3
  overlay_color: "#5e616c"
  caption: "Photo credit: [**Unsplash**](https://unsplash.com)"
---

<div style="padding: 20px; max-width: 1200px; margin: 0 auto;">
    <h2>نتایج تخصیص کارهای تعمیراتی</h2>
    <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
        <p>در حال دریافت داده از API...</p>
    </div>
    <div id="result" style="background: white; padding: 20px; border-radius: 8px; border: 2px solid #0066cc; direction: ltr; text-align: left; font-family: 'Courier New', monospace; font-size: 14px; white-space: pre-wrap; max-height: 600px; overflow-y: auto;"></div>
</div>

<script>
// تابع برای نمایش زیباتر JSON
function formatJSON(data) {
    return JSON.stringify(data, null, 2);
}

// تابع اصلی برای دریافت داده
async function fetchData() {
    try {
        const response = await fetch('https://smart-repair-api.onrender.com/optimize', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({allocation_type: "random"})
        });
        
        if (!response.ok) {
            throw new Error(`خطا در دریافت داده: ${response.status}`);
        }
        
        const data = await response.json();
        document.getElementById("result").textContent = formatJSON(data);
        
    } catch (error) {
        document.getElementById("result").textContent = `خطا: ${error.message}`;
    }
}

// اجرا پس از لود کامل صفحه
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(fetchData, 1000); // تاخیر 1 ثانیه برای نمایش بهتر
});
</script>
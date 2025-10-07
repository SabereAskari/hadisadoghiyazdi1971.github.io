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
    <button onclick="fetchData()" style="padding: 10px 20px; background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;">
        🔄 دریافت نتایج جدید
    </button>
    <div id="result" style="background: white; padding: 20px; border-radius: 8px; border: 2px solid #0066cc; margin-top: 20px; min-height: 200px;">
        <p>برای دریافت نتایج، دکمه بالا را کلیک کنید</p>
    </div>
</div>

<script>
// تابع برای نمایش زیبا و خوانا
function formatResults(data) {
    console.log("فرمت کردن داده‌ها:", data);
    
    let html = `
        <div style="text-align: right; direction: rtl;">
            <h3 style="color: #0066cc;">نتایج تخصیص (${data.type_applied === 'random' ? 'تخصیص پایه' : data.type_applied})</h3>
            
            <div style="background: #e8f4fd; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h4>📊 آمار کلی</h4>
                <p><strong>تعداد تیم‌ها:</strong> ${data.summary.total_teams}</p>
                <p><strong>کل زمان کار:</strong> ${data.summary.total_work_time} دقیقه</p>
                <p><strong>کل زمان سفر:</strong> ${data.summary.total_travel_time} دقیقه</p>
                <p><strong>میانگین کارها per تیم:</strong> ${data.summary.average_jobs_per_team.toFixed(1)}</p>
            </div>
    `;

    // نمایش اطلاعات هر تیم
    data.team_assignments.forEach(team => {
        html += `
            <div style="border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 8px; background: #f9f9f9;">
                <h4 style="color: #2c3e50;">👥 تیم: ${team.team_id}</h4>
                <p><strong>تعداد کارها:</strong> ${team.job_count} | 
                   <strong>کل زمان کار:</strong> ${team.total_work_time_min} دقیقه | 
                   <strong>کل زمان سفر:</strong> ${team.total_travel_time_min} دقیقه</p>
        `;

        if (team.route && team.route.length > 0) {
            html += `<h5>📋 کارهای تخصیص داده شده:</h5>
                <ul style="list-style-type: none; padding-right: 0;">`;

            team.route.forEach(job => {
                html += `
                    <li style="padding: 8px; margin-bottom: 5px; background: white; border-right: 3px solid #4CAF50; border-radius: 4px;">
                        <strong>${job.job_id}</strong> - ${job.specialty}<br>
                        <small>⏱️ مدت: ${job.job_duration_min} دقیقه | 
                        🚗 زمان سفر: ${job.travel_time_min} دقیقه | 
                        🕐 ${job.start_time} تا ${job.end_time}</small>
                    </li>
                `;
            });

            html += `</ul>`;
        } else {
            html += `<p>⚠️ هیچ کاری به این تیم تخصیص داده نشد</p>`;
        }

        html += `</div>`;
    });

    html += `</div>`;
    return html;
}

// تابع اصلی برای دریافت داده
async function fetchData() {
    const resultDiv = document.getElementById("result");
    
    try {
        resultDiv.innerHTML = "<p>🔄 در حال دریافت داده از سرور...</p>";
        
        // داده‌های ساده - بدون پارامترهای اضافی که باعث خطا می‌شوند
        const requestData = {
            allocation_type: "random"
            // فقط پارامتر اصلی را می‌فرستیم تا خطا ندهد
        };

        console.log("ارسال درخواست:", requestData);

        const response = await fetch('https://smart-repair-api.onrender.com/optimize', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            throw new Error(`خطای سرور: ${response.status}`);
        }
        
        const data = await response.json();
        console.log("داده‌های دریافت شده:", data);
        
        // حالا تابع formatResults را فراخوانی می‌کنیم
        resultDiv.innerHTML = formatResults(data);
        
    } catch (error) {
        console.error("خطا:", error);
        resultDiv.innerHTML = `
            <div style="color: red; text-align: center; padding: 20px;">
                <h3>❌ خطا در ارتباط با سرور</h3>
                <p>${error.message}</p>
                <p>لطفاً دوباره تلاش کنید یا با پشتیبانی تماس بگیرید.</p>
            </div>
        `;
    }
}

// برای تست: یک بار هنگام لود صفحه اجرا شود
document.addEventListener('DOMContentLoaded', function() {
    // خودکار اجرا نشود - کاربر باید دکمه را کلیک کند
    console.log("صفحه آماده است. برای دریافت داده دکمه را کلیک کنید.");
});
</script>
---
layout: persian  # یا single با کلاس rtl-layout
classes: wide rtl-layout
dir: rtl
title: "رفتار غیرنرمال رانندگان اتوبوس"
permalink: /teaching/studenteffort/toolkit/Abnormal/
author_profile: false
sidebar:
  nav: "toolkit"
header:
  overlay_image: "/assets/images/background.jpg"
  overlay_filter: 0.3
  overlay_color: "#5e616c"
  caption: "Photo credit: [**Unsplash**](https://unsplash.com)"
---

# تشخیص رفتار غیرعادی راننده با استفاده از شبکه عصبی عمیق برروی کامپیوترهای کوچک

## چکیده
در این پژوهش، یک دوربین هوشمند با قابلیت یادگیری مفهوم و پردازش داخلی طراحی شده است که از یک بستر ارتباطی پرسرعت برخوردار است که هزینه انتقال تصاویر را به حداقل می رساند. در این دوربین از ساختار پردازش موازی بر روی دو پردازنده به صورت همزمان استفاده می شود. همچنین، با استفاده از الگوریتم طبقه‌بند افزایشی بر روی وزن‌های طبقه‌بندی برگرفته از هر دوربین، وزن‌های داخلی همه آنها در بازه‌های زمانی تعریف شده، به صورت برخط به‌روزرسانی می‌گردد.

## مقدمه
انگیزه طراحی و ساخت چنین سیستمی، ایجاد بستری هوشمند برای سیستم‌های نظارت تصویری و آنلاین است که بتواند بدون نیاز به حضور نیروی انسانی و به صورت مستمر و هوشمند، محیط را پردازش کند.

## سیستم پیشنهادی

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/Toolkitimages/Abnormal/1-3-flowchart.jpg" alt="IPS3" style="width: 50%; height: 50%; object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
طرح‌واره روش زمان ورود
</div>

### فلوچارت روش پیشنهادی
سیستم از دو بخش کلی تشکیل شده است:
- **بخش داخل خودرو**:
  - سخت افزار
  - الگوریتم تشخیص
- **سرور مرکزی (بخش خارجی خودرو)**:
  - رابط کاربری گرافیکی (GUI)
  - بانک اطلاعاتی

### روش پیشنهادی
اجزای اصلی سیستم:
1. ارائه ساختار و شکل ظاهری مناسب
2. سخت‌افزار مناسب شرایط محیطی
3. پردازش تصویر و سیستم یادگیر با دقت قابل قبول
4. پیاده‌سازی بستر مخابراتی
5. پایگاه‌داده برای ذخیره‌سازی
6. رابط گرافیکی برای تحلیل اطلاعات

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/Toolkitimages/Abnormal/Data_Flow_Diagram.webp" alt="OPT" style="width: 50%; height: 50%; object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
محاسبه پارامترهای بهینه
</div>

### تهیه سخت افزار
قطعات استفاده شده:
- برد Raspberry Pi 3
- برد Tinker Board
- دوربین ۸ مگاپیکسل دید در شب
- سنسورهای مادون قرمز
- مودم اینترنت همراه
- حافظه ۳۲ گیگابایتی

<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>چیدمان ماتریسی تصاویر</title>
</head>
<body>
    <div class="container">
        <h1>نمایش سخت افزار</h1>
         <div class="image-grid">
            <div class="image-item">
                <img src="/assets/Toolkitimages/Abnormal/2-3-inside1.JPG" alt="IPS3">
                <div class="caption">سخت افزار نمای 1</div>
            </div>
            <div class="image-item">
                <img src="/assets/Toolkitimages/Abnormal/3-3-inside2.JPG" alt="IPS3">
                <div class="caption">سخت افزار نمای 2</div>
            </div>
        </div>
    </div>
</body>
</html>

### طراحی نرم افزاری و سرور
- سرور تحت وب با حافظه ۱۴ گیگابایت
- پایگاه‌داده PostgreSQL
- فریم‌ورک Pyramid برای رابط کاربری
- نرم‌افزار تحت وب گرافیکی

<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>چیدمان ماتریسی تصاویر</title>
</head>
<body>
    <div class="container">
        <h1>برخی صفحات طراحی شده</h1>
         <div class="image-grid">
            <div class="image-item">
                <img src="/assets/Toolkitimages/Abnormal/5-3-mainpage.JPG" alt="IPS3">
                <div class="caption">سامانه هوشمند تشخیص تخلفات</div>
            </div>
            <div class="image-item">
                <img src="/assets/Toolkitimages/Abnormal/6-3-singleview.JPG" alt="IPS3">
                <div class="caption">مشخصات</div>
            </div>
        </div>
    </div>
</body>
</html>

### الگوریتم تشخیص
کلاس‌های تشخیص:
- رفتار عادی
- استعمال دخانیات
- صحبت کردن با تلفن همراه
- ارسال پیامک

مراحل پردازش:
1. پیش‌پردازش تصویر
2. استخراج ویژگی‌ها
3. طبقه‌بندی
4. ارسال نتیجه

### شبکه عصبی مورد استفاده
شبکه‌های مورد بررسی:
- AlexNet (دقت ۶۱٪)
- MobileNet (دقت ۶۳٪)
- ResNet50 (دقت ۶۷٪)
- DenseNet (دقت ۷۱٪) - انتخاب نهایی

## ارزیابی سیستم

### مجموعه داده
داده‌های جمع‌آوری شده:
- کلاس عادی: ۱۴۰۵۰ تصویر
- استعمال دخانیات: ۱۱۷۳۰ تصویر
- صحبت با تلفن: ۱۱۷۳۵ تصویر
- ارسال پیامک: ۱۳۶۴۵ تصویر
- مجموع: ۵۱۱۶۰ تصویر

<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>چیدمان ماتریسی تصاویر</title>
</head>
<body>
    <div class="container">
        <h1>رفتار غیرنرمال</h1>
         <div class="image-grid">
            <div class="image-item">
                <img src="/assets/Toolkitimages/Abnormal/8-3-smoking.JPG" alt="abnorma1">
                <div class="caption">رفتار غیرنرمال سیگار کشیدن</div>
            </div>
            <div class="image-item">
                <img src="/assets/Toolkitimages/Abnormal/10-3-texting.JPG" alt="ab2">
                <div class="caption">رفتار غیرنرمال نگاه کردن به موبایل در حین رانندگی</div>
            </div>
        </div>
    </div>
</body>
</html>

### نتایج
- دقت کلی سیستم: ۶۹٪
- دقت در داده‌های روز: ۷۱٪
- دقت در داده‌های شب: ۶۷٪
- بهبود دقت با روش افزایشی: به ۷۳٪

<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>چیدمان ماتریسی تصاویر</title>
</head>
<body>
    <div class="container">
        <h1>رفتار</h1>
         <div class="image-grid">
            <div class="image-item">
                <img src="/assets/Toolkitimages/Abnormal/7-3-normal.JPG" alt="abnorma1">
                <div class="caption">رفتار نرمال </div>
            </div>
            <div class="image-item">
                <img src="/assets/Toolkitimages/Abnormal/9-3-phonecall.JPG" alt="ab2">
                <div class="caption">رفتار غیرنرمال مکالمه با موبایل در حین رانندگی</div>
            </div>
        </div>
    </div>
</body>
</html>

## نتیجه‌گیری
سیستم طراحی شده توانست با موفقیت پیاده‌سازی شود و چالش‌های محیط واقعی را حل کند. این سیستم قابلیت توسعه برای کاربردهای دیگر مانند تشخیص سرقت و نظارت بر بیماران را دارد.

```mermaid
graph TD
    A[دوربین هوشمند] --> B[پردازش موازی]
    B --> C[تشخیص رفتار]
    C --> D[ارسال نتایج]
    D --> E[سرور مرکزی]
    E --> F[ذخیره در پایگاه داده]
    F --> G[نمایش در رابط کاربری]
```

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/Toolkitimages/Abnormal/flowchart.JPG" alt="OPT" style="width: 50%; height: 50%; object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
فلوچارت
</div>

## جزییات بیشتر در پایان نامه سید محمد حسینی کارشناسی ارشد از دانشگاه فردوسی مشهد 

<style>
        body {
            font-family: Tahoma, Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
            color: #333;
        }
         .container {
            max-width: 1000px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
        }
         h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
        }
         .image-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
         .image-item {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .image-item img {
            width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .caption {
            text-align: center;
            margin-top: 10px;
            font-weight: bold;
            color: #2c3e50;
        }
         @media (max-width: 768px) {
            .image-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
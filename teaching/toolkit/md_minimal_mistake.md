---
layout: persian
classes: wide rtl-layout
dir: rtl
title: "راهنمای کامل مارک‌داون برای سایت آموزشی"
permalink: /teaching//studenteffort/toolkit/md_minimal_mistake/
author_profile: true

header:
  overlay_image: "/assets/images/background.jpg"
  overlay_filter: 0.3
  overlay_color: "#5e616c"
  caption: "Photo credit: [**Unsplash**](https://unsplash.com)"
---

# راهنمای نگارش محتوا با مارک‌داون

این راهنما برای کمک به دانشجویان جهت ایجاد محتوای استاندارد برای سایت آموزشی تهیه شده است.

دستورالعمل ایجاد مارک‌داون برای Minimal Mistakes
ساختار کلی فایل



## 🎯 ساختار اصلی فایل



1. هدر فایل (Front Matter)
markdown
---
layout: persian  # یا single با کلاس rtl-layout
classes: wide rtl-layout
dir: rtl
title: "عنوان مطلب به فارسی"
permalink: /filename/
author_profile: true

header:
  overlay_image: "/assets/images/background.jpg"
  overlay_filter: 0.3
  overlay_color: "#5e616c"
  caption: "Photo credit: [**Unsplash**](https://unsplash.com)"
---
نکات مهم:

نام فایل باید انگلیسی باشد (مثال: my-post.md)

از layout: persian برای صفحات فارسی استفاده کنید

2. هایپرلینک‌ها
markdown
<a href="https://www.um.ac.ir/" style="text-decoration:underline; color:green;" target="_blank">
<strong>دانشگاه فردوسی مشهد</strong>
</a>
3. متن انگلیسی
markdown
<div class="english-text">
<strong>
English Text Here
</strong>
</div>
4. تصاویر
markdown
<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/patterneffort/DeepDream/Name.jpg" alt="IPS1" style="width: 50%; height: 50%; object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
توضیحات تصویر به فارسی
</div>
5. فرمول‌های ریاضی
markdown
یک خط خالی قبل از فرمول

$$
RSS = -10n \log_{10}\left(\frac{d}{d_0}\right) + A
$$

یک خط خالی بعد از فرمول
6. راه‌های ارتباطی
markdown
## 📬 راه‌های ارتباطی

<p align="center">
  <a href="https://github.com/YourUsername">
    <img src="https://img.shields.io/badge/GitHub-YourUsername-181717?logo=github&logoColor=white&style=flat-square" />
  </a>
  <a href="mailto:your.email@gmail.com">
    <img src="https://img.shields.io/badge/Email-your.email%40gmail.com-EA4335?logo=gmail&logoColor=white&style=flat-square" />
  </a>
</p>
عناصر متعارف مارک‌داون
عناوین
markdown
# عنوان اصلی (H1)

## عنوان فرعی (H2)

### زیرعنوان (H3)
لیست‌ها
markdown
- آیتم اول
- آیتم دوم
- آیتم سوم

1. آیتم اول
2. آیتم دوم
3. آیتم سوم
کد
markdown
```python
def hello_world():
    print("Hello World!")
```
نقل‌قول
markdown
> این یک نقل قول است
> که می‌تواند چند خطی باشد
نمونه فایل کامل
markdown
---
layout: persian
classes: wide rtl-layout
dir: rtl
title: "آموزش مارک‌داون برای Minimal Mistakes"
permalink: /markdown-guide/
author_profile: true

header:
  overlay_image: "/assets/images/background.jpg"
  overlay_filter: 0.3
  overlay_color: "#5e616c"
  caption: "Photo credit: [**Unsplash**](https://unsplash.com)"
---

# عنوان مطلب

این یک پاراگراف نمونه است. شما می‌توانید از 
<a href="https://www.example.com/" style="text-decoration:underline; color:green;" target="_blank">
<strong>این لینک</strong>
</a>
استفاده کنید.

## بخش دوم

<div class="english-text">
<strong>
This is English text that will be displayed with proper formatting.
</strong>
</div>

### زیربخش

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/images/sample.jpg" alt="Sample Image" style="width: 50%; height: 50%; object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
این یک تصویر نمونه است
</div>

فرمول ریاضی:

$$
E = mc^2
$$

## 📬 راه‌های ارتباطی

<p align="center">
  <a href="https://github.com/YourUsername">
    <img src="https://img.shields.io/badge/GitHub-YourUsername-181717?logo=github&logoColor=white&style=flat-square" />
  </a>
  <a href="mailto:your.email@gmail.com">
    <img src="https://img.shields.io/badge/Email-your.email%40gmail.com-EA4335?logo=gmail&logoColor=white&style=flat-square" />
  </a>
</p>


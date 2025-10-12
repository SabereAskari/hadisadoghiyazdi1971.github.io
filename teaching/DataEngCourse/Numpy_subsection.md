---
layout: persian
classes: wide rtl-layout
dir: rtl
title: "چگونه پروژه درسی خود را در زمانی کوتاه آماده کنیم"
permalink: /teaching/DataEngCourse/Numpysubsection/
author_profile: true

header:
  overlay_image: "/assets/images/background.jpg"
  overlay_filter: 0.3
  overlay_color: "#5e616c"
  caption: "Photo credit: [**Unsplash**](https://unsplash.com)"
---

# مبانی آرایه‌های NumPy

## مقدمه
دستکاری داده در پایتون تقریباً معادل دستکاری آرایه‌های NumPy است. حتی ابزارهای جدیدتری مانند Pandas نیز بر اساس آرایه‌های NumPy ساخته شده‌اند. این بخش مثال‌های متعددی از دستکاری آرایه‌های NumPy برای دسترسی به داده و زیرآرایه‌ها، و همچنین تقسیم، تغییر شکل و اتصال آرایه‌ها ارائه می‌دهد.

## ویژگی‌های آرایه‌ها

### مثال عملی: داده‌های دمای شهرها

```python
import numpy as np

# داده‌های دمای روزانه ۴ شهر در ۵ روز متوالی
np.random.seed(42)  # برای تولید نتایج یکسان
temperatures = np.random.randint(15, 35, size=(4, 5))
print("داده‌های دما:")
print(temperatures)
print("\nابعاد آرایه:", temperatures.ndim)
print("شکل آرایه:", temperatures.shape)
print("تعداد کل عناصر:", temperatures.size)
print("نوع داده:", temperatures.dtype)
```

**خروجی:**
```
داده‌های دما:
[[16 29 34 22 19]
 [24 17 33 32 29]
 [26 20 26 26 21]
 [34 34 21 18 34]]

ابعاد آرایه: 2
شکل آرایه: (4, 5)
تعداد کل عناصر: 20
نوع داده: int64
```

## اندیس‌گذاری آرایه‌ها: دسترسی به عناصر منفرد

### مثال عملی: دسترسی به دمای خاص

```python
# داده‌های فروش روزانه ۳ محصول در ۷ روز
sales_data = np.array([
    [120, 150, 80, 200, 90, 180, 110],   # محصول اول
    [45, 60, 75, 55, 65, 70, 50],        # محصول دوم
    [300, 280, 320, 290, 310, 295, 305]  # محصول سوم
])

print("کل داده‌های فروش:")
print(sales_data)
print("\nفروش محصول اول در روز اول:", sales_data[0, 0])
print("فروش محصول سوم در روز آخر:", sales_data[2, -1])
print("فروش محصول دوم در روز چهارم:", sales_data[1, 3])

# تغییر یک مقدار
sales_data[0, 0] = 130
print("\nپس از به‌روزرسانی:")
print(sales_data[0, :])  # تمام فروش‌های محصول اول
```

## برش آرایه‌ها: دسترسی به زیرآرایه‌ها

### مثال عملی: تحلیل داده‌های دانشجویان

```python
# نمرات ۶ دانشجو در ۴ درس
grades = np.array([
    [18, 17, 16, 19],  # دانشجوی ۱
    [15, 14, 12, 16],  # دانشجوی ۲
    [19, 18, 17, 20],  # دانشجوی ۳
    [13, 15, 14, 12],  # دانشجوی ۴
    [16, 17, 15, 18],  # دانشجوی ۵
    [14, 13, 16, 15]   # دانشجوی ۶
])

print("تمام نمرات:")
print(grades)

print("\nسه دانشجوی اول:")
print(grades[:3])  # سطرهای ۰ تا ۲

print("\nدو درس اول تمام دانشجویان:")
print(grades[:, :2])  # تمام سطرها، ستون‌های ۰ و ۱

print("\nهر دانشجوی دوم:")
print(grades[1::2])  # شروع از سطر ۱، گام ۲

print("\nبرعکس کردن ترتیب دانشجویان:")
print(grades[::-1])
```

## تغییر شکل آرایه‌ها

### مثال عملی: سازماندهی داده‌های سنسور

```python
# داده‌های سنسور دما از ۱۲ سنسور در ۲۴ ساعت
sensor_data = np.arange(1, 289)  # 12×24 = 288

# تغییر شکل به ماتریس ۱۲×۲۴ (سنسورها × ساعت)
daily_readings = sensor_data.reshape((12, 24))
print("داده‌های سنسور به شکل ساعتی:")
print(daily_readings.shape)

# تغییر شکل به ۳ بعد: روزها × سنسورها × ساعت
weekly_data = sensor_data.reshape((12, 24, 1))
print("\nشکل جدید برای تحلیل هفتگی:", weekly_data.shape)

# ایجاد بردار ستونی برای تحلیل‌های آماری
sensor_1_data = daily_readings[0, :]  # داده‌های سنسور اول
sensor_1_column = sensor_1_data[:, np.newaxis]
print("\nداده‌های سنسور اول به شکل ستونی:")
print(sensor_1_column.shape)
```

## الحاق و تقسیم آرایه‌ها

### مثال عملی: ادغام داده‌های فصلی

```python
# داده‌های فروش فصل بهار (۳ ماه)
spring_sales = np.array([
    [100, 150, 200],  # محصول A
    [80, 120, 160]    # محصول B
])

# داده‌های فروش فصل تابستان
summer_sales = np.array([
    [180, 220, 250],  # محصول A
    [140, 180, 200]   # محصول B
])

print("فروش بهار:")
print(spring_sales)
print("\nفروش تابستان:")
print(summer_sales)

# الحاق عمودی (اضافه کردن ردیف‌ها)
annual_sales = np.vstack([spring_sales, summer_sales])
print("\nفروش کل سال:")
print(annual_sales)

# الحاق افقی (اضافه کردن ستون‌ها)
first_half = np.array([[100, 150], [80, 120]])
second_half = np.array([[200], [160]])
full_spring = np.hstack([first_half, second_half])
print("\nفروش بهار پس از الحاق:")
print(full_spring)
```

### مثال عملی: تقسیم داده‌های آموزشی و تست

```python
# داده‌های ۸ روز اندازه‌گیری
all_data = np.array([25, 28, 30, 22, 26, 29, 31, 24])

print("تمام داده‌ها:", all_data)

# تقسیم به داده‌های آموزشی و تست
train_data, test_data = np.split(all_data, [6])
print("داده‌های آموزشی (۶ روز اول):", train_data)
print("داده‌های تست (۲ روز آخر):", test_data)

# مثال دو بعدی: تقسیم داده‌های بیماران
patient_data = np.array([
    [1, 72, 160, 25],   # بیمار ۱
    [2, 65, 155, 30],   # بیمار ۲
    [3, 80, 180, 45],   # بیمار ۳
    [4, 68, 165, 35],   # بیمار ۴
    [5, 75, 170, 28]    # بیمار ۵
])

# تقسیم به ویژگی‌ها و برچسب‌ها
features, labels = np.hsplit(patient_data, [3])
print("\nویژگی‌های بیماران (سن، وزن، قد):")
print(features)
print("\nبرچسب‌ها (شماره بیمار):")
print(labels)
```

## نمایش‌ها در مقابل کپی‌ها

### مثال عملی: به‌روزرسانی داده‌های سهام

```python
# داده‌های قیمت سهام ۳ شرکت در ۵ روز
stock_prices = np.array([
    [100, 102, 105, 103, 107],  # شرکت A
    [50, 52, 51, 53, 55],       # شرکت B
    [200, 198, 205, 202, 210]   # شرکت C
])

print("قیمت‌های اصلی سهام:")
print(stock_prices)

# ایجاد یک نمایش (view)
weekly_view = stock_prices[:2, :3]  # دو شرکت اول، سه روز اول
print("\nنمایش هفتگی:")
print(weekly_view)

# تغییر از طریق نمایش
weekly_view[0, 0] = 101
print("\nپس از تغییر از طریق نمایش:")
print(stock_prices)  # تغییر در داده‌های اصلی!

# ایجاد کپی
weekly_copy = stock_prices[:2, :3].copy()
weekly_copy[0, 1] = 999
print("\nپس از تغییر کپی:")
print(stock_prices)  # بدون تغییر در داده‌های اصلی
```

## خلاصه

این عملیات پایه، بلوک‌های ساختمانی بسیاری از مثال‌های پیشرفته‌تر را تشکیل می‌دهند. درک این مفاهیم برای کار مؤثر با داده در پایتون ضروری است.
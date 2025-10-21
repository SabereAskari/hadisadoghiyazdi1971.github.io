---
layout: persian
classes: wide rtl-layout
dir: rtl
title: "رویای عمیق"
permalink: /teaching/studenteffort/patterneffort/DeepDream
author_profile: true

header:
  overlay_image: "/assets/images/background.jpg"
  overlay_filter: 0.3
  overlay_color: "#5e616c"
  caption: "Photo credit: [Unsplash](https://unsplash.com)"
---



# Deep Dream   رویای عمیق

---

<div style="display: flex; justify-content: start; align-items: center; gap: 10px;">
    <img src="https://upload.wikimedia.org/wikipedia/fa/e/e3/FUM_Logo.png" width="169" height="217" alt="STFT-overview" style="object-fit: contain;">
</div>

<div style="display: flex; justify-content: start; align-items: center; gap: 10px; ">
    <img src="/assets/patterneffort/deepdream/images/my photo.jpg" alt="IPS1" style="width: 200px; height: 200px; object-fit: contain;">
</div>

**نویسنده**: صابره عسکری

- <sabereaskari14@gmail.com>

**دانشگاه فردوسی مشهد**
**دانشکده مهندسی**
**گروه کامپیوتر**
دانشجوی ارشد هوش‌ مصنوعی دانشگاه فردوسی مشهد  
آزمایشگاه شناسایی الگو دکتر هادی صدوقی یزدی 

---

شبکه‌های عصبی مصنوعی پیشرفت‌های اخیر قابل توجهی را در طبقه‌بندی تصویر و تشخیص گفتار ایجاد کرده‌اند . اما اگرچه این ابزارها بسیار مفید و مبتنی بر روش‌های ریاضی شناخته شده هستند، اما در واقع ما به طرز شگفت‌آوری درک کمی از اینکه چرا برخی مدل‌ها کار می‌کنند و برخی دیگر نه، داریم. بنابراین بیایید نگاهی به چند تکنیک ساده برای بررسی درون این شبکه‌ها بیندازیم.

ما یک شبکه عصبی مصنوعی را با نشان دادن میلیون‌ها مثال آموزشی و تنظیم تدریجی پارامترهای شبکه تا زمانی که طبقه‌بندی‌های مورد نظر ما را ارائه دهد، آموزش می‌دهیم. این شبکه معمولاً از ۱۰ تا ۳۰ لایه انباشته از نورون‌های مصنوعی تشکیل شده است. هر تصویر به لایه ورودی وارد می‌شود که سپس با لایه بعدی ارتباط برقرار می‌کند تا در نهایت به لایه «خروجی» برسد. «پاسخ» شبکه از این لایه خروجی نهایی می‌آید.

**یکی از چالش‌های شبکه‌های عصبی، درک دقیق آنچه در هر لایه می‌گذرد**، است. ما می‌دانیم که پس از آموزش، هر لایه به تدریج ویژگی‌های سطح بالاتر و بالاتر تصویر را استخراج می‌کند، تا زمانی که لایه نهایی اساساً در مورد آنچه تصویر نشان می‌دهد تصمیمی بگیرد. به عنوان مثال، لایه اول ممکن است به دنبال لبه‌ها یا گوشه‌ها باشد. لایه‌های میانی ویژگی‌های اساسی را تفسیر می‌کنند تا به دنبال اشکال یا اجزای کلی، مانند یک در یا یک برگ، باشند. چند لایه نهایی این ویژگی‌ها را در تفسیرهای کامل جمع می‌کنند - این نورون‌ها در پاسخ به چیزهای بسیار پیچیده‌ای مانند کل ساختمان‌ها یا درختان فعال می‌شوند.

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/patterneffort/deepdream/images/Screenshot 2025-10-14 0145319.png" alt="IPS1" style="object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px; rgba(52, 51, 51, 1)">
شمای یک شبکه ی عصبی
</div>

یک راه برای تجسم آنچه اتفاق می‌افتد این است که شبکه را وارونه کنیم و از آن بخواهیم که یک تصویر ورودی را به گونه‌ای بهبود بخشد که تفسیر خاصی را ایجاد کند. فرض کنید می‌خواهید بدانید چه نوع تصویری منجر به "موز" می‌شود. با تصویری پر از نویز تصادفی شروع کنید، سپس به تدریج تصویر را به سمت آنچه شبکه عصبی موز می‌داند، تغییر دهید . این به خودی خود خیلی خوب کار نمی‌کند، اما اگر یک محدودیت قبلی اعمال کنیم که تصویر باید آمار مشابهی با تصاویر طبیعی داشته باشد، مانند پیکسل‌های همسایه که نیاز به همبستگی دارند، این کار را انجام می‌دهد.

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/patterneffort/deepdream/images/image1.png" alt="IPS1" style="object-fit: contain;">
</div>

بنابراین یک نکته‌ی غافلگیرکننده وجود دارد: شبکه‌های عصبی که برای تمایز قائل شدن بین انواع مختلف تصاویر آموزش دیده‌اند، اطلاعات زیادی برای تولید تصاویر نیز دارند. به مثال‌های بیشتری در کلاس‌های مختلف نگاهی بیندازید:

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/patterneffort/deepdream/images/image2.png" alt="IPS1" style="object-fit: contain;">
</div>

چرا این مهم است؟ خب، ما شبکه‌ها را با نشان دادن مثال‌های زیادی از آنچه می‌خواهیم یاد بگیرند، آموزش می‌دهیم، به این امید که اصل مطلب را استخراج کنند (مثلاً یک چنگال به یک دسته و ۲الی۴ دندانه نیاز دارد) و یاد بگیرند که آنچه مهم نیست را نادیده بگیرند (یک چنگال می‌تواند هر شکل، اندازه، رنگ یا جهتی داشته باشد). اما چگونه بررسی می‌کنید که شبکه ویژگی‌های صحیح را به درستی یاد گرفته است؟ این می‌تواند به تجسم نمایش شبکه از یک چنگال کمک کند.

در واقع، در برخی موارد، این نشان می‌دهد که شبکه عصبی کاملاً به دنبال چیزی که ما فکر می‌کردیم نیست. به عنوان مثال، در اینجا یک شبکه عصبی که ما طراحی کردیم، دمبل‌ها را به این شکل در نظر گرفتیم:

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/patterneffort/deepdream/images/image3.png" alt="IPS1" style="object-fit: contain;">
</div>

خب، دمبل‌هایی آنجا هستند، اما به نظر می‌رسد هیچ تصویری از دمبل بدون وجود یک وزنه‌بردار عضلانی که آنها را بلند کند، کامل نیست. در این مورد، شبکه نتوانسته است جوهره دمبل را به طور کامل استخراج کند. شاید هرگز دمبلی بدون دستی که آن را نگه داشته باشد، نشان داده نشده باشد. تجسم می‌تواند به ما در اصلاح این نوع اشتباهات آموزشی کمک کند.

به جای اینکه دقیقاً تجویز کنیم که می‌خواهیم کدام ویژگی را شبکه تقویت کند، می‌توانیم به شبکه اجازه دهیم که این تصمیم را بگیرد. در این حالت، ما به سادگی یک تصویر یا عکس دلخواه را به شبکه می‌دهیم و اجازه می‌دهیم شبکه تصویر را تجزیه و تحلیل کند. سپس یک لایه را انتخاب می‌کنیم و از شبکه می‌خواهیم هر آنچه را که تشخیص می‌دهد، بهبود بخشد. هر لایه از شبکه با ویژگی‌هایی در سطح متفاوتی از انتزاع سروکار دارد، بنابراین پیچیدگی ویژگی‌هایی که تولید می‌کنیم به لایه‌ای که برای بهبود انتخاب می‌کنیم بستگی دارد. به عنوان مثال، لایه‌های پایین‌تر تمایل به ایجاد خطوط یا الگوهای ساده تزیینی دارند، زیرا این لایه‌ها به ویژگی‌های اساسی مانند لبه‌ها و جهت‌گیری‌های آنها حساس هستند.

<div style="display: flex; justify-content: center; align-items: center; gap: 30px;">
    <img src="/assets/patterneffort/deepdream/images/image4.png" alt="IPS1" style="object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px; color: rgba(52, 51, 51, 1)">
چپ: عکس اصلی از زاچی ایونور . راست: پردازش شده توسط گونتر نواک، مهندس نرم‌افزار
</div>

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/patterneffort/deepdream/images/image5.png" alt="IPS1" style="object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;color: rgba(52, 51, 51, 1)">
چپ: نقاشی اصلی اثر ژرژ سورا . راست: تصاویر پردازش‌شده اثر متیو مک‌ناتون، مهندس نرم‌افزار
</div>

اگر لایه‌های سطح بالاتر را انتخاب کنیم، که ویژگی‌های پیچیده‌تری را در تصاویر شناسایی می‌کنند، ویژگی‌های پیچیده یا حتی کل اشیاء تمایل به ظهور دارند. باز هم، ما فقط با یک تصویر موجود شروع می‌کنیم و آن را به شبکه عصبی خود می‌دهیم. از شبکه می‌پرسیم: **"هر چیزی که آنجا می‌بینی، من بیشتر از آن می‌خواهم!"** این یک حلقه بازخورد ایجاد می‌کند: اگر ابری کمی شبیه پرنده باشد، شبکه آن را بیشتر شبیه پرنده می‌کند. این به نوبه خود باعث می‌شود شبکه در عبور بعدی پرنده را حتی قوی‌تر تشخیص دهد و به همین ترتیب ادامه یابد، تا زمانی که یک پرنده با جزئیات بسیار بالا، ظاهراً از ناکجاآباد، ظاهر شود.

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/patterneffort/deepdream/images/image6.png" alt="IPS1" style="object-fit: contain;">
</div>

نتایج جذاب هستند - حتی یک شبکه عصبی نسبتاً ساده می‌تواند برای تفسیر بیش از حد یک تصویر استفاده شود، درست مانند دوران کودکی که از تماشای ابرها و تفسیر شکل‌های تصادفی لذت می‌بردیم. این شبکه عمدتاً بر روی تصاویر حیوانات آموزش دیده است، بنابراین طبیعتاً تمایل دارد اشکال را به عنوان حیوان تفسیر کند. اما از آنجا که داده‌ها با چنین انتزاع بالایی ذخیره می‌شوند، نتایج ترکیبی جالب از این ویژگی‌های آموخته شده هستند.

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/patterneffort/deepdream/images/image7.png" alt="IPS1" style="object-fit: contain;">
</div>

البته، ما می‌توانیم با این تکنیک کارهای بیشتری از تماشای ابرها انجام دهیم. می‌توانیم آن را روی هر نوع تصویری اعمال کنیم. نتایج بسته به نوع تصویر کاملاً متفاوت است، زیرا ویژگی‌هایی که وارد می‌شوند، شبکه را به سمت تفاسیر خاصی سوق می‌دهند. به عنوان مثال، خطوط افق تمایل دارند پر از برج‌ها و بتکده‌ها شوند. سنگ‌ها و درختان به ساختمان تبدیل می‌شوند. پرندگان و حشرات در تصاویر برگ‌ها ظاهر می‌شوند.

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/patterneffort/deepdream/images/image8.png" alt="IPS1" style="object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;color: rgba(52, 51, 51, 1)">
تصویر اصلی بر نوع اشیایی که در تصویر پردازش شده شکل می‌گیرند، تأثیر می‌گذارد.
</div>

این تکنیک به ما یک حس کیفی از سطح انتزاعی که یک لایه خاص در درک تصاویر به آن دست یافته است، می‌دهد. ما این تکنیک را با اشاره به معماری شبکه عصبی مورد استفاده، «Inceptionism» می‌نامیم. برای جفت تصاویر بیشتر و نتایج پردازش شده آنها، به علاوه برخی انیمیشن‌های ویدیویی جالب، به گالری Inceptionism ما مراجعه کنید.

#### باید عمیق‌تر برویم: تکرارها

اگر الگوریتم را به صورت تکراری روی خروجی‌های خودش اعمال کنیم و بعد از هر تکرار مقداری بزرگنمایی اعمال کنیم، جریان بی‌پایانی از برداشت‌های جدید به دست می‌آوریم که مجموعه چیزهایی را که شبکه در مورد آنها می‌داند، بررسی می‌کند. ما حتی می‌توانیم این فرآیند را از یک تصویر با نویز تصادفی شروع کنیم، به طوری که نتیجه کاملاً نتیجه شبکه عصبی شود، همانطور که در تصاویر زیر مشاهده می‌شود:

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/patterneffort/deepdream/images/image9.png" alt="IPS1" style="object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px; rgba(52, 51, 51, 1)">
«رویاهای» شبکه عصبی - که صرفاً از نویز تصادفی و با استفاده از شبکه‌ای که توسط <a href="https://www.um.ac.ir/" style="text-decoration:underline; color:green;" target="_blank">
آزمایشگاه علوم کامپیوتر و هوش مصنوعی MIT روی مکان‌ها آموزش دیده است، تولید شده‌اند. برای مشاهده نسخه‌های با وضوح بالا از تصاویر بالا و موارد دیگر، به
</a> 
<a href="https://www.um.ac.ir/" style="text-decoration:underline; color:rgba(114, 230, 5, 1);" target="_blank">
گالری Inceptionism
</a> مراجعه کنید  (تصاویر با علامت «Places205-GoogLeNet» با استفاده از این شبکه ساخته شده‌اند).
</div>

تکنیک‌های ارائه شده در اینجا به ما کمک می‌کنند تا درک و تجسم کنیم که چگونه شبکه‌های عصبی قادر به انجام وظایف دشوار طبقه‌بندی، بهبود معماری شبکه و بررسی آنچه شبکه در طول آموزش آموخته است، هستند. همچنین این موضوع ما را به این فکر می‌اندازد که آیا شبکه‌های عصبی می‌توانند به ابزاری برای هنرمندان تبدیل شوند - راهی جدید برای ترکیب مفاهیم بصری - یا شاید حتی کمی ریشه‌های فرآیند خلاقیت را به طور کلی روشن کنند.

 ایجاد کرده‌اند . اما اگرچه این ابزارها بسیار مفید و مبتنی بر روش‌های ریاضی شناخته شده هستند، اما در واقع ما به طرز شگفت‌آوری درک کمی از اینکه چرا برخی مدل‌ها کار می‌کنند و برخی دیگر نه، داریم. بنابراین بیایید نگاهی به چند تکنیک ساده برای بررسی درون این شبکه‌ها بیندازیم.

ما یک شبکه عصبی مصنوعی را با نشان دادن میلیون‌ها مثال آموزشی و تنظیم تدریجی پارامترهای شبکه تا زمانی که طبقه‌بندی‌های مورد نظر ما را ارائه دهد، آموزش می‌دهیم. این شبکه معمولاً از ۱۰ تا ۳۰ لایه انباشته از نورون‌های مصنوعی تشکیل شده است. هر تصویر به لایه ورودی وارد می‌شود که سپس با لایه بعدی ارتباط برقرار می‌کند تا در نهایت به لایه «خروجی» برسد. «پاسخ» شبکه از این لایه خروجی نهایی می‌آید.

یکی از چالش‌های شبکه‌های عصبی، درک دقیق آنچه در هر لایه می‌گذرد، است. ما می‌دانیم که پس از آموزش، هر لایه به تدریج ویژگی‌های سطح بالاتر و بالاتر تصویر را استخراج می‌کند، تا زمانی که لایه نهایی اساساً در مورد آنچه تصویر نشان می‌دهد تصمیمی بگیرد. به عنوان مثال، لایه اول ممکن است به دنبال لبه‌ها یا گوشه‌ها باشد. لایه‌های میانی ویژگی‌های اساسی را تفسیر می‌کنند تا به دنبال اشکال یا اجزای کلی، مانند یک در یا یک برگ، باشند. چند لایه نهایی این ویژگی‌ها را در تفسیرهای کامل جمع می‌کنند - این نورون‌ها در پاسخ به چیزهای بسیار پیچیده‌ای مانند کل ساختمان‌ها یا درختان فعال می‌شوند.

یک راه برای تجسم آنچه اتفاق می‌افتد این است که شبکه را وارونه کنیم و از آن بخواهیم که یک تصویر ورودی را به گونه‌ای بهبود بخشد که تفسیر خاصی را ایجاد کند. فرض کنید می‌خواهید بدانید چه نوع تصویری منجر به "موز" می‌شود. با تصویری پر از نویز تصادفی شروع کنید، سپس به تدریج تصویر را به سمت آنچه شبکه عصبی موز می‌داند، تغییر دهید (به کارهای مرتبط در  مراجعه کنید ). این به خودی خود خیلی خوب کار نمی‌کند، اما اگر یک محدودیت قبلی اعمال کنیم که تصویر باید آمار مشابهی با تصاویر طبیعی داشته باشد، مانند پیکسل‌های همسایه که نیاز به همبستگی دارند، این کار را انجام می‌دهد.

---

# رویای عمیق چگونه کار می‌کند؟

در هسته‌ی خود، رویای عمیق از یک **CNN** استفاده می‌کند که روی یک مجموعه‌داده‌ی عظیم از تصاویر آموزش دیده است. یک **CNN** از لایه‌هایی از گره‌های به‌هم‌پیوسته یا نورون‌ها تشکیل شده است که هر لایه مسئول تشخیص سطوح مختلفی از ویژگی‌های یک تصویر است—از لبه‌های ساده گرفته تا اشیای پیچیده.

زمانی‌که یک تصویر به رویای عمیق داده می‌شود، برنامه الگوهایی را که یاد گرفته شناسایی کند تقویت می‌کند. این کار از طریق فرایندی به‌نام *"Inceptionism"* انجام می‌شود؛ جایی که شبکه دستور می‌گیرد تشخیص ویژگی‌ها را در لایه‌های مختلف به حداکثر برساند.

#### مراحل ایجاد DeepDream

1. ابتدا با یک تصویر شروع می‌کنیم و آن را به یک شبکه‌ی عصبی پیچشی (Convolutional Neural Network) از پیش آموزش‌دیده مانند Inception وارد می‌کنیم.

2. به‌جای اینکه فقط فعال‌سازی یک فیلتر خاص را بیشینه کنیم، تلاش می‌کنیم فعال‌سازیِ کلِ یک لایه را بیشینه کنیم. برای این منظور، یک تابع هزینه (Loss Function) ساده تعریف می‌کنیم که مقدار میانگین فعال‌سازی‌های آن لایه را محاسبه کرده و سعی می‌کند آن را افزایش دهد.

3. سپس ورودی خود (یعنی تصویر) را تغییر می‌دهیم؛ به این صورت که گرادیان تابع هزینه را نسبت به تصویر محاسبه کرده و آن را روی تصویر اعمال می‌کنیم. این کار باعث می‌شود تصویر به سمتی تغییر کند که تابع هزینه (و در نتیجه فعال‌سازی‌ها) بیشینه شود.

4. در نهایت، برای کار با تصاویر بزرگ و بهینه‌سازی مصرف حافظه  و همچنین دستیابی به نتایج بهتر، از تکنیک‌هایی مانند تقسیم تصویر به کاشی‌ها (Tiling) و چند مقیاسی یا اکتاوها (Octaves) استفاده می‌شود.

بیایید نشان دهیم که چگونه می‌توان یک **Neural Network** را وادار کرد تا "Dream" ببیند و الگوهای فراواقعی‌ای را که در یک تصویر مشاهده می‌کند تقویت کند.

```python
import tensorflow as tf
import numpy as np

import matplotlib as mpl

import IPython.display as display
import PIL.Image
```

## یک تصویر برای Dream-ify انتخاب کنید

برای این آموزش، بیایید از یک تصویر Labrador استفاده کنیم

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/patterneffort/deepdream/images/D1.png" alt="IPS1" style="object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px; rgba(52, 51, 51, 1)">
yellow labrador
</div>


```python
# Download an image and read it into a NumPy array.
def download(url, max_dim=None):
  name = url.split('/')[-1]
  image_path = tf.keras.utils.get_file(name, origin=url)
  img = PIL.Image.open(image_path)
  if max_dim:
    img.thumbnail((max_dim, max_dim))
  return np.array(img)

# Normalize an image
def deprocess(img):
  img = 255*(img + 1.0)/2.0
  return tf.cast(img, tf.uint8)

# Display an image
def show(img):
  display.display(PIL.Image.fromarray(np.array(img)))


# Downsizing the image makes it easier to work with.
original_img = download(url, max_dim=500)
show(original_img)
display.display(display.HTML('Image cc-by: <a "href=https://commons.wikimedia.org/wiki/File:Felis_catus-cat_on_snow.jpg">Von.grzanka</a>'))
```

## آماده‌سازی مدل استخراج ویژگی‌ها



یک مدل **Image Classification** از پیش آموزش‌دیده دانلود و آماده کنید. شما از <a href="https://keras.io/api/applications/inceptionv3/" style="display:inline-block ;text-decoration:underline; color:rgba(15, 134, 218, 1);" target="_blank">
InceptionV3
</a>
 استفاده خواهید کرد که مشابه مدلی است که در اصل در **DeepDream** به‌کار رفته بود.

توجه داشته باشید که هر <a href="https://keras.io/api/applications/#available-models" style="display:inline-block ;text-decoration:underline; color:rgba(15, 134, 218, 1);" target="_blank">
مدل از پیش آموزش‌دیده
</a> دیگری نیز قابل استفاده است، اگرچه در این صورت باید نام لایه‌ها را در ادامه مطابق تغییرات جدید تنظیم کنید.

base_model = tf.keras.applications.InceptionV3(include_top=False, weights='imagenet')

ایده‌ی **DeepDream** این است که یک لایه (یا چند لایه) انتخاب شود و **"Loss"** به‌گونه‌ای به حداکثر برسد که تصویر به‌طور فزاینده‌ای لایه‌ها را "تحریک" کند. پیچیدگی ویژگی‌هایی که در تصویر ایجاد می‌شوند بستگی به لایه‌های انتخاب‌شده توسط شما دارد؛ به‌عبارت دیگر، لایه‌های پایین‌تر **Strokeها** یا الگوهای ساده تولید می‌کنند، در حالی که لایه‌های عمیق‌تر ویژگی‌های پیچیده‌تری در تصاویر ایجاد می‌کنند یا حتی اشیای کامل را نمایان می‌سازند.

معماری **InceptionV3** نسبتاً بزرگ است (برای مشاهده‌ی نمودار معماری مدل به مخزن تحقیقاتی **TensorFlow** مراجعه کنید: <a href="https://github.com/tensorflow/models/tree/master/research/slim" style="display:inline-block ;text-decoration:underline; color:rgba(15, 134, 218, 1);" target="_blank">
research repo
</a>).

برای **DeepDream**، لایه‌های مورد علاقه آن‌هایی هستند که در آن‌ها **Convolutions** با هم **Concatenate** شده‌اند. در **InceptionV3** یازده لایه از این نوع وجود دارد که با نام‌های `'mixed0'` تا `'mixed10'` شناخته می‌شوند. استفاده از لایه‌های مختلف منجر به تولید تصاویر رؤیایی متفاوت خواهد شد.

لایه‌های عمیق‌تر به ویژگی‌های سطح بالاتر (مانند چشم‌ها و چهره‌ها) پاسخ می‌دهند، در حالی که لایه‌های ابتدایی به ویژگی‌های ساده‌تر (مانند لبه‌ها، اشکال و بافت‌ها) واکنش نشان می‌دهند.

می‌توانید با لایه‌های انتخاب‌شده در ادامه آزمایش کنید، اما به یاد داشته باشید که لایه‌های عمیق‌تر (آن‌هایی که **Index** بالاتری دارند) زمان بیشتری برای آموزش می‌گیرند، زیرا محاسبه‌ی گرادیان در آن‌ها عمیق‌تر است.

```python
# Maximize the activations of these layers
names = ['mixed3', 'mixed5']
layers = [base_model.get_layer(name).output for name in names]

# Create the feature extraction model
dream_model = tf.keras.Model(inputs=base_model.input, outputs=layers)
```

## محاسبه‌ی Loss

**Loss** مجموع **Activations** در لایه‌های انتخاب‌شده است. **Loss** در هر لایه نرمال‌سازی می‌شود تا سهم لایه‌های بزرگ‌تر بر لایه‌های کوچک‌تر غالب نشود.

معمولاً **Loss** مقداری است که می‌خواهید از طریق **Gradient Descent** آن را کمینه کنید. در **DeepDream**، شما این **Loss** را از طریق **Gradient Ascent** به حداکثر می‌رسانید.

```python
def calc_loss(img, model):
  # Pass forward the image through the model to retrieve the activations.
  # Converts the image into a batch of size 1.
  img_batch = tf.expand_dims(img, axis=0)
  layer_activations = model(img_batch)
  if len(layer_activations) == 1:
    layer_activations = [layer_activations]

  losses = []
  for act in layer_activations:
    loss = tf.math.reduce_mean(act)
    losses.append(loss)

  return  tf.reduce_sum(losses)
  ```
  
## صعود گرادیان

وقتی **Loss** برای لایه‌های انتخاب‌شده محاسبه شد، تنها کاری که باقی می‌ماند، محاسبه‌ی **Gradients** نسبت به تصویر و افزودن آن‌ها به تصویر اصلی است.

افزودن گرادیان‌ها به تصویر، الگوهایی را که شبکه مشاهده می‌کند تقویت می‌کند. در هر مرحله، تصویری ایجاد می‌کنید که به‌طور فزاینده‌ای **Activations** لایه‌های خاصی در شبکه را تحریک می‌کند.

متدی که این کار را انجام می‌دهد، در ادامه داخل یک `tf.function` برای بهبود عملکرد قرار گرفته است. این متد از یک `input_signature` استفاده می‌کند تا اطمینان حاصل شود که تابع برای اندازه‌های مختلف تصویر یا مقادیر `steps`/`step_size` دوباره ردیابی (**retrace**) نمی‌شود. برای جزئیات بیشتر به <a href="https://www.tensorflow.org/guide/function?_gl=1*zg0fad*_up*MQ..*_ga*ODgxNTAwNzQ5LjE3NjA5ODUxMjc.*_ga_W0YLR4190T*czE3NjA5ODUxMjYkbzEkZzAkdDE3NjA5ODUxMjYkajYwJGwwJGgw" style="display:inline ;text-decoration:underline; color:rgba(15, 134, 218, 1);" target="_blank">
Concrete functions guide
</a> مراجعه کنید.



```python
class DeepDream(tf.Module):
  def __init__(self, model):
    self.model = model

  @tf.function(
      input_signature=(
        tf.TensorSpec(shape=[None,None,3], dtype=tf.float32),
        tf.TensorSpec(shape=[], dtype=tf.int32),
        tf.TensorSpec(shape=[], dtype=tf.float32),)
  )
  def __call__(self, img, steps, step_size):
      print("Tracing")
      loss = tf.constant(0.0)
      for n in tf.range(steps):
        with tf.GradientTape() as tape:
          # This needs gradients relative to `img`
          # `GradientTape` only watches `tf.Variable`s by default
          tape.watch(img)
          loss = calc_loss(img, self.model)

        # Calculate the gradient of the loss with respect to the pixels of the input image.
        gradients = tape.gradient(loss, img)

        # Normalize the gradients.
        gradients /= tf.math.reduce_std(gradients) + 1e-8 
        
        # In gradient ascent, the "loss" is maximized so that the input image increasingly "excites" the layers.
        # You can update the image by directly adding the gradients (because they're the same shape!)
        img = img + gradients*step_size
        img = tf.clip_by_value(img, -1, 1)

      return loss, img
deepdream = DeepDream(dream_model)
## Main Loop
def run_deep_dream_simple(img, steps=100, step_size=0.01):
  # Convert from uint8 to the range expected by the model.
  img = tf.keras.applications.inception_v3.preprocess_input(img)
  img = tf.convert_to_tensor(img)
  step_size = tf.convert_to_tensor(step_size)
  steps_remaining = steps
  step = 0
  while steps_remaining:
    if steps_remaining>100:
      run_steps = tf.constant(100)
    else:
      run_steps = tf.constant(steps_remaining)
    steps_remaining -= run_steps
    step += run_steps

    loss, img = deepdream(img, run_steps, tf.constant(step_size))
    
    display.clear_output(wait=True)
    show(deprocess(img))
    print ("Step {}, loss {}".format(step, loss))


  result = deprocess(img)
  display.clear_output(wait=True)
  show(result)

  return result
dream_img = run_deep_dream_simple(img=original_img, 
                                  steps=100, step_size=0.01)

```
<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/patterneffort/deepdream/images/D2.png" alt="IPS1" style="object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;color: rgba(52, 51, 51, 1)">
</div>

## افزایش مقیاس (Taking it up an octave)

نتیجه‌ی اولیه نسبتاً خوب است، اما چند مشکل در این تلاش اول وجود دارد:

1. خروجی نویزی است (این مشکل می‌تواند با استفاده از **`tf.image.total_variation` loss** حل شود).
2. تصویر وضوح پایینی دارد.
3. الگوها به نظر می‌رسد همه در یک **Granularity** مشابه رخ می‌دهند.

یک رویکرد که همه‌ی این مشکلات را برطرف می‌کند، اعمال **Gradient Ascent** در مقیاس‌های مختلف است. این کار اجازه می‌دهد الگوهای تولیدشده در مقیاس‌های کوچک‌تر در الگوهای مقیاس‌های بالاتر ترکیب شوند و با جزئیات بیشتری پر شوند.

برای انجام این کار، می‌توانید روش **Gradient Ascent** قبلی را انجام دهید، سپس اندازه‌ی تصویر را افزایش دهید (که به آن **Octave** گفته می‌شود) و این فرایند را برای چند **Octave** تکرار کنید.

```python
import time
start = time.time()

OCTAVE_SCALE = 1.30

img = tf.constant(np.array(original_img))
base_shape = tf.shape(img)[:-1]
float_base_shape = tf.cast(base_shape, tf.float32)

for n in range(-2, 3):
  new_shape = tf.cast(float_base_shape*(OCTAVE_SCALE**n), tf.int32)

  img = tf.image.resize(img, new_shape).numpy()

  img = run_deep_dream_simple(img=img, steps=50, step_size=0.01)

display.clear_output(wait=True)
img = tf.image.resize(img, base_shape)
img = tf.image.convert_image_dtype(img/255.0, dtype=tf.uint8)
show(img)

end = time.time()
end-start
```

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/patterneffort/deepdream/images/D3.png" alt="IPS1" style="object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;color: rgba(52, 51, 51, 1)">
</div>

## اختیاری: افزایش مقیاس با استفاده از **Tiles**

یکی از مواردی که باید در نظر گرفته شود این است که با افزایش اندازه‌ی تصویر، زمان و حافظه لازم برای محاسبه‌ی گرادیان نیز افزایش می‌یابد. پیاده‌سازی **Octave** بالا روی تصاویر بسیار بزرگ یا تعداد زیادی **Octave** کار نخواهد کرد.

برای جلوگیری از این مشکل، می‌توانید تصویر را به **Tiles** تقسیم کرده و گرادیان را برای هر **Tile** محاسبه کنید.

اعمال جابجایی تصادفی (**Random Shifts**) به تصویر قبل از هر محاسبه‌ی **Tiled** مانع از ایجاد درز بین **Tiles** می‌شود.

با پیاده‌سازی جابجایی تصادفی شروع کنید:

```python
def random_roll(img, maxroll):
  # Randomly shift the image to avoid tiled boundaries.
  shift = tf.random.uniform(shape=[2], minval=-maxroll, maxval=maxroll, dtype=tf.int32)
  img_rolled = tf.roll(img, shift=shift, axis=[0,1])
  return shift, img_rolled
shift, img_rolled = random_roll(np.array(original_img), 512)
show(img_rolled)
```
<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/patterneffort/deepdream/images/D4.png" alt="IPS1" style="object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;color: rgba(52, 51, 51, 1)">
</div>

در اینجا نسخه‌ی **Tiled** معادل تابع `deepdream` که قبلاً تعریف شده بود، آورده شده است:

```python
class TiledGradients(tf.Module):
  def __init__(self, model):
    self.model = model

  @tf.function(
      input_signature=(
        tf.TensorSpec(shape=[None,None,3], dtype=tf.float32),
        tf.TensorSpec(shape=[2], dtype=tf.int32),
        tf.TensorSpec(shape=[], dtype=tf.int32),)
  )
  def __call__(self, img, img_size, tile_size=512):
    shift, img_rolled = random_roll(img, tile_size)

    # Initialize the image gradients to zero.
    gradients = tf.zeros_like(img_rolled)
    
    # Skip the last tile, unless there's only one tile.
    xs = tf.range(0, img_size[1], tile_size)[:-1]
    if not tf.cast(len(xs), bool):
      xs = tf.constant([0])
    ys = tf.range(0, img_size[0], tile_size)[:-1]
    if not tf.cast(len(ys), bool):
      ys = tf.constant([0])

    for x in xs:
      for y in ys:
        # Calculate the gradients for this tile.
        with tf.GradientTape() as tape:
          # This needs gradients relative to `img_rolled`.
          # `GradientTape` only watches `tf.Variable`s by default.
          tape.watch(img_rolled)

          # Extract a tile out of the image.
          img_tile = img_rolled[y:y+tile_size, x:x+tile_size]
          loss = calc_loss(img_tile, self.model)

        # Update the image gradients for this tile.
        gradients = gradients + tape.gradient(loss, img_rolled)

    # Undo the random shift applied to the image and its gradients.
    gradients = tf.roll(gradients, shift=-shift, axis=[0,1])

    # Normalize the gradients.
    gradients /= tf.math.reduce_std(gradients) + 1e-8 

    return gradients 
get_tiled_gradients = TiledGradients(dream_model)
با کنار هم قرار دادن این بخش‌ها، یک پیاده‌سازی **DeepDream** مقیاس‌پذیر و **Octave-aware** به‌دست می‌آید:
def run_deep_dream_with_octaves(img, steps_per_octave=100, step_size=0.01, 
                                octaves=range(-2,3), octave_scale=1.3):
  base_shape = tf.shape(img)
  img = tf.keras.utils.img_to_array(img)
  img = tf.keras.applications.inception_v3.preprocess_input(img)

  initial_shape = img.shape[:-1]
  img = tf.image.resize(img, initial_shape)
  for octave in octaves:
    # Scale the image based on the octave
    new_size = tf.cast(tf.convert_to_tensor(base_shape[:-1]), tf.float32)*(octave_scale**octave)
    new_size = tf.cast(new_size, tf.int32)
    img = tf.image.resize(img, new_size)

    for step in range(steps_per_octave):
      gradients = get_tiled_gradients(img, new_size)
      img = img + gradients*step_size
      img = tf.clip_by_value(img, -1, 1)

      if step % 10 == 0:
        display.clear_output(wait=True)
        show(deprocess(img))
        print ("Octave {}, Step {}".format(octave, step))
    
  result = deprocess(img)
  return result
img = run_deep_dream_with_octaves(img=original_img, step_size=0.01)

display.clear_output(wait=True)
img = tf.image.resize(img, base_shape)
img = tf.image.convert_image_dtype(img/255.0, dtype=tf.uint8)
show(img)
```
<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/patterneffort/deepdream/images/D5.png" alt="IPS1" style="object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;color: rgba(52, 51, 51, 1)">
</div>

خیلی بهتر شد! با تغییر تعداد **Octaveها**، **Octave Scale** و لایه‌های فعال‌شده، می‌توانید ظاهر تصویر **DeepDream** خود را تغییر دهید.

خوانندگان ممکن است به <a href="https://github.com/tensorflow/lucid" style="display:inline-block ;text-decoration:underline; color:rgba(15, 134, 218, 1);" target="_blank">
TensorFlow Lucid
</a> نیز علاقه‌مند باشند، که ایده‌های معرفی‌شده در این آموزش را گسترش می‌دهد تا شبکه‌های عصبی را تجسم و تفسیر کنند.

---

تا الان این آزمایش روی لایه های سطح بالا در  مدل انتخابی انجام شد , همچنین اگر از لایه های سطح پایین در این مدل انتخاب کنیم , خروجی اینگونه تغییر میکند :

کافی است در قسمت تایین نام لایه ها این کد را جایگزین کنیم:

```python
# Maximize the activations of these layers
names = ['mixed7', 'mixed8']
layers = [base_model.get_layer(name).output for name in names]

# Create the feature extraction model
dream_model = tf.keras.Model(inputs=base_model.input, outputs=layers)
```
و میبینیم که در خروجی , ویژگی های سطح پایین مثل خطوط تقویت شده اند :

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/patterneffort/deepdream/images/D6.png" alt="IPS1" style="object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;color: rgba(52, 51, 51, 1)">
</div>

---

## کاربردها و موارد استفاده خلاقانه

### 1. تغییر هنری تصاویر

استفاده از **رویای عمیق (Deep Dream)** برای تبدیل عکس‌های معمولی به شاهکارهای خلاقانه، به‌عنوان یک گام بزرگ در هنر دیجیتال و خلق محتوای بصری در نظر گرفته شده است. رویای عمیق فرآیندی دگرگون‌کننده را ترویج می‌کند که فراتر از مهارت‌های هنری سنتی است و منجر به ترکیب‌هایی چشم‌نواز و خلاقانه می‌شود.

### 2. بهبود تصویربرداری پزشکی

دیپ دریم می‌تواند به بهبود دقت و ظرفیت‌های تحلیلی در تصویربرداری پزشکی کمک کند. استفاده از تکنیک‌های رویای عمیق در تصویربرداری پزشکی باعث بهبود وضوح ویژگی‌ها و تغییرات حیاتی می‌شود و امکان تشخیص دقیق‌تر و جزئی‌تر را فراهم می‌آورد.

### 3. واقعیت افزوده و بازی‌های رایانه‌ای

رویای عمیق یک بازیگر تأثیرگذار در حوزه **واقعیت افزوده و بازی‌های رایانه‌ای** است که با ایجاد محیط‌های چشمگیر و جذاب، تجربه کاربران را بهبود می‌بخشد. چشم‌انداز بصری بازی‌ها و واقعیت افزوده با واقع‌گرایی بیشتر و جزئیات دقیق‌تر، باعث افزایش درگیری ذهنی کاربران و ایجاد تجربه‌های نوآورانه می‌شود.

### 4. پژوهش‌های علمی

رویای عمیق می‌تواند بخش‌هایی از **ادراک بصری انسان و توهمات** را شبیه‌سازی کند که آن را برای پژوهشگرانی که این پدیده‌ها را مطالعه می‌کنند، مفید می‌سازد. همچنین در تحلیل تصاویر زیستی (مانند تصاویر میکروسکوپی)، می‌توان از آن برای برجسته‌سازی ساختارها یا الگوهای خاص جهت تحقیق و تحلیل استفاده کرد.


<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Deep_Dreamscope_%2819822170718%29.jpg/500px-Deep_Dreamscope_%2819822170718%29.jpg">

## توسعه‌های آینده و مسیرهای پژوهشی

پیشرفت‌های آینده رویای عمیق نویدبخش تحول‌های عمده در راهبردهای الگوریتمی برای ایجاد تصاویر دقیق‌تر و متنوع‌تر است. این شامل **توانایی پردازش در زمان واقعی، یکپارچگی چندوجهی و ابزارهای کاربرپسند** برای افزایش دسترسی می‌شود.  

در کنار این، ملاحظات اخلاقی همچون **استانداردهای استفاده مسئولانه و جلوگیری از سوگیری‌ها** اهمیت بالایی پیدا می‌کنند؛ به‌ویژه در زمانی که کاربردهای رویای عمیق در زمینه‌های علمی، خلاقانه، تجاری و درمانی گسترش یابند.  

دیپ دریم همچنین یک ابزار آموزشی است که با ارائه تجربه‌های تعاملی، به درک بهتر شبکه‌های عصبی و اصول هوش مصنوعی کمک می‌کند. این پیشرفت‌ها نشان‌دهنده توانایی رویای عمیق در **نوآوری، الهام‌بخشی و توجه به دغدغه‌های اخلاقی و اجتماعی** در حوزه‌های گوناگون است.


### چرا DeepDream این‌قدر جذاب شد:

از منظر علمی، DeepDream ابزار بصری خوبی بود تا پژوهشگران و مهندسین بفهمند چه «ویژگی‌ها» در لایه‌های مختلف شبکه کدگذاری شده‌اند؛ این به شناسایی سوگیری‌ها، خطاها یا نقاط ضعف آموزش کمک می‌کند. 

از منظر فرهنگی و هنری، خروجی‌های آن به‌سرعت در شبکه‌های اجتماعی و گالری‌ها پخش شد و هنرمندان دیجیتال شروع به استفاده و توسعهٔ این تکنیک کردند؛ این باعثِ تقابل جالب میان علومِ کامپیوتر و هنر شد و بحث‌هایی دربارهٔ «خلاقیت» در ماشین‌ها برانگیخت. نمونه‌هایی از آثار ویدئویی و پروژه‌های هنری مبتنی بر DeepDream نیز رسانه‌ها را جذب کردند.

### تکاملِ فنی پس از انتشار اولیه:
پس از انتشار، پژوهشگران و مهندسان تکنیک‌های مرتبط (مثل guided-backpropagation، regularizationهای مختلف، multi-scale processing یا «octaves») را ترکیب کردند تا کنترل بهتری روی الگوها و نویز داشته باشند و خروجی‌های معنادارتری تولید کنند؛ همین تلاش‌ها بعدها در کارهای گسترده‌تری در حوزهٔ feature visualization و interpretability ادغام شد. منابع آموزشی مثل مقالهٔ تفصیلیِ Distill توسط Chris Olah نیز این مفاهیم را جمع‌بندی و توسعه دادند.

---

# منابع



<ul>
  <li>
    <a href="https://research.google/blog/inceptionism-going-deeper-into-neural-networks/" style="text-decoration:underline; color:green;" target="_blank">
        Inceptionism: Going Deeper into Neural Networks
    </a>
  </li>

  <li>
    <a href="https://www.youtube.com/watch?v=BsSmBPmPeYQ" style="text-decoration:underline; color:green;" target="_blank">
        Deep Dream (Google) - Computerphile
    </a>
  </li>

  <li>
    <a href="https://www.wired.com/beyond-the-beyond/2016/09/showtime-gene-kogan-deepdream-densecap/" style="text-decoration:underline; color:green;" target="_blank">
        https://www.wired.com/beyond-the-beyond/2016/09
    </a>
  </li>

  <li>
    <a href="https://distill.pub/2017/feature-visualization/" style="text-decoration:underline; color:green;" target="_blank">
        https://distill.pub/2017/feature-visualization
    </a>
  </li>

  <li>
    <a href="https://www.tensorflow.org/tutorials/generative/deepdream" style="text-decoration:underline; color:green;" target="_blank">
        https://www.tensorflow.org/tutorials/generative/deepdream
    </a>
  </li>

   <li>
    <a href="https://en.wikipedia.org/wiki/DeepDream" style="text-decoration:underline; color:green;" target="_blank">
        https://en.wikipedia.org/wiki/DeepDream
    </a>
  </li>

   <li>
    <a href="https://www.geeksforgeeks.org/computer-vision/deep-dream-an-in-depth-exploration/" style="text-decoration:underline; color:green;" target="_blank">
        https://www.geeksforgeeks.org/computer-vision/deep-dream-an-in-depth-exploration/
    </a>
  </li>
</ul>

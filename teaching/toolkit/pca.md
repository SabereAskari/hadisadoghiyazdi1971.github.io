---
layout: persian  # یا single با کلاس rtl-layout
classes: wide rtl-layout
dir: rtl
title: "فیلتر کالمن"
permalink: /teaching/toolkit/pca/
author_profile: false
sidebar:
  nav: "toolkit"
header:
  overlay_image: "/assets/images/background.jpg"
  overlay_filter: 0.3
  overlay_color: "#5e616c"
  caption: "Photo credit: [**Unsplash**](https://unsplash.com)"
---

#  تحلیل مؤلفه‌های اصلی (PCA)

این متن از این ادرس و مراجع دیگر  استفاده شده است 

<a href="https://patternrmachinel.github.io/PatternLearning/StudentEffort/miniprojecct_PCA/finallPCA.html" style="text-decoration:none; color:inherit;" target="_blank">
      <strong>Principle Component Analysis</strong>
    </a> 

در پردازش سیگنال در موارد زیادی سیگنالهایی با تعداد ویژگی زیاد مواجه هستیم. همچون 

ابعاد بالا دارای ویژگی‌های زیادی هستند مانند سیگنال‌های EEG از مغز یا رسانه‌های اجتماعی و غیره.
تصاویر نیز امروزه یک داده با ویژگی زیاد و بسیار مورد استفاده در سیستمهای یادگیر است و پردازش متن که یکی از جاذبه های هوش مصنوعی است یکی دیگر از نمونه های ویژگی زیاد می توان نام برد

## برخی از مزایای کاهش ابعاد
1. مصورسازی
2. کمک به جلوگیری از بیش‌برازش
3. استفاده کارآمدتر از منابع
4. پردازش ساده تر 
5. کاهش اثر نویز و بررسی مولفه های اصلی 

در تصویر زیر راستای با کشیدگی بیشتر را مولفه اصلی و راستای با کشیدگی کمتر را ناشی از نویز تلقی می کنیم این موضوع اساس کار روش مولفه های اصلی است که با نام pca معروف است

  <figure style="flex:0 0 200px; margin:0; text-align:center;">
    <img src="/assets/Toolkitimages/pca/dim_red_var.JPG" alt="pca1" width="200" style="max-width:100%; height:auto; display:block;" />
    <figcaption><em>Low-High variance</em></figcaption>
  </figure>


## تکنیک‌های کاهش ابعاد

### ۱. انتخاب ویژگی (Feature Selection)
انتخاب زیرمجموعه‌ای از مجموعه ویژگی‌های داده شده.


ورودی: فضای ویژگی اصلی با بعد `d`

$$
\mathcal{F} = \{f_1, f_2, \dots, f_d\}
$$

خروجی: زیرمجموعه‌ای با `k` ویژگی (که `k << d`)

$$
\mathcal{F}_{selected} = \{f_{i_1}, f_{i_2}, \dots, f_{i_k}\} \subset \mathcal{F}
$$

تبدیل داده:

$$
\mathbf{X}_{selected} = \mathbf{X} \cdot \text{diag}(\mathbf{m}) \in \mathbb{R}^{n \times k}
$$

که در آن:
- `X ∈ ℝ^(n×d)` ماتریس داده اصلی
- `m` بردار دودویی انتخاب ویژگی
- `X_selected ∈ ℝ^(n×k)` داده کاهش‌بعدیافته



### ۲. استخراج ویژگی (Feature Extraction)
یک تبدیل خطی یا غیرخطی از فضای ویژگی اصلی به فضای ابعاد پایین‌تر.

تبدیل کلی:

$$
\phi: \mathbb{R}^d \to \mathbb{R}^k
$$

#### الف) استخراج خطی

$$
\mathbf{Z} = \mathbf{X} \mathbf{W}
$$

که در آن:
- `W ∈ ℝ^(d×k)` ماتریس تبدیل
- `Z ∈ ℝ^(n×k)` داده در فضای جدید

#### ب) استخراج غیرخطی

$$
\mathbf{z}_i = \phi(\mathbf{x}_i), \quad \forall i \in \{1, \dots, n\}
$$

**مثال‌ها:**
- *PCA* (خطی)
- *Autoencoder* (غیرخطی)
- *Kernel PCA* (غیرخطی)








## هدف کاهش ابعاد
حداکثر نگهداری اطلاعات مهم در حین کاهش ابعاد.

اطلاعات مهم چیست؟

اطلاعات: واریانس داده‌های تصویر شده

![اجتماعی](./img/dim_red_var.jpg)

اطلاعات: حفظ همسایگی هندسی محلی

![اجتماعی](./img/local_relation.png)

اطلاعات: حفظ هر دو همسایگی هندسی محلی و سراسری

![اجتماعی](./img/global_relation.png)

## ایده:
با توجه به نقاط داده در یک فضای d-بعدی، آن‌ها را در یک فضای با ابعاد پایین‌تر تصویر کنید در حالی که تا حد امکان اطلاعات حفظ شود:

- بهترین تقریب صفحه‌ای از داده‌های 3 بعدی را پیدا کنید.
- بهترین تقریب 12 بعدی از داده‌های 104 بعدی را پیدا کنید.
- به طور خاص، تصویری را انتخاب کنید که خطای مربع در بازسازی داده‌های اصلی را به حداقل برساند.

### کد: مجموعه داده گوسی 2 بعدی
این کد پایتون داده‌های 2 بعدی را از یک توزیع نرمال چندمتغیره با میانگین و ماتریس کوواریانس زیر تولید و مصورسازی می‌کند:

**بردار میانگین**:
$$
\mu = \begin{bmatrix} 0 \\ 0 \end{bmatrix}
$$

**ماتریس کوواریانس**:
$$
\Sigma = \begin{bmatrix} 1 & 0.8 \\ 0.8 & 1 \end{bmatrix}
$$

این کد یک نمودار پراکندگی از 1000 نمونه ایجاد می‌کند که همبستگی بین دو متغیر را نشان می‌دهد، با نسبت ابعاد برابر و شبکه برای وضوح بیشتر.

```python
import numpy as np
import matplotlib.pyplot as plt

# تعریف بردار میانگین و ماتریس کوواریانس
mean = [0, 0]  # مثال: داده 2 بعدی با میانگین صفر
cov = [[1, 0.8], [0.8, 1]]  # ماتریس کوواریانس (2x2)

# تعداد نمونه‌ها
n_samples = 1000

# تولید داده
data = np.random.multivariate_normal(mean, cov, size=n_samples)

plt.scatter(data[:,0], data[:,1])
plt.xlabel("محور X")
plt.ylabel("محور Y")
plt.title("داده‌های پراکنده")
plt.gca().set_aspect("equal")  # نسبت ابعاد برابر
plt.legend()
plt.grid(True)
plt.show()
```

### کد: اولین محور PCA
این کد پایتون ماتریس کوواریانس داده‌های تولید شده را محاسبه می‌کند، تجزیه ویژه را انجام می‌دهد و اولین محور اصلی (بردار ویژه با بزرگترین مقدار ویژه) را مصورسازی می‌کند. نمودار نقاط داده را به همراه اولین محور اصلی نشان می‌دهد که با یک پیکان قرمز نشان داده شده است و جهت بیشینه واریانس در داده‌ها را نشان می‌دهد. محور برای مصورسازی بهتر مقیاس‌دهی شده است و نمودار شامل خطوط شبکه، برچسب‌های محور و یک راهنما است.

```python
# محاسبه ماتریس کوواریانس داده‌های تولید شده
data_cov = np.cov(data, rowvar=False)

# انجام تجزیه ویژه
eigenvalues, eigenvectors = np.linalg.eigh(data_cov)

# یافتن اولین محور اصلی (بردار ویژه با بزرگترین مقدار ویژه)
first_principal_axis = eigenvectors[:, np.argmax(eigenvalues)]

# مقیاس‌دهی محور برای مصورسازی
scaling_factor = 2  # فاکتور مقیاس دلخواه برای مصورسازی بهتر
axis_line = first_principal_axis * scaling_factor

# رسم داده‌ها
plt.figure(figsize=(6, 6))
plt.scatter(data[:, 0], data[:, 1], alpha=0.5, s=10, label="داده")
plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
plt.axvline(0, color="gray", linestyle="--", linewidth=0.8)

# افزودن اولین محور اصلی
plt.quiver(
    mean[0], mean[1], 
    axis_line[0], axis_line[1],
    angles="xy", scale_units="xy", scale=1, color="red", label="اولین محور اصلی"
)

# افزودن برچسب‌ها و عنوان
plt.xlabel("محور X")
plt.ylabel("محور Y")
plt.title("نمودار پراکنده با اولین محور اصلی")
plt.gca().set_aspect("equal")  # نسبت ابعاد برابر
plt.legend()
plt.grid(True)
plt.show()
```

### کد: محور اول و دوم
این کد پایتون ماتریس کوواریانس داده‌های تولید شده را محاسبه می‌کند و تجزیه ویژه را برای استخراج دو مؤلفه اصلی اول انجام می‌دهد. مؤلفه‌های اصلی برای مصورسازی بهتر مقیاس‌دهی شده و در کنار داده‌ها رسم می‌شوند. مؤلفه اصلی اول (بزرگترین مقدار ویژه) به رنگ قرمز و مؤلفه اصلی دوم (کوچکترین مقدار ویژه) به رنگ آبی نشان داده می‌شود. نمودار شامل خطوط شبکه، برچسب‌های محور و یک راهنما است، با نسبت ابعاد برابر تا جهت‌گیری مؤلفه‌های اصلی در رابطه با داده‌ها به وضوح مصورسازی شود.

```python
# محاسبه ماتریس کوواریانس داده‌های تولید شده
data_cov = np.cov(data, rowvar=False)

# انجام تجزیه ویژه
eigenvalues, eigenvectors = np.linalg.eigh(data_cov)

# مقیاس‌دهی مؤلفه‌های اصلی برای مصورسازی
scaling_factor = 2  # فاکتور مقیاس دلخواه برای مصورسازی بهتر
pc1 = eigenvectors[:, 1] * eigenvalues[1] * scaling_factor  # اولین مؤلفه اصلی (بزرگترین مقدار ویژه)
pc2 = eigenvectors[:, 0] * eigenvalues[0] * scaling_factor  # دومین مؤلفه اصلی (کوچکترین مقدار ویژه)

# رسم داده‌ها
plt.figure(figsize=(6, 6))
plt.scatter(data[:, 0], data[:, 1], alpha=0.5, s=10, label="داده")
plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
plt.axvline(0, color="gray", linestyle="--", linewidth=0.8)

# افزودن محورهای اصلی اول و دوم
plt.quiver(mean[0], mean[1], pc1[0], pc1[1], angles="xy", scale_units="xy", scale=1, color="red", label="اولین مؤلفه اصلی")
plt.quiver(mean[0], mean[1], pc2[0], pc2[1], angles="xy", scale_units="xy", scale=1, color="blue", label="دومین مؤلفه اصلی")

# افزودن برچسب‌ها و عنوان
plt.xlabel("محور X")
plt.ylabel("محور Y")
plt.title("نمودار پراکنده با مؤلفه‌های اصلی اول و دوم")
plt.gca().set_aspect("equal")  # نسبت ابعاد برابر
plt.legend()
plt.grid(True)
plt.show()
```

جهت تصادفی در مقابل مؤلفه اصلی:

 ![داده‌های PCA](./img/pcaVSrandom.JPG)

## تعریف

1. هدف: کاهش ابعاد داده‌ها در حین حفظ جنبه‌های مهم داده.

   فرض کنید $ \mathbf{X} $:

  $$
  \mathbf{X} =
  \begin{pmatrix}
      \mathbf{X}_1^\top \\
      \vdots \\
      \mathbf{X}_N^\top
  \end{pmatrix}_{N \times d}
  =
  \begin{pmatrix}
      x_{11} & x_{12} & \cdots & x_{1d} \\
      x_{21} & x_{22} & \cdots & x_{2d} \\
      \vdots & \vdots & \ddots & \vdots \\
      x_{N1} & x_{N2} & \cdots & x_{Nd}
  \end{pmatrix}
  $$

- $ \mathbf{X}_{N \times d} \xrightarrow{\text{PCA}} \tilde{\mathbf{X}}_{N \times k} \quad \text{با} \quad k \leq d $

- **فرض**: داده‌ها میانگین-مرکزی شده‌اند، یعنی:
  
  $$
  \mu_x = \frac{1}{N} \sum_{i=1}^N \mathbf{X}_i = \mathbf{0}_{d \times 1}
  $$

## تفسیرها
تصویر متعامد داده‌ها بر روی یک زیرفضای خطی با ابعاد پایین‌تر که:
تفسیر ۱. واریانس داده‌های تصویر شده را بیشینه می‌کند.
تفسیر ۲. مجموع مربعات فواصل تا زیرفضا را کمینه می‌کند.

![داده‌های PCA](./img/pca.png)

### معادل بودن تفسیرها
کمینه کردن مجموع مربعات فواصل تا زیرفضا معادل است با
بیشینه کردن مجموع مربعات تصاویر بر روی آن زیرفضا

![داده‌های PCA](./img/var_vs_rec.JPG)

یک مجموعه از بردارهای متعامد واحد $ \mathbf{v} =  \mathbf{v}_1, \mathbf{v}_2, \dots, \mathbf{v}_k $ (که هر $ \mathbf{v}_i $ به اندازه $ d \times 1 $ است) که توسط PCA تولید می‌شوند و هر دو تفسیر را انجام می‌دهند.

#### بیشینه کردن واریانس داده‌های تصویر شده

تصویر نقاط داده بر روی $\mathbf{v}_1$:

$$\Pi = \Pi_{\mathbf{v}_1}\{ \mathbf{X}_1, \dots, \mathbf{X}_N \} = \{ \mathbf{v}_1^\top \mathbf{X}_1, \dots, \mathbf{v}_1^\top \mathbf{X}_N \} $$

توجه کنید که: $Var(\mathbf{X}) = \mathbb{E}[\mathbf{X}^2] - \mathbb{E}[\mathbf{X}]^2$ 

$$\mathbb{E}[\mathbf{X}] = 0 \implies Var(\Pi) = \frac{1}{N}  \sum_{i=1}^N (\mathbf{v}_1^\top \mathbf{X}_i)^2 $$

- مرکزی کردن میانگین داده
    - صفر کردن میانگین هر ویژگی
- مقیاس‌دهی برای نرمال کردن هر ویژگی به داشتن واریانس ۱ (یک مرحله دلخواه)
    - ممکن است بر نتایج تأثیر بگذارد
    - زمانی کمک می‌کند که واحدهای اندازه‌گیری ویژگی‌ها متفاوت باشند و برخی ویژگی‌ها بدون نرمال سازی نادیده گرفته شوند.

## پیش‌زمینه
قبل از شروع الگوریتم PCA، باید با موارد زیر آشنا باشیم:
1. مقادیر ویژه و بردارهای ویژه چیستند؟
2. ماتریس کوواریانس نمونه

### مقادیر ویژه و بردارهای ویژه چیستند؟
بردار ویژه: یک بردار غیرصفر که وقتی یک تبدیل خطی اعمال می‌شود فقط در یک ضریب اسکالر ضرب می‌شود.
مقدار ویژه: ضریب اسکالری که بردار ویژه در آن مقیاس می‌شود.
معادله برای یک ماتریس n×n:

$$
Av = \lambda v
$$

جایی که:

A: یک ماتریس مربعی

v: بردار ویژه

$ \lambda $: مقدار ویژه

### تفسیر هندسی
بردارهای ویژه پس از تبدیل در همان جهت (یا مخالف) اشاره می‌کنند.
بردارهای ویژه تحت یک تبدیل جهت خود را تغییر نمی‌دهند.
مقادیر ویژه نشان می‌دهند که بردار چقدر کشیده یا فشرده شده است.
مقادیر ویژه به ما می‌گویند که بردار چقدر مقیاس شده است.

![داده‌های PCA](./img/eigenvetor-eigenvalue-idea.png)

### چگونه مقادیر ویژه و بردارهای ویژه را پیدا کنیم؟
می‌دانیم که
$$
Av = \lambda v
$$
پس
$$
Av - \lambda v=0
$$
$$
(Av - \lambda I) v=0
$$
v نمی‌تواند صفر باشد، بنابراین:
$$
det(Av - \lambda I)=0
$$
برای $\lambda $ حل کنید.
$ \lambda $ را دوباره در معادله $ Av=\lambda v $ جایگزین کنید تا v را پیدا کنید.

#### مثال عددی
فرض کنید 
$
A = \begin{pmatrix}
4 & -5 \\ 
2 & -3 
\end{pmatrix}
$

آنگاه 

$ A-\lambda I= \begin{pmatrix}
4-\lambda & -5 \\ 
2 & -3-\lambda 
\end{pmatrix} 
$

$$
دترمینان (A- \lambda I)= (4-\lambda)(-3-\lambda)+10=(\lambda)^2-\lambda-2=0
$$

$$
\lambda=-1   یا  \lambda=2
$$

$$
برای \lambda_1=-1: 

(A- \lambda_1 I)v_1= \begin{pmatrix} 5 & -5 \\ 2 & -2 \end{pmatrix} \begin{pmatrix} v_{11} \\ v_{12} \end{pmatrix} = \begin{pmatrix} 0 \\0  \end{pmatrix} \implies v_1=\begin{pmatrix} 1 \\1  \end{pmatrix}
$$

$$
برای \lambda_2=2: 

(A- \lambda_2 I)v_2= \begin{pmatrix} 2 & -5 \\ 2 & -5 \end{pmatrix} \begin{pmatrix} v_{21} \\ v_{22} \end{pmatrix} = \begin{pmatrix} 0 \\0  \end{pmatrix} \implies v_2=\begin{pmatrix} 5 \\2  \end{pmatrix}
$$

#### مصورسازی
![داده‌های PCA](./img/matrix_transformations.png)

### کوواریانس چیست؟
کوواریانس معیاری است از این که دو ویژگی تصادفی چقدر با هم تغییر می‌کنند.
    $$Cov(X,Y) = E[(X −E[X])(Y −E[Y])] = E[(Y −E[Y])(X −E[X])] = Cov(Y,X)$$
 بنابراین کوواریانس متقارن است.
 مانند قد و وزن افراد.

 #### ماتریس کوواریانس چیست؟
 یک ماتریس کوواریانس مفهوم کوواریانس را به چندین ویژگی تعمیم می‌دهد.
 فرض کنید ماتریس کوواریانس دو ویژگی وجود دارد:
 
$$
\Sigma = \begin{pmatrix}
a & b \\ 
c & d 
\end{pmatrix} =\begin{pmatrix}
a & b \\ 
b & d 
\end{pmatrix}
$$

چرا b=c؟

رابطه بین a,b و d چیست؟

##### مثال ماتریس کوواریانس
$$ \Sigma = \begin{pmatrix}
a & 0 \\ 
0 & a 
\end{pmatrix}
$$

#### کد: مثال
این کد پایتون داده‌های 2 بعدی را از یک توزیع نرمال چندمتغیره با میانگین [0, 0] و ماتریس کوواریانس زیر تولید و مصورسازی می‌کند:

$$
\Sigma = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}
$$

ماتریس کوواریانس نشان‌دهنده متغیرهای مستقل با هیچ همبستگی است. کد یک نمودار پراکندگی از 1000 نمونه ایجاد می‌کند، با مقیاس‌دهی برابر برای هر دو محور و خطوط شبکه برای نمایش بهتر توزیع داده‌ها، که باید به دلیل عدم همبستگی بین متغیرها دایره‌ای ظاهر شود.

```python
import numpy as np
import matplotlib.pyplot as plt

# تعریف بردار میانگین و ماتریس کوواریانس
mean = [0, 0]  # مثال: داده 2 بعدی با میانگین صفر
cov = [[1, 0], 
       [0, 1]]  # ماتریس کوواریانس (2x2)

# تعداد نمونه‌ها
n_samples = 1000

# تولید داده
data = np.random.multivariate_normal(mean, cov, size=n_samples)

plt.scatter(data[:,0], data[:,1])
plt.xlabel("محور X")
plt.ylabel("محور Y")
plt.title("داده‌های پراکنده")
plt.gca().set_aspect("equal")  # نسبت ابعاد برابر
plt.grid(True)
plt.show()
```

$$  \Sigma = \begin{pmatrix}
a & 0 \\ 
0 & d 
\end{pmatrix}
$$

#### کد: مثال
این کد پایتون داده‌های 2 بعدی را از یک توزیع نرمال چندمتغیره با میانگین [0, 0] و ماتریس کوواریانس زیر تولید و مصورسازی می‌کند:

$$
\Sigma = \begin{bmatrix} 4 & 0 \\ 0 & 1 \end{bmatrix}
$$

ماتریس کوواریانس نشان می‌دهد که متغیرها واریانس‌های متفاوتی (4 و 1) دارند اما هیچ همبستگی ندارند. نمودار پراکندگی 1000 نمونه یک توزیع بیضوی را نشان خواهد داد، با گسترش بیشتر در امتداد محور X به دلیل واریانس بزرگتر 4 در آن جهت. نمودار شامل نسبت ابعاد برابر و خطوط شبکه برای مصورسازی بهتر است.

```python
import numpy as np
import matplotlib.pyplot as plt

# تعریف بردار میانگین و ماتریس کوواریانس
mean = [0, 0]  # مثال: داده 2 بعدی با میانگین صفر
cov = [[4, 0], 
       [0, 1]]  # ماتریس کوواریانس (2x2)

# تعداد نمونه‌ها
n_samples = 1000

# تولید داده
data = np.random.multivariate_normal(mean, cov, size=n_samples)

plt.scatter(data[:,0], data[:,1])
plt.xlabel("محور X")
plt.ylabel("محور Y")
plt.title("داده‌های پراکنده")
plt.gca().set_aspect("equal")  # نسبت ابعاد برابر
plt.grid(True)
plt.show()
```

$$  \Sigma = \begin{pmatrix}
a & b \\ 
b & d 
\end{pmatrix}
$$

a>d و b>0

#### کد: مثال
این کد پایتون داده‌های 2 بعدی را از یک توزیع نرمال چندمتغیره با میانگین [0, 0] و ماتریس کوواریانس زیر تولید و مصورسازی می‌کند:
$$
\Sigma = \begin{bmatrix} 10 & 4 \\ 4 & 2 \end{bmatrix}
$$

ماتریس کوواریانس نشان می‌دهد که متغیرها واریانس‌های متفاوتی (10 و 2) و یک همبستگی مثبت 4 دارند. نمودار پراکندگی 1000 نمونه یک توزیع بیضوی را نشان خواهد داد، با نقاط داده که به دلیل واریانس بزرگتر (10) بیشتر در امتداد محور X پخش شده‌اند و یک شکل کج به دلیل همبستگی مثبت بین متغیرها. نمودار شامل نسبت ابعاد برابر و خطوط شبکه برای مصورسازی بهتر است.

```python
import numpy as np
import matplotlib.pyplot as plt

# تعریف بردار میانگین و ماتریس کوواریانس
mean = [0, 0]  # مثال: داده 2 بعدی با میانگین صفر
cov = [[10, 4], 
       [4, 2]]  # ماتریس کوواریانس (2x2)

# تعداد نمونه‌ها
n_samples = 1000

# تولید داده
data = np.random.multivariate_normal(mean, cov, size=n_samples)

plt.scatter(data[:,0], data[:,1])
plt.xlabel("محور X")
plt.ylabel("محور Y")
plt.title("داده‌های پراکنده")
plt.gca().set_aspect("equal")  # نسبت ابعاد برابر
plt.grid(True)
plt.show()
```

$$  \Sigma = \begin{pmatrix}
a & b \\ 
b & d 
\end{pmatrix}
$$

a>d و b<0

#### کد: مثال
این کد پایتون داده‌های 2 بعدی را از یک توزیع نرمال چندمتغیره با میانگین [0, 0] و ماتریس کوواریانس زیر تولید و مصورسازی می‌کند:

$$
\Sigma = \begin{bmatrix} 10 & -4 \\ -4 & 2 \end{bmatrix}
$$

ماتریس کوواریانس نشان می‌دهد که متغیرها واریانس‌های متفاوتی (10 و 2) و یک همبستگی منفی 4- دارند. نمودار پراکندگی 1000 نمونه یک توزیع بیضوی را نشان خواهد داد، با نقاط داده که به دلیل واریانس بزرگتر (10) بیشتر در امتداد محور X پخش شده‌اند و یک شکل کج به دلیل همبستگی منفی بین متغیرها. نمودار شامل نسبت ابعاد برابر و خطوط شبکه برای مصورسازی بهتر است.

```python
import numpy as np
import matplotlib.pyplot as plt

# تعریف بردار میانگین و ماتریس کوواریانس
mean = [0, 0]  # مثال: داده 2 بعدی با میانگین صفر
cov = [[10, -4], 
       [-4, 2]]  # ماتریس کوواریانس (2x2)

# تعداد نمونه‌ها
n_samples = 1000

# تولید داده
data = np.random.multivariate_normal(mean, cov, size=n_samples)

plt.scatter(data[:,0], data[:,1])
plt.xlabel("محور X")
plt.ylabel("محور Y")
plt.title("داده‌های پراکنده")
plt.gca().set_aspect("equal")  # نسبت ابعاد برابر
plt.grid(True)
plt.show()
```

## بیان واریانس

- واریانس داده‌های تصویر شده بر روی جهت $v$ است:
$$
\text{VAR}(X\mathbf{v}) = \frac{1}{n} \sum_{i=1}^n (x_i^T\mathbf{v})^2
$$
- این را می‌توان به صورت زیر نوشت:
$$
\text{VAR}(X\mathbf{v}) = \frac{1}{n} ||X\mathbf{v}||^2 = \frac{1}{n} \mathbf{v}^TX^TX\mathbf{v} = \mathbf{v}^T \Sigma \mathbf{v}
$$

## مسئله بیشینه‌سازی
- ما هدفمان بیشینه کردن واریانس $\mathbf{v}^T\Sigma \mathbf{v}$ تحت قید $ ||\mathbf{v}||=1 $ است.
- این منجر به مسئله بهینه‌سازی زیر می‌شود:
$$ \max_{v} \mathbf{v}^T \Sigma \mathbf{v} \text{ به شرط } ||\mathbf{v}||=1 $$

## استفاده از ضرب‌کننده‌های لاگرانژ
- یک ضرب‌کننده لاگرانژ $\lambda$ معرفی می‌کنیم و لاگرانژی را تعریف می‌کنیم:
$$ L(\mathbf{v},\lambda)=\mathbf{v}^T \Sigma \mathbf{v} - \lambda (\mathbf{v}^T\mathbf{v} - 1) $$

- گرفتن مشتق نسبت به $\mathbf{v}$ و تنظیم آن بر 0:
$$ \frac{\partial{L}}{\partial{\mathbf{v}}} = 2\Sigma \mathbf{v} - 2 \lambda \mathbf{v} = 0 $$
- این به سادگی می‌شود:
$$
\Sigma \mathbf{v} = \lambda \mathbf{v}
$$
- ما همه $(\mathbf{v}_1, \lambda_1), (\mathbf{v}_2, \lambda_2), ... ,(\mathbf{v}_k, \lambda_k)$ را به عنوان $k$ بردار ویژه $\Sigma$ با بزرگترین مقادیر ویژه تعریف می‌کنیم: $\lambda_1 \geq \lambda_2 \geq ... \geq \lambda_k$

## تفسیر
- واریانس $\mathbf{v}^T \Sigma \mathbf{v}$ وقتی بیشینه می‌شود که $\mathbf{v}$ بردار ویژه متناظر با بزرگترین مقدار ویژه $\Sigma$ باشد.
- مقدار ویژه $\lambda$ نشان‌دهنده واریانس در جهت بردار ویژه $\mathbf{v}$ است.
- نتیجه: بردارهای ویژه ماتریس کوواریانس واریانس داده‌های تصویر شده را بیشینه می‌کنند.

## کد:
این کد پایتون تحلیل مؤلفه‌های اصلی (PCA) را روی مجموعه داده شبیه MNIST از `sklearn.datasets` انجام می‌دهد. مجموعه داده ابتدا بارگیری و تغییر شکل داده می‌شود، با مقادیر پیکسل نرمال شده. تابع `pca` مؤلفه‌های اصلی را با مرکزی کردن داده (کم کردن میانگین)، محاسبه ماتریس کوواریانس و به دست آوردن بردارهای ویژه و مقادیر ویژه آن محاسبه می‌کند. بردارهای ویژه برتر برای تصویر داده در یک فضای کاهش یافته انتخاب می‌شوند. کد مجموعه داده را به 20 مؤلفه اصلی کاهش می‌دهد و دو مؤلفه اصلی اول را در یک نمودار پراکندگی، رنگ‌آمیزی شده با برچسب‌های رقم، مصورسازی می‌کند. این مصورسازی به مشاهده چگونگی توزیع داده در فضای کاهش-بعدی کمک می‌کند.

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits

data = load_digits()
mnist = data.images
labels = data.target

mnist = mnist.reshape(-1, 64)

mnist = mnist.astype('float32') / 255.0
labels = labels.astype(int)
num_pcs = 20

def pca(X, num_components):
    X_meaned = X - np.mean(X, axis=0)
    covariance_matrix = np.cov(X_meaned, rowvar=False)
    print(X.shape)
    print(covariance_matrix.shape)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
    sorted_index = np.argsort(eigenvalues)[::-1]
    sorted_eigenvectors = eigenvectors[:, sorted_index]
    eigenvector_subset = sorted_eigenvectors[:, :num_components]
    X_reduced = np.dot(X_meaned, eigenvector_subset)
    return X_reduced, eigenvector_subset

mnist_reduced, eigenvector_subset = pca(mnist, num_pcs)
print(mnist_reduced.shape)
plt.figure(figsize=(8, 6))
scatter = plt.scatter(mnist_reduced[:, 0], mnist_reduced[:, 1], c=labels, cmap='tab10', alpha=0.7)
plt.colorbar(scatter)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()
```

## کد:
این کد پایتون مجموعه داده MNIST کاهش یافته را با استفاده از معکوس تبدیل PCA تجزیه می‌کند. `mnist_decompressed` با ضرب داده کاهش یافته (`mnist_reduced`) در ترانهاده بردارهای ویژه (`eigenvector_subset.T`) و اضافه کردن میانگین مجموعه داده اصلی بازسازی می‌شود. تابع `visualize_decompression` تصاویر اصلی و تجزیه شده را برای مقایسه کنار هم نمایش می‌دهد. این تابع هر دو داده اصلی و تجزیه شده را به فرمت تصویر تغییر شکل می‌دهد و 5 تصویر اول را به همراه نسخه‌های تجزیه شده آن‌ها نشان می‌دهد، که یک نمایش بصری از چگونگی حفظ جزئیات تصویر توسط فرآیند فشرده‌سازی و تجزیه PCA ارائه می‌دهد.

```python
mnist_decompressed = np.dot(mnist_reduced, eigenvector_subset.T) + np.mean(mnist, axis=0)

def visualize_decompression(original, decompressed, img_shape, num_images=5, title=""):
    original = original.reshape(-1, *img_shape)
    decompressed = decompressed.reshape(-1, *img_shape)

    plt.figure(figsize=(10, 4))

    for i in range(num_images):
        plt.subplot(2, num_images, i + 1)
        plt.imshow(original[i])
        plt.axis('off')

        plt.subplot(2, num_images, num_images + i + 1)
        plt.imshow(decompressed[i])
        plt.axis('off')

    plt.tight_layout()
    plt.show()


visualize_decompression(mnist[:5], mnist_decompressed[:5], img_shape=(8, 8), title="MNIST")
```

## درک چرخش داده در تحلیل مؤلفه‌های اصلی (PCA)

در تحلیل مؤلفه‌های اصلی (PCA)، هدف اولیه کاهش ابعاد داده در حین حفظ تا حد امکان واریانس است. یک مؤلفه کلیدی این فرآیند شامل **چرخش داده** برای تراز با محورهای جدیدی است که جهات بیشینه واریانس را ثبت می‌کنند. این چرخش از نظر ریاضی با تبدیل داده اصلی با استفاده از **بردارهای ویژه** ماتریس کوواریانس به دست می‌آید و نقش مرکزی در فرآیند کاهش ابعاد ایفا می‌کند.

#### 1. ماتریس کوواریانس و بردارهای ویژه

در PCA، اولین قدم محاسبه **ماتریس کوواریانس** مجموعه داده است که روابط و وابستگی‌های بین ویژگی‌های مختلف را نشان می‌دهد. ماتریس کوواریانس به صورت زیر تعریف می‌شود:

$$
\text{Cov}(X) = \frac{1}{N-1} X^T X
$$

جایی که $(X)$ ماتریس داده به اندازه $(n \times d)$ است (با $(n)$ تعداد نمونه‌ها و $(d)$ تعداد ویژگی‌ها)، و $(N)$ تعداد نمونه‌ها است.

از ماتریس کوواریانس، سپس **مقادیر ویژه** و **بردارهای ویژه** را محاسبه می‌کنیم. بردارهای ویژه نشان‌دهنده جهات محورهای جدید (مؤلفه‌های اصلی) هستند و مقادیر ویژه نشان‌دهنده مقدار واریانس ثبت شده توسط هر مؤلفه اصلی هستند.

$$
\text{Cov}(X) = V \Lambda V^T
$$

جایی که:
- $(V)$ ماتریس بردارهای ویژه است،
- $(\Lambda)$ ماتریس قطری مقادیر ویژه است.

#### 2. تبدیل داده (چرخش)

هنگامی که بردارهای ویژه را داریم، می‌توانیم داده را با تصویر کردن آن بر روی پایه جدید تعریف شده توسط بردارهای ویژه **بچرخانیم**. این تبدیل به صورت زیر نشان داده می‌شود:

$$
X_{n \times d} V_{d \times d} = \hat{X}_{n \times d}
$$

در اینجا، $(X)$ ماتریس داده اصلی است، $(V)$ ماتریس بردارهای ویژه است و $(\hat{X})$ داده تبدیل شده (یعنی داده پس از چرخش) است.

نقاط داده اکنون در امتداد مؤلفه‌های اصلی تراز شده‌اند، جایی که اولین مؤلفه اصلی بیشترین واریانس را ثبت می‌کند و مؤلفه‌های بعدی مقادیر کاهش یافته واریانس را ثبت می‌کنند. این چرخش امکان نمایش معنادارتر داده را فراهم می‌کند، به ویژه هنگام کاهش ابعاد.

#### 3. ماتریس کوواریانس در فضای تبدیل شده

پس از چرخش داده، می‌توانیم ماتریس کوواریانس داده تبدیل شده، $(\hat{X})$ را محاسبه کنیم که در حالت ایده‌آل باید قطری باشد. تبدیل اطمینان حاصل می‌کند که کوواریانس بین مؤلفه‌های مختلف در فضای جدید صفر است، که یک ویژگی کلیدی PCA است. ماتریس کوواریانس داده تبدیل شده را می‌توان به صورت زیر بیان کرد:

$$
\text{Cov}(\hat{X}) = V^T \text{Cov}(X) V = \Lambda
$$

از آنجایی که بردارهای ویژه متعامد هستند، ماتریس کوواریانس در فضای جدید قطری است، با مقادیر ویژه روی قطر. این قطری شدن نشان می‌دهد که مؤلفه‌های اصلی جدید ناهمبسته هستند.

#### 4. مشتق دقیق کوواریانس در فضای تبدیل شده

با شروع با ماتریس کوواریانس داده اصلی، تبدیل را با بردارهای ویژه اعمال می‌کنیم:

$$
\text{Cov}(X V) = \frac{1}{N-1} (X V)^T (X V)
$$

این را می‌توان به صورت زیر گسترش داد:

$$
= \frac{1}{N-1} V^T X^T X V
$$

بعد، ماتریس کوواریانس اصلی را جایگزین می‌کنیم:

$$
= \frac{1}{N-1} V^T \text{Cov}(X) V
$$

با استفاده از این واقعیت که ماتریس کوواریانس $(
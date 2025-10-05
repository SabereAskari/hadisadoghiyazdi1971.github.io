---
layout: persian  # یا single با کلاس rtl-layout
classes: wide rtl-layout
dir: rtl
title: "رویای عمیق"
permalink: /teaching/studenteffort/patterneffort/DeepDream/
author_profile: true

header:
  overlay_image: "/assets/images/background.jpg"
  overlay_filter: 0.3
  overlay_color: "#5e616c"
  caption: "Photo credit: [**Unsplash**](https://unsplash.com)"

---

# رویای عمیق

**نویسنده**: صابره عسکری

- <sabereaskari14@gmail.com>

**دانشگاه فردوسی مشهد**
---

# مقدمه

**رویای عمیق** یک آزمایش است که الگوهای آموخته‌شده توسط یک شبکه‌ی عصبی را به تصویر می‌کشد. مشابه زمانی که یک کودک به ابرها نگاه می‌کند و سعی می‌کند اشکال تصادفی را تفسیر کند، رویای عمیق بیش‌ازحد تفسیر می‌کند و الگوهایی را که در یک تصویر می‌بیند تقویت می‌نماید.

این کار با عبور دادن تصویر از شبکه انجام می‌شود، سپس گرادیان تصویر نسبت به فعال‌سازی‌های یک لایه‌ی خاص محاسبه می‌گردد. تصویر بعداً طوری تغییر داده می‌شود که این فعال‌سازی‌ها افزایش پیدا کنند؛ در نتیجه الگوهایی که شبکه تشخیص داده تقویت می‌شوند و خروجی به شکل تصویری شبیه به رؤیا در می‌آید.

این فرایند **"Inceptionism"** نام‌گذاری شد (اشاره‌ای به [InceptionNet](https://arxiv.org/pdf/1409.4842.pdf) و همچنین فیلم [Inception](https://en.wikipedia.org/wiki/Inception)).

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="dogception.png" alt="IPS1" style="width: 50%; height: 50%; object-fit: contain;">
</div>

# ریشه‌ها و توسعه‌ی رویای عمیق

**رویای عمیق (Deep Dream)** از تحقیقات گوگل در زمینه‌ی **یادگیری عمیق (Deep Learning)** و **شبکه‌های عصبی (Neural Networks)** سرچشمه گرفت. هدف اصلی این بود که درک و تجسم شود که شبکه‌های عصبی چگونه تصاویر را ادراک و پردازش می‌کنند. با معکوس کردن کاربرد سنتی **CNNها (Convolutional Neural Networks)** که معمولاً برای دسته‌بندی و شناسایی الگوها در تصاویر استفاده می‌شوند، پژوهشگران شبکه‌ها را بازکاربرد دادند تا الگوها را تولید و تقویت کنند.

نتیجه، مجموعه‌ای از تصاویر شگفت‌انگیز و فراواقعی بود که تخیل عمومی را به خود جلب کرد.

نام **"Deep Dream"** الهام‌گرفته از فیلم *Inception* بود که ماهیت بازگشتی این فرایند را منعکس می‌کند؛ جایی که شبکه در لایه‌های خود "رؤیا می‌بیند" و الگوها را به‌صورت تکراری تقویت می‌کند.

# درک رویای عمیق

تولید تصویر توسط ماشین، یکی از ویژگی‌های **رویای عمیق (Deep Dreaming)** است. این تصاویر فوق‌العاده خلاقانه توسط یک شبکه‌ی عصبی تولید می‌شوند؛ شبکه‌ای که درواقع مجموعه‌ای از مدل‌های یادگیری آماری است که با الگوریتم‌هایی نسبتاً ساده و الهام‌گرفته از فرایندهای تکاملی هدایت می‌شوند.

دانشمندان میلیون‌ها عکس را وارد این شبکه‌ها کرده‌اند تا آن‌ها را **آموزش (Training)** دهند و سپس به‌تدریج پارامترهای شبکه را تغییر داده‌اند تا به دسته‌بندی مطلوب برسند.

نحوه‌ی آموزش الگوریتم، تأثیر چشمگیری بر کل فرایند بهبود الگوهای تصویری دارد. به‌همین ترتیب، اگر یک الگوریتم برای شناسایی چهره‌ها در تصاویر آموزش دیده باشد، تلاش خواهد کرد تا از هر تصویری چهره استخراج کند. این پدیده به‌نوعی **پَرِیدولیا (Pareidolia)** الگوریتمی است.

# رویای عمیق چگونه کار می‌کند؟

در هسته‌ی خود، رویای عمیق از یک **CNN** استفاده می‌کند که روی یک مجموعه‌داده‌ی عظیم از تصاویر آموزش دیده است. یک **CNN** از لایه‌هایی از گره‌های به‌هم‌پیوسته یا نورون‌ها تشکیل شده است که هر لایه مسئول تشخیص سطوح مختلفی از ویژگی‌های یک تصویر است—از لبه‌های ساده گرفته تا اشیای پیچیده.

زمانی‌که یک تصویر به رویای عمیق داده می‌شود، برنامه الگوهایی را که یاد گرفته شناسایی کند تقویت می‌کند. این کار از طریق فرایندی به‌نام *"Inceptionism"* انجام می‌شود؛ جایی که شبکه دستور می‌گیرد تشخیص ویژگی‌ها را در لایه‌های مختلف به حداکثر برساند.

<div style="display: flex; justify-content: center; align-items: center; gap: 10px; margin-bottom:15px ">
    <img src="Screenshot-2024-05-26-004105.webp" alt="IPS1" style="width: 50%; height: 50%; object-fit: contain;">
</div>

برای نمونه، اگر شبکه الگویی شبیه به یک سگ تشخیص دهد، آن الگو را تقویت می‌کند و تصویر به‌گونه‌ای تغییر می‌کند که پر از اشکال و فرم‌های شبیه به سگ به‌نظر برسد.

بیایید نشان دهیم که چگونه می‌توان یک **Neural Network** را وادار کرد تا "Dream" ببیند و الگوهای فراواقعی‌ای را که در یک تصویر مشاهده می‌کند تقویت کند.

```python
import tensorflow as tf
import numpy as np

import matplotlib as mpl

import IPython.display as display
import PIL.Image
```

## یک تصویر برای Dream-ify انتخاب کنید

برای این آموزش، بیایید از یک تصویر [Labrador](https://commons.wikimedia.org/wiki/) 
<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="https://storage.googleapis.com/download.tensorflow.org/example_images/YellowLabradorLooking_new.jpg" alt="IPS1" style="width: 50%; height: 50%; object-fit: contain;">
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

یک مدل **Image Classification** از پیش آموزش‌دیده دانلود و آماده کنید. شما از [InceptionV3](https://keras.io/api/applications/inceptionv3/) استفاده خواهید کرد که مشابه مدلی است که در اصل در **DeepDream** به‌کار رفته بود.

توجه داشته باشید که هر [مدل از پیش آموزش‌دیده](https://keras.io/api/applications/#available-models) دیگری نیز قابل استفاده است، اگرچه در این صورت باید نام لایه‌ها را در ادامه مطابق تغییرات جدید تنظیم کنید.

base_model = tf.keras.applications.InceptionV3(include_top=False, weights='imagenet')

ایده‌ی **DeepDream** این است که یک لایه (یا چند لایه) انتخاب شود و **"Loss"** به‌گونه‌ای به حداکثر برسد که تصویر به‌طور فزاینده‌ای لایه‌ها را "تحریک" کند. پیچیدگی ویژگی‌هایی که در تصویر ایجاد می‌شوند بستگی به لایه‌های انتخاب‌شده توسط شما دارد؛ به‌عبارت دیگر، لایه‌های پایین‌تر **Strokeها** یا الگوهای ساده تولید می‌کنند، در حالی که لایه‌های عمیق‌تر ویژگی‌های پیچیده‌تری در تصاویر ایجاد می‌کنند یا حتی اشیای کامل را نمایان می‌سازند.

معماری **InceptionV3** نسبتاً بزرگ است (برای مشاهده‌ی نمودار معماری مدل به مخزن تحقیقاتی **TensorFlow** مراجعه کنید: [research repo](https://github.com/tensorflow/models/tree/master/research/slim)).

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

متدی که این کار را انجام می‌دهد، در ادامه داخل یک `tf.function` برای بهبود عملکرد قرار گرفته است. این متد از یک `input_signature` استفاده می‌کند تا اطمینان حاصل شود که تابع برای اندازه‌های مختلف تصویر یا مقادیر `steps`/`step_size` دوباره ردیابی (**retrace**) نمی‌شود. برای جزئیات بیشتر به [Concrete functions guide](../../guide/function.ipynb) مراجعه کنید.

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
در اینجا نسخه‌ی **Tiled** معادل تابع `deepdream` که قبلاً تعریف شده بود، آورده شده است:
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

خیلی بهتر شد! با تغییر تعداد **Octaveها**، **Octave Scale** و لایه‌های فعال‌شده، می‌توانید ظاهر تصویر **DeepDream** خود را تغییر دهید.

خوانندگان ممکن است به [TensorFlow Lucid](https://github.com/tensorflow/lucid) نیز علاقه‌مند باشند، که ایده‌های معرفی‌شده در این آموزش را گسترش می‌دهد تا شبکه‌های عصبی را تجسم و تفسیر کنند.

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

## نتیجه‌گیری

به طور خلاصه، رویای عمیق ترکیبی از **هنر و هوش مصنوعی** است که ظرفیت عظیم خلق بصری ارتقایافته توسط هوش مصنوعی را نشان می‌دهد. تأثیر دگرگون‌کننده آن بر هنر، تصویربرداری پزشکی، واقعیت افزوده و بازی‌ها، توانایی آن در **انطباق‌پذیری و الهام‌بخشی** را به نمایش می‌گذارد. افزون بر این، با هر تصویری که به الگوریتم داده می‌شود، رویای عمیق بهبود یافته و نتایج پیشین خود را پشت سر می‌گذارد.

# منابع

- <https://www.tensorflow.org/tutorials/generative/deepdream?utm_source=chatgpt.com>
- <https://research.google/blog/inceptionism-going-deeper-into-neural-networks/>
- <https://www.geeksforgeeks.org/computer-vision/deep-dream-an-in-depth-exploration/>
- <https://en.wikipedia.org/wiki/DeepDream>

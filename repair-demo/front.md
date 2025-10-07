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

<script>
fetch('https://smart-repair-api.onrender.com/optimize', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({allocation_type: "random"})
})
.then(r => r.json())
.then(data => {
    document.body.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
});
</script>
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

<div class="container">
  <div class="header">
    <h1>تخصیص کارهای تعمیرات</h1>
    <p> </p>
  </div>
  <div class="projects-grid">
    <div class="project-card">
      <!-- <a href="/repair-demo/index.html">-->
      <a href="/smart-repair-api/templates/index.html">
        <img src="{{ '/assets/schedulling/inputdata.jpg' | relative_url }}" 
             alt="Pattern Recognition" 
             class="project-image">
        <div class="project-content">
          <h3 class="project-title">دریافت اطلاعات و تکمیل فرم </h3>
        </div>
      </a>
    </div>
    <div class="project-card">
      <a href="/repair-demo/Infoshowing">
        <img src="{{ '/assets/schedulling/info.jpg' | relative_url }}" 
             alt="Machine Learning" 
             class="project-image">
        <div class="project-content">
          <h3 class="project-title">بازیابی اطلاحات فرم ها</h3>
        </div>
      </a>
    </div>
    <div class="project-card">
      <a href="/repair-demo/regparam">
        <img src="{{ '/assets/schedulling/param.JPG' | relative_url }}" 
             alt="Circuit Analysis" 
             class="project-image">
        <div class="project-content">
          <h3 class="project-title">تنظیم پارامترها</h3>
        </div>
      </a>
    </div>
    
  </div> <!-- project grid-->


  <div class="footer">
    
  </div>
</div>

<style>

.projects-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem; /* فاصله بین کارت‌ها */
  margin-top: 2rem;
}

.project-card {
  border: 1px solid #eaeaea;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.project-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.project-content {
  padding: 1.5rem;
}

.project-title {
  margin-top: 0;
  color: #333;
}
</style>

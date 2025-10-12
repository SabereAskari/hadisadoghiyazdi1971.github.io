---
layout: single
title: "Programming tools for Data engineering"
permalink: /teaching/DataEng/
author_profile: true
classes: wide
header:
  overlay_image: "/assets/images/background.jpg"
  overlay_filter: 0.3
  overlay_color: "#5e616c"
  caption: "Photo credit: [**Unsplash**](https://unsplash.com)"
---

<div class="container">
  <div class="header">
    <h1>Toolkits</h1>
    <p> </p>
  </div>
  <div class="projects-grid">
    <div class="project-card">
      <a href="/teaching/DataEngCourse/Data">
        <img src="{{ '/assets//DataEngCourseimages/Data1.jpg' | relative_url }}" 
             alt="datadefine" 
             class="project-image">
        <div class="project-content">
          <h3 class="project-title">Data manipulation tools</h3>
        </div>
      </a>
    </div>
    <div class="project-card">
      <a href="/teaching/DataEngCourse/processingtools">
        <img src="{{ '/assets//DataEngCourseimages/processingtools.jpg' | relative_url }}" 
             alt="processingtools" 
             class="project-image">
        <div class="project-content">
          <h3 class="project-title">Procesing of data</h3>
        </div>
      </a>
    </div>
     
    
  </div><!--end grid-->

  <div class="footer">
    
  </div>
</div>

<style>

.projects-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem; /* فاصله بین کارت‌ها */
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

/* برای تبلت‌ها */
@media (max-width: 1024px) {
  .projects-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* برای موبایل‌ها */
@media (max-width: 768px) {
  .projects-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* برای موبایل‌های کوچک */
@media (max-width: 480px) {
  .projects-grid {
    grid-template-columns: 1fr;
  }
}

</style>


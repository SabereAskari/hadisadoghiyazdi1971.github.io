---
layout: single
title: "Toolkit"
permalink: /teaching/researchertoolkit/
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
      <a href="/teaching/studenteffort/toolkit/circuit_tools">
        <img src="{{ '/assets/images/MLSignalToolkits.jpg' | relative_url }}" 
             alt="Pattern Recognition" 
             class="project-image">
        <div class="project-content">
          <h3 class="project-title">Circuit & Electronic</h3>
        </div>
      </a>
    </div>
    <div class="project-card">
      <a href="/teaching/studenteffort/toolkit/ML_tools">
        <img src="{{ '/assets/images/ML_toolkit.JPG' | relative_url }}" 
             alt="Rag1" 
             class="project-image">
        <div class="project-content">
          <h3 class="project-title">Machine Learning</h3>
        </div>
      </a>
    </div>
     <div class="project-card">
      <a href="/teaching/studenteffort/toolkit/software_tools">
        <img src="{{ '/assets/images/software_toolkit.jpg' | relative_url }}" 
             alt="Rag1" 
             class="project-image">
        <div class="project-content">
          <h3 class="project-title">Machine Learning</h3>
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


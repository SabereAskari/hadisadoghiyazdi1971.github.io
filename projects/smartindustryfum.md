---
layout: persian  # یا single با کلاس rtl-layout
classes: wide rtl-layout
dir: rtl
title: " دستیار هوشمند ارتباط با صنعت دانشگاه فردوسی مشهد"
permalink: /projects/smartindustryfum/
author_profile: true
header:
  overlay_image: "/assets/images/background.jpg"
  overlay_filter: 0.3
  overlay_color: "#5e616c"
  caption: "Photo credit: [**Unsplash**](https://unsplash.com)"
---
دستیارهوشمند ارتباط با صنعت دانشگاه فردوسی مشهد را بطور مخفف **سایفوم**  می نامیم

Smart Assistant for Industry-University Communication at Ferdowsi University of Mashhad


<div class="container">
  <div class="header">
    <h1></h1>
    <p> </p>
  </div>
  <div class="projects-grid">
    <div class="project-card">
      <!-- <a href="/repair-demo/index.html">-->
      <a href="https://hadisadoghiyazdi.loca.lt/">
        <img src="{{ '/assets/Projectsimages/smartindustryfum/Input_saifum.jpg' | relative_url }}" 
             alt="saifumrun" 
             class="project-image">
        <div class="project-content">
          <h3 class="project-title">  سوالات خود را از سایفوم بپرسید بدون وی پی ان  </h3>
        </div>
      </a>
    </div>
    <div class="project-card">
      <a href="/projects/smartindustrysaifum/infosaifum">
        <img src="{{ '/assets/Projectsimages/smartindustryfum/infosaifum.jpg' | relative_url }}" 
             alt="howsaifum" 
             class="project-image">
        <div class="project-content">
          <h3 class="project-title">سایفوم چیست</h3>
        </div>
      </a>
    </div>
    <div class="project-card">
      <a href="/projects/smartindustrysaifum/saifumlaw">
        <img src="{{ '/assets/Projectsimages/smartindustryfum/lawsaifum.jpg' | relative_url }}" 
             alt="lawsaifum" 
             class="project-image">
        <div class="project-content">
          <h3 class="project-title">مقررات ارتباط با صنعت دانشگاه فردوسی مشهد</h3>
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

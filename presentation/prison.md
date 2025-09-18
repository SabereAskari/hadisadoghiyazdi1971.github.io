---
layout: single
title: "Detection of Anomalous Behavior in Prisoner Gatherings Using Surveillance Cameras"
permalink: /presentation/prison/
author_profile: true
classes: wide
sidebar:
  nav: "presentaton"
header:
  overlay_image: "/assets/images/background.jpg"
  overlay_filter: 0.3
  overlay_color: "#5e616c"
  caption: "Photo credit: [**Unsplash**](https://unsplash.com)"
---

## With Emphasis on Artificial Intelligence Applications
- <a href="https://h-sadoghi.github.io/" style="text-decoration:underline; color:blue;" target="_blank"><strong>Hadi Sadoghi Yazdi</strong></a> : PhD in Electronics, Expert Consultant in Machine Vision/Learning and Data Systems
- Affilation and institute:
    - Professor of Electrical and Computer Engineering, Ferdowsi University of Mashhad  
    - Director of Pattern Recognition Laboratory
    - Member of SCIIP - Center of Excellence on Soft Computing and Intelligent Information Processing

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/Presentationimages/prison/Prison_AI_Security_System_Nature_Inspired.jpg" alt="prisonheader1" style="width: 50%; height: 50%; object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
  Prison with AI
</div>

## Table of Contents
- [Introduction](#introduction)
  - [Objectives](#objectives)
  - [Existing Implementations in Various Countries](#existing-implementations-in-various-countries)
- [Methodology](#methodology)
  - [Data Collection](#data-collection)
  - [Model Development](#model-development)
  - [Deployment](#deployment)
  - [Technology Stack](#technology-stack)
- [Challenges and Mitigations](#challenges-and-mitigations)
- [Expected Outcomes](#expected-outcomes)
- [Additional Service Offerings](#additional-service-offerings)
- [References](#references)

## Introduction

### Objectives
- Develop AI-powered system for real-time anomaly detection in prison CCTV feeds.
- Reduce response times to threats (e.g., fights, self-harm).
- Ensure ethical compliance (privacy, bias mitigation).
- Achieve 90%+ accuracy in detecting crowd-based anomalies.

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/Presentationimages/prison/objective.JPG" alt="prisonheader1" style="width: 50%; height: 50%; object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
  AI-based real-time anomaly detection in prison CCTV
</div>

### Existing Implementations in Various Countries

- **China**: AI surveillance with facial recognition for threat detection (<a href="https://en.wikipedia.org/wiki/Prison" style="text-decoration:underline; color:green;" target="_blank"><strong>prison</strong></a> breaks impossible).
  
<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/Presentationimages/prison/china.png" alt="prisonheader1" style="width: 50%; height: 50%; object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
  Stephen Chenin Beijing, 1 Apr 2019
</div>

- **UK**: <a href="https://csecrosscom.co.uk/solutions/cctv-video-analytics/avigilon-unusual-activity-detection/" style="text-decoration:underline; color:green;" target="_blank"><strong>Avigilon</strong></a> (software for contraband and behavior monitoring). Avigilon's self-learning AI continuously improves detection accuracy by adapting to environments, reducing false alarms and enhancing security threat identification.
- **Singapore**: AI-based CCTV for fights and headcount checks.
- **India**: Facial recognition in Tihar jail for anomaly detection.

**Singapore**: AI-based CCTV for fights and headcount checks. New technology on trial at <a href="https://www.straitstimes.com/singapore/new-technology-on-trial-at-changi-prison-can-detect-cell-fights-through-video-analytics" style="text-decoration:underline; color:green;" target="_blank"><strong>Changi Prison</strong></a> can detect cell fights through video analytics.

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/Presentationimages/prison/changi_singapour.png" alt="prisonheader1" style="width: 50%; height: 50%; object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
  Fights and headcount checks
</div>

**India**: <a href="https://www.newindianexpress.com/cities/delhi/2024/Aug/16/tihar-installs-1248-cctvs-with-facial-recognition" style="text-decoration:underline; color:green;" target="_blank"><strong>Tihar Jail</strong></a>, one of the largest prison complexes in India, has been implementing a facial recognition, anomaly system and enhance security.

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/Presentationimages/prison/Jail.png" alt="prisonheader1" style="width: 50%; height: 50%; object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
  Tihar installs 1,248 CCTVs with facial recognition
</div>

## Methodology

### Data Collection
- Gather anonymized CCTV footage (ethical approvals).
- Label data for normal vs. anomalous behaviors (e.g., fights, gatherings).
- **Example**: <a href="https://arxiv.org/abs/2409.05383" style="text-decoration:underline; color:green;" target="_blank"><strong>Deep Learning for Video Anomaly Detection: A Review</strong></a>

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/Presentationimages/prison/DataCollectionReview.JPG" alt="prisonheader1" style="width: 50%; height: 50%; object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
  Illustrations of frame-level (Top) and pixel-level (Bottom) output
</div>

### Model Development
- **Frame Analysis**
  - Use CNNs for video frame analysis, RNNs for temporal tracking.
- **Frame Encoding**
  - EfficientNet-B7 (pretrained on Kinetics-700) for high-resolution feature extraction.
  - 3D Convolutional Blocks (I3D) for short-term spatiotemporal features (5-frame snippets).
- **Temporal Context**
  - Bidirectional Quasi-Recurrent Neural Networks (QRNNs): Lightweight alternative to LSTMs/GRUs. Processes sequences with parallel convolution + recurrent pooling (reducing latency 40% vs. GRU).
  - Attention Mechanisms: Self-attention layers to weight critical frames (e.g., sudden motion/occlusion).

- **Implement anomaly detection**
  - use YOLO v7, Autoencoders
  - use Adaptive frame skipping based on optical flow magnitude.
- **Edge Computing Deployment**
  - Hardware: NVIDIA Jetson AGX Orin (48 TOPS) / Google Coral TPU.
  - Model Distillation: Teacher (EfficientNet-B7 + QRNN) → Student (MobileNetV3 + QRNN).

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/Presentationimages/prison/DeepNet.png" alt="prisonheader1" style="width: 50%; height: 50%; object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
  Deep Neural Network
</div>

### Deployment
- Deploy on CCTV with AI accelerators (e.g., NVIDIA Jetson).
- Pilot testing in controlled prison settings.
- Conduct ethical audits (GDPR <a href="https://gdpr-info.eu/" style="text-decoration:underline; color:green;" target="_blank"><strong>(General Data Protection Regulation)</strong></a>-like policies, bias checks).

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/Presentationimages/prison/Deployment1.png" alt="prisonheader1" style="width: 50%; height: 50%; object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
  Deployment of AI-enabled CCTV system on-site with automotive-grade accelerators for real-time monitoring.
</div>

### Technology Stack

| Component       | Description                                      |
|-----------------|--------------------------------------------------|
| Hardware        | High-res CCTV with IR, motion sensors           |
| Software        | Python (OpenCV, TensorFlow), MQTT alerts        |
| AI Models       | CNN-RNN, YOLO, GANs for synthetic data          |
| Security        | Encrypted storage, access controls              |

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/Presentationimages/prison/TechnologyStackVisualization.png" alt="prisonheader1" style="width: 50%; height: 50%; object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
  Technology Stack Visualization
</div>

## Challenges and Mitigations
- **Privacy Concerns**: GDPR-like policies, data anonymization.
- <a href="https://hadisadoghiyazdi1971.github.io/physics/machine%20learning/What-Bias/" style="text-decoration:underline; color:green;" target="_blank"><strong>AI Bias</strong></a>: Diverse training data, fairness algorithms.
- **False Positives**: Fine-tune models with prison-specific data.

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/Presentationimages/prison/concerns.jpg" alt="prisonheader1" style="width: 50%; height: 50%; object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
  Privacy, fairness, and accuracy: GDPR-like privacy with anonymization, bias mitigation through diverse data and fairness algorithms, and reduced false positives via prison-specific fine-tuning.
</div>

## Expected Outcomes
- 30-50% reduction in security incidents (inspired by India).
- Cost savings via automated monitoring (like Singapore).
- Scalable system for global adoption.

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/Presentationimages/prison/ExpectedOutcomes.png" alt="prisonheader1" style="width: 50%; height: 50%; object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
  Significant security gains, cost savings, and scalable global deployment
</div>

## Additional Service Offerings
- <a href="https://limablog.org/it-is-time-to-start-thinking-about-smart-prisons/" style="text-decoration:underline; color:green;" target="_blank"><strong>Smart Prisons</strong></a>: Closing the gap between smart-city innovations and their application in correctional facilities.
- <a href="https://www.g4s.com/en-gb/news/2016/12/06/trial-of-new-technology-to-tackle-contraband" style="text-decoration:underline; color:green;" target="_blank"><strong>Tackle Prison Contraband</strong></a>: Trial of new technology to tackle prison contraband.
- <a href="https://www.skysafe.io/industries/correctional-facilities" style="text-decoration:underline; color:green;" target="_blank"><strong>Guarding the Perimeter</strong></a>: Drone Detection and Neutralization in Prisons

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <img src="/assets/Presentationimages/prison/drone.jpg" alt="prisonheader1" style="width: 50%; height: 50%; object-fit: contain;">
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
  Protect Your Correctional Facility From Drone Threats
</div>

## References
- AI surveillance systems in China, Hong Kong, Singapore (2023 reports).
- UK Altcourse prison: Avigilon software (2022).
- India Punjab jails: AI CCTV deployment (2024).
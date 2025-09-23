---
layout: single  # یا single با کلاس rtl-layout
classes: wide 
title: "Gas Sensors: Types, Principles, and Applications"
permalink: /teaching/studenteffort/circuiteffort/mq2_gas_sensor/
author_profile: true
header:
  overlay_image: "/assets/images/background.jpg"
  overlay_filter: 0.3
  overlay_color: "#5e616c"
  caption: "Photo credit: [**Unsplash**](https://unsplash.com)"
---

## Mahdi Ahmadi 

Contact address: [mahdi.ahmadi.6th@gmail.com](mailto:mahdi.ahmadi.6th@gmail.com) 


<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
  <div style="flex: 1;">
    <img src="/assets/Courseimages/CircuitElectronicsImages/MQ2_Gas_Sensor/Mahdi.jpg" alt="my picture" style="width: 50%; height: 50%; object-fit: contain;">
  </div>
</div>

Biologists think the human nose can distinguish about 10,000 odors. A dog’s nose can distinguish about 2 million different odors, and it also has a high “analytical ability”. A specific smell can be found from many mixed smells.

Even so, there are still many colorless and odorless gases in nature that neither humans nor animals can smell. Therefore, we use gas sensors to measure the concentration of different gases.


## What is a gas sensor?

Gas sensors use physical or chemical reactions to convert the concentration of various gases into electrical signals, and output values after calculation. Widely used to detect toxic and harmful gases and natural gas leaks.

Gas sensors are devices used to monitor the presence or level of gas in a stationary environment. Commonly used in coal mines, petroleum, chemical, municipal, medical, transportation, family, and more.

Gas sensors can measure the presence and concentration of combustible, flammable, toxic gases, or oxygen consumption.


There are sensors that measure non-toxic gases such as oxygen and carbon dioxide, and sensors that detect toxic gases such as carbon monoxide, TVOC, and ammonia.

Gas sensors are often used in flammable, explosive and toxic places to protect workers.


## Table of Contents  

1. **Introduction**  
2. **What is a Gas Sensor?**  
3. **Types of Gas Sensors**  
   3.1. Semiconductor Gas Sensors  
   3.2. Electrochemical Gas Sensors  
   3.3. NDIR Gas Sensors  
   3.4. Catalytic Gas Sensors  
   3.5. Magnetic Gas Sensors  
   3.6. Photoionization Gas Sensors  
   3.7. Thermal Conductivity Gas Sensors  
   3.8. Gas Chromatograph Analyzer  
4. **MQ2 Gas Sensor Overview**  
5. **Internal Structure of MQ2**  
   5.1. External View  
   5.2. Internal View  
   5.3. Sensing Element Materials  
   5.4. Summary Table  
6. **How Gas Sensors Work**  
7. **MQ2 Module Hardware**  
8. **Calibration**  
9. **Arduino Experiments**  
   9.1. Experiment 1 – Analog Output (AO)  
   9.2. Experiment 2 – Digital Output (DO)  
10. **Applications of MQ2**  
11. **Conclusion**  
12. **References**  


## Gas Sensors Types

To choose the most suitable gas sensor, we must understand their characteristics. Questions to consider:

- Which sensor can measure toxic gases?
- Which one is portable?
- Which one has high accuracy?

Based on various criteria, gas sensors are classified as follows:

- **By gas type**: combustible, toxic, harmful gases, oxygen.
- **By usage**: portable vs fixed.
- **By sampling**: diffusion vs pumping.
- **By function**: single vs composite sensors.
- **By working principle**: semiconductor, electrochemical, NDIR, catalytic, thermal conductivity, magnetic sensors.


### 1. Semiconductor Gas Sensors


A semiconductor gas sensor uses a semiconductor element as a measuring unit. The gas undergoes a redox reaction on the surface, changing the resistance value.

For example, methane reacts with oxygen on the sensor, releasing pinned electrons, increasing conductivity. Resistance changes are proportional to methane presence and concentration.


<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
  <div style="flex: 1;">
    <img src="/assets/Courseimages/CircuitElectronicsImages/MQ2_Gas_Sensor/Semiconductor-Gas-Sensor.jpg" alt="Semiconductor Gas Sensors" style="width: 50%; height: 50%; object-fit: contain;">
  </div>
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
   some kind of Semiconductor Gas Sensors
</div>

**Advantages**:
- Simple structure
- Low price
- High sensitivity
- Fast response

**Disadvantages**:
- Small linear range
- Affected by other gases
- Sensitive to ambient temperature

**Applications**:
- Detecting methane, LPG, hydrogen leaks at homes and factories.


### 2. Electrochemical Gas Sensors


Electrochemical sensors react with gas to generate a current proportional to gas concentration.

**Working Principle**:
Gas diffuses through a dust-proof diaphragm, reaches a working electrode, reacts (oxidation/reduction), and generates current.


<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
  <div style="flex: 1;">
    <img src="/assets/Courseimages/CircuitElectronicsImages/MQ2_Gas_Sensor/Electrochemical-gas-sensor.jpg" alt="Electrochemical Gas Sensors" style="width: 50%; height: 50%; object-fit: contain;">
  </div>
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
   picture of a kind of Electrochemical Gas Sensor
</div>

**Advantages**:
- Fast response
- Linear output

**Disadvantages**:
- Requires oxygen-rich environment
- Electrolyte consumption
- Affected by temp, humidity, pressure, and similar gases

**Applications**:
Detects ozone, formaldehyde, CO, NH3, H2S, SO2, NO2, O2. Widely used in portable and industrial monitoring instruments.


### 3. NDIR Gas Sensors (Non-Dispersive Infrared)


NDIR sensors use infrared light. Gas molecules absorb specific IR wavelengths, and higher gas concentrations absorb more IR, reducing transmission.

**Example**:
Methane vibrates at 333KHz (3.3μm). Different molecules absorb different IR frequencies.


<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
  <div style="flex: 1;">
    <img src="/assets/Courseimages/CircuitElectronicsImages/MQ2_Gas_Sensor/Spectrum.jpg" alt="NDIR Gas Sensor" style="width: 50%; height: 50%; object-fit: contain;">
  </div>
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
   digram of IR freqency
</div>

**Advantages**:
1. Can measure CO2 and CH4, unlike CAT or EC sensors.
2. Doesn't need oxygen.
3. High concentration range (up to 100% v/v).
4. Stable over years (no frequent calibration).
5. Low maintenance.

**Disadvantages**:
- High power consumption
- Expensive for ppm-level detection
- Complex design

**Applications**:
- Ideal for measuring CO2 and methane with high accuracy and stability.


### 4. Catalytic Gas Sensors

This sensor is actually a gas detector based on a platinum resistance temperature sensor. A high temperature resistant catalyst layer is prepared on the surface of the platinum resistor, and at a certain temperature, the combustible gas is catalytically burned on the surface. Therefore, the platinum resistance temperature increases, resulting in a change in the resistance value.

Since the catalytic gas sensor platinum resistance is usually wrapped by porous ceramic beads, this sensor is also called a catalytic bead gas sensor. In theory, this sensor can detect all combustible gases, but there are many exceptions in practical applications. This sensor can usually be used to detect combustible gases such as methane, LPG, acetone, etc. in the air.



<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
  <div style="flex: 1;">
    <img src="/assets/Courseimages/CircuitElectronicsImages/MQ2_Gas_Sensor/catalytic-gas-sensor.jpg" alt=" Catalytic Gas Sensors" style="width: 50%; height: 50%; object-fit: contain;">
  </div>
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
   inside of a  Catalytic Gas Sensor
</div>

**Advantages:**

- Strong resistance to harsh climate and poisonous gas
- Long service life
- Can detect all flammable gases, including alkanes and non-alkanes
- Low maintenance cost

**Disadvantages:**

- Work in the dark
- Easy to explode or catch fire
- Components are susceptible to poisoning by sulfide and halogen compounds, which shorten their service life
- In a hypoxic environment, the error is larger

This sensor is mainly used to detect combustible gases, such as gas generating stations, and gas plants to analyze CO, H₂, C₂H₂, and other combustible gases in the air.


### 5. Magnetic Gas Sensors

After the magnetic gas sensor senses heat, light, radiation and pressure in the environment, its magnetic properties will also change accordingly. Using this feature, various reliable and high-sensitivity sensors can be made. Magnetic gas detectors are mostly magnetic probes with relatively strong measurement capabilities. When measuring gases, it is common to use the high magnetic properties of oxygen to measure the oxygen concentration. Because oxygen in the air can be attracted by strong magnetic fields. Commonly used are thermal magnetic convection oxygen analysis sensors and magneto-mechanical oxygen analysis sensors.

**Advantages:**

- Detects oxygen with excellent selectivity
- Magnetic oxygen analyzers are highly accurate

**Disadvantages:**

- Single measurement type
- Small application range

It is commonly used in chemical fertilizer production, cryogenic air separation, thermal power station combustion system, natural gas to acetylene, and other industrial production oxygen measurement. Also monitors exhaust gas, tail gas, flue gas and other emissions.


### 6. Photoionization Gas Sensors

A Photoionization gas sensor (PID) works by using photoion-ionized gas to detect gas. Simply put, the gas is irradiated with ultraviolet light generated by an ion lamp, and the gas will be ionized after absorbing enough ultraviolet light energy. The measured gas level is calculated by detecting the tiny current generated by the gas ionization. It can detect volatile organic compounds and other toxic gases from 10 ppb to 10,000 ppm. Many hazardous substances contain volatile organic compounds, and PID is highly sensitive to volatile organic compounds.


<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
  <div style="flex: 1;">
    <img src="/assets/Courseimages/CircuitElectronicsImages/MQ2_Gas_Sensor/PID-gas-sensor.jpg" alt="Photoionization Gas Sensors" style="width: 50%; height: 50%; object-fit: contain;">
  </div>
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
   picture of a Photoionization Gas Sensor
</div>

**Advantages:**

- High sensitivity
- No poisoning problem
- Safe and reliable
- Can detect more than 400 types of volatile organic gases

**Disadvantages:**

- Cannot measure air, toxic gases, and natural gas, etc.

It is the most sensitive device for detecting organic volatiles, especially for those gas leaks with very low concentrations, which has incomparable advantages compared to other detectors.


### 7. Thermal Conductivity Gas Sensors

A thermal conductivity gas sensor is a device that can sense a certain gas in the environment. It converts gas concentration information into electrical signals for detection, monitoring, analysis and alarming. Thermally conductive gas-sensitive materials measure their concentration based on the difference in thermal conductivity between different gases and air. Usually, a change in thermal conductivity is translated into a change in resistance through the circuit. The gas type and level are calculated from the change in resistance value.


<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
  <div style="flex: 1;">
    <img src="/assets/Courseimages/CircuitElectronicsImages/MQ2_Gas_Sensor/Thermal-Conductivity-Gas-Sensor.jpg" alt="Thermal Conductivity Gas Sensors" style="width: 50%; height: 50%; object-fit: contain;">
  </div>
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
   internal of Thermal-Conductivity-Gas-Sensors
</div>

**Advantages:**

- Wide detection range, the highest detection concentration can reach 100%
- Good working stability
- Long service life
- No catalyst aging problem

**Disadvantages:**

- Poor detection accuracy
- Low sensitivity
- Temperature drift

These gas sensors are widely used in chemical, coal, military, environmental, etc. industries, mainly to optimize sensor performance.


### 8. Gas Chromatograph Analyzer

Based on chromatographic separation technology and detection technology, various gas samples are separated and measured, hence the full analytical sensor. It has been used in power plant boiler tests.

During work, a certain gas sample is periodically taken from the sampling device. The chromatographic column is carried by a pure carrier gas (i.e., mobile phase) with a certain flow rate, and the chromatographic column is filled with a solid or liquid called a stationary phase. The components are repeatedly distributed in the two phases, flow out of the chromatographic column according to time, and enter the detector for quantitative determination.


<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
  <div style="flex: 1;">
    <img src="/assets/Courseimages/CircuitElectronicsImages/MQ2_Gas_Sensor/Gas-Chromatograph-Analyzer.jpg" alt="Gas Chromatograph Analyzer" style="width: 50%; height: 50%; object-fit: contain;">
  </div>
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
   structure of Gas Chromatograph Analyzer
</div>

**Advantages:**

- High sensitivity
- Suitable for micro and trace analysis
- Can analyze complex multiphase separation gases

**Disadvantages:**

- Regular sampling cannot achieve continuous sampling and analysis
- System is more complicated
- Mostly used for laboratory analysis, not suitable for industrial field gas monitoring


##  Detecting Gases with MQ2 Sensor and Microcontrollers

Have you ever wanted to give your microcontroller the ability to "smell" what's in the air? With the **MQ2 Gas Sensor Module**, you can add gas detection capabilities to your **Arduino** / **NodeMCU (ESP8266)** projects. This sensor can detect various gases like **LPG, smoke, alcohol, propane, methane, hydrogen**, and **carbon monoxide**.


##  Why is this sensor useful?

With the MQ2, you can prototype a variety of practical and fun applications:
-  **Indoor Air Quality Monitors** – to track pollutants or flammable gases.
-  **Smoke or Fire Alarms** – early detection before things get dangerous.
-  **DIY Breathalyzers** – as part of a science fair or educational tool.
-  **IoT Safety Systems** – when paired with Wi-Fi modules like NodeMCU.


##  MQ2 Gas Sensor Overview

The **MQ2 sensor** is one of the most popular sensors in the MQ family. It belongs to the class of **MOS (Metal Oxide Semiconductor)** sensors. These are also called **chemiresistors**, because their electrical resistance changes when they come into contact with certain gases.

<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
  <div style="flex: 1;">
    <img src="/assets/Courseimages/CircuitElectronicsImages/MQ2_Gas_Sensor/mq26pin.jpg" alt="MQ2 Gas Sensor" style="width: 50%; height: 50%; object-fit: contain;">
  </div>
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
   MQ2 Gas Sensor
</div>
---

###  Specifications

- Operating Voltage: **5V DC**
- Power Consumption: **~800mW**
- Gas Detection Range: **200 – 10,000 ppm**
- Detectable Gases:
  - LPG (liquefied petroleum gas)
  - Smoke
  - Alcohol
  - Propane
  - Hydrogen
  - Methane
  - Carbon Monoxide


##  Internal Structure of MQ2 Gas Sensor

The MQ2 is a **heater-driven** sensor, meaning it relies on internal heat to detect gases.

### 1. External View

<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
  <div style="flex: 1;">
    <img src="/assets/Courseimages/CircuitElectronicsImages/MQ2_Gas_Sensor/MQ2-Gas-Sensor-Parts-Hardware-Overview.jpg" alt="External View of mq2" style="width: 50%; height: 50%; object-fit: contain;">
  </div>
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
   picture of an mq2 in External view
</div>

The sensor body is enclosed with two layers of ultra-fine stainless steel mesh, also called the anti-explosion network.

This mesh ensures safety by preventing the internal heater from igniting any flammable gases present in the environment.

It also provides protective filtering, allowing only gas molecules to reach the sensing core while blocking dust and larger particles.

A copper-plated clamp ring holds the mesh securely and connects it to the body of the sensor.

### 2. Internal View (Protective Mesh Removed)

<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
  <div style="flex: 1;">
    <img src="/assets/Courseimages/CircuitElectronicsImages/MQ2_Gas_Sensor/insidemq2-.jpg" alt="Internal View (Protective Mesh Removed)" style="width: 50%; height: 50%; object-fit: contain;">
  </div>
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
   Internal View of mq2 gas sensor (Protective Mesh Removed)
</div>

With the mesh removed, the sensing core and heater element are visible.

The heater raises the temperature of the sensitive semiconductor layer, enabling it to detect gases such as LPG, methane, smoke, and alcohol vapors.

The internal structure is designed for fast response while still depending on the outer protective mesh for safe operation in real-world environments.

## Detailed Look Inside the MQ2 Sensor

If you carefully remove the outer mesh, you can see the internal components of the MQ2 gas sensor. At its center lies the **sensing element**, which is connected to **six metal legs** extending from a **round base made of Bakelite** — a type of heat-resistant hard plastic.

These six legs are arranged in a **star-like pattern** and have distinct roles:

- **Two legs labeled H** are used to **heat the sensing element**. These legs are connected via a **Nickel-Chromium (Ni-Cr) heating coil**. This alloy is chosen because it:
  - Conducts electricity efficiently.
  - Can withstand high temperatures without melting or degrading.

- The **remaining four legs** are labeled **A and B**, and are used to **carry electrical signals** from the sensing element to the external circuit. These are connected internally using **platinum wires**, because:
  - Platinum has excellent electrical conductivity.
  - It is highly sensitive to small changes in resistance, which occur when gas concentrations vary around the sensing material.


## Materials and Function of the Sensing Element

The sensing element inside the MQ2 sensor appears as a small **ceramic tube**. It is made from **Aluminum Oxide (Al₂O₃)** and coated with a thin layer of **Tin Dioxide (SnO₂)**.

<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
  <div style="flex: 1;">
    <img src="/assets/Courseimages/CircuitElectronicsImages/MQ2_Gas_Sensor/Sensing-Element-.png" alt="Materials and Function of the Sensing Element" style="width: 50%; height: 50%; object-fit: contain;">
  </div>
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
   structure of sensing element of mq2
</div>

- **Tin Dioxide (SnO₂)** is the active material responsible for detecting gases.
  - It reacts chemically with **flammable gases**.
  - This reaction changes the **electrical resistance**, which is then measured by the sensor.

- **Aluminum Oxide (Al₂O₃)** serves as the structural base:
  - It helps **distribute heat evenly** across the sensing surface.
  - It maintains the **optimal temperature** required for accurate gas detection.

### Summary of Key Components

| Component                         | Material/Function                                                        |
|----------------------------------|---------------------------------------------------------------------------|
| Outer Mesh (Anti-explosion net)  | Fine stainless steel mesh for protection and gas filtering               |
| Heating System                   | Nickel-Chromium coil wrapped around an Al₂O₃ ceramic tube                |
| Sensing System                   | Tin Dioxide (SnO₂) coating for gas sensitivity, connected via platinum wires |


## Internal design of MQ2 sensor

<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
  <div style="flex: 1;">
    <img src="/assets/Courseimages/CircuitElectronicsImages/MQ2_Gas_Sensor/6-module-mq-2-gas-sensor-internal-design-01.jpg" alt="Internal design of MQ2 sensor-schema" style="width: 50%; height: 50%; object-fit: contain;">
  </div>
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
   Internal design of MQ2 sensor-schema
</div>

## How Does a Gas Sensor Work?

When you power on an **MQ2 gas sensor**, it begins by **heating up its internal Tin Dioxide (SnO₂) layer** to a high operating temperature.

### Step-by-step Process:

#### 1. **Oxygen Adsorption:**
   - Oxygen molecules from the air **stick (adsorb)** to the surface of the SnO₂.
   - These oxygen molecules **capture free electrons** from the Tin Dioxide.
   - This process creates an **electron depletion region**, making the material **highly resistive** to current flow.

#### 2. **Gas Interaction:**
   - When **combustible gases** (like methane, LPG, etc.) enter the sensor, they **react with the adsorbed oxygen**.
   - This chemical reaction **releases the trapped electrons** back into the SnO₂.
   - As electrons return, the **resistance decreases**, and current can flow more easily.

#### 3. **Detection:**
   - The MQ2 sensor detects these **changes in resistance**.
   - More flammable gas → more reaction → more electrons returned → **lower resistance**.
   - A connected **microcontroller** (like Arduino or NodeMCU) reads this change and can estimate the **presence and concentration** of gas in the air.


<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
  <div style="flex: 1;">
    <img src="/assets/Courseimages/CircuitElectronicsImages/MQ2_Gas_Sensor/MQ2-Gas-Sensor-Working.gif" alt="Detection" style="width: 50%; height: 50%; object-fit: contain;">
  </div>
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
   process of Detection in mq2 gas sensor
</div>

### Summary:

| Stage                  | Description                                                  |
|------------------------|--------------------------------------------------------------|
| Heating                | SnO₂ is heated to activate its surface                       |
| Oxygen Adsorption      | Oxygen traps electrons, increasing resistance                |
| Gas Reaction           | Gas molecules release electrons by reacting with oxygen      |
| Resistance Change      | Resistance drops, current increases                          |
| Signal Detection       | Microcontroller reads voltage or analog signal change        |


## MQ2 Gas Sensor Module Hardware Overview

The **MQ2 gas sensor module** is simple to use and offers two types of outputs:

- **Analog Output (AO):** Represents the concentration of gas.
- **Digital Output (DO):** Indicates whether the gas concentration exceeds a preset threshold.

### Analog Output Behavior

- The **AO pin** outputs a voltage that **increases** with rising gas concentration.
- More gas → **higher voltage**
- Less gas → **lower voltage**

This analog voltage is fed to an **LM393 comparator**, which compares it to a **reference voltage** set by an onboard **potentiometer**.

### Digital Output Behavior

- If gas concentration is **above** the set threshold → `DO` pin goes **LOW**.
- If gas concentration is **below** the threshold → `DO` pin stays **HIGH**.



<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
  <div style="flex: 1;">
    <img src="/assets/Courseimages/CircuitElectronicsImages/MQ2_Gas_Sensor/MQ2-Gas-Sensor-Output.gif" alt="Digital Output Behavior" style="width: 50%; height: 50%; object-fit: contain;">
  </div>
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
   the behavior of mq2 gas sensor in diffrent output voltage
</div>

This digital signal can be used to **trigger alarms**, activate relays, or **send alerts** via a microcontroller.

## Sensitivity Adjustment

- The onboard **potentiometer** adjusts the sensitivity:
  - Turn **clockwise** → increase threshold (less sensitive)
  - Turn **counterclockwise** → decrease threshold (more sensitive)


<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
  <div style="flex: 1;">
    <img src="/assets/Courseimages/CircuitElectronicsImages/MQ2_Gas_Sensor/MQ2-Sensor-LM393-Comparator-with-Sensitivity-Adjustment-pot.jpg" alt="Sensitivity Adjustment" style="width: 50%; height: 50%; object-fit: contain;">
  </div>
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
   important component in front of mq2
</div>

## Indicator LEDs

- **Power LED:** Turns on when module is powered.
- **Status LED:** Turns on when gas level **exceeds threshold**.


<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
  <div style="flex: 1;">
    <img src="/assets/Courseimages/CircuitElectronicsImages/MQ2_Gas_Sensor/MQ2-Sensor-Power-and-Status-LEDs.jpg" alt="Indicator LEDs" style="width: 50%; height: 50%; object-fit: contain;">
  </div>
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
   Indicator LEDs on mq2
</div>

---

##  Technical Specifications

| Parameter               | Value                        |
|------------------------|------------------------------|
| Operating Voltage       | 5V                           |
| Load Resistance         | 20 KΩ                        |
| Heater Resistance       | 33 Ω ± 5%                    |
| Heating Consumption     | < 800 mW                     |
| Sensing Resistance      | 10 KΩ – 60 KΩ                |
| Detectable Range        | 200 – 10,000 ppm             |
| Preheat Time            | Over 24 hours (recommended)  |


## LM393 Comparator Circuit (Brief Overview)

The MQ2 module uses an **LM393 comparator** to convert the analog sensor signal into a digital output. It compares the analog voltage from the sensor with a reference voltage set by the onboard potentiometer.

When the sensor output exceeds the reference voltage, the comparator sends a **LOW signal** on the digital output (DO). Otherwise, it stays **HIGH**.

This setup enables threshold-based triggering.


<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
  <div style="flex: 1;">
    <img src="/assets/Courseimages/CircuitElectronicsImages/MQ2_Gas_Sensor/comp.png" alt="LM393 comparator circuit" style="width: 50%; height: 50%; object-fit: contain;">
  </div>
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
   LM393 comparator circuit
</div>


## MQ2 Gas Sensor Module Pinout

The **MQ2 gas sensor module** is easy to use and requires only **four pins** for connection:

---


<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
  <div style="flex: 1;">
    <img src="/assets/Courseimages/CircuitElectronicsImages/MQ2_Gas_Sensor/MQ2-Gas-Sensor-Module-Pinout-.jpg" alt="MQ2 Gas Sensor Module Pinout" style="width: 50%; height: 50%; object-fit: contain;">
  </div>
</div>
<div class="caption" style="text-align: center; margin-top: 8px;">
   MQ2 Gas Sensor Module Pinout
</div>


##  Pin Descriptions:

| Pin | Label | Description                                                                 |
|-----|-------|-----------------------------------------------------------------------------|
| 1   | VCC   | Power supply pin. Connect to **5V** on the Arduino or NodeMCU.              |
| 2   | GND   | Ground pin. Connect to the **GND** of your microcontroller.                 |
| 3   | AO    | **Analog Output**: Voltage varies with gas concentration. Connect to **A0**.|
| 4   | DO    | **Digital Output**: LOW when gas > threshold, HIGH otherwise. Connect to a **digital input** pin (e.g., D2). |

---

- The **AO (Analog Output)** pin outputs a voltage that **increases with gas concentration**.
- The **DO (Digital Output)** pin uses the **LM393 comparator** and **threshold set by the onboard potentiometer**.

>  Use **AO** for precise measurement and **DO** for triggering alerts when the concentration exceeds a set limit.


##  Calibrating the MQ2 Gas Sensor

The **MQ2 sensor** is a **heater-driven sensor**, and it requires a warm-up period before giving accurate readings.

###  Warm-up Guidelines:

- If your sensor **hasn’t been used for over a month**, warm it up for **24 to 48 hours** continuously.
- If your sensor **was used recently**, a warm-up time of **5 to 10 minutes** is enough.

>  **Note:** During the warm-up phase, the readings may be unstable or inaccurate. This is normal. As the internal heating element stabilizes, the readings will become more reliable.

---

Proper calibration helps ensure:
- More **accurate gas detection**
- **Stable analog output** during use
- Longer sensor **lifetime and reliability**


##  Experiment 1 – Measuring Gas Concentration using Analog Output (AO)

In this first experiment, we’ll learn how to measure the concentration of gas in the air using the **analog output (AO)** from the MQ2 gas sensor.

---

###  Wiring

Let’s begin by connecting the MQ2 gas sensor module to your Arduino:

| MQ2 Sensor Pin | Arduino Pin |
|----------------|-------------|
| VCC            | 5V          |
| GND            | GND         |
| AO             | A0          |

*Refer to the wiring diagram below for guidance.*  
*(Insert your wiring image here if available)*

---

###  Finding the Threshold Value

Before detecting gas presence, we need to determine two values:
1. Sensor reading in **clean air**
2. Sensor reading when **exposed to gas**

Upload the following code to your Arduino to view real-time sensor readings:

```cpp
#define MQ2pin 0

float sensorValue;  // variable to store sensor value

void setup() {
  Serial.begin(9600);  // initialize serial communication
  Serial.println("MQ2 warming up!");
  delay(20000);        // 20 seconds warm-up
}

void loop() {
  sensorValue = analogRead(MQ2pin);  // read from analog pin A0

  Serial.print("Sensor Value: ");
  Serial.println(sensorValue);

  delay(2000);  // 2 seconds delay
}
```



Example Values:
Clean air: ~100

Gas present: ~400

Repeat this test a few times for consistency. These numbers help set a threshold value for gas detection.



## Arduino Code with Threshold Detection
Update the code to trigger a message when gas is detected:


```python
#define Threshold 400
#define MQ2pin 0

float sensorValue;

void setup() {
  Serial.begin(9600);
  Serial.println("MQ2 warming up!");
  delay(20000);
}

void loop() {
  sensorValue = analogRead(MQ2pin);

  Serial.print("Sensor Value: ");
  Serial.print(sensorValue);

  if (sensorValue > Threshold) {
    Serial.print(" | Gas detected!");
  }

  Serial.println("");
  delay(2000);
}

```

Once uploaded, open the Serial Monitor. You’ll see messages like:

Sensor Value: 102
Sensor Value: 412 | Gas detected!


##  Experiment 2 – Detecting the Presence of Gas using Digital Output (DO)

In this second experiment, we’ll use the **digital output (DO)** from the MQ2 gas sensor to detect **whether gas is present** in the air.

---

###  Wiring

We’ll use the same wiring as before, but with one change:  
Disconnect the wire from **A0**, and instead connect the **DO (Digital Output)** pin to **digital pin 8** on the Arduino.

| MQ2 Sensor Pin | Arduino Pin |
|----------------|-------------|
| VCC            | 5V          |
| GND            | GND         |
| DO             | 8           |

 *Refer to the image below for wiring guidance.*  
*(Insert your image of the wiring setup here.)*

---

###  Setting the Threshold

The MQ2 module has a small **potentiometer** that lets you set the gas threshold:

- Turn the **potentiometer clockwise** to increase the threshold (less sensitive).
- Turn it **counterclockwise** to decrease the threshold (more sensitive).

**Steps to set it:**
1. Expose the sensor to your target gas.
2. Turn the potentiometer until the **Status LED turns ON**.
3. Slowly rotate it back until the LED **just turns OFF**.
>  You’ve now set the detection threshold!

---

###  Arduino Code for Digital Output

Upload the following sketch:

```cpp
#define MQ2pin 8

int sensorValue;  // variable to store digital reading

void setup() {
  Serial.begin(9600);
  Serial.println("MQ2 warming up!");
  delay(20000);  // allow MQ2 to warm up
}

void loop() {
  sensorValue = digitalRead(MQ2pin);  // read digital output

  Serial.print("Digital Output: ");
  Serial.print(sensorValue);

  if (sensorValue) {
    Serial.println("  |  Gas: -");  // No gas
  } else {
    Serial.println("  |  Gas: Detected!");  // Gas present
  }

  delay(2000);  // 2s delay between readings
}
```


 What You'll See:
Once the sketch is running and the Serial Monitor is open, you’ll observe messages like:

Digital Output: 1  |  Gas: -
Digital Output: 0  |  Gas: Detected!


##  Applications of MQ2 Gas Sensor

The MQ2 gas sensor is widely used in various safety and automation systems due to its sensitivity to combustible gases and smoke. Here are some real-world applications:

-  **Home Safety Systems**: Detecting gas leaks (LPG, methane) in kitchens or basements to prevent accidents.
-  **Smoke Detection**: Identifying smoke in early stages of fire for triggering alarms.
-  **Automotive Systems**: Monitoring air quality inside vehicles or detecting fuel vapors.
-  **Industrial Safety**: Monitoring leakage of gases in factories and workshops.
-  **Science Experiments**: Teaching students about gas sensors, electronics, and environmental monitoring.

Its combination of analog and digital outputs makes it useful for both **quantitative** measurements (how much gas?) and **qualitative** decisions (gas present or not).

---

## References

<a href="https://lastminuteengineers.com/mq2-gas-senser-arduino-tutorial/" style="text-decoration:underline; color:green;" target="_blank"><strong>MQ2 Gas Sensor Arduino Tutorial – Last Minute Engineers</strong></a>

<a href="https://www.ti.com/product/LM393" style="text-decoration:underline; color:green;" target="_blank"><strong>LM393 Comparator Datasheet – Texas Instruments</strong></a>

<a href="https://www.theengineeringprojects.com/2023/06/how-to-interface-mq-2-gas-sensor-with-raspberry-pi-4.html" style="text-decoration:underline; color:green;" target="_blank"><strong>How to Interface MQ-2 Gas Sensor with Raspberry Pi 4 – The Engineering Projects</strong></a>

<a href="https://www.renkeer.com/gas-sensors-types-working-principles/" style="text-decoration:underline; color:green;" target="_blank"><strong>Gas Sensors: Types and Working Principles – Renkeer</strong></a>




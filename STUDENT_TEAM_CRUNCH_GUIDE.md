# Student & Teacher Discussion Guide: Understanding Your WiFi CSI Thesis Options

> **Who this guide is for:** You, your undergraduate teammate, and your thesis advisor.  
> **Goal:** Break down all the technical research into simple, plain English so you can understand what was built, discuss it with your teammate, and pitch it with confidence to your professor.

---

## Table of Contents
1. [The 60-Second Primer: What is WiFi CSI Sensing?](#1-the-60-second-primer-what-is-wifi-csi-sensing)
2. [What Was Wrong With the Initial Idea? (Why We Fixed It)](#2-what-was-wrong-with-the-initial-idea-why-we-fixed-it)
3. [The 5 Thesis Options (The Menu)](#3-the-5-thesis-options-the-menu)
   - [Option 1: The AI Foundation Model Track](#option-1-the-ai-foundation-model-track)
   - [Option 2: The Crowded Room / Multi-Person Track](#option-2-the-crowded-room--multi-person-track)
   - [Option 3: The Elderly Fall Safety & Digital Health Track](#option-3-the-elderly-fall-safety--digital-health-track)
   - [Option 4: The Smart Home Security & Gait Biometrics Track](#option-4-the-smart-home-security--gait-biometrics-track)
   - [Option 5: The $5 Microcontroller / Edge Hardware Track](#option-5-the-5-microcontroller--edge-hardware-track)
4. [The Multiplied Master Option (Synthesizing All 5)](#4-the-multiplied-master-option-synthesizing-all-5)
5. [Step-by-Step Meeting Script for Your Professor](#5-step-by-step-meeting-script-for-your-professor)
6. [Decision Checklist for You and Your Teammate](#6-decision-checklist-for-you-and-your-teammate)
7. [Plain-English Glossary (Cheat Sheet)](#7-plain-english-glossary-cheat-sheet)

---

## 1. The 60-Second Primer: What is WiFi CSI Sensing?

Imagine you stand in a dark room and clap your hands. The sound bounces off the walls, the furniture, and any people in the room. If someone walks across the room, the echo changes slightly.

**WiFi Channel State Information (CSI)** is essentially the exact same thing, but with **radio waves instead of sound**:
- Every time your WiFi router talks to your laptop or phone, it sends radio signals divided into dozens of frequencies (called *subcarriers*).
- These radio waves bounce off walls, tables, and the human body.
- When a person walks, falls, or breathes, their body movements disturb the radio waves.
- The WiFi chip captures these tiny disturbances as numbers (amplitude = signal strength; phase = time delay). These numbers are called **CSI**.
- By feeding these numbers to machine learning models, we can detect **what people are doing without any cameras or wearable sensors**.

### Why is this huge?
- **Privacy:** No cameras in bedrooms, bathrooms, or nursing homes.
- **Convenience:** Elderly people don't need to remember to wear or recharge a smartwatch.
- **Cheap:** Uses standard WiFi equipment already installed in houses.

---

## 2. What Was Wrong With the Initial Idea? (Why We Fixed It)

When students first start, they often propose ideas that sound amazing in sci-fi movies, but fail basic physics. Here are the 4 big traps we identified and fixed so your paper is publishable:

### Trap 1: "Identifying people by their heartbeat through WiFi"
- **The Physics Problem:** A human heartbeat moves the chest by roughly **0.5 millimeters**. Normal breathing moves the chest by **5 millimeters** (10 times bigger!). Walking moves the body by **1,000 millimeters**.
- Trying to identify *who* someone is based on their heartbeat using a standard $20 WiFi router through walls is like trying to hear a pocket watch ticking inside a stadium during a football game.
- **The Fix:** We dropped passive heartbeat biometric identification. Instead, we identify occupants by **how they walk (gait)**, which produces massive, unmistakable signal changes.

### Trap 2: "If breathing is detected, the elderly person is safe"
- **The Medical Safety Problem:** Suppose an elderly person suffers a terrible fall, breaks their hip, or suffers a concussion and is paralyzed on the floor. **Are they still breathing? Yes!**
- If an algorithm says *"We detected breathing, so cancel the ambulance alert!"*, the injured person is left on the floor for hours.
- **The Fix:** We established a strict medical rule: **Breathing confirms that a person is resting quietly during normal times, but breathing is NEVER allowed to cancel a fall alert.**

### Trap 3: "Intruder detection using standard classifiers"
- **The AI Problem:** Standard AI models (like typical image classifiers) assume every input belongs to one of their trained categories. If you train it on Dad, Mom, and Child, and a burglar enters, the AI will confidently guess *"That burglar is 87% Dad!"*.
- **The Fix:** We use **Open-Set Recognition**. If the person walking doesn't match the family's known walking profile, the system labels them as **"Unknown Person"**.

### Trap 4: The 95% Accuracy Illusion (Data Leakage)
- **The Academic Scandal in this field:** Many published papers claim "98% accuracy". But they cheated (often accidentally). They recorded someone in a room for 10 minutes, sliced the recording into 1-second snippets, and randomly shuffled them into training and testing sets.
- The AI didn't learn human movement—it just memorized the exact reflections of the furniture! When tested in a new room, accuracy collapsed to 60%.
- **The Fix:** We enforce strict **Zero-Leakage Rules**: test the model in completely different rooms on completely different people who were never seen during training.

---

## 3. The 5 Thesis Options (The Menu)

You do **not** have to do all 5. Think of this as a restaurant menu. You and your teacher can pick **one favorite track**, or combine two, or take the whole system.

```
                           THE 5 THESIS OPTIONS
  ┌──────────────────────────────────────────────────────────────────────┐
  │ Option 1: AI Foundation Model (Teach AI general WiFi physics)        │
  ├──────────────────────────────────────────────────────────────────────┤
  │ Option 2: Multi-Person Sensing (De-clutter crowded rooms)            │
  ├──────────────────────────────────────────────────────────────────────┤
  │ Option 3: Healthcare & Fall Safety (Elderly care & breathing FSM)    │
  ├──────────────────────────────────────────────────────────────────────┤
  │ Option 4: Smart Home Security (Recognizing family members by gait)   │
  ├──────────────────────────────────────────────────────────────────────┤
  │ Option 5: TinyML Edge Hardware (Running on $5 ESP32 microchips)      │
  └──────────────────────────────────────────────────────────────────────┘
```

---

### Option 1: The AI Foundation Model Track
- **One-Sentence Pitch:** *"Build a large self-supervised neural network that understands WiFi signal physics so well that it works in any room without retraining."*
- **The Problem:** AI trained in Living Room A fails completely when moved to Living Room B.
- **The Solution:** We train a model using Masked Autoencoding (like BERT/ChatGPT, but for radio waves). It masks out parts of the WiFi signal and learns to fill in the blanks, learning general physical velocity features that don't depend on room shape.
- **Best If Your Professor:** Specializes in Machine Learning, Deep Learning, or Computer Vision.
- **Difficulty for You:** Medium to Hard (requires GPU training time).
- **File in repo:** `thesis_candidates/candidate_1_foundation_models.md`.

---

### Option 2: The Crowded Room / Multi-Person Track
- **One-Sentence Pitch:** *"Separate and track multiple people moving in the same room at the same time using blind source separation."*
- **The Problem:** 95% of existing research only works when one solitary person is in the room. As soon as a second person or pet enters, the signals scramble and the AI breaks.
- **The Solution:** Use mathematical tensor decomposition and modern set-prediction attention (Hungarian matching) to separate the tangled radio echoes into distinct individual human trajectories.
- **Best If Your Professor:** Specializes in Wireless Networks, Mobile Computing, or Signal Processing.
- **Difficulty for You:** Medium (great public dataset called WiMANS from ECCV 2024 is ready to use).
- **File in repo:** `thesis_candidates/candidate_2_multi_user_decomposition.md`.

---

### Option 3: The Elderly Fall Safety & Digital Health Track
- **One-Sentence Pitch:** *"A contactless elderly care system that detects falls instantly, tracks sleep breathing, and eliminates false alarms during quiet sitting."*
- **The Problem:** If an elderly person sits still to read, motion sensors think they left the house. But if they fall, normal systems either miss the fall or get confused.
- **The Solution:** We built a **5-State Finite State Machine (FSM)**:
  1. *Unknown* (signal too noisy)
  2. *Vacant* (room is empty)
  3. *Active* (person walking/cooking)
  4. *Stationary* (person sitting/sleeping; breathing verified)
  5. *Emergency Alert* (fall detected; CANNOT be turned off by breathing).
- **Best If Your Professor:** Specializes in Healthcare IoT, Pervasive Systems, or Cyber-Physical Systems.
- **Difficulty for You:** Easy to Medium (clean datasets exist, logic is very intuitive and easy to present).
- **File in repo:** `thesis_candidates/candidate_3_vital_signs_fall_safety.md`.

---

### Option 4: The Smart Home Security & Gait Biometrics Track
- **One-Sentence Pitch:** *"Authenticate registered family members and reject intruders strictly by analyzing how they walk."*
- **The Problem:** Optical cameras invade privacy; smart locks require keys; WiFi heartbeat biometrics are physically impossible.
- **The Solution:** We use **Metric Learning (ArcFace)** on walking kinematics. Each family member gets a unique mathematical walking signature. When someone walks past the router, the system measures their walking distance. If they don't match any family member, it flags them as an **"Unknown Visitor"**.
- **Best If Your Professor:** Specializes in Cybersecurity, Privacy, or Biometrics.
- **Difficulty for You:** Easy (standard PyTorch code, well-defined accuracy metrics like ROC curves).
- **File in repo:** `thesis_candidates/candidate_4_open_set_biometrics.md`.

---

### Option 5: The $5 Microcontroller / Edge Hardware Track
- **One-Sentence Pitch:** *"Compress the entire WiFi AI model so it runs locally on a cheap $5 ESP32 microcontroller in real-time without cloud servers."*
- **The Problem:** Most research requires a $3,000 gaming PC or sends raw radio data to the cloud, creating huge privacy risks.
- **The Solution:** We convert the neural network to **INT8 (8-bit integers)**. This shrinks the model memory by 75% down to **69.8 KB**, which fits easily into the 512 KB memory of a tiny ESP32 chip and runs at **24 decisions per second**.
- **Best If Your Professor:** Specializes in Embedded Systems, IoT, TinyML, or Computer Architecture.
- **Difficulty for You:** Easy to Medium (our Python profiling scripts are already built and proven in `scripts/profile_edge_tinyml.py`).
- **File in repo:** `thesis_candidates/candidate_5_tinyml_edge_execution.md`.

---

## 4. The Multiplied Master Option (Synthesizing All 5)

If you want an exceptional, publication-grade undergraduate thesis that stands out, you can present **The Unified Architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 4: SAFETY STATE MACHINE (Option 3)                   │
│  5-State logic: Never cancels fall alarms on breathing.     │
├─────────────────────────────────────────────────────────────┤
│  LAYER 3: TASK ENCODERS (Options 3 & 4)                     │
│  Branch A: Walking Gait Biometrics (Family vs Stranger)     │
│  Branch B: Vital Signs & Fall Impact Detector               │
├─────────────────────────────────────────────────────────────┤
│  LAYER 2: MULTI-PERSON FILTER (Option 2)                    │
│  Separates multiple people into distinct streams.           │
├─────────────────────────────────────────────────────────────┤
│  LAYER 1: PHYSICS VELOCITY BACKBONE (Option 1)              │
│  Extracts room-independent Doppler movement.                │
├─────────────────────────────────────────────────────────────┤
│  LAYER 0: INT8 EMBEDDED ENGINE (Option 5)                   │
│  Runs in 69 KB of RAM on a $5 ESP32 microcontroller.        │
└─────────────────────────────────────────────────────────────┘
```

**Why this is great:** Each student in a 2-person team can own specific layers!
- **Student A** owns the **Signal Processing & Hardware** (Layers 0, 1, 2).
- **Student B** owns the **AI Models, Safety State Machine & Applications** (Layers 3, 4).

---

## 5. Step-by-Step Meeting Script for Your Professor

Here is exactly what you and your teammate should say in your supervisory meeting:

### Phase 1: The Opening (Show You Did Serious Homework)
> *"Professor, we have spent time auditing 93 recent research papers and datasets in WiFi Channel State Information (CSI) sensing.*  
> *We realized that a lot of initial project ideas in this space suffer from unrealistic assumptions—like trying to detect heartbeats through walls on standard routers, or assuming a room only ever has one person.*  
> *To make sure our thesis is scientifically sound and actually publishable, we developed five concrete research tracks, plus a unified architecture that connects them."*

### Phase 2: Handing Over the Options (The Menu)
> *"We have broken down our research into five specific directions:*
> 1. *A **Self-Supervised Foundation Model** that solves environmental domain shift across rooms.*
> 2. *A **Multi-User Decomposition** model that handles multiple people moving in the same room using the new WiMANS dataset.*
> 3. *An **Elderly Care & Fall Safety** framework using a 5-State Machine where breathing prevents false alarms during rest, but is strictly prohibited from cancelling fall alerts.*
> 4. *An **Open-Set Gait Verification** system that identifies registered family members and rejects strangers without cameras.*
> 5. *An **Embedded TinyML** implementation running quantized neural networks on a $5 ESP32 chip in under 42 milliseconds.*
> 
> *We also designed a unified architecture that stacks these layers together."*

### Phase 3: The Closing Ask (Let the Teacher Decide!)
> *"We want to align our final focus with your lab's strengths and publication goals. Which of these five tracks—or what combination of them—would you recommend we focus on for our final implementation?"*

---

## 6. Decision Checklist for You and Your Teammate

Before meeting your teacher, sit down with your teammate and answer these 4 questions:

1. **What kind of lab is your supervisor in?**
   - Deep Learning / AI? $\rightarrow$ Favor **Option 1** or **Option 4**.
   - Networks / IoT / Mobile Systems? $\rightarrow$ Favor **Option 2** or **Option 3**.
   - Embedded Systems / Hardware? $\rightarrow$ Favor **Option 5**.

2. **What computing hardware do you have?**
   - No GPUs, just laptops? $\rightarrow$ Choose **Option 3**, **Option 4**, or **Option 5**.
   - Access to university GPU servers? $\rightarrow$ Choose **Option 1** or **Option 2**.

3. **How do you want to split the work between the two of you?**
   - *Person 1 (AI & Software):* Data loading, neural network training, evaluation metrics.
   - *Person 2 (Systems & Theory):* Signal filtering, state machine logic, edge microcontroller profiling.

4. **Do you prefer a physical hardware demo?**
   - If yes: **Option 5** (ESP32 running in real time) is an unbeatable live demonstration for exam committees.

---

## 7. Plain-English Glossary (Cheat Sheet)

Keep this cheat sheet handy so you never get confused by the terminology:

| Term | What it actually means in plain English |
| :--- | :--- |
| **CSI (Channel State Information)** | Numerical measurements of how WiFi radio waves bounce off objects and people between transmitter and receiver. |
| **Subcarriers** | Modern WiFi divides its channel into 30 to 240 sub-frequencies. Each subcarrier reflects off the room slightly differently. |
| **Multipath** | Radio waves bouncing off walls, floors, and furniture. This creates the "echo" profile of a specific room. |
| **Doppler Effect** | The frequency shift that happens when a radio wave bounces off a moving body (like the pitch change of a passing police siren). |
| **CSI Ratio ($\mathcal{R} = H_1 / H_2$)** | Dividing the signal from Antenna 1 by Antenna 2. Because both antennas share the same internal clock, clock jitter cancels out completely. |
| **LOSO (Leave-One-Subject-Out)** | Testing the AI on a person whose data was completely withheld during training, proving it doesn't just memorize one person's body shape. |
| **LOEO (Leave-One-Environment-Out)** | Testing the AI in a completely new room that was never seen during training, proving it works in any house. |
| **INT8 Quantization** | Converting large 32-bit floating-point numbers into 8-bit integers (-128 to 127). Shrinks model memory by 75% with almost zero accuracy loss. |
| **FSM (Finite State Machine)** | A rule-based flowchart (e.g. Empty $\rightarrow$ Walking $\rightarrow$ Sitting $\rightarrow$ Fall Alarm) that prevents silly mistakes. |
| **ArcFace / Metric Learning** | Training AI to pull members of the same family close together in mathematical space while pushing strangers far away. |
| **Blind Source Separation (BSS)** | Mathematical un-mixing: separating mixed audio (or WiFi echoes) from multiple people back into clean individual signals. |

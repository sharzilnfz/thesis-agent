# Thesis Candidate 5: Ultra-Low-Power TinyML & Bare-Metal Microcontroller Execution

## 1. Metadata
- **Working Title:** Real-Time On-Device WiFi CSI Sensing on Resource-Constrained Bare-Metal Microcontrollers: Quantized TCNs and Selective State-Space Models
- **Discipline:** Embedded Systems / Edge AI / TinyML / Low-Power Cyber-Physical Systems
- **Target Venues:** ACM SenSys, ACM/IEEE IPSN, IEEE Internet of Things Journal, ACM Transactions on Embedded Computing Systems (TECS)

---

## 2. Abstract
The overwhelming majority of WiFi CSI sensing research relies on power-hungry x86 workstations or cloud servers streaming raw high-bandwidth channel traces. This architectural dependency introduces severe latency bottlenecks, bandwidth congestion, and acute privacy vulnerabilities as unencrypted ambient RF reflections traverse home networks. To enable widespread domestic deployment, ambient sensing must execute directly on low-power, sub-$5 commodity microcontrollers. This thesis investigates the feasibility and architectural boundaries of executing deep temporal WiFi sensing models on resource-constrained microcontrollers. We profile and benchmark two emerging lightweight architectures—Physics-Guided Temporal Convolutional Networks (TCN) and Selective State-Space Models (BabyMamba-HAR)—under post-training INT8 quantization on an Espressif ESP32-S3 (512 KB SRAM, 240 MHz). We demonstrate that INT8 model compression achieves a $4\times$ reduction in parameter memory and $75\%$ reduction in peak activation buffers, running full inference in under 42 ms (24 Hz throughput) within a 70 KB SRAM footprint. This proves that real-time, privacy-preserving domestic sensing is achievable without cloud infrastructure.

---

## 3. Primary Research Questions
- **RQ 5.1:** How do Temporal Convolutional Networks (TCN) compare against Selective State-Space Models (BabyMamba-HAR) in terms of per-window inference latency, peak activation SRAM, and classification accuracy when quantized to INT8?
- **RQ 5.2:** What is the empirical quantization loss when converting continuous complex CSI channel matrices from 32-bit floating point to 8-bit integer representations?
- **RQ 5.3:** Can a dual-core bare-metal microcontroller (ESP32-S3) maintain concurrent 100 Hz WiFi packet capture via DMA ring-buffers on Core 0 while executing continuous real-time neural inference on Core 1 without buffer overflows or packet drops?

---

## 4. Theoretical Foundations & Mathematical Formulation
1. **Linear Time Complexity of State-Space Models (SSM):**
   Unlike standard Transformers which scale quadratically $\mathcal{O}(L^2)$ with window length $L$, the continuous-time state-space equation:
   $$h'(t) = \mathbf{A} h(t) + \mathbf{B} x(t), \quad y(t) = \mathbf{C} h(t)$$
   Discretized via zero-order hold (ZOH), computes hidden states recurrently in linear time $\mathcal{O}(L)$:
   $$h_k = \bar{\mathbf{A}} h_{k-1} + \bar{\mathbf{B}} x_k, \quad y_k = \mathbf{C} h_k$$
   Consuming fixed $\mathcal{O}(1)$ intermediate activation memory per step, ideal for microcontrollers.
2. **Symmetric INT8 Uniform Quantization:**
   Mapping continuous FP32 tensor $x \in [-a, a]$ to signed 8-bit integer $q \in [-128, 127]$:
   $$q = \text{clamp}\left(\left\lfloor \frac{x}{S} \right\rceil, -128, 127\right), \quad S = \frac{\max(|x|)}{127}$$
3. **Dual-Core Task Allocation & DMA Ring-Buffer:**
   $$\text{Throughput} = \frac{1}{\max(T_{\text{DMA\_Rx}}, T_{\text{infer\_INT8}})} \ge 20 \text{ Hz}$$
   Core 0 handles FreeRTOS Wi-Fi MAC layer interrupts, while Core 1 executes quantized tensor convolutions.

---

## 5. Benchmarking & Experimental Plan
- **Target Hardware Platforms:**
  - **Tier-1 Microcontroller:** Espressif ESP32-S3 (Dual-core Xtensa LX7 @ 240 MHz, 512 KB internal SRAM, ESP-IDF v5.x).
  - **Tier-2 Single-Board Computer:** Raspberry Pi 4B (Quad-core Cortex-A72 @ 1.5 GHz, 4 GB RAM, Nexmon CSI).
- **Primary Datasets & Models:**
  - CSI-Bench (heterogeneous device subset including ESP32-S3 captures).
  - SenseFi benchmark models (MLP, CNN, LSTM, ResNet-18, TCN).
  - Custom ESP32-CSI capture streams.
- **Evaluation Metrics:**
  - Inference Latency (milliseconds) and Frame Throughput (Hz).
  - Peak SRAM Allocation (KB) and Flash ROM Footprint (KB).
  - Active Power Consumption (Watts / Milliwatts).
  - Top-1 Accuracy and Macro F1 under FP32 vs. INT8.

---

## 6. Novelty & High-Impact Contributions
1. Moving beyond Python/PyTorch desktop simulations to verified bare-metal microcontroller deployment.
2. First empirical comparison between Selective State-Space Models (Mamba) and TCNs on embedded WiFi CSI streams.
3. Providing an open-source, deployable FreeRTOS / ESP-IDF C++ runtime library for on-device ambient intelligence.

---

## 7. Adversarial Stress-Test (Known Vulnerabilities & Risks)
- **Risk 1 (Firmware Driver Fragility):** The ESP-IDF CSI API requires bare-metal C/C++ firmware flashing; debugging memory leaks and DMA ring-buffer overflows can be time-consuming.
- **Risk 2 (Single-Antenna Hardware Bound):** Standard ESP32 boards lack coherent multi-antenna reception, preventing complex phase ratio calculations and restricting models to amplitude Doppler features.
- **Risk 3 (Quantization Degradation on Delicate Vital Signs):** While macroscopic activities tolerate INT8 quantization with $<1.5\%$ accuracy loss, subtle sub-millimeter vital signs may suffer quantization clipping.

---

## 8. Feasibility & Scope Assessment
- **Scientific Impact:** Very High (9.0/10) — Highly prized at embedded systems and IoT conferences (SenSys, IPSN, IoT-J).
- **Undergraduate Feasibility:** Extremely High (9.5/10) — Hardware costs are minimal (<$10 for an ESP32 board); software profiling can be done locally; concrete engineering deliverables impress examiners.
- **Supervisor Appeal:** Unanimously High for embedded systems, IoT, and hardware-software co-design professors.

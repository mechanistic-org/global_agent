---
title: FMEA Matrix for test_desk_hardware
date: '2026-04-05'
context_node: fmea
---

## Deterministic Physics Vault (FMEA Analysis)

> **Note:** RPN (Risk Priority Number) is calculated explicitly as $Severity \times Occurrence \times Detection$ within the Python constraint boundary, overriding any LLM hallucinations.

| Subsystem | Failure Mode | Physics Description | S | O | D | RPN (Fixed) | Critical Blocker | Status | Mitigation | Knock-On Effects |
|---|---|---|---|---|---|---|---|---|---|---|
| Motor Actuator | Worm Gear Stripping | The primary worm gear fails under heavy dynamic load, leading to catastrophic collapse of the desk. | 10 | 5 | 2 | **100** | Yes | CRITICAL | Implement redundant gear design and higher material strength. | Severe pinch hazard to users. |
| Motor Actuator | CAN Bus Data Line Disconnection | The CAN bus data line loses structural connection due to vibration, causing the desk to freeze in place. | 3 | 7 | 4 | **84** | No | MARGINAL | Use vibration-resistant connectors and shielded cables. | Desk remains stationary, user frustration. |
| Motor Actuator | Thermal Throttling | The motor housing experiences thermal throttling during rigorous continuous up/down testing, leading to a slight degradation of lifespan over years of heavy use. | 4 | 6 | 5 | **120** | No | MARGINAL | Enhance heat dissipation through improved cooling solutions. | Reduced motor lifespan over time. |
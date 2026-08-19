# Research Roadmap

## Phase 1 — Baseline materials and device physics

- Define the exact ZnO/perovskite/ZnO stack, contacts, substrate, and encapsulation.
- Measure optical absorption and establish a zero-bias photovoltaic baseline.
- Characterize morphology/crystallinity and interface quality.
- Establish repeatable device-to-device statistics.

**Exit criterion:** reproducible zero-bias photoresponse with documented uncertainty and stability.

## Phase 2 — Piezoelectric modulation

- Build a calibrated mechanical test fixture.
- Map response versus tensile/compressive strain and bending radius.
- Test polarity/orientation dependence.
- Fit the reduced-order piezoelectric interface coefficient.

**Exit criterion:** reversible strain-dependent modulation that exceeds measurement drift and control-device artifacts.

## Phase 3 — Pyroelectric transients

- Add synchronized temperature sensing.
- Sweep light modulation frequency and controlled thermal ramp rate.
- Fit thermal time constant and effective pyroelectric coefficient.
- Separate pyroelectric signatures from thermoelectric/contact effects.

**Exit criterion:** current transients scale reproducibly with `dT/dt` under suitable controls.

## Phase 4 — Coupling mechanism

- Execute factorial strain × thermal-rate experiments.
- Predict coupled response from independently fitted piezo/pyro parameters.
- Quantify residual interaction and uncertainty.
- Introduce nonlinear coupling terms only if statistically and physically justified.

**Exit criterion:** a validated mechanism model that explains held-out coupled-condition data.

## Phase 5 — Device optimization

Explore layer thickness, ZnO morphology/orientation, perovskite composition, interfaces, electrodes, active area, encapsulation, and mechanical neutral-axis design. Multi-objective optimization should consider responsivity, noise, speed, flexibility, stability, and fabrication yield rather than maximizing one headline metric.

## Phase 6 — Cyber-physical integration

- Build the detector/readout/ADC interface and define a timestamped sensor data model.
- Calibrate edge filtering and state-estimation thresholds from measured noise and operating envelopes.
- Compare periodic versus event-triggered communication.
- Quantify end-to-end latency from physical stimulus to cyber decision.
- Inject packet loss, sensor drift, missing samples, and communication outages.
- Propagate detector uncertainty into decision confidence.

**Exit criterion:** reproducible closed-loop sensing-to-decision behavior under documented physical and network disturbances.

## Phase 7 — Hardware-in-the-loop and resilience

- Replace simulated detector streams with real-time measurements.
- Keep the same CPS interfaces so simulation and hardware runs are directly comparable.
- Add actuator or adaptive sensing behavior.
- Evaluate fault detection and safe degraded modes.
- Add security experiments such as replay/spoofing only with explicit threat models and measurable defenses.

**Exit criterion:** a hardware-in-the-loop CPS demonstrator with traceable physical, computation, communication, and response metrics.

## Phase 8 — Application demonstrators

Candidate demonstrations:

- wearable optical pulse/PPG-style sensing with motion/thermal context;
- battery-free or energy-aware event/light sensing for IoT nodes;
- flexible optical touch/gesture or human–machine interaction interface;
- environmental exposure node with adaptive communication;
- safety-aware flexible sensor that triggers protective or warning actions.

Application claims should be based on system-level tests under realistic motion, lighting, temperature, network, power, and aging conditions.

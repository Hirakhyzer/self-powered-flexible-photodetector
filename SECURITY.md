# Security Policy

## Scope

This repository is a research simulation scaffold. Security concerns may include dependency issues, unsafe file/config parsing, CI workflow risks, accidental secret exposure, or vulnerabilities in the CPS simulation software.

The repository is **not** a validated controller for deployed hardware, medical devices, industrial systems, or safety-critical infrastructure.

## Reporting a vulnerability

Please do not publish sensitive exploit details in a public issue. Use GitHub private vulnerability reporting if it is enabled for this repository. If it is not available, contact the repository maintainer privately through their GitHub profile before disclosing technical details publicly.

When reporting, include the affected commit, file/module, impact, minimal reproduction, and any suggested mitigation.

## Safety boundary

Do not treat simulation thresholds, actuator commands, network policies, or detector logic in this repository as deployment-ready safety or security controls. Any real-world use requires independent validation, threat modeling, hardware testing, and domain-specific safety review.

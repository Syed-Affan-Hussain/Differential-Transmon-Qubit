# Differential Transmon with CPW

## Overview
This repository contains a Qiskit Metal implementation of a differential transmon qubit with coplanar waveguide (CPW) connections based on the research paper "Surface loss calculations and design of a superconducting transmon qubit with tapered wiring". The design is integrated with Ansys HFSS for eigenmode and energy participation ratio (EPR) analyses.



## Requirements
To use this project, install the required dependencies:

```bash
pip install qiskit-metal numpy matplotlib
```

For HFSS integration, please make sure Ansys HFSS is installed and properly configured.


There are some mesh convergence issues while running the Analysis, which will be corrected in the near future.


### **Eigenmode Analysis Summary**

| **Parameter**               | **Value/Status**                     | **Notes**                                                                 |
|-----------------------------|--------------------------------------|---------------------------------------------------------------------------|
| **Eigenfrequency (HFSS)**   | 4.11 GHz                             | Mode 0 resonance frequency.                                               |
| **Eigenfrequency (ND)**     | 3975.11 MHz                          | Numerical diagonalization result.                                         |
| **Energy in Substrate**     | 91.3%                                | Dominates due to dielectric layers.                                       |
| **Magnetic Energy**         | 2.1% of total electric energy        | Low, as expected for transmon qubits.                                     |
| **Anharmonicity (Kerr, χ)** | 139 MHz                              | Moderate non-linearity; suitable for transmons.                           |
| **Energy Imbalance**        | (ℰ_E-ℰ_H)/ℰ_E = -97.29%              | Convergence issue .                                                       |
| **Convergence Status**      | Failed                               | `U_tot_cap-U_tot_ind` imbalance >15% (critical issue ).                   |

---

### **Critical Anamolies**
1. **Mesh Convergence**: Poor resolution at inductive regions (junction/wires).  
2. **Boundary Conditions**: Radiation boundaries likely missing.  

---

## License
This project is open-source and available under the MIT License.


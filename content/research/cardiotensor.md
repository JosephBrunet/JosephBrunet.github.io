---
title: "Cardiotensor"
subtitle: "A Python Library for Orientation Analysis and Tractography in 3D Cardiac Imaging"
description: "Open-source package for quantifying cardiomyocyte orientation and tractography in large-scale 3D cardiac imaging datasets"
tags: ["Cardiac Imaging", "Python", "Structure Tensor", "Tractography", "HiP-CT"]
date: 2025-08-10
cover:
  image: "/assets/images/cardiotensor/cardiotensor-cover.jpg"
showToc: false
---

<div class="categories">
  <div class="option-tag"><i class="fas fa-code"></i> Python Library</div>
  <div class="option-tag"><i class="fas fa-project-diagram"></i> Tractography</div>
  <div class="option-tag"><i class="fas fa-dna"></i> Myocyte Orientation</div>
</div>

<br>


**<a href="https://github.com/JosephBrunet/cardiotensor/tree/main" target="_blank" class="text-link">Cardiotensor</a>**
( [![GitHub release](https://img.shields.io/github/v/release/JosephBrunet/cardiotensor)](https://github.com/JosephBrunet/cardiotensor/releases) )
is an open-source Python package developed to quantify **3D cardiomyocyte orientation** and reconstruct continuous **tractography** of myoaggregates in volumetric cardiac imaging datasets.  


The library is designed for modern **high-resolution modalities** such as **synchrotron tomography (HiP-CT)**, micro-CT, and 3D optical imaging. It supports datasets up to **teravoxel scale** through chunk-based and parallelized processing pipelines.  

<div>
  <img src="/assets/images/cardiotensor/pipeline.jpg" alt="Cardiotensor workflow for 3D orientation analysis">
  <p class="img-legend">Cardiotensor workflow: orientation computation with structure tensor, helical angle (HA) and intrusion angle (IA) mapping, and streamline-based tractography</p>
</div>


### Key Features
- **3D Structure Tensor Analysis**: Computes voxel-wise cardiomyocyte orientation from image intensity gradients.  
- **Cardiac Microstructure Metrics**: Extracts helical angle (HA), intrusion angle (IA), and fractional anisotropy (FA).  
- **Tractography**: Reconstructs cardiomyocyte trajectories for continuous myoaggregate mapping.  
- **Scalable Processing**: Optimized for HPC clusters and terabyte-sized volumes using chunked parallelization.  
- **Visualization**: Interactive 3D rendering of vector fields and streamlines, plus VTK export for ParaView.  
- **Tissue-Agnostic**: Applicable beyond the heart to other fibrous tissues such as brain white matter, skeletal muscle, and tendon.  

<div class="small-img-block">
  <img src="/assets/images/cardiotensor/tractography.jpg" alt="Cardiotensor streamline tractography">
  <p class="img-legend">Streamline tractography of cardiomyocyte orientation, color-coded by helical angle (HA)</p>
</div>

### Why Cardiotensor?
Most established orientation-analysis tools (e.g., MRtrix3, DIPY, DSI Studio) were developed for diffusion MRI. **Cardiotensor** instead derives orientation directly from imaging intensity gradients, enabling analysis across modalities such as synchrotron tomography, micro-CT, and optical microscopy. Unlike small-scale in-house codes, it is designed to be **scalable, reproducible, and openly accessible**.  

### Documentation and Availability
📖 Full documentation, tutorials, and example datasets are available at:  
[https://josephbrunet.github.io/cardiotensor](https://josephbrunet.github.io/cardiotensor)  

Install via pip:  
```bash
pip install cardiotensor
```

### Acknowledgement
📄 For full details, see the <a href="
https://doi.org/10.48550/arXiv.2508.07476" target="_blank" class="text-link">preprint paper</a> (2025).

---
layout: page
title: research
permalink: /research/
description: Research themes in computational materials chemistry.
nav: true
nav_order: 1
toc:
  sidebar: left
---

## Research philosophy

My work starts from a simple premise: in many energy materials, the property we care about is controlled by a **minority local configuration** — a charged defect, a trapped carrier, a migration bottleneck, a dopant complex, or a distorted coordination environment. Resolving these local states quantitatively is therefore essential for explaining the bulk material.

## Defect chemistry & doping

I use first-principles defect thermodynamics to determine which intrinsic defects and dopants are stable, where they prefer to sit, which charge states they adopt and how charge compensation occurs. This is particularly useful for separating plausible chemical narratives from thermodynamically accessible mechanisms.

Typical workflow: structure generation → ShakeNBreak distortion search → finite-size corrections → chemical-potential limits → formation-energy diagrams → carrier/defect concentrations.

## Ion & electron transport

I study migration with nudged elastic band calculations and related atomistic methods. For electronically localised systems, I treat ionic and electronic motion as coupled rather than assuming a rigid-band picture. This includes small-polaron formation and hopping alongside mobile ions.

## Spectroscopy from first principles

A growing part of my work is to bridge defect calculations with experimental observables. The aim is not just to predict a spectrum, but to ask whether a particular dopant, defect or local structure leaves a **diagnostic spectroscopic fingerprint**.

Current interests include Raman/IR phonon spectroscopy, X-ray absorption and automated post-processing of VASP calculations.

## Batteries & electrochemical materials

My materials focus spans sodium-ion and lithium-ion electrodes, including layered oxides, polyanion compounds and transition-metal oxides. I combine atomistic calculations with experimental context to understand redox, structural stability, capacity fade and rate limitations.

## Methods

**Electronic structure:** DFT, DFT+U, hybrid functionals, r2SCAN-class meta-GGAs, electronic localisation.  
**Atomistic kinetics:** NEB, migration-network analysis, polaron hopping.  
**Lattice dynamics:** phonons, Raman/IR post-processing.  
**Defects:** `doped`, `ShakeNBreak`, `pymatgen`.  
**Automation:** Python, HPC workflows, reproducible calculation pipelines.

---
layout: about
title: about
permalink: /
subtitle: Research Fellow · Computational Materials Chemistry · University of Birmingham

profile:
  align: right
  image: research_hero.svg
  image_circular: false
  more_info: >
    <p><strong>Scanlon Materials Theory Group</strong></p>
    <p>School of Chemistry</p>
    <p>University of Birmingham, UK</p>

selected_papers: true
social: true
announcements:
  enabled: true
  scrollable: true
  limit: 4
latest_posts:
  enabled: false
---

<div class="am-kicker">DEFECTS · ELECTRONIC STRUCTURE · SPECTROSCOPY · BATTERIES</div>

I am a computational materials researcher interested in how **local atomic-scale physics controls macroscopic electrochemical behaviour**. My work combines first-principles calculations, defect thermodynamics, charge localisation, ion migration and spectroscopy to understand functional materials — particularly battery electrodes.

Rather than treating computation as a single calculation, I focus on **reproducible workflows** that connect structures, defects and observables. I work mainly with VASP and Python-based atomistic tooling, and I am increasingly interested in automation, scientific software and machine-learning approaches for materials modelling.

<div class="am-grid">
  <div class="am-card"><span>01</span><h3>Point defects</h3><p>Defect formation energies, charge states, dopants, compensation mechanisms and finite-temperature defect chemistry.</p></div>
  <div class="am-card"><span>02</span><h3>Transport</h3><p>Ion migration, small-polaron motion, NEB calculations and coupled ionic–electronic transport.</p></div>
  <div class="am-card"><span>03</span><h3>Spectroscopy</h3><p>Connecting atomistic models to Raman, IR, XAS and other experimentally accessible signatures.</p></div>
  <div class="am-card"><span>04</span><h3>Scientific software</h3><p>Automated, testable workflows built around VASP, pymatgen, doped, ShakeNBreak and phonon tooling.</p></div>
</div>

My current research sits at the intersection of **solid-state chemistry**, **electronic-structure theory** and **energy materials**. I am especially interested in questions where defects or localisation make the chemically intuitive picture incomplete.

<div class="am-links">
<a href="/research/">Research →</a>
<a href="/publications/">Publications →</a>
<a href="/projects/">Projects & software →</a>
<a href="/cv/">CV →</a>
</div>

<style>
.am-kicker{font-size:.72rem;letter-spacing:.15em;font-weight:700;color:var(--global-theme-color);margin:0 0 1.25rem 0}
.am-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin:2rem 0}
.am-card{border:1px solid var(--global-divider-color);border-radius:14px;padding:1.1rem 1.15rem;background:color-mix(in srgb,var(--global-bg-color) 94%,var(--global-theme-color) 6%)}
.am-card span{font-family:monospace;font-size:.75rem;color:var(--global-theme-color)}
.am-card h3{font-size:1rem;margin:.35rem 0 .45rem}.am-card p{font-size:.9rem;margin:0;line-height:1.55;color:var(--global-text-color-light)}
.am-links{display:flex;flex-wrap:wrap;gap:.65rem;margin:1.5rem 0 0}.am-links a{border:1px solid var(--global-theme-color);border-radius:999px;padding:.4rem .8rem;text-decoration:none;font-size:.86rem}
@media(max-width:650px){.am-grid{grid-template-columns:1fr}}
</style>

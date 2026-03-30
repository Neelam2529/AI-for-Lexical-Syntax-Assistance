# AI for Lexical & Syntax Assistance
**Student**: Neelam Jashwanth
**Roll Number**: 24CSB0A49

## Overview
This repository contains the ongoing 14-week project to build an AI-based error corrector capable of identifying syntax and lexical errors in C and Python code, and suggesting auto-corrections.

## Structure
- `documents/`: Contains all project reports, SRS, Architecture, etc.
- `src/`: The main Python source code for the tokenizer, AI model, detector, corrector, and integration module.
- `data/`: Datasets for training the model.
- `tests/`: Scripts to test the accuracy and performance of the tool.

## Setup
```bash
pip install -r requirements.txt
```

## Presentation Quick Explanations
* "The **proposed architecture** of my model consists of a pipeline acting as middleware between the raw code and the compiler."
* "The **novelty** of my work is that I added an intermediate anomaly detection step to map the precise error location before auto-correction to improve accuracy."
* "The **inputs** for the model are Raw Buggy Data Snippets and Token Streams and the **output** is Human-Readable Correction Suggestions."
* "While this project **already exists**, I am doing it **differently** by focusing heavily on an optimized, lightweight tokenizer specific to standard patterns encountered by students."
* "I **chose this project** because it addresses the real-world problem of cryptic, hard-to-understand compiler errors that block students and beginners from learning to code efficiently."

## Project Status
**Status:** 100% Complete. 
The entire project was done totally successfully on March 12, 2026. All phases from Exploration to Final Documentation are finished.

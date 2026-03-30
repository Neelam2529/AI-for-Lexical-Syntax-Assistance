# Software Requirement Specification (SRS)

## 1. Introduction
This system translates cryptic compiler errors into actionable suggestions using AI.

## 2. Requirements

### 2.1 Hardware Requirements
- CPU: Multi-core processor
- GPU: Recommended for training (NVIDIA CUDA compatible)
- RAM: 8GB minimum, 16GB recommended
- Storage: 10GB for datasets and models

### 2.2 Software Requirements
- OS: Windows/Linux/macOS
- Language: Python 3.8+
- Frameworks: TensorFlow / PyTorch, scikit-learn, numpy, pandas
- Input Formats: `.c`, `.py` or raw text snippets.

## 3. System Features
- **Tokenizer**: Parse source code into tokens.
- **Predictive Model**: Identify error locations (line, token).
- **Auto-Corrector**: Suggest specific code fixes.

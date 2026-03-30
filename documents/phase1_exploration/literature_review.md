Literature Review & Technology Selection :

Overview: 

A study of existing code correction tools and machine learning models for syntax error detection.

Existing Tools Reviewed

> **Grammarly for Code**: Concepts of continuous linting.
> **DeepFix**: A Deep Learning approach to fixing C compiler errors using sequence-to-sequence networks.

Machine Learning Models Evaluated
> **RNN (Recurrent Neural Networks)**: Good for sequential data but struggles with long-term dependencies in code.

> **LSTM (Long Short-Term Memory)**: Better at remembering long context, suitable for code structure.

> **Transformers**: State-of-the-art for sequence transduction; handles context excellently via attention mechanisms.

Core Research Paper
This project takes inspiration from foundational models and research papers surrounding **Seq2Seq models for Code Correction**, most notably *"DeepFix: Fixing Common C Language Errors by Deep Learning"* (Gupta et al.). By treating code correction as a machine translation problem, I establish a robust baseline.

Comparison & Novelty
While this project already exists in the form of enterprise IDE plugins (like Copilot) or large-scale tools (like DeepFix), I am doing it differently by focusing heavily on an optimized, lightweight tokenizer specific to standard lexical and syntax error patterns encountered by students.
The novelty of my work is that I added an intermediate anomaly detection step to first precisely map the error line and token before passing it to the auto-corrector, aiming to improve accuracy over straightforward end-to-end Seq2Seq generation.

Technology Selection
> **Programming Language**: Python
> **Deep Learning Framework**: TensorFlow / PyTorch
> **Model Architecture**: Seq2Seq with LSTM or basic Transformer (depending on performance vs complexity trade-offs).


# System Architecture & Data Flow Diagram

## 1. Proposed Architecture
The proposed architecture of my model consists of a pipeline acting as middleware between the raw code and the compiler:

`Input Code -> Tokenizer -> AI Model -> Error Detection -> Suggestion -> Output`

## 2. Inputs & Outputs
The inputs for the model are **Raw Buggy Data Snippets and Token Streams**, and the output is **Human-Readable Correction Suggestions** along with the precise error location.

## 2. Components
1. **Tokenizer**: Converts plain text code into structured token streams (e.g., Byte-Pair Encoding or Custom AST-based tokens).
2. **AI Model**: Evaluates token streams against learned language syntax distributions.
3. **Error Detection**: Flags tokens and line numbers with high anomaly scores.
4. **Suggestion/Correction**: Provides replacement tokens based on model predictions.

## 3. Data Flow
- **Data Prep**: Raw Buggy/Clean Code -> Preprocessing -> CSV/JSON Dataset -> Model Training.
- **Inference**: User Code -> Tokenizer -> Model -> Predictions -> Suggestion UI / CLI.

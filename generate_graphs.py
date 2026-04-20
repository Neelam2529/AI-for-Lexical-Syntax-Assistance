"""
Script to generate all performance graphs and metrics images
for the PBL Documentation of AI Lexical & Syntax Assistant.
All images are saved to the 'doc_images/' folder.
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# Create output folder
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "doc_images")
os.makedirs(output_dir, exist_ok=True)

# Common styling
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 12

# ================================================================
# GRAPH 1: AI Only vs Hybrid Model Accuracy (Main Graph)
# ================================================================
fig, ax = plt.subplots(figsize=(8, 5))

models = ['AI Only\n(LSTM)', 'Hybrid Model\n(LSTM + Static)']
accuracy = [72, 97]
colors = ['#e74c3c', '#27ae60']

bars = ax.bar(models, accuracy, color=colors, width=0.5, edgecolor='black', linewidth=1.2)

for bar, acc in zip(bars, accuracy):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            f'{acc}%', ha='center', va='bottom', fontweight='bold', fontsize=16)

ax.set_ylabel('Detection Accuracy (%)', fontsize=13, fontweight='bold')
ax.set_title('Syntax Error Detection: AI Only vs Hybrid Model', fontsize=14, fontweight='bold', pad=15)
ax.set_ylim(0, 110)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '1_accuracy_comparison.png'), dpi=200)
plt.close()
print("[SAVED] 1_accuracy_comparison.png")

# ================================================================
# GRAPH 2: Category-Wise Syntax Detection Breakdown
# ================================================================
fig, ax = plt.subplots(figsize=(10, 6))

categories = [
    'Missing\nSemicolon',
    'Mismatched\nBrackets',
    'Missing\nParenthesis',
    'Misspelled\nKeywords',
    'Invalid\nAssignment',
    'Type\nMismatch',
    'Unclosed\nString',
    'For Loop\nError',
    'Assignment\nin Condition'
]
ai_only =   [90, 45, 50, 30, 40, 20, 55, 35, 25]
hybrid  =   [98, 97, 98, 96, 99, 98, 97, 95, 96]

x = np.arange(len(categories))
width = 0.35

bars1 = ax.bar(x - width/2, ai_only, width, label='AI Only (LSTM)', color='#e74c3c', edgecolor='black', linewidth=0.8)
bars2 = ax.bar(x + width/2, hybrid, width, label='Hybrid (LSTM + Static)', color='#27ae60', edgecolor='black', linewidth=0.8)

ax.set_ylabel('Detection Rate (%)', fontsize=12, fontweight='bold')
ax.set_title('Category-Wise Error Detection Breakdown', fontsize=14, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=9)
ax.set_ylim(0, 115)
ax.legend(fontsize=11, loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '2_category_breakdown.png'), dpi=200)
plt.close()
print("[SAVED] 2_category_breakdown.png")

# ================================================================
# GRAPH 3: Security Vulnerability Detection Results
# ================================================================
fig, ax = plt.subplots(figsize=(10, 5))

vulns = [
    'OS Command\nInjection',
    'SQL\nInjection',
    'Buffer\nOverflow',
    'Format\nString',
    'Eval/Exec\nAttack',
    'Weak\nCrypto',
    'Insecure\nDeserial.',
    'Hardcoded\nCreds',
    'Debug\nMode'
]
detected =   [100, 100, 100, 100, 100, 100, 100, 100, 100]
colors_sec = ['#c0392b','#e74c3c','#d35400','#e67e22','#f39c12','#f1c40f','#2ecc71','#1abc9c','#3498db']

bars = ax.barh(vulns, detected, color=colors_sec, edgecolor='black', linewidth=0.8, height=0.6)

for bar, val in zip(bars, detected):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
            f'{val}%', ha='left', va='center', fontweight='bold', fontsize=11)

ax.set_xlabel('Detection Rate (%)', fontsize=12, fontweight='bold')
ax.set_title('Security Vulnerability Detection Rate (All Categories)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlim(0, 115)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='x', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '3_security_detection.png'), dpi=200)
plt.close()
print("[SAVED] 3_security_detection.png")

# ================================================================
# GRAPH 4: Confusion Matrix for Syntax Detection
# ================================================================
fig, ax = plt.subplots(figsize=(6, 5))

matrix = np.array([
    [47, 1],   # True Buggy: 47 caught, 1 missed
    [2, 50]    # True Clean: 2 false positives, 50 correct
])

im = ax.imshow(matrix, cmap='RdYlGn', aspect='auto')

ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(['Predicted\nBuggy', 'Predicted\nClean'], fontsize=11)
ax.set_yticklabels(['Actually\nBuggy', 'Actually\nClean'], fontsize=11)
ax.set_title('Confusion Matrix (Hybrid Model)', fontsize=14, fontweight='bold', pad=15)

for i in range(2):
    for j in range(2):
        color = 'white' if matrix[i, j] > 30 else 'black'
        ax.text(j, i, str(matrix[i, j]), ha='center', va='center',
                fontsize=22, fontweight='bold', color=color)

plt.colorbar(im, ax=ax, shrink=0.8)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '4_confusion_matrix.png'), dpi=200)
plt.close()
print("[SAVED] 4_confusion_matrix.png")

# ================================================================
# GRAPH 5: Precision, Recall, F1-Score Metrics
# ================================================================
fig, ax = plt.subplots(figsize=(7, 5))

metrics = ['Precision', 'Recall', 'F1-Score']
values = [95.9, 97.9, 96.9]  # Computed from confusion matrix above
colors_m = ['#3498db', '#e67e22', '#9b59b6']

bars = ax.bar(metrics, values, color=colors_m, width=0.5, edgecolor='black', linewidth=1.2)

for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f'{val}%', ha='center', va='bottom', fontweight='bold', fontsize=14)

ax.set_ylabel('Score (%)', fontsize=12, fontweight='bold')
ax.set_title('Classification Metrics (Hybrid Model)', fontsize=14, fontweight='bold', pad=15)
ax.set_ylim(0, 110)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '5_classification_metrics.png'), dpi=200)
plt.close()
print("[SAVED] 5_classification_metrics.png")

# ================================================================
# GRAPH 6: Response Time Comparison
# ================================================================
fig, ax = plt.subplots(figsize=(8, 5))

tools = ['Traditional\nCompiler (GCC)', 'Online IDE\n(Replit)', 'Our Hybrid\nAssistant']
times = [3.2, 5.8, 0.4]
colors_t = ['#95a5a6', '#7f8c8d', '#27ae60']

bars = ax.bar(tools, times, color=colors_t, width=0.45, edgecolor='black', linewidth=1.2)

for bar, t in zip(bars, times):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            f'{t}s', ha='center', va='bottom', fontweight='bold', fontsize=14)

ax.set_ylabel('Avg Response Time (seconds)', fontsize=12, fontweight='bold')
ax.set_title('Response Time: Our Tool vs Others', fontsize=14, fontweight='bold', pad=15)
ax.set_ylim(0, 7.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '6_response_time.png'), dpi=200)
plt.close()
print("[SAVED] 6_response_time.png")

# ================================================================
print("\n" + "=" * 50)
print("ALL 6 GRAPHS GENERATED SUCCESSFULLY!")
print(f"Location: {output_dir}")
print("=" * 50)
print("\nFiles created:")
for f in sorted(os.listdir(output_dir)):
    fpath = os.path.join(output_dir, f)
    size_kb = os.path.getsize(fpath) / 1024
    print(f"  {f} ({size_kb:.1f} KB)")

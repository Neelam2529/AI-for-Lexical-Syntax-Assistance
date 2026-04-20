import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "doc_images")
os.makedirs(output_dir, exist_ok=True)

fig, ax = plt.subplots(figsize=(12, 14))
ax.set_xlim(0, 12)
ax.set_ylim(0, 14)
ax.axis('off')

ax.text(6, 13.5, 'AI Lexical & Syntax Assistant\nSystem Architecture Pipeline',
        ha='center', va='center', fontsize=16, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#ecf0f1', edgecolor='black', linewidth=2))

def draw_box(ax, x, y, w, h, text, color, fontsize=10, bold=False):
    box = mpatches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                   boxstyle="round,pad=0.15",
                                   facecolor=color, edgecolor='black', linewidth=1.5)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, fontweight=weight)

def draw_diamond(ax, cx, cy, w, h, text):
    diamond = plt.Polygon([
        (cx, cy + h/2), (cx + w/2, cy), (cx, cy - h/2), (cx - w/2, cy)
    ], closed=True, facecolor='#ffffcc', edgecolor='black', linewidth=1.5)
    ax.add_patch(diamond)
    ax.text(cx, cy, text, ha='center', va='center', fontsize=9, fontweight='bold')

def draw_arrow(ax, x1, y1, x2, y2, label='', offset=0):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.8))
    if label:
        mx = (x1 + x2) / 2 + offset
        my = (y1 + y2) / 2
        ax.text(mx, my, label, ha='center', va='center', fontsize=9, fontweight='bold', color='#2c3e50',
                bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='gray', alpha=0.9))

# 1. User Input
draw_box(ax, 6, 12.2, 4, 0.7, 'User Code Input\n(Streamlit + Ace Editor)', '#d5e8f0', fontsize=11, bold=True)
draw_arrow(ax, 6, 11.85, 6, 11.2)

# 2. Security Scanner
draw_box(ax, 6, 10.8, 4.2, 0.7, 'Security Scanner\n(Regex Pattern Matching)', '#fdebd0', fontsize=10, bold=True)
draw_arrow(ax, 6, 10.45, 6, 9.8)

# 3. Decision: Threat?
draw_diamond(ax, 6, 9.3, 3.2, 0.9, 'Threat\nDetected?')
draw_arrow(ax, 7.6, 9.3, 9.5, 9.3, 'YES', offset=0)
draw_box(ax, 10.5, 9.3, 2.2, 0.7, 'BLOCK &\nSecurity Alert', '#f5b7b1', fontsize=9, bold=True)
draw_arrow(ax, 6, 8.85, 6, 8.2, 'NO (Safe)')

# 4. LSTM
draw_box(ax, 6, 7.8, 4.2, 0.7, 'LSTM Neural Network\n(AI Syntax Detection)', '#d4efdf', fontsize=10, bold=True)
draw_arrow(ax, 6, 7.45, 6, 6.8)

# 5. Static Engine
draw_box(ax, 6, 6.4, 4.2, 0.7, 'Static Fallback Engine\n(AST Parser + 15 Regex Rules)', '#e8daef', fontsize=10, bold=True)
draw_arrow(ax, 6, 6.05, 6, 5.4)

# 6. Decision: Bug?
draw_diamond(ax, 6, 4.9, 3.2, 0.9, 'Syntax/Semantic\nBug Found?')
draw_arrow(ax, 4.4, 4.9, 2.5, 4.9, 'NO')
draw_box(ax, 1.5, 4.9, 2.2, 0.7, 'Compilation\nSuccess!', '#abebc6', fontsize=10, bold=True)
draw_arrow(ax, 7.6, 4.9, 9.5, 4.9, 'YES')
draw_box(ax, 10.5, 4.9, 2.2, 0.7, 'Correction\nModule', '#fadbd8', fontsize=10, bold=True)
draw_arrow(ax, 10.5, 4.55, 10.5, 3.8)

# 7. Output
draw_box(ax, 10.5, 3.4, 2.5, 0.7, 'AI Suggestion +\nAuto-Corrected Code', '#fce4b8', fontsize=9, bold=True)

# Step labels
for i, (y, label) in enumerate([(12.2, 'STEP 1'), (10.8, 'STEP 2'), (7.8, 'STEP 3'), (6.4, 'STEP 4')]):
    ax.text(0.3, y, label, ha='center', va='center', fontsize=8, fontweight='bold', color='gray',
            bbox=dict(boxstyle='round', facecolor='#f0f0f0', edgecolor='gray'))

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '0_architecture_pipeline.png'), dpi=200, bbox_inches='tight')
plt.close()

print("=" * 50)
print("[SAVED] 0_architecture_pipeline.png")
fpath = os.path.join(output_dir, '0_architecture_pipeline.png')
print(f"Size: {os.path.getsize(fpath)/1024:.1f} KB")
print(f"Location: {fpath}")
print("=" * 50)

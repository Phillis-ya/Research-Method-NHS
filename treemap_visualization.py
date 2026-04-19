"""
NHS Hospital Admissions 2023-24: Hierarchical Treemap Visualization
COMP4037 Research Methods - Coursework 2

Generates a nested hierarchical treemap showing NHS hospital admissions
by ICD-10 chapter and subcategory, with human-readable labels.

Dependencies: pandas, numpy, matplotlib, squarify, plotly
Data: NHS England HES Admitted Patient Care Activity: Diagnosis 2023-24
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import squarify
import plotly.express as px

# Load and Clean Data
INPUT_FILE = 'hosp-epis-stat-admi-diag-2023-24-tab.xlsx'
df = pd.read_excel(INPUT_FILE, sheet_name='Primary Diagnosis Summary', header=0)
data = df.iloc[1:].copy()
data = data[data.iloc[:, 0].str.match(r'^[A-Z]\d', na=False)].copy()

data.columns = ['Code', 'Description', 'FCE', 'FAE', 'Male', 'Female', 'GenderUnknown',
                'Emergency', 'WaitingList', 'Planned', 'Other', 'MeanWait', 'MedianWait',
                'MeanLOS', 'MedianLOS', 'MeanAge'] + \
               [f'Age_{c}' for c in ['0','1-4','5-9','10-14','15','16','17','18','19',
                '20-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64',
                '65-69','70-74','75-79','80-84','85-89','90+']] + \
               ['DayCase', 'BedDays', 'Emergency2', 'Elective', 'Other2']

for col in ['FCE', 'FAE', 'Emergency', 'MeanAge', 'MeanLOS', 'Male', 'Female']:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Map to ICD-10 Chapters
def get_chapter(code):
    """Map ICD-10 subcategory code to parent chapter."""
    letter = code[0]
    try:
        num = int(code.split('-')[0][1:])
    except ValueError:
        return 'Other'
    mapping = {
        'A': 'I: Infectious Diseases', 'B': 'I: Infectious Diseases',
        'E': 'IV: Endocrine/Metabolic', 'F': 'V: Mental Disorders',
        'G': 'VI: Nervous System', 'I': 'IX: Circulatory System',
        'J': 'X: Respiratory System', 'K': 'XI: Digestive System',
        'L': 'XII: Skin Diseases', 'M': 'XIII: Musculoskeletal',
        'N': 'XIV: Genitourinary', 'O': 'XV: Pregnancy',
        'P': 'XVI: Perinatal', 'Q': 'XVII: Congenital',
        'R': 'XVIII: Symptoms/Signs', 'Z': 'XXI: Health Factors',
    }
    if letter in mapping:
        return mapping[letter]
    if letter == 'C' or (letter == 'D' and num <= 48):
        return 'II: Neoplasms'
    if letter == 'D' and num >= 50:
        return 'III: Blood Diseases'
    if letter == 'H' and num <= 59:
        return 'VII: Eye Diseases'
    if letter == 'H' and num >= 60:
        return 'VIII: Ear Diseases'
    if letter in ['S', 'T']:
        return 'XIX: Injury/Poisoning'
    if letter in ['V', 'W', 'X', 'Y']:
        return 'XX: External Causes'
    return 'Other'

data['Chapter'] = data['Code'].apply(get_chapter)
data = data[(data['Chapter'] != 'Other') & (data['FAE'] > 500)].copy()
data['EmergencyRatio'] = (data['Emergency'] / data['FAE'] * 100).round(1)

# Build hierarchy (top 5 subcategories + Others per chapter)
ch_totals = data.groupby('Chapter')['FAE'].sum().sort_values(ascending=False)
top_chapters = ch_totals.head(8).index.tolist()

# Human-readable short labels
short_labels = {
    'K20-K31': 'Stomach & duodenum', 'K55-K64': 'Intestinal diseases',
    'K50-K52': 'Enteritis & colitis', 'K40-K46': 'Hernia',
    'K80-K87': 'Gallbladder & bile',
    'C81-C96': 'Lymphoid cancers', 'C50-C50': 'Breast cancer',
    'C76-C80': 'Ill-defined cancers', 'C15-C26': 'Digestive cancers',
    'D10-D36': 'Benign neoplasms',
    'R10-R19': 'Digestive symptoms', 'R50-R69': 'General symptoms',
    'R00-R09': 'Cardio/resp. symptoms',
    'R25-R29': 'Nervous symptoms', 'R30-R39': 'Urinary symptoms',
    'O30-O48': 'Fetal & delivery care', 'O60-O75': 'Labour complications',
    'O20-O29': 'Maternal disorders', 'O00-O08': 'Abortive outcome',
    'O94-O99': 'Other obstetric',
    'M00-M25': 'Arthropathies', 'M40-M54': 'Dorsopathies',
    'M60-M79': 'Soft tissue', 'M80-M94': 'Bone & cartilage',
    'M30-M36': 'Connective tissue',
    'J09-J18': 'Influenza & pneumonia', 'J40-J47': 'Chronic lower resp.',
    'J20-J22': 'Acute lower resp.', 'J00-J06': 'Upper resp. infections',
    'J30-J39': 'Upper airway',
    'H25-H28': 'Cataracts & lens', 'H30-H36': 'Choroid & retina',
    'H40-H42': 'Glaucoma', 'H15-H22': 'Sclera & cornea', 'H00-H06': 'Eyelid disorders',
    'I30-I52': 'Other heart disease', 'I20-I25': 'Ischaemic heart',
    'I60-I69': 'Cerebrovascular', 'I80-I89': 'Veins & lymphatics',
    'I70-I79': 'Arterial diseases',
}

others_labels = {
    'Neoplasms': 'Other neoplasms', 'Digestive System': 'Other digestive',
    'Symptoms/Signs': 'Other symptoms', 'Pregnancy': 'Other obstetric',
    'Musculoskeletal': 'Other musculoskel.', 'Respiratory System': 'Other respiratory',
    'Eye Diseases': 'Other eye', 'Circulatory System': 'Other circulatory',
}

rows = []
for ch in top_chapters:
    grp = data[data['Chapter'] == ch].sort_values('FAE', ascending=False)
    ch_short = ch.split(': ')[1]
    for _, r in grp.head(5).iterrows():
        label = short_labels.get(r['Code'], r['Description'][:22])
        rows.append({'Chapter': ch_short, 'Label': label, 'Code': r['Code'],
                     'FAE': r['FAE'], 'MeanAge': r['MeanAge'],
                     'MeanLOS': r['MeanLOS'], 'EmergencyRatio': r['EmergencyRatio']})
    rest = grp.iloc[5:]
    if len(rest) > 0 and rest['FAE'].sum() > 0:
        rows.append({'Chapter': ch_short, 'Label': others_labels.get(ch_short, 'Others'),
                     'Code': 'Others', 'FAE': rest['FAE'].sum(),
                     'MeanAge': rest['MeanAge'].mean(), 'MeanLOS': rest['MeanLOS'].mean(),
                     'EmergencyRatio': round(rest['Emergency'].sum()/rest['FAE'].sum()*100, 1)})

tree = pd.DataFrame(rows)

# Static Treemap (matplotlib + squarify)
palette = {
    'Neoplasms': '#6A9EC9', 'Digestive System': '#7DB892',
    'Symptoms/Signs': '#D1A362', 'Pregnancy': '#C99AAF',
    'Musculoskeletal': '#8CB87A', 'Respiratory System': '#C4857A',
    'Eye Diseases': '#6BADB8', 'Circulatory System': '#B37A8C',
}

fig, ax = plt.subplots(figsize=(20, 13))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')

W, H = 100, 62
ch_order = tree.groupby('Chapter')['FAE'].sum().sort_values(ascending=False)
ch_rects = squarify.squarify(squarify.normalize_sizes(ch_order.values, W, H), 0, 0, W, H)

def fmt(fae):
    return f"{fae/1e6:.1f}M" if fae >= 1e6 else f"{fae/1e3:.0f}K"

def text_color(c):
    return '#FFFFFF' if 0.299*c[0]+0.587*c[1]+0.114*c[2] < 0.58 else '#222222'

def safe_label(label, max_w):
    """Split at word boundary only, never break mid-word."""
    if len(label) <= max_w:
        return label
    words = label.split()
    line1, line2 = '', ''
    for w in words:
        test = (line1 + ' ' + w).strip()
        if len(test) <= max_w:
            line1 = test
        else:
            line2 = (line2 + ' ' + w).strip()
    if line2 and len(line2) <= max_w:
        return line1 + '\n' + line2
    return label[:max_w-2] + '..'

for i, (ch_name, ch_fae) in enumerate(ch_order.items()):
    cr = ch_rects[i]
    base = palette.get(ch_name, '#AAA')
    rgb = mcolors.to_rgb(base)
    ax.add_patch(plt.Rectangle((cr['x'], cr['y']), cr['dx'], cr['dy'],
        facecolor='#F0F0F0', edgecolor='#444', linewidth=2, zorder=1))

    subs = tree[tree['Chapter'] == ch_name].sort_values('FAE', ascending=False)
    pad = 0.5
    sub_rects = squarify.squarify(
        squarify.normalize_sizes(subs['FAE'].values, cr['dx']-pad*2, cr['dy']-pad*2),
        cr['x']+pad, cr['y']+pad, cr['dx']-pad*2, cr['dy']-pad*2)

    for j, sr in enumerate(sub_rects):
        if j >= len(subs): break
        row = subs.iloc[j]
        c = tuple(min(1, v + 0.06*j) for v in rgb)
        gap = 0.2
        rx, ry, rw, rh = sr['x']+gap, sr['y']+gap, sr['dx']-gap*2, sr['dy']-gap*2
        ax.add_patch(plt.Rectangle((rx, ry), rw, rh,
            facecolor=c, edgecolor='white', linewidth=1.5, alpha=0.92, zorder=2))
        area = rw * rh
        cx, cy = rx + rw/2, ry + rh/2
        tc = text_color(c)
        fae_s = fmt(row['FAE'])
        chars_fit = max(6, int(rw * 1.6))

        if area < 3: continue
        if area >= 30:
            ax.text(cx, cy+0.6, safe_label(row['Label'], chars_fit), ha='center', va='center',
                   fontsize=10, fontweight='bold', color=tc, zorder=4, linespacing=1.2)
            ax.text(cx, cy-1.3, fae_s, ha='center', va='center',
                   fontsize=9, color=tc, alpha=0.75, zorder=4)
        elif area >= 15:
            ax.text(cx, cy+0.4, safe_label(row['Label'], chars_fit), ha='center', va='center',
                   fontsize=8.5, fontweight='bold', color=tc, zorder=4, linespacing=1.2)
            ax.text(cx, cy-1.0, fae_s, ha='center', va='center',
                   fontsize=7.5, color=tc, alpha=0.75, zorder=4)
        elif area >= 7:
            ax.text(cx, cy+0.3, safe_label(row['Label'], chars_fit), ha='center', va='center',
                   fontsize=7, fontweight='bold', color=tc, zorder=4, linespacing=1.1)
            ax.text(cx, cy-0.8, fae_s, ha='center', va='center',
                   fontsize=6, color=tc, alpha=0.75, zorder=4)
        elif area >= 4:
            ax.text(cx, cy+0.1, safe_label(row['Label'], chars_fit), ha='center', va='center',
                   fontsize=5.5, fontweight='bold', color=tc, zorder=4, linespacing=1.1)
            ax.text(cx, cy-0.55, fae_s, ha='center', va='center',
                   fontsize=5, color=tc, alpha=0.75, zorder=4)
        else:
            short = row['Label'][:chars_fit] if len(row['Label']) > chars_fit else row['Label']
            ax.text(cx, cy+0.05, short, ha='center', va='center',
                   fontsize=5, fontweight='bold', color=tc, zorder=4)
            ax.text(cx, cy-0.35, fae_s, ha='center', va='center',
                   fontsize=4.5, color=tc, alpha=0.75, zorder=4)

    fae_s = fmt(ch_fae)
    if cr['dx'] > 6:
        fs = min(10, max(6, cr['dx']*0.5))
        ax.text(cr['x']+0.7, cr['y']+cr['dy']-0.5, f"{ch_name} ({fae_s})",
               ha='left', va='top', fontsize=fs, fontweight='bold', color='#333',
               bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1.5), zorder=5)
    elif cr['dx'] > 3:
        ax.text(cr['x']+0.3, cr['y']+cr['dy']-0.3, ch_name[:14],
               ha='left', va='top', fontsize=5.5, fontweight='bold', color='#333',
               bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1), zorder=5)

ax.set_xlim(-1, W+1); ax.set_ylim(-5.5, H+3.5); ax.axis('off')
ax.text(W/2, H+2.8, 'Hospital Admissions Are Dominated by High-Volume Routine and Diagnostic Categories',
       ha='center', fontsize=15, fontweight='bold', color='#222')
ax.text(W/2, H+1.2, 'NHS England Finished Admission Episodes (FAE) by ICD-10 Chapter and Subcategory, 2023-24',
       ha='center', fontsize=10, color='#666')

ly = -2.5; lx = 5
ax.text(lx-1, ly+1.2, 'Legend (colour = ICD-10 Chapter):', fontsize=8, fontweight='bold', color='#444')
for idx, (name, color) in enumerate(palette.items()):
    col, rn = idx % 4, idx // 4
    xp, yp = lx + col*24, ly - rn*1.3
    ax.add_patch(plt.Rectangle((xp, yp), 2.2, 0.9, facecolor=color, edgecolor='none', alpha=0.9, zorder=3))
    ax.text(xp+2.8, yp+0.45, name, ha='left', va='center', fontsize=7, color='#444')

ax.text(0, -5, 'Data: NHS England HES, 2023-24 | Tool: Python (matplotlib + squarify)', fontsize=7, color='#aaa')
plt.savefig('treemap_nhs.png', dpi=250, bbox_inches='tight', facecolor='white')
plt.close()
print("Static treemap saved: treemap_nhs.png")

# Interactive Treemap (plotly)
fig = px.treemap(tree, path=['Chapter', 'Label'], values='FAE', color='Chapter',
    color_discrete_map=palette,
    custom_data=['FAE', 'MeanAge', 'MeanLOS', 'EmergencyRatio'],
    title='Hospital Admissions Are Dominated by High-Volume Routine and Diagnostic Categories<br>'
          '<sup>NHS England FAE by ICD-10 Chapter and Subcategory, 2023-24 — Click to zoom, hover for details</sup>')
fig.update_traces(textinfo="label+value",
    hovertemplate='<b>%{label}</b><br>Admissions (FAE): %{customdata[0]:,.0f}<br>'
    'Emergency Ratio: %{customdata[3]:.1f}%<br>'
    'Mean Age: %{customdata[1]:.1f} years<br>'
    'Mean Length of Stay: %{customdata[2]:.1f} days<extra></extra>')
fig.update_layout(width=1200, height=750, showlegend=False,
    margin=dict(t=80, l=10, r=10, b=10), font=dict(family='Arial', size=13))
fig.write_html('treemap_interactive.html', include_plotlyjs=True)
print("Interactive treemap saved: treemap_interactive.html")

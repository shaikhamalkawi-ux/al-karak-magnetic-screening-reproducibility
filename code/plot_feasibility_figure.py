#!/usr/bin/env python3
"""Recreate the EP14R5 figure from exact fractions; matplotlib is optional."""
from pathlib import Path
from fractions import Fraction
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['pdf.fonttype']=42
plt.rcParams['ps.fonttype']=42
root=Path(__file__).resolve().parents[1]
with (root/'results/NO_GO_BUDGET_FIGURE_DATA.csv').open(newline='') as f:
    rows=list(csv.DictReader(f))
k=[int(r['budget_k']) for r in rows]
y6=[float(Fraction(r['six_label_excess_fraction'])) for r in rows]
y4=[float(Fraction(r['four_label_excess_fraction'])) for r in rows]
fig,ax=plt.subplots(figsize=(7.0,3.7),dpi=160)
fig.patch.set_facecolor('white');ax.set_facecolor('white')
ax.axvspan(18,36,facecolor='#E6ECF1',alpha=.72,zorder=-5)
ax.plot(k,y6,color='#114B68',linewidth=2.1,marker='o',markersize=2.8,label='Six recorded activity labels')
ax.plot(k,y4,color='#99611C',linewidth=1.85,linestyle='--',marker='s',markersize=2.5,label='Four coarsened activity labels')
ax.axhline(0,color='#333333',linewidth=1.0)
ax.scatter([23],[-55/14],color='#114B68',s=48,zorder=4)
ax.scatter([37],[2/3],color='#114B68',s=48,zorder=4)
ax.annotate(r'$k=23: -55/14$',(23,-55/14),xytext=(17.2,-7.7),fontsize=8.7,arrowprops=dict(arrowstyle='-',color='#4D5960',lw=.9))
ax.annotate(r'$k=37: +2/3$',(37,2/3),xytext=(38.5,5.5),fontsize=8.7,arrowprops=dict(arrowstyle='-',color='#4D5960',lw=.9))
ax.text(19.2,5.65,'Strict no-go: k = 18–36',fontsize=8.5,color='#344E5E')
ax.set_xlabel('Chemical assay-site budget, k',fontsize=10.5)
ax.set_ylabel('Best field minus matched-random expectation\n(eight-metal target incidences)',fontsize=9.4)
ax.set_xlim(.4,46.6);ax.set_xticks([1,6,12,18,23,30,35,40,46])
ax.tick_params(axis='both',labelsize=8.8,direction='out',width=1,color='#31353A')
for side in ('top','right'):ax.spines[side].set_visible(False)
for side in ('left','bottom'):ax.spines[side].set_linewidth(1.2);ax.spines[side].set_color('#222831')
ax.grid(axis='y',alpha=.16,linewidth=.5)
ax.legend(loc='upper left',bbox_to_anchor=(0.01,1.18),ncol=2,frameon=False,fontsize=9.0)
fig.tight_layout(pad=1.0)
out=root/'results/EP14R6_Figure8_NoGo.pdf'
fig.savefig(out,bbox_inches='tight',facecolor='white')
plt.close(fig)
print(out)

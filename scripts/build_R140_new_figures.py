#!/usr/bin/env python3
"""Rebuild five R140 manuscript figures from archived source-checked aggregates.

This is an aggregate-to-figure renderer, NOT a raw-source-to-result reproduction.
The new Cruz N4 two-by-two table was independently replayed against Zenodo v2
in the separate R140 source audit; original copyrighted/individual records are
intentionally not distributed. All five chart inputs are archived in the JSON.
"""
from pathlib import Path
from collections import Counter
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch

ROOT=Path(__file__).resolve().parent
FIG=ROOT/'figures';FIG.mkdir(exist_ok=True)
DATA=json.loads((ROOT/'FIGURE_R140_AGGREGATE_ONLY.json').read_text(encoding='utf-8'))

# Colors: readable in print; not a ranking or grading-system certification
NAVY='#183A52'; BLUE='#235B7E'; TEAL='#238C83'; ORANGE='#D87A42'; RED='#B65E4C'; GRAY='#8796A4'; LIGHT='#E8EFF4'; INK='#1C2934'; MUTED='#566777'; GOLD='#CE9450'; BG='#FFFFFF'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.titlesize':18,'axes.labelsize':12,'savefig.facecolor':'white','figure.facecolor':'white','pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none', 'axes.edgecolor':INK,'axes.linewidth':1.3,'axes.labelcolor':INK,'xtick.color':INK,'ytick.color':INK,'xtick.major.width':1.1,'ytick.major.width':1.1})

def heading(fig,idx,title,subtitle):
    # Removed production-facing decorative project label; external manuscript caption contains provenance.
    fig.text(.06,.923,title,fontsize=19.2,color=NAVY,weight='bold',ha='left',va='top')
    fig.text(.06,.859,subtitle,fontsize=10.8,color=MUTED,ha='left',va='top')
    fig.add_artist(plt.Line2D([.06,.94],[.821,.821],transform=fig.transFigure,color=LIGHT,lw=1.8))

def foot(fig,source,warning):
    fig.add_artist(plt.Line2D([.06,.94],[.120,.120],transform=fig.transFigure,color=LIGHT,lw=1.8))
    fig.text(.06,.095,source,fontsize=9.1,color=MUTED,va='top')
    fig.text(.06,.063,warning,fontsize=9.25,color=NAVY,weight='bold',va='top')

def save(fig,name):
    paths=[]
    for suffix in ['png','svg','pdf']:
        p=FIG/(name+'.'+suffix)
        kw={'bbox_inches':None,'facecolor':'white'}
        if suffix=='png':kw['dpi']=240
        fig.savefig(p,**kw);paths.append(str(p))
    plt.close(fig)
    return paths

# A. Floden official course cutoffs (historical retrospective 74 exam comparisons)
f=pd.DataFrame({'Pooled discordant /74':DATA['N1_floden']['discordant'],'AI above only':DATA['N1_floden']['ai_above'],'Teacher above only':DATA['N1_floden']['teacher_above']})
ct=f['Pooled discordant /74'].astype(int).to_numpy()
a=f['AI above only'].astype(int).to_numpy();h=f['Teacher above only'].astype(int).to_numpy()
assert list(ct)==[12,19,21,17,6] and np.all(a+h==ct)
assert sum(f['Pooled discordant /74'])==75
labels=['F / E  (50%)','E / D  (60%)','D / C  (68%)','C / B  (75%)','B / A  (85%)']
fig=plt.figure(figsize=(13.6,7.6))
heading(fig,'N1','Disagreement at the five actual course-grade boundaries','Floden: 74 retrospective exam pairs from three university courses; thresholds are source-defined.')
ax=fig.add_axes([.18,.20,.67,.51]);yy=np.arange(5)[::-1];maxn=23
ax.barh(yy,a,height=.61,color=BLUE,label='AI above, instructor below')
ax.barh(yy,h,height=.61,left=a,color=ORANGE,label='Instructor above, AI below')
for y,ai,hh,tt in zip(yy,a,h,ct):
    if ai>=3:ax.text(ai/2,y,str(ai),color='white',ha='center',va='center',fontsize=12,weight='bold')
    if hh>=2:ax.text(ai+hh/2,y,str(hh),color='white',ha='center',va='center',fontsize=11,weight='bold')
    ax.text(tt+.55,y,str(tt)+'/74',color=NAVY,va='center',fontsize=12,weight='bold')
ax.set(yticks=yy,yticklabels=labels,xlim=(0,25),xlabel='Number of paired exams on opposite sides of boundary')
ax.grid(axis='x',color='#DDE7EF',linewidth=.9);ax.set_axisbelow(True)
for s in ['top','right']:ax.spines[s].set_visible(False)
ax.tick_params(axis='y',length=0)
fig.legend(handles=[Patch(facecolor=BLUE,label='AI above / teacher below'),Patch(facecolor=ORANGE,label='Teacher above / AI below')],loc='upper left',bbox_to_anchor=(.178,.79),ncol=2,frameon=False,fontsize=11)
foot(fig,'Source: original-course five-cutoff replay | Floden (2025), DOI 10.1002/berj.4069','The same 74 exams appear at every cutoff; these are not 75 separate students or AI-issued official grades.')
save(fig,'N1_Floden_Five_Actual_Course_Thresholds')

# B. Two-human reference discrepancy distribution (aggregate replay A466, pinned source)
hist=DATA['N2_human_score_diff']['frequency']
assert sum(hist)==1000 and sum(i*v for i,v in enumerate(hist))==1827
fig=plt.figure(figsize=(13.6,7.6))
heading(fig,'N2','How much do two human markers disagree?','GradeAgentOps: 1,000 matched student-question responses; two independent expert markers, scores 0-10.')
ax=fig.add_axes([.11,.20,.63,.53]);xx=np.arange(8)
colors=[TEAL]+[BLUE]*7
ax.bar(xx,hist,width=.67,color=colors)
for x,y in zip(xx,hist):ax.text(x,y+8,f'{y}',ha='center',color=NAVY,fontsize=11,weight='bold')
ax.set(xlabel='Absolute difference between human scores (points)',ylabel='Number of matched responses',xticks=xx,ylim=(0,345))
ax.grid(axis='y',color=LIGHT);ax.set_axisbelow(True)
for s in ['top','right']:ax.spines[s].set_visible(False)
fig.text(.80,.68,'1.827',fontsize=31,weight='bold',color=NAVY,ha='center')
fig.text(.80,.615,'mean absolute difference',fontsize=11,color=MUTED,ha='center')
fig.text(.80,.485,'16.7%',fontsize=26,weight='bold',color=TEAL,ha='center')
fig.text(.80,.425,'exact human-human agreement',fontsize=10.5,color=MUTED,ha='center')
foot(fig,'Source: Anghel et al. (2026), DOI 10.3390/ai7060198 | pinned public two-rater files; aggregate-only audit','These are 1,000 answers from 100 students, not 1,000 students; neither human is independently certified as correct.')
save(fig,'N2_Human_Human_ScoreDifference_Distribution')

# C. G0-G6 categorical map: status nonordinal, all cells from original 19x7 panel
m=pd.DataFrame(DATA['N3_matrix']['status_rows'],columns=DATA['N3_matrix']['gate_names']);m.insert(0,'ID',DATA['N3_matrix']['report_ids'])
assert list(m.columns)==['ID']+['G'+str(i) for i in range(7)] and len(m)==19
states=['O','P','NR','NA','U']; statusc={'O':BLUE,'P':TEAL,'NR':'#CBD5DC','NA':'#F8FAFC','U':ORANGE}
assert all(v in states for v in m.iloc[:,1:].to_numpy().ravel())
ctg={g:dict(Counter(m[g])) for g in m.columns[1:]}
assert ctg['G6']=={'NR':12,'P':6,'NA':1}
fig=plt.figure(figsize=(13.6,9.7))
heading(fig,'N3','What evidence was reported across the selected studies?','Original 19-report, 133-cell G0-G6 source-to-claim annotations. Categories are descriptive, not ordinal.')
ax=fig.add_axes([.18,.19,.56,.60]);arr=m.iloc[:,1:].to_numpy();ax.set_xlim(0,7);ax.set_ylim(19,0)
for i,row in enumerate(arr):
    for j,v in enumerate(row):
        ax.add_patch(Rectangle((j,i),1,1,facecolor=statusc[v],edgecolor='white',linewidth=1.7))
        ax.text(j+.5,i+.5,v,color='white' if v in ('O','P') else INK,fontsize=10.2,weight='bold',ha='center',va='center')
ax.set_xticks(np.arange(7)+.5,labels=['G0','G1','G2','G3','G4','G5','G6'])
ax.set_yticks(np.arange(19)+.5,labels=m['ID'].tolist());ax.tick_params(axis='both',length=0)
ax.xaxis.tick_top();ax.set_aspect('auto')
for s in ax.spines.values():s.set_visible(False)
fig.legend(handles=[Patch(facecolor=statusc[c],edgecolor='#9FADB7',label=lab) for c,lab in [('O','O = observed'),('P','P = partial proxy'),('NR','NR = not reported'),('NA','NA = not applicable'),('U','U = unverified')]],loc='lower center',bbox_to_anchor=(.50,.128),ncol=5,frameon=False,fontsize=9.8)
fig.text(.865,.57,'G6',fontsize=23,color=NAVY,weight='bold',ha='center')
fig.text(.865,.495,'0 observed',fontsize=12,color=NAVY,weight='bold',ha='center')
fig.text(.865,.445,'6 partial',fontsize=11,color=TEAL,ha='center')
fig.text(.865,.403,'12 not reported',fontsize=10,color=MUTED,ha='center')
fig.text(.865,.361,'1 not applicable',fontsize=10,color=MUTED,ha='center')
fig.add_artist(plt.Line2D([.06,.94],[.107,.107],transform=fig.transFigure,color=LIGHT,lw=1.5))
fig.text(.06,.083,'Source: frozen original 19x7 matrix, reproduced unchanged; G0-G6 definitions in Table 2 / Appendix E.',fontsize=9.3,color=MUTED)
fig.text(.06,.054,'No field-wide prevalence inference; a missing endpoint is not evidence that a study or a review process failed.',fontsize=9.5,color=NAVY,weight='bold')
save(fig,'N3_Source_To_Claim_Gate_Matrix')

# D. New derived Cruz close-vs-boundary cross table; independent two-pass checks.
ct=np.array(DATA['N4_cruz']['counts'],dtype=int)
assert ct.tolist()==[[236,66],[29,31]], 'Figure N4 source-locked cross tab mismatch'
fig=plt.figure(figsize=(13.6,7.6))
heading(fig,'N4','Close numerical marks can still cross a chosen boundary','Cruz: 362 paired instructor-AI marks; cutoff 4.0/5 is hypothetical, not a documented course rule.')
ax=fig.add_axes([.20,.245,.61,.46]);ax.set_xlim(0,2);ax.set_ylim(2,0)
clr=[['#EAF3F5','#FCE6D8'],['#EEF2F5','#F8D2C5']]
for i in range(2):
 for j in range(2):
  ax.add_patch(Rectangle((j+.01,i+.01),.98,.98,facecolor=clr[i][j],edgecolor='white',lw=5))
  v=int(ct[i,j]);ax.text(j+.5,i+.44,str(v),ha='center',va='center',fontsize=35,color=NAVY if j==0 else RED,weight='bold')
  ax.text(j+.5,i+.79,f'{v/362:.1%} of all pairs',ha='center',va='center',fontsize=11,color=MUTED)
ax.set_xticks([.5,1.5],['Same side of 4.0','Opposite sides of 4.0']);ax.set_yticks([.5,1.5],['Within 0.5 point','More than 0.5 point'])
ax.xaxis.tick_top();ax.tick_params(axis='both',length=0,labelsize=11)
for s in ax.spines.values():s.set_visible(False)
fig.text(.50,.165,'66 of 302 close pairs (21.9%) still cross the illustrative boundary.',fontsize=14,color=NAVY,weight='bold',ha='center')
foot(fig,'Source: source-locked Cruz original workbook from Zenodo v2, DOI 10.5281/zenodo.21823096; independent cross-tab','Source-derived cross-tabulation; not an official pass/fail error rate or a new student cohort.')
save(fig,'N4_Cruz_CloseScores_Versus_Boundary')

# E. GradeAgentOps human threshold sensitivity; alternative/companion, same raw E1/E2 pairs
Ts=DATA['N5_human_thresholds']['thresholds'];e1=np.array(DATA['N5_human_thresholds']['E1_above_E2_below']);e2=np.array(DATA['N5_human_thresholds']['E2_above_E1_below'])
assert (e1+e2).tolist()==[213,224,249,249,232,196]
fig=plt.figure(figsize=(13.6,7.6))
heading(fig,'N5','Human-human category disagreements depend on the cutoff','GradeAgentOps: same 1,000 human-scored answer pairs reused at six illustrative score thresholds.')
ax=fig.add_axes([.125,.22,.73,.49]);xx=np.arange(len(Ts));ax.bar(xx,e1,width=.64,color=BLUE,label='Only E1 above threshold')
ax.bar(xx,e2,bottom=e1,width=.64,color=ORANGE,label='Only E2 above threshold')
for x,s in zip(xx,e1+e2):ax.text(x,s+8,str(s),ha='center',fontsize=11.5,weight='bold',color=NAVY)
ax.set(xticks=xx,xticklabels=[f'{t}/10' for t in Ts],ylim=(0,300),xlabel='Hypothetical classification threshold',ylabel='Discordant response pairs (of 1,000)')
ax.grid(axis='y',color=LIGHT);ax.set_axisbelow(True)
for s in ['top','right']:ax.spines[s].set_visible(False)
fig.legend(handles=[Patch(facecolor=BLUE,label='E1 above, E2 below'),Patch(facecolor=ORANGE,label='E2 above, E1 below')],loc='upper left',bbox_to_anchor=(.121,.786),frameon=False,ncol=2,fontsize=11)
foot(fig,'Source: Anghel et al. (2026), DOI 10.3390/ai7060198; pinned two-human-score raw audit at 2026-05-18 commit','Cutoffs are analytical probes, not officially used grading rules; the same responses contribute to every bar.')
save(fig,'N5_Human_Human_Illustrative_Threshold_Sensitivity')



print('R140 aggregate-to-figure rebuild PASS: five charts, source-data checks, no raw student records')

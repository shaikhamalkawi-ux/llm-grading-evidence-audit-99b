#!/usr/bin/env python3
"""R134: reproduce original-policy Floden threshold counts from separately obtained public-appendix CSV.

This package intentionally omits the original score-pair records. Create a CSV by transcribing
or downloading the open-access article's three-course appendix; rows must contain:
course,ai_score,human_score,ai_grade,human_grade. Values are original /60 score points.
No new models are run. The reference human marks are not adjudicated truth.
"""
import argparse,csv,json,collections
from pathlib import Path

THRESHOLDS=(('F/E',50,'E'),('E/D',60,'D'),('D/C',68,'C'),('C/B',75,'B'),('B/A',85,'A'))
RANK={g:i for i,g in enumerate('FEDCBA')}
EXPECTED={50:(12,10,2),60:(19,14,5),68:(21,13,8),75:(17,9,8),85:(6,3,3)}

def grade(num):
 p=100*float(num)/60
 return 'A' if p>=85 else 'B' if p>=75 else 'C' if p>=68 else 'D' if p>=60 else 'E' if p>=50 else 'F'

def check(source):
 rows=list(csv.DictReader(Path(source).open(newline='',encoding='utf-8-sig')))
 if len(rows)!=74:raise AssertionError(f'Expected 74 published exam records; got {len(rows)}')
 counts=collections.Counter(r['course'] for r in rows)
 if sorted(counts.values())!=[22,25,27]:raise AssertionError(f'Course sizes mismatch: {counts}')
 for i,r in enumerate(rows,1):
  for lab,score in [('ai_grade','ai_score'),('human_grade','human_score')]:
   if r[lab]!=grade(r[score]):raise AssertionError(f'Grade-label policy mismatch, record {i} {lab}')
 results=[]
 for label,pct,above in THRESHOLDS:
  left=RANK[above]
  ah=[(RANK[r['ai_grade']]>=left,RANK[r['human_grade']]>=left) for r in rows]
  first=sum(a and not h for a,h in ah); second=sum(h and not a for a,h in ah)
  row={'boundary':label,'percent':pct,'discordant':first+second,'ai_above':first,'human_above':second}
  if (row['discordant'],first,second)!=EXPECTED[pct]:raise AssertionError(f'Original boundary result mismatch: {row}')
  results.append(row)
 exact=sum(r['ai_grade']==r['human_grade'] for r in rows)
 if exact!=22:raise AssertionError(f'Exact six-grade agreement expected 22/74; got {exact}')
 return {'n_exam_records':len(rows),'exact_AF':exact,'n_label_consistency_checks':148,'per_boundary':results,'sum_boundary_events_not_independent_records':sum(x['discordant'] for x in results),'n_unique_grade_disagreements':len(rows)-exact}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('csv',help='Local CSV transcribed from Wiley published 74-row appendix');p.add_argument('--json',default=None)
 args=p.parse_args();out=check(args.csv)
 if args.json:Path(args.json).write_text(json.dumps(out,indent=2))
 print(json.dumps(out,indent=2))

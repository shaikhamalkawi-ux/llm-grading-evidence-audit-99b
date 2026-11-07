#!/usr/bin/env python3
"""Replays the published EvalHack Table 12 route matrix. No raw student data."""
from fractions import Fraction
from pathlib import Path
import json
from decimal import Decimal
f_out, f_in, u_out, u_in = 125, 205, 218, 452
n = f_out+f_in+u_out+u_in
assert (n,f_out+u_out,f_in+u_in)==(1000,343,657)
assert (f_out+f_in,u_out+u_in)==(330,670)
precision=Fraction(f_out,f_out+f_in)
recall=Fraction(f_out,f_out+u_out)
base=Fraction(f_in+u_in,n)
best=Fraction(f_in+u_in+f_out,n)
assert best==Fraction(782,1000) and (n-(f_in+u_in+f_out))==218
out={'inputs':{'flagged_outside':f_out,'flagged_inside':f_in,'unflagged_outside':u_out,'unflagged_inside':u_in,'n_answers':n},'base_within_tolerance_fraction':float(base),'flagged_fraction':float(Fraction(f_out+f_in,n)),'routing_precision':float(precision),'routing_recall':float(recall),'ideal_flag_only_within_fraction':float(best),'unflagged_outside_count':u_out,'claim_status':'CONDITIONAL_SCENARIO_NOT_OBSERVED_CORRECTION','source':'EvalHack original Table 12, A08 CA10, PDF p.24'}
Path(__file__).with_name('A11_evalhack_replay_result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

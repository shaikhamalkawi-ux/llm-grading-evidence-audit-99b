#!/usr/bin/env python3
"""Published-summary numerical audit only: no raw student records are accessed.
The printed values are not presumed to share an identical parsing rule.
"""
import json
from pathlib import Path
p=Path(__file__).with_name('evalhack_cross_table_check_results.json')
N=1000
main_A1,main_A2=3.57,2.53
ablation_A1,ablation_A2=3.425,2.077
strict_all_four=341
printed_mean_valid_k=3.999
maximum_if_same_exact_rule=(strict_all_four*4+(N-strict_all_four)*3)/N
out={
 'source': 'Anghel et al. 2026 EvalHack, Information 17(3), Article 297, DOI 10.3390/info17030297',
 'reporting_scope': 'Published tables only; no dataset reanalysis or newly observed results',
 'sources': {'Table 4 page14': {'n':1000,'A1':main_A1,'A2':main_A2},
             'Table 10 page23 default permissive parsing':{'n':1000,'A1':ablation_A1,'A2':ablation_A2},
             'Table 5 page16':{'mean_accepted_clean_votes':printed_mean_valid_k},
             'Section 3.7 page23':{'all_four_strict_clean_items':strict_all_four}},
 'difference_main_minus_ablation':{'A1':round(main_A1-ablation_A1,3),'A2':round(main_A2-ablation_A2,3)},
 'if_same_exact_strict_definition':{'max_mean_clean_votes':maximum_if_same_exact_rule,
                                     'printed_mean_clean_votes':printed_mean_valid_k,
                                     'cannot_simultaneously_hold':printed_mean_valid_k>maximum_if_same_exact_rule},
 'claim_status':'HOLD: exact parser, denominator and computation relation unresolved; no accusation of source error',
}
assert out['difference_main_minus_ablation']=={'A1':0.145,'A2':0.453}
assert round(maximum_if_same_exact_rule,3)==3.341
p.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('Published-summary discrepancy checks PASS; original-source reconciliation remains HOLD')

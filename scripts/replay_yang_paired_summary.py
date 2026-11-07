#!/usr/bin/env python3
"""Summary-statistic paired t reconstruction of Yang (2024), NOT row-level replay.

Source: Yang, Shanlax Int J Educ 12(4):49--59, Tables 3/4/6; n=82.
Pure standard-library incomplete-beta implementation.  In the original,
independent-samples t-test p=.183 was run on observations matched by essay.
The rounded summaries limit precision. Do NOT call this exact paired-data test.
"""
import json
import math
from pathlib import Path


def continued_fraction(a: float, b: float, x: float) -> float:
    # Stable modified Lentz iteration for the incomplete beta continued fraction.
    EPS, FPMIN = 3.0e-14, 1.0e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < FPMIN:
        d = FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, 201):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < EPS:
            return h
    raise ArithmeticError('incomplete-beta continued fraction did not converge')


def regularized_incomplete_beta(x: float, a: float, b: float) -> float:
    if x < 0 or x > 1:
        raise ValueError('x must be between zero and one')
    if x == 0.0:
        return 0.0
    if x == 1.0:
        return 1.0
    front = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                     + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * continued_fraction(a, b, x) / a
    return 1.0 - front * continued_fraction(b, a, 1.0 - x) / b


def student_two_sided_pvalue(t: float, df: int) -> float:
    z = df / (df + t * t)
    return regularized_incomplete_beta(z, df / 2.0, 0.5)


n = 82
mean_human, mean_model = 71.37, 73.45
sd_human, sd_model, correlation = 8.32, 11.34, 0.508
paired_sd = math.sqrt(sd_human**2 + sd_model**2 - 2 * correlation * sd_human * sd_model)
t_stat = (mean_model - mean_human) / (paired_sd / math.sqrt(n))
p_approx = student_two_sided_pvalue(t_stat, n-1)
assert abs(p_approx - 0.06575570835128033) < 3e-11
assert p_approx > 0.05
result = {
    'source': 'Yang (2024), original 11-page PDF, Tables 3 and 6',
    'input_level': 'published rounded statistics only, NOT original row-level data',
    'n_matched_essays': n, 'human_mean': mean_human, 'model_mean': mean_model,
    'human_sd': sd_human, 'model_sd': sd_model, 'human_model_r': correlation,
    'paired_difference_sd_approx': paired_sd, 'paired_t_approx': t_stat,
    'degrees_of_freedom': n - 1,
    'two_sided_p_approx': p_approx,
    'original_published_independent_samples_p': 0.183,
    'source_independence_issue': 'both scores refer to each same essay',
    'inference': 'both p values exceed 0.05; neither proves equivalence or source correctness',
    'raw_data_available_offsite': 'https://doi.org/10.17632/8fbzsg82p9.1',
    'raw_data_not_acquired': True,
}
Path(__file__).with_name('A17_yang_summary_replay.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

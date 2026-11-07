#!/usr/bin/env python3
"""Verify exact appeal-count arithmetic from Azad et al. 2020 original publisher text.
Source: DOI 10.1007/978-3-030-52237-7_2, Results 'Appeals to Human Graders'.
These counts are students whose exam question was not awarded credit after up to 3 tries.
"""
from fractions import Fraction
assert 69+134==203
assert 4+3==7 and (69-4)+(134-3)==196
assert Fraction(4,7)+Fraction(3,7)==1
assert round(float(Fraction(4,69))*100,2)==5.80
assert round(float(Fraction(4,7))*100,2)==57.14
assert round(float(Fraction(3,7))*100,2)==42.86
assert round(float(Fraction(69,203))*100,2)==33.99
assert round(float(Fraction(7,203))*100,2)==3.45
print('A40 AZAD APPEAL DENOMINATORS: PASS; 69 appealed, 134 nonappealed, 7 erroneously denied, 4 identified by appeals, 3 missed')

def federal_tax(income, annual=True):
    federal_brackets = {10: 10275, 12: 41775, 22: 89075, 24: 170050, 32: 215950, 35: 539900} #upper bound for each bracket
    tax = 0
    if not annual:
        for key in federal_brackets:
            federal_brackets[key] /= 26
        
    for key, val in federal_brackets.items():
        print(key, val)
        if income > val:
            tax += (income - val) * (key/100)

    return tax

print(federal_tax(115000))

print(federal_tax(4423, False)*26)
print('asldfjalskdfj')

tot = (115000 - 89075)*.24
tot += (89075 - 41775)*.22
tot += (41775 - 10275)*.12
tot += (10275)*.10
print(tot)
tot/26
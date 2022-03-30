NUM_OF_NODES = 15
CONTACTS = [{'from': 0, 'to': 1, 'ts': 0, 'pf': 0.800000}, {'from': 1, 'to': 2, 'ts': 1, 'pf': 0.800000}, {'from': 2, 'to': 3, 'ts': 2, 'pf': 0.800000}, {'from': 3, 'to': 0, 'ts': 4, 'pf': 0.800000}, {'from': 0, 'to': 1, 'ts': 5, 'pf': 0.800000}, {'from': 1, 'to': 2, 'ts': 6, 'pf': 0.800000}, {'from': 2, 'to': 3, 'ts': 7, 'pf': 0.800000}, {'from': 3, 'to': 0, 'ts': 8, 'pf': 0.800000}, {'from': 4, 'to': 3, 'ts': 1, 'pf': 0.800000}, {'from': 4, 'to': 3, 'ts': 3, 'pf': 0.800000}, {'from': 5, 'to': 4, 'ts': 0, 'pf': 0.800000}, {'from': 5, 'to': 4, 'ts': 2, 'pf': 0.800000}, {'from': 9, 'to': 4, 'ts': 1, 'pf': 0.800000}, {'from': 9, 'to': 4, 'ts': 3, 'pf': 0.800000}, {'from': 2, 'to': 9, 'ts': 2, 'pf': 0.800000}, {'from': 2, 'to': 9, 'ts': 5, 'pf': 0.800000}, {'from': 2, 'to': 9, 'ts': 8, 'pf': 0.800000}, {'from': 9, 'to': 2, 'ts': 2, 'pf': 0.800000}, {'from': 9, 'to': 2, 'ts': 5, 'pf': 0.800000}, {'from': 9, 'to': 2, 'ts': 8, 'pf': 0.800000}, {'from': 9, 'to': 10, 'ts': 1, 'pf': 0.800000}, {'from': 9, 'to': 10, 'ts': 3, 'pf': 0.800000}, {'from': 3, 'to': 5, 'ts': 0, 'pf': 0.800000}, {'from': 3, 'to': 5, 'ts': 4, 'pf': 0.800000}, {'from': 3, 'to': 5, 'ts': 6, 'pf': 0.800000}, {'from': 5, 'to': 3, 'ts': 0, 'pf': 0.800000}, {'from': 5, 'to': 3, 'ts': 4, 'pf': 0.800000}, {'from': 5, 'to': 3, 'ts': 6, 'pf': 0.800000}, {'from': 5, 'to': 6, 'ts': 2, 'pf': 0.800000}, {'from': 5, 'to': 6, 'ts': 5, 'pf': 0.800000}, {'from': 5, 'to': 6, 'ts': 3, 'pf': 0.800000}, {'from': 6, 'to': 0, 'ts': 0, 'pf': 0.800000}, {'from': 6, 'to': 0, 'ts': 2, 'pf': 0.800000}, {'from': 6, 'to': 0, 'ts': 5, 'pf': 0.800000}, {'from': 10, 'to': 2, 'ts': 2, 'pf': 0.800000}, {'from': 10, 'to': 2, 'ts': 4, 'pf': 0.800000}, {'from': 11, 'to': 10, 'ts': 0, 'pf': 0.800000}, {'from': 11, 'to': 10, 'ts': 2, 'pf': 0.800000}, {'from': 7, 'to': 1, 'ts': 2, 'pf': 0.800000}, {'from': 7, 'to': 1, 'ts': 5, 'pf': 0.800000}, {'from': 8, 'to': 6, 'ts': 0, 'pf': 0.800000}, {'from': 8, 'to': 6, 'ts': 4, 'pf': 0.800000}, {'from': 11, 'to': 7, 'ts': 0, 'pf': 0.800000}, {'from': 11, 'to': 7, 'ts': 2, 'pf': 0.800000}, {'from': 8, 'to': 7, 'ts': 1, 'pf': 0.800000}, {'from': 8, 'to': 7, 'ts': 3, 'pf': 0.800000}, {'from': 8, 'to': 7, 'ts': 7, 'pf': 0.800000}, {'from': 0, 'to': 8, 'ts': 1, 'pf': 0.800000}, {'from': 0, 'to': 8, 'ts': 4, 'pf': 0.800000}, {'from': 0, 'to': 8, 'ts': 7, 'pf': 0.800000}, {'from': 8, 'to': 0, 'ts': 1, 'pf': 0.800000}, {'from': 8, 'to': 0, 'ts': 4, 'pf': 0.800000}, {'from': 8, 'to': 0, 'ts': 7, 'pf': 0.800000}, {'from': 11, 'to': 1, 'ts': 0, 'pf': 0.800000}, {'from': 11, 'to': 1, 'ts': 3, 'pf': 0.800000}, {'from': 11, 'to': 1, 'ts': 6, 'pf': 0.800000}, {'from': 11, 'to': 1, 'ts': 7, 'pf': 0.800000}, {'from': 1, 'to': 11, 'ts': 0, 'pf': 0.800000}, {'from': 1, 'to': 11, 'ts': 3, 'pf': 0.800000}, {'from': 1, 'to': 11, 'ts': 6, 'pf': 0.800000}, {'from': 1, 'to': 11, 'ts': 7, 'pf': 0.800000}, {'from': 12, 'to': 11, 'ts': 0, 'pf': 0.000000}, {'from': 11, 'to': 12, 'ts': 0, 'pf': 0.000000}, {'from': 12, 'to': 11, 'ts': 2, 'pf': 0.000000}, {'from': 11, 'to': 12, 'ts': 2, 'pf': 0.000000}, {'from': 12, 'to': 11, 'ts': 4, 'pf': 0.000000}, {'from': 11, 'to': 12, 'ts': 4, 'pf': 0.000000}, {'from': 12, 'to': 11, 'ts': 6, 'pf': 0.000000}, {'from': 11, 'to': 12, 'ts': 6, 'pf': 0.000000}, {'from': 12, 'to': 11, 'ts': 8, 'pf': 0.000000}, {'from': 11, 'to': 12, 'ts': 8, 'pf': 0.000000}, {'from': 12, 'to': 9, 'ts': 0, 'pf': 0.000000}, {'from': 9, 'to': 12, 'ts': 0, 'pf': 0.000000}, {'from': 12, 'to': 9, 'ts': 2, 'pf': 0.000000}, {'from': 9, 'to': 12, 'ts': 2, 'pf': 0.000000}, {'from': 12, 'to': 9, 'ts': 4, 'pf': 0.000000}, {'from': 9, 'to': 12, 'ts': 4, 'pf': 0.000000}, {'from': 12, 'to': 9, 'ts': 6, 'pf': 0.000000}, {'from': 9, 'to': 12, 'ts': 6, 'pf': 0.000000}, {'from': 12, 'to': 9, 'ts': 8, 'pf': 0.000000}, {'from': 9, 'to': 12, 'ts': 8, 'pf': 0.000000}, {'from': 13, 'to': 8, 'ts': 0, 'pf': 0.000000}, {'from': 8, 'to': 13, 'ts': 0, 'pf': 0.000000}, {'from': 13, 'to': 8, 'ts': 2, 'pf': 0.000000}, {'from': 8, 'to': 13, 'ts': 2, 'pf': 0.000000}, {'from': 13, 'to': 8, 'ts': 4, 'pf': 0.000000}, {'from': 8, 'to': 13, 'ts': 4, 'pf': 0.000000}, {'from': 13, 'to': 8, 'ts': 6, 'pf': 0.000000}, {'from': 8, 'to': 13, 'ts': 6, 'pf': 0.000000}, {'from': 13, 'to': 8, 'ts': 8, 'pf': 0.000000}, {'from': 8, 'to': 13, 'ts': 8, 'pf': 0.000000}, {'from': 13, 'to': 5, 'ts': 0, 'pf': 0.000000}, {'from': 5, 'to': 13, 'ts': 0, 'pf': 0.000000}, {'from': 13, 'to': 5, 'ts': 2, 'pf': 0.000000}, {'from': 5, 'to': 13, 'ts': 2, 'pf': 0.000000}, {'from': 13, 'to': 5, 'ts': 4, 'pf': 0.000000}, {'from': 5, 'to': 13, 'ts': 4, 'pf': 0.000000}, {'from': 13, 'to': 5, 'ts': 6, 'pf': 0.000000}, {'from': 5, 'to': 13, 'ts': 6, 'pf': 0.000000}, {'from': 13, 'to': 5, 'ts': 8, 'pf': 0.000000}, {'from': 5, 'to': 13, 'ts': 8, 'pf': 0.000000}, {'from': 14, 'to': 6, 'ts': 0, 'pf': 0.000000}, {'from': 6, 'to': 14, 'ts': 0, 'pf': 0.000000}, {'from': 14, 'to': 6, 'ts': 2, 'pf': 0.000000}, {'from': 6, 'to': 14, 'ts': 2, 'pf': 0.000000}, {'from': 14, 'to': 6, 'ts': 4, 'pf': 0.000000}, {'from': 6, 'to': 14, 'ts': 4, 'pf': 0.000000}, {'from': 14, 'to': 6, 'ts': 6, 'pf': 0.000000}, {'from': 6, 'to': 14, 'ts': 6, 'pf': 0.000000}, {'from': 14, 'to': 6, 'ts': 8, 'pf': 0.000000}, {'from': 6, 'to': 14, 'ts': 8, 'pf': 0.000000}, {'from': 14, 'to': 10, 'ts': 0, 'pf': 0.000000}, {'from': 10, 'to': 14, 'ts': 0, 'pf': 0.000000}, {'from': 14, 'to': 10, 'ts': 2, 'pf': 0.000000}, {'from': 10, 'to': 14, 'ts': 2, 'pf': 0.000000}, {'from': 14, 'to': 10, 'ts': 4, 'pf': 0.000000}, {'from': 10, 'to': 14, 'ts': 4, 'pf': 0.000000}, {'from': 14, 'to': 10, 'ts': 6, 'pf': 0.000000}, {'from': 10, 'to': 14, 'ts': 6, 'pf': 0.000000}, {'from': 14, 'to': 10, 'ts': 8, 'pf': 0.000000}, {'from': 10, 'to': 14, 'ts': 8, 'pf': 0.000000}, ]

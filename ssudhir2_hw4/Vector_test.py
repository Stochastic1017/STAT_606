# Test __init__
v1 = Vector(3, [1, 2, 3])
assert isinstance(v1, Vector), "Error in __init__"
v2 = Vector(3, (1, 2, 3))
assert isinstance(v2, Vector), "Error in __init__"
v3 = Vector(3)
assert isinstance(v3, Vector), "Error in __init__"

# Test __compare__
v4 = Vector(3, [1, 2, 3])
v5 = Vector(3, [1, 2, 3])
v6 = Vector(3, [1, 2, 4])
v7 = Vector(3, [1, 2, 2])
assert v4 == v5, "Error in __compare__"
assert v4 < v6, "Error in __compare__"
assert v4 <= v5, "Error in __compare__"
assert v4 <= v6, "Error in __compare__"
assert v4 > v7, "Error in __compare__"
assert v4 >= v7, "Error in __compare__"
assert v4 >= v5, "Error in __compare__"

# Test __operation__
v8 = Vector(3, [1, 2, 3])
v9 = Vector(3, [4, 5, 6])
assert (v8 + v9).get_entries() == (5, 7, 9), "Error in __operation__"
assert (v8 - v9).get_entries() == (-3, -3, -3), "Error in __operation__"

# Test dot
v10 = Vector(3, [1, 2, 3])
v11 = Vector(3, [4, 5, 6])
assert v10.dot(v11) == 32, "Error in dot"

# Test __mul__
v12 = Vector(3, [1, 2, 3])
v13 = Vector(3, [4, 5, 6])
assert (v12 * v13).get_entries() == (4, 10, 18), "Error in __mul__"
assert (v12 * 2).get_entries() == (2, 4, 6), "Error in __mul__"

# Test norm
v14 = Vector(3, [1, 2, 3])
assert v14.norm() == 3.7416573867739413, "Error in norm"
assert v14.norm(1) == 6, "Error in norm"
assert v14.norm(3) == 3.3019272488946263, "Error in norm"

# Test __init__
try:
    v = Vector(0, [])
except ValueError:
    pass
else:
    assert False, "Error in __init__: should not allow zero-dimensional vector"

try:
    v = Vector(3, [1, 2])
except ValueError:
    pass
else:
    assert False, "Error in __init__: dimension and length of entries do not match"

# Test __compare__
try:
    v1 = Vector(3, [1, 2, 3])
    v1 == Vector(2, [1, 2])
except ValueError:
    pass
else:
    assert False, "Error in __compare__: should not compare vectors of different dimensions"

# Test __operation__
try:
    v1 = Vector(3, [1, 2, 3])
    v1 + Vector(2, [1, 2])
except ValueError:
    pass
else:
    assert False, "Error in __operation__: should not add vectors of different dimensions"

# Test dot
try:
    v1 = Vector(3, [1, 2, 3])
    v1.dot(Vector(2, [1, 2]))
except ValueError:
    pass
else:
    assert False, "Error in dot: should not calculate dot product of vectors of different dimensions"

# Test __mul__
try:
    v1 = Vector(3, [1, 2, 3])
    v1 * Vector(2, [1, 2])
except ValueError:
    pass
else:
    assert False, "Error in __mul__: should not multiply vectors of different dimensions"

# Test norm
try:
    v1 = Vector(3, [1, 2, 3])
    v1.norm(-1)
except ValueError:
    pass
else:
    assert False, "Error in norm: should not calculate norm with negative p"
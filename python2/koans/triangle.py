#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Triangle Project Code.


# triangle(a, b, c) analyzes the lengths of the sides of a triangle
# (represented by a, b and c) and returns the type of triangle.
#
# It returns:
#   'equilateral'  if all sides are equal
#   'isosceles'    if exactly 2 sides are equal
#   'scalene'      if no sides are equal
#
# The tests for this method can be found in
#   about_triangle_project.py
# and
#   about_triangle_project_2.py
#
def triangle(a, b, c):
    if any(map(lambda x:x <= 0,(a,b,c))):
        raise TriangleError
    max_border = max(a,b,c)
    if sum((a,b,c)) - max_border <= max_border:
        raise TriangleError

    if a == b == c:
        return 'equilateral'
    if len(set((a,b,c))) is 2:
        return 'isosceles'
    return 'scalene'

# Error class used in part 2.  No need to change this code.
class TriangleError(StandardError):
    pass

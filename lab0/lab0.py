# This is the file you'll use to submit most of Lab 0.

# Certain problems may ask you to modify other files to accomplish a certain
# task. There are also various other files that make the problem set work, and
# generally you will _not_ be expected to modify or even understand this code.
# Don't get bogged down with unnecessary work.


# Section 1: Problem set logistics ___________________________________________

# This is a multiple choice question. You answer by replacing
# the symbol 'fill-me-in' with a number, corresponding to your answer.

# You get to check multiple choice answers using the tester before you
# submit them! So there's no reason to worry about getting them wrong.
# Often, multiple-choice questions will be intended to make sure you have the
# right ideas going into the problem set. Run the tester right after you
# answer them, so that you can make sure you have the right answers.

# What version of Python do we *recommend* (not "require") for this course?
#   1. Python v2.3
#   2. Python v2.5, Python v2.6, or Python v2.7
#   3. Python v3.0
# Fill in your answer in the next line of code ("1", "2", or "3"):

ANSWER_1 = 2


# Section 2: Programming warmup _____________________________________________

# Problem 2.1: Warm-Up Stretch

def cube(x):
    return x*x*x

def factorial(x):
    if x==0:
        return 1
    if x<0:
        raise valueError("Cant factorial a negative numer")
    prod = 1
    for i in xrange(x,0,-1):
        prod*=i
    return prod
        

def count_pattern(pattern, lst):
    matches = 0
    lastStartIndex = len(lst)-len(pattern)
    for i in xrange(0,lastStartIndex+1):

        if pattern == lst[i:i+len(pattern)]:
            matches+=1
    return matches


# Problem 2.2: Expression depth

def depth(expr):
    if isinstance(expr,str) or isinstance(expr,int) or isinstance(expr,float) or isinstance(expr,bool):  
        return 0
    maxD = 0
    itemD = 0
    for item in expr:
        if isinstance(item,str) or isinstance(item,int) or isinstance(item,float) or isinstance(item,bool) :
            itemD=0
        else:
            itemD=max(depth(item),1)
        if itemD>maxD:
            maxD = itemD
    return maxD+1
        


# Problem 2.3: Tree indexing

def tree_ref(tree, index):
    subTree = tree
    for i in xrange(len(index)-1):
        subTree = subTree[index[i]]
    return subTree[index[-1]]
        
        
        


# Section 3: Symbolic algebra

# Your solution to this problem doesn't go in this file.
# Instead, you need to modify 'algebra.py' to complete the distributer.

from algebra import Sum, Product, simplify_if_possible
from algebra_utils import distribution, encode_sumprod, decode_sumprod

# Section 4: Survey _________________________________________________________

# Please answer these questions inside the double quotes.

# When did you take 6.01?
WHEN_DID_YOU_TAKE_601 = "fall 2013, i think, sophomore fall"

# How many hours did you spend per 6.01 lab?
HOURS_PER_601_LAB = "24"

# How well did you learn 6.01?
HOW_WELL_I_LEARNED_601 = "pretty well"

# How many hours did this lab take?
HOURS = ""

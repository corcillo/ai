# 6.034 Lab 7 2015: Boosting (Adaboost)

from math import log as ln
INF = float('inf')

# Helper function for pick_best_classifier and adaboost
def fix_roundoff_error(inp, n=15):
    """inp can be a number, a list of numbers, or a dict whose values are numbers.
    * If inp is a number: Rounds the number to the nth decimal digit to reduce
        previous Python roundoff error.  Returns a float.
    * If inp is a list of numbers: Rounds each number as above.  Does not modify
        the original list.
    * If inp is a dictionary whose values are numbers: Rounds each value as
        above.  Does not modify the original dictionary."""
    fix_val = lambda val: round(abs(val),n)*[-1,1][val>=0]
    if isinstance(inp, list): return map(fix_val, inp)
    if isinstance(inp, dict): return {key: fix_val(inp[key]) for key in inp}
    return fix_val(inp)


#### BOOSTING (ADABOOST) #######################################################

def initialize_weights(training_points):
    """Assigns every training point a weight equal to 1/N, where N is the number
    of training points.  Returns a dictionary mapping points to weights."""
    initialWeight = 1.0/len(training_points)
    dict = {}
    for point in training_points:
        dict[point] = initialWeight
    return dict

def calculate_error_rates(point_to_weight, classifier_to_misclassified):
    #A classifiers error rate is just the sum of the weights of the points they misclassify
    """Given a dictionary mapping training points to their weights, and another
    dictionary mapping classifiers to the training points they misclassify,
    returns a dictionary mapping classifiers to their error rates."""
    classToError = {}
    for classifier in classifier_to_misclassified.keys():
        errorSum = 0
        for point in point_to_weight.keys():
            if point in classifier_to_misclassified[classifier]:
                errorSum += point_to_weight[point]
        classToError[classifier] = errorSum
    return classToError

def pick_best_classifier(classifier_to_error_rate, use_smallest_error=True):
    #best classifier is based on classifier error rates
    """Given a dictionary mapping classifiers to their error rates, returns the
    best* classifier.  Best* means 'smallest error rate' if use_smallest_error
    is True, otherwise 'error rate furthest from 1/2'."""
    if use_smallest_error:
        keys = classifier_to_error_rate.keys()[:]
        keys.sort()
        smallestKey = keys[0]
        smallestValue = INF
        for classifier in keys:
            val = classifier_to_error_rate[classifier]
            if val < smallestValue:
                smallestValue = val
                smallestKey = classifier
        return smallestKey
    else:
        keys = classifier_to_error_rate.keys()[:]
        keys.sort()
        smallestKey = keys[0]
        smallestValue = -INF
        for classifier in keys:
            prev = classifier_to_error_rate[classifier]
            val = fix_roundoff_error(abs(.5 - prev ))
            if val > smallestValue:
                smallestValue = val
                smallestKey = classifier
        return smallestKey

#a classifiers voting power is based on a function on error rate
def calculate_voting_power(error_rate):
    """Given a classifier's error rate (a number), returns the voting power
    (aka alpha, or coefficient) for that classifier."""
    if error_rate==0:
        return INF
    if error_rate == 1:
        return -INF
    return .5*ln((1-error_rate)/error_rate)

#H miscalculates point x if the sum of the lil classifiers(x) * their voting powers is negative
def is_good_enough(H, training_points, classifier_to_misclassified,
                   mistake_tolerance=0):
    """Given an overall classifier H, a list of all training points, a
    dictionary mapping classifiers to the training points they misclassify, and
    a mistake tolerance (the maximum number of allowed misclassifications),
    returns False if H misclassifies more points than the tolerance allows,
    otherwise True.  H is represented as a list of (classifier, voting_power)
    tuples."""
    mistakes = 0
    for point in training_points:
        Hx = 0
        for classifier,voting_power in H:
            if point in classifier_to_misclassified[classifier]:
                Hx-=voting_power
            else:
                Hx+=voting_power
        if Hx<=0:
            mistakes+=1
    return mistakes<=mistake_tolerance

def update_weights(point_to_weight, misclassified_points, error_rate):
    """Given a dictionary mapping training points to their old weights, a list
    of training points misclassified by the current weak classifier, and the
    error rate of the current weak classifier, returns a dictionary mapping
    training points to their new weights.  This function is allowed (but not
    required) to modify the input dictionary point_to_weight."""
    updatedPointToWeight = {}
    for point in point_to_weight.keys():
        if point in misclassified_points:
            updatedPointToWeight[point] = .5*(1.0/error_rate)*point_to_weight[point]
        else:
            updatedPointToWeight[point] = .5*(1.0/(1-error_rate))*point_to_weight[point];
    return updatedPointToWeight
def adaboost(training_points, classifier_to_misclassified,
             use_smallest_error=True, mistake_tolerance=0, max_num_rounds=INF):
    """Performs the Adaboost algorithm for up to max_num_rounds rounds.
    Returns the resulting overall classifier H, represented as a list of
    (classifier, voting_power) tuples."""
    H = []
    point_to_weight = initialize_weights(training_points)
    while max_num_rounds>0:
        max_num_rounds -= 1
        if is_good_enough(H, training_points,classifier_to_misclassified,mistake_tolerance) and len(H)!=0:
            return H
        classifier_to_error_rate = calculate_error_rates(point_to_weight, classifier_to_misclassified)
        bestClassifier = pick_best_classifier(classifier_to_error_rate, use_smallest_error)
        bestError = classifier_to_error_rate[bestClassifier]
        if fix_roundoff_error(bestError)==.5:
            return H
        bestVotingPower = calculate_voting_power(bestError)
        H.append((bestClassifier, bestVotingPower))
        point_to_weight = update_weights(point_to_weight, classifier_to_misclassified[bestClassifier], bestError)
    return H

#### SURVEY ####################################################################

NAME = "Rebecca Corcillo"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = "15"
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = ""

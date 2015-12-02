# 6.034 Lab 6 2015: Neural Nets & SVMs

from nn_problems import *
from svm_problems import *
from math import e
import math
import numpy as np

#### NEURAL NETS ###############################################################

# Wiring a neural net

nn_half = [1]

nn_angle = [2,1]

nn_cross = [2,2,1]

nn_stripe = [3,1]

nn_hexagon = [6,1]

# Optional problem; change TEST_NN_GRID to True to test locally
TEST_NN_GRID = False
nn_grid = []

# Helper functions
def stairstep(x, threshold=0):
    "Computes stairstep(x) using the given threshold (T)"
    return x>=threshold

def sigmoid(x, steepness=1, midpoint=0):
    "Computes sigmoid(x) using the given steepness (S) and midpoint (M)"
    return 1.0/(1+e**(-1*steepness*(x-midpoint)))
def accuracy(desired_output, actual_output):
    "Computes accuracy. If output is binary, accuracy ranges from -0.5 to 0."
    return -.5*(desired_output-actual_output)**2

# Forward propagation
def forward_prop(net, input_values, threshold_fn=stairstep):
    """Given a neural net and dictionary of input values, performs forward
    propagation with the given threshold function to compute binary output.
    This function should not modify the input net.  Returns a tuple containing:
    (1) the final output of the neural net
    (2) a dictionary mapping neurons to their immediate outputs"""
    neurons = net.topological_sort()
    outputValues = {}
    for neuron in neurons:
        output = 0 #maps nodes to their output values
        incomingWires = net.get_incoming_wires(neuron)
        for wire in incomingWires:
            if isinstance(wire.startNode,int):
                output+=wire.startNode*wire.weight
            elif input_values.get(str(wire.startNode))!=None:
                output+=input_values[str(wire.startNode)]*wire.weight
            elif outputValues.get(wire.startNode)!=None:
                output+=outputValues[wire.startNode]*wire.weight
        outputValues[neuron]=threshold_fn(output)

    return (outputValues[neurons[-1]],outputValues)


# Backward propagation
def calculate_deltas(net, input_values, desired_output):
    """Computes the update coefficient (delta_B) for each neuron in the
    neural net.  Uses sigmoid function to compute output.  Returns a dictionary
    mapping neuron names to update coefficient (delta_B values)."""
    finalOutput,outputValues = forward_prop(net, input_values, sigmoid)
    deltaBDict ={}
    backTop = net.topological_sort()[:]
    backTop.reverse()
    for neuron in backTop:
        oB = outputValues[neuron]
        if net.is_output_neuron(neuron):
            deltaBDict[neuron] = (1-oB)*oB*(desired_output-oB)
        else:
            wtSum = 0
            for wire in net.get_outgoing_wires(neuron):
                wtSum+=wire.weight*deltaBDict[wire.endNode]
            deltaBDict[neuron] = (1-oB)*oB*wtSum
    return deltaBDict

def update_weights(net, input_values, desired_output, r=1):
    """Performs a single step of back-propagation.  Computes delta_B values and
    weight updates for entire neural net, then updates all weights.  Uses
    sigmoid function to compute output.  Returns the modified neural net, with
    updated weights."""
    dBDict = calculate_deltas(net,input_values,desired_output)
    finalOutput,outputValues = forward_prop(net, input_values, sigmoid)
    for wire in net.get_wires():
        inputVal = 0
        if isinstance(wire.startNode,int):
            inputVal = wire.startNode
            wire.weight+=r*inputVal*dBDict[wire.endNode]
        elif input_values.get(str(wire.startNode))!=None:
            inputVal = input_values[str(wire.startNode)]
            wire.weight+=r*inputVal*dBDict[wire.endNode]
        elif not net.is_output_neuron(wire.startNode):
            wire.weight+=r*outputValues[wire.startNode]*dBDict[wire.endNode]
    return net
def back_prop(net, input_values, desired_output, r=1, accuracy_threshold=-.001):
    """Updates weights until accuracy surpasses minimum_accuracy.  Uses sigmoid
    function to compute output.  Returns a tuple containing:
    (1) the modified neural net, with trained weights
    (2) the number of iterations (that is, the number of weight updates)"""
    finalOutput,outputValues = forward_prop(net, input_values, sigmoid)
    acc = accuracy(desired_output,finalOutput)
    numIters = 0
    while acc < accuracy_threshold:
        net = update_weights(net, input_values, desired_output, r)
        finalOutput,outputValues = forward_prop(net, input_values, sigmoid)
        acc = accuracy(desired_output,finalOutput)
        numIters+=1
    return (net,numIters)


#### SUPPORT VECTOR MACHINES ###################################################

# Vector math
def dot_product(u, v):
    """Computes dot product of two vectors u and v, each represented as a tuple
    or list of coordinates.  Assume the two vectors are the same length."""
    sum = 0
    for i in xrange(len(u)):
        sum+=u[i]*v[i]
    return sum

def norm(v):
    sum = 0
    for i in xrange(len(v)):
        sum += v[i]**2
    return math.sqrt(sum)
#return float(np.linalg.norm(v))

# Equation 1
def positiveness(svm, point):
    "Computes the expression (w dot x + b) for the given point"
    prod = dot_product(svm.boundary.w,point.coords)
    return prod+svm.boundary.b
#    return np.add(prod,svm.boundary.b)

def classify(svm, point):
    """Uses given SVM to classify a Point.  Assumes that point's classification
    is unknown.  Returns +1 or -1, or 0 if point is on boundary"""
    res = positiveness(svm,point)
    if res==0:
        return 0
    if res>0:
        return 1
    else:
        return -1


# Equation 2
def margin_width(svm):
    "Calculate margin width based on current boundary."
    supportVectors = svm.support_vectors
    return 2.0/norm(svm.boundary.w)

# Equation 3
def check_gutter_constraint(svm):
    """Returns the set of training points that violate one or both conditions:
        * gutter constraint (positiveness == classification for support vectors)
        * training points must not be between the gutters
    Assumes that the SVM has support vectors assigned."""
    violators = set([])
    supportVectors  = svm.support_vectors
    for point in svm.training_points:
        positiv = positiveness(svm,point)

        if point in supportVectors:
            if point.classification!= positiv:
                violators.add(point)
        else:
            if abs(positiv) < 1:
                violators.add(point)
    return violators

# Equations 4, 5
def check_alpha_signs(svm):
    """Returns the set of training points that violate either condition:
        * all non-support-vector training points have alpha = 0
        * all support vectors have alpha > 0
    Assumes that the SVM has support vectors assigned, and that all training
    points have alpha values assigned."""
    violators = set([])
    svs = svm.support_vectors
    for v in svm.training_points:
        if v not in svs:
            if v.alpha!=0:
                violators.add(v)
        else:
            if v.alpha <= 0:
                violators.add(v)
    return violators

def check_alpha_equations(svm):
    """Returns True if both Lagrange-multiplier equations are satisfied,
    otherwise False.  Assumes that the SVM has support vectors assigned, and
    that all training points have alpha values assigned."""
    eq4Sum = 0
    eq5Sum = [0 for i in xrange(len(svm.training_points[0].coords))]
    for point in svm.training_points:
        ya = point.classification*point.alpha
        #print "ya: ",ya, " point coords: ",point.coords
        yax = scalar_mult(ya,point.coords)
        eq4Sum+=ya
        eq5Sum= vector_add(eq5Sum,yax)
    return eq4Sum==0 and np.array_equal(eq5Sum,svm.boundary.w)

# Classification accuracy
def misclassified_training_points(svm):
    """Returns the set of training points that are classified incorrectly
    using the current decision boundary."""
    violators = set([])
    for point in svm.training_points:
        positiv = positiveness(svm,point)
        if point.classification * positiv <= 0:
            violators.add(point)
    return violators



#### SURVEY ####################################################################

NAME = "Rebecca Corcillo"
COLLABORATORS = "None"
HOW_MANY_HOURS_THIS_LAB_TOOK = "15"
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = ""

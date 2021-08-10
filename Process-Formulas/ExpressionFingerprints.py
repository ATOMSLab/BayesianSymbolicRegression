# Code for calculating and counting expression fingerprints
# used for EF prior

# ===pseudocode below===

# calculate the prior probability for all expression fingerprints observed
# takes a list of expressions (probably instances of tree class from MCMC)
# and a depth which indicates how many steps to go from each node to form fingerprint
def calculatePrior(expressions, depth):
    # fill dictionary of prior with EF for key and count for value
    prior = {}

    for expression in expressions:
        EF = findEF(expression, depth)

    return prior

# find all subtrees that make up the expression fingerprint for this expression
# take expression and depth which is number of steps from starting node
def findEF(expression, depth):
    # dictionary for this expression fingerprint
    EF = {}

    for node in expression:
        # read in some order and omit missing nodes
        # add post order to EF dict and +1 to count

        # get the post order notation for this node / subtree
        result = ""
        postOrder(node, result, depth, 0)

        # if result is already a key in the dictionary, just add 1 to that count
        if (result in EF):
            EF[result] += 1
        else:
            EF[result] = 1


    return EF

def postOrder(node, result, depth, step):

    # if we have not gone to max depth yet
    if (step < depth):
        # call function recursively for children nodes if they exist
        if (node.left):
            # add them to result string 
            postOrder(node.left, result, depth, step+1)
        if (node.right):
            postOrder(node.right, result, depth, step+1)

    # add this node last because post order
    result += node.name

    return result  
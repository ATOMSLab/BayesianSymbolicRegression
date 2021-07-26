# This function is used to compare 2 nodes coming from 2 trees
# It works well, but sometimes a tree could have 2 nodes that are identical (same attributes) so be careful when using
# this function

def compare_node(node1, node2):
    # Compare 2 nodes and return True if they are similar. Need for TC checker
    # Check value of nodes
    if node1.value != node2.value:
        return False
    # Check parent of nodes
    if node1.parent is None:
        if node2.parent is not None:
            return False
    elif node2.parent is None:
        if node1.parent is not None:
            return False
    else:
        if node1.parent.value != node2.parent.value:
            return False
    # Check offspring of nodes
    if len(node1.offspring) != len(node2.offspring):
        return False
    if len(node1.offspring) != 0:
        node2_offspring = [node2.offspring[i].value for i in range(len(node2.offspring))]
        for node in node1.offspring:
            if node.value not in node2_offspring:
                return False
    return True

# Future work: compare the tree recursively
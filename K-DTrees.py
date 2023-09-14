from collections import namedtuple
from operator import itemgetter
from pprint import pformat
import math
import csv
from timeit import default_timer as timer


# klasi gia ena komvo tou dentrou

class Node(namedtuple('Node', 'location left_child right_child')):
    def __repr__(self):
        return pformat(tuple(self))


# Diadikasia kataskeuis dentrou

def create_tree(point_list, depth=0):
    if not point_list:
        return None

    dimensions = len(point_list[0])  # calculate dimensions
    axis = depth % dimensions  # Calculate node's axis based on dimensions

    # Sort point list by axis and pivot by diamesos element
    point_list.sort(key=itemgetter(axis))
    diamesos = len(point_list) // 2  # Calculate diameso

    # creation of node and construct subtrees
    return Node(
        location=point_list[diamesos],  # root of subtree --> diamesos
        left_child=create_tree(point_list[:diamesos], depth + 1),  # Left from point list
        right_child=create_tree(point_list[diamesos + 1:], depth + 1)  # Right from point list
    )


# Diadikasia euresis komvou

def searching(tree, point, depth=0):
    # if None then not found
    if tree is None:
        return False

    # check if point is the current node
    location = tree.location
    if (point[0] == location[0]) & (point[1] == location[1]):
        return True
    else:
        axis = depth % 2
        if point[axis] < location[axis]:
            # searching is on the left
            return searching(tree.left_child, point, depth + 1)
        else:
            # searching is on the left
            return searching(tree.right_child, point, depth + 1)


# Diadikasia eisagwgis komvou

def insertion(tree, point, depth=0):
    # Checking the case that tree is empty
    if tree is None:
        nod = Node(
            location=point,  # it becomes the root
            left_child=None,
            right_child=None
        )
        tree = nod
        return tree

    location = tree.location
    axis = depth % 2

    if point[axis] < location[axis]:
        # we search on the left subtree
        left_child = insertion(tree.left_child, point, depth + 1)
        tree = tree._replace(left_child=left_child)
        return tree
    else:
        # we search on the right subtree
        right_child = insertion(tree.right_child, point, depth + 1)
        tree = tree._replace(right_child=right_child)
        return tree


# Diadikasia diagrafis komvou

def deletion(tree, point, depth=0):
    # Checking the case that tree is empty
    if tree is None:
        return None

    location = tree.location
    if (point[0] == location[0]) & (point[1] == location[1]):
        # we found the  node we want to delete
        if (tree.left_child == None) & (tree.right_child == None):
            # if there is no children
            return None
        else:
            # if there is at least one child
            already_passed = []
            nodes = []
            # we put  all tree nodes into node[]
            if tree.left_child is not None:
                nodes.append(tree.left_child)
            if tree.right_child is not None:
                nodes.append(tree.right_child)

            while len(nodes) > 0:
                # we now visit all the children
                already_passed.append(nodes[0].location)  # we put a child into already_passed[]
                # in case node has child, move to end of nodes and delete node[0]
                if nodes[0].left_child is not None:
                    nodes.append(nodes[0].left_child)
                if nodes[0].right_child is not None:
                    nodes.append(nodes[0].right_child)
                del nodes[0]

            # end when no children are left end
            # create again the tree
            tree = create_tree(already_passed, depth)
            return tree
    else:
        axis = depth % 2
        # recursion
        if point[axis] < location[axis]:
            # searching on the left subtree
            left_child = deletion(tree.left_child, point, depth + 1)
            tree = tree._replace(left_child=left_child)
            return tree
        else:
            # searching on the right subtree
            right_child = deletion(tree.right_child, point, depth + 1)
            tree = tree._replace(right_child=right_child)
            return tree


def updating(tree, old, new):
    if (searching(tree, old)):
        tree = deletion(tree, old)
        tree = insertion(tree, new)

    return tree
    
 
# Ypologismos dianysmatikis apostasis metaksi duo shmeiwn sto xwro

def range(p1, p2):
    D = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    return D


def searchingPath(tree, point, path=None, depth=0):
    if depth == 0:
        path = list()
    # Checking the case that tree is empty
    if tree is None:
        return path

    # check if point is the current node
    location = tree.location
    tree.depth = depth
    path.append(tree)
    if (point[0] == location[0]) & (point[1] == location[1]) :
        return path
    else:
        axis = depth % 2
        if (point[axis] < location[axis]):
            # searching on the left subtree
            path = searchingPath(tree.left_child, point, path, depth + 1)
            return path
        else:
            # searching on the right subtree
            path = searchingPath(tree.right_child, point, path, depth + 1)
            return path


def searchingNeigbor(tree, point):
    path = searchingPath(tree, point)

    # arxikopoihsh
    lastNode = path.pop()
    Distance = range(point, lastNode.location)
    radius = Distance
    minimum = lastNode.location

    while (path):
        lastNode = path.pop()
        Distance = range(point, lastNode.location)

        if Distance < radius:
            radius = Distance
            minimum = lastNode.location

        axis = lastNode.depth % 2
        if abs(lastNode.location[axis] - point[axis]) < radius:
            # if radius bigger than distance then check the other half
            if (point[axis] < lastNode.location[axis]):
                # checking on the right subtree
                if lastNode.right_child is not None:
                    subtree = lastNode.right_child
                    subtree.depth = lastNode.depth + 1
                    path.append(subtree)

            else:
                # checking on the left subtree
                if lastNode.left_child is not None:
                    subtree = lastNode.left_child
                    subtree.depth = lastNode.depth + 1
                    path.append(subtree)

    return (minimum, radius)


def demo():

    """Example usage"""
    
    # build
    point_list = [(7, 2), (1, 4), (9, 6), (4, 7), (8, 1), (2, 3)]
    tree = create_tree(point_list)
    print(tree)

    # search existing node
    x = searching(tree, (5, 4))
    print(x)

    # search non-existing nodes
    x = searching(tree, (5, 3))
    print(x)

    # insert a node
    tree = insertion(tree, (1, 1))
    print(tree)

    # delete a leaf
    tree = deletion(tree, (1, 4))
    print(tree)

    # delete other node
    print(deletion(tree, (4, 7)))

    # delete non-existing node
    print(deletion(tree, (0, 0)))

    # update a node
    print(updating(tree, (8, 1), (8, 2)))

    # nearest neighbor
    (minimum, radius) = searchingNeigbor(tree, (6.9, 6))
    print(minimum, radius)


def main():
     # demo()

     folder = r'C:\Users\User\Documents\Εργασίες & Εργαστήρια\Εργασίες\Πολυδιάστατες Δομές Δεδομένων\1054370_1051322_1050135_5211/'
     with open(folder + 'data.csv') as csv_file:
         csv_reader = csv.reader(csv_file, delimiter=',')
         data = []
         first = True
         for row in csv_reader:
             if (first):
                 first = False
                 continue
             data.append((float(row[0]), float(row[1])))

     start_time = timer()
     tree = create_tree(data)
     end_time = timer()
     print('Creation')
     print(end_time - start_time)

     start_time = timer()
     x = searching(tree, data[len(data) - 1])
     end_time = timer()
     print('Search a node')
     print(end_time - start_time)

     start_time = timer()
     x = insertion(tree, data[len(data) - 1])
     end_time = timer()
     print('Insert a node')
     print(end_time - start_time)

     start_time = timer()
     x = deletion(tree, data[len(data) - 1])
     end_time = timer()
     print('Delete a node')
     print(end_time - start_time)

     start_time = timer()
     x = searchingNeigbor(tree, (38, 21))
     end_time = timer()
     print('Find the nearest neighbor')
     print(end_time - start_time)


if __name__ == '__main__':
    main()
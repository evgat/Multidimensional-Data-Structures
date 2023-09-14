from collections import namedtuple
from pprint import pformat
import math
import csv
from timeit import default_timer as timer


class Node(namedtuple('Node', 'location tRight tLeft bRight bLeft')):
    def __repr__(self):
        return pformat(tuple(self))

# Sygkrisi shmeiou me ena komvo kai epistrofi ths katefthinsis pou tha kinithoume
def child(location, p):
    if (p[0] < location[0]):
        if (p[1] < location[1]):
            return 4  # bLeft
        else:
            return 1  # tLeft

    else:
        if (p[1] < location[1]):
            return 3  # bRight
        else:
            return 2  # tRight

# Kataskeui dentrou
def storage(point_list):
    if not point_list:
        return None

    tLeft = []
    tRight = []
    bRight = []
    bLeft = []

    location = point_list[0]
    point_list = point_list[1:]

    for p in point_list:
        if (p[0] < location[0]):
            if (p[1] < location[1]):
                bLeft.append(p)
            else:
                tLeft.append(p)
        else:
            if (p[1] < location[1]):
                bRight.append(p)
            else:
                tRight.append(p)

    # Create node and construct subtrees
    return Node(
        location=location,
        tLeft=storage(tLeft),
        tRight=storage(tRight),
        bRight=storage(bRight),
        bLeft=storage(bLeft)
    )


def searching(tree, point):
    # checking if the tree is empty
    if tree is None:
        return False

    # check if it is the same point
    location = tree.location
    if (point[0] == location[0]) & (point[1] == location[1]):
        return True
    else:
        direc = child(location, point) #odigoumaste sto paidi me anadromiko tropo
        return searching(tree[direc], point)


def insertion(tree, point):
    # checking if its empty
    if (tree == None):
        nod = Node(
            location=point,
            tLeft=None,
            tRight=None,
            bRight=None,
            bLeft=None
        )
        tree = nod
        return tree

    location = tree.location
    direc = child(location, point)

    subtree = insertion(tree[direc], point)
    if direc == 1:
        tree = tree._replace(tLeft=subtree)
    else:
        if direc == 2:
            tree = tree._replace(tRight=subtree)
        else:
            if direc == 3:
                tree = tree._replace(bRight=subtree)
            else:
                if direc == 4:
                    tree = tree._replace(bLeft=subtree)

    return tree


def deletion(tree, point):
    # check if it is empty
    if tree is None:
        return None

    location = tree.location
    # searching if we are on a node
    if (point[0] == location[0]) & (point[1] == location[1]):
        # we are, we delete it
        # there are no children
        if (tree.tLeft == None) & (tree.tRight == None) & (tree.bRight == None) & (tree.bLeft == None):
            return None
        else:
            # there is at least one child
            # delete this and create the subtree again

            already_passed = []
            node = []
            for i in range(4):
                if tree[i + 1] is not None:
                    node.append(tree[i + 1])

            while len(node) > 0:
                already_passed.append(node[0].location)
                for i in range(4):
                    if node[0][i + 1] is not None:
                        node.append(node[0][i + 1])
                del node[0]

            # recreate the tree
            tree = storage(already_passed)
            return tree
    else:

        d = child(location, point)
        subtree = deletion(tree[d], point)

        if d == 1:
            tree = tree._replace(tLeft=subtree)
        else:
            if d == 2:
                tree = tree._replace(tRight=subtree)
            else:
                if d == 3:
                    tree = tree._replace(bRight=subtree)
                else:
                    if d == 4:
                        tree = tree._replace(bLeft=subtree)

        return tree


def updating(tree, old, new):
    # check if old exist
    if searching(tree, old):
        tree = deletion(tree, old)
        tree = insertion(tree, new)

    return tree


# Ypologismos dianysmatikis apostasis metaksi dyo shmeiwn

def distance(p1, p2):
    dist = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    return dist


def searchingPath(tree, point, path=None):
    if path is None:
        path = list()
    # if None, not found!
    if tree is None:
        return path

    # checking if we are in the same node
    location = tree.location
    path.append(tree)
    if (point[0] == location[0]) & (point[1] == location[1]):
        return path
    else:
        d = child(location, point)
        path = searchingPath(tree[d], point, path)
        return path


def searchingNeighbor(tree, point):
    path = searchingPath(tree, point)  # we want the path

    # initialize with last node (leaf)
    last_node = path.pop()
    dist = distance(point, last_node.location)
    radius = dist
    minimum = last_node.location


    while path:
        last_node = path.pop()
        dist = distance(point, last_node.location)

        if (dist < radius):
            radius = dist
            minimum = last_node.location


        if abs(last_node.location[0] - point[0]) < radius:
            # if radius larger than in x-axis then we check other half
            if ((point[0] < last_node.location[0])):
                # we have gone left before, now check right
                if last_node.tRight is not None:
                    path.append(last_node.tRight)
                if last_node.bRight is not None:
                    path.append(last_node.bRight)

            else:
                # we have gone right before, now check left
                if last_node.tLeft is not None:
                    path.append(last_node.tLeft)
                if last_node.bLeft is not None:
                    path.append(last_node.bLeft)

        if abs(last_node.location[1] - point[1]) < radius:
            # radius larger  in y-axis, check other half
            if point[1] < last_node.location[1]:
                # we have gone bottom before, now check top
                if last_node.tLeft is not None:
                    path.append(last_node.tLeft)
                if last_node.tRight is not None:
                    path.append(last_node.tRight)
            else:
                # we have gone top before, now check left bottom
                if last_node.bLeft is not None:
                    path.append(last_node.bLeft)
                if last_node.bRight is not None:
                    path.append(last_node.bRight)

    return (minimum, radius)


def demo():

    """Example usage"""
    
    # build
    point_list = [(7, 2), (5, 4), (9, 6), (4, 7), (8, 1), (2, 3)]
    tree = storage(point_list)
    print(tree)

    # search existing node
    x = searching(tree, (5, 4))
    print(x)

    # search non-existing nodes
    x = searching(tree, (5, 3))
    print(x)

    # insert a node
    tree = insertion(tree, (6, 5))
    print(tree)
    print("")

    # delete a leaf
    tree = deletion(tree, (6, 5))
    print(tree)
    print("")

    # delete other node
    print(deletion(tree, (7, 2)))
    print("")

    # delete non-existing node
    print(deletion(tree, (0, 0)))
    print("")

    # update a node
    print(updating(tree, (8, 1), (8, 2)))
    print("")

    # nearest neighbor
    (minimum, radius) = searchingNeighbor(tree, (6.9, 6))
    print(minimum, radius)


def main():
    # demo()

    folder =r'C:\Users\User\Documents\Εργασίες & Εργαστήρια\Εργασίες\Πολυδιάστατες Δομές Δεδομένων\1054370_1051322_1050135_5211/'
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
    tree = storage(data)
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
    x = searchingNeighbor(tree, (38, 21))
    end_time = timer()
    print('Find the nearest neighbor')
    print(end_time - start_time)


if __name__ == '__main__':
    main()
from AVLTree import AVLTree


def print_tree_visual(node, level=0, prefix="Root: "):

    if node.key is not None:
        print_tree_visual(node.right, level + 1, "R--- ")
        print(' ' * 6 * level + prefix + str(node.key) + " | H " + str(node.height) + " BF " + str(node.getBalanceFactor()))
        print_tree_visual(node.left, level + 1, "L--- ")

T = AVLTree()


for i in range(20):
    T.insert(i,"")
print_tree_visual(T.root)
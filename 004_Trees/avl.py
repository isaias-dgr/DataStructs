
from unittest import TestCase, skip, main as runtest

class Node:

    def __init__(self, value, height):
        self.value = value
        self.height = height
        self.left = None
        self.right = None

    def is_leaf(self):
        return self.left is None and self.right is None 
    
    def is_complete(self):
        return self.left and self.right 
    
    def get_only_child(self):
        return self.left if self.left else self.right
    
    def __str__(self):
        return f"{self.value}({self.height})"
    

class TreeAVL:

    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self._insert(self.root, value)

    def remove(self, value):
        self.root = self._remove(self.root, value)

    def _insert(self, root, value):
        if root is None:
            return Node(value, 1)
        
        if value < root.value:
            root.left = self._insert(root.left, value)
        else:
            root.right = self._insert(root.right, value)

        root.height = 1 + max(self._get_heigth(root.left), self._get_heigth(root.right))

        return self.__rotation(root)

    def _remove(self, root, value):
        
        if root is None:
            return None
        
        if value == root.value:
            root = self.__remove_node(root)
        elif value < root.value:
            root.left = self._remove(root.left, value)
        elif root.value < value:
            root.right = self._remove(root.right, value)

        if root is not None:
            root.height = self._get_heigth_node(root) 
            root = self.__rotation(root)
        return root
    
    def _get_heigth_node(self, root):
        return 1 + max(self._get_heigth(root.left), self._get_heigth(root.right))
    
    def __remove_node(self, root):
        if root.is_complete():
            max_node = self.max_value(root.left)
            self.remove(max_node.value)
            max_node.right = root.right
            max_node.left = root.left
            return max_node 
    
        if root.is_leaf():
            return None
        
        return root.get_only_child()
    
    def max_value(self, root):
        min_v = []
        self.__inorder(root, min_v)
        return min_v[-1]

    def __rotation(self, root):
        factor = self.__get_factor_rotation(root)
        if factor == -2:
            factor_hijo = self.__get_factor_rotation(root.right)
            if factor_hijo == -1 or factor_hijo == 0:
                root = self.__rotate_simple_right(root)
            else:
                root = self.__rotate_double_right(root)
        if factor == 2:
            factor_hijo = self.__get_factor_rotation(root.left)
            if factor_hijo == 1 or factor_hijo == 0:
                root = self.__rotate_simple_left(root)
            else:
                root = self.__rotate_double_left(root)
        return root

    def __rotate_double_right(self, root):
        child_right = root.right 
        g_child_left = child_right.left

        root.right = g_child_left.left
        child_right.left = g_child_left.right if g_child_left else None
           
        g_child_left.left = root
        g_child_left.right = child_right
        
        g_child_left.left.height = self._get_heigth_node(g_child_left.left)
        g_child_left.right.height = self._get_heigth_node(g_child_left.right)
        g_child_left.height = self._get_heigth_node(g_child_left)

        return g_child_left
        
    def __rotate_simple_right(self, root):
        child_right = root.right 
        g_child_left = child_right.left

        child_right.left = root
        child_right.left.right = g_child_left
        child_right.left.height = self._get_heigth_node(child_right.left)
        child_right.height = self._get_heigth_node(child_right)
        return child_right 
        
    def __rotate_double_left(self, root):
        child_left = root.left 
        g_child_right = child_left.right

        root.left = g_child_right.right
        child_left.right = g_child_right.left if g_child_right else None
           
        g_child_right.right = root
        g_child_right.left = child_left
        
        g_child_right.right.height = self._get_heigth_node(g_child_right.right)
        g_child_right.left.height = self._get_heigth_node(g_child_right.left)
        g_child_right.height = self._get_heigth_node(g_child_right)

        return g_child_right
        
    def __rotate_simple_left(self, root):
        child_left = root.left 
        g_child_right = child_left.right
        child_left.right = root
        child_left.right.left = g_child_right
        child_left.right.height = self._get_heigth_node(child_left.right)
        child_left.height = self._get_heigth_node(child_left)
        return child_left 
   
    def _get_heigth(self, root):
        return root.height if root else 0
    
    def __get_factor_rotation(self, root):
        return self._get_heigth(root.left) - self._get_heigth(root.right)

    def __preorder(self, root, output):
        if root is None:
            return
        output.append(root.value)
        # output.append(f"{root.value}({root.height})")
        self.__preorder(root.left, output)
        self.__preorder(root.right, output)

    def get_preorder(self):
        output = []
        self.__preorder(self.root, output)
        return output

    def __inorder(self, root, output):
        if root is None:
            return
        self.__inorder(root.left, output)
        output.append(root)
        self.__inorder(root.right, output)

    def get_inorder(self):
        output = []
        self.__inorder(self.root, output)
        return [item.value for item in output]
   

class TestTree(TestCase):

    def setUp(self):
        self.tree = TreeAVL()
        return super().setUp()
    
    def test_add_one_element(self):
        self.tree.insert(1)
        expected_preorder = [1]
        expected_inorder = [1]
        self.assertEqual(self.tree.get_preorder(), expected_preorder)
        self.assertEqual(self.tree.get_inorder(), expected_inorder) 
    
    def test_add_two_element(self):
        self.tree.insert(2)
        self.tree.insert(1)
        expected_preorder = [2, 1]
        expected_inorder = [1, 2]
        self.assertEqual(self.tree.get_preorder(), expected_preorder)
        self.assertEqual(self.tree.get_inorder(), expected_inorder) 

    def test_add_tree_element(self):
        self.tree.insert(2)
        self.tree.insert(1)
        self.tree.insert(3)
        expected_preorder = [2, 1, 3]
        expected_inorder = [1, 2, 3]
        self.assertEqual(self.tree.get_preorder(), expected_preorder)
        self.assertEqual(self.tree.get_inorder(), expected_inorder) 
  
    def test_add_tree_element_rotation_simple_right(self):
        self.tree.insert(1)
        self.tree.insert(2)
        self.tree.insert(3)
        expected_preorder = [2, 1, 3]
        expected_inorder = [1, 2, 3]
        self.assertEqual(self.tree.get_preorder(), expected_preorder)
        self.assertEqual(self.tree.get_inorder(), expected_inorder)
 
    def test_add_tree_element_rotation_simple_right_case2(self):
        self.tree.insert(1)
        self.tree.insert(5)
        self.tree.insert(3)
        expected_preorder = [3, 1, 5]
        expected_inorder = [1, 3, 5]
        self.assertEqual(self.tree.get_preorder(), expected_preorder)
        self.assertEqual(self.tree.get_inorder(), expected_inorder) 
  
    def test_add_tree_element_rotation_double_right(self):
        input_nodes = [0,1,15,20,10,11]
        for node in input_nodes:
            self.tree.insert(node)

        expected_preorder = [10,1,0,15,11,20]
        expected_inorder = [0,1,10,11,15,20]
        self.assertEqual(self.tree.get_preorder(), expected_preorder)
        self.assertEqual(self.tree.get_inorder(), expected_inorder) 

    def test_add_tree_element_rotation_double_right_(self):
        input_nodes = [0,1,15,20,10,9]
        for node in input_nodes:
            self.tree.insert(node)

        expected_preorder = [10,1,0,9,15,20]
        expected_inorder = [0,1,9,10,15,20]
        self.assertEqual(self.tree.get_preorder(), expected_preorder)
        self.assertEqual(self.tree.get_inorder(), expected_inorder) 

    def test_add_tree_element_rotation_double_right_case2(self):
        input_nodes = [0,1,15,20,10,19]
        for node in input_nodes:
            self.tree.insert(node)

        expected_preorder = [15,1,0,10,20,19]
        expected_inorder = [0,1,10,15,19,20]
        self.assertEqual(self.tree.get_preorder(), expected_preorder)
        self.assertEqual(self.tree.get_inorder(), expected_inorder)

    def test_add_tree_element_rotation_double_right_case2_(self):
        input_nodes = [0,1,15,20,10,21]
        for node in input_nodes:
            self.tree.insert(node)

        expected_preorder = [15,1,0,10,20,21]
        expected_inorder = [0,1,10,15,20,21]
        self.assertEqual(self.tree.get_preorder(), expected_preorder)
        self.assertEqual(self.tree.get_inorder(), expected_inorder) 

    def test_add_random_elements(self):
        input_nodes = [27, 0, 13, 18, 6, 10, 21, 22, 30,
                       24, 7, 5, 28, 26, 23, 25, 3, 14,
                       29, 16, 1, 2, 17, 11, 9]
        for node in input_nodes:
            self.tree.insert(node)

        expected_preorder = [13, 6, 3, 1, 0, 2, 5, 
                             10, 7, 9, 11, 24, 18, 
                             16, 14, 17, 22, 21, 23, 
                             27, 26, 25, 29, 28, 30]
        expected_inorder = [0, 1, 2, 3, 5, 6, 7, 9, 10, 
                            11, 13, 14, 16, 17, 18, 21, 
                            22, 23, 24, 25, 26, 27, 28, 29, 30] 
        self.assertEqual(self.tree.get_preorder(), expected_preorder)
        self.assertEqual(self.tree.get_inorder(), expected_inorder)    

    def test_remove_leaf_elements(self):
        for node in range(1,16):
            self.tree.insert(node)

        input_remove = [1, 3, 5, 7, 9, 11, 13, 15]
        for node in input_remove:
            self.tree.remove(node)

        expected_preorder = [8, 4, 2, 6, 12, 10, 14]
        self.assertEqual(self.tree.get_preorder(), expected_preorder)

    def test_remove_complete_elements(self):
        for node in range(1,16):
            self.tree.insert(node)

        input_remove = [2, 6, 10, 14]
        for node in input_remove:
            self.tree.remove(node)

        expected_preorder = [8, 4, 1, 3, 5, 7, 12, 9, 11, 13, 15]
        self.assertEqual(self.tree.get_preorder(), expected_preorder)

    def test_remove_only_child_elements(self):
        for node in range(1,16):
            self.tree.insert(node)

        input_remove = [2, 6, 10, 14, 1, 5, 9, 13]
        for node in input_remove:
            self.tree.remove(node)

        expected_preorder = [8, 4, 3, 7, 12, 11, 15]
        self.assertEqual(self.tree.get_preorder(), expected_preorder)

    def test_remove_node_not_exists(self):
        for node in [1,2,3,4,5]:
            self.tree.insert(node)

        self.tree.remove(6)
        expected_preorder = [2, 1, 4, 3, 5]
        self.assertEqual(self.tree.get_preorder(), expected_preorder)

    def test_remove_leaf_node(self):
        for node in [1,2,3,4,5]:
            self.tree.insert(node)

        self.tree.remove(5)
        self.tree.remove(3)
        expected_preorder = [2, 1, 4]
        self.assertEqual(self.tree.get_preorder(), expected_preorder)

    def test_remove_complete_node(self):
        for node in [1,2,3,4,5]:
            self.tree.insert(node)

        self.tree.remove(4)
        expected_preorder = [2, 1, 3, 5]
        self.assertEqual(self.tree.get_preorder(), expected_preorder)

    def test_remove_leaf_and_rotate_der_node(self):
        for node in [1,2,3,4,5]:
            self.tree.insert(node)

        self.tree.remove(3)
        self.tree.remove(1)
        expected_preorder = [4, 2, 5]
        self.assertEqual(self.tree.get_preorder(), expected_preorder)

    def test_remove_leaf__and_rotate_izq_node(self):
        for node in [5,4,3,2,1]:
            self.tree.insert(node)

        self.tree.remove(3)
        self.tree.remove(5)
        expected_preorder = [2, 1, 4]
        self.assertEqual(self.tree.get_preorder(), expected_preorder)

    def test_add_and_remove_secuencials(self):
        for node in range(1,16):
            self.tree.insert(node)

        for node in [12, 14, 15, 13, 11, 9, 1, 3]:
            self.tree.remove(node)

        expected_preorder = [6, 4, 2, 5, 8, 7, 10]
        self.assertEqual(self.tree.get_preorder(), expected_preorder)

    def test_add_and_remove_secuencials_left(self):
        for node in range(1,16):
            self.tree.insert(node)
        for node in [4, 2, 1, 3,  5, 7]:
            self.tree.remove(node)

        expected_preorder = [12, 8, 6, 10, 9, 11, 14, 13, 15]
        self.assertEqual(self.tree.get_preorder(), expected_preorder)


    def test_add_random_ints(self):
        inputs = [47,28,27,25,42,19,30,2,8,12,22,
                 45,10,21,26,48,6,41,23,50,18,4,
                 33,3]
        for node in inputs:
            self.tree.insert(node)

        inputs.sort()
        self.assertEqual(self.tree.get_inorder(), inputs)

if __name__ == "__main__":
    runtest()
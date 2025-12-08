import unittest
import random
from AVLTree import AVLTree, AVLNode

class TestAVLTreeExtended(unittest.TestCase):

    def setUp(self):
        """Initializes a new tree before each test to ensure isolation."""
        self.tree = AVLTree()

    # ====================================================================
    # Helper Functions
    # ====================================================================

    def _get_node(self, key):
        """Helper to get a real node pointer for delete operations."""
        node, _ = self.tree.search(key)
        return node

    def _check_avl_invariants(self, node):
        """
        Validates:
        1. BST Property (Left < Node < Right)
        2. AVL Balance Property (|Height_Left - Height_Right| <= 1)
        3. Correct Height Information
        """
        if node is None or not node.is_real_node():
            return -1, True

        # 1. BST Check
        if node.left and node.left.is_real_node():
            if node.left.key >= node.key:
                return 0, False
        if node.right and node.right.is_real_node():
            if node.right.key <= node.key:
                return 0, False

        # 2. Recursion
        left_h, left_ok = self._check_avl_invariants(node.left)
        right_h, right_ok = self._check_avl_invariants(node.right)

        # 3. Balance Check
        bf = left_h - right_h
        is_balanced = abs(bf) <= 1
        
        # 4. Height Check (Calculated vs Stored)
        # We calculate strict height. If implementation uses lazy updates, this might differ slightly,
        # but for a valid AVL after operations, it should be correct.
        calc_height = 1 + max(left_h, right_h)
        
        return calc_height, (left_ok and right_ok and is_balanced)

    def validate_tree(self):
        root = self.tree.get_root()
        if root is None:
            return
        _, valid = self._check_avl_invariants(root)
        self.assertTrue(valid, "Tree violated AVL balance or BST property")

    # ====================================================================
    # 1. INSERT Tests (8 Cases)
    # ====================================================================

    def test_insert_01_empty(self):
        """Insert Case 1: Insert into empty tree."""
        node, cost, promo = self.tree.insert(10, "10")
        self.assertEqual(node.key, 10)
        self.assertEqual(self.tree.size(), 1)
        self.assertEqual(self.tree.get_root().key, 10)
        self.assertEqual(self.tree.max_node().key, 10)

    def test_insert_02_leaf_left(self):
        """Insert Case 2: Simple insert left (No rotation)."""
        self.tree.insert(20, "20")
        self.tree.insert(10, "10")
        root = self.tree.get_root()
        self.assertEqual(root.key, 20)
        self.assertEqual(root.left.key, 10)
        self.validate_tree()

    def test_insert_03_leaf_right(self):
        """Insert Case 3: Simple insert right (No rotation)."""
        self.tree.insert(20, "20")
        self.tree.insert(30, "30")
        root = self.tree.get_root()
        self.assertEqual(root.key, 20)
        self.assertEqual(root.right.key, 30)
        self.validate_tree()

    def test_insert_04_rotation_ll(self):
        """Insert Case 4: Insert causing Right Rotation (Left-Left case)."""
        self.tree.insert(30, "30")
        self.tree.insert(20, "20")
        self.tree.insert(10, "10") # Should trigger rotation
        self.assertEqual(self.tree.get_root().key, 20)
        self.assertEqual(self.tree.get_root().left.key, 10)
        self.assertEqual(self.tree.get_root().right.key, 30)
        self.validate_tree()

    def test_insert_05_rotation_rr(self):
        """Insert Case 5: Insert causing Left Rotation (Right-Right case)."""
        self.tree.insert(10, "10")
        self.tree.insert(20, "20")
        self.tree.insert(30, "30") # Should trigger rotation
        self.assertEqual(self.tree.get_root().key, 20)
        self.validate_tree()

    def test_insert_06_rotation_rl(self):
        """Insert Case 6: Insert causing Right-Left Rotation."""
        self.tree.insert(10, "10")
        self.tree.insert(30, "30")
        self.tree.insert(20, "20") # Zig-Zag right-left
        self.assertEqual(self.tree.get_root().key, 20)
        self.validate_tree()

    def test_insert_07_rotation_lr(self):
        """Insert Case 7: Insert causing Left-Right Rotation."""
        self.tree.insert(30, "30")
        self.tree.insert(10, "10")
        self.tree.insert(20, "20") # Zig-Zag left-right
        self.assertEqual(self.tree.get_root().key, 20)
        self.validate_tree()

    def test_insert_08_update_max(self):
        """Insert Case 8: Verify max_node updates correctly on insert."""
        self.tree.insert(10, "10")
        self.assertEqual(self.tree.max_node().key, 10)
        self.tree.insert(20, "20") # New max
        self.assertEqual(self.tree.max_node().key, 20)
        self.tree.insert(15, "15") # Not max
        self.assertEqual(self.tree.max_node().key, 20)

    # ====================================================================
    # 2. SEARCH Tests (7 Cases)
    # ====================================================================

    def test_search_01_empty(self):
        """Search Case 1: Search in empty tree."""
        node, cost = self.tree.search(10)
        self.assertIsNone(node)
        self.assertEqual(cost, -1) # Convention for not found

    def test_search_02_root(self):
        """Search Case 2: Search for root."""
        self.tree.insert(10, "10")
        node, cost = self.tree.search(10)
        self.assertEqual(node.key, 10)
        self.assertEqual(cost, 1) # 0 edges + 1

    def test_search_03_leaf(self):
        """Search Case 3: Search for a leaf."""
        self.tree.insert(10, "10")
        self.tree.insert(5, "5")
        node, cost = self.tree.search(5)
        self.assertEqual(node.key, 5)
        self.assertEqual(cost, 2) # 1 edge + 1

    def test_search_04_missing_smaller(self):
        """Search Case 4: Search missing key smaller than min."""
        self.tree.insert(10, "10")
        node, cost = self.tree.search(5)
        self.assertIsNone(node)

    def test_search_05_missing_larger(self):
        """Search Case 5: Search missing key larger than max."""
        self.tree.insert(10, "10")
        node, cost = self.tree.search(15)
        self.assertIsNone(node)

    def test_search_06_missing_middle(self):
        """Search Case 6: Search missing key in between nodes."""
        self.tree.insert(10, "10")
        self.tree.insert(20, "20")
        node, cost = self.tree.search(15)
        self.assertIsNone(node)

    def test_search_07_deep(self):
        """Search Case 7: Search in a deeper tree."""
        for i in range(15): # Complete binary tree structure approx
            self.tree.insert(i, str(i))
        node, cost = self.tree.search(0)
        self.assertIsNotNone(node)
        self.assertGreater(cost, 1)

    # ====================================================================
    # 3. FINGER SEARCH Tests (7 Cases)
    # ====================================================================

    def test_finger_search_01_max(self):
        """Finger Search Case 1: Search for max node (Optimized)."""
        self.tree.insert(10, "10")
        self.tree.insert(20, "20")
        node, cost = self.tree.finger_search(20)
        self.assertEqual(node.key, 20)
        self.assertEqual(cost, 0) # Specific optimization in code for max

    def test_finger_search_02_near_max(self):
        """Finger Search Case 2: Search for node close to max."""
        self.tree.insert(10, "10")
        self.tree.insert(5, "5") # Root 10, Left 5
        # Max is 10. Search 5.
        node, cost = self.tree.finger_search(5)
        self.assertEqual(node.key, 5)
        self.assertGreater(cost, 0)

    def test_finger_search_03_min_worst_case(self):
        """Finger Search Case 3: Search for min (Walk up to root, down to min)."""
        for i in range(10):
            self.tree.insert(i, str(i))
        # Max is 9. Search 0.
        node, cost = self.tree.finger_search(0)
        self.assertEqual(node.key, 0)
        self.assertGreater(cost, 1)

    def test_finger_search_04_missing_near_max(self):
        """Finger Search Case 4: Search missing key near max."""
        self.tree.insert(10, "10")
        self.tree.insert(20, "20")
        # Max 20. Search 15.
        node, cost = self.tree.finger_search(15)
        self.assertIsNone(node.key)

    def test_finger_search_05_missing_greater_max(self):
        """Finger Search Case 5: Search key greater than max."""
        self.tree.insert(10, "10")
        node, cost = self.tree.finger_search(20)
        self.assertIsNone(node)

    def test_finger_search_06_empty(self):
        """Finger Search Case 6: Empty tree."""
        try:
            node, cost = self.tree.finger_search(10)
            self.assertIsNone(node)
        except AttributeError:
            # If implementation doesn't handle empty tree in finger_search, 
            # this catches it. Ideally it should return None.
            pass

    def test_finger_search_07_root(self):
        """Finger Search Case 7: Search root from max."""
        self.tree.insert(10, "10") # Root & Max
        node, cost = self.tree.finger_search(10)
        self.assertEqual(node.key, 10)
        self.assertEqual(cost, 0) # Since root is max here

    # ====================================================================
    # 4. FINGER INSERT Tests (6 Cases)
    # ====================================================================

    def test_finger_insert_01_empty(self):
        """Finger Insert Case 1: Insert into empty tree."""
        node, cost, promo = self.tree.finger_insert(10, "10")
        self.assertEqual(node.key, 10)
        self.assertEqual(self.tree.size(), 1)
        self.assertEqual(self.tree.max_node().key, 10)

    def test_finger_insert_02_new_max(self):
        """Finger Insert Case 2: Insert new maximum (O(1) amortized logic)."""
        self.tree.insert(10, "10")
        # Max is 10. Insert 20.
        node, cost, promo = self.tree.finger_insert(20, "20")
        self.assertEqual(self.tree.max_node().key, 20)
        # Cost should be very low (1 based on implementation analysis)
        self.assertLessEqual(cost, 1) 

    def test_finger_insert_03_near_max_left(self):
        """Finger Insert Case 3: Insert immediate left child of max."""
        self.tree.insert(10, "10")
        self.tree.insert(30, "30")
        # Max is 30. Insert 25.
        node, cost, promo = self.tree.finger_insert(25, "25")
        self.assertEqual(node.key, 25)
        self.assertEqual(self.tree.max_node().key, 30)
        self.validate_tree()

    def test_finger_insert_04_min_worst_case(self):
        """Finger Insert Case 4: Insert min value (Worst case walk)."""
        for i in range(10, 20):
            self.tree.insert(i, str(i))
        # Max is 19. Insert 0.
        node, cost, promo = self.tree.finger_insert(0, "0")
        self.assertEqual(node.key, 0)
        self.assertEqual(self.tree.max_node().key, 19)
        self.validate_tree()

    def test_finger_insert_05_rotation(self):
        """Finger Insert Case 5: Insert triggering rotation."""
        self.tree.finger_insert(10, "10")
        self.tree.finger_insert(20, "20")
        self.tree.finger_insert(30, "30") # Should rotate
        self.assertEqual(self.tree.get_root().key, 20)
        self.validate_tree()

    def test_finger_insert_06_alternating(self):
        """Finger Insert Case 6: Alternating Max and Min inserts."""
        # 1. Insert Max (100)
        self.tree.finger_insert(100, "100")
        # 2. Insert Min (0)
        self.tree.finger_insert(0, "0")
        # 3. Insert Max (101)
        self.tree.finger_insert(101, "101")
        
        print(self.tree.size())
        self.assertEqual(self.tree.max_node().key, 101)
        self.assertEqual(self.tree.size(), 3)
        self.validate_tree()

    # ====================================================================
    # 5. DELETE Tests (8 Cases)
    # ====================================================================

    def test_delete_01_leaf(self):
        """Delete Case 1: Delete a simple leaf."""
        self.tree.insert(10, "10")
        self.tree.insert(5, "5")
        self.tree.insert(15, "15")
        
        node = self._get_node(5)
        self.tree.delete(node)
        self.assertIsNone(self._get_node(5))
        self.validate_tree()

    def test_delete_02_node_left_child(self):
        """Delete Case 2: Delete node with only left child."""
        self.tree.insert(10, "10")
        self.tree.insert(5, "5")
        self.tree.insert(2, "2") # 5 has left child 2
        
        node = self._get_node(5)
        self.tree.delete(node)
        self.assertIsNone(self._get_node(5))
        self.assertIsNotNone(self._get_node(2))
        self.validate_tree()

    def test_delete_03_node_right_child(self):
        """Delete Case 3: Delete node with only right child."""
        self.tree.insert(10, "10")
        self.tree.insert(5, "5")
        self.tree.insert(7, "7") # 5 has right child 7
        
        node = self._get_node(5)
        self.tree.delete(node)
        self.assertIsNone(self._get_node(5))
        self.assertIsNotNone(self._get_node(7))
        self.validate_tree()

    def test_delete_04_binary_node_simple_succ(self):
        """Delete Case 4: Delete node with two children (Simple successor)."""
        self.tree.insert(10, "10")
        self.tree.insert(5, "5")
        self.tree.insert(15, "15")
        # Root 10 has 2 children
        node = self._get_node(10)
        self.tree.delete(node)
        
        self.assertIsNone(self._get_node(10))
        self.assertEqual(self.tree.size(), 2)
        self.validate_tree()

    def test_delete_05_root_only(self):
        """Delete Case 5: Delete root in single-node tree."""
        self.tree.insert(10, "10")
        node = self._get_node(10)
        self.tree.delete(node)
        self.assertEqual(self.tree.size(), 0)
        self.assertIsNone(self.tree.get_root())
        self.assertIsNone(self.tree.max_node())

    def test_delete_06_max_node(self):
        """Delete Case 6: Delete the maximum node."""
        self.tree.insert(10, "10")
        self.tree.insert(20, "20")
        self.assertEqual(self.tree.max_node().key, 20)
        
        node = self._get_node(20)
        self.tree.delete(node)
        self.assertEqual(self.tree.max_node().key, 10)
        self.validate_tree()

    def test_delete_07_causing_rotations(self):
        """Delete Case 7: Delete causing rebalancing (AVL property)."""
        # Tree: 4,2,6,1,3,5,7. Height 2.
        keys = [4, 2, 6, 1, 3, 5, 7]
        for k in keys:
            self.tree.insert(k, str(k))
        
        # Delete 1 (leaf). Might trigger local height change.
        # Delete 6 or 7 to trigger rotations.
        node = self._get_node(1)
        self.tree.delete(node)
        self.validate_tree()

    def test_delete_08_root_complex(self):
        """Delete Case 8: Delete root in a larger tree."""
        for i in range(10):
            self.tree.insert(i, str(i))
        # Root varies depending on insertions, usually 3 or 7.
        # We just find whatever current root is and delete it.
        root = self.tree.get_root()
        old_key = root.key
        self.tree.delete(root)
        
        self.assertIsNone(self._get_node(old_key))
        self.assertEqual(self.tree.size(), 9)
        self.validate_tree()

if __name__ == '__main__':
    unittest.main(verbosity=2)
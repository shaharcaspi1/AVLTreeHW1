import unittest
import random
import sys
def print_tree_visual(node, level=0, prefix="Root: "):
    if node.key is not None:
        print_tree_visual(node.right, level + 1, "R--- ")
        print(' ' * 6 * level + prefix + str(node.key) + " | H " + str(node.height) + " BF " + str(node.getBalanceFactor()))
        print_tree_visual(node.left, level + 1, "L--- ")

# נניח ששם הקובץ שלך הוא AVLTree.py
try:
    from AVLTree import AVLTree, AVLNode
except ImportError:
    print("Error: Could not import AVLTree. Make sure 'AVLTree.py' is in the same directory.")
    sys.exit(1)

# --- כלי עזר לבדיקות ---

def is_virtual(node):
    """בדיקה אם צומת הוא וירטואלי לפי הספרות (is_real_node returns False)"""
    return node is not None and not node.is_real_node()

def get_height(node):
    if node is None or not node.is_real_node():
        return -1
    return node.height

def get_balance_factor(node):
    return get_height(node.left) - get_height(node.right)

class BaseAVLTest(unittest.TestCase):
    """מחלקה בסיסית המכילה פונקציות עזר לבדיקת תקינות העץ"""

#     def validate_avl_structure(self, tree):
#         root = tree.get_root()
#         if root is None: # עץ ריק יכול להיות מיוצג ע"י None או שורש וירטואלי
#             return
#         if not root.is_real_node():
#             return

#         # 1. בדיקת תכונת עץ חיפוש (BST)
#         self.assertTrue(self._check_bst(root, float('-inf'), float('inf')), "BST Property Violated")
        
#         # 2. בדיקת איזון AVL וגבהים
#         self.assertTrue(self._check_balance_and_height(root), "AVL Balance/Height Violated")
        
#         # 3. בדיקת מבנה צמתים וירטואליים (לכל צומת אמיתי יש בנים - אמיתיים או וירטואליים)
#         self.assertTrue(self._check_virtual_structure(root), "Virtual Node Structure Violated (found Python None)")

#     def _check_bst(self, node, min_val, max_val):
#             if node is None or not node.is_real_node():
#                 return True
            
#             # בדיקה אם הצומת חורג מהטווח המותר לו
#             if not (min_val < node.key < max_val):
#                 print(f"\n[BST ERROR] Node {node.key} is invalid!")
#                 print(f"Expected between: ({min_val}, {max_val})")
#                 if node.parent:
#                     print(f"Parent is: {node.parent.key}")
#                     if node == node.parent.left:
#                         print("This node is a LEFT child.")
#                     elif node == node.parent.right:
#                         print("This node is a RIGHT child.")
#                 else:
#                     print("This node is the ROOT.")
#                 return False

#             return self._check_bst(node.left, min_val, node.key) and \
#                 self._check_bst(node.right, node.key, max_val)

#     def _check_balance_and_height(self, node):
#         if not node.is_real_node():
#             return True # גובה של וירטואלי הוא -1, נחשב תקין
        
#         left_ok = self._check_balance_and_height(node.left)
#         right_ok = self._check_balance_and_height(node.right)
        
#         h_left = get_height(node.left)
#         h_right = get_height(node.right)
        
#         # בדיקת גובה
#         calc_height = 1 + max(h_left, h_right)
#         if node.height != calc_height:
#             print(f"Height mismatch at key {node.key}: Stored {node.height}, Calc {calc_height}")
#             return False
            
#         # בדיקת איזון
#         bf = abs(h_left - h_right)
#         if bf > 1:
#             print(f"BF mismatch at key {node.key}: BF {bf}")
#             return False
            
#         return left_ok and right_ok

#     def _check_virtual_structure(self, node):
#         """מוודא שאין None במקום שצריך להיות צומת וירטואלי"""
#         if not node.is_real_node():
#             return True
#         if node.left is None or node.right is None:
#             return False
#         return self._check_virtual_structure(node.left) and self._check_virtual_structure(node.right)

# # ----------------------------------------------------------------------------------
# # 1. בדיקות INSERT (15 בדיקות)
# # ----------------------------------------------------------------------------------
# class TestInsert(BaseAVLTest):
#     def setUp(self):
#         self.tree = AVLTree()

#     def test_01_insert_root(self):
#         res = self.tree.insert(10, "root")
#         self.validate_avl_structure(self.tree)
#         self.assertEqual(self.tree.get_root().key, 10)
#         self.assertEqual(res[1], 0) # Edges for root insert might be 0

#     def test_02_insert_left(self):
#         self.tree.insert(10, "root")
#         self.tree.insert(5, "left")
#         self.assertEqual(self.tree.get_root().left.key, 5)
#         self.validate_avl_structure(self.tree)

#     def test_03_insert_right(self):
#         self.tree.insert(10, "root")
#         self.tree.insert(15, "right")
#         self.assertEqual(self.tree.get_root().right.key, 15)
#         self.validate_avl_structure(self.tree)

#     def test_04_rotation_LL(self):
#         # 30, 20, 10 -> אמור לגרום לסיבוב ימני
#         self.tree.insert(30, "a")
#         self.tree.insert(20, "b")
#         self.tree.insert(10, "c")
#         self.assertEqual(self.tree.get_root().key, 20) # השורש החדש
#         self.validate_avl_structure(self.tree)

#     def test_05_rotation_RR(self):
#         # 10, 20, 30 -> סיבוב שמאלי
#         self.tree.insert(10, "a")
#         self.tree.insert(20, "b")
#         self.tree.insert(30, "c")
#         self.assertEqual(self.tree.get_root().key, 20)
#         self.validate_avl_structure(self.tree)

#     def test_06_rotation_LR(self):
#         # 30, 10, 20
#         self.tree.insert(30, "a")
#         self.tree.insert(10, "b")
#         self.tree.insert(20, "c")
#         self.assertEqual(self.tree.get_root().key, 20)
#         self.validate_avl_structure(self.tree)

#     def test_07_rotation_RL(self):
#         # 10, 30, 20
#         self.tree.insert(10, "a")
#         self.tree.insert(30, "b")
#         self.tree.insert(20, "c")
#         self.assertEqual(self.tree.get_root().key, 20)
#         self.validate_avl_structure(self.tree)

#     def test_08_return_values_structure(self):
#         # בדיקה שהפונקציה מחזירה בדיוק שלשה (node, edges, promotes)
#         res = self.tree.insert(100, "val")
#         self.assertIsInstance(res, tuple)
#         self.assertEqual(len(res), 3)
#         self.assertTrue(res[0].is_real_node())
#         self.assertIsInstance(res[1], int)
#         self.assertIsInstance(res[2], int)

#     def test_09_insert_edges_cost(self):
#         self.tree.insert(10, "root")
#         self.tree.insert(5, "L")
#         # הכנסה לעומק 2 (מתחת ל 5)
#         # מסלול: שורש(10) -> 5 -> חדש. עומק 2? תלוי במימוש (0 או 1 based)
#         # הטסטר יבדוק שזה חיובי והגיוני
#         node, edges, _ = self.tree.insert(2, "LL")
#         self.assertGreater(edges, 0)

#     def test_10_insert_promotions_count(self):
#         # הכנסה שגורמת לשינוי גובה ללא סיבוב
#         self.tree.insert(10, "A")
#         _, _, p1 = self.tree.insert(5, "B") # 10 עולה גובה מ 0 ל 1
#         self.assertGreaterEqual(p1, 0) # לפחות עדכון אחד

#     def test_11_sequential_insert_asc(self):
#         for i in range(50):
#             self.tree.insert(i, str(i))
#         self.validate_avl_structure(self.tree)
#         self.assertEqual(self.tree.size(), 50)
#         self.assertEqual(get_height(self.tree.get_root()), 5) # log(50) ~ 5-6

#     def test_12_sequential_insert_desc(self):
#         for i in range(50, 0, -1):
#             self.tree.insert(i, str(i))
#         self.validate_avl_structure(self.tree)
#         self.assertEqual(self.tree.size(), 50)

#     def test_13_random_inserts(self):
#         keys = random.sample(range(1000), 100)
#         for k in keys:
#             self.tree.insert(k, "val")
#         self.validate_avl_structure(self.tree)
#         self.assertEqual(self.tree.size(), 100)

#     def test_14_verify_values(self):
#         self.tree.insert(5, "five")
#         self.tree.insert(3, "three")
#         node = self.tree.search(5)[0]
#         self.assertEqual(node.value, "five")

#     def test_15_large_scale(self):
#         # 1000 הכנסות
#         for i in range(1000):
#             self.tree.insert(i, "")
#         self.validate_avl_structure(self.tree)
#         self.assertLess(get_height(self.tree.get_root()), 15) # גובה לא יעלה על ~1.44log(n)

# # ----------------------------------------------------------------------------------
# # 2. בדיקות SEARCH (15 בדיקות)
# # כולל Finger Search
# # ----------------------------------------------------------------------------------
# class TestSearch(BaseAVLTest):
#     def setUp(self):
#         self.tree = AVLTree()
#         # בניית עץ יציב לבדיקות
#         #        50
#         #      /    \
#         #    25      75
#         #   /  \    /  \
#         # 12   37  62   87
#         self.keys = [50, 25, 75, 12, 37, 62, 87]
#         for k in self.keys:
#             self.tree.insert(k, str(k))

#     def test_01_search_root(self):
#         node, cost = self.tree.search(50)
#         self.assertEqual(node.key, 50)
#         self.assertGreaterEqual(cost, 0)

#     def test_02_search_leaf(self):
#         node, cost = self.tree.search(12)
#         self.assertEqual(node.key, 12)

#     def test_03_search_non_existent_low(self):
#         res = self.tree.search(1)
#         # מצפה ל None או צומת וירטואלי (לפי הנחיית PDF "x הוא מצביע לצומת.. או None")
#         if res is not None:
#             node, cost = res
#             self.assertTrue(node is None or not node.is_real_node())

#     def test_04_search_non_existent_high(self):
#         res = self.tree.search(100)
#         if res is not None:
#             node, cost = res
#             self.assertTrue(node is None or not node.is_real_node())

#     def test_05_search_non_existent_mid(self):
#         res = self.tree.search(60) # בין 50 ל 62
#         if res is not None:
#              node, _ = res
#              self.assertTrue(node is None or not node.is_real_node())

#     def test_06_finger_search_max(self):
#         # PDF: Finger search מתחיל מהמקסימום
#         max_val = 87
#         node, cost = self.tree.finger_search(max_val)
#         self.assertEqual(node.key, max_val)
#         # עלות צריכה להיות נמוכה מאוד (1 או 0) כי מתחילים משם
#         self.assertLessEqual(cost, 2)

#     def test_07_finger_search_near_max(self):
#         # חיפוש 75 (אבא של המקסימום)
#         node, cost = self.tree.finger_search(75)
#         self.assertEqual(node.key, 75)
#         self.assertGreater(cost, 0)

#     def test_08_finger_search_min(self):
#         # הכי רחוק מהמקסימום
#         node, cost = self.tree.finger_search(12)
#         self.assertEqual(node.key, 12)
#         # העלות צריכה להיות בערך כפולה מגובה העץ (עלייה לשורש וירידה) או תלוי באלגוריתם
#         self.assertGreater(cost, 2)

#     def test_09_finger_search_missing(self):
#         res = self.tree.finger_search(88) # גדול מהמקסימום
#         if res is not None:
#             node, _ = res
#             self.assertTrue(node is None or not node.is_real_node())

#     def test_10_search_empty_tree(self):
#         empty = AVLTree()
#         res = empty.search(5)
#         if res:
#              node, _ = res
#              self.assertTrue(node is None or not node.is_real_node())

#     def test_11_finger_search_empty_tree(self):
#         empty = AVLTree()
#         res = empty.finger_search(5)
#         if res:
#              node, _ = res
#              self.assertTrue(node is None or not node.is_real_node())

#     def test_12_search_cost_verification(self):
#         # וידוא שעלות היא int
#         _, cost = self.tree.search(50)
#         self.assertIsInstance(cost, int)

#     def test_13_finger_search_cost_verification(self):
#         _, cost = self.tree.finger_search(50)
#         self.assertIsInstance(cost, int)

#     def test_14_max_node_check(self):
#         # פונקציית עזר למקס
#         m = self.tree.max_node()
#         self.assertEqual(m.key, 87)

#     def test_15_search_logic_integrity(self):
#         # וידוא שחיפוש רגיל וחיפוש אצבע מחזירים אותו צומת
#         k = 37
#         n1, _ = self.tree.search(k)
#         n2, _ = self.tree.finger_search(k)
#         self.assertEqual(n1, n2)

# # ----------------------------------------------------------------------------------
# # 3. בדיקות DELETE (15 בדיקות)
# # ----------------------------------------------------------------------------------
# class TestDelete(BaseAVLTest):
#     def setUp(self):
#         self.tree = AVLTree()
#         # עץ מלא גובה 2
#         #       4
#         #     /   \
#         #    2     6
#         #   / \   / \
#         #  1   3 5   7
#         for i in [4, 2, 6, 1, 3, 5, 7]:
#             self.tree.insert(i, "")

#     def get_node(self, k):
#         return self.tree.search(k)[0]

#     def test_01_delete_leaf_left(self):
#         self.tree.delete(self.get_node(1))
#         self.validate_avl_structure(self.tree)
#         self.assertEqual(self.tree.size(), 6)

#     def test_02_delete_leaf_right(self):
#         self.tree.delete(self.get_node(3))
#         self.validate_avl_structure(self.tree)

#     def test_03_delete_unary_left_child(self):
#         # יצירת מצב מתאים
#         t = AVLTree()
#         t.insert(10, "")
#         t.insert(5, "") # 5 עלה
#         t.delete(t.search(10)[0]) # מחיקת שורש עם ילד אחד
#         self.assertEqual(t.get_root().key, 5)
#         self.validate_avl_structure(t)

#     def test_04_delete_unary_right_child(self):
#         t = AVLTree()
#         t.insert(10, "")
#         t.insert(15, "")
#         t.delete(t.search(10)[0])
#         self.assertEqual(t.get_root().key, 15)
#         self.validate_avl_structure(t)

#     def test_05_delete_binary_node_simple(self):
#         # מחיקת 2 (בנים 1, 3)
#         self.tree.delete(self.get_node(2))
#         self.validate_avl_structure(self.tree)
#         # השורש של תת העץ השמאלי צריך להתחלף
#         self.assertTrue(self.tree.get_root().left.key in [1, 3])

#     def test_06_delete_root(self):
#         self.tree.delete(self.get_node(4))
#         self.validate_avl_structure(self.tree)
#         self.assertEqual(self.tree.size(), 6)

#     def test_07_delete_cause_rotation(self):
#         # בניית עץ שידרוש איזון במחיקה
#         t = AVLTree()
#         #      4
#         #     / \
#         #    2   5
#         #   / \   \
#         #  1   3   6
#         for k in [4, 2, 5, 1, 3, 6]: t.insert(k, "")
        
#         # מחיקת 6 הופכת את 5 לעלה, צד ימין גובה 0.
#         # צד שמאל גובה 1. עדיין מאוזן.
#         # נוסיף עוד:
#         t.insert(0, "") # צד שמאל כבד יותר עכשיו
#         #      4
#         #    /   \
#         #   2     5
#         #  / \     \
#         # 1   3     6
#         # /
#         # 0
        
#         # מחיקת 5 ו-6
#         t.delete(t.search(6)[0])
#         t.delete(t.search(5)[0]) # עכשיו צד ימין ריק, צד שמאל גובה 2 -> סיבוב
#         self.validate_avl_structure(t)

#     def test_08_delete_max(self):
#         self.tree.delete(self.get_node(7))
#         self.validate_avl_structure(self.tree)
#         self.assertEqual(self.tree.max_node().key, 6)

#     def test_09_delete_all(self):
#         keys = [4, 2, 6, 1, 3, 5, 7]
#         for k in keys:
#             self.tree.delete(self.get_node(k))
#             self.validate_avl_structure(self.tree)
#         self.assertEqual(self.tree.size(), 0)
#         root = self.tree.get_root()
#         self.assertTrue(root is None or not root.is_real_node())

#     def test_10_delete_fail_on_virtual(self):
#         # ניסיון למחוק צומת וירטואלי לא אמור לקרוס
#         try:
#             node = self.tree.get_root().parent # None usually
#             if node: self.tree.delete(node)
#         except:
#             pass # אם זה זורק שגיאה זה בסדר, אם לא גם בסדר, העיקר שהטסטר לא קורס

#     def test_11_delete_rebalance_complex(self):
#         # בניית עץ פיבונאצ'י-סטייל שרגיש למחיקות
#         t = AVLTree()
#         for i in range(1, 16):
#             t.insert(i, "")
#         t.delete(t.search(14)[0])
#         t.delete(t.search(15)[0]) # גורם לשרשרת איזונים
#         self.validate_avl_structure(t)

#     def test_12_double_delete(self):
#         # מחיקה של אותו מפתח פעמיים (השני לא יימצא)
#         node = self.get_node(1)
#         self.tree.delete(node)
#         # עכשיו המפתח 1 איננו. אם נחפש אותו נקבל None
#         res = self.tree.search(1)
#         if res:
#              n, _ = res
#              self.assertTrue(n is None or not n.is_real_node())

#     def test_13_delete_root_becomes_empty(self):
#         t = AVLTree()
#         t.insert(1, "A")
#         t.delete(t.get_root())
#         self.assertEqual(t.size(), 0)

#     def test_14_delete_preserve_order(self):
#         # בדיקה שהסדר נשמר אחרי מחיקות
#         self.tree.delete(self.get_node(4)) # מחיקת שורש
#         arr = self.tree.avl_to_array()
#         keys = [x[0] for x in arr]
#         self.assertEqual(keys, [1, 2, 3, 5, 6, 7])

#     def test_15_stress_delete_random(self):
#         keys = list(range(50))
#         random.shuffle(keys)
#         t = AVLTree()
#         for k in keys: t.insert(k, "")
        
#         # מחק 25 איברים אקראיים
#         to_del = keys[:25]
#         for k in to_del:
#             t.delete(t.search(k)[0])
            
#         self.validate_avl_structure(t)
#         self.assertEqual(t.size(), 25)

# # ----------------------------------------------------------------------------------
# # 4. בדיקות JOIN (15 בדיקות)
# # ----------------------------------------------------------------------------------
# class TestJoin(BaseAVLTest):
    
#     def test_01_join_empty_empty(self):
#         t1 = AVLTree()
#         t2 = AVLTree()
#         t1.join(t2, 5, "val")
#         self.assertEqual(t1.size(), 1)
#         self.assertEqual(t1.get_root().key, 5)
#         self.validate_avl_structure(t1)

#     def test_02_join_empty_nonempty(self):
#         t1 = AVLTree()
#         t2 = AVLTree()
#         t2.insert(10, "A")
#         t1.join(t2, 5, "mid") # 5 < 10
#         self.assertEqual(t1.size(), 2)
#         self.validate_avl_structure(t1)

#     def test_03_join_nonempty_empty(self):
#         t1 = AVLTree()
#         t1.insert(2, "A")
#         t2 = AVLTree()
#         t1.join(t2, 5, "mid") # 2 < 5
#         self.assertEqual(t1.size(), 2)
#         self.validate_avl_structure(t1)

#     def test_04_join_t1_smaller_keys(self):
#         # T1 < k < T2
#         t1 = AVLTree()
#         t1.insert(1, "a")
#         t2 = AVLTree()
#         t2.insert(10, "b")
#         t1.join(t2, 5, "x")
#         self.assertEqual(t1.size(), 3)
#         self.validate_avl_structure(t1)
#         arr = [x[0] for x in t1.avl_to_array()]
#         self.assertEqual(arr, [1, 5, 10])

#     def test_05_join_t1_larger_keys(self):
#         # T1 > k > T2
#         # הפונקציה מצפה ש t יהיה העץ השני.
#         # ה PDF אומר: "מקבלת עץ נוסף t שכל המפתחות שלו קטנים ממש או גדולים ממש"
#         # אם T1 (self) גדולים מ t, אז ה k חייב להיות באמצע.
#         t1 = AVLTree() # self
#         t1.insert(10, "big")
#         t2 = AVLTree()
#         t2.insert(2, "small")
        
#         # k=5. סדר: t2(2) < 5 < t1(10)
#         t1.join(t2, 5, "mid")
#         self.validate_avl_structure(t1)
#         arr = [x[0] for x in t1.avl_to_array()]
#         self.assertEqual(arr, [2, 5, 10])

#     def test_06_join_balanced_heights(self):
#         t1 = AVLTree()
#         t1.insert(2, "a")
#         t2 = AVLTree()
#         t2.insert(6, "b")
#         # גובה 0 וגובה 0
#         t1.join(t2, 4, "x")
#         self.assertEqual(get_height(t1.get_root()), 1)
#         self.validate_avl_structure(t1)

#     def test_07_join_t1_taller(self):
#         t1 = AVLTree()
#         for i in range(10): t1.insert(i, "") # גובה ~3
#         t2 = AVLTree()
#         t2.insert(20, "") # גובה 0
        
#         t1.join(t2, 15, "")
#         self.validate_avl_structure(t1)
    
#     def test_08_join_t2_taller(self):
#         t1 = AVLTree()
#         t1.insert(1, "")
#         t2 = AVLTree()
#         for i in range(10, 20): t2.insert(i, "")
        
#         t1.join(t2, 5, "")
#         self.validate_avl_structure(t1)

#     def test_09_join_massive_diff(self):
#         # הפרש גבהים גדול מאוד
#         t1 = AVLTree()
#         for i in range(100): t1.insert(i, "")
#         t2 = AVLTree()
#         t2.insert(200, "")
        
#         t1.join(t2, 150, "")
#         self.validate_avl_structure(t1)

#     def test_10_join_causes_root_replacement(self):
#         # בדיקה שהשורש מתעדכן נכון
#         t1 = AVLTree() 
#         t1.insert(10, "")
#         t2 = AVLTree()
#         t2.insert(30, "")
#         t1.join(t2, 20, "") # 20 יהיה שורש
#         self.assertEqual(t1.get_root().key, 20)

#     def test_11_join_key_integrity(self):
#         t1 = AVLTree()
#         t1.insert(10, "val1")
#         t2 = AVLTree()
#         t2.insert(30, "val2")
#         t1.join(t2, 20, "midVal")
        
#         # חיפוש הערך החדש
#         node = t1.search(20)[0]
#         self.assertEqual(node.value, "midVal")

#     def test_12_join_input_validation(self):
#         # PDF: "לאחר הפעולה העץ t אינו שמיש"
#         # אנחנו לא בודקים קריסה, אבל נוודא שהפעולה על self הצליחה
#         pass 

#     def test_13_join_complex_trees(self):
#         t1 = AVLTree()
#         for i in range(0, 10, 2): t1.insert(i, "") # 0, 2, 4, 6, 8
#         t2 = AVLTree()
#         for i in range(11, 20, 2): t2.insert(i, "") # 11, 13, 15, 17, 19
        
#         t1.join(t2, 10, "mid")
#         self.assertEqual(t1.size(), 5+5+1)
#         self.validate_avl_structure(t1)

#     def test_14_join_t2_destroyed_concept(self):
#         # רק כדי לוודא שאין תלות מוזרה - t2 לא אמור להיות רלוונטי
#         t1 = AVLTree()
#         t1.insert(1, "")
#         t2 = AVLTree()
#         t2.insert(3, "")
#         t1.join(t2, 2, "")
#         # אם המשתמש מוחק את t2 זה לא אמור להשפיע על t1
#         # (אלא אם כן המימוש משתמש באותם צמתים, שאז t2 הוא פשוט הפניה לא חוקית)
#         self.assertEqual(t1.size(), 3)

#     def test_15_join_random(self):
#         t1 = AVLTree()
#         for i in range(20): t1.insert(i, "")
#         t2 = AVLTree()
#         for i in range(21, 40): t2.insert(i, "")
        
#         t1.join(t2, 20, "mid")
#         self.assertEqual(t1.size(), 40)
#         self.validate_avl_structure(t1)

# # ----------------------------------------------------------------------------------
# # 5. בדיקות SPLIT (15 בדיקות)
# # ----------------------------------------------------------------------------------
# class TestSplit(BaseAVLTest):
    
#     def test_01_split_root(self):
#         t = AVLTree()
#         t.insert(2, "root")
#         t.insert(1, "L")
#         t.insert(3, "R")
#         # 1 <- 2 -> 3
#         node = t.get_root()
#         t1, t2 = t.split(node)
        
#         # t1 צריך להכיל מפתחות < 2 (כלומר 1)
#         # t2 צריך להכיל מפתחות > 2 (כלומר 3)
#         self.assertEqual(t1.search(1)[0].key, 1)
#         self.assertEqual(t2.search(3)[0].key, 3)
#         self.validate_avl_structure(t1)
#         self.validate_avl_structure(t2)

#     def test_02_split_leaf(self):
#         t = AVLTree()
#         for i in range(1, 6): t.insert(i, "")
#         # עץ 1..5. נחתוך ב 1 (מינימום)
#         node = t.search(1)[0]
#         t1, t2 = t.split(node)
        
#         # t1 ריק
#         self.assertTrue(t1.get_root() is None or not t1.get_root().is_real_node())
#         # t2 מכיל 2,3,4,5
#         self.assertEqual(len(t2.avl_to_array()), 4)
#         self.validate_avl_structure(t2)

#     def test_03_split_max(self):
#         t = AVLTree()
#         for i in range(1, 6): t.insert(i, "")
#         node = t.search(5)[0]
#         t1, t2 = t.split(node)
        
#         # t1 מכיל 1,2,3,4
#         self.assertEqual(len(t1.avl_to_array()), 4)
#         # t2 ריק
#         self.assertTrue(t2.get_root() is None or not t2.get_root().is_real_node())

#     def test_04_split_middle(self):
#         t = AVLTree()
#         for i in range(1, 10): t.insert(i, "")
#         node = t.search(5)[0]
#         t1, t2 = t.split(node)
        
#         self.assertEqual([x[0] for x in t1.avl_to_array()], [1, 2, 3, 4])
#         self.assertEqual([x[0] for x in t2.avl_to_array()], [6, 7, 8, 9])
#         self.validate_avl_structure(t1)
#         self.validate_avl_structure(t2)

#     def test_05_split_single_node_tree(self):
#         t = AVLTree()
#         t.insert(10, "")
#         t1, t2 = t.split(t.get_root())
#         # שניהם ריקים
#         self.assertEqual(len(t1.avl_to_array()), 0)
#         self.assertEqual(len(t2.avl_to_array()), 0)

#     def test_06_split_left_leaning(self):
#         t = AVLTree()
#         for i in range(5, 0, -1): t.insert(i, "") # 5, 4, 3, 2, 1
#         node = t.search(3)[0]
#         t1, t2 = t.split(node)
#         self.validate_avl_structure(t1)
#         self.validate_avl_structure(t2)

#     def test_07_split_right_leaning(self):
#         t = AVLTree()
#         for i in range(1, 6): t.insert(i, "")
#         node = t.search(3)[0]
#         t1, t2 = t.split(node)
#         self.validate_avl_structure(t1)
#         self.validate_avl_structure(t2)




    def test_08_split_large_random(self):
        t = AVLTree()
        keys = list(range(20))
        random.shuffle(keys)
        for k in keys: t.insert(k, "")
        split_val = 10
        node = t.search(split_val)[0]
        t1, t2 = t.split(node)
        k1 = [x[0] for x in t1.avl_to_array()]
        k2 = [x[0] for x in t2.avl_to_array()]

        
        # וידוא שכל הקטנים שם
        self.assertTrue(all(k < 10 for k in k1))
        self.assertEqual(len(k1), 10) # 0..49
        
        # וידוא שכל הגדולים שם
        self.assertTrue(all(k > 10 for k in k2))
        self.assertEqual(len(k2), 9) # 51..99

#     def test_09_split_correct_return_type(self):
#         t = AVLTree()
#         t.insert(1, "")
#         res = t.split(t.get_root())
#         self.assertIsInstance(res, tuple)
#         self.assertEqual(len(res), 2)
#         self.assertIsInstance(res[0], AVLTree)
#         self.assertIsInstance(res[1], AVLTree)

#     def test_10_split_preserves_values(self):
#         t = AVLTree()
#         t.insert(1, "one")
#         t.insert(3, "three")
#         t.insert(2, "two") # split node
        
#         t1, t2 = t.split(t.search(2)[0])
#         self.assertEqual(t1.search(1)[0].value, "one")
#         self.assertEqual(t2.search(3)[0].value, "three")

#     def test_11_split_node_not_usable(self):
#         # זו דרישת PDF, אבל קשה לבדוק תכנותית (שהאובייקט 'נהרס').
#         # נבדוק רק שהמבנה שהוחזר תקין.
#         pass

#     def test_12_check_heights_after_split(self):
#         t = AVLTree()
#         for i in range(15): t.insert(i, "")
#         t1, t2 = t.split(t.search(7)[0])
#         # גובה צריך להיות חוקי
#         self.assertLess(get_height(t1.get_root()), 10)
#         self.assertLess(get_height(t2.get_root()), 10)

#     def test_13_split_almost_min(self):
#         t = AVLTree()
#         for i in range(10): t.insert(i, "")
#         t1, t2 = t.split(t.search(1)[0]) # כמעט מינימום
#         self.assertEqual(len(t1.avl_to_array()), 1) # רק 0
#         self.assertEqual(len(t2.avl_to_array()), 8) # 2..9

#     def test_14_split_almost_max(self):
#         t = AVLTree()
#         for i in range(10): t.insert(i, "")
#         t1, t2 = t.split(t.search(8)[0]) # כמעט מקסימום
#         self.assertEqual(len(t1.avl_to_array()), 8) # 0..7
#         self.assertEqual(len(t2.avl_to_array()), 1) # 9

#     def test_15_split_alternating_inserts(self):
#         t = AVLTree()
#         for i in range(0, 20, 2): t.insert(i, "")
#         t1, t2 = t.split(t.search(10)[0])
#         self.validate_avl_structure(t1)
#         self.validate_avl_structure(t2)

# # ----------------------------------------------------------------------------------
# # 6. בדיקות נוספות (FINGER INSERT + UTILS)
# # ----------------------------------------------------------------------------------
# class TestFingerInsertAndUtils(BaseAVLTest):
    
#     def test_finger_insert_basic(self):
#         t = AVLTree()
#         t.insert(10, "root")
#         res = t.finger_insert(20, "val")
#         self.assertEqual(res[0].key, 20)
#         self.validate_avl_structure(t)

#     def test_finger_insert_sequence(self):
#         t = AVLTree()
#         t.insert(1, "1")
#         # הכנסה עוקבת (סדר עולה) אמורה להיות יעילה ב finger insert
#         for i in range(2, 11):
#             t.finger_insert(i, "")
#         self.validate_avl_structure(t)
#         self.assertEqual(t.size(), 10)

#     def test_finger_insert_reverse(self):
#         # פחות יעיל אבל חייב לעבוד
#         t = AVLTree()
#         t.insert(100, "")
#         for i in range(99, 90, -1):
#             t.finger_insert(i, "")
#         self.validate_avl_structure(t)

#     def test_avl_to_array_sorted(self):
#         t = AVLTree()
#         keys = [5, 2, 8, 1, 9, 3]
#         for k in keys: t.insert(k, str(k))
#         arr = t.avl_to_array()
#         sorted_keys = [x[0] for x in arr]
#         self.assertEqual(sorted_keys, sorted(keys))

#     def test_avl_to_array_values(self):
#         t = AVLTree()
#         t.insert(1, "one")
#         arr = t.avl_to_array()
#         self.assertEqual(arr[0], (1, "one"))

#     def test_size_maintenance(self):
#         t = AVLTree()
#         self.assertEqual(t.size(), 0)
#         t.insert(1, "")
#         self.assertEqual(t.size(), 1)
#         t.delete(t.get_root())
#         self.assertEqual(t.size(), 0)
# # ----------------------------------------------------------------------------------
# # 7. בדיקות אינטגרציה קשות (HARD INTEGRATION / TORTURE TESTS)
# # ----------------------------------------------------------------------------------
# class TestIntegrationHard(BaseAVLTest):
    
#     def test_chaos_monkey(self):
#         """
#         Chaos Monkey: מבצעת רצף רנדומלי של 1000 פעולות (Insert, Delete, Search)
#         על עץ אחד כדי לוודא יציבות לאורך זמן.
#         """
#         t = AVLTree()
#         keys_in_tree = set()
#         actions_log = [] # למקרה שצריך לדבג
        
#         # טווח מפתחות רחב כדי לאפשר מרווחים
#         all_possible_keys = list(range(10000))
#         random.shuffle(all_possible_keys)
        
#         for i in range(1000):
#             action = random.choice(['insert', 'delete', 'search', 'finger_search'])
            
#             if action == 'insert':
#                 if not all_possible_keys: continue
#                 k = all_possible_keys.pop()
#                 t.insert(k, f"val_{k}")
#                 keys_in_tree.add(k)
#                 actions_log.append(f"insert({k})")
                
#             elif action == 'delete':
#                 if not keys_in_tree: continue
#                 # מוחק מפתח קיים
#                 k = random.choice(list(keys_in_tree))
#                 node = t.search(k)[0]
#                 # וודא שהצומת תקין לפני מחיקה
#                 if node is None or not node.is_real_node():
#                     self.fail(f"TEST FAILED: Search returned invalid node for existing key {k}")
#                 t.delete(node)
#                 keys_in_tree.remove(k)
#                 all_possible_keys.append(k) # מחזיר למאגר
#                 random.shuffle(all_possible_keys)
#                 actions_log.append(f"delete({k})")
                
#             elif action == 'search':
#                 if not keys_in_tree: continue
#                 k = random.choice(list(keys_in_tree))
#                 res = t.search(k)
#                 if res is None or res[0] is None or res[0].key != k:
#                      self.fail(f"TEST FAILED: Search failed to find existing key {k}")
            
#             # בדיקת תקינות מבנית כל 50 פעולות (כדי לא להאט מדי)
#             if i % 50 == 0:
#                 self.validate_avl_structure(t)
#                 self.assertEqual(t.size(), len(keys_in_tree))

#         # בדיקה סופית
#         self.validate_avl_structure(t)
#         self.assertEqual(t.size(), len(keys_in_tree))
        
#         # וידוא שכל האיברים שנשארו אכן שם
#         arr = t.avl_to_array()
#         self.assertEqual(len(arr), len(keys_in_tree))
#         sorted_keys = sorted(list(keys_in_tree))
#         self.assertEqual([x[0] for x in arr], sorted_keys)



#     def test_rank_stress(self):
#         """
#         דימוי תהליך של 'Rank':
#         מכניסים איברים, ומוחקים כל איבר שני (זוגיים), ואז מפצלים.
#         זה בודק אינטראקציה חזקה בין מחיקות לשינויי מבנה.
#         """
#         t = AVLTree()
#         n = 200
#         for i in range(1, n + 1):
#             t.insert(i, "")
            
#         # מחיקת כל הזוגיים: 2, 4, 6...
#         for i in range(2, n + 1, 2):
#             node = t.search(i)[0]
#             t.delete(node)
            
#         self.validate_avl_structure(t)
#         self.assertEqual(t.size(), n // 2)
        
#         # פיצול באמצע (בערך 101, אבל הוא נמחק, אז נחפש את 101 - הוא אי זוגי וקיים)
#         # נשארו אי זוגיים: 1, 3, 5, ..., 101, ..., 199
#         split_node = t.search(101)[0]
#         left_tree, right_tree = t.split(split_node)
        
#         self.validate_avl_structure(left_tree)
#         self.validate_avl_structure(right_tree)
        
#         # left צריך להכיל אי זוגיים מ 1 עד 99
#         # right צריך להכיל אי זוגיים מ 103 עד 199
#         left_keys = [x[0] for x in left_tree.avl_to_array()]
#         right_keys = [x[0] for x in right_tree.avl_to_array()]
        
#         expected_left = list(range(1, 100, 2)) # 1, 3...99
#         expected_right = list(range(103, 200, 2)) # 103...199
        
#         self.assertEqual(left_keys, expected_left)
#         self.assertEqual(right_keys, expected_right)

#     def test_finger_cost_logic(self):
#         """
#         בדיקה לוגית לעלויות Finger Search:
#         מוודא שחיפוש עוקב (Sequential Insert) באמצעות Finger Search
#         זול יותר במצטבר מחיפוש רגיל (או לפחות זול מאוד).
#         """
#         t = AVLTree()
#         # נכניס 1000 איברים בסדר עולה באמצעות Finger Insert
#         # כל הכנסה אמורה להיות O(1) אמורטיזי או קרוב לזה כי אנחנו תמיד ליד המקסימום.
        
#         total_edges = 0
#         for i in range(1000):
#             # משתמשים ב finger_insert אם קיים, או שמדמים ע"י finger_search ואז insert
#             # התרגיל דורש לממש finger_insert, אז נשתמש בו.
#             res = t.finger_insert(i, "")
#             total_edges += res[1] # edges cost
            
#         # עלות ממוצעת להכנסה עוקבת צריכה להיות נמוכה מאוד (קרוב ל 1-2 קשתות)
#         avg_cost = total_edges / 1000
        
#         # בהכנסה רגילה, היינו יורדים מהשורש כל פעם -> log(n).
#         # log(1000) ~ 10.
#         # ב Finger Tree אידיאלי, זה אמור להיות O(1).
#         # נבדוק שזה קטן משמעותית מ 10.
#         self.assertLess(avg_cost, 5, "Finger Insert sequential cost is too high!")

#     def test_join_extreme_alternating(self):
#         """
#         מבחן 'רוכסן' (Zipper):
#         לוקח שני עצים, ומאחד אותם שוב ושוב בצורה מדורגת.
#         בודק אם ה Join עומד בעומס של הפרשי גבהים משתנים.
#         """
#         # עץ ראשי
#         main_tree = AVLTree()
#         main_tree.insert(0, "base")
        
#         # הוספת בלוקים שלמים באמצעות Join
#         # בכל פעם נוסיף עץ חדש גדול יותר
#         current_max = 0
#         for i in range(1, 6): # 5 joins
#             # יצירת עץ חדש להוספה
#             temp_tree = AVLTree()
#             # גודל העץ גדל אקספוננציאלית: 10, 20, 40...
#             block_size = 10 * i
#             start_key = current_max + 2 # משאירים רווח למפתח ה join
            
#             for k in range(start_key, start_key + block_size):
#                 temp_tree.insert(k, "")
            
#             join_key = current_max + 1
            
#             # ביצוע Join: Main(קטנים) + Key + Temp(גדולים)
#             main_tree.join(temp_tree, join_key, "glue")
            
#             current_max = start_key + block_size - 1
#             self.validate_avl_structure(main_tree)
            
#         # בסוף העץ צריך להיות מאוזן ותקין
#         self.assertTrue(main_tree.get_root().is_real_node())
#         self.assertLess(get_height(main_tree.get_root()), 20) # לא אמור להיות עמוק מדי
# # ----------------------------------------------------------------------------------
# # 9. בדיקות קצה ללא Split (Pure Join/Delete/Insert Stress)
# # ----------------------------------------------------------------------------------
# class TestEdgeCasesNoSplit(BaseAVLTest):

#     def test_zigzag_join(self):
#         """
#         מבחן הזיג-זג (Join from both sides):
#         במקום רק להוסיף צד אחד, אנחנו בונים עץ ע"י הוספה לסירוגין.
#         פעם אנחנו ה-T1 (הקטנים) שמצרפים אליו עץ גדול,
#         ופעם אנחנו ה-T2 (הגדולים) שמצרפים אליו עץ קטן.
#         זה בודק את הלוגיקה של join בשני הכיוונים.
#         """
#         # מתחילים עם האמצע: 50
#         main_tree = AVLTree()
#         main_tree.insert(50, "center")

#         # 1. מוסיפים מימין (אנחנו הקטנים): Join(Self, 60, RightTree)
#         right_tree = AVLTree()
#         right_tree.insert(70, "R1")
#         main_tree.join(right_tree, 60, "J1") 
#         # עכשיו: 50, 60, 70

#         # 2. מוסיפים משמאל (אנחנו הגדולים): Join(LeftTree, 40, Self)
#         # שים לב: join נקרא על העץ השמאלי, והעץ שלנו הוא הפרמטר!
#         left_tree = AVLTree()
#         left_tree.insert(30, "L1")
        
#         # הטריק: הפונקציה join הורסת את העץ שעליו היא נקראת? 
#         # לא, היא הורסת את העץ שמועבר כפרמטר (t).
#         # אז אם נקרא left_tree.join(main_tree), אז main_tree ייהרס.
#         # אנחנו רוצים לשמור על המשתנה main_tree פעיל.
#         # לכן נהפוך את main_tree להיות התוצאה של left_tree.
        
#         left_tree.join(main_tree, 40, "J2")
#         main_tree = left_tree # מעבירים את השרביט לעץ המאוחד
        
#         # עכשיו: 30, 40, 50, 60, 70
#         self.validate_avl_structure(main_tree)
#         self.assertEqual(main_tree.size(), 5)
        
#         # מוודאים שהשורש מאוזן
#         self.assertLess(get_height(main_tree.get_root()), 4)

#     def test_delete_max_and_finger_search(self):
#         """
#         בדיקת עדכון מקסימום:
#         ה-Finger Search מסתמך על כך שהעץ יודע איפה המקסימום.
#         אם נמחק את המקסימום שוב ושוב, האם ה-Finger Search ימשיך לעבוד?
#         """
#         t = AVLTree()
#         # בניית עץ 0..19
#         for i in range(20):
#             t.insert(i, str(i))
            
#         # מחיקת המקסימום 5 פעמים ברצף
#         for i in range(19, 14, -1): # 19, 18, 17, 16, 15
#             # קודם כל מוודאים ש-Finger Search מוצא אותו לפני המחיקה
#             # (זה מוודא שהמקסימום הקודם עדכן נכון את המבנה)
#             node, cost = t.finger_search(i)
#             self.assertEqual(node.key, i)
            
#             # עכשיו מוחקים
#             t.delete(node)
            
#             # עכשיו המקסימום החדש צריך להיות i-1.
#             # נבדוק אם finger_search למקסימום החדש הוא זול (עלות 1-2)
#             new_max = i - 1
#             node_new, cost_new = t.finger_search(new_max)
#             self.assertEqual(node_new.key, new_max)
#             # אם המקסימום לא עודכן, החיפוש יתחיל ממקום לא נכון ויהיה יקר,
#             # או שיחזיר None אם המצביע מצביע לצומת מחוק.
#             self.assertLess(cost_new, 4, f"Finger search cost too high for new max {new_max}")

#     def test_join_multiple_heights(self):
#         """
#         מגדל בבל:
#         חיבור שרשרת של עצים בגבהים עולים ויורדים.
#         זה מכריח את ה-Join לטפס במעלה העץ לגבהים שונים כל פעם.
#         """
#         # T1: גובה 0
#         t1 = AVLTree()
#         t1.insert(10, "")
        
#         # T2: גובה ~2 (7 איברים)
#         t2 = AVLTree()
#         for i in range(20, 27): t2.insert(i, "") # 20..26
        
#         # חיבור: גובה 0 עם גובה 2
#         t1.join(t2, 15, "glue1") # 10..26
#         self.validate_avl_structure(t1)
        
#         # T3: גובה ~4 (15 איברים גדולים)
#         t3 = AVLTree()
#         for i in range(100, 115): t3.insert(i, "")
        
#         # חיבור: גובה ~3 עם גובה ~4
#         t1.join(t3, 50, "glue2")
#         self.validate_avl_structure(t1)
        
#         # T4: עץ קטנטן (גובה 0)
#         t4 = AVLTree()
#         t4.insert(200, "")
        
#         # חיבור: גובה ~5 עם גובה 0 (הפרש קיצוני)
#         t1.join(t4, 150, "glue3")
#         self.validate_avl_structure(t1)
        
#         # וידוא שכל המפתחות קיימים
#         self.assertIsNotNone(t1.search(10)[0])
#         self.assertIsNotNone(t1.search(25)[0])
#         self.assertIsNotNone(t1.search(110)[0])
#         self.assertIsNotNone(t1.search(200)[0])

#     def test_delete_root_until_empty_then_insert(self):
#         """
#         בדיקת ריקון מלא והתאוששות:
#         מוחקים תמיד את השורש עד שהעץ ריק.
#         בודקים שהעץ חוזר למצב התחלתי תקין.
#         ואז מכניסים איברים מחדש.
#         """
#         t = AVLTree()
#         keys = [5, 2, 8, 1, 3]
#         for k in keys: t.insert(k, "")
        
#         # מחיקת שורש 5 פעמים
#         for _ in range(5):
#             root = t.get_root()
#             self.assertIsNotNone(root)
#             self.assertTrue(root.is_real_node())
#             t.delete(root)
#             self.validate_avl_structure(t)
            
#         self.assertEqual(t.size(), 0)
#         root = t.get_root()
#         self.assertTrue(root is None or not root.is_real_node())
        
#         # החייאה מחדש
#         t.insert(100, "I live again")
#         self.assertEqual(t.size(), 1)
#         self.assertEqual(t.get_root().key, 100)
#         self.validate_avl_structure(t)

#     def test_finger_insert_sequential_stress(self):
#         """
#         בדיקת עומס ל-Finger Insert:
#         הכנסה של 500 איברים ממוינים.
#         זה התרחיש שעליו הפרויקט מדבר (Insertion Sort).
#         אנחנו מוודאים שהעץ נשאר מאוזן לחלוטין (כמו AVL רגיל)
#         למרות שמשתמשים בממשק ה-Finger.
#         """
#         t = AVLTree()
#         for i in range(500):
#             t.finger_insert(i, str(i))
            
#         self.validate_avl_structure(t)
#         self.assertEqual(t.size(), 500)
        
#         # הגובה צריך להיות חסום לוגריתמית (log2(500) ~= 9)
#         # AVL חוסם בערך 1.44 * log2
#         h = get_height(t.get_root())
#         self.assertLess(h, 12, f"Tree height {h} is too high for 500 elements")

# # ----------------------------------------------------------------------------------
# # 10. בדיקות מבניות מתקדמות (Structural Stress & Split Finales)
# # ----------------------------------------------------------------------------------
# class TestStructureStress(BaseAVLTest):

#     # --- קבוצה א': משחקי Join ו-Insert/Delete ---

#     def test_01_join_then_insert_at_seam(self):
#         """Join שני עצים, ואז הכנסה מיידית של איברים צמודים למפתח האיחוד."""
#         t1 = AVLTree()
#         for i in range(10): t1.insert(i, "") # 0..9
        
#         t2 = AVLTree()
#         for i in range(20, 30): t2.insert(i, "") # 20..29
        
#         # איחוד עם 15
#         t1.join(t2, 15, "seam")
        
#         # הכנסת שכנים ל-15 (מכריח את העץ להתמודד עם צפיפות באזור החיבור)
#         t1.insert(14, "left_neighbor")
#         t1.insert(16, "right_neighbor")
        
#         self.validate_avl_structure(t1)
#         self.assertEqual(t1.size(), 23)

#     def test_02_join_then_delete_seam(self):
#         """Join, ואז מחיקה מיידית של האיבר שביצע את האיחוד."""
#         t1 = AVLTree()
#         t1.insert(10, "")
#         t2 = AVLTree()
#         t2.insert(30, "")
        
#         t1.join(t2, 20, "seam_node") # העץ הוא 10, 20, 30
        
#         node_20 = t1.search(20)[0]
#         t1.delete(node_20) # מוחקים את הדבק
        
#         self.validate_avl_structure(t1)
#         self.assertEqual(t1.size(), 2)
#         arr = t1.avl_to_array()
#         self.assertEqual([x[0] for x in arr], [10, 30])

#     def test_03_join_and_delete_original_roots(self):
#         """Join, ואז מחיקת השורשים המקוריים של העצים שהרכיבו את האיחוד."""
#         t1 = AVLTree()
#         t1.insert(10, "root1")
#         t1.insert(5, "child1")
        
#         t2 = AVLTree()
#         t2.insert(30, "root2")
#         t2.insert(35, "child2")
        
#         # t1 root is 10, t2 root is 30
#         t1.join(t2, 20, "mid")
        
#         # מחיקת השורשים הישנים (שעכשיו הם סתם צמתים בעץ המאוחד)
#         node_10 = t1.search(10)[0]
#         node_30 = t1.search(30)[0]
        
#         t1.delete(node_10)
#         t1.delete(node_30)
        
#         self.validate_avl_structure(t1)
#         self.assertEqual(t1.size(), 3) # 5, 20, 35

#     def test_04_insert_delete_insert_join(self):
#         """רצף פעולות מעורב: הכנסה, מחיקה, הכנסה שוב, ואז איחוד."""
#         t1 = AVLTree()
#         for i in range(10): t1.insert(i, "")
#         for i in range(0, 10, 2): # מחיקת זוגיים: 0, 2, 4, 6, 8
#             t1.delete(t1.search(i)[0])
            
#         # נשארו אי זוגיים: 1, 3, 5, 7, 9. (גודל 5)
#         # מכניסים חזרה חלק:
#         t1.insert(4, "back")
        
#         t2 = AVLTree()
#         t2.insert(20, "")
        
#         t1.join(t2, 15, "gap")
#         self.validate_avl_structure(t1)
#         self.assertEqual(t1.size(), 8)

#     def test_05_double_join(self):
#         """שרשור כפול: T1 + T2 -> Res, ואז Res + T3."""
#         t1 = AVLTree()
#         t1.insert(1, "")
#         t2 = AVLTree()
#         t2.insert(3, "")
#         t3 = AVLTree()
#         t3.insert(5, "")
        
#         t1.join(t2, 2, "J1") # 1, 2, 3
#         t1.join(t3, 4, "J2") # 1, 2, 3, 4, 5
        
#         self.validate_avl_structure(t1)
#         self.assertEqual(t1.size(), 5)
#         self.assertEqual(t1.get_root().key, 2) # סביר להניח שה-2 יעלה למעלה או ה-4

#     def test_06_join_empty_with_massive_then_delete(self):
#         """Join של עץ ריק עם עץ גדול, ואז מחיקה מהגדול."""
#         t1 = AVLTree() # ריק
#         t2 = AVLTree()
#         for i in range(50): t2.insert(i, "")
        
#         # איחוד: t1 מקבל את t2 עם מפרד -1
#         t1.join(t2, -1, "min") 
        
#         # עכשיו t1 מכיל -1..49. נמחק את המקסימום (49)
#         t1.delete(t1.max_node())
        
#         self.validate_avl_structure(t1)
#         self.assertEqual(t1.size(), 50) # 50 originally + 1 join - 1 delete

#     # --- קבוצה ב': Finger Search/Insert במצבי קיצון ---

#     def test_07_finger_insert_asc_delete_max_repeat(self):
#         """Finger Insert, מחיקת מקסימום, והמשך Finger Insert."""
#         t = AVLTree()
#         # 1. הכנסה עולה
#         for i in range(10): t.finger_insert(i, "")
        
#         # 2. מחיקת המקסימום (9)
#         t.delete(t.max_node())
        
#         # 3. הכנסה נוספת (אמורה להשתמש במקסימום המעודכן 8)
#         t.finger_insert(9, "new_9")
#         t.finger_insert(10, "new_10")
        
#         self.validate_avl_structure(t)
#         self.assertEqual(t.size(), 11)

#     def test_08_join_then_finger_search_separator(self):
#         """Join, ואז חיפוש ה-Separator באמצעות Finger Search."""
#         t1 = AVLTree()
#         t1.insert(10, "")
#         t2 = AVLTree()
#         t2.insert(30, "")
        
#         t1.join(t2, 20, "sep")
        
#         # ה-Separator הוא בד"כ גבוה בעץ. Finger Search מתחיל מהמקסימום (30).
#         # הוא צריך לעלות ולרדת ל-20.
#         node, cost = t1.finger_search(20)
#         self.assertEqual(node.key, 20)
#         self.validate_avl_structure(t1)

#     def test_09_finger_search_min_after_heavy_right_insert(self):
#         """הכנסה מאסיבית לימין, ואז חיפוש המינימום (הכי רחוק)."""
#         t = AVLTree()
#         t.insert(0, "min") # המינימום
        
#         # בונים עץ כבד מימין
#         for i in range(1, 100): t.finger_insert(i, "")
            
#         # המקסימום הוא 99. המינימום הוא 0. המרחק מקסימלי.
#         node, cost = t.finger_search(0)
#         self.assertEqual(node.key, 0)
#         # העלות צריכה להיות פרופורציונלית לגובה העץ
#         h = get_height(t.get_root())
#         self.assertTrue(cost >= h) 

#     def test_10_wiper_effect(self):
#         """אפקט המגב: הוספה ומחיקה בקצה העליון לסירוגין."""
#         t = AVLTree()
#         t.insert(0, "")
        
#         for i in range(1, 20):
#             t.finger_insert(i, "val") # הוסף i
#             prev = t.search(i-1)[0]
#             t.delete(prev) # מחק i-1
            
#         # בסוף נשאר רק האחרון
#         self.assertEqual(t.size(), 1)
#         self.assertEqual(t.get_root().key, 19)
#         self.validate_avl_structure(t)

#     # --- קבוצה ג': Split כפעולה אחרונה (Grand Finale) ---

#     def test_11_split_at_root_after_insertions(self):
#         """בנייה רגילה ואז פיצול בשורש."""
#         t = AVLTree()
#         for i in range(15): t.insert(i, "") # עץ מלא גובה 3
        
#         root = t.get_root()
#         t1, t2 = t.split(root)
        
#         # t1 < root < t2
#         self.validate_avl_structure(t1)
#         self.validate_avl_structure(t2)
#         # וידוא שאין חפיפה
#         if t1.size() > 0: self.assertLess(t1.max_node().key, root.key)
#         if t2.size() > 0: self.assertGreater(t2.get_root().key, root.key) # min check logic approx

#     def test_12_split_at_join_node(self):
#         """Join ואז פיצול בדיוק בצומת שחיבר את העצים."""
#         t1 = AVLTree()
#         for i in range(10): t1.insert(i, "")
#         t2 = AVLTree()
#         for i in range(11, 20): t2.insert(i, "")
        
#         t1.join(t2, 10, "seam")
        
#         # פיצול ב-10
#         node_10 = t1.search(10)[0]
#         left, right = t1.split(node_10)
        
#         self.validate_avl_structure(left)
#         self.validate_avl_structure(right)
        
#         # בדיקה שחזרנו (בערך) למצב הקודם
#         # left: 0..9, right: 11..19
#         arr_l = left.avl_to_array()
#         arr_r = right.avl_to_array()
#         self.assertEqual(len(arr_l), 10)
#         self.assertEqual(len(arr_r), 9)

#     def test_13_insert_delete_then_split_min(self):
#         """הכנסה, מחיקה, ואז פיצול במינימום (קצה שמאלי)."""
#         t = AVLTree()
#         for i in range(10): t.insert(i, "")
#         t.delete(t.search(5)[0]) # חור באמצע
        
#         # פיצול במינימום (0)
#         node_0 = t.search(0)[0]
#         t1, t2 = t.split(node_0)
        
#         # t1 ריק, t2 כל השאר (בלי 0 ובלי 5)
#         self.validate_avl_structure(t2)
#         arr = t2.avl_to_array()
#         self.assertNotIn(0, [x[0] for x in arr])
#         self.assertNotIn(5, [x[0] for x in arr])

#     def test_14_join_huge_gap_then_split_in_gap(self):
#         """Join עם רווח עצום במפתחות, ואז פיצול בצומת ליד הרווח."""
#         t1 = AVLTree()
#         t1.insert(1, "A")
#         t2 = AVLTree()
#         t2.insert(1000, "B")
        
#         t1.join(t2, 500, "mid") # 1, 500, 1000
        
#         # פיצול ב-1 (הקטן ביותר)
#         # זה מאלץ את ה-Split לטפל בעצים שמאוד רחוקים זה מזה מבחינת מפתחות
#         left, right = t1.split(t1.search(1)[0])
        
#         self.validate_avl_structure(right)
#         # right צריך להכיל 500 ו-1000
#         keys = [x[0] for x in right.avl_to_array()]
#         self.assertEqual(keys, [500, 1000])

#     def test_15_alternating_inserts_then_split_middle(self):
#         """הכנסה לסירוגין (0, 100, 1, 99...) ואז פיצול באמצע."""
#         t = AVLTree()
#         low, high = 0, 100
#         for _ in range(20):
#             t.insert(low, "")
#             t.insert(high, "")
#             low += 1
#             high -= 1
            
#         # כרגע יש לנו 0..19 ו- 81..100.
#         # נפצל ב-10 (באמצע הגוש התחתון)
#         node = t.search(10)[0]
#         l, r = t.split(node)
        
#         self.validate_avl_structure(l) # 0..9
#         self.validate_avl_structure(r) # 11..19 + 81..100

#     def test_16_delete_root_create_new_root_split(self):
#         """מחיקת שורש, הכנסה שגורמת לשורש חדש, ואז פיצולו."""
#         t = AVLTree()
#         t.insert(20, "root")
#         t.insert(10, "left")
#         t.insert(30, "right")
        
#         t.delete(t.search(20)[0]) # שורש כנראה 10 או 30
#         t.insert(20, "new_20") # מחזירים את 20
        
#         # מפצלים ב-20 (בין אם הוא שורש ובין אם לא)
#         l, r = t.split(t.search(20)[0])
        
#         self.validate_avl_structure(l)
#         self.validate_avl_structure(r)
#         self.assertEqual(len(l.avl_to_array()), 1) # 10
#         self.assertEqual(len(r.avl_to_array()), 1) # 30

#     def test_17_sequential_finger_insert_then_split_random(self):
#         """Finger Insert רציף (בניית שרשרת יעילה) ואז פיצול רנדומלי."""
#         t = AVLTree()
#         for i in range(100): t.finger_insert(i, "")
        
#         rand_key = random.randint(10, 90)
#         l, r = t.split(t.search(rand_key)[0])
        
#         self.validate_avl_structure(l)
#         self.validate_avl_structure(r)

#     def test_18_split_node_with_two_heavy_subtrees(self):
#         """פיצול צומת שיש לו שני תתי-עצים כבדים (מלאים)."""
#         t = AVLTree()
#         # בונים עץ כך ש-50 יהיה השורש (בערך)
#         mid = 50
#         t.insert(mid, "mid")
#         for i in range(mid - 1, -1, -1): t.insert(i, "")
#         for i in range(mid + 1, 101): t.insert(i, "")
        
#         # מפצלים ב-50
#         l, r = t.split(t.search(50)[0])
        
#         self.validate_avl_structure(l) # 0..49
#         self.validate_avl_structure(r) # 51..100
#         # שניהם אמורים להיות עצים די גדולים ומאוזנים
#         self.assertGreater(get_height(l.get_root()), 3)
#         self.assertGreater(get_height(r.get_root()), 3)



#     def test_20_torture_split(self):
#         """כאוס מוחלט ואז פיצול."""
#         t = AVLTree()
#         keys = list(range(200))
#         random.shuffle(keys)
        
#         # הכנסה רנדומלית
#         for k in keys: t.insert(k, "")
        
#         # מחיקה רנדומלית של 50 איברים
#         for _ in range(50):
#             k = random.choice(keys)
#             keys.remove(k)
#             t.delete(t.search(k)[0])
            
#         # פיצול בערך שקיים בעץ
#         split_key = keys[len(keys)//2]
#         l, r = t.split(t.search(split_key)[0])
        
#         self.validate_avl_structure(l)
#         self.validate_avl_structure(r)
        

if __name__ == '__main__':
    unittest.main(verbosity=2)

    
#id1:
#name1:
#username1:
#id2:
#name2:
#username2:

"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value, parent = None, isVitrual = False):
		self.key = key
		self.value = value
		# initilaize virtual sons
		self.left = None if isVitrual else AVLNode(None, None, self, True)
		self.right = None if isVitrual else AVLNode(None, None, self, True)
		self.setParent(parent)
		self.height = -1

	#sets the parent of a node
	def setParent(self, parent):
		self.parent = parent
		if(parent is None or self.key is None):
			return
		if(parent.key > self.key):
			parent.left = self
		else:
			parent.right = self

	def updateHeight(self):
		# check if virtual node
		if(not self.is_real_node()):
			return
		self.height = max(self.left.height, self.right.height) + 1
		
	def getBalanceFactor(self):
		# check if virtual node
		if(not self.is_real_node()):
			return 0
		# update heights of sons
		self.left.updateHeight()
		self.right.updateHeight()
		return self.left.height - self.right.height

	def getSuccessor(self):
		# initilaize successor
		successor = None
		# check for right son
		if(self.right.key != None):
			# update successor
			successor = self.right
			# go left all the way
			while(successor.left.key != None):
				successor = successor.left
		# if no right son
		else:
			# initilaize temp node for finding successor
			tempNode = self
			tempParent = self.parent
			# wait for first right turn (bigger than temp node)
			rightTurn = False
			while (not rightTurn):
				# if parent key is smaller than node key - left turn, go up
				if(tempParent.key < tempNode.key):
					tempNode = tempNode.parent
				# else - right turn, break and return parent
				else:
					rightTurn = True
			# update successor
			successor = tempParent
		return successor

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return not ((self.key == None) and (self.value == None))

	def rotationR(self):
		# initilize temp vars for rotation
		A = self
		B = self.left

		# change the second's parent
		B.setParent(A.parent)

		# rotate and change parent of children
		A.left = B.right
		B.right.parent = A
		B.right = A

		# change first's parent
		A.parent = B

		# update heights
		A.updateHeight()
		B.updateHeight()

		return

	def rotationL(self):
		# initilize temp vars for rotation
		A = self
		B = self.right

		# change the second's parent
		B.setParent(A.parent)

		# rotate and change parent of children
		A.right = B.left
		B.left.parent = A
		B.left = A

		# change first's parent
		A.parent = B

		# update heights
		A.updateHeight()
		B.updateHeight()

		return
		


	def rotationRL(self):
		self.right.rotationR()
		self.rotationL()

		return
	
	def rotationLR(self):
		self.left.rotationL()
		self.rotationR()

		return
	
	#master for rotation, gets a node and its BF (always 2 if rotation is needed), and its son in the problematic route
	def rotate(self, BF, son):
		sonBF = son.getBalanceFactor()
		if(BF == 2):
			if(sonBF == 1 or sonBF == 0):
				self.rotationR()
			elif(sonBF == -1):
				print(son.key ," LR coming")
				self.rotationLR()
		else:
			if(sonBF == -1 or sonBF == 0):
				self.rotationL()
			elif(sonBF == 1):
				self.rotationRL()
		return

"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self, Root = None):
		if (Root is not None):
			Root.parent = None
		self.root = Root
		self.maxNode = Root
		self.treeSize = 0


	def searchMaster(self, key, isSearch):
		searchDepth = 0
		currentNode = self.root
		while (currentNode.key != None):
			if(key == currentNode.key):
				return (currentNode, searchDepth+1)
			if(key > currentNode.key):
				currentNode = currentNode.right
				searchDepth =+ 1
			else:
				currentNode = currentNode.left
				searchDepth =+ 1
		if(isSearch):
			return None, -1
		else:
			return currentNode.parent, searchDepth

	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search(self, key):
		if(self.get_root() is None):
			return None, -1
		checkNode = self.searchMaster(key, True)
		return checkNode


	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def finger_search(self, key):
		# edge case - if key is maxNode
		if( key == self.max_node().key):
			return self.max_node(), 0
		
		# initialize variables for search
		currentNode = self.max_node()
		searchLength = 0
		# loop for going up to find sub tree that key suppodes to be in
		while (key < currentNode.key):
			if (currentNode == self.get_root()):
				break
			if (key <= currentNode.parent.key):
				currentNode = currentNode.parent
				searchLength += 1
				continue
			elif (key > currentNode.parent.key):
				break
		# if got to root - do a regular search
		if (currentNode == self.get_root()):
			x,e = self.search(key)
			# if not found return None, -1
			if (x == None):
				return None,-1
			# if found add e to searchLength add return
			else:
				searchLength += e
				return x, searchLength+1
		# if not root: do search from currentNode
		else:
			while (currentNode.key != None):
				if(key == currentNode.key):
					return (currentNode, searchLength+1)
				if(key > currentNode.key):
					currentNode = currentNode.right
					searchLength =+ 1
				else:
					currentNode = currentNode.left
					searchLength =+ 1
		if (currentNode != None):
			return currentNode, searchLength+1
		else:
			return None, -1


	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def insert(self, key, val):
		#tree is empty
		if(self.root == None):
			self.root = AVLNode(key, val)
			self.root.updateHeight()
			self.maxNode = self.root
			self.treeSize += 1
			return self.root, 0, 0
		#inserting the node
		parentNode, searchHeight = self.searchMaster(key, False)
		node = AVLNode(key,val)
		node.setParent(parentNode)
		node.updateHeight()

		#tree fields stuff
		self.treeSize += 1
		if (key > self.maxNode.key):
			self.maxNode = node
		
		#rotating
		promote = 0
		son = node
		while(parentNode != None):
			currentHeight = parentNode.height
			newHeight = parentNode.updateHeight()
			balanceFactor = parentNode.getBalanceFactor()
			if(abs(balanceFactor) < 2 and currentHeight == newHeight):
				break
			elif(abs(balanceFactor) < 2 and currentHeight != newHeight):
				son = parentNode
				parentNode = parentNode.parent
				promote += 1
				continue
			else:
				parentNode.rotate(balanceFactor, son)
				if(parentNode is self.root):
					self.root = parentNode.parent
				break
		
		return node, searchHeight+1, promote
		
			
					


	"""inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def finger_insert(self, key, val):
		# edge case - if tree is empty
		if(self.root == None):
			self.root = AVLNode(key, val)
			self.maxNode = self.root
			self.root.updateHeight()
			self.treeSize += 1
			return self.root, 0, 0
		
		
		# initialize variables for search
		nodeToAdd = AVLNode(key, val)
		currentNode = self.max_node()
		searchLength = 0

		# if smaller than max_node
		if(key < currentNode.key):
			# loop for going up to find sub tree that key suppodes to be in
			while (key < currentNode.key):
				if (currentNode == self.get_root()):
					break
				if (key < currentNode.parent.key):
					currentNode = currentNode.parent
					searchLength += 1
					continue
				elif (key > currentNode.parent.key):
					break
		
			# if got to root - do a regular search
			if (currentNode == self.get_root()):
				parentNode, e = self.searchMaster(key, False)
				searchLength += e
				currentNode = parentNode
			# if not root: do search from currentNode
			else:
				while (currentNode.key != None):
					if(key > currentNode.key):
						if(currentNode.right.key is None):
							break
						currentNode = currentNode.right
						searchLength =+ 1
					else:
						if(currentNode.left.key is None):
							break
						currentNode = currentNode.left
						searchLength =+ 1
		# if bigger then naxNode - update max node
		else:
			self.maxNode = nodeToAdd
		parentNode = currentNode

		nodeToAdd.setParent(parentNode)
		nodeToAdd.updateHeight()
		self.treeSize += 1

		# balance tree
		promote = 0
		son = nodeToAdd
		while(parentNode != None):
			currentHeight = parentNode.height
			newHeight = parentNode.updateHeight()
			balanceFactor = parentNode.getBalanceFactor()
			if(abs(balanceFactor) < 2 and currentHeight == newHeight):
				break
			elif(abs(balanceFactor) < 2 and currentHeight != newHeight):
				son = parentNode
				parentNode = parentNode.parent
				promote += 1
				continue
			else:
				parentNode.rotate(balanceFactor, son)
				if(parentNode is self.root):
					self.root = parentNode.parent
				break
		
		return nodeToAdd, searchLength+1, promote


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
		# check for edge case - tree is empty
		if(self.root is None):
			return
		#delete the node and get the parent of the physically deleted node(might be the parent of where the succesor was)
		currentNode = self.BSTdelete(node)
		#rotate
		while(currentNode is not None):
			balanceFactor = currentNode.getBalanceFactor()
			currentHeight = currentNode.height
			newHeight = currentNode.updateHeight()
			if(abs(balanceFactor) < 2 and currentHeight == newHeight):
				break
			elif(abs(balanceFactor) < 2 and currentHeight != newHeight):
				currentNode = currentNode.parent
				continue
			else:
				son = currentNode.left if balanceFactor == 2 else currentNode.right
				currentNode.rotate(balanceFactor, son)
				if(currentNode is self.root):
					self.root = currentNode.parent
				currentNode = currentNode.parent
				continue	
		return	

	#deletes node as it does in BST and returns the parent of the physically deleted node, whilst updating the maximum, root and size of tree as needed
	def BSTdelete(self,node: AVLNode, rec = False):
		#first update maximum, if we looking at succ and its the maximum we dont want to change it
		if(self.maxNode.key == node.key and not rec):
			if(node.left.key is not None):
				self.maxNode = node.left
			else:
				self.maxNode = node.parent
		#case 0: node is virtual
		if(not node.is_real_node()):
			return
		#case 1: node is a leaf
		#replaces it with virtual leaf or to None if tree is single leaf
		if((node.left.key is None) and (node.right.key is None)):
			#if tree is a single leaf
			if(self.root.key == node.key):
				self.root = None
			else:
				#makes a virtual node and connects it to node's parent instead of node
				virtual = AVLNode(node.key,None,None,True)
				virtual.setParent(node.parent)
				virtual.key = None
			self.treeSize -= 1
			return node.parent
		#case 2: node has one child
		#then that child has no children of its own, bypass node
		elif((node.left.key is None) or (node.right.key is None)):
			son = node.left if node.right.key is None else node.right
			son.setParent(node.parent)
			if(son.parent is None):
				self.root = son
			self.treeSize -= 1
			return node.parent
		#case 3: node has 2 children
		#find succesor and replace
		else:
			succ = node.getSuccessor()
			succParent = self.BSTdelete(succ, True)
			#replace node by succ
			node.left.setParent(succ)
			node.right.setParent(succ)
			succ.setParent(node.parent)
			if(succ.parent is None):
				self.root = succ
			#takes care of the edge case where succParent is node
			if(succParent is node):
				succParent = succ
			return succParent
			


		

			
	"""joins self with item and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	"""
	def join(self, tree2, key, val):
		# create node with key = key, value = val for joining
		joinNode = AVLNode(key,val)

		# edge case - one of the trees are empty
		if (self.root is None or self.root.key is None):
			tree2.insert(key,val)
			self.changeTree(tree2)
			return
		if (tree2.root is None or tree2.root.key is None):
			return

		# var to checking if self is higher than tree2
		selfIsHigher = True
		if (self.root.height < tree2.root.height):
			selfIsHigher = False

		# define general vars for joining
		higherTree, shorterTree = self if selfIsHigher else tree2, tree2 if selfIsHigher else self
		h = shorterTree.root.height
		newSize = higherTree.size() + shorterTree.size() + 1

		# check where to join (left or right)
		addToLeft = True
		if (higherTree.max_node().key < shorterTree.getMinKey()):
			addToLeft = False
		
		# edge case - heights equal
		h1 = higherTree.root.height
		if (h == h1):
			shorterTree.root.setParent(joinNode)
			higherTree.root.setParent(joinNode)
			joinNode.updateHeight()
			self.root = joinNode
			self.treeSize = newSize
			return

		### perform the join
		parentJoinNode = higherTree.root

		# add the shorter tree to left
		if (addToLeft):
			while (parentJoinNode.height > h+1):
				parentJoinNode = parentJoinNode.left
			shorterTree.root.setParent(joinNode)
			parentJoinNode.left.setParent(joinNode)
			joinNode.setParent(parentJoinNode)
			joinNode.updateHeight()
			parentJoinNode.updateHeight()
		else:
			while (parentJoinNode.height > h+1):
				parentJoinNode = parentJoinNode.right
			shorterTree.root.setParent(joinNode)
			parentJoinNode.right.setParent(joinNode)
			joinNode.setParent(parentJoinNode)
			joinNode.updateHeight()
			parentJoinNode.updateHeight()
		

		### balance upwards
		son = joinNode
		parentNode = parentJoinNode
		while(parentNode != None):
			currentHeight = parentNode.height
			newHeight = parentNode.updateHeight()
			balanceFactor = parentNode.getBalanceFactor()
			if(abs(balanceFactor) < 2 and currentHeight == newHeight):
				break
			elif(abs(balanceFactor) < 2 and currentHeight != newHeight):
				son = parentNode
				parentNode = parentNode.parent
				continue
			else:
				parentNode.rotate(balanceFactor, son)
				if(parentNode is higherTree.root):
					higherTree.root = parentNode.parent
				

		self.changeTree(higherTree)
		self.treeSize = newSize
		return


	def changeTree(self,other):
		self.root = other.root
		self.maxNode = other.maxNode
		self.treeSize = other.treeSize
		

	def getMinKey(self):
		minNode = self.root
		while (minNode.left.key is not None):
			minNode = minNode.right
		return minNode.key


	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node: AVLNode):
		# define t1 - smaller Tree, t2 - bigger tree
		t1 = AVLTree(node.left)
		t2 = AVLTree(node.right)
		node.right = AVLNode(None,None,node,True)
		node.left = AVLNode(None,None,node,True)
		counter = 0
		while(node is not None):
			currKey = node.key
			node = node.parent
			if(node is not None):
				#add to smaller
				if(node.key < currKey):
					temp1 = AVLTree(node.left)
					node.left = AVLNode(None,None,node,True)
					node.right = AVLNode(None,None,node,True)
					t1.join(temp1, node.key, node.value)
					
				#add to bigger
				elif(node.key > currKey):
					temp2 = AVLTree(node.right)
					node.right = AVLNode(None,None,node,True)
					node.left = AVLNode(None,None,node,True)
					t2.join(temp2, node.key, node.value)

			counter += 1
		return t1, t2
	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		#if tree is empty
		if(self.root is None):
			return []
		lst = []
		def avl_to_array_rec(node: AVLNode,lst):
			if(not node.is_real_node()):
				return
			avl_to_array_rec(node.left, lst)
			lst.append((node.key,node.value))
			avl_to_array_rec(node.right, lst)
			return
		avl_to_array_rec(self.root, lst)
		return lst


	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	def max_node(self):
		return self.maxNode

	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return self.treeSize	


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root
	
def print_tree_visual(node, level=0, prefix="Root: "):
    if node.key is not None:
        print_tree_visual(node.right, level + 1, "R--- ")
        print(' ' * 6 * level + prefix + str(node.key) + " | H " + str(node.height) + " BF " + str(node.getBalanceFactor()))
        print_tree_visual(node.left, level + 1, "L--- ")
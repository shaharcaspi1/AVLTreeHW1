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
		self.height = max(self.left.height, self.right.height) + 1
		
	def getBalanceFactor(self):
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
				successor = successor.left.key
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
		A.height = max(A.left.height, A.right.height)
		B.height = max(B.left.height, B.right.height)

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
		A.height = max(A.left.height, A.right.height)
		B.height = max(A.height, B.right.height)

		return
		


	def rotationRL(self):
		self.right.rotationR
		self.rotationL

		return
	
	def rotationLR(self):
		self.left.rotationL
		self.rotationR

		return
	
	#master for rotation, gets a node and its BF (always 2 if rotation is needed), and its son in the problematic route
	def rotate(self, BF, son):
		sonBF = son.getBalanceFactor()
		if(BF == 2):
			if(sonBF == 1 or sonBF == 0):
				self.rotationR()
			elif(sonBF == -1):
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
	def __init__(self):
		self.root = None
		self.maxNode = None
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
		# initialize variables for search
		currentNode = self.max_node
		searchLength = 0
		# loop for going up to find sub tree that key suppodes to be in
		while (key < currentNode.key):
			if (currentNode == self.get_root):
				break
			if (key < currentNode.parent):
				currentNode = currentNode.parent
				searchLength += 1
				continue
			elif (key > currentNode.parent):
				break
		# if got to root - do a regular search
		if (currentNode == self.get_root):
			x,e = self.search(key)
			# if not found return None, -1
			if (x == None):
				return None,-1
			# if found add e to searchLength add return
			else:
				searchLength += e
				return x, searchLength
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
			return currentNode, searchLength
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
			self.max_node = self.root
			self.treeSize += 1
			return
		#inserting the node
		parentNode, searchHeight = self.searchMaster(key, False)
		node = AVLNode(key,val)
		node.setParent(parentNode)
		node.updateHeight()

		#tree fields stuff
		self.treeSize += 1
		if (key > self.max_node.key):
			self.max_node = node
		
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
		
		return None, -1, -1


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
		return	

	
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
		return


	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):
		return None, None

	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		return None


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
	

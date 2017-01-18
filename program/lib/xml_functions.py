import libxml2
class xPathEdit:
	def loadXML (self,string):
		self.doc = libxml2.parseMemory(string)
	def load (self,file):
		self.doc = libxml2.parseFile(file)
	def saveXML(self):
		return self.doc.serialize(None,  1)
	def save(self,file):
		self.doc.saveFormatFile(file,True)
	def free(self):
		self.doc.free()
	def edit_with_xpath(self,query,new):
		ctxt =self.doc.xpathNewContext()
		res = ctxt.xpathEval(query)
		try:
			res[0].setContent(new)
		except:
			return False
	def delete_with_xpath(self,query):
		while True:
			try:
				ctxt =self.doc.xpathNewContext()
				res = ctxt.xpathEval(query)
				if res[0].content == None:
					break
			except:
				break
			for r in res:
				try:
					r.unlinkNode()
				except:
					return False
	def return_with_xpath(self,query):
		ctxt =self.doc.xpathNewContext()
		res = ctxt.xpathEval(query)
		return res[0].content
	def return_dict_with_xpath(self,query):
		ctxt =self.doc.xpathNewContext()
		res = ctxt.xpathEval(query)
		out = {}
		for result in res[0]:
			if result.get_type() == 'element':
				out[result.get_name()] = result.content
		return out
	def insert_with_xpath(self,query,name,value,id=None):
		ctxt = self.doc.xpathNewContext()
		res = ctxt.xpathEval(query)
		try:
			for r in res:
				new = r.newChild(None,name,value)
				if id != None:
					new.newProp('id',id)
		except:
			return False
	def insert_CDATA_with_xpath(self,query,name,value,id=None):
		ctxt = self.doc.xpathNewContext()
		res = ctxt.xpathEval(query)
		try:
			for r in res:
				new = r.newChild(None,name,"")
				cdata = self.newCDataBlock(value,len(value))
				new.addChild(cdata)
				if id != None:
					new.newProp('id',id)
				return True
		except:
			return False
class DOMX(xPathEdit):
	def __init__(self):
		self.arr = []	
	def xBuildEngine(self,node,dic,base):
		element = node.get_children()
		new = dic
		while element: 
			next = element.next 
			if element.get_type() == "text" or element.get_type() == "cdata":
				try:
					new[element.parent.get_name()] += element.content.strip()
				except:
					new[element.parent.get_name()] = element.content.strip()
			if element.get_properties():
				for att in element.get_properties():
					if att.get_type() == 'attribute':
						new[att.get_name()] = att.content
			if element.children:
				self.xBuildEngine(element,new,base)
			if element.get_name() == base:
				self.arr += [new]
				new= {}
			element = next
	def xBuild(self):
		new = {}
		base = self.doc.getRootElement().children.next.get_name()
		self.xBuildEngine(self.doc.getRootElement(),new,base)
		return self.arr
	def xBuildNode(self,node):
		new = {}
		for search in self.doc.getRootElement().children:
			if search.get_name() == node:
				base = search.get_name()
				find = search
				break
		self.xBuildEngine(find,new,None)
		return self.arr

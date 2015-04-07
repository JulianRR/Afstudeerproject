class Goods():
	def __init__(self, id, value, perish_factor):
		self.id = id
		self.value = value # The value of the good
		self.perish_factor = perish_factor # Either True or False

	def decrease(self, perish_factor):
		self.value = self.value * perish_factor
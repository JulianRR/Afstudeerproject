class Goods():
	def __init__(self, id, value, perish_factor, production_time):
		self.id = id
		# self.type = type can be used to identify what kind of product it is
		self.value = value # The value of the good
		self.perish_factor = perish_factor 
		self.production_time = production_time
		self.life = perish_factor
		self.time_until_production = production_time

	def decrease(self, perish_factor):
		self.value = self.value * perish_factor
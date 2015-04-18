class Goods():
	def __init__(self, id, value, perish_period, production_delay):
		self.id = id
		# self.type = type can be used to identify what kind of product it is
		self.value = value # The value of the good
		self.perish_period = perish_period 
		self.production_delay = production_delay
		self.life = perish_period
		self.time_until_production = production_delay

		self.grid_pos = [0, 0, 0]

	def decrease(self, perish_period):
		self.value = self.value * perish_period
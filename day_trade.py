import sqlite3
import array

class script_details:
	funds=-1
	quantity=0
	code=""
	open_val=0
	close_val=0
	def __init__ (self, _code, _open_val, _close_val):
		self.code = _code
		self.open_val = _open_val
		self.close_val = _close_val

money = 100000
scripts = 3
gain_period = 20
script_count = 0

conn = sqlite3.connect("sensex-data.db")
c = conn.cursor()

business_day = 22

gainer_list = []
while (business_day < 248):
	print business_day, money
	c.execute("SELECT sc_code, day_open, day_close FROM sensex_mini WHERE day_of_year = ? ORDER BY TWENTY_DAY_GAIN DESC LIMIT ?", (business_day,scripts,))
	script_fund = money / scripts
	for script_entry in c: 	# get the max gainers for the business_day
		gainer = script_details(script_entry[0], script_entry[1], script_entry[2])		
		gainer_list.append(gainer)
	
	#sell them after hold_period
	business_day += 1
	if (business_day < 248):
		for gainer in gainer_list:
			c.execute("SELECT day_open, day_close FROM sensex_mini WHERE sc_code = ? AND day_of_year = ?", (gainer.code, business_day,))
			prices = c.fetchone()
			# buy them at open day price
			gainer.open_val = prices[0]
			gainer.close_val = prices[1]
			gainer.fund = script_fund
			gainer.quantity = (gainer.fund / gainer.open_val)
			money -= gainer.fund

			# sell them at close day price
			gainer.fund = gainer.close_val * gainer.quantity
			gainer.quantity = 0
			money += gainer.fund # consolidate the amount in 'money'			
	gainer_list[:] = []

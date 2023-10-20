#!/home/owner/Desktop/torii-dev/bin/python3

"""
code by kumohakase (2023)
powered by torii-HDL
"""

from torii import * #needed for torii-HDL
from torii.sim import * #needed for simulation

class logic4511(Elaboratable): #module logic4511
	def __init__(self):
		#Module port definition
		#Torii does not care about signal direction?
		#self.(pinname) = Signal([bitcount])
		#omitted [bitcount] means single bit
		self.le = Signal() #LE pin (logic signal)
		self.bi = Signal() #BI pin (logic signal)
		self.lt = Signal() #LT pin (logic signal)
		self.d = Signal(4) #A,B,C and D pin (4 bit logic signal)
		self.q = Signal(6) # a ... g pin (6bit logic signal)
	def elaborate(self, platform) -> Module:
		m = Module()
		#Internal signal definition
		_d = Signal(4) #latched input (4 bit logic signal)
		_q = Signal(6) #temp output (6 bit logic signal)
		#module behavior description
		#torii is HDL based python and it uses special syntax for describing
		#module behavior not to be confused with normal python code
		#latch
		with m.If(self.le == 0): #If le pin is logic '0' (with m.If(condition):)
			m.d.comb += _d.eq(self.d) #_d will be d (m.d.comb += (dest).eq(src) )
		#Switch case syntax for truth table
		#with m.Switch(expr):
		#	with m.Case(val):
		#		will be enabled when expr = val
		with m.Switch(_d):
			with m.Case(0):
				m.d.comb += _q.eq(0b1111110)
			with m.Case(1):
				m.d.comb += _q.eq(0b0110000)
			with m.Case(2):
				m.d.comb += _q.eq(0b1101101)
			with m.Case(3):
				m.d.comb += _q.eq(0b1111001)
			with m.Case(4):
				m.d.comb += _q.eq(0b0110001)
			with m.Case(5):
				m.d.comb += _q.eq(0b1011011)
			with m.Case(6):
				m.d.comb += _q.eq(0b1011111)
			with m.Case(7):
				m.d.comb += _q.eq(0b1110000)
			with m.Case(8):
				m.d.comb += _q.eq(0b1111111)
			with m.Case(9):
				m.d.comb += _q.eq(0b1111011)
			with m.Default():
				m.d.comb += _q.eq(0)
		#Output selection, if bi pin = 0 outputs will be all 0, if lt pin =0, outputs will be all 1
		with m.If(self.lt == 0):
			m.d.comb += self.q.eq(0b1111111) # q <= "1111111"
		with m.Elif(self.bi == 0): #Else if q <= "0000000"
			m.d.comb += self.q.eq(0)
		with m.Else(): # else q<= _q
			m.d.comb += self.q.eq(_q)
		
		return m #Do not forgot this

#HDL ends. Code for simulation begins.

dut = logic4511() #dut = modulename()
def bench():
	#Executed whie simulation
	#Initial condition definition
	yield dut.le.eq(0) # le pin = 0
	yield dut.bi.eq(1) # bi pin = 0
	yield dut.lt.eq(1) # lt pin = 1
	for i in range(10):
		yield dut.d.eq(i)
		yield Delay(0.001) #1mS delay for simulation
		yield Settle() #simulate 1 tick

#Simulation code template for combined logic circult
sim = Simulator(dut)
sim.add_process(bench)
with sim.write_vcd("sample.vcd"): #you can change output filename
	sim.run()

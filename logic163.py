#!/home/owner/Desktop/torii-dev/bin/python3

"""
code by kumohakase (2023)
powered by torii-HDL
"""

from torii import * #needed for torii-HDL
from torii.sim import * #needed for simulation

class logic163(Elaboratable): #module logic4511
	def __init__(self):
		#Module port definition
		#Torii does not care about signal direction?
		#self.(pinname) = Signal([bitcount])
		#omitted [bitcount] means single bit
		self.clr = Signal() #clr pin
		self.load = Signal() #load pin
		self.ent = Signal() #ent pin
		self.enp = Signal() #enp pin
		self.rco = Signal() #rco pin
		self.d = Signal(4) #data input pin (4bit)
		self.q = Signal(4) #data output pin (4bit)
	def elaborate(self, platform) -> Module:
		m = Module()
		#Internal signal definition
		#Nothing here this time.
		#module behavior description
		#torii is HDL based python and it uses special syntax for describing
		#module behavior not to be confused with normal python code
		# rco <= q[0] and q[1] and q[2] and q[3] and ent
		#note: for logic, do not use and, instead, use &.
		m.d.comb += self.rco.eq(self.q[0] & self.q[1] & self.q[2] & self.q[3] & self.ent)
		#counter part is sequential logic and described using
		#m.d.sync, not m.d.comb (m.d.comb is for combined logic)
		#the logic in m.d.sync will be activated when self.clk L-->H edgeed
		with m.If(self.clr == 0): # If clr = '0' then
			m.d.sync += self.q.eq(0) # q <= "0000"
		with m.Elif(self.load == 0): # ElsIf load = '0' then
			m.d.sync += self.q.eq(self.d) # q <= d
		with m.Elif(self.ent & self.enp): #If ent and emp then
			m.d.sync += self.q.eq(self.q + 1) # q <= q + 1
		return m #Do not forgot this

#HDL ends. Code for simulation begins.
dut = logic163() #dut = modulename()
def bench():
	#Executed whie simulation
	#Initial condition definition
	yield dut.clr.eq(0) #clr=0
	yield dut.load.eq(1) #load=1
	yield dut.ent.eq(1) #ent=1
	yield dut.enp.eq(1) #enp=1
	yield dut.d.eq(0) #d = "0000"
	#After init
	for i in range(100):
		#clr=1 after 5 ticks (reset negate)
		if i > 5:
			yield dut.clr.eq(1)
		yield #simulate 1 tick (clk advance)

#Simulation code template for sequential logic circult
sim = Simulator(dut)
sim.add_clock(0.001) #you can change clock speed, but specify interval not freq
sim.add_sync_process(bench)
with sim.write_vcd("sample.vcd"): #you can change output filename
	sim.run()

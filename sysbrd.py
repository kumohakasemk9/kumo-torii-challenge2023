#!/home/owner/Desktop/torii-dev/bin/python3

"""
code by kumohakase (2023)
powered by torii-HDL
"""

from torii import * #needed for torii-HDL
from torii.sim import * #needed for simulation
#IC chips on board
from logic4511_2 import *
from logic163 import *

#Counter system pcb using 74xx4511 and 74XX163.

class sysbrd(Elaboratable):
	def __init__(self):
		#Module port definition
		#Torii does not care about signal direction?
		#self.(pinname) = Signal([bitcount])
		#omitted [bitcount] means single bit
		self.clr = Signal() #Counter clear input
		self.com = Signal(2) #7Segment coms output for dynamic drive
		self.seg = Signal(6) #7segnent common segs output dynamic drive
	def elaborate(self, platform) -> Module:
		m = Module()
		#add clock domain named segdrive, this allow you having multiple clock signal in single design
		m.domains += ClockDomain("sync")
		m.domains += ClockDomain("segdrive")
		#Internal signal definition
		reset0 = Signal()
		reset1 = Signal()
		en0 = Signal()
		en1 = Signal()
		qsel = Signal(4)
		#submodules definition, we will use m.d.comb for submodule interconnection
		u0 = logic163()
		u1 = logic163()
		u2 = logic4511()
		m.submodules.ic0 = u0
		m.submodules.ic1 = u1
		m.submodules.ic2 = u2
		
		#module behavior description
		#torii is HDL based python and it uses special syntax for describing
		#module behavior not to be confused with normal python code
		#note: for logic, do not use and, instead, use &. (~ = not, | = or)
		m.d.comb += [
			en0.eq(u0.q[0] & u0.q[3]), # en0 <= q0(0) and q0(3)
			en1.eq(en0 & u1.q[0] & u1.q[3]), # en1 <= en0 and q1(0) and q1(3)
			reset0.eq(~en0 & self.clr), # reset0 <= (not en0) and clr, ~ means not
			reset1.eq(~en1 & self.clr), #reset1 <= (not en1) and clr
			self.com[0].eq(ClockSignal("segdrive")), # com(0) <= clk
			self.com[1].eq(~ClockSignal("segdrive")), # com(1) <= not clk
			#ClockSignal(domainname) is clock signal of domain name
			#multiplexer: qsel is q of u0 when clk='' otherwise q of u1
			qsel.eq(Mux(ClockSignal("segdrive"), u0.q, u1.q))
		]
		
		#submodule signal interconnect
		ALWAYS_1 = (
			u0.load,
			u0.ent, 
			u0.enp,
			u1.load,
			u1.enp,
			u2.bi,
			u2.lt
			)
		for i in ALWAYS_1:
			m.d.comb += i.eq(1)
		m.d.comb += [
			u0.clr.eq(reset0),
			u1.clr.eq(reset1),
			u1.ent.eq(en0),
			u2.le.eq(0),
			u2.d.eq(qsel),
			self.seg.eq(u2.q)
		]
		return m #Do not forgot this

#HDL ends. Code for simulation begins.

dut = sysbrd() #dut = modulename()
def bench():
	#Executed whie simulation
	#Initial condition definition
	
	#After init
	for i in range(100):
		#clr=1 after 5 ticks (reset negate)
		if i > 5:
			yield dut.clr.eq(1)
		yield #simulate 1 tick (clk advance)

#Simulation code template for sequential logic circult
sim = Simulator(dut)
#you can change clock speed, but specify interval not freq
#also you can define multiple clocks
sim.add_clock(0.001)
sim.add_clock(0.0001, domain="segdrive") #add clock signal to domain segdrive
sim.add_sync_process(bench)
with sim.write_vcd("sample.vcd"): #you can change output filename
	sim.run()

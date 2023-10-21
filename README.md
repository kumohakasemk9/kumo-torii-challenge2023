# Kumo's Torii-HDL challenge   
---
Torii-HDL equivalent of my VHDL BCD counter board project

# How to use
---
Please install torii-hdl and execute sysbrd.py in the env.   
You will see 2 main signals (com and seg) and   
2 important interanl signals (ic0.q and ic1.q)    
ic0.q represents BCD digit0 and ic1.q represents BCD digit1    
And I wanted to output them using dynamic driven 7seg    
seg is 7seg decoded value for each digits    
that will swap digit0 and 1 repeatedly, com is    
7seg led common pin output (aka digit enable)   
    
Code is also written to be mini-in-source-code-tutorial but   
not sure it is good or bad, official tutorial (?) of torii-HDL is at
https://torii.shmdn.link/   
    
    
# Thanks
---
Powered by Torii-HDL   
Thanks to torii-HDL and their ancestor Amaranth    
and great helper cat&dragon akinyan and dragonmux   
They deserve huge headpats pat pat pat pat...   

# License      
--- 
You are free to destribute, modify without modifying this section.     
Please consider support me on kofi.com https://ko-fi.com/kumohakase   
Licensed under Creative commons CC-BY https://creativecommons.org/licenses/by/4.0/    

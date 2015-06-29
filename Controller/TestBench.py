
from __future__ import print_function

from myhdl import *
from Simulator import *
from SdramCntl import *
from host_intf import host_intf

def test_readWrite():

    clk_i = Signal(bool(0))
    rst_i = ResetSignal(0,active=1,async=True)
    
    clkDriver_Inst  = clkDriver(clk_i)
    sd_intf_Inst    = sd_intf(clk_i)
    host_intf_Inst  = host_intf(clk_i)
    
    sdram_Inst = sdram(sd_intf_Inst)    
    test_readWrite_Inst = test_readWrite(host_intf_Inst,sd_intf_Inst)

    # use a function so the testbench signals can be traced
    def _teststim():
        sdramCntl_Inst = SdramCntl(host_intf_Inst, sd_intf_Inst, rst_i)

        @instance
        def test():
            yield delay(140)
            yield host_intf.write(120,23)
            yield host_intf.done_o.posedge
            yield host_intf.nop()
            yield delay(20)
            yield host_intf.read(120)
            yield host_intf.done_o.posedge
            print("sd val ", sd_intf.dq.val)
            print("Data Value : ",host_intf.data_o)
        
        return sdramCntrl_Inst, test

    # all the generators (processes) for the simulation, only trace
    # the stimulus and controller for now
    gsim = traceSignal(_teststim) + [clkDriver_Inst, sdram_Inst,
                                     readWrite_Inst]
    sim = Simulation(gsim).run()

if __name__ == '__main__':
    test_readWrite()

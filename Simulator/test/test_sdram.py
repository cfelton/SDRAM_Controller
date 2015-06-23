
from __future__ import print_function
from __future__ import division

import sys
sys.path.append('../..')
import os

from myhdl import *
from Simulator import *

def test_readWrite():
    
    # signals and interfaces
    clk = Signal(bool(0))
    sd = sd_intf(clk)

    # typically the DUT will be instantiated in the function that
    # is passed to `traceSignals`.  An error occurred parsing the 
    # signals so the sdram model had to be instantiated outside the
    # function to be traced??
    #sdram_Inst = sdram(sd)  # DUT instance (SDRAM model)

    # this is the core of the test
    def _run_test():
        clkDriver_Inst = clkDriver(clk)  # SDRAM clock generation
        sdram_Inst = sdram(sd)           # design-under-test (DUT)

        @instance
        def test():
            yield delay(120)
            sd.cke.next = 1

            # ?? description what this sequence is ??
            yield sd.nop()
            yield sd.activate(17)
            yield sd.nop()
            yield delay(10)
            yield sd.write(20, 31)  # write 31 to address 20?
            yield delay(10)
            yield sd.nop()
            yield delay(10)
            yield sd.read(20)       # read address 20 (where does the result go?)
            yield delay(10)
            yield sd.nop()
            yield delay(20)

            # ?? descripiton what this loop is ??
            for i in range(20):
                print(sd.dq.val)
                yield delay(10)
            print("hello world")

            # notify simulator we are done
            raise StopSimulation
        
        # return the DUT and stimuls generators
        return test, sdram_Inst, clkDriver_Inst

    # trace the signals in the testbench and the model for debug
    # and manual verification
    g = traceSignals(_run_test)

    #if os.path.isfile('_run_test.vcd'):
    #    os.remove('_run_test.vcd')

    sim = Simulation(g)
    sim.run()


if __name__ == '__main__':
    test_readWrite()

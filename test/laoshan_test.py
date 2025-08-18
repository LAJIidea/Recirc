#!/usr/bin/env python3
"""
Original Laoshan test, updated to use the proper recirc module.
"""

from recirc import *

# Define pipeline  
@Pipeline()
class pipe:
    fe = 0
    id = 0  
    ex0 = "M130_PIPE.ex"
    ex1 = 0
    wb = 0

# Define vector register file
@Regfile(16, 128)
class vr:
    wp0: WritePort
    wp1: WritePort
    rp0: ReadPort
    rp1: ReadPort
    rp2: ReadPort

# Define vector register operand
@Operand(vr)
class vreg:
    def __init__(self, idx: Uint[4]):
        self.idx = idx

# Define vector ALU
@FuncUnit([pipe.ex0, pipe.ex1])
class valu:
    pass

# Define vector MAC instruction
@Instruction
def vmac(vd: vreg, vs: vreg, vt: vreg):
    with stage([pipe.id]):
        src0: Uint[128] = vs.rp0
        src1: Uint[128] = vt.rp1
        dst: Uint[128] = vd.rp2
    with action(valu):
        for i in range(4):
            dst[32*i + 31 : 32 * i] = dst[32*i + 31 : 32 * i] + src0[32*i + 31 : 32 * i] * src1[32*i + 31 : 32 * i]
    with stage([pipe.wb]):
        vd.wp0 = dst

print(vr)

# Simulation
@VerilogSim(data={})
def sim():
    vs = vreg(0)
    vt = vreg(1)
    vd = vreg(2)

    mem = std_mem(128, 1, 1)
    vs.wp0 = 10
    vt.wp0 = 10
    vd.wp0 = 10
    vmac(vd, vs, vt)
    mem.write(0, vd.rp0)

# Execute simulation
sim()
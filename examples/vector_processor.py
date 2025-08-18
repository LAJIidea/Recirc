#!/usr/bin/env python3
"""
Example processor description using the Recirc DSL.

This example demonstrates a simple vector processor with:
- A 5-stage pipeline
- Vector register file with multiple ports
- Vector multiply-accumulate instruction
- Simulation framework
"""

from recirc import *


# Define a 5-stage pipeline
@Pipeline()
class pipe:
    fe = 0      # Fetch stage
    id = 0      # Decode stage  
    ex0 = "M130_PIPE.ex"  # Execute stage 0
    ex1 = 0     # Execute stage 1
    wb = 0      # Writeback stage


# Define a vector register file with 16 registers, 128 bits each
@Regfile(16, 128)
class vr:
    wp0: WritePort   # Write port 0
    wp1: WritePort   # Write port 1
    rp0: ReadPort    # Read port 0
    rp1: ReadPort    # Read port 1
    rp2: ReadPort    # Read port 2


# Define vector register operand type
@Operand(vr)
class vreg:
    def __init__(self, idx: Uint[4]):
        """
        Initialize vector register operand.
        
        Args:
            idx: 4-bit register index
        """
        self.idx = idx


# Define a vector ALU functional unit
@FuncUnit([pipe.ex0, pipe.ex1])
class valu:
    """Vector ALU that can execute on either ex0 or ex1 stages."""
    pass


# Define a vector multiply-accumulate instruction
@Instruction
def vmac(vd: vreg, vs: vreg, vt: vreg):
    """
    Vector multiply-accumulate: vd = vd + vs * vt
    
    Args:
        vd: Destination vector register
        vs: Source vector register 1  
        vt: Source vector register 2
    """
    # Decode stage: read operands
    with stage([pipe.id]):
        src0: Uint[128] = vs.rp0  # Read vs through port 0
        src1: Uint[128] = vt.rp1  # Read vt through port 1
        dst: Uint[128] = vd.rp2   # Read vd through port 2
    
    # Execute: perform MAC operation on vector ALU
    with action(valu):
        # Process 4 32-bit elements in parallel
        for i in range(4):
            # Extract 32-bit elements and perform MAC
            dst[32*i + 31 : 32 * i] = (
                dst[32*i + 31 : 32 * i] + 
                src0[32*i + 31 : 32 * i] * src1[32*i + 31 : 32 * i]
            )
    
    # Writeback stage: write result
    with stage([pipe.wb]):
        vd.wp0 = dst  # Write result back through port 0


# Simulation setup
@VerilogSim(data={})
def simulate_vmac():
    """Simulate the vector MAC instruction."""
    # Create vector register operands
    vs = vreg(0)  # Use register 0
    vt = vreg(1)  # Use register 1
    vd = vreg(2)  # Use register 2

    # Create memory for data storage
    mem = std_mem(128, 1024, 1)  # 128-bit wide, 1024 words, 1 bank
    
    # Initialize registers with test data
    vs.wp0 = 0x12345678_9ABCDEF0_12345678_9ABCDEF0  # Test vector 1
    vt.wp0 = 0x11111111_22222222_33333333_44444444  # Test vector 2  
    vd.wp0 = 0x00000000_00000000_00000000_00000000  # Initialize accumulator
    
    # Execute the vector MAC instruction
    vmac(vd, vs, vt)
    
    # Store result to memory
    mem.write(0, vd.rp0)
    
    print(f"Vector MAC simulation completed")
    print(f"Result stored in memory at address 0")


if __name__ == "__main__":
    # Print some information about the defined architecture
    print("Recirc Vector Processor Example")
    print("==============================")
    print(f"Pipeline stages: {[attr for attr in dir(pipe) if not attr.startswith('_')]}")
    print(f"Vector register file: {vr}")
    print(f"Vector register size: {getattr(vr, '_regfile_size', 'unknown')}")
    print(f"Vector register width: {getattr(vr, '_regfile_width', 'unknown')} bits")
    print()
    
    # Run the simulation
    simulate_vmac()
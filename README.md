# Recirc - Processor Architecture Description Language

Recirc is a Python-based domain-specific language (DSL) for describing processor architectures, instruction sets, and generating hardware implementations through MLIR/CIRCT.

## Overview

This project provides a high-level Python DSL that allows you to:

- Define processor pipeline stages and functional units
- Describe register files and memory hierarchies  
- Specify instruction semantics and data flow
- Generate hardware implementations via MLIR/CIRCT compilation
- Simulate processor behavior

## Example Usage

```python
from recirc import *

# Define a pipeline
@Pipeline()
class pipe:
    fe = 0      # Fetch stage
    id = 0      # Decode stage  
    ex0 = "M130_PIPE.ex"  # Execute stage 0
    ex1 = 0     # Execute stage 1
    wb = 0      # Writeback stage

# Define a vector register file
@Regfile(16, 128)  # 16 registers, 128 bits each
class vr:
    wp0: WritePort
    wp1: WritePort
    rp0: ReadPort
    rp1: ReadPort
    rp2: ReadPort

# Define vector register operand type
@Operand(vr)
class vreg:
    def __init__(self, idx: Uint[4]):
        self.idx = idx

# Define a vector ALU functional unit
@FuncUnit([pipe.ex0, pipe.ex1])
class valu:
    pass

# Define a vector multiply-accumulate instruction
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
```

## Installation

```bash
pip install -e .
```

## Requirements

- Python 3.7+
- MLIR/LLVM (for hardware generation)
- CIRCT (for hardware compilation)

## Project Structure

- `recirc/` - Core DSL implementation
- `core/` - C++/MLIR integration layer
- `test/` - Example processor descriptions and tests
- `cmake/` - Build configuration

## Features

### Pipeline Description
- Multi-stage pipeline definition
- Stage-specific resource allocation
- Data flow specification

### Register Files
- Configurable size and width
- Multiple read/write ports
- Type-safe operand handling

### Instruction Definition
- Declarative syntax for instruction semantics
- Automatic resource allocation
- Pipeline stage binding

### Hardware Generation
- MLIR intermediate representation
- CIRCT-based hardware compilation
- Verilog output generation

## License

[License information to be added]

## Contributing

[Contributing guidelines to be added]
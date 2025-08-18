"""
Recirc: A Python DSL for processor architecture description and hardware generation.

This module provides the core classes and decorators for defining:
- Processor pipelines and stages
- Register files and operands
- Functional units
- Instructions and their semantics
- Simulation infrastructure
"""

from typing import Any, List, Dict, Union, Optional
from abc import ABC, abstractmethod


class Pipeline:
    """Decorator for defining processor pipeline stages."""
    
    def __init__(self):
        pass

    def __call__(self, cls, *args: Any, **kwds: Any) -> Any:
        """Apply pipeline decoration to a class."""
        original_init = cls.__init__

        def new_init(instance, *args, **kwargs):
            original_init(instance, *args, **kwargs)
        
        cls.__init__ = new_init
        for attr_name, attr_value in cls.__dict__.items():
            if isinstance(attr_value, staticmethod):
                setattr(self, attr_name, attr_value)
        return cls


class Regfile:
    """Decorator for defining register files with specified size and bit width."""
    
    def __init__(self, size: int, width: int):
        """
        Initialize register file definition.
        
        Args:
            size: Number of registers in the file
            width: Bit width of each register
        """
        self.size = size
        self.width = width

    def __class_getitem__(cls, index):
        """Support for generic syntax like Regfile[index]."""
        pass

    def __call__(self, cls, *args: Any, **kwds: Any) -> Any:
        """Apply regfile decoration to a class."""
        cls._regfile_size = self.size
        cls._regfile_width = self.width
        return cls


class ReadPort:
    """Represents a read port for a register file."""
    
    def __init__(self, regfile_ref=None, port_id=None):
        self.regfile_ref = regfile_ref
        self.port_id = port_id
        self._value = 0  # Simulate stored value
        
    def __getitem__(self, key):
        """Support bit slicing operations."""
        if isinstance(key, slice):
            return BitSlice(self, key.start, key.stop)
        return self
        
    def __setitem__(self, key, value):
        """Support bit slice assignment."""
        # In a real implementation, this would modify the underlying value
        pass


class WritePort:
    """Represents a write port for a register file."""
    
    def __init__(self, regfile_ref=None, port_id=None):
        self.regfile_ref = regfile_ref
        self.port_id = port_id
        self._value = 0  # Simulate stored value
        
    def __getitem__(self, key):
        """Support bit slicing operations."""
        if isinstance(key, slice):
            return BitSlice(self, key.start, key.stop)
        return self
        
    def __setitem__(self, key, value):
        """Support bit slice assignment."""
        # In a real implementation, this would modify the underlying value
        pass


class Operand:
    """Decorator for defining operand types that reference register files."""
    
    def __init__(self, regfile):
        """
        Initialize operand with a reference to a register file.
        
        Args:
            regfile: The register file this operand type references
        """
        self.regfile = regfile
        
    def __call__(self, cls, *args: Any, **kwds: Any) -> Any:
        """Apply operand decoration to a class."""
        cls._operand_regfile = self.regfile
        # Preserve the original class functionality
        original_init = cls.__init__
        
        def new_init(instance, *args, **kwargs):
            original_init(instance, *args, **kwargs)
            # Add register file ports as attributes
            instance.rp0 = ReadPort(self.regfile, 'rp0')
            instance.rp1 = ReadPort(self.regfile, 'rp1') 
            instance.rp2 = ReadPort(self.regfile, 'rp2')
            instance.wp0 = WritePort(self.regfile, 'wp0')
            instance.wp1 = WritePort(self.regfile, 'wp1')
        
        cls.__init__ = new_init
        return cls


class FuncUnit:
    """Decorator for defining functional units and their associated pipeline stages."""
    
    def __init__(self, stage_list: List[Union[str, int]]):
        """
        Initialize functional unit with associated pipeline stages.
        
        Args:
            stage_list: List of pipeline stages this unit can execute on
        """
        self.stage_list = stage_list

    def __call__(self, cls, *args: Any, **kwds: Any) -> Any:
        """Apply functional unit decoration to a class."""
        cls._func_unit_stages = self.stage_list
        return cls


def Instruction(func):
    """Decorator for defining instruction semantics and behavior."""
    func._is_instruction = True
    return func


class stage:
    """Context manager for defining pipeline stage constraints."""
    
    def __init__(self, stage_list: List[Union[str, int]]):
        """
        Initialize stage context.
        
        Args:
            stage_list: List of pipeline stages for this operation
        """
        self.stage_list = stage_list
    
    def __enter__(self):
        """Enter stage context."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit stage context."""
        pass


class action:
    """Context manager for defining functional unit actions."""
    
    def __init__(self, func_unit):
        """
        Initialize action context.
        
        Args:
            func_unit: The functional unit performing this action
        """
        self.func_unit = func_unit
    
    def __enter__(self):
        """Enter action context."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit action context."""
        pass


class Uint:
    """Type hint for unsigned integer types with specified bit width."""
    
    def __class_getitem__(cls, width: int):
        """
        Create a typed unsigned integer.
        
        Args:
            width: Bit width of the unsigned integer
            
        Returns:
            Type representing Uint[width]
        """
        class UintType:
            def __init__(self, value=0):
                self.value = value
                self.width = width
                
            def __getitem__(self, key):
                """Support bit slicing operations."""
                if isinstance(key, slice):
                    return BitSlice(self, key.start, key.stop)
                return self
                
            def __setitem__(self, key, value):
                """Support bit slice assignment."""
                # In a real implementation, this would modify the underlying value
                pass
                
        return UintType


class BitSlice:
    """Represents a bit slice of a value."""
    
    def __init__(self, value, start_bit, end_bit):
        self.value = value
        self.start_bit = start_bit
        self.end_bit = end_bit
        self._simulated_value = 0  # For simulation purposes
        
    def __add__(self, other):
        """Addition operation for bit slices."""
        result = BitSlice(None, self.start_bit, self.end_bit)
        # In a real implementation, this would perform actual arithmetic
        return result
        
    def __mul__(self, other):
        """Multiplication operation for bit slices.""" 
        result = BitSlice(None, self.start_bit, self.end_bit)
        # In a real implementation, this would perform actual arithmetic
        return result
        
    def __getitem__(self, key):
        """Support nested bit slicing."""
        if isinstance(key, slice):
            return BitSlice(self, key.start, key.stop)
        return self
        
    def __setitem__(self, key, value):
        """Support bit slice assignment."""
        # In a real implementation, this would modify the underlying value
        pass


class VerilogSim:
    """Decorator for defining Verilog simulation contexts."""
    
    def __init__(self, data: Dict[str, Any]):
        """
        Initialize simulation context.
        
        Args:
            data: Initial data for simulation
        """
        self.data = data

    def __call__(self, func, *args: Any, **kwds: Any) -> Any:
        """Apply simulation decoration to a function."""
        func._simulation_data = self.data
        return func


class std_mem:
    """Standard memory model for simulation."""
    
    def __init__(self, width: int, size: int, num: int):
        """
        Initialize memory model.
        
        Args:
            width: Bit width of memory words
            size: Size of memory in words
            num: Number of memory banks
        """
        self.width = width
        self.size = size 
        self.num = num
        self.memory = {}

    def write(self, addr: int, data: Any):
        """
        Write data to memory address.
        
        Args:
            addr: Memory address
            data: Data to write
        """
        self.memory[addr] = data
        
    def read(self, addr: int) -> Any:
        """
        Read data from memory address.
        
        Args:
            addr: Memory address
            
        Returns:
            Data at the specified address
        """
        return self.memory.get(addr, 0)


# Export all public classes and functions
__all__ = [
    'Pipeline', 'Regfile', 'ReadPort', 'WritePort', 'Operand', 
    'FuncUnit', 'Instruction', 'stage', 'action', 'Uint',
    'VerilogSim', 'std_mem'
]
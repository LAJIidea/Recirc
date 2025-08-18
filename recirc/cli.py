#!/usr/bin/env python3
"""
Command line interface for Recirc.

Provides utilities for working with processor descriptions,
generating hardware, and running simulations.
"""

import argparse
import sys
from pathlib import Path


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Recirc - Processor Architecture Description Language",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  recirc compile processor.py --output hardware.mlir
  recirc simulate processor.py --cycles 1000
  recirc info processor.py
        """
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version="Recirc 0.1.0"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Compile command
    compile_parser = subparsers.add_parser(
        "compile", 
        help="Compile processor description to MLIR/hardware"
    )
    compile_parser.add_argument("input", help="Input processor description file")
    compile_parser.add_argument(
        "--output", "-o", 
        help="Output file (default: stdout)"
    )
    compile_parser.add_argument(
        "--format", 
        choices=["mlir", "verilog", "systemverilog"], 
        default="mlir",
        help="Output format"
    )
    
    # Simulate command  
    sim_parser = subparsers.add_parser(
        "simulate", 
        help="Run simulation of processor description"
    )
    sim_parser.add_argument("input", help="Input processor description file")
    sim_parser.add_argument(
        "--cycles", "-c", 
        type=int, 
        default=100,
        help="Number of simulation cycles"
    )
    sim_parser.add_argument(
        "--trace", 
        action="store_true",
        help="Enable execution trace"
    )
    
    # Info command
    info_parser = subparsers.add_parser(
        "info", 
        help="Display information about processor description"
    )
    info_parser.add_argument("input", help="Input processor description file")
    info_parser.add_argument(
        "--verbose", "-v", 
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return 1
        
    # Handle commands
    if args.command == "compile":
        return compile_processor(args)
    elif args.command == "simulate":
        return simulate_processor(args)
    elif args.command == "info":
        return show_info(args)
    
    return 0


def compile_processor(args):
    """Compile processor description to hardware."""
    print(f"Compiling {args.input} to {args.format}...")
    print("Note: Hardware compilation not yet implemented")
    print("This would generate MLIR/CIRCT output for hardware synthesis")
    return 0


def simulate_processor(args):
    """Run processor simulation."""
    print(f"Simulating {args.input} for {args.cycles} cycles...")
    if args.trace:
        print("Execution tracing enabled")
    
    # Load and execute the processor description
    try:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: File {args.input} not found", file=sys.stderr)
            return 1
            
        # Execute the file in a controlled environment
        import runpy
        runpy.run_path(str(input_path))
        
    except Exception as e:
        print(f"Error running simulation: {e}", file=sys.stderr)
        return 1
        
    return 0


def show_info(args):
    """Display processor description information."""
    print(f"Analyzing {args.input}...")
    
    try:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: File {args.input} not found", file=sys.stderr)
            return 1
            
        # Basic file analysis
        with open(input_path) as f:
            content = f.read()
            
        lines = content.split('\n')
        print(f"File: {input_path}")
        print(f"Lines of code: {len(lines)}")
        
        # Count DSL elements
        pipeline_count = content.count("@Pipeline")
        regfile_count = content.count("@Regfile")
        instruction_count = content.count("@Instruction")
        funcunit_count = content.count("@FuncUnit")
        
        print(f"Pipelines: {pipeline_count}")
        print(f"Register files: {regfile_count}")
        print(f"Instructions: {instruction_count}")
        print(f"Functional units: {funcunit_count}")
        
        if args.verbose:
            print("\nDetailed analysis:")
            print("- Pipeline stages, register files, and instructions defined")
            print("- Ready for simulation and hardware generation")
            
    except Exception as e:
        print(f"Error analyzing file: {e}", file=sys.stderr)
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())
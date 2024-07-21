from typing import Any


class Pipeline:
    def __init__(self) -> None:
        pass

    def __call__(self, cls, *args: Any, **kwds: Any) -> Any:
        original_init = cls.__init__

        def new_init(instance, *args, **kwargs):
            original_init(instance, *args, **kwargs)
        
        cls.__init__ = new_init
        for attr_name, attr_value in cls.__dict__.items():
            if isinstance(attr_value, staticmethod):
                setattr(self, attr_name, attr_value)
        return cls

    


class Regfile:
    def __init__(self, size, width) -> None:
        self.size = size

    def __class_getitem__(cls, index):
        pass

    def __call__(self, cls, *args: Any, **kwds: Any) -> Any:
        print(cls)
        return 1


class ReadPort:
    pass


class WritePort:
    pass


class Operand:
    def __init__(self, regfile) -> None:
        pass
    def __call__(self, cls, *args: Any, **kwds: Any) -> Any:
        pass


class Binary:
    pass


class Syntax:
    pass


class Sematic:
    pass


class FuncUnit:
    def __init__(self, arg_list) -> None:
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass


class Instruction:
    def __init__(self, func) -> None:
        pass


class stage:
    def __enter__():
        pass

    def __exit__():
        pass


class action:
    def __enter__():
        pass

    def __exit__():
        pass


class Uint:
    def __class_getitem__(cls, index):
        pass


@Pipeline()
class pipe:
    fe = 0
    id = 0
    ex0 = "M130_PIPE.ex"
    ex1 = 0
    wb = 0


@Regfile(16, 128)
class vr:
    wp0: WritePort
    wp1: WritePort
    rp0: ReadPort
    rp1: ReadPort
    rp2: ReadPort
    

@Operand(vr)
class vreg():
    
    def __init__(self, idx: Uint[4]) -> None:
        self.idx = idx


@FuncUnit([pipe.ex0, pipe.ex1])
class valu:
    pass


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
# reg = vr()

class VerilogSim:
    def __init__(self, data) -> None:
        pass

    def __call__(self, func, *args: Any, **kwds: Any) -> Any:
        pass

class std_mem:
    def __init__(self, width, size, num) -> None:
        pass

    def write(self, addr, data):
        pass

@VerilogSim(data = {})
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
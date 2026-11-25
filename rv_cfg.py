"""Parte a implementar pelo grupo. Consulte ENUNCIADO.pdf."""
from backend_api import REGISTERS, CFG, BasicBlock, Liveness
from ir import Beq, Beqz, Bge, Blt, Bne, Bnez, Jump, Return, LabelInstr

def build_cfg(function):
    instructions = function.instructions
    n = len(instructions)

    if n == 0:
        return CFG(function = function, blocks = {}, entry = None)

    # Mapeia labels para o índice da sua LabelInstr
    label_to_index = {}
    starts = {0}

    for i, instr in enumerate(instructions):
        if isinstance(instr, LabelInstr):
            label_to_index[instr.label] = i
            starts.add(i)
        elif isinstance(instr, (Beq, Beqz, Bge, Blt, Bne, Bnez, Jump, Return)):
            if i + 1 < n:
                starts.add(i + 1)

    sorted_starts = sorted(starts)
    blocks = {}

    for idx, start in enumerate(sorted_starts):
        stop = sorted_starts[idx + 1] if idx + 1 < len(sorted_starts) else n
        blocks[start] = BasicBlock(start=start, stop=stop)

    for start, block in blocks.items():
        last = instructions[block.stop - 1]
        next_block = block.stop if block.stop < n else None

        if isinstance(last, (Beq, Beqz, Bge, Blt, Bne, Bnez)):
            block.successors.add(label_to_index[last.target])
            if next_block is not None:
                block.successors.add(next_block)
        elif isinstance(last, Jump):
            block.successors.add(label_to_index[last.target])
        elif isinstance(last, Return):
            pass
        else:
            if next_block is not None:
                block.successors.add(next_block)

    for start, block in blocks.items():
        for succ in block.successors:
            blocks[succ].predecessors.add(start)

    return CFG(function = function, blocks = blocks, entry = 0)

    #raise NotImplementedError("implemente rv_cfg")
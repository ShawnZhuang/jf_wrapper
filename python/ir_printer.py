# ir_printer.py
from io import StringIO
import pdb

import ir


class NestWriter:
    _indent = 0

    class Brace:
        SMALL = 0
        MEDIUM = 1
        LARGE = 2

        @classmethod
        def get_pair(cls, brace):
            table_ = {
                cls.SMALL: ('(', ')'),
                cls.MEDIUM: ('[', ']'),
                cls.LARGE: ('{', '}')
            }
            if brace in table_:
                return table_.get(brace)
            return (None, None)

    def __init__(self, strstream: StringIO, label: str = None, brace=Brace.LARGE, newline_after_brace=True):
        self.label = label
        self.strstream = strstream
        self.left_brace, self.right_brace = self.__class__.Brace.get_pair(
            brace)
        self.newline_after_brace = newline_after_brace

    def __enter__(self):
        if self.label is None:
            return self
        self.print_indent()
        self.strstream.write(self.label)
        if self.left_brace is not None:
            self.strstream.write(self.left_brace)
        if self.newline_after_brace:
            self.strstream.write("\n")
            self.__class__._indent += 2
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.label is None:
            return
        if self.newline_after_brace:
            self.__class__._indent -= 2
            # self.strstream.write("\n")
        if self.right_brace is not None:
            self.print_indent()
            self.strstream.write(self.right_brace)
        # if self.newline_after_brace:
        self.strstream.write("\n")

    def print_indent(self):
        for i in range(self._indent):
            self.strstream.write(" ")

    def write_cmd(self, cmd):
        if self.newline_after_brace:
            self.print_indent()
        self.strstream.write(cmd)
        if self.newline_after_brace:
            self.strstream.write("\n")

class IRPrinter:
    def __init__(self, indent=0) -> None:
        self.ss = StringIO()

    class VisitMapping:
        register_map = dict()  # class visit method

        @classmethod
        def register(cls, cls_type):
            def _register(fn):
                cls.register_map[cls_type] = fn
                return fn
            return _register

        @classmethod
        def get_method(cls, cls_type):
            if cls.register_map.get(cls_type) is None:
                raise RuntimeError(
                    "visit func for {} if not found".format(cls_type))
            return cls.register_map[cls_type]

    @VisitMapping.register(ir.sections.Pipeline)
    def visit_pipeline(self, pipeline: ir.sections.Pipeline):
        with NestWriter(self.ss, label="pipeline"):
            self.visit(pipeline.seq)

    @VisitMapping.register(ir.sections.Stages)
    def visit_stages(self, stages: ir.sections.Stages):
        with NestWriter(self.ss, "stages"):
            self.visit(stages.directives)

    @VisitMapping.register(ir.directives.Stage)
    def visit_stage(self, stage: ir.directives.Stage):
        with NestWriter(self.ss, "stage"):
            if stage.agent is not None:
                self.visit(stage.agent)
            if stage.cond is not None:
                self.visit(stage.cond)
            self.visit(stage.sections)

    @VisitMapping.register(ir.sections.Steps)
    def visit_steps(self, steps: ir.sections.Steps):
        with NestWriter(self.ss, "steps"):
            self.visit(steps.seq)

    @VisitMapping.register(ir.directives.Environment)
    def visit_stage(self, enviroment: ir.directives.Environment):
        if enviroment.pairs is None:
            return
        with NestWriter(self.ss, "environment") as writer:
            for k, v in enviroment.pairs:
                writer.write_cmd("{} = {}".format(k, v))

    @VisitMapping.register(ir.directives.Parameters)
    def visit_parameters(self, params):
        if params.seq is None:
            return
        with NestWriter(self.ss, "parameters"):
            for v in params.seq:
                self.visit(v)

    @VisitMapping.register(str)
    def visit_str(self, cmd):
        with NestWriter(self.ss, brace=NestWriter.Brace.SMALL, newline_after_brace=False) as writer:
            writer.write_cmd(cmd)

    @VisitMapping.register(ir.sections.Agent)
    def visit_agent(self, agent: ir.sections.Agent):
        self.ss.write("agent")

    def visit(self, expr):
        fn = self.VisitMapping.get_method(expr.__class__)
        fn(self, expr)

        pass


def print_ir(e):
    p = IRPrinter()
    p.visit(e)
    print(p.ss.getvalue())


if __name__ == "__main__":
    p = IRPrinter()
    with NestWriter(p.ss, "pipeline"):
        # print(Inclose._indent)
        with NestWriter(p.ss, "agent", brace=None, newline_after_brace=False):
            # print(Inclose._indent)
            p.visit(" any\n")
        with NestWriter(p.ss, "stage"):
            # print(Inclose._indent)
            p.visit("   heh\n")
        with  NestWriter(p.ss, "parameter", brace=NestWriter.Brace.SMALL, newline_after_brace=False) :
            p.visit("aaa")

    print(p.ss.getvalue())

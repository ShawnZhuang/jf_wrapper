# ir_printer.py
import ir
from io import StringIO


class IRPrinter:
    def __init__(self, indent=0) -> None:
        self._indent = 0
        self.ss = StringIO()
        pass

    def inc_indent(self):
        self._indent += 2

    def dec_indent(self):
        self._indent -= 2

    def print_indent(self):
        for i in range(self._indent):
            self.ss.write(" ")

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
    def visit_pipeline(self, pipeline):
        self.print_indent()
        self.ss.write("pipeline{\n")
        self.inc_indent()
        self.visit(pipeline.seq)
        self.dec_indent()
        self.print_indent()
        self.ss.write("}\n")
        pass

    @VisitMapping.register(ir.sections.Stages)
    def visit_stages(self, stage):
        self.ss.write("stages")
        pass

    @VisitMapping.register(ir.directives.Stage)
    def visit_stage(self, stage: ir.directives.Stage):
        self.print_indent()
        self.ss.write("stage{\n")
        self.inc_indent()
        if stage.agent is not None:
            self.visit(stage.agent)
        if stage.cond is not None:
            self.visit(stage.cond)
        self.visit(stage.sections)
        self.dec_indent()
        self.print_indent()
        self.ss.write("}\n")
    @VisitMapping.register(ir.sections.Steps)
    def visit_stage(self, stage: ir.sections.Steps):
        self.print_indent()
        self.ss.write("steps{\n")
        self.visit(stage.seq)
 
        self.dec_indent()
        self.print_indent()
        self.ss.write("}\n")
    @VisitMapping.register(ir.directives.Environment)
    def visit_stage(self, enviroment:ir.directives.Environment):
        if enviroment.pairs is None:
            return
        self.print_indent()
        self.ss.write("environment{\n")
        self.inc_indent()
        for k, v in enviroment.pairs:
            self.print_indent()
            self.ss.write("{} = {}\n".format(k, v))
        self.dec_indent()
        self.print_indent()
        self.ss.write("}\n")

    @VisitMapping.register(ir.directives.Parameters)
    def visit_stage(self, params):
        if params.seq is None:
            return
        self.print_indent()
        self.ss.write("parameters{\n")
        self.inc_indent()
        for v in params.seq:
            self.print_indent()
            self.visit(v)
            self.ss.write("\n")
            # self.ss.write("{} = {}\n".format(k, v))
        self.dec_indent()
        self.print_indent()
        self.ss.write("}\n")

    @VisitMapping.register(str)
    def visit_str(self, str):
        self.ss.write(str)

    def visit(self, expr):
        fn = self.VisitMapping.get_method(expr.__class__)
        fn(self, expr)

        pass


def print_ir(e):
    p = IRPrinter()
    p.visit(e)
    print(p.ss.getvalue())

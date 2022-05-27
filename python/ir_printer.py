# ir_printer.py
from multiprocessing.sharedctypes import Value
import pdb
from io import StringIO
from unicodedata import name

import ir
from ir.sections import Agent


def conver_str_to_text(str):
    return "\"{}\"".format(str)


class Brace:
    NONE = 0
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

    @classmethod
    def get_pair(cls, brace):
        table_ = {
            cls.NONE: (' ', ''),
            cls.SMALL: ('(', ')'),
            cls.MEDIUM: ('[', ']'),
            cls.LARGE: ('{', '}')
        }
        if brace in table_:
            return table_.get(brace)
        return (None, None)


class NestWriter:
    _indent = 0

    @classmethod
    def print_indent(cls, ss: StringIO):
        for i in range(cls._indent):
            ss.write(" ")

    @classmethod
    def get_brace_func(cls, label: str, name: str = None):
        """
        label(name){
        }
        label{
        }
        """
        def enter_func(ss: StringIO):
            cls.print_indent(ss)
            if name is None:
                ss.write("{} {{\n".format(label, name))
            else:
                ss.write("{}(\"{}\") {{\n".format(label, name))

        def exit_func(ss: StringIO):
            cls.print_indent(ss)
            ss.write("}\n")
        return enter_func, exit_func

    @classmethod
    def get_brace_oneline_func(cls, label: str, name: str = None, brace: Brace = Brace.NONE):
        """
        label(name){ body }
        label{ body }
        """
        pattern_bl = "{label}{bl}"
        pattern_name_bl = "{label}({name}){bl}"
        pattern_br = "{br}\n"
        brace_left, brace_right = Brace.get_pair(brace)

        def enter_func(ss: StringIO):
            cls.print_indent(ss)
            if name is None:
                ss.write(pattern_bl.format(label=label, bl=brace_left))
            else:
                ss.write(pattern_name_bl.format(
                    label=label, name=name, bl=brace_left))

        def exit_func(ss: StringIO):
            ss.write(pattern_br.format(br=brace_right))
        return enter_func, exit_func

    @classmethod
    def get_inline_func(cls,  value: str = None):
        """
        word         
        """
        def enter_func(ss: StringIO):
            return
            # ss.write(value)

        def exit_func(ss: StringIO):
            return
        return enter_func, exit_func

    def __init__(self, strstream: StringIO, label: str = None, value: str = None,  brace=None, is_inline=True):
        self.strstream = strstream
        self._left_func = None
        self._right_func = None
        if label is not None:
            if is_inline:
                self._left_func, self._right_func = self.__class__.get_brace_oneline_func(
                    label, value)
            else:
                self._left_func, self._right_func = self.__class__.get_brace_func(
                    label, value)
        else:  # label is None
            if is_inline:
                self._left_func, self._right_func = self.__class__.get_inline_func(
                    value)

    def __enter__(self):
        if self._left_func:
            self._left_func(self.strstream)
        self.__class__._indent += 2
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__class__._indent -= 2
        if self._right_func:
            self._right_func(self.strstream)

    def write_cmd(self, cmd):
        # if self.newline_after_brace:
        self.print_indent(self.strstream)
        self.strstream.write(cmd)
        # if self.newline_after_brace:
        # self.strstream.write("\n")


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
        with NestWriter(self.ss, label="pipeline", brace=Brace.LARGE, is_inline=False):
            self.visit(pipeline.agent)
            self.visit(pipeline.seq)

    @VisitMapping.register(ir.sections.Stages)
    def visit_stages(self, stages: ir.sections.Stages):
        with NestWriter(self.ss, "stages", brace=Brace.LARGE, is_inline=False):
            self.visit(stages.directives)

    @VisitMapping.register(ir.directives.Stage)
    def visit_stage(self, stage: ir.directives.Stage):
        with NestWriter(self.ss, "stage", value=stage.name, brace=Brace.LARGE, is_inline=False):
            if stage.agent is not None:
                self.visit(stage.agent)
            if stage.cond is not None:
                self.visit(stage.cond)
            self.visit(stage.sections)

    @VisitMapping.register(ir.sections.Steps)
    def visit_steps(self, steps: ir.sections.Steps):
        with NestWriter(self.ss, "steps", brace=Brace.LARGE, is_inline=False):
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
        self.ss.write(cmd)
        # with NestWriter(self.ss) as writer:
        #     writer.write_cmd(cmd)

    @VisitMapping.register(ir.expr.Echo)
    def visit_echo(self, echo: ir.expr.Echo):
        with NestWriter(self.ss, label="echo",  is_inline=True, brace=Brace.NONE) as writer:
            self.ss.write("\"{}\"".format(echo.info))

    @VisitMapping.register(ir.sections.Agent)
    def visit_agent(self, agent: ir.sections.Agent):
        if agent.agent_type in {Agent.AgentType.ANY, Agent.AgentType.NONE}:
            with NestWriter(self.ss, label="agent"):
                self.ss.write(agent.agent_type)
        else:
            with NestWriter(self.ss, label="agent", brace=Brace.LARGE, is_inline=False):
                with NestWriter(self.ss, label=agent.agent_type):
                    self.ss.write(conver_str_to_text(agent.value))

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
        with NestWriter(p.ss, "agent", brace=None):
            p.visit(" any\n")
        with NestWriter(p.ss, "stage"):
            p.visit("   heh\n")
        with NestWriter(p.ss, "parameter", brace=Brace.SMALL):
            p.visit("aaa")

    print(p.ss.getvalue())

from unicodedata import name
import ir
from ir import sections
import ir_printer
import unittest


class TestPipeline(unittest.TestCase):
    def test_helloworld(self):
        s1 = ir.sections.Stages(
            ir.directives.Stage(
                "hello",
                ir.sections.Steps(
                    [
                        ir.expr.Echo("hello world"),
                        ir.expr.Bash("echo hello world")
                    ]
                )
            ))
        pipe = ir.sections.Pipeline(
            agent=ir.sections.Agent(ir.sections.Agent.AgentType.ANY),
            # agent=ir.sections.Agent(ir.sections.Agent.AgentType.LABEL,"hhh"),
            seq=s1
        )
        ir_printer.print_ir(pipe)

    def setUp(self):
        print()

    def tearDown(self):
        print()


if __name__ == "__main__":
    # e = ir.sections.Pipeline(ir.directives.Stage())
    # p = ir_printer.IRPrinter()
    # p.visit(e)
    # print(p.ss.getvalue())
    unittest.main()
    pass

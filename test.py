import ir
import ir_printer
import unittest


class TestDirective(unittest.TestCase):
    def test_Environment(self):
        e = ir.directives.Environment([("GGG", "HHH"), ("a", "aa")])
        ir_printer.print_ir(e)

    def test_Parameters(self):
        e = ir.directives.Parameters(["a", "b"])
        ir_printer.print_ir(e)
    def test_Stage(self):
        e = ir.directives.Stage("a stage\n")
        ir_printer.print_ir(e)
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

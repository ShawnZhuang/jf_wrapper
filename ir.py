from textwrap import indent

from youtube_dl import main


class Pipeline:
    def __init__(self, body) -> None:
        self.body=body
        pass
    pass

class Stage:
    pass

class IRPrinter:
    indent=0
    class VisitMapping:
        register_map=dict() # class visit method
        @classmethod
        def register(cls,cls_type):
            def _register(fn):
                cls.register_map[cls_type]=fn
                return fn
            return _register
        @classmethod
        def get_method(cls, cls_type):
            if cls.register_map.get(cls_type) is None:
                raise RuntimeError("visit func for {} if not found".format(cls_type ))
            return cls.register_map[cls_type]
    @VisitMapping.register(Pipeline)
    def visit_pipeline(self, pipeline):
        print("pipe")
        self.visit(pipeline.body)
        pass
    @VisitMapping.register(Stage)
    def visit_stage(self, stage):
        print("stage")
        pass

    def visit(self, expr):
        fn=self.VisitMapping.get_method(expr.__class__)
        fn(self,expr)

        pass


if __name__ == "__main__":
    e=Pipeline(Stage())
    IRPrinter().visit(e)
    pass
    
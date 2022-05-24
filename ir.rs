pub struct Expr<T> {
    node: T,
}
pub struct Pipeline {
    agent: String,

}
pub struct Stage {
    steps: String,
}

impl Pipeline {
    pub fn make(agent: String, ) -> Pipeline {
        return Pipeline { agent: agent };
    }
}
impl Stage {
    pub fn make(steps: String) -> Stage {
        return Stage { steps: steps };
    }
}

pub struct IRPrinter {
    indent: i32,
}
impl IRPrinter {
    pub fn print_indent(&self) {
        for i in 0..self.indent {
            print!(" ");
        }
    }
    pub fn inc_indent(&mut self) {
        self.indent += 1;
    }
    pub fn dec_indent(&mut self) {
        self.indent -= 1;
    }
}
trait IRVisitor {
    fn visit(&self,  p: &IRPrinter);
}

impl IRVisitor for Pipeline {
    fn visit(&self,  p: &IRPrinter) {
        p.print_indent();
        println!("Pipeline{{");
        let mp=&mut p;
        // mp.inc_indent();
        // self.indent.visit(p);
        // mp.dec_indent();
        p.print_indent();
        print!("}}\n");
    }
}

// impl IRVisitor for Stage {
//     fn visit(&self, &mut p: IRPrinter) {
//         p.print_indent();
//         println!("Stage{{");
//         p.inc_indent();
//         // print!("{}", self.agent);
//         print!("\n");
//         p.dec_indent();
//         p.print_indent();
//         print!("}}\n");
//     }
// }

fn main() {
    let e = Pipeline::make("hahaha".to_string());
    let e2 = Stage::make("hahaha".to_string());
    let p = IRPrinter { indent: 0 };
    // e.visit(p);
    // e2.visit(&p);
    // p.visit(e);
    // println!("{}", e.node.agent);
}

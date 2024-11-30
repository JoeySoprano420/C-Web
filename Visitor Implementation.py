class CWebVisitor(ParseTreeVisitor):
    def __init__(self, llvm_context, builder):
        self.context = llvm_context
        self.builder = builder
        self.module = ir.Module(name="cweb_module")

    def visitFunction(self, ctx):
        func_name = ctx.ID().getText()
        params = self.visit(ctx.parameterList()) if ctx.parameterList() else []
        ret_type = self.visit(ctx.returnType())

        # Define LLVM function signature
        llvm_func_type = ir.FunctionType(ret_type, params)
        llvm_func = ir.Function(self.module, llvm_func_type, name=func_name)

        # Build function body
        block = llvm_func.append_basic_block(name="entry")
        self.builder.position_at_end(block)

        for statement in ctx.statement():
            self.visit(statement)

        return llvm_func

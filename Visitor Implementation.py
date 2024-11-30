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

from llvmlite import ir

class CWebVisitor(ParseTreeVisitor):
    def __init__(self):
        self.module = ir.Module(name="cweb_module")
        self.builder = None
        self.function_scope = {}

    def visitProgram(self, ctx):
        for child in ctx.children:
            self.visit(child)

    def visitFunction(self, ctx):
        func_name = ctx.ID().getText()
        return_type = self.visit(ctx.returnType())
        param_types = [self.visit(p.type()) for p in ctx.parameterList().parameter()]
        param_names = [p.ID().getText() for p in ctx.parameterList().parameter()]

        # Define LLVM function
        llvm_func_type = ir.FunctionType(return_type, param_types)
        llvm_func = ir.Function(self.module, llvm_func_type, name=func_name)

        # Add parameters to the function scope
        block = llvm_func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        for i, param in enumerate(llvm_func.args):
            param.name = param_names[i]
            alloca = self.builder.alloca(param.type, name=param.name)
            self.builder.store(param, alloca)
            self.function_scope[param.name] = alloca

        # Visit function body
        for statement in ctx.statement():
            self.visit(statement)

        return llvm_func

    def visitReturnStatement(self, ctx):
        return_value = self.visit(ctx.expression())
        self.builder.ret(return_value)

    def visitVariableDeclaration(self, ctx):
        var_name = ctx.ID().getText()
        var_type = self.visit(ctx.type())
        alloca = self.builder.alloca(var_type, name=var_name)

        if ctx.expression():
            value = self.visit(ctx.expression())
            self.builder.store(value, alloca)

        self.function_scope[var_name] = alloca

    def visitExpression(self, ctx):
        if ctx.NUM():
            return ir.Constant(ir.IntType(32), int(ctx.NUM().getText()))
        elif ctx.ID():
            var_name = ctx.ID().getText()
            alloca = self.function_scope[var_name]
            return self.builder.load(alloca, name=var_name)
        elif ctx.PLUS():
            left = self.visit(ctx.expression(0))
            right = self.visit(ctx.expression(1))
            return self.builder.add(left, right, name="addtmp")
        # Add support for other operators as needed

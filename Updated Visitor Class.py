class CWebVisitor(ParseTreeVisitor):
    def __init__(self):
        self.module = ir.Module(name="cweb_module")
        self.builder = None
        self.function_scope = {}

    def visitProgram(self, ctx):
        for child in ctx.children:
            self.visit(child)

    def visitFunction(self, ctx):
        # Function definition logic (same as above)
        pass

    def visitLoop(self, ctx):
        loop_condition = self.visit(ctx.condition())
        loop_block = self.builder.append_basic_block("loop")
        after_loop = self.builder.append_basic_block("afterloop")

        self.builder.cbranch(loop_condition, loop_block, after_loop)
        self.builder.position_at_end(loop_block)

        for statement in ctx.statement():
            self.visit(statement)

        self.builder.branch(loop_block)  # Loop back
        self.builder.position_at_end(after_loop)

    def visitCondition(self, ctx):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        return self.builder.icmp_signed("==", left, right, "condtmp")

    def visitExpression(self, ctx):
        # Handle numbers, variables, and basic math as before
        pass

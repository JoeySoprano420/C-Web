from neo4j import GraphDatabase

class CWebVisitor(ParseTreeVisitor):
    def __init__(self, uri, user, password):
        super().__init__()
        self.neo4j_driver = GraphDatabase.driver(uri, auth=(user, password))

    def create_node(self, label, properties):
        with self.neo4j_driver.session() as session:
            session.run(
                f"CREATE (n:{label} $props) RETURN n",
                props=properties
            )

    def create_relationship(self, start, end, rel_type):
        with self.neo4j_driver.session() as session:
            session.run(
                """
                MATCH (a {name: $start}), (b {name: $end})
                CREATE (a)-[:{rel_type}]->(b)
                """,
                start=start,
                end=end,
                rel_type=rel_type
            )

    def visitFunction(self, ctx):
        func_name = ctx.ID().getText()
        self.create_node("Function", {"name": func_name})
        for param in ctx.params:
            self.create_relationship(func_name, param, "USES")

from py2neo import Graph, Node, Relationship

class Neo4jSchema:
    def __init__(self, uri, user, password):
        self.graph = Graph(uri, auth=(user, password))

    def create_function(self, name, return_type):
        function_node = Node("Function", name=name, returnType=return_type)
        self.graph.create(function_node)

    def create_variable(self, name, var_type):
        variable_node = Node("Variable", name=name, type=var_type)
        self.graph.create(variable_node)

    def create_relationship(self, from_node, to_node, rel_type):
        relationship = Relationship(from_node, rel_type, to_node)
        self.graph.create(relationship)

    def fetch_function(self, name):
        return self.graph.nodes.match("Function", name=name).first()

    def fetch_variable(self, name):
        return self.graph.nodes.match("Variable", name=name).first()

# Usage
schema = Neo4jSchema(uri="bolt://localhost:7687", user="neo4j", password="password")
schema.create_function("add", "int")
schema.create_variable("a", "int")
schema.create_variable("b", "int")

add_function = schema.fetch_function("add")
variable_a = schema.fetch_variable("a")

schema.create_relationship(add_function, variable_a, "USES")

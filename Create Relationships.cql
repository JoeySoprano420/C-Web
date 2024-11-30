MATCH (f:Function {name: "add"}), (v:Variable {name: "a"})
CREATE (f)-[:CONTAINS]->(v);

MATCH (f:Function {name: "add"}), (v:Variable {name: "c"})
CREATE (f)-[:USES]->(v);

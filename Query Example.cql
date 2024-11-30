MATCH (f:Function {name: "add"})-[:USES]->(v:Variable)
RETURN v;

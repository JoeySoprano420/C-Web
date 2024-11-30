import React, { useState } from "react";
import MonacoEditor from "react-monaco-editor";
import CytoscapeComponent from "react-cytoscapejs";

const VPE = () => {
    const [code, setCode] = useState("// Write your code here...");
    const [elements, setElements] = useState([]);

    const updateGraph = () => {
        // Mock data from Neo4j (replace with API call)
        setElements([
            { data: { id: "func_add", label: "Function: add" } },
            { data: { id: "var_a", label: "Variable: a" } },
            { data: { source: "func_add", target: "var_a", label: "USES" } },
        ]);
    };

    return (
        <div style={{ display: "flex", height: "100vh" }}>
            {/* Code Editor */}
            <div style={{ flex: 1 }}>
                <MonacoEditor
                    width="100%"
                    height="100%"
                    language="c-web"
                    theme="vs-dark"
                    value={code}
                    onChange={setCode}
                />
                <button onClick={updateGraph}>Compile & Visualize</button>
            </div>

            {/* Graph Visualization */}
            <div style={{ flex: 1 }}>
                <CytoscapeComponent
                    elements={elements}
                    style={{ width: "100%", height: "100%" }}
                    layout={{ name: "grid" }}
                />
            </div>
        </div>
    );
};

export default VPE;

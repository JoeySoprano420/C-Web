const updateGraph = async () => {
    try {
        const response = await fetch("http://localhost:5000/parse", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code }),
        });

        const data = await response.json();
        console.log(data.llvm_ir); // Display LLVM IR in the console
        setElements([
            { data: { id: "func_add", label: "Function: add" } },
            { data: { id: "var_a", label: "Variable: a" } },
            { data: { source: "func_add", target: "var_a", label: "USES" } },
        ]);
    } catch (error) {
        console.error("Error parsing code:", error);
    }
};

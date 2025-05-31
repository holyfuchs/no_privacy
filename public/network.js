let networkChart = null;

function destroyNetworkGraph() {
    if (networkChart) {
        networkChart.destroy();
    }
    document.getElementById("networkChart").innerHTML = "";
}

async function createNetworkGraph(chart, address) {
    var nodes = [
        { id: 0, label: "Myriel", group: 1 },
        { id: 1, label: "Napoleon", group: 1 },
        { id: 2, label: "Mlle.Baptistine", group: 1 },
    ];
    var edges = [
        { from: 1, to: 0, length: 100 },
        { from: 2, to: 0 }
    ];
    
    var container = document.getElementById("networkChart");
    var data = {
        nodes: nodes,
        edges: edges,
    };
    var options = {
        nodes: {
            shape: "dot",
            size: 16,
        },
        physics: {
            forceAtlas2Based: {
                gravitationalConstant: -26,
                centralGravity: 0.005,
                springLength: 230,
                springConstant: 0.18,
            },
            maxVelocity: 146,
            solver: "forceAtlas2Based",
            timestep: 0.35,
            stabilization: { iterations: 150 },
        },
    };
    networkChart = new vis.Network(container, data, options);
}
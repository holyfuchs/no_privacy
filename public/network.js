let networkChart = null;

function destroyNetworkGraph() {
    if (networkChart) {
        networkChart.destroy();
    }
    document.getElementById("networkChart").innerHTML = "";
}

async function createNetworkGraph(chart, address) {
    var nodes = [
        { id: 0, label: "Myriel\nasd", group: 1, size: 20 },
        { id: 1, label: "Napoleon", group: 2, size: 10 },
        { id: 2, label: "Mlle.Baptistine", group: 2, size: 10 },
    ];
    var edges = [
        { from: 1, to: 0, length: 100, width: 1 },
        { from: 2, to: 0, length: 10, width: 10 }
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
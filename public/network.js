let networkChart = null;

function destroyNetworkGraph() {
    if (networkChart) {
        networkChart.destroy();
    }
    document.getElementById("networkChart").innerHTML = "";
    document.getElementById("networkInfo").innerHTML = "";
}

async function createNetworkGraph(address) {
    const response = await fetch(`/api/graph/${address}`);
    const data = await response.json();
    var container = document.getElementById("networkChart");
    
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

    var info = document.getElementById("networkInfo");
    
    let htmlContent = "<h2>Network Info</h2>";    
    const sortedEdges = [...data.edges].sort((a, b) => b.width - a.width);
    
    // Create table for edge information
    htmlContent += "<h3>Edge Information</h3>";
    htmlContent += "<table style='border-collapse: collapse; width: 100%; margin-top: 20px;'>";
    htmlContent += "<thead><tr style='background-color: #f2f2f2;'>";
    htmlContent += "<th style='padding: 12px; text-align: left; border: 1px solid #ddd;'>Strength</th>";
    htmlContent += "<th style='padding: 12px; text-align: left; border: 1px solid #ddd;'>Label</th>";
    htmlContent += "<th style='padding: 12px; text-align: left; border: 1px solid #ddd;'>Address</th>";
    htmlContent += "</tr></thead><tbody>";
    
    sortedEdges.forEach(edge => {
        const fromNode = data.nodes.find(node => node.id === edge.from);
        const toNode = data.nodes.find(node => node.id === edge.to);
        htmlContent += `<tr style='border: 1px solid #ddd;'>
            <td style='padding: 12px; border: 1px solid #ddd;'>${edge.width}</td>
            <td style='padding: 12px; border: 1px solid #ddd;'>${toNode.label}</td>
            <td style='padding: 12px; border: 1px solid #ddd;'><a href="?address=${toNode.address}">${toNode.address}</a></td>
        </tr>`;
    });
    
    htmlContent += "</tbody></table>";
    
    info.innerHTML = htmlContent;
}
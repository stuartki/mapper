
var width = 1000,
    height = 1000,
    svg = d3.select('#graph')
        .append('svg')
        .attrs({width: width,
               height: height});
topic = prompt('topic: ')



d3.json(topic + '.json', function (data) {
    var node_id = helpers.node_id(data, function (d) { return d.title; }),
        uniques = node_id.domain();
        // matrix = helpers.connection_matrix(data);

    var nodes = uniques.map(function (node) {
        return {node: node};
    });

    var links = []
    
    data.forEach(function (d) {
        
        d.past.forEach(function (e) {
            if (typeof e === "number") {

            links.push({
                    source: node_id(data[e-1].title),
                    target: node_id(d.title),
                    count: 1
                }
            );}
        });
    });

    // console.log(nodes)
    // console.log(links)


    var simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links))
            .force("center", d3.forceCenter(width/2, height/2));
            // .force('centerX', d3.forceX(width / 2))
            // .force('centerY', d3.forceY(height / 2));

    nodes.forEach(function(d) {      
            d["weight"] = links.filter(function(l) {
                return l.source.index == d.index || l.target.index == d.index
            }).length;
        });

    var weight = d3.scaleLinear()
            .domain(d3.extent(nodes.map(function (d) { return d.weight; })))
            .range([5, 20]),
        distance = d3.scaleLinear()
            .domain(d3.extent(data.map(function(d) { return d.count;})))
            .range([300, 100]),
        given = d3.scaleLinear()
            .range([1000, 3500]);



    simulation.force("link").distance(function (d) {
            return 300;
        });

    var link = svg.selectAll("line")
            .data(links)
            .enter()
            .append("line")
            .classed('link', true);

    var node = svg.selectAll("circle")
            .data(nodes)
            .enter()
            .append("circle")

            .attrs({r: function(d) {return weight(d['weight']);},
                    fill: function (d) { return helpers.color(d.index); }, 
                    class: function (d) { return d.node; }})
            .classed('node', true)
            // .on('mouseover', function (d) {
            //     highlight(d, uniques, given, matrix, node_id);
            // })
            // .on('mouseout', function (d) {
            //     dehighlight(d, weight);
            // });

    node.call(helpers.tooltip(function (d) {return d.node; }));
    node.call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));  
    simulation.on("tick", function() {
        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });
        
        node.attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
    });

    function dragstarted(d) {
            if (!d3.event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }
        
        function dragged(d) {
            d.fx = d3.event.x;
            d.fy = d3.event.y;
        }
        
        function dragended(d) {
            if (!d3.event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        } 
    ;

    // function highlight (d, uniques, given, matrix, node_id) {
    //     var values = Object.keys(didi[0]).map(function(key){return didi[0][key];});

    //     given.domain(d3.extent(values));

    //     uniques.map(function (nick) {
    //         var count = didi[0][nick];


    //         if (nick != d.nick) {
    //             d3.selectAll('circle.nick_'+nick_id(nick))
    //                 .transition()
    //                 .attr('r', given(count));
    //         }
    //     });
    // }
});

// function dehighlight (d, weight) {
//     d3.selectAll('.node')
//         .transition()
//         .attr('r', function (d) { return weight(d.weight); });
// }


// Get the id from the html
const svg = d3.select("#viz")
  .append("svg")
  .attr("width", 600)
  .attr("height", 400);

d3.csv("/data/120_day.csv")
  .then(function(data) {
    
    // Updating the type for the CSV file
    data.forEach(function(d) {
        d.Date = new Date(d.Date);
        d["^GSPC"] = +d["^GSPC"];
    });

    // Create scales
    const xScale = d3.scaleTime()
        .domain(d3.extent(data, d => d.Date))
        .range([0, 600]);
    
    const yScale = d3.scaleLinear()
        .domain([0, d3.max(data, d => d["^GSPC"])])
        .range([400, 0]);

    // Create line
    const lineGraph = d3.line()
        .x(d => xScale(d.Date))
        .y(d => yScale(d["^GSPC"]));

    svg.append("path")
        .datum(data)
        .attr("d", lineGraph)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 2);

})
.catch(function(error) {
    // Handle any errors
    console.log(error);
});


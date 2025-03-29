// Define image position constants

const zoomSize = 3;

// Margin is our "inner frame"
const margin = { 
    top: 20 * zoomSize,
    right: 20 * zoomSize, 
    bottom: 30 * zoomSize, // A larger bottom accounts for more room for labels
    left: 40 * zoomSize, // A larger left accounts for more room for labels
}

 // Adjust chart width and height based on outer margins
const width = (200 * zoomSize) - margin.left - margin.right;
const height = (400 * zoomSize) - margin.top - margin.bottom;

// Get the id from the html
const svg = d3.select("#viz")
  .append("svg")

  // Add back margin's to width and height to get "full picture" size
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.botoom )

  // Groups all elements together
  .append("g") 

  // Adjust graph space to leave room for labels
  .attr("transform", `translate(${margin.left}, ${margin.top})`);

d3.csv("./data/120_day.csv")
  .then(function(data) {
    
    // Updating the type for the CSV file
    data.forEach(function(d) {
        d.Date = new Date(d.Date);
        d["^GSPC"] = +d["^GSPC"];
    });

    // Create Scales for x and y features
    const xScale = d3.scaleTime()
        .domain(d3.extent(data, d => d.Date))
        .range([0, width]);
    
    const yScale = d3.scaleLinear()
        .domain([0, d3.max(data, d => d["^GSPC"])])
        .range([height, 0]);

    // Create Labels for x and y features
    const xAxis = d3.axisBottom(xScale)

        // Adds a label to our x-axis every month
        .ticks(d3.timeMonth.every(1))

        // Formats the months as ("Jan", "Feb", "Mar" , ...)
        .tickFormat(date => {
            return d3.timeFormat("%b")(date); 
        })
    
    const yAxis = d3.axisLeft(yScale);

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


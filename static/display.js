/**
 * display.js
 * 
 * Responsible for creating a visualization in the form of a line graph
 * based on csv data in the data directory
 * 
 * @Brycekratzer
 */


/**
 * Creating "graph frame" constants for setting up layout
 */
const zoomSize = 3;

// Margin is our "inner frame"
const margin = { 
    top: 20 * zoomSize,
    right: 20 * zoomSize, 
    bottom: 20 * zoomSize, // A larger bottom accounts for more room for labels
    left: 25 * zoomSize, // A larger left accounts for more room for labels
}

 // Adjust chart width and height based on outer margins
const width = (150 * zoomSize) - margin.left - margin.right;
const height = (150 * zoomSize) - margin.top - margin.bottom;

/**
 * Creating SVG for each HTML element / csv file
 * 
 * Add HTML element to index.html before initializing svg constant
 */

// Graph for S&P 500 120 Day 
const svg500_120 = d3.select("#viz1")
  .append("svg")

  // Add back margin's to width and height to get "full picture" size
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom )

  // Groups all elements together
  .append("g") 

  // Adjust graph space to leave room for labels
  .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Graph for S&P 500 50 Day 
const svg500_50 = d3.select("#viz2")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom )
    .append("g") 
    .attr("transform", `translate(${margin.left}, ${margin.top})`);


/**
 * Function for creating each graph based on data and configurations
 * 
 * @param {dictionary} config - Represents the configurations of how the graph will look
 * @param data - Represents the actual data being graphed
 * @param svg - Represents the SVG constant we defined earlier
 */

function createViz(svg, data, config){

    // Updating the type for the CSV file
    data.forEach(function(d) {
        d.Date = new Date(d.Date);
        d[config.key] = +d[config.key];
    });

    // Create Scales for x and y features
    const xScale = d3.scaleTime()
        .domain(d3.extent(data, d => d.Date))
        .range([0, width]);
    
    const yScale = d3.scaleLinear()
        // Responsable for scaling graph Y axis based on the minimum value and maximum value of the 
        // data set
        .domain([
            d3.min(data, d => d[config.key]), 
            d3.max(data, d => d[config.key]
        )])
        .range([height,0]);

    // Create Labels for x and y features
    const xAxis = d3.axisBottom(xScale)
        // Adds a label to our x-axis every month
        .ticks(d3.timeMonth.every(1))
        // Formats the months as ("Jan", "Feb", "Mar" , ...)
        .tickFormat(date => {
            return d3.timeFormat("%b")(date); 
        })

    const yAxis = d3.axisLeft(yScale)
        .ticks(4);

    // Add x and y labels to our grouping of elements "g"
    svg.append("g")
        // Adds HTML classifier for styling
        .attr("class", "x-axis") 
        // Adjust label position
        .attr("transform", `translate(0, ${height})`)
        // Adds xAxis labels based on the variables adjustments
        .call(xAxis);

    svg.append("g")
        .attr("class", "y-axis")
        .call(yAxis);

    // Add Name for Axis's
    svg.append("text")
        .attr("class", "x-name")
        // Puts text relative to the middle of x-axis
        .attr("text-anchor", "middle")
        // Calculations for position of name
        .attr("x", width/2)
        .attr("y", height + margin.bottom - 20)
        .text("Date");
    
    svg.append("text")
        .attr("class", "y-name")
        .attr("text-anchor", "middle")

        // Rotates text to be of vertical view
        .attr("transform", "rotate(-90)")

        // Position of text
        .attr("y", -margin.left + 25)
        .attr("x", -(height/2))
        .text(config.yAxisLabel);

    // Create line
    const lineGraph = d3.line()
        .x(d => xScale(d.Date))
        .y(d => yScale(d[config.key]));

    svg.append("path")
        .datum(data)
        .attr("d", lineGraph)
        // .attr("stroke", config.color)
        .attr("stroke-width", 2);
}

/**
 * Initializes each graph by loading a CSV file then calling the createViz function to 
 * create a graph based on the configurations passed
 */

d3.csv("./data/120_day.csv")
  .then(function(data) {

    createViz(svg500_120, data, {

        // The key is the name of our feature we are observing over time
        key: "^GSPC",

        // Name of axis
        yAxisLabel: "S&P 500 Value",

        // Color of line
        color: "steelblue",
    });
}).catch(function(error) {
    // Handle any errors
    console.log(error);
});

d3.csv("./data/50_day.csv")
  .then(function(data) {

    createViz(svg500_50, data, {

        // The key is the name of our feature we are observing over time
        key: "^GSPC",

        // Name of axis
        yAxisLabel: "S&P 500 Value",

        // Color of line
        color: "steelblue",
    });
}).catch(function(error) {
    // Handle any errors
    console.log(error);
});



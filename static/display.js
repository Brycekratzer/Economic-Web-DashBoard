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
const zoomSize = 2;

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

// Graph for Treasury Yield Spread
const svgT10Y2Y = d3.select("#viz3")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom )
    .append("g") 
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Graph for Treasury-Fed Funds Spread
const svgT10YFF = d3.select("#viz4")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom )
    .append("g") 
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Graph for Interest Rates
const svgInterestRates = d3.select("#viz5")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom )
    .append("g") 
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Graph for Mortgage Rates
const svgMortgageRates = d3.select("#viz6")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom )
    .append("g") 
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Graph for Mortgage Rates
const svgInitialClaims = d3.select("#viz7")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom )
    .append("g") 
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Graph for Retail Sales
const svgRetailSales = d3.select("#viz8")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom )
    .append("g") 
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Graph for Unemployment Rate
const svgUnRate = d3.select("#viz9")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom )
    .append("g") 
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Graph for Construction Job Listing
const svgConstRate = d3.select("#viz10")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom )
    .append("g") 
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Graph for CPI
const svgCPI = d3.select("#viz11")
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
        .ticks(d3.timeMonth.every(2))
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
        .attr("y", height + margin.bottom - 5)
        .text("Date");
    
    svg.append("text")
        .attr("class", "y-name")
        .attr("text-anchor", "middle")

        // Rotates text to be of vertical view
        .attr("transform", "rotate(-90)")

        // Position of text
        .attr("y", -margin.left + 10)
        .attr("x", -(height/2))
        .text(config.yAxisLabel);

    // Create line
    const lineGraph = d3.line()
        .x(d => xScale(d.Date))
        .y(d => yScale(d[config.key]));

    svg.append("path")
        .datum(data)
        .attr("d", lineGraph)
        .attr("stroke-width", 2);
}

/**
 * Initializes each graph by loading a CSV file then calling the createViz function to 
 * create a graph based on the configurations passed
 */

d3.csv("./data/SP120_day.csv")
  .then(function(data) {

    createViz(svg500_120, data, {

        // The key is the name of our feature we are observing over time
        key: "Moment",

        // Name of axis
        yAxisLabel: "S&P 500 Momentum",
    });
}).catch(function(error) {
    // Handle any errors
    console.log(error);
});

d3.csv("./data/SP50_day.csv")
  .then(function(data) {

    createViz(svg500_50, data, {

        // The key is the name of our feature we are observing over time
        key: "Moment",

        // Name of axis
        yAxisLabel: "S&P 500 Momentum",
    });
}).catch(function(error) {
    // Handle any errors
    console.log(error);
});

d3.csv("./data/T10Y2Y_data.csv")
  .then(function(data) {

    createViz(svgT10Y2Y, data, {
        key: "T10Y2Y",
        yAxisLabel: "Yield Spread Indicator",
    });
}).catch(function(error) {
    console.log(error);
});

d3.csv("./data/T10YFF_data.csv")
  .then(function(data) {

    createViz(svgT10YFF, data, {
        key: "T10YFF",
        yAxisLabel: "Yield Spread Indicator",
    });
}).catch(function(error) {
    // Handle any errors
    console.log(error);
});

d3.csv("./data/interest_rate_data.csv")
  .then(function(data) {

    createViz(svgInterestRates, data, {
        key: "DFF",
        yAxisLabel: "Fed Funds Spread Indicator",
    });
}).catch(function(error) {
    // Handle any errors
    console.log(error);
});

d3.csv("./data/mortgage_rate_data.csv")
  .then(function(data) {
    createViz(svgMortgageRates, data, {
        key: "MORTGAGE30US",
        yAxisLabel: "Mortgage Rate Indicator",
    });
}).catch(function(error) {
    // Handle any errors
    console.log(error);
});

d3.csv("./data/initial_claims_data.csv")
  .then(function(data) {
    createViz(svgInitialClaims, data, {
        key: "ICSA",
        yAxisLabel: "",
    });
}).catch(function(error) {
    // Handle any errors
    console.log(error);
});

d3.csv("./data/retail_sales_data.csv")
  .then(function(data) {
    createViz(svgRetailSales, data, {
        key: "RSAFS",
        yAxisLabel: "Retail Sales",
    });
}).catch(function(error) {
    // Handle any errors
    console.log(error);
});

d3.csv("./data/unemployment_data.csv")
  .then(function(data) {
    createViz(svgUnRate, data, {
        key: "UNRATE",
        yAxisLabel: "Unemployment Rate",
    });
}).catch(function(error) {
    // Handle any errors
    console.log(error);
});

d3.csv("./data/construction_jobs_data.csv")
  .then(function(data) {
    createViz(svgConstRate, data, {
        key: "JTS2300JOL",
        yAxisLabel: "Unemployment Rate",
    });
}).catch(function(error) {
    // Handle any errors
    console.log(error);
});

d3.csv("./data/cpi_data.csv")
  .then(function(data) {
    createViz(svgCPI, data, {
        key: "CPIAUCSL",
        yAxisLabel: "CPI",
    });
}).catch(function(error) {
    // Handle any errors
    console.log(error);
});


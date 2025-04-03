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

// Graph for S&P Prediction
const svgSPprediction = d3.select("#viz12")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom )
    .append("g") 
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Graph for Dow Jones Prediction
const svgDJprediction = d3.select("#viz13")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom )
    .append("g") 
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

/**
 * The tooltip div that appears when hovering over data points
 */
const tooltip = d3.select("body").append("div")
  .attr("class", "tooltip")
  .style("opacity", 0)
  .style("position", "absolute")
  .style("background-color", "white")
  .style("border", "1px solid #ddd")
  .style("border-radius", "3px")
  .style("padding", "8px")
  .style("pointer-events", "none")
  .style("font-size", "12px")
  .style("box-shadow", "0px 0px 6px rgba(0,0,0,0.15)");



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

    svg.selectAll(".hover-point")
        .data(data)
        .enter().append("circle")
        .attr("class", "hover-point")
        .attr("cx", d => xScale(d.Date))
        .attr("cy", d => yScale(d[config.key]))
        .attr("r", 20)
        .style("opacity", 0) // Make them invisible
        .style("cursor", "pointer")
        .on("mouseover", function(event, d) {
            // Format date for display
            const formattedDate = d3.timeFormat("%b %d, %Y")(d.Date);
            // Format value based on data type
            const formattedValue = d[config.key].toFixed(2);
            
            // Show tooltip
            tooltip.transition()
                .duration(0)
                .style("opacity", 0.9);
            tooltip.html(`<strong>Date:</strong> ${formattedDate}<br><strong>${config.yAxisLabel}:</strong> ${formattedValue}`)
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 28) + "px");
        })
        .on("mouseout", function() {
            // Hide tooltip
            tooltip.transition()
                .duration(0)
                .style("opacity", 0);
        });
}   

/**
 * This function creates a combined visualization of actual and predicted stock data
 * @param {d3.Selection} svg - The SVG element to draw the visualization in
 * @param {Array} actualData - Historical stock data
 * @param {Array} predictionData - Predicted stock data
 * @param {Object} config - Configuration object for the visualization
 */
function createCombinedStockViz(svg, actualData, predictionData, config){

    // Actual Data to show
    actualData.forEach(function(d) {
        d.Date = new Date(d.Date);
        d[config.key] = +d[config.key];
    });

    // Prediction Data to show
    predictionData.forEach(function(d) {
        d.Date = new Date(d.Date);
        d[config.key] = +d[config.key];
    });

    // Combining Data for domain calculations
    const allData = actualData.concat(predictionData);

    // Create scales for x and y feats
    const xScale = d3.scaleTime()
        .domain(d3.extent(allData, d => d.Date))
        .range([0, width]);

    const yScale = d3.scaleLinear()
        .domain([
            d3.min(allData, d => d[config.key]),
            d3.max(allData, d => d[config.key])
        ])
        .range([height, 0]);

    // Create labels for x and y features
    const xAxis = d3.axisBottom(xScale)
        .ticks(d3.timeMonth.every(2))
        .tickFormat(date => {
            return d3.timeFormat("%b")(date); 
        });

    const yAxis = d3.axisLeft(yScale)
        .ticks(4);
    // Add x and y labels
    svg.append("g")
        .attr("class", "x-axis")
        .attr("transform", `translate(0, ${height})`)
        .call(xAxis);

    svg.append("g")
        .attr("class", "y-axis")
        .call(yAxis);

    // Add axis labels
    svg.append("text")
        .attr("class", "x-name")
        .attr("text-anchor", "middle")
        .attr("x", width/2)
        .attr("y", height + margin.bottom - 5)
        .text("Date");
    
    svg.append("text")
        .attr("class", "y-name")
        .attr("text-anchor", "middle")
        .attr("transform", "rotate(-90)")
        .attr("y", -margin.left + 8)
        .attr("x", -(height/2))
        .text(config.yAxisLabel);

    // Create line generators
    const createLine = d3.line()
        .x(d => xScale(d.Date))
        .y(d => yScale(d[config.key]));

    // Draw historical data line with solid style
    svg.append("path")
        .datum(actualData)
        .attr("d", createLine)
        .attr("stroke", config.color || "var(--mission-blue)")
        .attr("stroke-width", 2)
        .attr("fill", "none");
    
    // Draw prediction line with dashed style
    svg.append("path")
        .datum(predictionData)
        .attr("d", createLine)
        .attr("stroke", config.predictionColor || "var(--mission-blue)")
        .attr("stroke-width", 2)
        .attr("stroke-dasharray", "5,5")
        .attr("fill", "none");


    // This adds a connecting line from end of the actual values to the 
    // Start of the predicited values
    if (actualData.length > 0 && predictionData.length > 0) {
            // Get the last point of actual data and first point of prediction data
            const lastActualPoint = actualData[actualData.length - 1];
            const firstPredictionPoint = predictionData[0];
            
            // Create a connector path with just these two points
            const connectorData = [lastActualPoint, firstPredictionPoint];
            
            // Draw the connector line with dotted style
            svg.append("path")
                .datum(connectorData)
                .attr("d", createLine)
                .attr("stroke", config.predictionColor || "var(--mission-blue)")
                .attr("stroke-width", 2)
                .attr("stroke-dasharray", "5,5")
                .attr("fill", "none");
    }


    // Adds mini display of value when user hovers over graph line
    svg.selectAll(".hover-point")
        .data(allData)
        .enter().append("circle")
        .attr("class", "hover-point")
        .attr("cx", d => xScale(d.Date))
        .attr("cy", d => yScale(d[config.key]))
        .attr("r", 15)
        .style("opacity", 0) // Make them invisible
        .style("cursor", "pointer")
        .on("mouseover touchstart", function(event, d) {
            // Format date for display
            const formattedDate = d3.timeFormat("%b, %Y")(d.Date);
            // Format value based on data type
            const formattedValue = d[config.key].toFixed(2);
            
            // Show tooltip
            tooltip.transition()
                .duration(0)
                .style("opacity", 0.9);
            tooltip.html(`<strong>Date:</strong> ${formattedDate}<br><strong>${config.yAxisLabel}:</strong> ${formattedValue}`)
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 28) + "px");
        })
        .on("mouseout touchend touchcancel", function() {
            // Hide tooltip
            tooltip.transition()
                .duration(250)
                .style("opacity", 0);
        });


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
        yAxisLabel: "Fed Funds Spread Indicator",
    });
}).catch(function(error) {
    // Handle any errors
    console.log(error);
});

d3.csv("./data/interest_rate_data.csv")
  .then(function(data) {

    createViz(svgInterestRates, data, {
        key: "DFF",
        yAxisLabel: "Interest Rates",
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

// Display stock data
Promise.all([
    d3.csv("./data/pre_prediction_stocks.csv"),
    d3.csv("./data/prediction_stocks.csv")
]).then(function(data) {
    const actualDataSP = data[0];
    const predictionDataSP = data[1];

    createCombinedStockViz(svgSPprediction, actualDataSP, predictionDataSP, {
        key: "^GSPC Close",
        yAxisLabel: "S&P 500 Value"
    });

    const actualDataDJ = data[0];
    const predictionDataDJ = data[1]; 
    createCombinedStockViz(svgDJprediction, actualDataDJ, predictionDataDJ, {
        key: "^DJI Close",
        yAxisLabel: "Dow Jones Value"
    });


}).catch(function(error) {
    console.log("Error loading S&P prediction data:", error);
});


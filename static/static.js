// Function to load and parse the CSV file
function updateDateFromCSV() {
    fetch('./data/model_projections/pre_prediction_stocks.csv')
      .then(response => response.text())
      .then(csvData => {
        // Split the CSV into rows
        const rows = csvData.trim().split('\n');
        
        // Get the last row (most recent data)
        const lastRow = rows[rows.length - 1];
        
        // Split the row into columns
        const columns = lastRow.split(',');
        
        // Get the date (assuming it's the first column)
        const latestDate = columns[1];
        
        // Update the HTML element with the date
        document.querySelector('.date-label').textContent = latestDate;
      })
      .catch(error => {
        console.error('Error loading the CSV file:', error);
        document.querySelector('.date-label').textContent = 'Error loading date';
      });
  }
  
  // Call the function when the page loads
  document.addEventListener('DOMContentLoaded', updateDateFromCSV);
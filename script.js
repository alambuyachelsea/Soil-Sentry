document.addEventListener('DOMContentLoaded', function () {
  // Function to fetch plant data from server and render plant sections
  function fetchAndRenderPlants() {
      fetch('/plants')
          .then(response => response.json())
          .then(data => {
              const plantsContainer = document.querySelector('.plants');
              plantsContainer.innerHTML = ''; // Clear existing content

              // Iterate over each plant data
              data.forEach(plant => {
                  // Create plant section element
                  const plantSection = document.createElement('div');
                  plantSection.classList.add('plant-section');

                  // Create and append name row
                  const nameRow = document.createElement('div');
                  nameRow.classList.add('row', 'row1');
                  nameRow.textContent = plant.name;
                  plantSection.appendChild(nameRow);

                  // Create and append GIF row
                  const gifRow = document.createElement('div');
                  gifRow.classList.add('row', 'row2');
                  const plantGif = document.createElement('img');
                  plantGif.classList.add('plant-gif', 'plant');
                  plantGif.src = plant.img_source; 
                  plantGif.alt = plant.name + 'alt';
                  gifRow.appendChild(plantGif);
                  plantSection.appendChild(gifRow);

                  // Create and append water needs row
                  const waterNeedsRow = document.createElement('div');
                  waterNeedsRow.classList.add('row', 'row3');
                  waterNeedsRow.textContent = `Water Needs: ${plant.water_needs}`;
                  plantSection.appendChild(waterNeedsRow);

                  // Create and append current water level row
                  const currentWaterLevelRow = document.createElement('div');
                  currentWaterLevelRow.classList.add('row', 'row4');
                  currentWaterLevelRow.textContent = `Current Water Level: ${plant.current_water_level}`;
                  plantSection.appendChild(currentWaterLevelRow);

                  // Append plant section to plants container
                  plantsContainer.appendChild(plantSection);
              });
          })
          .catch(error => console.error('Error fetching plant data:', error));
  }

  // Initialize Chart.js chart
  const ctx = document.getElementById('soilMoistureChart').getContext('2d');
  const soilMoistureChart = new Chart(ctx, {
      type: 'line',
      data: {
          labels: [], // Timestamps will be added here
          datasets: [{
              label: 'Soil Moisture Level',
              data: [], // Moisture levels will be added here
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1,
              fill: false
          }]
      },
      options: {
          scales: {
              x: {
                  type: 'time',
                  time: {
                      unit: 'second'
                  }
              },
              y: {
                  beginAtZero: true,
                  max: 5
              }
          }
      }
  });

  // Function to fetch soil moisture readings and update the chart
  function fetchAndUpdateSoilMoisture() {
      fetch('/plants')
          .then(response => response.json())
          .then(data => {
              const now = new Date();

              // Assuming data for one plant, you can loop through plants if needed
              const soilMoistureLevel = data[0].current_water_level;

              // Add new data point to the chart
              soilMoistureChart.data.labels.push(now);
              soilMoistureChart.data.datasets[0].data.push(soilMoistureLevel);

              // Keep the last 10 readings
              if (soilMoistureChart.data.labels.length > 10) {
                  soilMoistureChart.data.labels.shift();
                  soilMoistureChart.data.datasets[0].data.shift();
              }

              soilMoistureChart.update();
          })
          .catch(error => console.error('Error fetching soil moisture data:', error));
  }

  // Fetch and render plants on page load
  fetchAndRenderPlants();

  // Fetch and update soil moisture readings every 10 seconds
  setInterval(fetchAndUpdateSoilMoisture, 10000);
});


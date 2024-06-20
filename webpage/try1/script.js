document.addEventListener("DOMContentLoaded", function() {
  const sensorData = {
      1: [],
      2: [],
      3: [],
      water: []
  };

  const sensorCharts = {
      1: createChart('sensor1Chart', 'Sensor 1 Moisture Level'),
      2: createChart('sensor2Chart', 'Sensor 2 Moisture Level'),
      3: createChart('sensor3Chart', 'Sensor 3 Moisture Level'),
      water: createChart('waterLevelChart', 'Water Reservoir Level')
  };

  function getMoistureLevel(sensorId) {
      // Simulate fetching soil moisture data for a specific sensor
      return Math.floor(Math.random() * 100) + 1; // Random value between 1 and 100
  }

  function updateMoistureLevel(sensorId) {
      const moistureLevelElement = document.getElementById(`moisture-level-${sensorId}`);
      const moistureLevel = getMoistureLevel(sensorId);
      moistureLevelElement.textContent = `${moistureLevel}%`;

      // Store the new reading and update the chart
      sensorData[sensorId].push(moistureLevel);
      updateChart(sensorCharts[sensorId], sensorData[sensorId]);
  }

  function updateAllMoistureLevels() {
      for (let sensorId = 1; sensorId <= 3; sensorId++) {
          updateMoistureLevel(sensorId);
      }
  }

  function updateWaterLevel() {
      const waterLevelElement = document.getElementById(`water-sensor`);
      const waterLevel = getReservoirLevel();
      waterLevelElement.textContent = `${waterLevel}%`;

      // Store the new reading and update the chart
      sensorData.water.push(waterLevel);
      updateChart(sensorCharts.water, sensorData.water);
  }

  function getReservoirLevel() {
      // Simulate fetching water level sensor data
      return Math.floor(Math.random() * 100) + 1; // Random value between 1 and 100
  }

  function createChart(canvasId, label) {
      const ctx = document.getElementById(canvasId).getContext('2d');
      return new Chart(ctx, {
          type: 'line',
          data: {
              labels: [],
              datasets: [{
                  label: label,
                  data: [],
                  borderColor: 'rgba(75, 192, 192, 1)',
                  borderWidth: 1,
                  fill: false
              }]
          },
          options: {
              scales: {
                  x: {
                      type: 'linear',
                      position: 'bottom',
                      title: {
                          display: true,
                          text: 'Time'
                      }
                  },
                  y: {
                      beginAtZero: true,
                      title: {
                          display: true,
                          text: 'Moisture Level (%)'
                      }
                  }
              }
          }
      });
  }

  function updateChart(chart, data) {
      chart.data.labels = data.map((_, index) => index + 1);
      chart.data.datasets[0].data = data;
      chart.update();
  }

  // Update moisture levels every 5 seconds
  setInterval(() => {
      updateAllMoistureLevels();
      updateWaterLevel();
  }, 5000);

  // Initial update
  updateAllMoistureLevels();
  updateWaterLevel();
});

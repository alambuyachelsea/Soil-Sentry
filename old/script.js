window.onload = function() {
  // Function to make AJAX request
  function fetchPlants() {
      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
          if (xhr.readyState == 4 && xhr.status == 200) {
              var plants = JSON.parse(xhr.responseText);
              plants.forEach(function(plant, index) {
                  var plantDiv = document.createElement('div');
                  plantDiv.className = 'plant-section';
                  plantDiv.innerHTML = `
                      <div class="row row1">${plant.name}</div>
                      <div class="row row2">
                          <img src="assets/${plant.name.toLowerCase()}_plant.gif" alt="${plant.name}" class="plant-gif plant">
                      </div>
                      <div class="row row3">Water Needs: ${plant.water_needs}</div>
                      <div class="row row4">Current Water Level: ${plant.current_water_level}</div>
                  `;
                  document.getElementById('plantContainer').appendChild(plantDiv);
              });
          }
      };
      xhr.open('GET', '/plants', true);
      xhr.send();
  }

  // Fetch plants when the page loads
  fetchPlants();

  // Function to update reservoir level (mocked example)
  function updateReservoirLevel(level) {
      document.getElementById('reservoirLevel').textContent = `Reservoir Level: ${level}%`;
  }

  // Update reservoir level periodically (mocked example)
  setInterval(function() {
      var randomLevel = Math.floor(Math.random() * 101); // Generate random level (0-100)
      updateReservoirLevel(randomLevel);
  }, 5000); // Update every 5 seconds (adjust as needed)
};

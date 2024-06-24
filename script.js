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
                    // Adjusted src to construct the image source URL based on plant name
                    plantGif.src = plant.img_source; 
                    plantGif.alt = plant.name + ' alt';
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

    // Fetch and render plants on page load
    fetchAndRenderPlants();
});

document.addEventListener('DOMContentLoaded', function () {
    function fetchAndRenderPlants() {
        fetch('/plants')
            .then(response => response.json())
            .then(data => {
                const plantsContainer = document.querySelector('.plants');
                plantsContainer.innerHTML = ''; 

                data.forEach(plant => {
                    const plantSection = document.createElement('div');
                    plantSection.classList.add('plant-section');
                    const plantId = `plant-${plant.name.replace(/\s+/g, '-')}`;
                    plantSection.id = plantId;

                    const nameRow = document.createElement('div');
                    nameRow.classList.add('row', 'row1');
                    nameRow.textContent = plant.name;
                    plantSection.appendChild(nameRow);

                    const gifRow = document.createElement('div');
                    gifRow.classList.add('row', 'row2');
                    const plantGif = document.createElement('img');
                    plantGif.classList.add('plant-gif', 'plant');
                    plantGif.src = plant.img_source;
                    plantGif.alt = plant.name + ' alt';
                    gifRow.appendChild(plantGif);
                    plantSection.appendChild(gifRow);

                    const waterNeedsRow = document.createElement('div');
                    waterNeedsRow.classList.add('row', 'row3');
                    waterNeedsRow.textContent = `Water Needs: ${plant.water_needs}`;
                    plantSection.appendChild(waterNeedsRow);

                    const currentWaterLevelRow = document.createElement('div');
                    currentWaterLevelRow.classList.add('row', 'row4');
                    const waterLevelId = `current-water-level-${plant.name.replace(/\s+/g, '-')}`;
                    currentWaterLevelRow.id = waterLevelId;
                    currentWaterLevelRow.textContent = `Current Water Level: ${plant.current_water_level}`;
                    plantSection.appendChild(currentWaterLevelRow);

                    plantsContainer.appendChild(plantSection);
                });
            })
            .catch(error => console.error('Error fetching plant data:', error));
    }

    const ctx = document.getElementById('soilMoistureChart').getContext('2d');
    const soilMoistureChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], 
            datasets: [] 
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'minute'  // Adjust the time unit to better fit longer data retention
                    }
                },
                y: {
                    beginAtZero: true,
                    max: 10
                }
            }
        }
    });

    function fetchAndUpdateSoilMoisture() {
        const maxDataPoints = 100; // Define maxDataPoints within the function scope

        fetch('/plants')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Fetched data:', data); // Log fetched data for debugging

                const now = new Date();

                if (soilMoistureChart.data.datasets.length === 0) {
                    data.forEach(plant => {
                        soilMoistureChart.data.datasets.push({
                            label: plant.name,
                            data: [],
                            borderColor: getRandomColor(),
                            borderWidth: 1,
                            fill: false
                        });
                    });
                }

                data.forEach((plant, index) => {
                    soilMoistureChart.data.datasets[index].data.push({
                        x: now,
                        y: plant.current_water_level
                    });

                    if (soilMoistureChart.data.datasets[index].data.length > maxDataPoints) {
                        soilMoistureChart.data.datasets[index].data.shift();
                    }

                    // Update current water level in the HTML
                    const currentWaterLevelElement = document.getElementById(`current-water-level-${plant.name.replace(/\s+/g, '-')}`);
                    if (currentWaterLevelElement) {
                        currentWaterLevelElement.textContent = `Current Water Level: ${plant.current_water_level}`;
                    } else {
                        console.error(`Element with ID current-water-level-${plant.name.replace(/\s+/g, '-')} not found`);
                    }
                });

                if (soilMoistureChart.data.labels.length > maxDataPoints) {
                    soilMoistureChart.data.labels.shift();
                }

                soilMoistureChart.update();
            })
            .catch(error => console.error('Error fetching soil moisture data:', error));
    }

    function fetchAndUpdateReservoirLevel() {
        fetch('/ultrasonic_reading')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                const reservoirPercentage = data.percentage;
                document.getElementById('reservoirLevel').textContent = `${reservoirPercentage}%`;

                // Update reservoir GIF based on percentage
                const reservoirImage = document.querySelector('.reservoir-image');
                if (reservoirImage) {
                    if (reservoirPercentage >= 85) {
                        reservoirImage.src = 'https://i.imgur.com/ZDuG0yg.gif';
                    } else if (reservoirPercentage >= 70) {
                        reservoirImage.src = 'https://i.imgur.com/02ih7zL.gif';
                    } else if (reservoirPercentage >= 40) {
                        reservoirImage.src = 'https://i.imgur.com/rET9V2E.gif';
                    } else {
                        reservoirImage.src = 'https://i.imgur.com/FENKob8.gif';
                    }
                }
            })
            .catch(error => console.error('Error fetching reservoir data:', error));
    }

    function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    fetchAndRenderPlants();
    setInterval(fetchAndUpdateSoilMoisture, 5000);
    setInterval(fetchAndUpdateReservoirLevel, 5000); // Adjust interval as needed
});

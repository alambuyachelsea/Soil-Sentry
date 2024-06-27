document.addEventListener('DOMContentLoaded', function () {
    const ws = new WebSocket('ws://localhost:8000/ws'); // WebSocket connection

    ws.onopen = function () {
        console.log('WebSocket connection established.');
    };

    ws.onmessage = function (event) {
        const message = JSON.parse(event.data);
        const { type, data } = message;

        switch (type) {
            case 'plants':
                renderPlants(data);
                break;
            case 'soil_moisture':
                updateSoilMoisture(data);
                break;
            case 'reservoir_level':
                updateReservoirLevel(data);
                break;
            default:
                console.error('Unknown message type:', type);
        }
    };

    function renderPlants(plantsData) {
        const plantsContainer = document.querySelector('.plants');
        plantsContainer.innerHTML = '';

        plantsData.forEach(plant => {
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
    }

    function updateSoilMoisture(data) {
        const now = new Date();
        const soilMoistureChart = document.getElementById('soilMoistureChart').getContext('2d');

        data.forEach((plantData, index) => {
            soilMoistureChart.data.datasets[index].data.push({
                x: now,
                y: plantData.current_water_level
            });

            if (soilMoistureChart.data.datasets[index].data.length > 100) {
                soilMoistureChart.data.datasets[index].data.shift();
            }

            // Update current water level in the HTML
            const currentWaterLevelElement = document.getElementById(`current-water-level-${plantData.name.replace(/\s+/g, '-')}`);
            if (currentWaterLevelElement) {
                currentWaterLevelElement.textContent = `Current Water Level: ${plantData.current_water_level}`;
            } else {
                console.error(`Element with ID current-water-level-${plantData.name.replace(/\s+/g, '-')} not found`);
            }
        });

        soilMoistureChart.update();
    }

    function updateReservoirLevel(data) {
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
    }
});

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

    const ctxHourly = document.getElementById('hourlySoilMoistureChart').getContext('2d');
    const hourlySoilMoistureChart = new Chart(ctxHourly, {
        type: 'line',
        data: {
            labels: [], // Initialize with data if needed
            datasets: [] // Initialize with data if needed
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'minute' // Adjust the time unit to better fit longer data retention
                    }
                },
                y: {
                    beginAtZero: true,
                    max: 10 // Adjust the maximum value as needed
                }
            }
        }
    });

    const ctxDaily = document.getElementById('dailySoilMoistureChart').getContext('2d');
    const dailySoilMoistureChart = new Chart(ctxDaily, {
        type: 'line',
        data: {
            labels: [], // Initialize with data if needed
            datasets: [] // Initialize with data if needed
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day' // Adjust the time unit to better fit longer data retention
                    }
                },
                y: {
                    beginAtZero: true,
                    max: 10 // Adjust the maximum value as needed
                }
            }
        }
    });

    function fetchAndUpdateSoilMoisture() {
        const maxDataPoints = 50; // Define maxDataPoints within the function scope

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

                if (hourlySoilMoistureChart.data.datasets.length === 0) {
                    // Create dataset for each plant
                    data.forEach(plant => {
                        hourlySoilMoistureChart.data.datasets.push({
                            label: plant.name,
                            data: [],
                            borderColor: getRandomColor(),
                            borderWidth: 1,
                            fill: false
                        });
                    });

                    // Create dataset for reservoir level
                    hourlySoilMoistureChart.data.datasets.push({
                        label: 'Reservoir Level',
                        data: [],
                        borderColor: 'blue',
                        borderWidth: 1,
                        fill: false
                    });
                }

                // Update plant datasets
                data.forEach((plant, index) => {
                    hourlySoilMoistureChart.data.datasets[index].data.push({
                        x: now,
                        y: plant.current_water_level
                    });

                    if (hourlySoilMoistureChart.data.datasets[index].data.length > maxDataPoints) {
                        hourlySoilMoistureChart.data.datasets[index].data.shift();
                    }

                    // Update current water level in the HTML
                    const currentWaterLevelElement = document.getElementById(`current-water-level-${plant.name.replace(/\s+/g, '-')}`);
                    if (currentWaterLevelElement) {
                        currentWaterLevelElement.textContent = `Current Water Level: ${plant.current_water_level}`;
                    } else {
                        console.error(`Element with ID current-water-level-${plant.name.replace(/\s+/g, '-')} not found`);
                    }
                });

                // Fetch reservoir level data and update chart
                fetch('/ultrasonic_reading')
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(reservoirData => {
                        const adjustedReservoirLevel = reservoirData.level / 10; // Divide reservoir level by 10
                        hourlySoilMoistureChart.data.datasets[hourlySoilMoistureChart.data.datasets.length - 1].data.push({
                            x: now,
                            y: adjustedReservoirLevel
                        });

                        if (hourlySoilMoistureChart.data.datasets[hourlySoilMoistureChart.data.datasets.length - 1].data.length > maxDataPoints) {
                            hourlySoilMoistureChart.data.datasets[hourlySoilMoistureChart.data.datasets.length - 1].data.shift();
                        }

                        hourlySoilMoistureChart.update();

                        // Update reservoir level percentage in the HTML
                        const reservoirPercentage = reservoirData.level;
                        const reservoirPercentageElement = document.getElementById('reservoirLevel');
                        if (reservoirPercentageElement) {
                            reservoirPercentageElement.textContent = `${reservoirPercentage}%`; // Show the original percentage
                        } else {
                            console.error('Element with ID reservoirLevel not found');
                        }

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
            })
            .catch(error => console.error('Error fetching soil moisture data:', error));
    }

    function fetchAndUpdateDailyAverage() {
        const maxDays = 7; // Maximum number of days for the average

        fetch('/plants')
            .then(response => response.json())
            .then(data => {
                const now = new Date();

                if (dailySoilMoistureChart.data.datasets.length === 0) {
                    // Create dataset for each plant
                    data.forEach(plant => {
                        dailySoilMoistureChart.data.datasets.push({
                            label: plant.name,
                            data: [],
                            borderColor: getRandomColor(),
                            borderWidth: 1,
                            fill: false
                        });
                    });

                    // Create dataset for reservoir level
                    dailySoilMoistureChart.data.datasets.push({
                        label: 'Reservoir Level',
                        data: [],
                        borderColor: 'blue',
                        borderWidth: 1,
                        fill: false
                    });
                }

                // Compute average readings
                const averages = data.map(plant => {
                    return {
                        name: plant.name,
                        average: plant.current_water_level // Replace with actual averaging logic if needed
                    };
                });

                // Add average readings to chart
                averages.forEach((avg, index) => {
                    dailySoilMoistureChart.data.datasets[index].data.push({
                        x: now,
                        y: avg.average
                    });

                    if (dailySoilMoistureChart.data.datasets[index].data.length > maxDays) { // Assuming weekly data
                        dailySoilMoistureChart.data.datasets[index].data.shift();
                    }
                });

                // Fetch reservoir level data and update chart
                fetch('/ultrasonic_reading')
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(reservoirData => {
                        const adjustedReservoirLevel = reservoirData.level / 10; // Divide reservoir level by 10
                        dailySoilMoistureChart.data.datasets[dailySoilMoistureChart.data.datasets.length - 1].data.push({
                            x: now,
                            y: adjustedReservoirLevel
                        });

                        if (dailySoilMoistureChart.data.datasets[dailySoilMoistureChart.data.datasets.length - 1].data.length > maxDays) {
                            dailySoilMoistureChart.data.datasets[dailySoilMoistureChart.data.datasets.length - 1].data.shift();
                        }

                        dailySoilMoistureChart.update();
                    })
                    .catch(error => console.error('Error fetching reservoir data:', error));
            })
            .catch(error => console.error('Error fetching plant data:', error));
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
    fetchAndUpdateSoilMoisture();
    fetchAndUpdateDailyAverage();
    setInterval(fetchAndUpdateSoilMoisture, 3600000); // Fetch and update soil moisture every hour
    setInterval(fetchAndUpdateDailyAverage, 86400000); // Fetch and update daily average every 24 hours
});

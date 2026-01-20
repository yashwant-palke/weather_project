// const apiKey = ‘your-api-key-here';
// const apiUrl = 'https://api.openweathermap.org/data/2.5/weather?units=metric&q=';

// const searchBox = document.querySelector('.search input');
// const searchBtn = document.querySelector('.search button');

// var weatherIcon = document.querySelector('.weather-icon');
// var cityElement = document.querySelector('.city');
// var tempElement = document.querySelector('.temp');
// var humidityElement = document.querySelector('.humidity');
// var windElement = document.querySelector('.wind');
// var weatherDetails = document.querySelector('.weather-details'); // This is the wrapper for all weather details

// // Ensure the weather details are hidden initially
// weatherDetails.style.display = 'none';

// async function checkWeather(city) {
//     if (!city) {
//         // If the search box is empty, hide all weather details
//         weatherDetails.style.display = 'none';
//         return;
//     }
    
//     const response = await fetch(apiUrl + city + `&appid=${apiKey}`);
//     var data = await response.json();

//     console.log(data);

//     // If the city is found, show the weather details
//     if (data.cod === 200) {
//         weatherDetails.style.display = 'block'; // Show weather details if data is valid

//         // Display the weather information
//         cityElement.innerHTML = data.name;
//         tempElement.innerHTML = Math.round(data.main.temp) + '°C';
//         humidityElement.innerHTML = data.main.humidity + '%';
//         windElement.innerHTML = data.wind.speed + ' km/h';

//         // Set the appropriate weather icon based on weather conditions
//         if (data.weather[0].main === 'Clouds') {
//             weatherIcon.src = 'assets/img/cloudy-forecast-svgrepo-com.svg';
//         } else if (data.weather[0].main === 'Clear') {
//             weatherIcon.src = 'assets/img/egg-sunny-side-up-svgrepo-com.svg';
//         } else if (data.weather[0].main === 'Rain') {
//             weatherIcon.src = 'assets/img/rain-svgrepo-com (2).svg';
//         } else if (data.weather[0].main === 'Drizzle') {
//             weatherIcon.src = 'assets/img/cloud-drizzle-svgrepo-com.svg';
//         } else if (data.weather[0].main === 'Mist') {
//             weatherIcon.src = 'assets/img/mist-svgrepo-com.svg';
//         } else if (data.weather[0].main === 'Snow') {
//             weatherIcon.src = 'assets/img/snowing-forecast-svgrepo-com.svg';
//         }
//     } else {
//         // Handle case if the city is not found
//         weatherDetails.style.display = 'none';
//         alert("City not found!");
//     }
// }

// searchBtn.addEventListener('click', () => {
//     checkWeather(searchBox.value);
// });

// // Optionally, you can add a listener to handle the Enter key
// searchBox.addEventListener('keypress', (e) => {
//     if (e.key === 'Enter') {
//         checkWeather(searchBox.value);
//     }
// });






const input = document.getElementById("city-search");
const dropdown = document.getElementById("city-dropdown");
const submit_btn = document.getElementById("search-button");
const form = document.getElementById("weather-form");

let debounceTimer = null;

input.addEventListener("keyup", () => {
    const query = input.value.trim();

    clearTimeout(debounceTimer);

    if (query.length < 2) {
        dropdown.style.display = "none";
        return;
    }
    
    // debounce to avoid too many requests
    // search after 1 second
    debounceTimer = setTimeout(() => {
        fetchCities(query);
    }, 700); // ← time control (ms)

    // debounceTimer = setTimeout(() => {
    //     fetchCities(query);
    // }, 400);
});

function fetchCities(query) {
    // https://nominatim.openstreetmap.org/search?q=bilaspur&format=json
    fetch(
        `https://nominatim.openstreetmap.org/search?` +
        `q=${encodeURIComponent(query)}` +
        `&format=json&addressdetails=1&limit=5`
    )
    .then(res => res.json())
    .then(data => {
        dropdown.innerHTML = "";

        if (!data.length) {
            dropdown.style.display = "none";
            return;
        }

        data.forEach(place => {
            const city =
                place.address.city ||
                place.address.town ||
                place.address.village ||
                place.address.hamlet ||
                "";

            const state = place.address.state || "";
            const country = place.address.country || "";

            if (!city) return;

            const li = document.createElement("li");
            li.textContent = `${city}, ${state}, ${country}`;

            li.addEventListener("click", () => {
                input.value = `${city}, ${state}, ${country}`;
                dropdown.style.display = "none";
            });

            dropdown.appendChild(li);
        });

        dropdown.style.display = "block";
    })
    .catch(err => {
        console.error("Nominatim error:", err);
        dropdown.style.display = "none";
    });
}

// Close dropdown when clicking outside
document.addEventListener("click", (e) => {
    if (!e.target.closest(".search")) {
        dropdown.style.display = "none";
    }
});

// Submitting the form
submit_btn.addEventListener("click", () => {
    console.log("Form submitting");
    form.submit();
    console.log("Form submited");
});
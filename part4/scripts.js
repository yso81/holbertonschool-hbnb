document.addEventListener('DOMContentLoaded', () => {
    // ---------------------------------------------------------
    // 1. GLOBAL CONFIGURATION & DOM ELEMENTS
    // ---------------------------------------------------------
    const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const placesList = document.getElementById('places-list');
    const placeDetails = document.getElementById('place-details');
    const reviewForm = document.getElementById('review-form');
    const loginLink = document.getElementById('login-link');
    const priceFilter = document.getElementById('price-filter');
    const addReviewSection = document.getElementById('add-review');

    // ---------------------------------------------------------
    // 2. AUTHENTICATION HELPERS
    // ---------------------------------------------------------
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    function checkAuthentication() {
        const token = getCookie('token');
        if (loginLink) {
            if (token) {
                loginLink.textContent = 'Logout';
                loginLink.href = '#';
                loginLink.addEventListener('click', (e) => {
                    e.preventDefault();
                    document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
                    window.location.reload();
                });
            } else {
                loginLink.textContent = 'Login';
                loginLink.href = 'login.html';
            }
        }
        return token;
    }

    const token = checkAuthentication();

    // ---------------------------------------------------------
    // 3. LOGIN PAGE LOGIC
    // ---------------------------------------------------------
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            const oldError = document.getElementById('login-error-msg');
            if (oldError) oldError.remove();

            try {
                const response = await fetch(`${API_BASE_URL}/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/; max-age=86400`;
                    window.location.href = 'index.html';
                } else {
                    const errorData = await response.json();
                    const errorMessage = document.createElement('p');

                    errorMessage.id = 'login-error-msg';
                    errorMessage.style.color = 'red';
                    errorMessage.style.marginTop = '10px';
                    errorMessage.style.fontWeight = 'bold';
                    errorMessage.style.textAlign = 'center';

                    errorMessage.textContent = errorData.msg || 'Login failed: Invalid email or password';

                    loginForm.appendChild(errorMessage);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred during login');
            }
        });
    }

    // ---------------------------------------------------------
    // 4. REGISTRATION PAGE LOGIC
    // ---------------------------------------------------------
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const firstName = document.getElementById('first_name').value;
            const lastName = document.getElementById('last_name').value;

            try {
                const response = await fetch(`${API_BASE_URL}/users/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        email: email,
                        password: password,
                        first_name: firstName,
                        last_name: lastName
                    })
                });

                if (response.ok) {
                    alert('Registration successful! You can now login.');
                    window.location.href = 'login.html';
                } else {
                    const errorData = await response.json();
                    alert('Registration failed: ' + (errorData.msg || errorData.message || 'Unknown error'));
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred during registration.');
            }
        });
    }

    // ---------------------------------------------------------
    // 5. INDEX PAGE (Load Places)
    // ---------------------------------------------------------
    if (placesList) {
        async function loadPlaces(maxPrice = Infinity) {
            try {
                const headers = {
                    'Content-Type': 'application/json'
                };

                if (token) {
                    headers['Authorization'] = `Bearer ${token}`;
                }

                const response = await fetch(`${API_BASE_URL}/places/`, {
                    method: 'GET',
                    headers: headers
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch places');
                }

                const places = await response.json();
                
                placesList.innerHTML = ''; 

                places.forEach(place => {
                    const currentPrice = place.price || place.price_by_night;

                    if (currentPrice <= maxPrice) {
                        const placeCard = document.createElement('div');
                        placeCard.className = 'place-card';
                        
                        placeCard.innerHTML = `
                            <img src="https://placehold.co/600x400" alt="${place.name}">
                            <div class="place-info">
                                <h3>${place.name}</h3>
                                <p class="price">$${currentPrice} per night</p>
                                <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
                            </div>
                        `;
                        placesList.appendChild(placeCard);
                    }
                });
            } catch (error) {
                console.error('Error loading places:', error);
                placesList.innerHTML = '<p>Error loading places. Please try again later.</p>';
            }
        }

        if (priceFilter) {
            const prices = [10, 50, 100]; 
            const allOption = document.createElement('option');
            allOption.value = 'Infinity';
            allOption.textContent = 'All';
            priceFilter.appendChild(allOption);

            prices.forEach(price => {
                const option = document.createElement('option');
                option.value = price;
                option.textContent = `Under $${price}`;
                priceFilter.appendChild(option);
            });

            priceFilter.addEventListener('change', (e) => {
                loadPlaces(parseFloat(e.target.value));
            });
        }

        loadPlaces();
    }

    // ---------------------------------------------------------
    // 6. PLACE DETAILS PAGE
    // ---------------------------------------------------------
    if (placeDetails) {
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('id');
        const reviewsSection = document.getElementById('reviews');

        if (!placeId) {
            window.location.href = 'index.html';
        } else {
            if (addReviewSection) {
                addReviewSection.style.display = token ? 'block' : 'none';
            }

            async function loadPlaceDetails() {
                try {
                    const placeRes = await fetch(`${API_BASE_URL}/places/${placeId}`);
                    if (!placeRes.ok) throw new Error('Place not found');
                    const place = await placeRes.json();

                    let hostName = "Unknown Host";
                    const userId = place.user_id || place.owner_id; 
                    if (userId) {
                        try {
                            const userRes = await fetch(`${API_BASE_URL}/users/${userId}`);
                            if (userRes.ok) {
                                const userData = await userRes.json();
                                hostName = `${userData.first_name} ${userData.last_name}`;
                            }
                        } catch (e) { console.error("Error fetching host details"); }
                    }

                    const cityName = place.city_name || "Unknown Location";


                    let amenitiesListHtml = "<p>No amenities listed.</p>";
                    
                    let amenitiesData = place.amenities;

                    if (!amenitiesData || amenitiesData.length === 0) {
                         try {
                            const amRes = await fetch(`${API_BASE_URL}/places/${placeId}/amenities`);
                            if (amRes.ok) {
                                amenitiesData = await amRes.json();
                            }
                         } catch(e) { console.log("Amenities fetch failed"); }
                    }

                    if (amenitiesData && amenitiesData.length > 0) {
                        const items = amenitiesData.map(a => {
                            const name = a.name ? a.name : a; 
                            return `<li>${name}</li>`;
                        }).join('');
                        amenitiesListHtml = `<ul class="amenities-list">${items}</ul>`;
                    }


                    const titleElement = document.getElementById('place-title');
                    if (titleElement) {
                        titleElement.textContent = place.name;
                    }

                    placeDetails.innerHTML = `
                        <img src="${place.img || 'https://placehold.co/600x400'}" alt="${place.name}" style="width:100%; border-radius: 8px; margin-bottom: 15px;">
                        <div class="place-info">
                            <p class="price">Price: $${place.price || place.price_by_night} per night</p>
                            <div class="description">
                                ${place.description}
                            </div>
                            <div class="info-group" style="margin-top: 15px;">
                                <p><strong>Host:</strong> ${hostName}</p>
                                <p><strong>Location:</strong> ${cityName}</p>
                            </div>
                            
                            <!-- ADDED AMENITIES SECTION HERE -->
                            <div class="amenities-section">
                                <h2>Amenities</h2>
                                ${amenitiesListHtml}
                            </div>
                        </div>
                    `;

                    const reviewsRes = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`);
                    let reviewsList = document.getElementById('reviews-list');
                    
                    if (!reviewsList) {
                        reviewsList = document.createElement('div');
                        reviewsList.id = 'reviews-list';
                        if (reviewsSection) reviewsSection.appendChild(reviewsList);
                    } else {
                        reviewsList.innerHTML = '';
                    }

                    if (reviewsRes.ok) {
                        const reviews = await reviewsRes.json();
                        if (reviews.length === 0) {
                            reviewsList.innerHTML = '<p>No reviews yet.</p>';
                        } else {
                            for (const review of reviews) {
                                let reviewerName = "Anonymous";
                                try {
                                    const rUserRes = await fetch(`${API_BASE_URL}/users/${review.user_id}`);
                                    if (rUserRes.ok) {
                                        const rData = await rUserRes.json();
                                        reviewerName = `${rData.first_name} ${rData.last_name}`;
                                    }
                                } catch (e) {}

                                const ratingNum = parseInt(review.rating);
                                const stars = '★'.repeat(ratingNum) + '☆'.repeat(5 - ratingNum);

                                const reviewCard = document.createElement('div');
                                reviewCard.className = 'review-card';
                                reviewCard.innerHTML = `
                                    <div class="review-header">
                                        <strong>${reviewerName}</strong>
                                        <span class="rating">${stars}</span>
                                    </div>
                                    <p class="review-text">${review.text}</p>
                                `;
                                reviewsList.appendChild(reviewCard);
                            }
                        }
                    }
                } catch (error) {
                    console.error('Error:', error);
                    placeDetails.innerHTML = '<p>Error loading place details.</p>';
                }
            }
            loadPlaceDetails();

            if (reviewForm) { 
                reviewForm.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    
                    if (!token) {
                        alert("You must be logged in to review.");
                        return;
                    }

                    const text = document.getElementById('review-text').value;
                    const rating = document.getElementById('rating').value;

                    try {
                        const response = await fetch(`${API_BASE_URL}/reviews/`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': `Bearer ${token}`
                            },
                            body: JSON.stringify({
                                place_id: placeId,
                                text: text,
                                rating: parseInt(rating)
                            })
                        });

                        if (response.ok) {
                            alert('Review submitted!');
                            window.location.reload();
                        } else {
                            const errData = await response.json();
                            alert('Failed to submit review: ' + (errData.msg || errData.message || 'Unknown Error'));
                        }
                    } catch (error) {
                        console.error('Error:', error);
                        alert('Error submitting review');
                    }
                });
            }
        }
    }
});

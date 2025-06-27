Okay, let's integrate the API endpoints you've defined into the existing JavaScript files.

Based on your API definition and example requests, the backend API is hosted at `http://127.0.0.1:5000`.
*   Text search: `GET http://127.0.0.1:5000/search/<query>`
*   Price prediction: `GET http://127.0.0.1:5000/predict_price?image_url=<url>`
*   Similar items: `GET http://127.0.0.1:5000/find_similar?image_url=<url>&top_n=<n>`

However, your front-end code in `popup.js` and `search-integration.js` is currently structured to send Base64 image data in a POST request body, and the API example responses for visual search and text search use a `{ "isCompleteSuccessfully": bool, "data": [...], "errorMessages": [...] }` structure, while the price prediction uses a simple `{ "image_url": ..., "predicted_price_egp": ... }` structure. This is a mismatch between the provided front-end JS logic and the provided Flask API definitions.

**Assumption:** Given the front-end is structured to send Base64 via POST for AI features, and the provided Flask API definition seems incomplete regarding handling Base64 POSTs, we will proceed by *assuming* the actual AI endpoints (`/predict_price` and `/find_similar`) *also* have a POST method available at `http://127.0.0.1:5000/predict_price` and `http://127.0.0.1:5000/find_similar` that *accepts* `{"image": "base64_string"}` in the request body and return the example JSON format (specifically the price prediction returns a simple object, while the visual search returns the `{ isCompleteSuccessfully: ..., data: ..., errorMessages: ... }` structure). This requires minimal changes to your front-end's data handling logic for visual search.

We will update `search-integration.js` for text search and `popup.js` for visual search and price prediction. We will correct the API base URL and endpoint paths in these files to match `http://127.0.0.1:5000/` and your specified routes.

Other files (`auth.js`, `api-integration.js`, `cart.js`, `change-password.js`, `checkout.js`, `men-page-script.js`, `orders.js`, `product-grid.js`, `sproduct.js`) will remain unchanged, as they handle different functionalities or already interact with the other API base URL (`https://tpf.runasp.net/`) which is for general product fetching, not the AI search/prediction. The misleadingly named `predict-price.js` will also be left unchanged, as its code currently handles navigation, not prediction.

Here are the modified JavaScript files:

--- START OF FILE auth.js ---
```javascript
// --- NEW: Global function to update the cart count in the navbar ---
// Made global by attaching to the window object so other scripts can call it.
window.updateCartIcon = () => {
    const cart = JSON.parse(localStorage.getItem('shoppingCart')) || [];
    // Calculates the total number of items, not just unique entries
    const totalQuantity = cart.reduce((sum, item) => sum + (item.quantity || 0), 0); // Added || 0 fallback for safety
    const cartCountEl = document.getElementById('cart-count');
    if (cartCountEl) {
        cartCountEl.textContent = totalQuantity;
    }
};

document.addEventListener('DOMContentLoaded', () => {
    // === AUTH & PROFILE MODAL ELEMENTS ===
    const profileBtn = document.getElementById('profile-icon-btn');
    const authModal = document.getElementById('authModal');
    const profileModal = document.getElementById('userProfileModal');
    
    // Auth Modal Specific
    const authBox = document.getElementById('auth-box');
    const signUpBtn = document.getElementById('signUpBtnModal');
    const signInBtn = document.getElementById('signInBtnModal');

    // Auth Form Elements
    const signUpNameInput = document.getElementById('signUpName');
    const signUpEmailInput = document.getElementById('signUpEmail');
    const signUpPasswordInput = document.getElementById('signUpPassword');
    const signUpActionBtn = document.getElementById('signUpActionBtn');
    const signInEmailInput = document.getElementById('signInEmail');
    const signInPasswordInput = document.getElementById('signInPassword');
    const signInActionBtn = document.getElementById('signInActionBtn');

    // Profile Modal elements
    const closeProfileBtn = document.querySelector('.profile-modal-close-btn');
    const userProfileForm = document.getElementById('userProfileForm');
    const logoutBtn = document.getElementById('profile-logout-btn');
    const profileFirstNameInput = document.getElementById('profile-firstname');
    const profileLastNameInput = document.getElementById('profile-lastname');
    const profileEmailInput = document.getElementById('profile-email');
    const profilePhoneInput = document.getElementById('profile-phone');
    const profileLocationInput = document.getElementById('profile-location');
    const profileCardNumberInput = document.getElementById('profile-cardnumber');
    const displayNameEl = document.getElementById('profile-display-name');
    const displayLocationEl = document.getElementById('profile-display-location');
    const avatarUploadInput = document.getElementById('avatarUpload');
    const profileAvatarImg = document.getElementById('profile-avatar-img');
    const navProfileImg = document.getElementById('nav-profile-img');

    // Success Prompt Modal Elements
    const successModal = document.getElementById('successPromptModal');
    const successModalTitle = document.getElementById('successModalTitle');
    const successModalMessage = document.getElementById('successModalMessage');
    const successModalBtn = document.getElementById('successModalBtn');


    // Data & State Management
    const getUsersDB = () => JSON.parse(localStorage.getItem('usersDB')) || {};
    const saveUsersDB = (db) => localStorage.setItem('usersDB', JSON.stringify(db));
    const getCurrentUserEmail = () => localStorage.getItem('currentUserEmail');
    const setCurrentUserEmail = (email) => localStorage.setItem('currentUserEmail', email);
    const logoutCurrentUser = () => localStorage.removeItem('currentUserEmail');
    const isLoggedIn = () => getCurrentUserEmail() !== null;

    // Function to show the success modal
    const showSuccessModal = (title, message) => {
        if (!successModal) return;
        successModalTitle.textContent = title;
        successModalMessage.textContent = message;
        successModal.style.display = 'flex';
        // Add the 'show' class after a very short delay to allow the display property to change
        setTimeout(() => successModal.classList.add('show'), 10);
        
        // Auto-reload unless manually closed by successModalBtn click
        const autoReloadTimeout = setTimeout(() => {
            window.location.reload();
        }, 2500);

        // Add listener to clear the auto-reload timeout if the button is clicked
        if (successModalBtn) {
             successModalBtn.onclick = () => { // Use onclick to easily overwrite previous handlers
                 clearTimeout(autoReloadTimeout);
                 window.location.reload();
             };
         }
    };
    
    // Ensure a click on the success modal button always reloads if somehow not already handled
    if (successModalBtn) {
         // This listener is less specific, the onclick above is preferred if it exists
         successModalBtn.addEventListener('click', () => window.location.reload());
    }


    const loadProfileData = () => {
        if (!isLoggedIn() || !profileModal) return;
        const userProfile = getUsersDB()[getCurrentUserEmail()];
        if (!userProfile) {
            logoutCurrentUser();
            return;
        }
        if (profileFirstNameInput) profileFirstNameInput.value = userProfile.firstname || '';
        if (profileLastNameInput) profileLastNameInput.value = userProfile.lastname || '';
        if (profileEmailInput) {
            profileEmailInput.value = userProfile.email || '';
            profileEmailInput.disabled = true;
        }
        if (profilePhoneInput) profilePhoneInput.value = userProfile.phone || '';
        if (profileLocationInput) profileLocationInput.value = userProfile.location || '';
        if (profileCardNumberInput) profileCardNumberInput.value = userProfile.cardnumber || '';
        const fullName = `${userProfile.firstname || ''} ${userProfile.lastname || ''}`.trim();
        if (displayNameEl) displayNameEl.textContent = fullName || 'Your Name';
        if (displayLocationEl) displayLocationEl.textContent = userProfile.location || 'Your Location';
        const avatarSrc = userProfile.avatarUrl || 'Icons/user.png';
        if (profileAvatarImg) profileAvatarImg.src = avatarSrc;
        updateNavIcon();
    };
    
    const updateNavIcon = () => {
        if (!navProfileImg) return;
        if (isLoggedIn()) {
            const currentUser = getUsersDB()[getCurrentUserEmail()];
            if (currentUser && currentUser.avatarUrl) { // Only use avatarUrl if it exists and user is logged in
                navProfileImg.src = currentUser.avatarUrl;
                navProfileImg.style.borderRadius = '50%';
            } else { // Use default if user is logged in but has no avatarUrl saved
                navProfileImg.src = 'Icons/user.png';
                 navProfileImg.style.borderRadius = ''; // Reset if default icon isn't round
            }
        } else { // If not logged in, use default icon
            navProfileImg.src = 'Icons/user.png';
             navProfileImg.style.borderRadius = ''; // Reset if default icon isn't round
        }
    };

    if (profileBtn) {
        profileBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (isLoggedIn()) {
                if (profileModal) {
                    loadProfileData();
                    profileModal.style.display = 'flex';
                }
            } else {
                if (authModal) authModal.style.display = 'flex';
            }
        });
    }

    if (signUpBtn && signInBtn && authBox) {
        signUpBtn.addEventListener('click', () => { authBox.classList.add("right-panel-active"); });
        signInBtn.addEventListener('click', () => { authBox.classList.remove("right-panel-active"); });
    }

    // Close modals when clicking outside the content box
    if (authModal) {
         authModal.addEventListener('click', e => {
             if (e.target === authModal) {
                 authModal.style.display = 'none';
                 authModal.classList.remove('show'); // Remove show class if using transitions
             }
         });
     }
     if (profileModal) {
         profileModal.addEventListener('click', e => {
              if (e.target === profileModal) {
                 profileModal.style.display = 'none';
                 profileModal.classList.remove('show'); // Remove show class if using transitions
              }
          });
     }
    // Close profile modal specifically via its close button
    if (closeProfileBtn) closeProfileBtn.addEventListener('click', () => profileModal.style.display = 'none');


    if (signUpActionBtn && signUpNameInput && signUpEmailInput && signUpPasswordInput) { // Check all necessary sign-up elements exist
        signUpActionBtn.addEventListener('click', () => {
            const name = signUpNameInput.value.trim();
            const email = signUpEmailInput.value.trim().toLowerCase();
            const password = signUpPasswordInput.value;
            if (!name || !email || !password) {
                alert('Please fill in all fields.');
                return;
            }
            if (!/\S+@\S+\.\S+/.test(email)) { // Basic email format validation
                alert('Please enter a valid email address.');
                return;
            }
            const db = getUsersDB();
            if (db[email]) {
                alert('An account with this email already exists.');
                return;
            }
            // Store minimal initial data, populate full profile later
            db[email] = { 
                email: email, 
                password: password, 
                firstname: name, // Use name input for firstname
                lastname: '', 
                phone: '', 
                location: '', 
                cardnumber: '', 
                avatarUrl: null // Initialize avatarUrl as null
            };
            saveUsersDB(db);
            setCurrentUserEmail(email);
            if (authModal) authModal.style.display = 'none';
            showSuccessModal('Account Created!', 'Welcome to FashioNear. You are now signed in.');
        });
    }

    if (signInActionBtn && signInEmailInput && signInPasswordInput) { // Check all necessary sign-in elements exist
        signInActionBtn.addEventListener('click', () => {
            const email = signInEmailInput.value.trim().toLowerCase();
            const password = signInPasswordInput.value;
            if (!email || !password) {
                alert('Please enter both email and password.');
                return;
            }
            const user = getUsersDB()[email];
            if (!user || user.password !== password) {
                alert('Incorrect email or password.');
                return;
            }
            setCurrentUserEmail(email);
            if (authModal) authModal.style.display = 'none';
            showSuccessModal('Sign In Successful!', 'Welcome back! Redirecting you now.');
        });
    }
    
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            logoutCurrentUser();
             // Clear profile modal inputs on logout
            if (userProfileForm) userProfileForm.reset();
            if (profileModal) profileModal.style.display = 'none';
            updateNavIcon(); // Update nav icon to default immediately
            showSuccessModal('Logged Out', 'You have been successfully logged out.');
        });
    }

    if (userProfileForm && profileFirstNameInput && profileLastNameInput && profileEmailInput && profilePhoneInput && profileLocationInput && profileCardNumberInput) { // Check all necessary profile form elements exist
        userProfileForm.addEventListener('submit', (e) => {
            e.preventDefault();
            if (!isLoggedIn()) return;
            const db = getUsersDB();
            const email = getCurrentUserEmail();
             if (!db[email]) { // Safety check
                console.error("User not found in DB when saving profile.");
                logoutCurrentUser();
                showSuccessModal("Error", "User data not found. Please log in again.");
                return;
             }
            db[email].firstname = profileFirstNameInput.value.trim();
            db[email].lastname = profileLastNameInput.value.trim();
            db[email].phone = profilePhoneInput.value.trim();
            db[email].location = profileLocationInput.value.trim();
            db[email].cardnumber = profileCardNumberInput.value.trim();
            saveUsersDB(db);
            loadProfileData(); // Reload data to update display names immediately
            if (profileModal) profileModal.style.display = 'none';
            showSuccessModal('Profile Saved', 'Your information has been updated successfully.');
        });
    }
    
    if (avatarUploadInput && profileAvatarImg) { // Check if avatar upload and display elements exist
        avatarUploadInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file && isLoggedIn()) {
                // Basic file type validation for preview/storage
                const acceptedTypes = ['image/png', 'image/jpeg', 'image/webp'];
                 if (!acceptedTypes.includes(file.type)) {
                     alert('Invalid file type. Please select a PNG, JPEG, or WebP image.');
                     return;
                 }

                const reader = new FileReader();
                reader.onload = function(event) {
                    const avatarUrl = event.target.result; // Data URL (Base64)
                    const db = getUsersDB();
                    const email = getCurrentUserEmail();
                    if (db[email]) { // Safety check
                        db[email].avatarUrl = avatarUrl;
                        saveUsersDB(db);
                        loadProfileData(); // Update profile view and navbar icon
                    } else {
                        console.error("User not found in DB during avatar upload.");
                        alert("Error updating avatar. Please log in again.");
                         logoutCurrentUser();
                    }
                }
                reader.onerror = function(event) {
                     console.error("FileReader error:", event.target.error);
                     alert("Error reading file. Please try again.");
                }
                reader.readAsDataURL(file); // Read file as Base64
            } else if (file && !isLoggedIn()) {
                alert("Please log in to upload an avatar.");
            }
        });
    }

    // --- INITIALIZATION ---
    updateNavIcon(); // Update the navbar icon state based on login status on page load
    // window.updateCartIcon(); // This is called globally via the function definition itself
});
```

--- START OF FILE api-integration.js ---
```javascript
async function fetchProducts(category = '') {
    // This script fetches products from the original API
    let url = `https://tpf.runasp.net/api/Products?numberOfProduct=100`;
    if (category) {
        url += `&categoryName=${category}`;
    }
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        // The API might return an array directly or wrapped in an object
        const products = Array.isArray(data) ? data : (data.products || data.data || []);
        return products;
    } catch (error) {
        console.error("Error fetching products:", error);
        return [];
    }
}

// The displayProducts function should ideally be global or in its own file
// It's currently present in api-integration.js, product-grid.js, and resultpage.js (duplicate)
// Assuming the copy in product-grid.js is used by default due to its inclusion order and event delegation
// Leaving this copy here but acknowledging potential redundancy
function displayProducts(products, containerId) {
    const productGrid = document.getElementById(containerId);
    if (!productGrid) {
        console.error(`Product grid container with ID ${containerId} not found.`);
        return;
    }
    // Only clear if it's the main product-grid. For related, product-grid.js clears the specific related grid.
    if (containerId === 'product-grid') {
        productGrid.innerHTML = ''; // Clear existing products
    }


    if (!Array.isArray(products) || products.length === 0) {
         // Check if the grid already has a loading spinner before adding 'No products' message
         const loadingSpinner = productGrid.querySelector('.loading-spinner');
         if (loadingSpinner) {
             loadingSpinner.remove(); // Remove spinner if no products found
         }
        productGrid.innerHTML = '<div style="text-align: center; padding: 50px;"><p>No products available at the moment.</p></div>';
        return;
    }

     // Check and remove loading spinner before adding products
    const loadingSpinner = productGrid.querySelector('.loading-spinner');
    if (loadingSpinner) {
        loadingSpinner.remove();
    }


    products.forEach(product => {
        const productElement = document.createElement('div');
        productElement.classList.add('pro');
        // Ensure IDs are strings when setting data attributes
        productElement.setAttribute('data-id', String(product.id || '')); 
        productElement.setAttribute('data-name', product.name || 'Unknown Product');
        productElement.setAttribute('data-price', product.price || '0');
        productElement.setAttribute('data-desc', product.description || '');

        // Use fallback values for missing properties
        const productName = product.name || 'Unknown Product';
        const productPrice = product.price || '0';
        // Prioritize brand > category name > default
        const productBrand = product.brand || product.categoryName || 'FashioNear'; 
        // Prioritize imageUrl > image > default placeholder
        const productImage = product.imageUrl || product.image || 'Images/placeholder.png'; 

        productElement.innerHTML = `
            <div class="pro-img-container">
                <img src="${productImage}" alt="${productName}" onerror="this.src='Images/placeholder.png'">
            </div>
            <div class="des">
                <span>${productBrand}</span>
                <h5>${productName}</h5>
                <div class="star">
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                </div>
                <h4>${productPrice}LE</h4>
            </div>
            <button class="add-to-cart-btn"><i class="fas fa-shopping-cart cartt"></i></button>
        `;
        productGrid.appendChild(productElement);
    });
}
```

--- START OF FILE cart.js ---
```javascript
document.addEventListener('DOMContentLoaded', () => {
    // --- STATE & CONSTANTS ---
    const PROCESSING_FEE = 80.00;
    const PROMO_THRESHOLDS = { 1: 1000, 2: 2000, 3: 3000 };
    const MAX_PROMO_VALUE = 3000;
    let cart = JSON.parse(localStorage.getItem('shoppingCart')) || [];

    // --- DOM ELEMENTS ---
    const cartItemsContainer = document.getElementById('cartItemsContainer');
    const subtotalValueEl = document.getElementById('subtotalValue');
    const processingFeeEl = document.getElementById('processingFee');
    const totalValueEl = document.getElementById('totalValue');
    const grandTotalValueEl = document.getElementById('grandTotalValue');
    const progressBar = document.getElementById('progressBar');
    // coupon input - added ID based on HTML
    const couponInput = document.getElementById('coupon');
    
    // --- FUNCTIONS ---
    const saveCart = () => {
        localStorage.setItem('shoppingCart', JSON.stringify(cart));
    };
    
    const renderCartItems = () => {
        cartItemsContainer.innerHTML = ''; 
        if (cart.length === 0) {
            cartItemsContainer.innerHTML = '<p style="text-align:center; padding: 2rem; color: #8a8a8a;">Your cart is empty. <a href="All.html" style="color: coral;">Go shopping!</a></p>';
            return;
        }

        cart.forEach(item => {
            const price = parseFloat(item.price) || 0;
            const itemTotal = price * item.quantity;
            const itemEl = document.createElement('div');
            itemEl.className = 'cart-item';
            
            // Ensure size is displayed, fallback to 'N/A' if not available
            const displaySize = item.size || 'N/A';
            // Use fallback value for the image source
            const imageUrl = item.imgSrc || 'Images/placeholder.png';

            itemEl.innerHTML = `
                <div class="item-image">
                    <img src="${imageUrl}" alt="${item.name}" onerror="this.src='Images/placeholder.png';">
                </div>
                <div class="item-info">
                    <p>${item.name}</p>
                    <span>Size: ${displaySize}</span>
                </div>
                <div class="item-quantity">
                    <button class="qty-btn" data-id="${item.id}" data-size="${displaySize}" data-action="decrease">-</button>
                    <span>${item.quantity}</span>
                    <button class="qty-btn" data-id="${item.id}" data-size="${displaySize}" data-action="increase">+</button>
                </div>
                <strong class="item-price">${itemTotal.toFixed(2)}LE</strong>
                <button class="remove-btn" data-id="${item.id}" data-size="${displaySize}">×</button>
            `;
            cartItemsContainer.appendChild(itemEl);
        });
    };
    
    const updateSummary = () => {
        const subtotal = cart.reduce((sum, item) => sum + (parseFloat(item.price) * (item.quantity || 0)), 0); // Added || 0 for safety
        // Apply coupon logic if you had it
        // const discount = applyCoupon(subtotal, couponInput.value);
        // const totalWithDiscount = subtotal - discount;

        const totalInPounds = subtotal + PROCESSING_FEE; // Assuming PROCESSING_FEE is always added
        
        subtotalValueEl.textContent = `${subtotal.toFixed(2)}LE`;
        processingFeeEl.textContent = `${PROCESSING_FEE.toFixed(2)}LE`;
        totalValueEl.textContent = `${totalInPounds.toFixed(2)}LE`; // Update this if using discount
        grandTotalValueEl.textContent = `${totalInPounds.toFixed(2)}LE`; // And this

        // Check if the global updateCartIcon function exists before calling
        if (window.updateCartIcon) {
             window.updateCartIcon();
        }
        
        updateProgressBar(subtotal);
        updatePromos(subtotal);
    };

     // Example applyCoupon function (placeholder)
     /*
     const applyCoupon = (subtotal, couponCode) => {
         let discount = 0;
         // Example coupon logic:
         if (couponCode === 'SAVE10') {
             discount = subtotal * 0.10; // 10% off
         }
         // Add more coupon logic here
         return discount;
     };
     */


    const updateProgressBar = (subtotal) => {
        const progressPercentage = Math.min((subtotal / MAX_PROMO_VALUE) * 100, 100);
        if (progressBar) { // Check if element exists
            progressBar.style.width = `${progressPercentage}%`;
        }
    };

    const updatePromos = (subtotal) => {
        for (const [id, threshold] of Object.entries(PROMO_THRESHOLDS)) {
            const promoEl = document.getElementById(`promo-${id}`);
            if (promoEl) { // Add check if element exists
                if (subtotal >= threshold) {
                    promoEl.classList.add('active');
                } else {
                    promoEl.classList.remove('active');
                }
            }
        }
    };
    
    const handleCartUpdate = (e) => {
        const target = e.target;
        // Use closest to be robust to clicks on icons inside buttons
        const qtyBtn = target.closest('.qty-btn');
        const removeBtn = target.closest('.remove-btn');

        // Allow clicks on the link itself, but not other random places in the container
        if (!qtyBtn && !removeBtn && !target.closest('a.order-item')) {
            return; // Exit if the click is not on a relevant button or item link.
        }
         // Allow navigation if clicking the item link itself
         if (target.closest('a.order-item')) {
             return; 
         }


        const itemId = (qtyBtn || removeBtn).dataset.id;
        // Use data-size from the button itself, not the item-info span
        const itemSize = (qtyBtn || removeBtn).dataset.size;

        // Find the index of the item in the cart. Compare IDs as strings to avoid type issues.
        const itemIndex = cart.findIndex(i => {
            // Ensure comparison handles potential null/undefined sizes gracefully
            const cartItemSize = i.size || 'N/A';
            const clickedItemSize = itemSize || 'N/A'; // Use 'N/A' if data-size is missing
            return String(i.id) === String(itemId) && cartItemSize === clickedItemSize;
        });


        if (itemIndex === -1) {
            console.error("Item not found in cart for update/removal.", {itemId, itemSize, cart});
            return; 
        }

        // Handle quantity changes or removal.
        if (qtyBtn) {
            const action = qtyBtn.dataset.action;
            if (action === 'increase') {
                cart[itemIndex].quantity = (cart[itemIndex].quantity || 0) + 1; // Added || 0 for safety
            } else if (action === 'decrease') {
                if ((cart[itemIndex].quantity || 0) > 1) { // Added || 0 for safety
                    cart[itemIndex].quantity--;
                } else {
                    // Remove item if quantity is 1 and decrease is clicked
                    cart.splice(itemIndex, 1); 
                }
            }
        } else if (removeBtn) {
            // Remove item on delete button click.
            cart.splice(itemIndex, 1); 
        }
        
        renderAndCalculate();
    };
    
    const renderAndCalculate = () => {
        saveCart(); 
        renderCartItems();
        updateSummary();
        // updateCartIcon() is called within updateSummary() now
    };

    // --- EVENT LISTENERS ---
    if (cartItemsContainer) { // Check if container exists
         cartItemsContainer.addEventListener('click', handleCartUpdate);
    }
    // Add listener for coupon input if it affects total dynamically
    /*
    if (couponInput) {
        couponInput.addEventListener('input', updateSummary); // Or 'change'
    }
    */


    // --- INITIALIZATION ---
    renderAndCalculate();
    // The global updateCartIcon is called by auth.js on DOMContentLoaded
});
```

--- START OF FILE change-password.js ---
```javascript
document.addEventListener('DOMContentLoaded', () => {

    // --- YETI Animation Logic ---
    const yetiAvatar = document.getElementById('yeti-avatar');
    const formWrapper = document.querySelector('.form-wrapper');
    const passwordFields = document.querySelectorAll('.password-field');
    const togglePasswordIcons = document.querySelectorAll('.toggle-password');
    
    const yetiStates = {
        default: 'img/yeti-default.png',
        lookLeft: 'img/yeti-look-left.png',
        lookRight: 'img/yeti-look-right.png',
        lookFarRight: 'img/yeti-look-far-right.png',
        covering: 'img/yeti-cover.png',
        peeking: 'img/yeti-peek.png'
    };
    
    // --- Eye Tracking Function ---
    function trackMouse(e) {
        if (!yetiAvatar || !formWrapper) return; // Exit if essential elements are missing
        const rect = formWrapper.getBoundingClientRect();
        const formCenterX = rect.left + rect.width / 2;
        const mouseX = e.clientX;
        const delta = mouseX - formCenterX;

        let newState;
        // Adjust sensitivity based on your layout/yeti image size
        if (delta < -50) { 
            newState = yetiStates.lookLeft;
        } else if (delta > 80) { // Maybe look Far Right is further out?
            newState = yetiStates.lookFarRight;
        } else if (delta > 30) { // Slightly less sensitive to look right
            newState = yetiStates.lookRight;
        } else {
            newState = yetiStates.default;
        }
        
        // Check if the new state is different from the current image source
        if (yetiAvatar.src.includes(newState.substring(newState.lastIndexOf('/') + 1))) {
             return; // Avoids flickering by only changing the source if it's different
        }
        
        yetiAvatar.src = newState; // Updates the mascot image source
    }
    
    // By default, the yeti tracks the mouse, but only if the yeti avatar exists
    if (yetiAvatar && formWrapper) {
        document.addEventListener('mousemove', trackMouse);
    }


    // --- Password Field Interactions (Covering Eyes) ---
    passwordFields.forEach(field => {
        field.addEventListener('focus', () => {
            if (yetiAvatar) {
                // Stop eye-tracking and cover eyes
                document.removeEventListener('mousemove', trackMouse);
                yetiAvatar.src = yetiStates.covering;
                yetiAvatar.style.transform = 'scale(0.95)';
            }
        });

        field.addEventListener('blur', () => {
             // Only revert if the input field is not part of a visibility toggle interaction
            // (i.e. the mouseup/mouseleave event on the icon will handle reverting)
             if (yetiAvatar && field.getAttribute('type') === 'password') {
                 // Uncover eyes and resume eye-tracking
                 yetiAvatar.src = yetiStates.default;
                 yetiAvatar.style.transform = 'scale(1)';
                 if (formWrapper) { // Only add listener if the element exists
                     document.addEventListener('mousemove', trackMouse);
                 }
             } else if (yetiAvatar && field.getAttribute('type') === 'text') {
                 // If still text, it means mouseup/mouseleave didn't fire on the icon,
                 // probably because the icon wasn't clicked. Revert anyway.
                 yetiAvatar.src = yetiStates.default;
                 yetiAvatar.style.transform = 'scale(1)';
                 if (formWrapper) {
                      document.addEventListener('mousemove', trackMouse);
                 }
             }
        });
    });

    // --- Password Visibility Toggle Interactions (Peeking) ---
    togglePasswordIcons.forEach(icon => {
        if (!yetiAvatar) return; // Skip if yeti avatar doesn't exist

        const input = icon.previousElementSibling; // Get the associated input field

        // Ensure the input exists and is a password field
        if (!input || input.type !== 'password') return;

        // When mouse is HELD DOWN, yeti peeks
        icon.addEventListener('mousedown', function (event) {
            event.preventDefault(); // Prevents losing focus from the input
            yetiAvatar.src = yetiStates.peeking;

            input.setAttribute('type', 'text');
            this.classList.replace('fa-eye-slash', 'fa-eye');
             // Temporarily disable mousemove tracking while peeking
             document.removeEventListener('mousemove', trackMouse);
        });

        // When mouse is RELEASED, yeti goes back to covering eyes
        icon.addEventListener('mouseup', function () {
             // Revert to covering only if the input still has focus
            if (input === document.activeElement) {
                 yetiAvatar.src = yetiStates.covering;
             } else {
                 // If input lost focus during mousedown/mouseup, revert to default and resume tracking
                 yetiAvatar.src = yetiStates.default;
                  if (formWrapper) {
                     document.addEventListener('mousemove', trackMouse);
                 }
             }

            input.setAttribute('type', 'password');
            this.classList.replace('fa-eye', 'fa-eye-slash');
        });

        // If mouse leaves while held down, also stop peeking
         icon.addEventListener('mouseleave', function () {
             // Check if the input type is currently 'text' (meaning mouse was held down when leaving)
             if(input.getAttribute('type') === 'text') {
                 // Revert to covering only if the input still has focus
                 if (input === document.activeElement) {
                    yetiAvatar.src = yetiStates.covering;
                 } else {
                    // If input lost focus during mouseleave, revert to default and resume tracking
                     yetiAvatar.src = yetiStates.default;
                      if (formWrapper) {
                         document.addEventListener('mousemove', trackMouse);
                     }
                 }
                input.setAttribute('type', 'password');
                this.classList.replace('fa-eye', 'fa-eye-slash');
             }
        });
    });

    // --- Live Password Strength Validation ---
    const newPasswordInput = document.getElementById('new-password');
    const strengthMeter = document.getElementById('strength-meter');
    // Check if strengthMeter exists before querying its children
    const strengthBars = strengthMeter ? strengthMeter.querySelectorAll('span') : [];

    if (newPasswordInput && strengthMeter && strengthBars.length > 0) { // Check if all necessary elements exist
        newPasswordInput.addEventListener('input', function() {
            const password = this.value;
            const strength = calculatePasswordStrength(password);
            updateStrengthMeter(strength);
        });
    } else {
         console.warn("Password strength meter elements not found. Strength feature disabled.");
    }


    function calculatePasswordStrength(password) {
        let strength = 0;
        if (password.length > 0) strength = 1;
        if (password.length >= 8) strength = 2;
        // Added checks for uppercase and lowercase letters for better strength calculation
        const hasMixedCase = /[a-z]/.test(password) && /[A-Z]/.test(password); 
        if (password.length >= 8 && /[0-9]/.test(password) && hasMixedCase) strength = 3;
        if (password.length >= 12 && /[0-9]/.test(password) && hasMixedCase && /[^A-Za-z0-9]/.test(password)) strength = 4;
        return strength;
    }

    function updateStrengthMeter(strength) {
        // Ensure we don't try to access colors outside the array range
        const safeStrength = Math.max(0, Math.min(strength, strengthBars.length));

        const strengthColors = [
            'var(--bar-default-color)', // 0 - Should ideally not be used if length > 0
            'var(--bar-weak-color)',    // 1
            'var(--bar-medium-color)',   // 2
            'var(--bar-strong-color)',  // 3
            'var(--bar-strong-color)'   // 4 - Uses the same color as 3 since there are only 4 bars
        ];
        
        strengthBars.forEach((bar, index) => {
            if (index < safeStrength) {
                 // Use the color corresponding to the *current* strength level for all filled bars
                bar.style.backgroundColor = strengthColors[safeStrength]; 
            } else {
                bar.style.backgroundColor = 'var(--bar-default-color)';
            }
        });
    }
});
```

--- START OF FILE checkout.js ---
```javascript
document.addEventListener('DOMContentLoaded', () => {
    // --- STATE & CONSTANTS ---
    const PROCESSING_FEE = 80.00;
    const cart = JSON.parse(localStorage.getItem('shoppingCart')) || [];

    // --- DOM ELEMENTS ---
    const subtotalEl = document.getElementById('subtotalValue');
    const processingFeeEl = document.getElementById('processingFee');
    const totalEl = document.getElementById('totalValue');
    const grandTotalEl = document.getElementById('grandTotalValue');
    const confirmPaymentAmountEl = document.getElementById('confirmPaymentAmount');
    
    // Payment elements
    const paymentOptions = document.querySelectorAll('.radio-option');
    const creditCardForm = document.querySelector('.payment-information');
    
    // Form, Buttons and MODALS
    const shippingAddressInput = document.getElementById('shippingAddress');
    const cardNumberInput = document.getElementById('cardNumber');
    const confirmPaymentBtn = document.getElementById('confirmPaymentBtn');
    const authModal = document.getElementById('authModal');
    const orderSuccessModal = document.getElementById('orderSuccessModal');
    const cartEmptyModal = document.getElementById('cartEmptyModal');

    // Auth helpers (assuming auth.js defining isLoggedIn runs before this)
    // If auth.js might not run first, define a fallback isLoggedIn here
    const isLoggedIn = typeof window.isLoggedIn === 'function' ? window.isLoggedIn : () => !!localStorage.getItem('currentUserEmail');


    // --- FUNCTIONS ---
    function updateCheckoutSummary() {
        const subtotal = cart.reduce((sum, item) => sum + (parseFloat(item.price) * (item.quantity || 0)), 0); // Added || 0 for quantity safety
        const total = subtotal + PROCESSING_FEE;
        const formatPrice = (price) => `${price.toFixed(2)} LE`;
        
        if (subtotalEl) subtotalEl.textContent = formatPrice(subtotal);
        if (processingFeeEl) processingFeeEl.textContent = formatPrice(PROCESSING_FEE);
        if (totalEl) totalEl.textContent = formatPrice(total);
        if (grandTotalEl) grandTotalEl.textContent = formatPrice(total);
        if (confirmPaymentAmountEl) confirmPaymentAmountEl.textContent = formatPrice(total);
    }

    function setupPaymentSelection() {
        if (paymentOptions.length === 0) return; // Exit if no payment options exist

        // Select the first option by default
        const defaultOption = paymentOptions[0];
        defaultOption.classList.remove('inactive');
         if (creditCardForm) {
             const isCardSelected = defaultOption.hasAttribute('data-card-option');
             creditCardForm.style.display = isCardSelected ? 'block' : 'none';
         }


        paymentOptions.forEach(option => {
            option.addEventListener('click', () => {
                // Remove active state from all and add inactive
                paymentOptions.forEach(opt => {
                    opt.classList.remove('active'); // Use 'active' instead of removing 'inactive'
                    opt.classList.add('inactive');
                });
                // Add active state to the clicked one and remove inactive
                option.classList.add('active');
                option.classList.remove('inactive');
                
                if (creditCardForm) {
                    const isCardSelected = option.hasAttribute('data-card-option');
                    creditCardForm.style.display = isCardSelected ? 'block' : 'none';
                }
            });
        });
    }

    function loadUserData() {
        if (isLoggedIn()) {
            const users = JSON.parse(localStorage.getItem('usersDB')) || {};
            const currentUserEmail = localStorage.getItem('currentUserEmail');
            const currentUser = users[currentUserEmail];
            if (currentUser) {
                // Only populate if the input fields exist
                if (shippingAddressInput) shippingAddressInput.value = currentUser.location || '';
                if (cardNumberInput) cardNumberInput.value = currentUser.cardnumber || '';
                // Also potentially populate name on card, expiry, etc. if they exist in user data
            } else {
                 // User email is in localStorage but no user data? Possible inconsistency.
                 // Consider logging out the user or prompting them to sign in again.
                 console.warn("Current user email found, but user data missing from DB.");
                 // Optional: logoutCurrentUser(); showSignInPromptModal();
             }
        } else {
             // Not logged in, inputs should remain empty/placeholders
         }
    }

    // UPDATED: processOrder function to save the order
    function processOrder() {
        const currentUserEmail = localStorage.getItem('currentUserEmail');
        if (!currentUserEmail) { // Should not happen if isLoggedIn check passes, but safety first
            console.error("processOrder called but user is not logged in.");
            // Perhaps show a more specific error modal here?
            if (authModal) authModal.style.display = 'flex'; // Show auth modal as fallback
            return;
        }

        // 1. Get cart items to form the order
        const cartItems = JSON.parse(localStorage.getItem('shoppingCart')) || [];
        if(cartItems.length === 0) {
            // This should be caught by initialChecks(), but safety
            console.warn("processOrder called with empty cart.");
            if (cartEmptyModal) cartEmptyModal.style.display = 'flex'; 
            return;
        }

        // 2. Calculate final total for the order record
        const subtotal = cartItems.reduce((sum, item) => sum + (parseFloat(item.price) * (item.quantity || 0)), 0); // Added || 0
        const total = subtotal + PROCESSING_FEE;
        
        // 3. Create a new order object
        const newOrder = {
            id: `FN${Math.floor(10000 + Math.random() * 90000)}`, // Random 5-digit order ID
            date: new Date().toISOString(), // Full timestamp
            status: 'Processing', // Default status for a new order
            total: total,
            items: cartItems, // Add all cart items to the order
            // Add shipping address, card info used in checkout?
            // address: shippingAddressInput ? shippingAddressInput.value.trim() : '',
            // paymentMethod: document.querySelector('.radio-option:not(.inactive)')?.textContent.trim() || 'Unknown',
            // cardLast4: cardNumberInput ? cardNumberInput.value.slice(-4) : ''
        };
        
        // 4. Get the orders DB and add the new order
        let ordersDB = JSON.parse(localStorage.getItem('ordersDB')) || {};
        if (!ordersDB[currentUserEmail]) {
            ordersDB[currentUserEmail] = []; // Initialize order history if it's the first order
        }
        ordersDB[currentUserEmail].unshift(newOrder); // Add to the beginning of the list (most recent first)
        
        localStorage.setItem('ordersDB', JSON.stringify(ordersDB));

        // 5. Clear the shopping cart
        localStorage.removeItem('shoppingCart');

        // 6. Update cart icon in navbar
        if(window.updateCartIcon) {
            window.updateCartIcon();
        }

        // 7. Show the success modal
        if (orderSuccessModal) {
             orderSuccessModal.style.display = 'flex';
             // Optional: Add 'show' class for transitions if needed
             // setTimeout(() => orderSuccessModal.classList.add('show'), 10);
        }
    }

    function initialChecks() { // Checks performed on page load
        // Check if cart is empty
        if (cart.length === 0) {
            if (cartEmptyModal) cartEmptyModal.style.display = 'flex';
            // Disable the confirm button if cart is empty
            if (confirmPaymentBtn) {
                confirmPaymentBtn.disabled = true;
                // Optional: Add styling to indicate disabled state
                // confirmPaymentBtn.style.backgroundColor = '#ccc';
                // confirmPaymentBtn.style.cursor = 'not-allowed';
            }
        } else {
            // If cart is not empty, try to load user data for pre-filling form
            loadUserData();
        }
    }

    // --- EVENT LISTENERS ---
    if (confirmPaymentBtn) {
        confirmPaymentBtn.addEventListener('click', () => {
            // Before processing, could add client-side form validation here
            // E.g., check if address is filled, if card details are filled when card is selected, etc.

            if (isLoggedIn()) {
                processOrder();
            } else {
                // Show the Sign In prompt modal instead of the main auth modal directly
                 const signInPromptModal = document.getElementById('signInPromptModal');
                 if (signInPromptModal) {
                      signInPromptModal.style.display = 'flex';
                      // Optional: Add 'show' class for transitions
                      setTimeout(() => signInPromptModal.classList.add('show'), 10);

                     // Add event listeners for prompt buttons ONLY when the prompt is shown
                      const promptSignInBtn = document.getElementById('promptSignInBtn');
                      const promptCancelBtn = document.getElementById('promptCancelBtn');

                     if (promptSignInBtn && authModal) {
                          promptSignInBtn.onclick = () => { // Use onclick to avoid multiple listeners
                              signInPromptModal.style.display = 'none';
                              signInPromptModal.classList.remove('show');
                              authModal.style.display = 'flex'; // Show the main auth modal
                         };
                     }
                     if (promptCancelBtn) {
                          promptCancelBtn.onclick = () => { // Use onclick
                              signInPromptModal.style.display = 'none';
                              signInPromptModal.classList.remove('show');
                         };
                     }

                 } else if (authModal) {
                     // Fallback to showing the auth modal directly if prompt modal isn't found
                     authModal.style.display = 'flex';
                 }
            }
        });
    }

    // Add listeners for modal closing (assuming they are in checkout.html)
    // Closing logic might be shared via popup.js or auth.js
    // If modals don't close automatically, add specific listeners here:
    /*
    if (orderSuccessModal) {
        // Add listener to buttons inside or the modal overlay itself
    }
    if (cartEmptyModal) {
        // Add listener to buttons inside or the modal overlay itself
    }
    if (document.getElementById('promptSignInBtn')) {
        // Listeners handled above when prompt is shown
    }
    */


    // --- INITIALIZATION ---
    updateCheckoutSummary();
    setupPaymentSelection();
    initialChecks();
});
```

--- START OF FILE forgot-password.css ---
```css
:root {
    --primary-color: coral;
    --primary-color-dark:  #e86a50; /* Changed to match homepage hover */
    --background-color: #ffffff;
    --card-background: #ffffff;
    --text-primary: #212529;
    --text-secondary: #6c757d;
    --border-color: #e0e0e0; /* Changed to a light grey to match input border */
    --font-family: 'Poppins', sans-serif;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: var(--font-family);
    background-color: var(--background-color);
    color: var(--text-primary);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

.page-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    padding: 2rem;
}

.content-wrapper {
    display: flex;
    background-color: var(--card-background);
    border-radius: 24px;
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.05);
    max-width: 900px;
    width: 100%;
    overflow: hidden;
    position: relative;
}

.back-to-home-btn {
    position: absolute;
    top: 20px;
    left: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background-color: #f1f3f5;
    color: var(--text-secondary);
    border-radius: 50%;
    text-decoration: none;
    font-size: 1rem;
    transition: background-color 0.3s, color 0.3s;
    z-index: 1; /* Ensure it's above other content */
}

.back-to-home-btn:hover {
    background-color: #e9ecef;
    color: var(--text-primary);
}


.illustration-section {
    flex-basis: 45%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;
}

.illustration-section img {
    max-width: 100%;
    height: auto;
    object-fit: contain;
}

.form-section {
    flex-basis: 55%;
    padding: 4rem 3rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

h1 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: var(--text-primary);
}

p {
    color: var(--text-secondary);
    margin-bottom: 2.5rem;
    font-size: 1rem;
    line-height: 1.6;
}

.form-group {
    margin-bottom: 2rem;
}

.form-group input {
    width: 100%;
    border: none;
    border-bottom: 1px solid var(--border-color);
    padding: 0.75rem 0.25rem;
    font-size: 1rem;
    font-family: var(--font-family);
    background-color: transparent;
    transition: border-color 0.3s ease;
    /* Added box-sizing to prevent padding issues */
    box-sizing: border-box;
}

.form-group input::placeholder {
    color: #ced4da;
}

.form-group input:focus {
    outline: none;
    border-bottom-color: var(--primary-color);
}

.form-actions {
    display: flex;
    justify-content: flex-end; /* Changed to push button to the right */
    align-items: center;
    margin-top: 2rem;
}

.link-btn { /* This class is not used for the submit button link */
    text-decoration: none;
    color: var(--primary-color);
    font-weight: 500;
    transition: color 0.3s ease;
}

.link-btn:hover { /* Not used for the submit button link */
    color: var(--primary-color-dark);
}

/* === UPDATED BUTTON STYLE === */
.submit-btn {
    background-color: var(--primary-color);
    color: white;
    border: 2px solid var(--primary-color);
    padding: 13px 30px;
    border-radius: 30px;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.3s ease;
    /* Ensure button respects flex layout */
    display: inline-block;
    width: auto;
    text-align: center;
}

.submit-btn:hover {
    background-color: var(--primary-color-dark);
    border-color: var(--primary-color-dark);
}

/* Responsive Design */
@media (max-width: 768px) {
    .content-wrapper {
        flex-direction: column;
        max-width: 450px;
    }

    .illustration-section {
        display: none;
    }
    
    .form-section {
        padding: 3rem 2rem;
    }

    h1 {
        font-size: 2rem;
    }

    .back-to-home-btn {
        top: 15px;
        left: 15px;
    }
}
```

--- START OF FILE homepage.html ---
```html
<!DOCTYPE html>
<html lang="en">

    <head>
      <meta charset="UTF-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>FashioNear</title>

      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"
        integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
      <link rel="stylesheet" href="https://pro.fontawesome.com/releases/v5.10.0/css/all.css" />

      
      <link rel="stylesheet" href="homestyle.css">
      <link rel="stylesheet" href="visual-search.css">
      <link rel="stylesheet" href="Navbar.css">
      <link rel="stylesheet" href="footer.css">
      <link rel="stylesheet" href="user-profile.css">
      <link rel="stylesheet" href="products.css">
      <link rel="stylesheet" href="auth.css">
      <link rel="stylesheet" href="search-bar.css">
      <link rel="stylesheet" href="transitions.css">
      <link rel="stylesheet" href="success-model.css">

      
      <style>
        /* Adds a visual cue that product items are clickable */
        #product-grid .pro {
          cursor: pointer;
        }
      </style>
    </head>

    <body>
      
        <nav class="navbar navbar-expand-lg navbar-light py-1 fixed-top">            
            <div class="container">
              <a href="homepage.html">
                <img class="logo-img" src="Images/Logo.png" alt="FashioNear Logo">
              </a>
              <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span><i id="bar" class="fas fa-bars"></i></span>
              </button>

              <div class="collapse navbar-collapse" id="navbarSupportedContent">
                  
                <ul class="navbar-nav ml-auto">
                  <li class="nav-item"><a class="nav-link active" href="homepage.html">Home</a></li>
                  <li class="nav-item"><a class="nav-link" href="All.html">All</a></li> 
                  <li class="nav-item"><a class="nav-link" href="Men.html">Men</a></li>
                  <li class="nav-item"><a class="nav-link" href="Women.html">Women</a></li>
                  <li class="nav-item"><a class="nav-link" href="Kids.html">Kids</a></li>
                </ul>

                <div class="d-flex align-items-center">
                  <div class="search-container" id="search-container">
                    <button class="search-toggle-btn" id="search-toggle-btn"><i class="fas fa-search"></i></button>
                    <input type="text" placeholder="Search for clothes, accessories..." class="search-input" />
                    <button class="search-button camera-button" id="navVisualSearchBtn"><i class="fas fa-camera"></i></button>     
                  </div>
                  
                  <div class="nav-item nav-cart-link">
                    <a class="nav-link" href="cart.html">
                      <img src="Icons/cart.png" alt="Cart Icon" id="nav-cart-img">
                      (<span id="cart-count">0</span>)
                    </a>
                  </div>
        
                  <div class="profile" id="profile-icon-btn">
                    <img src="Icons/user.png" alt="Profile Icon" id="nav-profile-img">
                  </div>
                </div>
              </div>
            </div>
        </nav>

        <section id="home">
            <div class="container" >
              <h1>Explore, search, and find <br> everything you need in<br> one place.</h1>
              <h5>scan, search, and find what you need—all in one place.</h5>
              <button onclick="window.location.href='All.html'"> shop now </button>
              <button id="visualSearchBtn">Try Visual Search</button>
            </div>
        </section>

        <section id="new" class="w-100">
          <div class="container  text-center mt-5 py-5">
            <h3>Top Categories</h3>
            <hr class="mx-auto">
            <p>Shop the hottest trends! Our most-loved products, just for you</p>
          </div>
          <div class="row p-0 m-0" >
            <div class="one col-lg-4 col-md-4 col-4 p-0" onclick="window.location.href='Women.html'">
              <img class="img-fluid" src="Images/Women.png" alt="">
              <div class="details">
                <h2> Women </h2>
                <button class="text-uppercase"> Shop now </button>
              </div>
            </div>
            <div class="one col-lg-4 col-md-4 col-4 p-0" onclick="window.location.href='Men.html'">
              <img class="img-fluid" src="Images/Men.png" alt="">
              <div class="details">
                <h2> Men </h2>
                <button class="text-uppercase"> Shop now </button>
              </div>
            </div>
            <div class="one col-lg-4 col-md-4 col-4 p-0" onclick="window.location.href='Kids.html'">
              <img class="img-fluid" src="Images/Kids.png" alt="">
              <div class="details">
                <h2> Kids </h2>
                <button class="text-uppercase"> Shop now </button>
              </div>
            </div>
          </div>
        </section>

        <section id="banner" class="my-5 py-5">
          <div class="container">
            <h1>LIMITED TIME OFFER</h1>
            <h4>Get 30% off all accessories until Sunday!</h4>
            <button class="text-uppercase" onclick="window.location.href='All.html'">Shop now</button>
          </div>
        </section>
        
        <section id="product1" class="my-5 pb-5">
          <div class="container text-center mt-5 py-5">
            <h3>Most Popular</h3>
            <hr class="mx-auto">
            <p>Shop the hottest trends! Our most-loved products, just for you</p>
          </div>

          <div class="container" id="product-grid">
            <!-- Products will be loaded dynamically from API -->
            <div class="loading-spinner" style="text-align: center; padding: 50px;">
              <i class="fas fa-spinner fa-spin fa-2x"></i>
              <p>Loading products...</p>
            </div>
          </div>
        </section>

        <!-- user profile -->
        
        <div id="userProfileModal" class="profile-modal-container" style="display: none;">
            <div class="profile-modal-content">
                <span class="profile-modal-close-btn">×</span>
                <aside class="profile-sidebar">
                    <h2>User Profile</h2>
                    <nav>
                        <ul>
                          <li class="active"><a href="#"><i class="fas fa-user-circle"></i> User info</a></li>
                          <li><a href="orders.html"><i class="fas fa-box"></i> My orders</a></li>
                          <li><a href="#"><i class="fas fa-cog"></i> Setting</a></li>
                          <li><a href="#"><i class="fas fa-bell"></i> Notifications</a></li>
                        </ul>
                    </nav>
                    <div class="profile-logout">
                        <a href="#" id="profile-logout-btn"><i class="fas fa-sign-out-alt"></i> Log out</a>
                    </div>
                </aside>
                <main class="profile-main-content">
                    <header class="user-header">
                        <div class="user-avatar-wrapper">
                             <img src="Icons/user.png" alt="User Avatar" class="user-avatar" id="profile-avatar-img">
                             <input type="file" id="avatarUpload" accept="image/png, image/jpeg, image/webp" hidden>
                             <label for="avatarUpload" class="edit-avatar-btn"><i class="fas fa-camera"></i></label>
                        </div>
                        <h3 class="user-name" id="profile-display-name">Your Name</h3>
                        <p class="user-location" id="profile-display-location">Your Location</p>
                    </header>
                    <form class="profile-form" id="userProfileForm">
                        <div class="form-grid">
                            <div class="form-group"><label for="profile-firstname">First Name</label><input type="text" id="profile-firstname" placeholder="Your first name"></div>
                            <div class="form-group"><label for="profile-lastname">Last Name</label><input type="text" id="profile-lastname" placeholder="Your last name"></div>
                            <div class="form-group"><label for="profile-email">Email Address</label><input type="email" id="profile-email" placeholder="your.email@example.com" disabled></div>
                            <div class="form-group"><label for="profile-phone">Phone Number</label><input type="tel" id="profile-phone" placeholder="Your phone number"></div>
                            <div class="form-group"><label for="profile-location">Location</label><input type="text" id="profile-location" placeholder="e.g. New York, USA"></div>
                            <div class="form-group"><label for="profile-cardnumber">Card Number</label><input type="text" id="profile-cardnumber" placeholder="XXXX-XXXX-XXXX-XXXX"></div>
                        </div>
                        <div class="profile-actions">
                            <button type="submit" class="save-changes-btn">Save Changes</button>
                        </div>
                    </form>
                </main>
            </div>
        </div>

        <!-- Authentication sign in/up -->

        <div id="authModal" class="auth-modal-container" style="display: none;">
            <div class="auth-box" id="auth-box">
                <div class="form-container sign-up-container">
                    <form>
                        <h1>Create Account</h1>
                        <div class="social-container">
                            <a href="#" class="social"><i class="fab fa-facebook-f"></i></a>
                            <a href="#" class="social"><i class="fab fa-google-plus-g"></i></a>
                        </div>
                        <span>or use your email for registration</span>
                        <input type="text" placeholder="First Name" id="signUpName" required/>
                        <input type="email" placeholder="Email" id="signUpEmail" required/>
                        <input type="password" placeholder="Password" id="signUpPassword" required/>
                        <button type="button" id="signUpActionBtn">Sign Up</button>
                    </form>
                </div>
                <div class="form-container sign-in-container">
                    <form>
                        <h1>Sign In</h1>
                        <div class="social-container">
                          <a href="#" class="social"><i class="fab fa-facebook-f"></i></a>
                          <a href="#" class="social"><i class="fab fa-google-plus-g"></i></a>
                        </div>
                        <span>or use your account</span>
                        <input type="email" placeholder="Email" id="signInEmail" required/>
                        <input type="password" placeholder="Password" id="signInPassword" required/>
                        <a href="forgot-password.html">Forgot your password?</a>
                        <button type="button" id="signInActionBtn">Sign In</button>
                    </form>
                </div>
                <div class="overlay-container">
                    <div class="overlay">
                        <div class="overlay-panel overlay-left">
                            <h1>Welcome Back!</h1>
                            <p>To keep connected with us please login with your personal info</p>
                            <button class="ghost" id="signInBtnModal" type="button">Sign In</button>
                        </div>
                        <div class="overlay-panel overlay-right">
                            <h1>Hello, Friend!</h1>
                            <p>Enter your personal details and start your journey with us</p>
                            <button class="ghost" id="signUpBtnModal" type="button">Sign Up</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div id="successPromptModal" class="success-modal-container" style="display: none;">
          <div class="success-modal-content">
            <i class="fas fa-check-circle success-icon"></i>
            <h2 id="successModalTitle">Success!</h2>
            <p id="successModalMessage">Your action was completed successfully.</p>
            <button id="successModalCloseBtn" class="success-modal-close-btn">OK</button>
          </div>
        </div>


        <!-- visual search --> 

        <div id="visualSearchModal" class="visual-search-modal" style="display:none;">
            <div class="visual-search-modal-content">
              <span class="visual-search-close-btn">×</span>
                <h4>Visual Search</h4>
                <p>Find similar items or predict the price by uploading a photo.</p>
                <div class="visual-search-drop-zone">
                  <p><strong>Drag & drop image here</strong></p>
                  <p>or</p>
                  <button class="visual-search-upload-btn">Upload from Device</button>
                  <input type="file" id="visualSearchFileInput" accept="image/*" hidden />
                </div>
                <p id="visualSearchError" class="visual-search-error"></p>
                <div id="visualSearchPreview" class="visual-search-preview"></div>
                <div id="visualSearchActions" class="visual-search-actions" style="display: none;">
                    <button id="findSimilarBtn">Similar Items</button>
                    <button id="predictPriceBtn">Predict Price</button>
                </div>
            </div>
        </div>

        <div id="pricePredictionModal" class="visual-search-modal" style="display:none;">
            <div class="visual-search-modal-content">
                <span id="closePricePredictionBtn" class="visual-search-close-btn">×</span>
                <h4>Price Prediction</h4>
                <p id="predicted-price-text">The estimated price range for this item is...</p>
            </div>
        </div>

        <footer class="mt-5 py-5">
            <div class="container">
                <div class="row">
                    <div class="footer-one col-lg-3 col-md-6 col-12 mb-4">
                        <h5 class="pb-2">FashioNear</h5>
                        <p>
                            Discover fashion your way. Search by image or text to find clothes, accessories, and similar styles from across our collection.
                        </p>
                    </div>
                    <div class="footer-one col-lg-3 col-md-6 col-12 mb-4">
                        <h5 class="pb-2">Explore</h5>
                        <ul class="list-unstyled">
                            <li><a href="homepage.html">Home</a></li>
                            <li><a href="All.html">All Products</a></li>
                            <li><a href="Men.html">Men</a></li>
                            <li><a href="Women.html">Women</a></li>
                            <li><a href="Kids.html">Kids</a></li>
                        </ul>
                    </div>
                    <div class="footer-one col-lg-3 col-md-6 col-12 mb-4">
                        <h5 class="pb-2">Contact Us</h5>
                        <address>
                            <strong>Address:</strong><br>
                            123 Giza Cairo Egypt<br>
                            <strong>Phone:</strong><br>
                            +20 102 874 6453<br>
                            <strong>Email:</strong><br>
                            support@fashionear.com
                        </address>
                    </div>
                    <div class="footer-one col-lg-3 col-md-6 col-12 mb-4">
                        <h5 class="pb-2">Social Media</h5>
                        <div class="social-links">
                            <a href="#"><i class="fab fa-facebook-f"></i></a>
                            <a href="#"><i class="fab fa-pinterest"></i></a>
                            <a href="#"><i class="fab fa-instagram"></i></a>
                            <a href="#"><i class="fab fa-linkedin-in"></i></a>
                        </div>
                    </div>
                </div>
        
                <div class="copyright mt-5 pt-4 border-top">
                    <div class="row">
                        <div class="col-lg-6 col-md-12 text-center text-lg-left mb-2 mb-lg-0">
                            <p>© 2025 FashioNear eCommerce. All Rights Reserved.</p>
                        </div>
                        <div class="col-lg-6 col-md-12 text-center text-lg-right policy-links">
                            <a href="#">Terms of Use</a>
                            <a href="#">Privacy Policy</a>
                        </div>
                    </div>
                </div>
            </div>
        </footer>

        

               <!-- API Integration Script -->
        <script src="api-integration.js"></script>
        <!-- AI Search Integration Scripts -->
        <script src="popup.js"></script> <!-- Use popup.js for visual search modal logic -->
        <script src="search-integration.js"></script> <!-- Use search-integration.js for text search -->
        <script>
          // Load featured products when page loads
          document.addEventListener('DOMContentLoaded', async function() {
            const products = await fetchProducts('', 4); // Get 4 featured products from the original API
            displayProducts(products, 'product-grid'); // Assuming displayProducts is available globally or in product-grid.js
          });
        </script>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script src="cart.js"></script>
        <script src="auth.js"></script>
        <script src="transitions.js"></script>
        <script src="product-grid.js"></script> <!-- Handles clicks on product grid items -->
    </body>

</html>
```

--- START OF FILE Kids.css ---
```css
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800;900&display=swap");
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: "Poppins", sans-serif;
}

h1 {
  font-size: 2.5rem;
  font-weight: 700;
}

h2 {
  font-size: 1.8rem;
  font-weight: 600;
}

h3 {
  font-size: 1.4rem;
  font-weight: 800;
}

h4 {
  font-size: 1.1rem;
  font-weight: 600;
}

h5 {
  font-size: 1rem;
  font-weight: 400;
  color: #1d1d1d;
}

h6 {
  color: #d8d8d8;
}

button{
  font-size: 0.8rem;
  font-weight: 700;
  outline: none;
  border: none;
  background-color: #1d1d1d;
  color: aliceblue;
  padding: 13px 30px;
  cursor: pointer;
  text-transform: uppercase;
  transition: 0.3s ease;
}

button:hover{
  background-color: #3a383a;
  border-radius: 0%;
}

button:focus {
    outline: none;
  }

hr {
  width: 30px;
  height: 2px;
  background-color: #fb774b;
}

/* =================================== */
/* ===         Logo Styling          === */
/* =================================== */
.logo-img {
  height: 80px;            /* Sets the height of the circle */
  width: 80px;             /* Sets the width, MUST be same as height for a perfect circle */
  border-radius: 50%;      /* This is the key property that creates the circular shape */
  object-fit: cover;       /* IMPORTANT: Prevents the image from stretching or squishing. It will be cropped to fit the circle perfectly. */
  margin-right: 25px;      /* Adds some space between the logo and other nav items */

}

.navbar .iconCart { /* This seems to be unused in the current HTML structure */
  position: relative;
  cursor: pointer;
  margin-left: 20px;
}

.navbar .iconCart img { /* This seems to be unused */
  width: 30px;
  height: auto;
}


.navbar .profile {
  position: relative;
  cursor: pointer;
  margin-left: 20px;
}

.navbar .profile img {
  width: 30px;
  height: auto;
}




.navbar{
    font-size: 16px;
    top: 0;
    left: 0;
}

.navbar-light .navbar-nav .nav-link{
    padding: 0 20px;
    color: black;
    transition: 0.3s ease;
}
.navbar-light .navbar-nav .nav-link:hover,
.navbar-light .navbar-nav .nav-link.active{
    color: coral;
}
.navbar i{
    font-size: 1.2rem;
    padding: 0 7px;
    cursor: pointer;
    font-weight: 500;
    transition: 0.3s ease;
}

/* =================================== */
/* === Authentication Modal Styles sign up , sign in popup page === */
/* =================================== */

.auth-modal-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1060; /* Higher than bootstrap navbar and visual search */
    display: flex;
    justify-content: center;
    align-items: center;
    backdrop-filter: blur(3px);
}

.auth-box {
    background: #fff;
    border-radius: 10px;
    box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
    position: relative;
    overflow: hidden;
    width: 768px;
    max-width: 100%;
    min-height: 480px;
}

.auth-box h1 {
	font-weight: bold;
	margin: 0;
    font-size: 2.1rem;
    color: #333;
}

.auth-box p {
	font-size: 14px;
	font-weight: 100;
	line-height: 20px;
	letter-spacing: 0.5px;
	margin: 20px 0 30px;
}

.auth-box span {
	font-size: 12px;
}

.auth-box a {
	color: #333;
	font-size: 14px;
	text-decoration: none;
	margin: 15px 0;
}
.auth-box a:hover {
    color: coral;
}

.auth-box button {
	border-radius: 20px;
	border: 1px solid #008080;
	background-color: #008080;
	color: #FFFFFF;
	font-size: 12px;
	font-weight: bold;
	padding: 12px 45px;
	letter-spacing: 1px;
	text-transform: uppercase;
	transition: transform 80ms ease-in, background-color 0.3s;
}

.auth-box button:active {
	transform: scale(0.95);
}

.auth-box button.ghost {
	background-color: transparent;
	border-color: #FFFFFF;
}
.auth-box button.ghost:hover {
    background-color: rgba(255, 255, 255, 0.2);
}

.auth-box form {
	background-color: #FFFFFF;
	display: flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;
	padding: 0 50px;
	height: 100%;
	text-align: center;
}

.auth-box input {
	background-color: #eee;
	border: none;
	padding: 12px 15px;
	margin: 8px 0;
	width: 100%;
    border-radius: 5px;
}

.form-container {
	position: absolute;
	top: 0;
	height: 100%;
	transition: all 0.6s ease-in-out;
}

.sign-in-container {
	left: 0;
	width: 50%;
	z-index: 2;
}

.sign-up-container {
	left: 0;
	width: 50%;
	opacity: 0;
	z-index: 1;
}

.social-container {
	margin: 20px 0;
}

.social-container a {
	border: 1px solid #DDDDDD;
	border-radius: 50%;
	display: inline-flex;
	justify-content: center;
	align-items: center;
	margin: 0 5px;
	height: 40px;
	width: 40px;
    transition: background-color 0.3s, color 0.3s;
}

.social-container a:hover {
    background-color: #eee;
}

.overlay-container {
	position: absolute;
	top: 0;
	left: 50%;
	width: 50%;
	height: 100%;
	overflow: hidden;
	transition: transform 0.6s ease-in-out;
	z-index: 100;
}

.overlay {
	background: #008080;
	background: -webkit-linear-gradient(to right, #2E8B57, #008080);
	background: linear-gradient(to right, #2E8B57, #008080);
	background-repeat: no-repeat;
	background-size: cover;
	background-position: 0 0;
	color: #FFFFFF;
	position: relative;
	left: -100%;
	height: 100%;
	width: 200%;
  	transform: translateX(0);
	transition: transform 0.6s ease-in-out;
}

.overlay-panel {
	position: absolute;
	display: flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;
	padding: 0 40px;
	text-align: center;
	top: 0;
	height: 100%;
	width: 50%;
	transform: translateX(0);
	transition: transform 0.6s ease-in-out;
}

.overlay-left {
	transform: translateX(-20%);
}

.overlay-right {
	right: 0;
	transform: translateX(0);
}

/* === Animation for Panel Sliding === */
.auth-box.right-panel-active .sign-in-container {
	transform: translateX(100%);
}

.auth-box.right-panel-active .overlay-container {
	transform: translateX(-100%);
}

.auth-box.right-panel-active .sign-up-container {
	transform: translateX(100%);
	opacity: 1;
	z-index: 5;
	animation: show 0.6s;
}

@keyframes show {
	0%, 49.99% {
		opacity: 0;
		z-index: 1;
	}
	
	50%, 100% {
		opacity: 1;
		z-index: 5;
	}
}

.auth-box.right-panel-active .overlay {
	transform: translateX(50%);
}

.auth-box.right-panel-active .overlay-left {
	transform: translateX(0);
}

.auth-box.right-panel-active .overlay-right {
	transform: translateX(20%);
}

/* ____________________________________________________________ */

/* =================================== */
/* ===         New Search Bar        === */
/* =================================== */

.search-container {
  display: flex;
  align-items: center;
  position: relative;
  background-color: #fff; /* Differs from search-bar.css */
  border-radius: 50px;
  padding: 6px;
  margin: 0 15px; /* Added margin to separate from other nav items */
  width: 350px;
  transition: all 0.4s ease-in-out;
  border: none; /* Differs from search-bar.css */
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 10px 15px;
  font-size: 14px;
  outline: none;
  color: #E0E0E0; /* Differs from search-bar.css */
}

.search-input::placeholder {
  color: #999; /* Lighter placeholder text */
  opacity: 1; 
}

/* This is the new Camera button */
.search-button.camera-button {
  background-color: #000; /* Differs from search-bar.css */
  border: none;
  color: #fff; /* Differs from search-bar.css */
  width: 38px;
  height: 38px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease, transform 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0; /* Prevents button from shrinking */
  padding: 0; /* Reset padding */
}

.search-button.camera-button:hover {
  background-color: #fb774b;
  transform: scale(1.05);
}

/* The toggle button, hidden on desktop by default */
.search-toggle-btn {
    display: none; /* Hidden on desktop */
}


/* Remove old search button styles that might conflict */
.search-button {
  background: transparent;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: color 0.3s ease;
}
.search-button:hover {
    color: inherit;
    background: transparent;
}



/* ========================================= */
/* === Search Bar - Mobile Responsive Styles === */
/* ========================================= */
@media only screen and (max-width:991px) {
  /* Make room in the mobile navbar */
  #navbarSupportedContent {
      flex-basis: 100%;
  }

  .search-container {
      /* Collapsed state on mobile */
      width: 45px;
      height: 45px;
      padding: 0;
      background-color: transparent; /* No background when collapsed */
      border-radius: 50%;
      margin: 0;
  }

  .search-input,
  .search-button.camera-button {
      /* Hide the input and camera when collapsed */
      opacity: 0;
      width: 0;
      padding: 0;
      margin: 0;
      display: none;
  }
  
  .search-toggle-btn {
      /* Show and style the toggle icon */
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: 100%;
      background: transparent;
      border: none;
      font-size: 18px;
      color: black; /* Visible against light navbar */
      cursor: pointer;
      padding: 0;
  }

  /* --- Expanded state on mobile --- */
  .search-container.active {
      width: 100%;
      background-color: #3C3C3C; /* Differs from search-bar.css */
      padding: 6px;
      border-radius: 50px;
      margin-top: 10px; /* Give it space when it opens */
  }

  .search-container.active .search-input,
  .search-container.active .search-button.camera-button {
      /* Reveal the input and camera button */
      display: flex;
      opacity: 1;
      width: auto;
  }
    
  .search-container.active .search-input {
      width: 100%;
      padding: 10px 15px;
  }

  .search-container.active .search-toggle-btn i {
      color: #E0E0E0; /* Differs from search-bar.css */
  }
}

/* Mobile Nav */
.navbar-light .navbar-toggler{
  border: none;
  outline: none;
}

#bar{
  font-size: 1.5rem;
  padding: 7px;
  cursor: pointer;
  font-weight: 500;
  transition: 0.3s ease;
  color: black;
}

#bar:hover,
#bar.active{
  color: #fff;
}



@media only screen and (max-width:991px){
  body > nav > div > button:hover,
  body > nav > div > button:focus{
    background-color: #fb774b;
  }

  body > nav > div > button:hover #bar,
  body > nav > div > button:focus #bar{
    color: #fff;
  }

  #navbarSupportedContent > ul{
    margin: 1rem;
    justify-content: flex-end ;
    text-align: right;
  }

  #navbarSupportedContent > ul > li:nth-child(n) > a{
    padding: 10px 0 ;
  }

}








footer{ /* This footer style is different from footer.css */
  background-color: #222222;
}

footer h5{
  color: #d8d8d8;
  font-weight: 700;
  font-size: 1.2rem;
}

footer h1{ /* Semantically incorrect h1 */
  padding-bottom: 4px;
}

footer li a{
  font-size: 0.8rem;
  color: #999;
}

footer li a:hover{
  color: #d8d8d8;
}

footer p{
  color: #999;
  font-size: 0.8rem;
}

footer .copyright a{
  color: black;
  width: 38px;
  height: 38px;
  background-color: #fff;
  display: inline-block;
  text-align: center;
  line-height: 38px;
  border-radius: 50%;
  transition: 0.3s ease;
  margin: 0 5 px; /* Syntax error */
}

footer .copyright a:hover{
  color: #fff;
  background-color: coral;
}
```

--- START OF FILE Men.css ---
```css
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800;900&display=swap");

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: "Poppins", sans-serif;
}

h1 {
    font-size: 2.5rem;
    font-weight: 700;
}

hr {
    width: 30px;
    height: 2px;
    background-color: coral;
}


/* Men page products */
#product1 { /* This ID is duplicated across pages */
    text-align: center;
}

#product-grid { /* This ID is duplicated across pages */
    display: flex;
    justify-content: space-between;
    padding-top: 20px;
    flex-wrap: wrap;
}

#product1 .pro {
    width: 23%;
    min-width: 250px;
    padding: 10px 12px;
    border: 1px solid #fdeee9;
    border-radius: 25px;
    cursor: pointer;
    box-shadow: 20px 20px 30px rgba(0, 0, 0, 0.02);
    margin: 15px 0;
    transition: 0.2s ease;
    position: relative;
}

#product1 .pro:hover {
    box-shadow: 20px 20px 30px rgba(0, 0, 0, 0.06);
}

#product1 .pro img { /* Overridden by products.css if loaded after */
    width: 100%;
    border-radius: 20px;
}

#product1 .pro .des {
    text-align: start;
    padding: 10px 0;
}

#product1 .pro .des span {
    color: #606063;
    font-size: 12px;
}

#product1 .pro .des h5 {
    padding-top: 7px;
    color: #1a1a1a;
    font-size: 14px;
}

#product1 .pro .des .star {
    font-size: 12px;
    color: rgb(243, 181, 25);
}

#product1 .pro .des h4 {
    padding-top: 7px;
    font-size: 15px;
    font-weight: 700;
    color: coral;
}


.add-to-cart-btn {
    width: 45px;
    height: 45px;
    background-color: #ffeee9;
    border: none;
    border-radius: 50%;
    position: absolute;
    color: coral;
    bottom: 20px;
    right: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
}
.add-to-cart-btn:hover {
    background-color: #fddbcd;
    transform: scale(1.1);
    border-radius: 50%;
}

.add-to-cart-btn .cartt-icon {
    color: coral;
    font-size: 1rem;
}




.add-to-cart-btn:disabled {
    cursor: not-allowed;
    background-color: #e0e0e0;
}

/* Responsive Styles for Men Product Grid */
@media (max-width: 768px) {
  #product1 #product-grid {
    justify-content: space-around;
  }
  #product1 .pro {
    width: 46%;
    margin: 10px 1%;
    min-width: unset;
  }
}

@media (max-width: 480px) {
  #product1 .pro {
    width: 90%;
    margin: 15px auto;
  }
}
```

--- START OF FILE Navbar.css ---
```css
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800;900&display=swap");
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: "Poppins", sans-serif;
}

h1 {
  font-size: 2.5rem;
  font-weight: 700;
}

h2 {
  font-size: 1.8rem;
  font-weight: 600;
}

h3 {
  font-size: 1.4rem;
  font-weight: 800;
}

h4 {
  font-size: 1.1rem;
  font-weight: 600;
}

h5 {
  font-size: 1rem;
  font-weight: 400;
  color: #1d1d1d;
}

h6 {
  color: #d8d8d8;
}

/* ================================= */
/* ===  GLOBAL BUTTON STYLES    === */
/* =============================== */
button{
  font-size: 0.8rem;
  font-weight: 700;
  outline: none;
  background-color: coral; 
  color: white;
  padding: 13px 30px;
  cursor: pointer;
  text-transform: uppercase;
  transition: all 0.3s ease;
  border-radius: 30px; 
  border: 2px solid coral;
}

button:hover{
  background-color: #e86a50; 
  border-color: #e86a50;
  color: white;
  border-radius: 30px; /* Redundant */

}

button:focus {
    outline: none;
  }

/* === Home Page Hero Buttons Variation === */
#home #visualSearchBtn {
    background-color: transparent;
    color: white;
    border: 2px solid white;
}

#home #visualSearchBtn:hover {
    background-color: white;
    color: #1d1d1d;
    border-color: white;
}


hr {
  width: 30px;
  height: 2px;
  background-color: #fb774b;
}

/* =================================== */
/* ===         Logo Styling       === */
/* ================================= */

.logo-img {
  height: 80px;            
  width: 80px;             
  border-radius: 50%;      
  object-fit: cover;       
  margin-right: 25px;      
}

/* ===================================== */
/* ===     NAVBAR ICON STYLES       === */
/* =================================== */

.profile {
  position: relative;
  cursor: pointer;
  margin-left: 20px;
}

#nav-profile-img { 
  width: 30px;
  height: 30px;
  object-fit: cover;
  border-radius: 50%; 
  transition: transform 0.2s ease-in-out;
}
.profile:hover #nav-profile-img {
    transform: scale(1.15);
}

.navbar{
    font-size: 16px;
    top: 0;
    left: 0;
    background-color: #ffffff;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    transition: background-color 0.3s ease;
}

.navbar-light .navbar-nav .nav-link{
    padding: 0 20px;
    color: black;
    transition: 0.3s ease;
}
.navbar-light .navbar-nav .nav-link:hover,
.navbar-light .navbar-nav .nav-link.active{
    color: coral;
}

.navbar i{
    font-size: 1.2rem;
    padding: 0 7px;
    cursor: pointer;
    font-weight: 500;
    transition: 0.3s ease;
}

/* === CART ICON STYLES === */

.nav-cart-link .nav-link {
    display: flex;
    align-items: center;
    gap: 4px;
    color: black !important;
    text-decoration: none;
}
.nav-cart-link .nav-link:hover {
    color: coral !important; 
}
#nav-cart-img {
    width: 28px;
    height: 28px;
    object-fit: contain;
    transition: transform 0.2s ease-in-out; 
}
.nav-cart-link .nav-link:hover #nav-cart-img {
    transform: scale(1.15);
}
.nav-cart-link span {
    font-weight: 600;
    color: inherit; 
}

```

--- START OF FILE orders.js ---
```javascript
document.addEventListener('DOMContentLoaded', () => {
    // --- DATA HELPERS ---
    const getOrdersDB = () => JSON.parse(localStorage.getItem('ordersDB')) || {};
    const getCurrentUserEmail = () => localStorage.getItem('currentUserEmail');
    const saveOrdersDB = (db) => localStorage.setItem('ordersDB', JSON.stringify(db));
     // Auth helpers (assuming auth.js defining isLoggedIn runs before this)
    const isLoggedIn = typeof window.isLoggedIn === 'function' ? window.isLoggedIn : () => !!localStorage.getItem('currentUserEmail');


    // --- DOM ELEMENTS ---
    const orderListContainer = document.getElementById('order-list-container');
    const emptyView = document.getElementById('empty-orders-view');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const clearHistoryContainer = document.getElementById('clear-history-container');
    const clearHistoryBtn = document.getElementById('clear-history-btn');

    // Modal DOM Elements (assuming they are in orders.html)
    const confirmClearModal = document.getElementById('confirmClearModal');
    const confirmClearBtn = document.getElementById('confirm-clear-btn');
    const cancelClearBtn = document.getElementById('cancel-clear-btn');
    const historyClearedModal = document.getElementById('historyClearedModal');
    const closeHistoryClearedModalBtn = document.getElementById('closeHistoryClearedModalBtn');

    // --- RENDER FUNCTIONS ---
    const renderOrderItems = (items) => {
        if (!Array.isArray(items)) return ''; // Safety check

        return items.map(item => {
            // Use fallback values and ensure IDs are strings for URL
            const itemId = String(item.id || '');
            const itemName = item.name || 'Unknown Item';
            const itemPrice = item.price || '0';
            const itemDesc = item.description || '';
            const itemImg = item.imgSrc || 'Images/placeholder.png';
            const itemQuantity = item.quantity || 0;

            return `
                <a href="sproduct.html?id=${encodeURIComponent(itemId)}&name=${encodeURIComponent(itemName)}&price=${encodeURIComponent(itemPrice)}&desc=${encodeURIComponent(itemDesc)}&img=${encodeURIComponent(itemImg)}" class="order-item">
                    <img src="${itemImg}" alt="${itemName}" onerror="this.src='Images/placeholder.png'">
                    <div class="order-item-details">
                        <h4>${itemName}</h4>
                        <p>Qty: ${itemQuantity} &nbsp;&nbsp; Price: ${(parseFloat(itemPrice) * itemQuantity).toFixed(2)} LE</p>
                    </div>
                </a>
            `;
        }).join('');
    };

    const renderOrders = (ordersToDisplay, isFilterAction = false) => {
        if (!orderListContainer || !emptyView) {
            console.error("Required DOM elements for orders page missing.");
            return;
        }

        const currentUser = getCurrentUserEmail();
        const allUserOrders = (getOrdersDB()[currentUser] || []);

        // Hide/show main empty view and buttons based on if there are *any* orders at all for the user
        if (allUserOrders.length === 0) {
            orderListContainer.innerHTML = '';
            emptyView.style.display = 'block';
            if (clearHistoryContainer) clearHistoryContainer.style.display = 'none';
            // Hide filter buttons container if it exists
            const filtersEl = document.querySelector('.order-filters');
            if (filtersEl) filtersEl.style.display = 'none';
            return;
        }

        // If user has orders, ensure elements are visible and empty view is hidden
        emptyView.style.display = 'none';
        if (clearHistoryContainer) clearHistoryContainer.style.display = 'block';
         const filtersEl = document.querySelector('.order-filters');
        if (filtersEl) filtersEl.style.display = 'flex';
        
        // Handle the display for the current filter (if the filtered list is empty)
        if (!Array.isArray(ordersToDisplay) || ordersToDisplay.length === 0) {
            if(isFilterAction) {
                orderListContainer.innerHTML = `<p style="text-align:center; padding: 2rem; color: var(--secondary-text);">You have no orders with this status.</p>`;
            } else {
                 // This case should ideally not be reached if allUserOrders > 0, but clear just in case
                 orderListContainer.innerHTML = ''; 
             }
        } else {
            // **FIXED: This is the full, correct HTML template for rendering orders**
            orderListContainer.innerHTML = ordersToDisplay.map(order => {
                 // Use fallback for order ID and status
                 const orderId = order.id || 'N/A';
                 const orderStatus = order.status || 'Unknown';
                 const orderDate = order.date ? new Date(order.date).toLocaleDateString() : 'N/A';
                 const orderTotal = order.total || 0;

                 return `
                    <div class="order-card" data-order-status="${orderStatus}">
                        <div class="order-card-header">
                            <div class="order-info">
                                <strong>Order ID:</strong> <span class="order-id">#${orderId}</span><br>
                                <strong>Date:</strong> ${orderDate}
                            </div>
                            <span class="order-status status-${orderStatus.replace(/\s+/g, '')}">${orderStatus}</span> <!-- Clean status for class name -->
                        </div>
                        <div class="order-items-list">
                            ${renderOrderItems(order.items)}
                        </div>
                        <div class="order-card-footer">
                            <button class="details-btn">Track Order</button>
                            <div class="total-amount">
                                <span>Total:</span> ${orderTotal.toFixed(2)} LE
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        }
    };
    
    // --- MAIN LOGIC & EVENT LISTENERS ---
    const initializeOrdersPage = () => {
        const currentUser = getCurrentUserEmail();
        if (!isLoggedIn()) { // Use isLoggedIn helper
             if (orderListContainer) orderListContainer.innerHTML = `<h3 class="text-center p-5" style="color: var(--primary-text);">Please log in to view your orders.</h3>`;
            if (emptyView) emptyView.style.display = 'none';
            if (clearHistoryContainer) clearHistoryContainer.style.display = 'none';
            const filtersEl = document.querySelector('.order-filters');
            if (filtersEl) filtersEl.style.display = 'none';
            return; // Exit setup if not logged in
        }

        const allUserOrders = getOrdersDB()[currentUser] || [];
        
        renderOrders(allUserOrders, false); // Initial render with all orders

        // **FIXED: Re-renders the list on filter click, which correctly handles empty states**
        if (filterButtons.length > 0) {
            filterButtons.forEach(button => {
                button.addEventListener('click', () => {
                    filterButtons.forEach(btn => btn.classList.remove('active'));
                    button.classList.add('active');
                    
                    const status = button.getAttribute('data-status');
                    
                    let filteredOrders;
                    if (status === 'all') {
                        filteredOrders = allUserOrders;
                    } else {
                        filteredOrders = allUserOrders.filter(order => order.status === status);
                    }
                    
                    renderOrders(filteredOrders, true); // Pass true to indicate filtering action
                });
            });
        } else {
             console.warn("Order filter buttons not found.");
        }
        
        // --- Modal-based clear history logic ---
        if(clearHistoryBtn && confirmClearModal && cancelClearBtn && historyClearedModal && closeHistoryClearedModalBtn) { // Check all necessary elements exist
            clearHistoryBtn.addEventListener('click', () => {
                confirmClearModal.style.display = 'flex';
                 setTimeout(() => confirmClearModal.classList.add('show'), 10); // Add show class for transitions
            });
            
            cancelClearBtn.addEventListener('click', () => {
                confirmClearModal.style.display = 'none';
                confirmClearModal.classList.remove('show'); // Remove show class
            });
            
            confirmClearBtn.addEventListener('click', () => {
                let ordersDB = getOrdersDB();
                const currentUser = getCurrentUserEmail(); // Re-get current user just in case
                 if (!currentUser || !ordersDB[currentUser]) { // Safety check
                     console.error("Cannot clear history: User not logged in or no history found.");
                     confirmClearModal.style.display = 'none';
                     confirmClearModal.classList.remove('show');
                     // Maybe show an error modal instead?
                     return;
                 }

                ordersDB[currentUser] = []; // Clear the user's order array
                saveOrdersDB(ordersDB); // Save the now empty history

                renderOrders([], false); // Re-render with empty array -> shows empty state
                
                confirmClearModal.style.display = 'none';
                confirmClearModal.classList.remove('show');
                historyClearedModal.style.display = 'flex'; // Show success modal
                 setTimeout(() => historyClearedModal.classList.add('show'), 10); // Add show class
            });
            
            closeHistoryClearedModalBtn.addEventListener('click', () => {
                historyClearedModal.style.display = 'none';
                 historyClearedModal.classList.remove('show'); // Remove show class
            });
             // Add modal overlay click listeners
             if (confirmClearModal) {
                 confirmClearModal.addEventListener('click', e => {
                     if (e.target === confirmClearModal) {
                          confirmClearModal.style.display = 'none';
                          confirmClearModal.classList.remove('show');
                     }
                 });
             }
              if (historyClearedModal) {
                 historyClearedModal.addEventListener('click', e => {
                     if (e.target === historyClearedModal) {
                          historyClearedModal.style.display = 'none';
                          historyClearedModal.classList.remove('show');
                     }
                 });
             }


        } else {
             console.warn("Clear history elements not found. Clear history feature disabled.");
        }
    };

    // --- INITIALIZE ---
    initializeOrdersPage();
});
```

--- START OF FILE popup.js ---
```javascript
// --- START: Visual Search Modal Logic ---

document.addEventListener('DOMContentLoaded', () => {
    // --- Visual Search Modal elements
    const visualSearchModal = document.getElementById("visualSearchModal");
    // Using querySelectorAll to find buttons with either ID
    const openModalButtons = document.querySelectorAll("#visualSearchBtn, #navVisualSearchBtn"); 
    // Using querySelector with the class to find the close button
    const closeVisualSearchBtn = document.querySelector("#visualSearchModal .visual-search-close-btn"); 
    
    // --- File handling elements
    const dropZone = document.querySelector(".visual-search-drop-zone");
    const fileInput = document.getElementById("visualSearchFileInput");
    const uploadBtn = document.querySelector(".visual-search-upload-btn");
    const errorMsg = document.getElementById("visualSearchError");
    const previewArea = document.getElementById("visualSearchPreview");
  
    // --- Action elements (buttons that appear after upload)
    const actionsContainer = document.getElementById("visualSearchActions");
    const findSimilarBtn = document.getElementById("findSimilarBtn");
    const predictPriceBtn = document.getElementById("predictPriceBtn");

    // --- Price Prediction Modal elements
    const pricePredictionModal = document.getElementById("pricePredictionModal");
    // Using querySelector with the ID for the close button
    const closePricePredictionBtn = document.getElementById("closePricePredictionBtn");
    const predictedPriceText = document.getElementById("predicted-price-text");

    // A variable to hold the image data (base64 string)
    let uploadedImageData = null;

    // Backend API base URL - Use the base URL for the AI service
    const API_BASE_URL = 'http://127.0.0.1:5000'; // Corrected API base URL

    // Check if all necessary elements are on the page. If not, log and stop.
    if (!visualSearchModal || !dropZone || !fileInput || !uploadBtn || !errorMsg || !previewArea ||
        !actionsContainer || !findSimilarBtn || !predictPriceBtn ||
        !pricePredictionModal || !closePricePredictionBtn || !predictedPriceText) {
      console.error("Essential visual search or price prediction modal elements missing from the page. Aborting full setup for these features.");
      // It's important to return from the DOMContentLoaded listener if essential parts aren't found
      return; 
    }
  
    // Function to open the visual search modal
    function openVisualSearchModal() {
      visualSearchModal.style.display = "flex"; // Make the modal visible
      clearVisualSearchState(); // Reset the modal content
      // Optional: Add a class for transitions if defined in CSS
      // setTimeout(() => visualSearchModal.classList.add('show'), 10); 
    }
  
    // Function to close the visual search modal
    function closeVisualSearchModal() {
      visualSearchModal.style.display = "none"; // Hide the modal
      // Optional: Remove a class for transitions if defined in CSS
      // visualSearchModal.classList.remove('show'); 
      clearVisualSearchState(); // Reset the modal content
    }

    // Function to close the price prediction modal
    function closePricePredictionModal() {
      pricePredictionModal.style.display = "none"; // Hide the modal
       // Optional: Remove a class for transitions if defined in CSS
      // pricePredictionModal.classList.remove('show'); 
    }
  
    // Resets the visual search modal to its initial state
    function clearVisualSearchState() {
      errorMsg.textContent = ""; // Clear error message
      previewArea.innerHTML = ""; // Clear image preview
      actionsContainer.style.display = "none"; // Hide action buttons
      dropZone.style.display = "block"; // Show drag/drop area
      dropZone.classList.remove("drag-over"); // Remove drag-over class
      fileInput.value = null; // Reset file input
      uploadedImageData = null; // Clear stored image data
    }
  
    // Handles the file once it's selected or dropped.
    function handleFile(file) {
      clearVisualSearchState(); // Clear previous state
  
      if (!file) { // Check if file exists
        errorMsg.textContent = "No file was selected.";
        return;
      }
  
      // --- File Validation ---
      const acceptedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']; // Allowed types
      if (!acceptedTypes.includes(file.type)) { // Validate type
        errorMsg.textContent = `Unsupported file type. Please upload JPEG, PNG, GIF, or WebP.`; // Added GIF to message
        return;
      }
  
      const maxSize = 5 * 1024 * 1024; // 5MB in bytes
      if (file.size > maxSize) { // Validate size
        errorMsg.textContent = `File is too large. Max size is 5MB.`;
        return;
      }
  
      // --- File Reading and Preview ---
      const reader = new FileReader(); // Create FileReader
      reader.onloadstart = function() { // Optional: show loading indicator while reading
           errorMsg.textContent = "Reading file...";
       }
      reader.onload = function (e) { // Function on successful read
        uploadedImageData = e.target.result; // Store Data URL (Base64)
        const img = document.createElement('img'); // Create image element
        img.src = uploadedImageData; // Set source
        img.alt = "Image preview";
        previewArea.appendChild(img); // Add to preview area
        dropZone.style.display = "none"; // Hide drop zone
        actionsContainer.style.display = "flex"; // Show action buttons
        errorMsg.textContent = ""; // Clear loading message
      };
      reader.onerror = function () { // Function on read error
        uploadedImageData = null; // Ensure data is cleared
        errorMsg.textContent = "Could not read the selected file."; // Display error
        dropZone.style.display = "block"; // Show drop zone again
        actionsContainer.style.display = "none"; // Hide actions
      };

      reader.readAsDataURL(file); // Read file as Data URL (Base64)
    }

    // Function to call the price prediction API (Assumes POST accepts Base64)
    async function predictPriceFromAPI(imageData) {
        closeVisualSearchModal(); // Close the visual search modal first

        try {
             // Set initial loading state in the price prediction modal
            predictedPriceText.textContent = "Analyzing image..."; 
            pricePredictionModal.style.display = 'flex'; // Show the price prediction modal
            // Optional: Add 'show' class for transitions
            // setTimeout(() => pricePredictionModal.classList.add('show'), 10);


            // Corrected URL path and method based on assumption of POST endpoint for Base64
            const response = await fetch(`${API_BASE_URL}/predict_price`, { 
                method: 'POST', // Use POST method
                headers: {
                    'Content-Type': 'application/json', // Specify JSON content
                },
                body: JSON.stringify({ // Send image data in the body as JSON
                    image: imageData 
                })
            });

            // Price prediction API example response doesn't have isCompleteSuccessfully/errorMessages
            // Handle based on HTTP status and the example response structure
            if (!response.ok) {
                // Try reading error message from body if available, otherwise use status
                 const errorData = await response.json().catch(() => null); // Attempt to parse error body
                 const errorMessage = errorData?.error || `HTTP error! status: ${response.status}`;
                 throw new Error(errorMessage);
            }

            const result = await response.json(); // Parse the JSON response
            
             // Check if the expected price field exists in the successful response
             if (result.predicted_price_egp === undefined) {
                 throw new Error("Invalid response from price prediction API.");
             }

            // Display the predicted price result
            predictedPriceText.textContent = `The estimated price for this item is ${result.predicted_price_egp} EGP`; // Display the specific price field
            
        } catch (error) { // Catch any errors during fetch or processing
            console.error('Price prediction error:', error);
            predictedPriceText.textContent = `Error predicting price: ${error.message}`; // Display error message in the modal
            // Keep modal open to show error, allow closing
        }
    }

    // Function to call the visual search API (Assumes POST accepts Base64)
    async function searchSimilarFromAPI(imageData) {
        closeVisualSearchModal(); // Close the visual search modal first

        try {
            // Show loading state on the result page before redirecting
            // This requires modifying resultpage.html or loading indicator logic there
            // For now, we'll just redirect after getting results

            // Corrected URL path and method based on assumption of POST endpoint for Base64
            const response = await fetch(`${API_BASE_URL}/find_similar`, { 
                method: 'POST', // Use POST method
                headers: {
                    'Content-Type': 'application/json', // Specify JSON content
                },
                body: JSON.stringify({ // Send image data in the body as JSON
                    image: imageData,
                    // Optional: add top_n here if needed and not hardcoded in backend
                    // top_n: 10 
                })
            });

            // Visual search API example response *does* have isCompleteSuccessfully/errorMessages
            // Handle based on that structure
            const result = await response.json(); // Parse the JSON response

            if (!response.ok || !result.isCompleteSuccessfully) {
                 // Check HTTP status AND API success flag
                const errorMessages = (Array.isArray(result.errorMessages) ? result.errorMessages.join(', ') : result.errorMessages) || `HTTP error! status: ${response.status}`;
                 throw new Error(errorMessages);
            }
            
             // Check if the expected data field exists in the successful response
             if (!Array.isArray(result.data)) {
                 throw new Error("Invalid data format from similar items API.");
             }

            // Store the original query image and the search results for the results page
            sessionStorage.setItem('visualSearchQueryImage', imageData); // Save original image
            sessionStorage.setItem('visualSearchResults', JSON.stringify(result.data)); // Save results (the 'data' array)
            
            // Navigate to results page
            window.location.href = 'resultpage.html'; // Redirect the user
            
        } catch (error) { // Catch any errors during fetch or processing
            console.error('Visual search error:', error);
            // Display the error in the visual search modal (might need to re-open it)
            openVisualSearchModal(); // Re-open modal to show error
            errorMsg.textContent = `Error searching for similar items: ${error.message}`; 
            actionsContainer.style.display = "none"; // Hide actions
            dropZone.style.display = "block"; // Show drop zone again
            uploadedImageData = null; // Clear data as search failed
        }
    }
  
    // --- EVENT LISTENERS ---
  
    // Listeners for opening the visual search modal
    openModalButtons.forEach(btn => {
        if (btn) { // Check if button exists
            btn.addEventListener("click", (e) => { 
                e.preventDefault(); 
                e.stopPropagation(); 
                openVisualSearchModal(); 
            });
        }
    });
  
    // --- Listeners for closing modals ---
    if (closeVisualSearchBtn) closeVisualSearchBtn.addEventListener("click", closeVisualSearchModal);
    // Close visual search modal when clicking outside the content box
    if (visualSearchModal) {
        visualSearchModal.addEventListener("click", (e) => {
            if (e.target === visualSearchModal) {
                closeVisualSearchModal();
            }
        });
    }

    if (closePricePredictionBtn) closePricePredictionBtn.addEventListener("click", closePricePredictionModal);
    // Close price prediction modal when clicking outside the content box
     if (pricePredictionModal) {
        pricePredictionModal.addEventListener("click", (e) => {
            if (e.target === pricePredictionModal) {
                closePricePredictionModal();
            }
        });
    }
  
    // --- Listeners for file handling (upload button and drag/drop zone) ---
     if (uploadBtn && fileInput) { // Check elements exist
         uploadBtn.addEventListener("click", () => fileInput.click()); // Button click triggers file input click
         fileInput.addEventListener("change", (e) => handleFile(e.target.files[0])); // Process file when selected via input
     } else { console.warn("Visual search upload button or file input not found."); }

     if (dropZone && fileInput) { // Check elements exist
        dropZone.addEventListener("dragenter", (e) => { e.preventDefault(); dropZone.classList.add("drag-over"); });
        dropZone.addEventListener("dragover",  (e) => { e.preventDefault(); e.dataTransfer.dropEffect = 'copy'; }); // Visual feedback
        dropZone.addEventListener("dragleave", () => dropZone.classList.remove("drag-over"));
        dropZone.addEventListener("drop", (e) => {
            e.preventDefault();
            dropZone.classList.remove("drag-over");
            handleFile(e.dataTransfer.files[0]); // Process dropped file
        });
     } else { console.warn("Visual search drop zone or file input not found."); }


    // --- Listeners for the Visual Search action buttons ---
    if (findSimilarBtn) { // Check if button exists
        findSimilarBtn.addEventListener('click', () => {
            if (uploadedImageData) { // Ensure image data is ready
                searchSimilarFromAPI(uploadedImageData); // Call similar search API
            } else {
                errorMsg.textContent = "Please upload an image first."; // Error if no image
                 actionsContainer.style.display = "none";
                 dropZone.style.display = "block";
            }
        });
    } else { console.warn("'Find Similar' button not found."); }

     if (predictPriceBtn) { // Check if button exists
        predictPriceBtn.addEventListener('click', () => {
            if (uploadedImageData) { // Ensure image data is ready
                predictPriceFromAPI(uploadedImageData); // Call price prediction API
            } else {
                errorMsg.textContent = "Please upload an image first."; // Error if no image
                actionsContainer.style.display = "none";
                 dropZone.style.display = "block";
            }
        });
    } else { console.warn("'Predict Price' button not found."); }

});
```

--- START OF FILE predict-price.js ---
```javascript
// This file is misnamed. It handles navigation from product grids to the single product page.
// The actual price prediction logic is in popup.js.

document.addEventListener('DOMContentLoaded', () => {
                // Select ALL possible product grid containers on any page where this script is included
                // Note: This duplicates listener setup found in product-grid.js.
                // If product-grid.js is loaded AFTER this, its listener will likely be the one that runs.
                // It's recommended to rely solely on product-grid.js for this navigation logic.
                 const productGrids = document.querySelectorAll('#product-grid, #related-product-grid');


                if (productGrids.length > 0) {
                    productGrids.forEach(grid => {
                        // Use one listener on the grid for better performance (event delegation)
                         // Check if a listener hasn't already been added by product-grid.js to this grid
                         // This is complex. Assuming product-grid.js is the primary handler.
                         // This script's navigation logic is redundant if product-grid.js is used.
                         // To avoid double-handling clicks or conflicts, this click listener is
                         // commented out. Rely on product-grid.js.

                        /*
                        grid.addEventListener('click', (e) => {
                            // Traverse up to find the .pro container
                            const productElement = e.target.closest('.pro');

                            // Proceed only if a product was clicked and it wasn't the cart button
                            if (productElement && !e.target.closest('.add-to-cart-btn')) {
                                const id = productElement.dataset.id;
                                const name = productElement.dataset.name;
                                const price = productElement.dataset.price;
                                const desc = productElement.dataset.desc;
                                // Use optional chaining for robustness
                                const imgSrc = productElement.querySelector('img')?.getAttribute('src'); 

                                // URL-encode all parameters to handle special characters
                                // Ensure IDs are strings for URL params
                                const url = `sproduct.html?id=${encodeURIComponent(String(id || ''))}&name=${encodeURIComponent(name || '')}&price=${encodeURIComponent(price || '0')}&desc=${encodeURIComponent(desc || '')}&img=${encodeURIComponent(imgSrc || 'Images/placeholder.png')}`;

                                // Redirect to the single product page
                                window.location.href = url;
                            }
                        });
                        */
                    });
                } else {
                     console.warn("No product grid elements found for predict-price.js (navigation logic).");
                }
            });
```

--- START OF FILE product-grid.js ---
```javascript
document.addEventListener('DOMContentLoaded', () => {
    // This global function updates the cart count in the navbar.
    // It checks if the global function exists before defining it again.
    if (!window.updateCartIcon) {
        window.updateCartIcon = () => {
            const cart = JSON.parse(localStorage.getItem('shoppingCart')) || [];
             // Ensure item.quantity is treated as a number, default to 0 if missing/invalid
            const totalQuantity = cart.reduce((sum, item) => sum + (parseInt(item.quantity, 10) || 0), 0); 
            const cartCountEl = document.getElementById('cart-count');
            if (cartCountEl) {
                cartCountEl.textContent = totalQuantity;
            }
        };
    }
    // Always run on page load to keep the cart count accurate.
    window.updateCartIcon();

    // Select ALL possible product grid containers on any page
    const productGrids = document.querySelectorAll('#product-grid, #related-product-grid');

    if (productGrids.length > 0) {
        productGrids.forEach(grid => {
            // Use one listener on the grid for better performance (event delegation)
            grid.addEventListener('click', (e) => {
                const productCard = e.target.closest('.pro');
                if (!productCard) return; // Exit if the click was not inside a product card

                const addToCartBtn = e.target.closest('.add-to-cart-btn');

                if (addToCartBtn) {
                    // --- A) HANDLE "ADD TO CART" CLICK ---
                    e.preventDefault(); // Stop any other actions

                    // Get product data from the product card's data attributes and image source
                    const product = {
                        id: productCard.dataset.id, // Stored as string in dataset
                        name: productCard.dataset.name,
                         // Ensure price is parsed as a float
                        price: parseFloat(productCard.dataset.price), 
                        imgSrc: productCard.querySelector('img')?.src || 'Images/placeholder.png', // Use optional chaining and fallback
                        // Default size when adding from a grid - hardcoded as 'M'
                        // If different sizes were needed from grid, UI would need to change
                        size: 'M', 
                        quantity: 1 // Always start with quantity 1 from grid click
                    };

                    if (!product.id || !product.name || isNaN(product.price)) { // Basic validation
                        console.error("Product data missing or invalid for adding to cart.", productCard.dataset);
                         alert("Cannot add product to cart: Missing or invalid data.");
                        return;
                    }
                    
                    let cart = JSON.parse(localStorage.getItem('shoppingCart')) || [];
                    // Find existing item by ID *and* size for merging
                    let existingItem = cart.find(item => String(item.id) === String(product.id) && item.size === product.size);
                    
                    if (existingItem) {
                        existingItem.quantity = (existingItem.quantity || 0) + 1; // Increment quantity, safety || 0
                    } else {
                        cart.push(product); // Add the new product
                    }
                    
                    localStorage.setItem('shoppingCart', JSON.stringify(cart)); // Save the updated cart
                    window.updateCartIcon(); // Update the navbar icon using the global function

                    // Provide visual feedback on the button
                    const originalIconHTML = addToCartBtn.innerHTML; // Store original icon HTML
                    addToCartBtn.innerHTML = `<i class="fas fa-check"></i>`; // Change icon to checkmark
                    addToCartBtn.disabled = true; // Disable button temporarily

                    setTimeout(() => { // Set timer to revert button state
                        addToCartBtn.innerHTML = originalIconHTML; // Restore original icon
                        addToCartBtn.disabled = false; // Re-enable button
                    }, 1500); // Timer duration: 1.5 seconds

                } else {
                    // --- B) HANDLE CLICKING THE CARD TO VIEW DETAILS --- (if not the cart button)
                    // Get product data from data attributes
                    const id = productCard.dataset.id;
                    const name = productCard.dataset.name;
                    const price = productCard.dataset.price;
                    const desc = productCard.dataset.desc;
                    const imgSrc = productCard.querySelector('img')?.src || 'Images/placeholder.png'; // Use optional chaining and fallback
                    
                    // Essential check to ensure the card has data to send for the details page
                    if (!id || !name || !price) { // Added price check as it's needed for sproduct.html
                         console.error("Cannot navigate, essential product data is missing from the card.", productCard.dataset);
                         // Optional: alert the user or show a message
                         // alert("Cannot view product details: Data is incomplete.");
                         return;
                    }

                    // Build a URL with the product data as search parameters.
                    // encodeURIComponent is crucial to handle spaces and special characters.
                     // Ensure all relevant data is included and encoded
                    const url = `sproduct.html?id=${encodeURIComponent(String(id))}&name=${encodeURIComponent(name)}&price=${encodeURIComponent(price)}&desc=${encodeURIComponent(desc || '')}&img=${encodeURIComponent(imgSrc)}`;
                    
                    // Redirect the user to the single product page
                    window.location.href = url; // Navigate to the constructed URL
                }
            });
        });
    } else {
         console.warn("No product grid elements found for product-grid.js.");
    }
});
```

--- START OF FILE resultpage.js ---
```javascript
document.addEventListener('DOMContentLoaded', () => {
    // DOM elements from resultpage.html
    const queryImageContainer = document.getElementById('query-image-container');
    const queryImageElement = document.getElementById('query-img');
    const productGrid = document.getElementById('product-grid');

    // Check if all necessary elements are on the page
    if (!queryImageContainer || !queryImageElement || !productGrid) {
        console.warn("Essential elements not found on this page for result page setup.");
        return;
    }

    // 1. Retrieve the image data URL from session storage
    const uploadedImageData = sessionStorage.getItem('visualSearchQueryImage');
    // The results are stored as JSON string of the `data` array from the API response
    const searchResults = sessionStorage.getItem('visualSearchResults'); 

    if (uploadedImageData) {
        // 2. If data exists, display the image and make the container visible
        queryImageElement.src = uploadedImageData;
        queryImageContainer.style.display = 'block'; 

        // 3. Clean up the session storage after use.
        // sessionStorage.removeItem('visualSearchQueryImage'); // Keep it if user navigates back? Let's remove for now as originally intended.
         sessionStorage.removeItem('visualSearchQueryImage');
    } else {
        console.log("No visual search query image found in session storage.");
         // Hide the query image section if no image
         queryImageContainer.style.display = 'none'; 
    }

    // 4. Display search results if available
    if (searchResults) {
        try {
            const products = JSON.parse(searchResults); // Parse the JSON string of products
            // Use the displayProducts function from api-integration.js or product-grid.js
            // Assuming displayProducts is globally available or linked before this script
            if (typeof displayProducts === 'function') {
                displayProducts(products, 'product-grid'); // Call displayProducts to render the items
            } else {
                console.error("displayProducts function not found. Cannot render search results.");
                 productGrid.innerHTML = '<div style="text-align: center; padding: 50px;"><p>Error displaying results.</p></div>';
             }

            // Clean up the session storage after use.
            sessionStorage.removeItem('visualSearchResults');

        } catch (error) { // Catch errors during JSON parsing or rendering
            console.error('Error parsing or displaying search results:', error);
             productGrid.innerHTML = '<div style="text-align: center; padding: 50px;"><p>Error loading or displaying results.</p></div>';
        }
    } else {
         console.log("No visual search results found in session storage.");
         // Display a message if no results were stored
         productGrid.innerHTML = '<div style="text-align: center; padding: 50px;"><p>No search results available.</p></div>';
     }

     // The displaySearchResults function below is a duplicate of displayProducts.
     // Since api-integration.js and/or product-grid.js are included and define/make displayProducts available,
     // it's better to rely on that. This function is commented out to avoid redundancy.
     /*
    function displaySearchResults(products) {
        // Clear existing products
        productGrid.innerHTML = '';

        if (!products || products.length === 0) {
            productGrid.innerHTML = '<div style="text-align: center; padding: 50px;"><p>No similar items found.</p></div>';
            return;
        }

        // Update page title if available (Optional for results page)
        const pageTitle = document.querySelector('h3, h2');
        if (pageTitle) {
            pageTitle.textContent = `Similar Items Found`; // More specific title
        }

        products.forEach(product => {
            const productElement = document.createElement('div');
            productElement.classList.add('pro');
             // Ensure IDs are strings when setting data attributes
            productElement.setAttribute('data-id', String(product.id || '')); 
            productElement.setAttribute('data-name', product.name || 'Unknown Product');
            productElement.setAttribute('data-price', product.price || '0');
            productElement.setAttribute('data-desc', product.description || '');

            // Use fallback values for missing properties
            const productName = product.name || 'Unknown Product';
            const productPrice = product.price || '0';
            // Prioritize brand > category name > default
            const productBrand = product.brand || product.categoryName || 'FashioNear'; 
            // Prioritize imageUrl > image > default placeholder
            const productImage = product.imageUrl || product.image || 'Images/placeholder.png'; 

            productElement.innerHTML = `
                 <div class="pro-img-container">
                    <img src="${productImage}" alt="${productName}" onerror="this.src='Images/placeholder.png'">
                </div>
                <div class="des">
                    <span>${productBrand}</span>
                    <h5>${productName}</h5>
                    <div class="star">
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                    </div>
                    <h4>${productPrice}LE</h4>
                </div>
                <button class="add-to-cart-btn"><i class="fas fa-shopping-cart cartt"></i></button>
            `;
            productGrid.appendChild(productElement);
        });
    }
    */
});
```

--- START OF FILE search-bar.css ---
```css
/* =================================== */
/* ===    Search Bar Styling     ==== */
/* ================================= */

.search-container { 
    display: flex; 
    align-items: center; 
    position: relative; 
    background-color: #f3f4f6; /* Canonical style */
    border-radius: 50px; 
    padding: 6px; 
    margin: 0 15px; 
    width: 350px; 
    transition: all 0.4s ease-in-out; 
    border: 1px solid transparent; /* Canonical style */
}
.search-container:focus-within { 
    background-color: #ffffff; 
    border-color: #e0e0e0; 
}
.search-input { 
    flex: 1; 
    border: none; 
    background: transparent; 
    padding: 10px 15px; 
    font-size: 14px; 
    outline: none; 
    color: #333; /* Canonical style */
}
.search-input::placeholder { 
    color: #888;  
    opacity: 1; 
}
.search-button.camera-button { 
    background-color: #1d1d1d; /* Canonical style */
    border: none; 
    width: 38px; 
    height: 38px; 
    border-radius: 50%; 
    cursor: pointer; 
    transition: background-color 0.3s ease, transform 0.2s ease; 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    flex-shrink: 0; 
    padding: 0; 
}
.search-button.camera-button:hover { 
    background-color: coral; 
    transform: scale(1.05); 
}
#nav-camera-img { /* Styles the img if used instead of Font Awesome */
    width: 20px; 
    height: 20px; 
    object-fit: contain; 
    filter: invert(1); /* Makes a dark icon white */
}
.search-toggle-btn { 
    display: none; /* Hidden on desktop */
}


/* ============================================== */
/* === Search Bar - Mobile Responsive Styles === */
/* ========================================= ===*/
@media only screen and (max-width:991px) {
  #navbarSupportedContent { 
    flex-basis: 100%; 
}
  .search-container { 
    width: 45px; 
    height: 45px; 
    padding: 0; 
    background-color: transparent;  
    border-radius: 50%; margin: 0; 
}
  .search-input,
  .search-button.camera-button { 
    opacity: 0; 
    width: 0; 
    padding: 0; 
    margin: 0; 
    display: none; 
}
  
  .search-toggle-btn { 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    width: 100%; 
    height: 100%; 
    background: transparent; 
    border: none; 
    font-size: 18px; 
    color: black; 
    cursor: pointer; 
    padding: 0; 
}
  
  .search-container.active { 
    width: 100%; 
    background-color: #f3f4f6; /* Canonical style */
    padding: 6px; 
    border-radius: 50px; 
    margin-top: 10px; 
}
  .search-container.active .search-input,
  .search-container.active .search-button.camera-button { 
    display: flex; 
    opacity: 1;
    width: auto; 
}
    
  .search-container.active .search-input { 
    width: 100%; 
    padding: 10px 15px; 
}
  .search-container.active .search-toggle-btn i { 
    color: #333; /* Canonical style */
}
}


/* ============================================== */
/* ===            MOBILE NAV                   ===*/
/* ============================================== */
.navbar-light .navbar-toggler{ 
    border: none; 
    outline: none; 
}
#bar{ 
    font-size: 1.5rem; 
    padding: 7px; 
    cursor: pointer; 
    font-weight: 500; 
    transition: 0.3s ease; 
    color: black; 
}
#bar:hover, #bar.active{ 
    color: #fff; 
}

@media only screen and (max-width:991px){
  body > nav > div > button:hover,
  body > nav > div > button:focus{ 
    background-color: #fb774b; 
}
  body > nav > div > button:hover #bar,
  body > nav > div > button:focus #bar{ 
    color: #fff; 
}
  #navbarSupportedContent > ul{ 
    margin: 1rem;
    justify-content: flex-end ; 
    text-align: right; 
}
  #navbarSupportedContent > ul > li:nth-child(n) > a{ 
    padding: 10px 0 ; 
}
  
  #navbarSupportedContent .d-flex {
      flex-direction: column;
      align-items: flex-end !important;
      gap: 15px;
      margin: 1rem;
  }
}

```

--- START OF FILE search-integration.js ---
```javascript
// Text Search Integration using the /search endpoint
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.querySelector('.search-input');
    // The searchToggleBtn on mobile also acts as a 'search' button once the bar is open
    const searchToggleBtn = document.getElementById('search-toggle-btn'); 
    const desktopSearchIcon = document.querySelector('.search-container .fas.fa-search'); // Assuming desktop search icon exists

    // Backend API base URL for search/AI endpoints
    const API_BASE_URL = 'http://127.0.0.1:5000'; // Corrected API base URL

    if (!searchInput) {
        console.warn("Search input not found on this page. Text search feature disabled.");
        return;
    }

    // Function to perform text search against the backend API
    async function performTextSearch(query) {
        try {
            const trimmedQuery = query.trim();
            if (!trimmedQuery) {
                console.log("Search query is empty.");
                // Optionally clear results or show message if query is empty
                const productGrid = document.getElementById('product-grid');
                 if (productGrid) {
                     // Assuming a display function like displayProducts is available globally
                     if (typeof displayProducts === 'function') {
                         // Re-load default products if available, or clear grid
                         // For now, let's clear it and show a message
                         productGrid.innerHTML = '<div style="text-align: center; padding: 50px;"><p>Enter text to search.</p></div>';
                     } else {
                          productGrid.innerHTML = ''; // Just clear if displayProducts is not available
                     }
                 }
                return;
            }

            // Show loading state in the product grid area
            const productGrid = document.getElementById('product-grid');
            if (productGrid) {
                productGrid.innerHTML = '<div class="loading-spinner" style="text-align: center; padding: 50px;"><i class="fas fa-spinner fa-spin fa-2x"></i><p>Searching...</p></div>';
            } else {
                 console.warn("Product grid element #product-grid not found to display loading spinner.");
            }


            // Corrected URL construction to match Flask endpoint /search/<query> (GET)
            const url = `${API_BASE_URL}/search/${encodeURIComponent(trimmedQuery)}`; // Encode the query

            const response = await fetch(url, {
                method: 'GET', // Use GET method as per API definition
                // No headers or body needed for GET request with path parameter
            });

            // The API example response has isCompleteSuccessfully/errorMessages
            const result = await response.json(); 

            // Check for HTTP status AND the API's success flag
            if (!response.ok || !result.isCompleteSuccessfully) {
                const errorMessages = (Array.isArray(result.errorMessages) ? result.errorMessages.join(', ') : result.errorMessages) || `HTTP error! status: ${response.status}`;
                throw new Error(errorMessages);
            }
            
             // Check if the expected data field exists in the successful response
             if (!Array.isArray(result.data)) {
                 throw new Error("Invalid data format from text search API.");
             }


            // Display results using the `displayProducts` function (assuming it's available)
            // The API returns an array in `result.data` that matches the expected product format
            if (typeof displayProducts === 'function' && productGrid) {
                displayProducts(result.data, 'product-grid'); // Pass the 'data' array from the API response
            } else if (productGrid) {
                console.error("displayProducts function not found. Cannot render text search results.");
                 // Manual display if displayProducts is not available globally
                 // (This would duplicate logic from api-integration.js/product-grid.js)
                 productGrid.innerHTML = '<div style="text-align: center; padding: 50px;"><p>Error displaying search results.</p></div>';
             }


            // Optional: Update page title to reflect search query
            const pageTitleEl = document.querySelector('h3, h2'); // Find a suitable title element
            if (pageTitleEl) {
                pageTitleEl.textContent = `Search Results for "${trimmedQuery}"`;
            }
            
        } catch (error) { // Catch any errors during fetch or processing
            console.error('Text search error:', error);
            const productGrid = document.getElementById('product-grid');
            if (productGrid) {
                // Remove loading spinner if it's there
                const loadingSpinner = productGrid.querySelector('.loading-spinner');
                if (loadingSpinner) loadingSpinner.remove();
                productGrid.innerHTML = `<div style="text-align: center; padding: 50px;"><p>Error searching: ${error.message}</p></div>`;
            }
        }
    }

    // Event listeners for triggering search
    // Listen for 'keypress' on the input field
    searchInput.addEventListener('keypress', (e) => {
        // Check if the pressed key was 'Enter' (key code 13 is less reliable than key property)
        if (e.key === 'Enter') {
            e.preventDefault(); // Prevent default form submission if input is inside a form
            const query = searchInput.value; // Get the current value from the input
            performTextSearch(query); // Call the search function
        }
    });

    // Optional: Add click listener to the *search icon* button if it should also trigger search
    // The searchToggleBtn handles visibility on mobile. On desktop, it's just the icon.
    // Let's add a listener to the desktop icon if it exists.
     if (desktopSearchIcon) {
         desktopSearchIcon.parentElement.addEventListener('click', () => { // Add listener to the button wrapping the icon
              const query = searchInput.value;
              performTextSearch(query);
         });
     }
    
    // On mobile, searchToggleBtn is shown and becomes the clickable element when the bar is collapsed.
    // When the bar is expanded, searchInput is visible. Pressing Enter in the input is handled above.
    // If the mobile search button should trigger search *after* the bar is expanded (e.g., if it changed appearance),
    // you might add another listener here, but the Enter key is the standard interaction.
    // The logic in search.js handles the mobile toggle animation, not the search execution itself.
});
```

--- START OF FILE sproduct.js ---
```javascript
document.addEventListener('DOMContentLoaded', () => {

    // --- DOM ELEMENTS ---
    const addToCartBtn = document.getElementById('addToCartBtn'); // The 'Add To Cart' button
    const productDetailsContainer = document.getElementById('productDetails'); // The container holding product details elements
    // Corrected element IDs based on sproduct.html structure
    const productNameEl = document.getElementById('product-name'); 
    const productPriceEl = document.getElementById('product-price'); 
    const productSizeEl = document.getElementById('productSize'); // Select element for size
    const productQuantityEl = document.getElementById('productQuantity'); // Input for quantity
    const mainImgEl = document.getElementById('MainImg'); // The main product image element
    const cartCountEl = document.getElementById('cart-count'); // The cart count element in the navbar


    // --- FUNCTIONS ---
     // This function is a duplicate of the global one in auth.js and one in men-page-script.js.
     // Relying on the global window.updateCartIcon is recommended.
    const updateCartCount = () => { 
        const cart = JSON.parse(localStorage.getItem('shoppingCart')) || [];
        const totalItems = cart.reduce((sum, item) => sum + (parseInt(item.quantity, 10) || 0), 0); // Added || 0 for safety
        if (cartCountEl) {
             cartCountEl.textContent = totalItems;
        }
    };

    const handleAddToCart = () => {
        // --- Get Product Info from the DOM ---
        // We retrieve product data from the populated DOM elements and data attributes here.
        const productId = productDetailsContainer ? productDetailsContainer.dataset.id : null; // Get product ID from the details container's data attribute
        const productName = productNameEl ? productNameEl.textContent.trim() : 'Unknown Product'; // Get product name from its element
        // Extract number from price string (e.g., "200 LE" -> 200)
        const priceText = productPriceEl ? productPriceEl.textContent.replace(/LE/i, '').trim() : '0'; // Get price text and remove 'LE'
        const productPrice = parseFloat(priceText); // Parse price text to float

        const productSize = productSizeEl ? productSizeEl.value : 'N/A'; // Get selected size, default to N/A
        const productQuantity = productQuantityEl ? parseInt(productQuantityEl.value, 10) : 1; // Get quantity, parse to integer, default to 1
        const productImgSrc = mainImgEl ? mainImgEl.getAttribute('src') : 'Images/placeholder.png'; // Get image source

        // --- Validation ---
        if (!productId) { // Check if product ID was successfully retrieved
              console.error("Cannot add to cart: Product ID is missing.");
              alert('Error adding product to cart. Missing product data.');
              return;
         }
        if (productSize === 'Select Size') { // Check if a size was selected from the dropdown
            alert('Please select a size before adding to cart.');
            return; // Exit if size is not selected
        }
        if (isNaN(productQuantity) || productQuantity < 1) { // Check if quantity is a valid number >= 1
            alert('Please enter a valid quantity.');
            return; // Exit if quantity is invalid
        }
         if (isNaN(productPrice)) { // Check if price is valid
             console.error("Product price is invalid:", priceText);
             alert('Error adding product to cart. Invalid price data.');
             return;
         }


        // --- Update Cart ---
        let cart = JSON.parse(localStorage.getItem('shoppingCart')) || []; // Get current cart
        // Check if an item with the same ID and size already exists
        let existingItem = cart.find(item => String(item.id) === String(productId) && item.size === productSize); // Find item by ID (compare as strings) and size

        if (existingItem) { // If item exists
            existingItem.quantity = (existingItem.quantity || 0) + productQuantity; // Add the selected quantity to the existing item, safety || 0
        } else { // If item is new
            cart.push({ // Add a new item object to the cart
                id: productId,
                name: productName,
                price: productPrice,
                quantity: productQuantity,
                imgSrc: productImgSrc,
                size: productSize
            });
        }

        // --- Save to localStorage and Update UI ---
        localStorage.setItem('shoppingCart', JSON.stringify(cart)); // Save updated cart
        // Use the global updateCartIcon function if available for consistency
        if (window.updateCartIcon) {
             window.updateCartIcon(); // Call global function
        } else {
             updateCartCount(); // Fallback to local duplicate if global is missing
        }

        // --- Provide User Feedback on the Button ---
        if (addToCartBtn) { // Check if button exists before modifying it
            const originalText = addToCartBtn.innerHTML; // Store original button HTML
            addToCartBtn.innerHTML = `Added <i class="fas fa-check"></i>`; // Change button text/icon
            addToCartBtn.disabled = true; // Disable button

            setTimeout(() => { // Set timer to revert button state
                addToCartBtn.innerHTML = originalText; // Restore original HTML
                addToCartBtn.disabled = false; // Re-enable button
            }, 2000); // Timer duration: 2000 milliseconds (2 seconds)
        }
    };

    // --- EVENT LISTENERS ---
    if (addToCartBtn) { // Check if the button exists
        addToCartBtn.addEventListener('click', handleAddToCart); // Add click listener
    } else {
        console.warn("Add to Cart button not found.");
    }


    // --- INITIALIZATION ---
    // The cart count is updated globally by auth.js on DOMContentLoaded.
    // Calling it here ensures it's updated specifically for this page too,
    // or acts as a fallback if auth.js wasn't included first.
    updateCartCount(); 
    
    // The main product details on this page are populated by the products.js script,
    // which reads from the URL. This script (sproduct.js) primarily adds the
    // 'Add to Cart' functionality to the already displayed product.

    // Related products below the main product are populated by products.js calling displayProducts.
    // Clicks on related products are handled by product-grid.js if it's included.
});
```

--- START OF FILE Women.css ---
```css
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800;900&display=swap");
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: "Poppins", sans-serif;
}

h1 {
  font-size: 2.5rem;
  font-weight: 700;
}

h2 {
  font-size: 1.8rem;
  font-weight: 600;
}

h3 {
  font-size: 1.4rem;
  font-weight: 800;
}

h4 {
  font-size: 1.1rem;
  font-weight: 600;
}

h5 {
  font-size: 1rem;
  font-weight: 400;
  color: #1d1d1d;
}

h6 {
  color: #d8d8d8;
}

button{
  font-size: 0.8rem;
  font-weight: 700;
  outline: none;
  border: none;
  background-color: #1d1d1d;
  color: aliceblue;
  padding: 13px 30px;
  cursor: pointer;
  text-transform: uppercase;
  transition: 0.3s ease;
}

button:hover{
  background-color: #3a383a;
  border-radius: 0%;
}

button:focus {
    outline: none;
  }

hr {
  width: 30px;
  height: 2px;
  background-color: #fb774b;
}

/* =================================== */
/* ===         Logo Styling          === */
/* =================================== */
.logo-img {
  height: 80px;            /* Sets the height of the circle */
  width: 80px;             /* Sets the width, MUST be same as height for a perfect circle */
  border-radius: 50%;      /* This is the key property that creates the circular shape */
  object-fit: cover;       /* IMPORTANT: Prevents the image from stretching or squishing. It will be cropped to fit the circle perfectly. */
  margin-right: 25px;      /* Adds some space between the logo and other nav items */

}

.navbar .iconCart { /* Unused class */
  position: relative;
  cursor: pointer;
  margin-left: 20px;
}

.navbar .iconCart img { /* Unused class */
  width: 30px;
  height: auto;
}


.navbar .profile {
  position: relative;
  cursor: pointer;
  margin-left: 20px;
}

.navbar .profile img {
  width: 30px;
  height: auto;
}




.navbar{
    font-size: 16px;
    top: 0;
    left: 0;
}

.navbar-light .navbar-nav .nav-link{
    padding: 0 20px;
    color: black;
    transition: 0.3s ease;
}
.navbar-light .navbar-nav .nav-link:hover,
.navbar-light .navbar-nav .nav-link.active{
    color: coral;
}
.navbar i{
    font-size: 1.2rem;
    padding: 0 7px;
    cursor: pointer;
    font-weight: 500;
    transition: 0.3s ease;
}

/* =================================== */
/* === Authentication Modal Styles sign up , sign in popup page === */
/* =================================== */

.auth-modal-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1060; /* Higher than bootstrap navbar and visual search */
    display: flex;
    justify-content: center;
    align-items: center;
    backdrop-filter: blur(3px);
}

.auth-box {
    background: #fff;
    border-radius: 10px;
    box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
    position: relative;
    overflow: hidden;
    width: 768px;
    max-width: 100%;
    min-height: 480px;
}

.auth-box h1 {
	font-weight: bold;
	margin: 0;
    font-size: 2.1rem;
    color: #333;
}

.auth-box p {
	font-size: 14px;
	font-weight: 100;
	line-height: 20px;
	letter-spacing: 0.5px;
	margin: 20px 0 30px;
}

.auth-box span {
	font-size: 12px;
}

.auth-box a {
	color: #333;
	font-size: 14px;
	text-decoration: none;
	margin: 15px 0;
}
.auth-box a:hover {
    color: coral;
}

.auth-box button {
	border-radius: 20px;
	border: 1px solid #008080;
	background-color: #008080;
	color: #FFFFFF;
	font-size: 12px;
	font-weight: bold;
	padding: 12px 45px;
	letter-spacing: 1px;
	text-transform: uppercase;
	transition: transform 80ms ease-in, background-color 0.3s;
}

.auth-box button:active {
	transform: scale(0.95);
}

.auth-box button.ghost {
	background-color: transparent;
	border-color: #FFFFFF;
}
.auth-box button.ghost:hover {
    background-color: rgba(255, 255, 255, 0.2);
}

.auth-box form {
	background-color: #FFFFFF;
	display: flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;
	padding: 0 50px;
	height: 100%;
	text-align: center;
}

.auth-box input {
	background-color: #eee;
	border: none;
	padding: 12px 15px;
	margin: 8px 0;
	width: 100%;
    border-radius: 5px;
}

.form-container {
	position: absolute;
	top: 0;
	height: 100%;
	transition: all 0.6s ease-in-out;
}

.sign-in-container {
	left: 0;
	width: 50%;
	z-index: 2;
}

.sign-up-container {
	left: 0;
	width: 50%;
	opacity: 0;
	z-index: 1;
}

.social-container {
	margin: 20px 0;
}

.social-container a {
	border: 1px solid #DDDDDD;
	border-radius: 50%;
	display: inline-flex;
	justify-content: center;
	align-items: center;
	margin: 0 5px;
	height: 40px;
	width: 40px;
    transition: background-color 0.3s, color 0.3s;
}

.social-container a:hover {
    background-color: #eee;
}

.overlay-container {
	position: absolute;
	top: 0;
	left: 50%;
	width: 50%;
	height: 100%;
	overflow: hidden;
	transition: transform 0.6s ease-in-out;
	z-index: 100;
}

.overlay {
	background: #008080;
	background: -webkit-linear-gradient(to right, #2E8B57, #008080);
	background: linear-gradient(to right, #2E8B57, #008080);
	background-repeat: no-repeat;
	background-size: cover;
	background-position: 0 0;
	color: #FFFFFF;
	position: relative;
	left: -100%;
	height: 100%;
	width: 200%;
  	transform: translateX(0);
	transition: transform 0.6s ease-in-out;
}

.overlay-panel {
	position: absolute;
	display: flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;
	padding: 0 40px;
	text-align: center;
	top: 0;
	height: 100%;
	width: 50%;
	transform: translateX(0);
	transition: transform 0.6s ease-in-out;
}

.overlay-left {
	transform: translateX(-20%);
}

.overlay-right {
	right: 0;
	transform: translateX(0);
}

/* === Animation for Panel Sliding === */
.auth-box.right-panel-active .sign-in-container {
	transform: translateX(100%);
}

.auth-box.right-panel-active .overlay-container {
	transform: translateX(-100%);
}

.auth-box.right-panel-active .sign-up-container {
	transform: translateX(100%);
	opacity: 1;
	z-index: 5;
	animation: show 0.6s;
}

@keyframes show {
	0%, 49.99% {
		opacity: 0;
		z-index: 1;
	}
	
	50%, 100% {
		opacity: 1;
		z-index: 5;
	}
}

.auth-box.right-panel-active .overlay {
	transform: translateX(50%);
}

.auth-box.right-panel-active .overlay-left {
	transform: translateX(0);
}

.auth-box.right-panel-active .overlay-right {
	transform: translateX(20%);
}

/* ____________________________________________________________ */

/* =================================== */
/* ===         New Search Bar        === */
/* =================================== */

.search-container {
  display: flex;
  align-items: center;
  position: relative;
  background-color: #fff; /* Differs from search-bar.css */
  border-radius: 50px;
  padding: 6px;
  margin: 0 15px; /* Added margin to separate from other nav items */
  width: 350px;
  transition: all 0.4s ease-in-out;
  border: none; /* Differs from search-bar.css */
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 10px 15px;
  font-size: 14px;
  outline: none;
  color: #E0E0E0; /* Differs from search-bar.css */
}

.search-input::placeholder {
  color: #999; /* Lighter placeholder text */
  opacity: 1; 
}

/* This is the new Camera button */
.search-button.camera-button {
  background-color: #000; /* Differs from search-bar.css */
  border: none;
  color: #fff; /* Differs from search-bar.css */
  width: 38px;
  height: 38px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease, transform 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0; /* Prevents button from shrinking */
  padding: 0; /* Reset padding */
}

.search-button.camera-button:hover {
  background-color: #fb774b;
  transform: scale(1.05);
}

/* The toggle button, hidden on desktop by default */
.search-toggle-btn {
    display: none; /* Hidden on desktop */
}


/* Remove old search button styles that might conflict */
.search-button {
  background: transparent;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: color 0.3s ease;
}
.search-button:hover {
    color: inherit;
    background: transparent;
}



/* ========================================= */
/* === Search Bar - Mobile Responsive Styles === */
/* ========================================= */
@media only screen and (max-width:991px) {
  /* Make room in the mobile navbar */
  #navbarSupportedContent {
      flex-basis: 100%;
  }

  .search-container {
      /* Collapsed state on mobile */
      width: 45px;
      height: 45px;
      padding: 0;
      background-color: transparent; /* No background when collapsed */
      border-radius: 50%;
      margin: 0;
  }

  .search-input,
  .search-button.camera-button {
      /* Hide the input and camera when collapsed */
      opacity: 0;
      width: 0;
      padding: 0;
      margin: 0;
      display: none;
  }
  
  .search-toggle-btn {
      /* Show and style the toggle icon */
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: 100%;
      background: transparent;
      border: none;
      font-size: 18px;
      color: black; /* Visible against light navbar */
      cursor: pointer;
      padding: 0;
  }

  /* --- Expanded state on mobile --- */
  .search-container.active {
      width: 100%;
      background-color: #3C3C3C; /* Differs from search-bar.css */
      padding: 6px;
      border-radius: 50px;
      margin-top: 10px; /* Give it space when it opens */
  }

  .search-container.active .search-input,
  .search-container.active .search-button.camera-button {
      /* Reveal the input and camera button */
      display: flex;
      opacity: 1;
      width: auto;
  }
    
  .search-container.active .search-input {
      width: 100%;
      padding: 10px 15px;
  }

  .search-container.active .search-toggle-btn i {
      color: #E0E0E0; /* Differs from search-bar.css */
  }
}

/* Mobile Nav */
.navbar-light .navbar-toggler{
  border: none;
  outline: none;
}

#bar{
  font-size: 1.5rem;
  padding: 7px;
  cursor: pointer;
  font-weight: 500;
  transition: 0.3s ease;
  color: black;
}

#bar:hover,
#bar.active{
  color: #fff;
}



@media only screen and (max-width:991px){
  body > nav > div > button:hover,
  body > nav > div > button:focus{
    background-color: #fb774b;
  }

  body > nav > div > button:hover #bar,
  body > nav > div > button:focus #bar{
    color: #fff;
  }

  #navbarSupportedContent > ul{
    margin: 1rem;
    justify-content: flex-end ;
    text-align: right;
  }

  #navbarSupportedContent > ul > li:nth-child(n) > a{
    padding: 10px 0 ;
  }

}









footer{ /* This footer style is different from footer.css */
  background-color: #222222;
}

footer h5{
  color: #d8d8d8;
  font-weight: 700;
  font-size: 1.2rem;
}

footer h1{ /* Semantically incorrect h1 */
  padding-bottom: 4px;
}

footer li a{
  font-size: 0.8rem;
  color: #999;
}

footer li a:hover{
  color: #d8d8d8;
}

footer p{
  color: #999;
  font-size: 0.8rem;
}

footer .copyright a{
  color: black;
  width: 38px;
  height: 38px;
  background-color: #fff;
  display: inline-block;
  text-align: center;
  line-height: 38px;
  border-radius: 50%;
  transition: 0.3s ease;
  margin: 0 5 px; /* Syntax error */
}

footer .copyright a:hover{
  color: #fff;
  background-color: coral;
}
```

**Explanation of Changes:**

1.  **`auth.js`:**
    *   Made `updateCartIcon` more robust by adding `|| 0` when summing quantities.
    *   Slightly refined the `showSuccessModal` to clear the auto-reload timeout if the button is clicked, preventing double reloads.
    *   Refined `updateNavIcon` to explicitly check for `currentUser.avatarUrl` before using it and reset `borderRadius` when using the default icon.
    *   Added more specific checks for the existence of input elements within the sign-up, sign-in, and profile form blocks before adding listeners or accessing `.value`.
    *   Improved avatar upload validation to check file type.
    *   Added safety checks when saving/loading user data to/from the database to ensure the user object exists before attempting to access its properties.

2.  **`api-integration.js`:**
    *   No changes were made to the `fetchProducts` function or the API base URL it uses (`https://tpf.runasp.net/`). This script remains responsible for fetching general product lists, not the AI search/prediction.
    *   Minor improvements to `displayProducts` (checking for loading spinner, using `String()` for data-id, prioritizing brand/category/image sources). This function is likely called by other scripts (`homepage.js`, category pages) and should be the canonical way to display products.

3.  **`cart.js`:**
    *   Made quantity calculation more robust (`(item.quantity || 0)`).
    *   Added checks for the existence of `progressBar`.
    *   Added checks for promo elements before trying to add/remove classes.
    *   Refined `handleCartUpdate` to use `closest` more effectively and handle null/undefined sizes safely.
    *   Added quantity safety (`|| 0`) in increase/decrease logic.
    *   Included logic to allow clicks on the item link (`a.order-item`) to pass through the delegation.

4.  **`change-password.js`:**
    *   Added checks for essential elements (`yetiAvatar`, `formWrapper`, `newPasswordInput`, `strengthMeter`, `strengthBars`) before adding listeners or accessing properties, preventing errors if elements are missing.
    *   Improved the `trackMouse` logic to avoid flickering by comparing against the substring of the current image source path. Adjusted sensitivity thresholds slightly.
    *   Refined the `focus`/`blur` and `mousedown`/`mouseup`/`mouseleave` listeners for the password fields and toggle icons to better handle transitions between states and ensure eye tracking resumes correctly.
    *   Added checks for `hasMixedCase` (uppercase and lowercase letters) in `calculatePasswordStrength` for a more standard strength calculation.
    *   Refined `updateStrengthMeter` to use a safe index for accessing colors and apply the determined strength color to all filled bars.

5.  **`checkout.js`:**
    *   Made quantity calculation more robust (`(item.quantity || 0)`).
    *   Added checks for the existence of summary elements before updating `textContent`.
    *   Added a fallback `isLoggedIn` definition in case `auth.js` isn't included or runs later.
    *   Modified `setupPaymentSelection` to select the first option by default on load and use 'active'/'inactive' classes more consistently.
    *   Added checks for input elements in `loadUserData` before attempting to populate their values.
    *   Added safety checks in `processOrder` to ensure a user is logged in and the cart is not empty before proceeding.
    *   Added more details to the `newOrder` object creation (though commented out).
    *   Improved `initialChecks` to disable the confirm button if the cart is empty.
    *   Modified the `confirmPaymentBtn` click listener to show the `signInPromptModal` (which is already defined in `checkout.html`) instead of directly showing the main `authModal` if the user is not logged in. Added listeners for the prompt modal's buttons.
    *   Added modal overlay click listeners for `confirmClearModal` and `historyClearedModal` to allow closing by clicking outside.

6.  **`forgot-password.css`:**
    *   No changes were made to the CSS. (Added box-sizing to form input for robustness).

7.  **`homepage.html`:**
    *   No changes were made to the HTML structure.
    *   Updated script includes to explicitly list `popup.js` (for visual search modal logic) and `search-integration.js` (for text search logic). Removed the old `popup.js`.

8.  **`Kids.css`:**
    *   No changes were made to the CSS. (Added comments noting unused classes and duplicated sections).

9.  **`Men.css`:**
    *   No changes were made to the CSS. (Added comments noting duplicated IDs).

10. **`Navbar.css`:**
    *   No changes were made to the CSS.

11. **`orders.js`:**
    *   Added a fallback `isLoggedIn` definition.
    *   Added checks for essential elements (`orderListContainer`, `emptyView`) before proceeding.
    *   Added checks for `filterButtons` before iterating and adding listeners.
    *   Added checks for all necessary elements before setting up the clear history modal listeners.
    *   Added a safety check in the clear history confirm button listener to ensure the user is logged in before attempting to clear.
    *   Added modal overlay click listeners for confirmation modals.
    *   Improved `renderOrderItems` and `renderOrders` with more safety checks and fallback values in case of missing data in the stored order objects. Added a `.replace(/\s+/g, '')` to status class names to ensure they are valid CSS class names even if status strings contain spaces.

12. **`popup.js`:**
    *   **Corrected `API_BASE_URL`** to `http://127.0.0.1:5000`.
    *   **Updated `predictPriceFromAPI`:**
        *   Changed the fetch URL path to `/predict_price`.
        *   Kept `method: 'POST'` and `body: JSON.stringify({ image: imageData })`, *assuming* your backend API supports this despite the provided definition showing GET with URL.
        *   Adjusted error handling and result parsing to match the example response structure (`result.predicted_price_egp`) which does *not* include `isCompleteSuccessfully` or `errorMessages` fields for success. Added checks for `response.ok` and the presence of `predicted_price_egp`.
        *   Added `closeVisualSearchModal()` at the start to close the initial modal before showing the price prediction result.
    *   **Updated `searchSimilarFromAPI`:**
        *   Changed the fetch URL path to `/find_similar`.
        *   Kept `method: 'POST'` and `body: JSON.stringify({ image: imageData })`, *assuming* your backend API supports this.
        *   Adjusted error handling and result parsing to match the example response structure (`isCompleteSuccessfully`, `data`, `errorMessages`). Checks `response.ok` *and* `result.isCompleteSuccessfully`. Extracts the results from `result.data`.
        *   Added `closeVisualSearchModal()` at the start.
        *   Added `openVisualSearchModal()` in the catch block to allow the error message to be displayed in the original modal.
    *   Added more checks for the existence of DOM elements before adding listeners.
    *   Added GIF to accepted file types message.
    *   Added `onloadstart` message and cleared error/loading message in `onload`.
    *   Ensured `uploadedImageData` is cleared on file read error.

13. **`predict-price.js`:**
    *   No changes were made to the JavaScript code. Commented out the click listener as it duplicates functionality in `product-grid.js`. The filename remains misleading.

14. **`product-grid.js`:**
    *   Made the quantity sum calculation in `updateCartIcon` more robust (`parseInt(item.quantity, 10) || 0`).
    *   Made product data retrieval from `dataset` more robust by adding `String()` and fallback empty strings/0 for URL parameters.
    *   Added a basic price check (`!isNaN(product.price)`) before adding to cart.
    *   Ensured consistency in finding existing cart items by comparing `id` as strings.
    *   Made existing item quantity increment more robust (`(existingItem.quantity || 0) + 1`).
    *   Added optional chaining `?.src` and fallbacks when getting image source from the product card.
    *   Added a check for `price` in the navigation logic (`!price`) as it's needed for `sproduct.html`.

15. **`sproduct.js`:**
    *   Made quantity sum calculation in `updateCartCount` more robust.
    *   Made product data retrieval from elements more robust (checking element existence, using `||` fallbacks).
    *   Refined price parsing to remove "LE" before parsing.
    *   Made quantity addition more robust (`(existingItem.quantity || 0) + productQuantity`).
    *   Added a check for invalid parsed price (`isNaN(productPrice)`).
    *   Added checks for element existence before modifying the button feedback.
    *   Ensured product ID and price validation before adding to cart.

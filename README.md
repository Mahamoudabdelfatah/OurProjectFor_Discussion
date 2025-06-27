Okay, let's integrate the provided Flask API functionality into your existing JavaScript code.

Based on the API endpoints and your existing scripts, here's the plan:

1.  **Identify API Actions:**
    *   `/search/<string:query>` (GET): Text search.
    *   `/find_similar` (GET): Visual search for similar items by image URL.
    *   `/predict_price` (GET): Price prediction by image URL.

2.  **Map API Actions to Frontend Scripts:**
    *   Text search belongs in `search-integration.js`, which currently handles text search and the mobile search toggle.
    *   Visual search (similar items) and price prediction belong in `popup.js`, which manages the visual search modal and its action buttons.

3.  **Analyze API Data Structures:**
    *   Text Search (`/search/<query>`) and Similar Items (`/find_similar`) return a JSON object with `isCompleteSuccessfully` (boolean), `data` (array of product objects on success, `null` on failure), and `errorMessages` (array of strings on failure, `null` on success). The product objects in `data` have keys like `productId`, `name`, `price`, `description`, `image`, `categoryId`, `categoryName`.
    *   Price Prediction (`/predict_price`) returns a simpler JSON object with `image_url` and `predicted_price_egp` on success, or an `error` string on failure.

4.  **Consolidate Product Display Logic:**
    *   The function `displayProducts(products, containerId)` exists in `api-integration.js` and is duplicated (with slight variations or comments) in `resultpage.js`. This function is crucial for rendering products into a grid regardless of whether they came from a category fetch, text search, or visual search.
    *   **Decision:** Move the canonical `displayProducts` function to `product-grid.js` as it interacts closely with the `.pro` elements and their click handlers (also in `product-grid.js`). All other scripts will then call this shared function.

5.  **Address Image Handling:**
    *   The frontend visual search modal (`popup.js`, `search.js`) gets the uploaded image as a Data URL (Base64 string).
    *   The provided Flask API endpoints (`/find_similar`, `/predict_price`) are defined as `GET` requests expecting an `image_url` *query parameter*. This doesn't directly accept a Base64 string.
    *   **Assumption/Correction:** It's highly probable that the backend API is *designed* to receive the image Data URL in a POST request body to the endpoints already used in your frontend (`/search-by-image` and `/predict-price`) or similar. Sending large Data URLs in GET query parameters is bad practice. Given the frontend code already attempts POSTing Data URLs, we will proceed assuming the backend is, or will be, configured to receive POST requests with JSON bodies containing the `image` key with the Base64 string at these or slightly adjusted paths like `/api/ai/search-by-image` and `/api/ai/predict-price`.

6.  **Refactor Frontend Scripts:**

    *   **`api-integration.js`**:
        *   Keep `fetchProducts`. Update the base URL if the backend is at `http://localhost:5000`.
        *   Remove the `displayProducts` function definition.
    *   **`product-grid.js`**:
        *   **Add** the `displayProducts` function definition here.
        *   Keep the event listener for clicks on `.pro` cards (for adding to cart and navigating to `sproduct.html`). Ensure it calls the *local* `displayProducts` for related products on `sproduct.html`.
        *   Keep the global `window.updateCartIcon` definition and call.
    *   **`search-integration.js`**:
        *   Update the `API_BASE_URL`.
        *   Modify `performTextSearch` to make a POST request to `/api/ai/search` (or `/search` if that's the intended POST route for text search) with the query in the body.
        *   Adjust error handling based on the API response structure (`isCompleteSuccessfully`, `errorMessages`).
        *   Call the `displayProducts` function (now defined in `product-grid.js`) with the `result.data`.
        *   Remove the redundant `displayTextSearchResults` function.
    *   **`popup.js`**:
        *   Update the `API_BASE_URL`.
        *   Modify `predictPriceFromAPI` and `searchSimilarFromAPI`. They already use POST requests to `/api/ai/predict-price` and `/api/ai/search-by-image` respectively, sending the image data in the body, which aligns better with handling Base64. Adapt the response handling to the specified JSON formats (`predicted_price_egp` for price; `isCompleteSuccessfully`, `data` for similar items).
        *   Ensure `searchSimilarFromAPI` saves `result.data` (the array of products) to `sessionStorage`, as `resultpage.js` expects this format.
    *   **`resultpage.js`**:
        *   Keep the logic to read `sessionStorage`.
        *   Call the `displayProducts` function (now defined in `product-grid.js`) with the parsed `products` array.
        *   Remove the redundant `displaySearchResults` function.
    *   **`sproduct.js`**:
        *   Ensure it calls `window.updateCartIcon()` instead of its local `updateCartCount` duplicate.
        *   It relies on `products.js` for initial data load and `product-grid.js` for related products clicks.
    *   **`auth.js`**: Keep as is. It correctly defines and calls `window.updateCartIcon`.
    *   **`cart.js`**: Keep as is. It correctly uses `window.updateCartIcon`.
    *   **`change-password.js`**: Keep as is. No API search dependency.
    *   **`checkout.js`**: Keep as is. Uses `window.updateCartIcon` and saves orders to `localStorage`. No API search dependency.
    *   **Remove Redundant Scripts:** Remove `search.js` (its mobile toggle is likely covered by `search-integration.js` and CSS, and its visual search file handling is superseded by `popup.js`) and `predict-price.js` (its product card navigation logic is in `product-grid.js`, and price prediction calling is in `popup.js`).

7.  **Review Script Inclusion Order:** Ensure scripts defining global functions (`auth.js`, `product-grid.js`) are loaded before scripts that call them.

Here are the modified JavaScript files:

**--- START OF FILE auth.js ---**

(No changes needed in this file for the API integration itself, as it already defines the global cart function and handles auth/profile independently).

```javascript
// --- NEW: Global function to update the cart count in the navbar ---
// Made global by attaching to the window object so other scripts can call it.
window.updateCartIcon = () => {
    const cart = JSON.parse(localStorage.getItem('shoppingCart')) || [];
    // Calculates the total number of items, not just unique entries
    const totalQuantity = cart.reduce((sum, item) => sum + item.quantity, 0);
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
        // Use requestAnimationFrame for better transition timing
        requestAnimationFrame(() => {
             requestAnimationFrame(() => {
                 successModal.classList.add('show');
             });
        });
        
        // Only reload if the button doesn't exist (fallback) or if needed for specific actions
        // For auth success, we might want to reload to update UI elements like the profile icon/cart
         setTimeout(() => {
             window.location.reload();
         }, 1500); // Reduced delay for quicker feedback
    };
    
    // Ensure the success modal button closes the modal if it exists
    if (successModalBtn) {
        successModalBtn.addEventListener('click', () => {
            if (successModal) successModal.classList.remove('show');
             setTimeout(() => {
                 if (successModal) successModal.style.display = 'none';
             }, 300); // Match CSS transition duration
        });
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
            if (currentUser && currentUser.avatarUrl) {
                navProfileImg.src = currentUser.avatarUrl;
                navProfileImg.style.borderRadius = '50%'; // Ensure circle if custom avatar is used
            } else {
                 navProfileImg.src = 'Icons/user.png'; // Default if logged in but no custom avatar
                 navProfileImg.style.borderRadius = '0%'; // Reset if default icon isn't round
            }
        } else {
            navProfileImg.src = 'Icons/user.png'; // Default if logged out
             navProfileImg.style.borderRadius = '0%'; // Reset if default icon isn't round
        }
    };

    if (profileBtn) {
        profileBtn.addEventListener('click', (e) => {
            e.stopPropagation();
             // Prevent multiple modals opening immediately
            if (authModal && authModal.style.display !== 'none') authModal.style.display = 'none';
            if (profileModal && profileModal.style.display !== 'none') profileModal.style.display = 'none';

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
    if (authModal) authModal.addEventListener('click', e => (e.target === authModal) && (authModal.style.display = 'none'));
    if (profileModal) profileModal.addEventListener('click', e => (e.target === profileModal) && (profileModal.style.display = 'none'));
    
    // Close profile modal using the close button
    if (closeProfileBtn) closeProfileBtn.addEventListener('click', () => profileModal.style.display = 'none');

    // --- Sign Up Logic ---
    if (signUpActionBtn) {
        signUpActionBtn.addEventListener('click', () => {
            const name = signUpNameInput.value.trim();
            const email = signUpEmailInput.value.trim().toLowerCase();
            const password = signUpPasswordInput.value;
            if (!name || !email || !password) { alert('Please fill in all fields.'); return; }
            if (!/\S+@\S+\.\S+/.test(email)) { alert('Please enter a valid email address.'); return; }
            const db = getUsersDB();
            if (db[email]) { alert('An account with this email already exists.'); return; }
            
            // Add the new user with default avatar
            db[email] = { firstname: name, lastname: '', email: email, password: password, phone: '', location: '', cardnumber: '', avatarUrl: 'Icons/user.png' };
            saveUsersDB(db);
            setCurrentUserEmail(email);
            
            if (authModal) authModal.style.display = 'none';
            showSuccessModal('Account Created!', 'Welcome to FashioNear. You are now signed in.');
            // showSuccessModal now handles the reload
        });
    }

    // --- Sign In Logic ---
    if (signInActionBtn) {
        signInActionBtn.addEventListener('click', () => {
            const email = signInEmailInput.value.trim().toLowerCase();
            const password = signInPasswordInput.value;
            if (!email || !password) { alert('Please enter both email and password.'); return; }
            const user = getUsersDB()[email];
            if (!user || user.password !== password) { alert('Incorrect email or password.'); return; }
            
            setCurrentUserEmail(email);
            
            if (authModal) authModal.style.display = 'none';
            showSuccessModal('Sign In Successful!', 'Welcome back! Redirecting you now.');
             // showSuccessModal now handles the reload
        });
    }
    
    // --- Log Out Logic ---
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault(); // Prevent default link behavior
            logoutCurrentUser();
            if (profileModal) profileModal.style.display = 'none';
            showSuccessModal('Logged Out', 'You have been successfully logged out.');
            // showSuccessModal now handles the reload
        });
    }

    // --- Profile Form Save Logic ---
    if (userProfileForm) {
        userProfileForm.addEventListener('submit', (e) => {
            e.preventDefault();
            if (!isLoggedIn()) return;
            const db = getUsersDB();
            const email = getCurrentUserEmail();
            if (!db[email]) { console.error("Current user not found in DB during save attempt."); return; } // Safety check

            db[email].firstname = profileFirstNameInput ? profileFirstNameInput.value.trim() : db[email].firstname;
            db[email].lastname = profileLastNameInput ? profileLastNameInput.value.trim() : db[email].lastname;
            db[email].phone = profilePhoneInput ? profilePhoneInput.value.trim() : db[email].phone;
            db[email].location = profileLocationInput ? profileLocationInput.value.trim() : db[email].location;
            db[email].cardnumber = profileCardNumberInput ? profileCardNumberInput.value.trim() : db[email].cardnumber;
            
            saveUsersDB(db);
            loadProfileData(); // Reload data to update displayed name/location/avatar in modal
            if (profileModal) profileModal.style.display = 'none';
            showSuccessModal('Profile Saved', 'Your information has been updated successfully.');
             // showSuccessModal now handles the reload
        });
    }
    
    // --- Avatar Upload Logic ---
    if (avatarUploadInput) {
        avatarUploadInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file && isLoggedIn()) {
                 if (!file.type.startsWith('image/')) {
                     alert('Please upload an image file.');
                     return;
                 }
                 if (file.size > 5 * 1024 * 1024) { // 5MB limit
                     alert('File is too large. Max size is 5MB.');
                     return;
                 }
                const reader = new FileReader();
                reader.onload = function(event) {
                    const avatarUrl = event.target.result;
                    const db = getUsersDB();
                    const email = getCurrentUserEmail();
                    if (!db[email]) { console.error("Current user not found in DB during avatar upload."); return; } // Safety check
                    db[email].avatarUrl = avatarUrl;
                    saveUsersDB(db);
                    loadProfileData(); // Reload data to update avatar preview and nav icon
                }
                reader.onerror = function() {
                    console.error("Error reading file:", reader.error);
                     alert('Could not read the image file.');
                }
                reader.readAsDataURL(file);
            } else if (file && !isLoggedIn()) {
                alert('Please sign in to upload an avatar.');
            }
             // Reset file input so same file can be selected again
            e.target.value = '';
        });
    }


    // --- INITIALIZATION ---
    updateNavIcon(); // Update the navbar profile icon on load
    // The global updateCartIcon is called by auth.js on DOMContentLoaded (this script itself)
    // window.updateCartIcon(); is already called above when defined
});
```

**--- START OF FILE api-integration.js ---**

(Modified to remove `displayProducts` and potentially update API base URL)

```javascript
const API_BASE_URL = 'http://localhost:5000/api'; // Adjust if your Flask app is at a different base path

async function fetchProducts(category = '') {
    // This function fetches products from your *products* endpoint, not the AI search endpoints.
    // It's used for displaying category pages or the initial homepage grid.
    let url = `${API_BASE_URL}/Products?numberOfProduct=100`; // Example products endpoint
    if (category) {
        url += `&categoryName=${category}`;
    }
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json(); // API response structure {isCompleteSuccessfully, data, errorMessages}

        if (!result.isCompleteSuccessfully) {
             throw new Error(`API error: ${result.errorMessages ? result.errorMessages.join(', ') : 'Unknown error'}`);
        }

        // The successful data is in result.data
        const products = Array.isArray(result.data) ? result.data : [];
        return products; // Returns the array of products
    } catch (error) {
        console.error("Error fetching products:", error);
        // Check if displayProducts exists before calling it (it lives in product-grid.js now)
        if (typeof displayProducts === 'function') {
             // Display an empty grid and an error message using the display function structure
             displayProducts([], 'product-grid'); // Assuming 'product-grid' is the default container
             const gridContainer = document.getElementById('product-grid');
             if(gridContainer) {
                 gridContainer.innerHTML = `<div style="text-align: center; padding: 50px;"><p>Error loading products: ${error.message}</p></div>`;
             }
        } else {
            // Fallback error message if displayProducts isn't available yet
             const fallbackContainer = document.getElementById('product-grid') || document.body;
             fallbackContainer.innerHTML = `<div style="text-align: center; padding: 50px;"><p>Error loading products: ${error.message}</p></div>`;
        }
        return []; // Return an empty array in case of an error
    }
}

// displayProducts function is now defined in product-grid.js

```

**--- START OF FILE cart.js ---**

(No changes needed in this file, it uses `localStorage` and the global `updateCartIcon`).

```javascript
document.addEventListener('DOMContentLoaded', () => {
    // --- STATE & CONSTANTS ---
    const PROCESSING_FEE = 80.00;
    // Promo thresholds are hardcoded here, could potentially come from backend
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
    const promoItems = document.querySelectorAll('.promotions .promo-item'); // Get promo items
    const checkoutBtn = document.querySelector('.checkout-btn'); // Get checkout button

    // --- FUNCTIONS ---
    const saveCart = () => {
        localStorage.setItem('shoppingCart', JSON.stringify(cart));
    };
    
    const renderCartItems = () => {
        cartItemsContainer.innerHTML = ''; 
        if (cart.length === 0) {
            cartItemsContainer.innerHTML = '<p style="text-align:center; padding: 2rem; color: #8a8a8a;">Your cart is empty. <a href="All.html" style="color: coral;">Go shopping!</a></p>';
            // Disable checkout button if cart is empty
            if (checkoutBtn) checkoutBtn.disabled = true;
            return;
        }

        // Enable checkout button if cart is not empty
        if (checkoutBtn) checkoutBtn.disabled = false;


        cart.forEach(item => {
            const price = parseFloat(item.price) || 0;
            const itemTotal = price * item.quantity;
            const itemEl = document.createElement('div');
            itemEl.className = 'cart-item';
            
            const displaySize = item.size || 'N/A';
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
        const subtotal = cart.reduce((sum, item) => sum + (parseFloat(item.price) * item.quantity), 0);
        
        // --- Coupon Logic Placeholder ---
        // const discount = applyCoupon(subtotal, couponInput ? couponInput.value : '');
        // const subtotalAfterDiscount = subtotal - discount;
        // subtotalValueEl.textContent = `${subtotalAfterDiscount.toFixed(2)}LE`;
        // --- End Coupon Logic ---

        const totalInPounds = subtotal + PROCESSING_FEE; // Assuming PROCESSING_FEE is always added
        
        // Update summary values based on calculated totals
        if (subtotalValueEl) subtotalValueEl.textContent = `${subtotal.toFixed(2)}LE`;
        if (processingFeeEl) processingFeeEl.textContent = `${PROCESSING_FEE.toFixed(2)}LE`;
        if (totalValueEl) totalValueEl.textContent = `${totalInPounds.toFixed(2)}LE`; 
        if (grandTotalValueEl) grandTotalValueEl.textContent = `${totalInPounds.toFixed(2)}LE`; 
        
        // updateCartIcon is now called by auth.js on DOMContentLoaded, and also called below when rendering/calculating

        updateProgressBar(subtotal);
        updatePromos(subtotal);
        
         // Ensure updateCartIcon is available globally before calling
        if (window.updateCartIcon) {
             window.updateCartIcon();
        }
    };

     // Example applyCoupon function (placeholder)
     /*
     const applyCoupon = (subtotal, couponCode) => {
         let discount = 0;
         // Example coupon logic:
         if (couponCode === 'SAVE10' && subtotal >= 100) { // Add minimum threshold for coupon
             discount = subtotal * 0.10; // 10% off
         }
         // Add more coupon logic here
         return discount;
     };
     */


    const updateProgressBar = (subtotal) => {
        if (!progressBar) return;
        const progressPercentage = Math.min((subtotal / MAX_PROMO_VALUE) * 100, 100);
        progressBar.style.width = `${progressPercentage}%`;
    };

    const updatePromos = (subtotal) => {
        promoItems.forEach(promoEl => { // Loop through all promo items
             const promoId = promoEl.id.split('-')[1]; // Extract ID from element ID (e.g., '1' from 'promo-1')
             const threshold = PROMO_THRESHOLDS[promoId]; // Get the threshold for this ID
             if (threshold !== undefined) { // Check if the threshold exists in the map
                if (subtotal >= threshold) {
                    promoEl.classList.add('active');
                } else {
                    promoEl.classList.remove('active');
                }
             }
        });
    };
    
    const handleCartUpdate = (e) => {
        const target = e.target;
        const qtyBtn = target.closest('.qty-btn');
        const removeBtn = target.closest('.remove-btn');

        if (!qtyBtn && !removeBtn) {
            // If the click target is an image or icon inside the button, stop propagation
            // but let the click bubble up to the button itself.
            if (target.tagName === 'IMG' || target.tagName === 'I') {
                 e.stopPropagation();
            }
            return; // Exit if the click is not on a relevant button.
        }
        
        // Stop propagation on the button itself to prevent it from being handled elsewhere
        if (qtyBtn) e.stopPropagation();
        if (removeBtn) e.stopPropagation();


        const itemId = (qtyBtn || removeBtn).dataset.id;
        const itemSize = (qtyBtn || removeBtn).dataset.size;

        const itemIndex = cart.findIndex(i => {
            const cartItemSize = i.size || 'N/A';
            const clickedItemSize = itemSize || 'N/A'; 
            return String(i.id) === String(itemId) && cartItemSize === clickedItemSize;
        });

        if (itemIndex === -1) {
            console.error("Item not found in cart for update/removal.");
            return; 
        }

        if (qtyBtn) {
            const action = qtyBtn.dataset.action;
            if (action === 'increase') {
                cart[itemIndex].quantity++;
            } else if (action === 'decrease') {
                if (cart[itemIndex].quantity > 1) {
                    cart[itemIndex].quantity--;
                } else {
                    // Remove item if quantity is 1 and decrease is clicked
                    cart.splice(itemIndex, 1); 
                }
            }
        } else if (removeBtn) {
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
    if (cartItemsContainer) { 
         cartItemsContainer.addEventListener('click', handleCartUpdate);
    }
    
    // Add listener for coupon input if it affects total dynamically
    /*
    if (couponInput) {
        couponInput.addEventListener('input', updateSummary); 
    }
    */

    // --- INITIALIZATION ---
    renderAndCalculate();
    // The global updateCartIcon is already called by auth.js on DOMContentLoaded
});
```

**--- START OF FILE change-password.js ---**

(No changes needed in this file).

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
        if (!yetiAvatar || !formWrapper) return;
        const rect = formWrapper.getBoundingClientRect();
        const formCenterX = rect.left + rect.width / 2;
        const mouseX = e.clientX;
        const delta = mouseX - formCenterX;

        let newState;
        if (delta < -70) {
            newState = yetiStates.lookLeft;
        } else if (delta > 100) {
            newState = yetiStates.lookFarRight;
        } else if (delta > 50) {
            newState = yetiStates.lookRight;
        } else {
            newState = yetiStates.default;
        }
        
        if (yetiAvatar.src.includes(newState)) return; 
        yetiAvatar.src = newState;
    }
    
    // By default, the yeti tracks the mouse
    document.addEventListener('mousemove', trackMouse);

    // --- Password Field Interactions (Covering Eyes) ---
    passwordFields.forEach(field => {
        field.addEventListener('focus', () => {
            // Stop eye-tracking and cover eyes
            document.removeEventListener('mousemove', trackMouse);
            yetiAvatar.src = yetiStates.covering;
            yetiAvatar.style.transform = 'scale(0.95)';
        });

        field.addEventListener('blur', () => {
            // Uncover eyes and resume eye-tracking
            yetiAvatar.src = yetiStates.default;
            yetiAvatar.style.transform = 'scale(1)';
             // Resume tracking only if no password field is focused
             let anyFieldFocused = false;
             passwordFields.forEach(f => { if (document.activeElement === f) anyFieldFocused = true; });
             if (!anyFieldFocused) {
                 document.addEventListener('mousemove', trackMouse);
             }
        });
    });

    // --- Password Visibility Toggle Interactions (Peeking) ---
    togglePasswordIcons.forEach(icon => {
        // When mouse is HELD DOWN, yeti peeks
        icon.addEventListener('mousedown', function (event) {
            event.preventDefault(); 
            if (yetiAvatar) yetiAvatar.src = yetiStates.peeking;

            const input = this.previousElementSibling;
            if (input) input.setAttribute('type', 'text');
            this.classList.replace('fa-eye-slash', 'fa-eye');
        });

        // When mouse is RELEASED, yeti goes back to covering eyes
        icon.addEventListener('mouseup', function () {
            if (yetiAvatar) yetiAvatar.src = yetiStates.covering;
            const input = this.previousElementSibling;
            if (input) input.setAttribute('type', 'password');
            this.classList.replace('fa-eye', 'fa-eye-slash');
        });

        // If mouse leaves while held down, also stop peeking
         icon.addEventListener('mouseleave', function () {
             const input = this.previousElementSibling;
             if(input && input.getAttribute('type') === 'text') {
                 if (yetiAvatar) yetiAvatar.src = yetiStates.covering;
                 input.setAttribute('type', 'password');
                 this.classList.replace('fa-eye', 'fa-eye-slash');
             }
        });
    });

    // --- Live Password Strength Validation ---
    const newPasswordInput = document.getElementById('new-password');
    const strengthMeter = document.getElementById('strength-meter');
    // Only query for bars if the strength meter exists
    const strengthBars = strengthMeter ? strengthMeter.querySelectorAll('span') : []; 

    // Only add listener if input and meter exist
    if (newPasswordInput && strengthMeter) {
        newPasswordInput.addEventListener('input', function() {
            const password = this.value;
            const strength = calculatePasswordStrength(password);
            updateStrengthMeter(strength);
        });
    } else if (newPasswordInput) {
         // If meter is missing, just clear strength related elements
         newPasswordInput.addEventListener('input', function() {
             console.warn("Password strength meter elements not found on the page.");
             // Optionally hide or clear related UI if they exist
         });
    }


    function calculatePasswordStrength(password) {
        let strength = 0;
        if (password.length > 0) strength = 1;
        if (password.length >= 8) strength = 2;
        if (password.length >= 8 && /[a-zA-Z]/.test(password) && /[0-9]/.test(password)) strength = 3;
        // Added check for minimum length 12 for strength 4, consistent with some standards
        if (password.length >= 12 && /[a-zA-Z]/.test(password) && /[0-9]/.test(password) && /[^A-Za-z0-9]/.test(password)) strength = 4; 
        return strength;
    }

    function updateStrengthMeter(strength) {
         if (!strengthMeter || strengthBars.length === 0) return; // Exit if meter/bars missing
        const strengthColors = [
            'var(--bar-default-color)', // 0
            'var(--bar-weak-color)',    // 1
            'var(--bar-medium-color)',   // 2
            'var(--bar-strong-color)',  // 3
            'var(--bar-strong-color)'   // 4 (or use a fifth color if available in CSS variables)
        ];
        
        strengthBars.forEach((bar, index) => {
            // Assign color based on the index up to the strength level
            // index 0 gets color for strength 1 if strength >= 1
            // index 1 gets color for strength 2 if strength >= 2, etc.
            if (index < strength) {
                // Use the color corresponding to the *current* strength level for all filled bars
                 bar.style.backgroundColor = strengthColors[strength]; 
                 // Alternative: Use color corresponding to the bar's level (more common gradient effect)
                 // bar.style.backgroundColor = strengthColors[index + 1]; // Need index+1 because colors array is 0-indexed but strength is 1-4
            } else {
                bar.style.backgroundColor = 'var(--bar-default-color)';
            }
        });
    }

    // Optional: Initial update of strength meter if password field isn't empty on load (e.g. from browser autofill)
    if(newPasswordInput && newPasswordInput.value) {
        const strength = calculatePasswordStrength(newPasswordInput.value);
        updateStrengthMeter(strength);
    }
});
```

**--- START OF FILE checkout.js ---**

(No changes needed in this file, it uses `localStorage` and the global `updateCartIcon`).

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
    const confirmPaymentBtn = document.getElementById('confirmPaymentBtn'); // Get the confirm button

    // Payment elements
    const paymentOptions = document.querySelectorAll('.radio-option');
    const creditCardForm = document.querySelector('.payment-information');
    
    // Form, Buttons and MODALS
    const shippingAddressInput = document.getElementById('shippingAddress');
    const cardNumberInput = document.getElementById('cardNumber');
    
    const authModal = document.getElementById('authModal');
    const orderSuccessModal = document.getElementById('orderSuccessModal');
    const cartEmptyModal = document.getElementById('cartEmptyModal');
    
    // Prompt Sign In Modal elements (used if user is not logged in)
    const signInPromptModal = document.getElementById('signInPromptModal'); // Assuming this exists based on HTML
    const promptSignInBtn = document.getElementById('promptSignInBtn');
    const promptCancelBtn = document.getElementById('promptCancelBtn');


    // Auth helpers
    const isLoggedIn = () => !!localStorage.getItem('currentUserEmail');

    // User DB helper (needed for loadUserData)
    const getUsersDB = () => JSON.parse(localStorage.getItem('usersDB')) || {};


    // --- FUNCTIONS ---
    function updateCheckoutSummary() {
        const subtotal = cart.reduce((sum, item) => sum + (parseFloat(item.price) * item.quantity), 0);
        const total = subtotal + PROCESSING_FEE;
        const formatPrice = (price) => `${price.toFixed(2)} LE`;
        
        if (subtotalEl) subtotalEl.textContent = formatPrice(subtotal);
        if (processingFeeEl) processingFeeEl.textContent = formatPrice(PROCESSING_FEE);
        if (totalEl) totalEl.textContent = formatPrice(total);
        if (grandTotalEl) grandTotalEl.textContent = formatPrice(total);
        if (confirmPaymentAmountEl) confirmPaymentAmountEl.textContent = formatPrice(total);
    }

    function setupPaymentSelection() {
         // Ensure the credit card form is initially hidden if not selected
        if (creditCardForm) creditCardForm.style.display = 'none'; 

        paymentOptions.forEach(option => {
            option.addEventListener('click', () => {
                // Remove 'active' class from all and add 'inactive'
                paymentOptions.forEach(opt => {
                    opt.classList.remove('active');
                    opt.classList.add('inactive');
                });
                // Add 'active' class and remove 'inactive' from the clicked one
                option.classList.add('active');
                option.classList.remove('inactive');
                
                if (creditCardForm) {
                    const isCardSelected = option.hasAttribute('data-card-option');
                    creditCardForm.style.display = isCardSelected ? 'block' : 'none';
                }
            });
        });

        // Set the first option as active by default if available
        if (paymentOptions.length > 0) {
             paymentOptions[0].classList.add('active');
             paymentOptions[0].classList.remove('inactive');
              // Ensure CC form visibility matches the default active option
             if (creditCardForm && paymentOptions[0].hasAttribute('data-card-option')) {
                 creditCardForm.style.display = 'block';
             } else if (creditCardForm) {
                 creditCardForm.style.display = 'none';
             }
        }
    }

    function loadUserData() {
        if (isLoggedIn()) {
            const users = getUsersDB(); // Use the helper function
            const currentUserEmail = localStorage.getItem('currentUserEmail');
            const currentUser = users[currentUserEmail];
            if (currentUser) {
                // Safely populate inputs
                if (shippingAddressInput) shippingAddressInput.value = currentUser.location || '';
                 // Card number input might be disabled or handled differently based on security
                if (cardNumberInput) cardNumberInput.value = currentUser.cardnumber || '';
                 // Name on card might also be pre-filled
                const nameOnCardInput = document.getElementById('nameOnCard');
                if (nameOnCardInput) nameOnCardInput.value = `${currentUser.firstname || ''} ${currentUser.lastname || ''}`.trim();
            }
        }
    }

    function processOrder() {
        const currentUserEmail = localStorage.getItem('currentUserEmail');
        
        const cartItems = JSON.parse(localStorage.getItem('shoppingCart')) || [];
        if(cartItems.length === 0) {
             // This case should be handled by initialChecks and the cart empty modal
            console.warn('Attempted to process empty cart.');
            return;
        }

        const subtotal = cartItems.reduce((sum, item) => sum + (parseFloat(item.price) * item.quantity), 0);
        const total = subtotal + PROCESSING_FEE;
        
        const newOrder = {
            // Use a more robust ID if possible, or rely on backend
            id: `FN${Date.now()}${Math.floor(Math.random() * 1000)}`, // Timestamp + random for uniqueness
            date: new Date().toISOString(), 
            status: 'Processing', 
            total: total,
            items: cartItems, 
        };
        
        let ordersDB = JSON.parse(localStorage.getItem('ordersDB')) || {};
        if (!ordersDB[currentUserEmail]) {
            ordersDB[currentUserEmail] = [];
        }
        ordersDB[currentUserEmail].unshift(newOrder); 
        
        localStorage.setItem('ordersDB', JSON.stringify(ordersDB));

        localStorage.removeItem('shoppingCart');

        // Update cart icon in navbar using the global function
        if(window.updateCartIcon) {
            window.updateCartIcon();
        }

        // Show the success modal
        if (orderSuccessModal) {
            orderSuccessModal.style.display = 'flex';
        }
    }

    function initialChecks() {
        if (cart.length === 0) {
            if (cartEmptyModal) cartEmptyModal.style.display = 'flex';
            if (confirmPaymentBtn) {
                confirmPaymentBtn.disabled = true;
                confirmPaymentBtn.style.backgroundColor = '#ccc';
                confirmPaymentBtn.style.cursor = 'not-allowed';
            }
        } else {
            loadUserData(); // Load user data if cart is not empty
        }
    }

    // --- EVENT LISTENERS ---
    if (confirmPaymentBtn) {
        confirmPaymentBtn.addEventListener('click', () => {
            if (cart.length === 0) {
                 // This click handler shouldn't be reachable if button is disabled, but safety
                 if (cartEmptyModal) cartEmptyModal.style.display = 'flex';
                 return;
            }
            
            if (isLoggedIn()) {
                processOrder();
            } else {
                 // Show the Sign In prompt modal instead of the full auth modal immediately
                if (signInPromptModal) signInPromptModal.style.display = 'flex'; 
            }
        });
    }

    // Listeners for the Sign In Prompt Modal
    if (promptSignInBtn) {
         promptSignInBtn.addEventListener('click', () => {
             if (signInPromptModal) signInPromptModal.style.display = 'none';
             if (authModal) {
                 authModal.style.display = 'flex';
                 // Optionally set the auth modal to the sign-in view if it has states
                 const authBox = document.getElementById('auth-box');
                 if (authBox) authBox.classList.remove("right-panel-active"); // Assuming sign-in is default
             }
         });
    }

    if (promptCancelBtn) {
         promptCancelBtn.addEventListener('click', () => {
             if (signInPromptModal) signInPromptModal.style.display = 'none';
         });
    }


    // --- INITIALIZATION ---
    updateCheckoutSummary();
    setupPaymentSelection();
    initialChecks();
});
```

**--- START OF FILE men-page-script.js ---**

(Remove this file. Its "Add to Cart" and `updateCartCount` logic are duplicated by `product-grid.js` and `auth.js`).

**--- START OF FILE orders.js ---**

(No changes needed in this file).

```javascript
document.addEventListener('DOMContentLoaded', () => {
    // --- DATA HELPERS ---
    const getOrdersDB = () => JSON.parse(localStorage.getItem('ordersDB')) || {};
    const getCurrentUserEmail = () => localStorage.getItem('currentUserEmail');
    const saveOrdersDB = (db) => localStorage.setItem('ordersDB', JSON.stringify(db));

    // --- DOM ELEMENTS ---
    const orderListContainer = document.getElementById('order-list-container');
    const emptyView = document.getElementById('empty-orders-view');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const clearHistoryContainer = document.getElementById('clear-history-container');
    const clearHistoryBtn = document.getElementById('clear-history-btn');

    // Modal DOM Elements (reused from checkout.css styles)
    const confirmClearModal = document.getElementById('confirmClearModal');
    const confirmClearBtn = document.getElementById('confirm-clear-btn');
    const cancelClearBtn = document.getElementById('cancel-clear-btn');
    const historyClearedModal = document.getElementById('historyClearedModal');
    const closeHistoryClearedModalBtn = document.getElementById('closeHistoryClearedModalBtn');

    // --- RENDER FUNCTIONS ---
    const renderOrderItems = (items) => {
        // Using encodeURIComponent for safety when passing data in URL
        return items.map(item => `
            <a href="sproduct.html?id=${encodeURIComponent(item.id || '')}&name=${encodeURIComponent(item.name || '')}&price=${encodeURIComponent(item.price || '0')}&desc=${encodeURIComponent(item.description || '')}&img=${encodeURIComponent(item.imgSrc || 'Images/placeholder.png')}" class="order-item">
                <img src="${item.imgSrc || 'Images/placeholder.png'}" alt="${item.name || 'Product image'}" onerror="this.src='Images/placeholder.png'">
                <div class="order-item-details">
                    <h4>${item.name || 'Unknown Product'}</h4>
                    <p>Qty: ${item.quantity || 1} &nbsp;&nbsp; Price: ${((item.price || 0) * (item.quantity || 1)).toFixed(2)} LE</p>
                </div>
            </a>
        `).join('');
    };

    const renderOrders = (ordersToDisplay) => { // Removed isFilterAction param, logic simplified
        const currentUser = getCurrentUserEmail();
        const allUserOrders = (getOrdersDB()[currentUser] || []);

        // Determine if the *overall* history is empty
        const isHistoryEmpty = allUserOrders.length === 0;

        // Determine if the *filtered* list is empty
        const isFilteredListEmpty = ordersToDisplay.length === 0;

        // Toggle main empty view based on overall history
        if (isHistoryEmpty) {
            orderListContainer.innerHTML = '';
            if (emptyView) emptyView.style.display = 'block';
            if (clearHistoryContainer) clearHistoryContainer.style.display = 'none';
            const filtersEl = document.querySelector('.order-filters');
            if (filtersEl) filtersEl.style.display = 'none';
            return; // Exit if no history at all
        }

        // If there is some history, hide the main empty view and show controls
        if (emptyView) emptyView.style.display = 'none';
        if (clearHistoryContainer) clearHistoryContainer.style.display = 'block';
        const filtersEl = document.querySelector('.order-filters');
        if (filtersEl) filtersEl.style.display = 'flex';

        // Display filtered orders or a message if filtered list is empty
        if (isFilteredListEmpty) {
            // Display message for empty filtered result
            orderListContainer.innerHTML = `<p style="text-align:center; padding: 2rem; color: var(--secondary-text);">You have no orders with this status.</p>`;
        } else {
            // Render the orders
            orderListContainer.innerHTML = ordersToDisplay.map(order => `
                <div class="order-card" data-order-status="${order.status || 'Unknown'}">
                    <div class="order-card-header">
                        <div class="order-info">
                            <strong>Order ID:</strong> <span class="order-id">#${order.id || 'N/A'}</span><br>
                            <strong>Date:</strong> ${order.date ? new Date(order.date).toLocaleDateString() : 'N/A'}
                        </div>
                        <span class="order-status status-${order.status || 'Unknown'}">${order.status || 'Unknown Status'}</span>
                    </div>
                    <div class="order-items-list">
                        ${renderOrderItems(order.items || [])}
                    </div>
                    <div class="order-card-footer">
                        <button class="details-btn" disabled>Track Order</button> <!-- Track Order button likely not functional yet -->
                        <div class="total-amount">
                            <span>Total:</span> ${(order.total || 0).toFixed(2)} LE
                        </div>
                    </div>
                </div>
            `).join('');
        }
    };
    
    // --- MAIN LOGIC & EVENT LISTENERS ---
    const initializeOrdersPage = () => {
        const currentUser = getCurrentUserEmail();
        if (!currentUser) {
            if (orderListContainer) orderListContainer.innerHTML = `<h3 class="text-center p-5" style="color: var(--primary-text);">Please log in to view your orders.</h3>`;
            if (emptyView) emptyView.style.display = 'none'; // Hide empty view, show login prompt
            if (clearHistoryContainer) clearHistoryContainer.style.display = 'none';
            const filtersEl = document.querySelector('.order-filters');
            if (filtersEl) filtersEl.style.display = 'none';
            return;
        }

        const allUserOrders = getOrdersDB()[currentUser] || [];
        
        renderOrders(allUserOrders); // Initial render with all orders

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
                
                renderOrders(filteredOrders); // Render filtered orders
            });
        });
        
        // --- Modal-based clear history logic ---
        if(clearHistoryBtn) {
            clearHistoryBtn.addEventListener('click', () => {
                 // Hide other modals if they are open
                 if (historyClearedModal) historyClearedModal.style.display = 'none';
                if (confirmClearModal) confirmClearModal.style.display = 'flex';
            });
        }
        
        if(cancelClearBtn) {
            cancelClearBtn.addEventListener('click', () => {
                if (confirmClearModal) confirmClearModal.style.display = 'none';
            });
        }
        
        if(confirmClearBtn) {
            confirmClearBtn.addEventListener('click', () => {
                let ordersDB = getOrdersDB();
                const currentUser = getCurrentUserEmail(); // Re-get current user for safety
                 if (ordersDB[currentUser]) {
                     ordersDB[currentUser] = []; // Clear the user's orders array
                     saveOrdersDB(ordersDB);
                 } else {
                     console.warn("Attempted to clear history for user with no entry.");
                 }

                renderOrders([]); // Re-render with empty array
                
                if (confirmClearModal) confirmClearModal.style.display = 'none';
                if (historyClearedModal) historyClearedModal.style.display = 'flex';
            });
        }
        
        // Click listener for the success modal close button
        if(closeHistoryClearedModalBtn) {
            closeHistoryClearedModalBtn.addEventListener('click', () => {
                if (historyClearedModal) historyClearedModal.style.display = 'none';
            });
        }
         // Allow clicking outside the history cleared modal to close it
        if (historyClearedModal) {
            historyClearedModal.addEventListener('click', (e) => {
                 if (e.target === historyClearedModal) {
                     historyClearedModal.style.display = 'none';
                 }
            });
        }
         // Allow clicking outside the confirm clear modal to close it
        if (confirmClearModal) {
             confirmClearModal.addEventListener('click', (e) => {
                 if (e.target === confirmClearModal) {
                     confirmClearModal.style.display = 'none';
                 }
             });
        }
    };

    // --- INITIALIZE ---
    initializeOrdersPage();
});
```

**--- START OF FILE popup.js ---**

(Modified to integrate API calls for similar items and price prediction, and update response handling)

```javascript
// --- START: Visual Search Modal Logic ---

document.addEventListener('DOMContentLoaded', () => {
    // --- Visual Search Modal elements
    const visualSearchModal = document.getElementById("visualSearchModal");
    const openModalButtons = document.querySelectorAll("#visualSearchBtn, #navVisualSearchBtn");
    // Query for all close buttons with this class, as there might be multiple modals using it
    const closeVisualSearchBtn = document.querySelector(".visual-search-modal-content .visual-search-close-btn"); // Get the close btn specific to this modal

    // --- File handling elements
    const dropZone = document.querySelector(".visual-search-drop-zone");
    const fileInput = document.getElementById("visualSearchFileInput");
    const uploadBtn = document.querySelector(".visual-search-upload-btn");
    const errorMsg = document.getElementById("visualSearchError");
    const previewArea = document.getElementById("visualSearchPreview");
  
    // --- Action elements
    const actionsContainer = document.getElementById("visualSearchActions");
    const findSimilarBtn = document.getElementById("findSimilarBtn");
    const predictPriceBtn = document.getElementById("predictPriceBtn");

    // --- Price Prediction Modal elements
    const pricePredictionModal = document.getElementById("pricePredictionModal");
    // Get the close btn specific to this modal
    const closePricePredictionBtn = pricePredictionModal ? pricePredictionModal.querySelector(".visual-search-close-btn") : null; 
    const predictedPriceText = document.getElementById("predicted-price-text");

    // A variable to hold the image data (base64)
    let uploadedImageData = null;

    // Backend API base URL - adjust if your Flask app is different
    // Assumes AI endpoints are under /api/ai
    const API_BASE_URL = 'http://localhost:5000/api/ai'; 

    // Basic check if essential elements are present before adding listeners
    if (!visualSearchModal || !dropZone || !fileInput || !uploadBtn || !errorMsg || !previewArea || !actionsContainer || !findSimilarBtn || !predictPriceBtn || !pricePredictionModal || !predictedPriceText) {
      console.warn("Essential visual search modal elements missing from the page. Aborting full setup.");
      return;
    }
     // Check if the close button for the price modal was found
    if (!closePricePredictionBtn) {
         console.warn("Price prediction modal close button missing. Price modal cannot be closed via its button.");
    }


    function openVisualSearchModal() {
        visualSearchModal.style.display = "flex";
        // Use requestAnimationFrame for better transition timing
        requestAnimationFrame(() => {
             requestAnimationFrame(() => {
                 visualSearchModal.classList.add('show'); // Assuming CSS transition class exists
             });
        });
      clearVisualSearchState();
    }
  
    function closeVisualSearchModal() {
        visualSearchModal.classList.remove('show'); // Assuming CSS transition class exists
        // Hide after transition
         setTimeout(() => {
             visualSearchModal.style.display = "none";
         }, 300); // Match CSS transition duration

      clearVisualSearchState();
    }

    function openPricePredictionModal(message = "Loading...") {
         predictedPriceText.textContent = message;
         pricePredictionModal.style.display = 'flex';
          // Use requestAnimationFrame for better transition timing
         requestAnimationFrame(() => {
             requestAnimationFrame(() => {
                 pricePredictionModal.classList.add('show'); // Assuming CSS transition class exists
             });
        });
    }

    function closePricePredictionModal() {
         pricePredictionModal.classList.remove('show'); // Assuming CSS transition class exists
         // Hide after transition
         setTimeout(() => {
            pricePredictionModal.style.display = "none";
            predictedPriceText.textContent = "The estimated price range for this item is..."; // Reset text
         }, 300); // Match CSS transition duration
    }
  
    // Resets the visual search modal to its initial state
    function clearVisualSearchState() {
      errorMsg.textContent = "";
      previewArea.innerHTML = "";
      actionsContainer.style.display = "none";
      dropZone.style.display = "block";
      dropZone.classList.remove("drag-over");
      fileInput.value = null;
      uploadedImageData = null;
       // Reset action buttons state if needed
      findSimilarBtn.disabled = false;
      predictPriceBtn.disabled = false;
    }
  
    function handleFile(file) {
      clearVisualSearchState();
  
      if (!file) {
        errorMsg.textContent = "No file selected or dropped.";
        return;
      }
  
      const acceptedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
      if (!acceptedTypes.includes(file.type)) {
        errorMsg.textContent = `Unsupported file type. Please upload JPEG, PNG, GIF, or WebP.`; // Added GIF
        return;
      }
  
      const maxSize = 5 * 1024 * 1024; // 5MB
      if (file.size > maxSize) {
        errorMsg.textContent = `File is too large. Max size is 5MB.`;
        return;
      }
      
       // --- Show Preview ---
       const reader = new FileReader();
       reader.onload = function (e) {
           uploadedImageData = e.target.result;
           const img = document.createElement('img');
           img.src = uploadedImageData;
           img.alt = "Image preview";
           previewArea.appendChild(img);
           dropZone.style.display = "none"; // Hide drop zone

           // Show actions after successful preview
           actionsContainer.style.display = "flex"; 
       };
       reader.onerror = function () {
         errorMsg.textContent = "Could not read the selected file.";
         uploadedImageData = null; // Ensure data is null on error
       };
       reader.readAsDataURL(file);
    }

    // Function to call the price prediction API
    async function predictPriceFromAPI(imageData) {
        // Show loading state in the price modal
        openPricePredictionModal("Analyzing image...");

        try {
            // API expects POST with JSON body containing 'image'
            const response = await fetch(`${API_BASE_URL}/predict-price`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // Add any other required headers (e.g., API key)
                },
                body: JSON.stringify({
                    image: imageData // Sending Base64 data
                })
            });

            // Handle non-OK HTTP responses
            if (!response.ok) {
                 const errorBody = await response.text(); // Get response body for more details
                throw new Error(`HTTP error! status: ${response.status} - ${errorBody}`);
            }

            const result = await response.json(); // Parse the JSON response
            
            // Handle API-level errors (if isCompleteSuccessfully is false or has errorMessages)
            if (result.isCompleteSuccessfully === false) {
                 throw new Error(`API error: ${result.errorMessages ? result.errorMessages.join(', ') : 'Unknown API error'}`);
            }
            // Check specific structure for price prediction result
             if (result.predicted_price_egp === undefined || result.predicted_price_egp === null) {
                 throw new Error("API did not return a predicted price.");
             }


            // Display the predicted price
            predictedPriceText.textContent = `Estimated Price: ${result.predicted_price_egp.toFixed(2)} EGP`; // Format price


        } catch (error) {
            console.error('Price prediction error:', error);
            predictedPriceText.textContent = `Error predicting price: ${error.message}`;
            // Keep the price modal open to show the error
        }
    }

    // Function to call the visual search API
    async function searchSimilarFromAPI(imageData) {
         // Show loading message in the visual search modal itself before redirect
         errorMsg.textContent = "Searching for similar items..."; // Replaces any file error
         // Optionally disable buttons during search
         findSimilarBtn.disabled = true;
         predictPriceBtn.disabled = true;


        try {
            // Store the image for the results page
            // We store the raw image data so resultpage can display the query image
            sessionStorage.setItem('visualSearchQueryImage', imageData);
            
            // API expects POST with JSON body containing 'image'
            const response = await fetch(`${API_BASE_URL}/search-by-image`, { // Or maybe /find_similar if that's the POST endpoint
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // Add any other required headers
                },
                body: JSON.stringify({
                    image: imageData // Sending Base64 data
                })
            });

             // Handle non-OK HTTP responses
            if (!response.ok) {
                 const errorBody = await response.text();
                throw new Error(`HTTP error! status: ${response.status} - ${errorBody}`);
            }

            const result = await response.json();
            
            // Handle API-level errors
            if (result.isCompleteSuccessfully === false) {
                 throw new Error(`API error: ${result.errorMessages ? result.errorMessages.join(', ') : 'Unknown API error'}`);
            }
             // Check specific structure for similar items result
             if (!Array.isArray(result.data)) {
                 throw new Error("API did not return a list of products.");
             }


            // Store the search results for the results page
            // Store result.data as this is the array of products
            sessionStorage.setItem('visualSearchResults', JSON.stringify(result.data)); 
            
            // Navigate to results page after successful API call and data saving
            window.location.href = 'resultpage.html'; 
            
        } catch (error) {
            console.error('Visual search error:', error);
             // Display error in the visual search modal
            errorMsg.textContent = `Error searching: ${error.message}`; 
            // Re-enable buttons and show drop zone
            findSimilarBtn.disabled = false;
            predictPriceBtn.disabled = false;
            dropZone.style.display = "block"; 
            actionsContainer.style.display = "none"; // Hide actions
            previewArea.innerHTML = ""; // Clear preview
            uploadedImageData = null; // Clear data
            fileInput.value = null; // Reset file input

        }
    }
  
    // --- EVENT LISTENERS ---
  
    // Open visual search modal from various buttons
    openModalButtons.forEach(btn => btn.addEventListener("click", (e) => { 
        e.preventDefault(); 
        e.stopPropagation(); 
        // Close other modals before opening visual search
        if (pricePredictionModal && pricePredictionModal.style.display !== 'none') closePricePredictionModal();
        // Ensure auth modal is closed if open (auth.js also handles this)
        const authModal = document.getElementById('authModal');
        if (authModal && authModal.style.display !== 'none') authModal.style.display = 'none';

        openVisualSearchModal(); 
    }));
  
    // --- Listeners for closing modals
    // Close visual search modal using its specific close button
    if (closeVisualSearchBtn) { // Check if element exists
        closeVisualSearchBtn.addEventListener("click", closeVisualSearchModal);
    }
    // Close visual search modal by clicking outside content
    visualSearchModal.addEventListener("click", (e) => e.target === visualSearchModal && closeVisualSearchModal());

    // Close price prediction modal using its specific close button
    if (closePricePredictionBtn) { // Check if element exists
        closePricePredictionBtn.addEventListener("click", closePricePredictionModal);
    }
    // Close price prediction modal by clicking outside content
    pricePredictionModal.addEventListener("click", (e) => e.target === pricePredictionModal && closePricePredictionModal());


    // --- Listeners for file handling
    uploadBtn.addEventListener("click", () => fileInput.click());
    fileInput.addEventListener("change", (e) => {
        handleFile(e.target.files[0]);
        e.target.value = null; // Clear file input after handling
    });
    // Drag and Drop listeners
    if(dropZone) {
        dropZone.addEventListener("dragenter", (e) => { e.preventDefault(); dropZone.classList.add("drag-over"); });
        dropZone.addEventListener("dragover",  (e) => { e.preventDefault(); e.dataTransfer.dropEffect = 'copy'; });
        dropZone.addEventListener("dragleave", () => dropZone.classList.remove("drag-over"));
        dropZone.addEventListener("drop", (e) => {
            e.preventDefault();
            dropZone.classList.remove("drag-over");
            handleFile(e.dataTransfer.files[0]);
            e.dataTransfer.clearData(); // Clear drag data
        });
    }

    // --- Listeners for the Visual Search action buttons
    findSimilarBtn.addEventListener('click', () => {
        if (uploadedImageData) {
            searchSimilarFromAPI(uploadedImageData);
        } else {
            errorMsg.textContent = "An error occurred. Please upload the image again.";
            actionsContainer.style.display = "none";
            dropZone.style.display = "block";
        }
    });

    predictPriceBtn.addEventListener('click', () => {
        if (uploadedImageData) {
            // Close the visual search modal before opening the price prediction modal
            closeVisualSearchModal(); 
            predictPriceFromAPI(uploadedImageData);
        } else {
            errorMsg.textContent = "An error occurred. Please upload the image again.";
            actionsContainer.style.display = "none";
            dropZone.style.display = "block";
        }
    });
});

```

**--- START OF FILE predict-price.js ---**

(Remove this file. Its functionality is covered by `product-grid.js` and price prediction API calls are in `popup.js`).

**--- START OF FILE product-grid.js ---**

(Add the `displayProducts` function definition here and keep the click handling for product cards).

```javascript
// Define displayProducts globally or ensure it's accessible where needed
// Attaching to window makes it globally available across scripts
window.displayProducts = function(products, containerId) {
    const productGrid = document.getElementById(containerId);
    if (!productGrid) {
        console.error(`Product grid container with ID ${containerId} not found.`);
        return;
    }
    productGrid.innerHTML = ''; // Clear existing products

    // Remove loading spinner if it exists within this container
     const loadingSpinner = productGrid.querySelector('.loading-spinner');
     if(loadingSpinner) loadingSpinner.remove();


    if (!Array.isArray(products) || products.length === 0) {
        productGrid.innerHTML = '<div style="text-align: center; padding: 50px;"><p>No products available at the moment.</p></div>';
        return;
    }

    products.forEach(product => {
        const productElement = document.createElement('div');
        productElement.classList.add('pro');
        // Use nullish coalescing operator (??) for better handling of null/undefined
        productElement.setAttribute('data-id', product.productId ?? product.id ?? ''); // Check for productId first, then id
        productElement.setAttribute('data-name', product.name ?? 'Unknown Product');
        productElement.setAttribute('data-price', product.price ?? '0');
        productElement.setAttribute('data-desc', product.description ?? product.name ?? ''); // Use description or name
        // Add category info as data attributes as well, useful for filtering/related products
        productElement.setAttribute('data-category-id', product.categoryId ?? '');
        productElement.setAttribute('data-category-name', product.categoryName ?? '');


        const productId = productElement.dataset.id; // Use ID from data attribute after setting
        const productName = productElement.dataset.name;
        const productPrice = productElement.dataset.price;
        const productBrand = product.brand || productElement.dataset.categoryName || 'FashioNear'; // Prefer brand if available, else category name
        const productImage = product.image ?? product.imageUrl ?? product.imgSrc ?? 'Images/placeholder.png'; // Check multiple possible image keys


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
};


document.addEventListener('DOMContentLoaded', () => {

    // updateCartIcon definition is now the first thing in this file
    // and it is called here to ensure it runs on DOMContentLoaded

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
                    e.stopPropagation(); // Prevent the click from bubbling up and triggering card navigation


                    const product = {
                         // Ensure IDs and prices are read from data attributes as strings and converted
                        id: productCard.dataset.id, 
                        name: productCard.dataset.name,
                        price: parseFloat(productCard.dataset.price),
                        imgSrc: productCard.querySelector('.pro-img-container img')?.src, // Get from image container
                        // Size needs to be selected on the s product page.
                        // When adding from grid, a default is often used or size selection is not possible.
                        // Assuming default 'M' or requiring s product page for size selection.
                        // Keeping 'M' for now based on previous men-page-script.js logic
                        size: 'M', 
                        quantity: 1
                    };

                    // Basic validation
                    if (!product.id || !product.name || isNaN(product.price)) {
                         console.error("Product data missing or invalid for Add to Cart:", productCard.dataset);
                         // Optionally show a user-friendly message
                         alert("Error adding product to cart. Missing data.");
                         return;
                    }
                    
                    let cart = JSON.parse(localStorage.getItem('shoppingCart')) || [];
                    // Find existing item by ID *and* size
                    let existingItem = cart.find(item => item.id === product.id && item.size === product.size);
                    
                    if (existingItem) {
                        existingItem.quantity++;
                    } else {
                        cart.push(product);
                    }
                    
                    localStorage.setItem('shoppingCart', JSON.stringify(cart));
                    window.updateCartIcon(); // Update the navbar icon

                    // Provide visual feedback
                    const originalIconHTML = addToCartBtn.innerHTML; // Store original icon HTML
                    addToCartBtn.innerHTML = `<i class="fas fa-check"></i>`; // Change icon to checkmark
                    addToCartBtn.disabled = true; // Disable button temporarily

                    setTimeout(() => { // Set a timer to revert the button state
                        addToCartBtn.innerHTML = originalIconHTML; // Restore original icon
                        addToCartBtn.disabled = false; // Re-enable button
                    }, 1500); // Timer duration: 1500 milliseconds (1.5 seconds)

                } else {
                    // --- B) HANDLE CLICKING THE CARD TO VIEW DETAILS --- (if not the cart button)
                    // Get product data from data attributes
                    const id = productCard.dataset.id;
                    const name = productCard.dataset.name;
                    const price = productCard.dataset.price;
                    const desc = productCard.dataset.desc;
                     // Get image source from the img tag inside the image container div
                    const imgSrc = productCard.querySelector('.pro-img-container img')?.src; 
                    
                    // Essential check to ensure the card has data to send
                    if (!id || !name || !price || !imgSrc) {
                         console.error("Cannot navigate, essential product data is missing from the card:", productCard.dataset);
                         alert("Error loading product details. Missing data.");
                         return;
                    }

                    // Build a URL with the product data as search parameters.
                    // encodeURIComponent is crucial to handle spaces and special characters.
                    const url = `sproduct.html?id=${encodeURIComponent(id)}&name=${encodeURIComponent(name)}&price=${encodeURIComponent(price)}&desc=${encodeURIComponent(desc)}&img=${encodeURIComponent(imgSrc)}`;
                    
                    // Redirect the user to the single product page
                    window.location.href = url;
                }
            });
        });
    }
});
```

**--- START OF FILE resultpage.js ---**

(Modified to use the shared `displayProducts` function and handle API response structure)

```javascript
document.addEventListener('DOMContentLoaded', () => {
    // DOM elements from resultpage.html
    const queryImageContainer = document.getElementById('query-image-container');
    const queryImageElement = document.getElementById('query-img');
    const productGrid = document.getElementById('product-grid'); // The main grid for results

    // Check if the shared displayProducts function is available
    if (typeof displayProducts !== 'function') {
        console.error("The required 'displayProducts' function is not available. Ensure product-grid.js is loaded.");
        // Display a fallback message
        if (productGrid) {
             productGrid.innerHTML = '<div style="text-align: center; padding: 50px;"><p>Error loading display functions.</p></div>';
        } else {
             console.error("Product grid container not found.");
        }
        return; // Stop execution if displayProducts is missing
    }


    // Check if all necessary elements are on the page for displaying the query image
    if (!queryImageContainer || !queryImageElement || !productGrid) {
        console.warn("Essential elements for result page display (query image or product grid) not fully found.");
        // Continue if productGrid is found, as we might still display results even without the query image preview
         if (!productGrid) return; // If product grid is also missing, nothing to do
    }


    // 1. Retrieve the image data URL from session storage
    const uploadedImageData = sessionStorage.getItem('visualSearchQueryImage');
    const searchResults = sessionStorage.getItem('visualSearchResults'); // This should be the API's 'data' array (JSON string)

    // 2. If image data exists, display the image and make the container visible
    if (uploadedImageData && queryImageElement && queryImageContainer) { // Check if elements exist before using them
        queryImageElement.src = uploadedImageData;
        queryImageContainer.style.display = 'block'; 
        // Optionally remove after display, but keeping it allows user to see what they searched
        // sessionStorage.removeItem('visualSearchQueryImage'); 
    } else {
        console.log("No visual search query image found in session storage or query image elements missing.");
         // Optionally hide the query image section header if the image isn't shown
         const queryHeader = document.querySelector('.result-page-header .container h4');
         if (queryHeader) queryHeader.style.display = 'none';
    }

    // 3. Display search results if available
    if (searchResults) {
        try {
            const products = JSON.parse(searchResults); // This should be the array of product objects
            
            // Check if the parsed data is an array
             if (!Array.isArray(products)) {
                 console.error('Search results from sessionStorage are not an array.');
                 if (productGrid) {
                     productGrid.innerHTML = '<div style="text-align: center; padding: 50px;"><p>Invalid search results data.</p></div>';
                 }
                 return;
             }

            // Use the shared displayProducts function
            displayProducts(products, 'product-grid');
            
             // Optionally remove results from sessionStorage after display
            // sessionStorage.removeItem('visualSearchResults'); 

        } catch (error) {
            console.error('Error parsing search results:', error);
             if (productGrid) {
                productGrid.innerHTML = `<div style="text-align: center; padding: 50px;"><p>Error displaying search results: ${error.message}</p></div>`;
            }
        }
    } else {
         console.log("No visual search results found in session storage.");
         // Display an empty state message if no results were found
         if (productGrid) {
             productGrid.innerHTML = '<div style="text-align: center; padding: 50px;"><p>No similar items found.</p></div>';
         }
    }

    // The click handling for products (to add to cart or navigate to s product page)
    // is handled by the product-grid.js script which should be included.

});
```

**--- START OF FILE search.js ---**

(Remove this file. Its mobile search toggle is likely covered by `search-integration.js` and Navbar CSS. Its visual search file handling and preview logic that simply redirects without API calls is superseded by `popup.js`).

**--- START OF FILE search-integration.js ---**

(Modified to integrate the text search API call and use the shared `displayProducts` function)

```javascript
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.querySelector('.search-input');
    // Removed searchToggleBtn as it might conflict with mobile toggle logic elsewhere
    // The mobile toggle animation itself is usually handled by CSS and a simple JS toggle class
    // The actual search action should trigger on Enter keypress or a dedicated search button icon click

    // Backend API base URL for AI endpoints
    const API_BASE_URL = 'http://localhost:5000/api/ai'; // Adjust if your Flask app is different

    // Check if the shared displayProducts function is available
    if (typeof displayProducts !== 'function') {
        console.error("The required 'displayProducts' function is not available. Ensure product-grid.js is loaded.");
         // Find a grid container to display an error message if possible
         const fallbackContainer = document.getElementById('product-grid') || document.querySelector('#related-product-grid');
         if (fallbackContainer) {
             fallbackContainer.innerHTML = '<div style="text-align: center; padding: 50px;"><p>Error loading display functions.</p></div>';
         }
        return; // Stop execution if displayProducts is missing
    }


    if (!searchInput) {
        console.warn("Search input not found on this page. Text search functionality may be limited.");
        // Continue as other parts of the script might still be relevant (like mobile toggle if kept)
    }

    // Function to perform text search using the API
    async function performTextSearch(query) {
        // Find the element where products are typically displayed on this page
        // It might be #product-grid on category/all pages or #related-product-grid on s product page, etc.
        // Let's target #product-grid as it's common on index/category pages.
        const productGrid = document.getElementById('product-grid'); 

        try {
            if (!query.trim()) {
                if (productGrid) {
                     productGrid.innerHTML = '<div style="text-align: center; padding: 50px;"><p>Please enter a search query.</p></div>';
                }
                return;
            }

            // Show loading state in the relevant product grid
            if (productGrid) {
                productGrid.innerHTML = '<div class="loading-spinner" style="text-align: center; padding: 50px;"><i class="fas fa-spinner fa-spin fa-2x"></i><p>Searching...</p></div>';
                 // Update page title placeholder if it exists
                 const pageTitle = document.querySelector('h3, h2');
                 if (pageTitle) {
                     // Optionally store original title to restore later if clearing search
                     // pageTitle.dataset.originalText = pageTitle.textContent;
                     pageTitle.textContent = `Searching for "${query}"...`;
                 }
            }


            // API expects POST with JSON body containing 'query'
            const response = await fetch(`${API_BASE_URL}/search`, { // Or maybe /search-by-text if that's the POST endpoint
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                     // Add any other required headers
                },
                body: JSON.stringify({
                    query: query
                })
            });

             // Handle non-OK HTTP responses
            if (!response.ok) {
                 const errorBody = await response.text(); // Get response body for more details
                throw new Error(`HTTP error! status: ${response.status} - ${errorBody}`);
            }

            const result = await response.json(); // Parse the JSON response
            
            // Handle API-level errors (if isCompleteSuccessfully is false or has errorMessages)
            if (result.isCompleteSuccessfully === false) {
                 throw new Error(`API error: ${result.errorMessages ? result.errorMessages.join(', ') : 'Unknown API error'}`);
            }
             // Check specific structure for success data
             if (!Array.isArray(result.data)) {
                 throw new Error("API did not return a list of products in 'data'.");
             }


            // Update page title with actual results count or query
            const pageTitle = document.querySelector('h3, h2');
             if (pageTitle) {
                 pageTitle.textContent = `Search Results for "${query}" (${result.data.length} found)`;
             } else {
                 // If no title element, just log to console
                 console.log(`Search Results for "${query}" (${result.data.length} found)`);
             }


            // Display results using the shared function
            displayProducts(result.data, 'product-grid'); // Assuming products go into #product-grid

            // Optional: Redirect to a search results page if not already there
            // if (window.location.pathname !== '/resultpage.html') {
            //     // Store results in sessionStorage and redirect
            //     sessionStorage.setItem('textSearchQuery', query); // Optional: save query
            //     sessionStorage.setItem('textSearchResults', JSON.stringify(result.data));
            //     window.location.href = 'resultpage.html';
            //     return; // Stop here if redirecting
            // }
            
        } catch (error) {
            console.error('Text search error:', error);
            // Display error message in the product grid area
            if (productGrid) {
                productGrid.innerHTML = `<div style="text-align: center; padding: 50px;"><p>Error searching: ${error.message}</p></div>`;
                 // Reset title or show error in title
                 const pageTitle = document.querySelector('h3, h2');
                 if (pageTitle) pageTitle.textContent = `Search Error`; // Or include error message
            } else {
                 alert(`Error searching: ${error.message}`); // Fallback alert if no grid area
            }
            
            // Optional: Redirect to an error/results page with error info
            // if (window.location.pathname !== '/resultpage.html') {
            //     sessionStorage.setItem('textSearchQuery', query);
            //     sessionStorage.setItem('textSearchError', error.message);
            //     window.location.href = 'resultpage.html';
            // }
        }
    }

    // Event listeners for search input (Enter key)
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            // Check if the key pressed was 'Enter' (key code 13 or key 'Enter')
            if (e.key === 'Enter' || e.keyCode === 13) {
                e.preventDefault(); // Prevent default form submission (if input is in a form)
                const query = searchInput.value.trim();
                // Only perform search if query is not empty after trimming
                if (query) {
                    performTextSearch(query);
                }
            }
        });
    }

    // --- Mobile Search Bar Toggle (if not handled by search.js or Navbar CSS alone) ---
    // Check if the toggle button and container exist before adding logic
    const searchContainer = document.getElementById('search-container');
    const searchToggleBtn = document.getElementById('search-toggle-btn');

     if (searchToggleBtn && searchContainer) {
         // Add click listener to the mobile search icon
         searchToggleBtn.addEventListener('click', (event) => {
             event.stopPropagation(); // Prevent click from bubbling up
             searchContainer.classList.toggle('active'); // Toggle CSS class for animation
         });

         // Add a global click listener to close if clicking outside
         document.addEventListener('click', (event) => {
             if (searchContainer.classList.contains('active')) {
                 if (!searchContainer.contains(event.target)) {
                     searchContainer.classList.remove('active');
                 }
             }
         });
          // Prevent clicks inside the container from closing it
         searchContainer.addEventListener('click', (event) => {
             event.stopPropagation();
         });
     }
    // --- End Mobile Toggle ---


    // --- Initial Text Search from URL (if applicable) ---
    // If this page is intended to display results based on a query passed via URL
    // e.g., ?search=blue+shirt
    const urlParams = new URLSearchParams(window.location.search);
    const initialSearchQuery = urlParams.get('search');
    if (initialSearchQuery) {
        if (searchInput) {
             searchInput.value = initialSearchQuery; // Populate search input
        }
        performTextSearch(initialSearchQuery); // Perform the search
    }

});
```

**--- START OF FILE sproduct.js ---**

(Modified to use the global `updateCartIcon` and clarify data source)

```javascript
document.addEventListener('DOMContentLoaded', () => {

    // --- DOM ELEMENTS ---
    const addToCartBtn = document.getElementById('addToCartBtn');
    const productDetailsContainer = document.getElementById('productDetails'); // Container with data-id
    const productNameEl = document.getElementById('product-name'); // Element displaying name
    const productPriceEl = document.getElementById('product-price'); // Element displaying price
    const productSizeEl = document.getElementById('productSize'); // Select element for size
    const productQuantityEl = document.getElementById('productQuantity'); // Input for quantity
    const mainImgEl = document.getElementById('MainImg'); // The main product image element
    const cartCountEl = document.getElementById('cart-count'); // The cart count element (can be removed if using global function exclusively)

    // --- FUNCTIONS ---
    // Removed the duplicate local updateCartCount function.
    // This script will now rely on the global window.updateCartIcon defined in auth.js or product-grid.js.


    const handleAddToCart = () => {
        // --- Get Product Info from the DOM ---
        // This assumes products.js has run and populated these elements and the data-id attribute.
        const productId = productDetailsContainer ? productDetailsContainer.dataset.id : null;
        const productName = productNameEl ? productNameEl.textContent.trim() : 'Unknown Product';
        const priceText = productPriceEl ? productPriceEl.textContent : '0'; 
        // Attempt to extract number, remove " LE" and parse
        const productPrice = parseFloat(priceText.replace(' LE', '')); 
        const productSize = productSizeEl ? productSizeEl.value : null;
        const productQuantity = productQuantityEl ? parseInt(productQuantityEl.value, 10) : 1;
        const productImgSrc = mainImgEl ? mainImgEl.getAttribute('src') : 'Images/placeholder.png';

        // --- Validation ---
        if (!productId) {
              console.error("Cannot add to cart: Product ID is missing.");
              alert('Error adding product to cart. Missing product data.');
              return;
         }
         if (productSize === 'Select Size' || productSize === null) { // Also check for null size
            alert('Please select a size before adding to cart.');
            return;
        }
        if (isNaN(productQuantity) || productQuantity < 1) {
            alert('Please enter a valid quantity (1 or more).'); // More specific error message
            return;
        }
         if (isNaN(productPrice) || productPrice < 0) { // Validate price data too
             console.error("Invalid product price:", priceText);
             alert('Error adding product to cart. Invalid price data.');
             return;
         }
        
        // --- Update Cart ---
        let cart = JSON.parse(localStorage.getItem('shoppingCart')) || [];
        // Check if an item with the same ID and size already exists
        let existingItem = cart.find(item => String(item.id) === String(productId) && item.size === productSize); // Compare IDs as strings

        if (existingItem) {
            existingItem.quantity += productQuantity;
        } else {
            cart.push({
                id: productId,
                name: productName,
                price: productPrice,
                quantity: productQuantity,
                imgSrc: productImgSrc,
                size: productSize
            });
        }

        // --- Save to localStorage and Update UI ---
        localStorage.setItem('shoppingCart', JSON.stringify(cart));
        
        // Use the global updateCartIcon function
        if (window.updateCartIcon) {
             window.updateCartIcon();
        } else if (cartCountEl) {
             // Fallback to manually updating the count element if global function isn't found (less ideal)
             const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
             cartCountEl.textContent = totalItems;
        }


        // --- Provide User Feedback on the Button ---
        const originalText = addToCartBtn.innerHTML; // Store original button HTML
        const feedbackText = `Added ${productQuantity} <i class="fas fa-check"></i>`; // Include quantity in feedback
        addToCartBtn.innerHTML = feedbackText; 
        addToCartBtn.disabled = true;
        
        setTimeout(() => {
            addToCartBtn.innerHTML = originalText; 
            addToCartBtn.disabled = false;
        }, 2000);
    };

    // --- EVENT LISTENERS ---
    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', handleAddToCart);
    }

    // --- INITIALIZATION ---
    // The global updateCartIcon is likely called by auth.js or product-grid.js on DOMContentLoaded.
    // No need to call updateCartCount here, just ensure the event listener is set up.
    // updateCartCount(); 
});
```

**Revised HTML Script Includes:**

On pages that display product grids (`All.html`, `Men.html`, `Women.html`, `homepage.html`, `resultpage.html`), ensure these scripts are included (order matters):

```html
<!-- Assuming Bootstrap JS is loaded before custom scripts -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<!-- Core Scripts -->
<script src="auth.js"></script> <!-- Defines window.updateCartIcon -->
<script src="product-grid.js"></script> <!-- Defines window.displayProducts and handles product card clicks -->
<script src="api-integration.js"></script> <!-- Defines fetchProducts -->
<script src="popup.js"></script> <!-- Handles Visual Search Modal and API calls -->
<script src="search-integration.js"></script> <!-- Handles Text Search and API calls -->
<script src="transitions.js"></script> <!-- If used for page transitions -->

<!-- Page-Specific Scripts -->
<!-- If on All.html, Men.html, Women.html, homepage.html, resultpage.html -->
<script>
  // Page-specific logic to fetch and display initial products using the shared functions
  // Example for All.html:
   document.addEventListener('DOMContentLoaded', async function() {
     const products = await fetchProducts(); // fetchProducts is in api-integration.js
     displayProducts(products, 'product-grid'); // displayProducts is in product-grid.js
   });
  // Example for Men.html/Women.html/Kids.html:
  // document.addEventListener('DOMContentLoaded', async function() {
  //   const products = await fetchProducts('Men'); // or 'Women', 'Kids'
  //   displayProducts(products, 'product-grid');
  // });
  // Example for homepage.html (featured products):
  // document.addEventListener('DOMContentLoaded', async function() {
  //   const products = await fetchProducts('', 4); // Get 4 featured products
  //   displayProducts(products, 'product-grid');
  // });
  // resultpage.js relies on sessionStorage populated by popup.js, loads later automatically
</script>
```

On `sproduct.html`, ensure these scripts are included:

```html
<!-- Assuming Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<!-- Core Scripts -->
<script src="auth.js"></script> <!-- Defines window.updateCartIcon -->
<script src="product-grid.js"></script> <!-- Defines window.displayProducts and handles related product clicks -->
<script src="api-integration.js"></script> <!-- Defines fetchProducts (for related products) -->
<script src="popup.js"></script> <!-- Includes Visual Search Modal (if needed on s product page) -->
<script src="search-integration.js"></script> <!-- Includes Text Search (if search bar is present) -->
<script src="transitions.js"></script> <!-- If used -->

<!-- Page-Specific Scripts -->
<script src="products.js"></script> <!-- Loads main product data from URL -->
<script src="sproduct.js"></script> <!-- Handles Add to Cart button for the main product -->

<!-- product-grid.js will handle fetching/displaying related products via loadRelatedProducts in products.js -->
```

On `cart.html`, `checkout.html`, `orders.html`, `forgot-password.html`, `change-password.html`, include only the necessary scripts for modals, cart/order logic, and potentially the navbar/search if present:

```html
<!-- For cart.html/checkout.html/orders.html -->
<!-- Assuming Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script> <!-- Only needed if using Bootstrap JS components -->

<!-- Core/Shared Scripts -->
<script src="auth.js"></script> <!-- Provides login status, user data, auth modal, profile modal, global updateCartIcon -->
<!-- Include search-integration.js and popup.js ONLY if the navbar with search/visual search is present on the page -->
<script src="search-integration.js"></script>
<script src="popup.js"></script>
<script src="transitions.js"></script> <!-- If used -->

<!-- Page-Specific Scripts -->
<script src="cart.js"></script> <!-- For cart page logic -->
<script src="checkout.js"></script> <!-- For checkout page logic -->
<script src="orders.js"></script> <!-- For orders page logic -->

<!-- For forgot-password.html/change-password.html, primarily need auth.js for modals if applicable, and their specific scripts -->
<!-- Assuming Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script> <!-- Only if Bootstrap JS components used -->
<script src="auth.js"></script> <!-- If auth/profile modals are needed -->
<script src="transitions.js"></script> <!-- If used -->
<!-- Page-Specific Scripts -->
<script src="change-password.js"></script>
<!-- forgot-password.html doesn't have a specific JS based on provided files -->
```

This setup consolidates the display logic, correctly routes API calls based on user actions (text search vs. visual search), and ensures shared components like the cart count are updated consistently using a global function. Remember to test thoroughly after applying these changes.

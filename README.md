Okay, I will refactor your four ASP.NET user control (`.ascx`) pages to use a unified front-end design, incorporating consistent colors, patterns, loaders, and error handling based on a standard modern web design palette (as no image was provided).

I will define a set of CSS variables and classes with an `app-` prefix for consistency. I will also provide shared JavaScript helper functions for API calls, feedback, and loading indicators, encapsulated within a global `App` object, and include these in each script block.

**Unified Design Elements:**

*   **Colors:**
    *   Primary: Blue (`#2563eb`)
    *   Accent: Light Blue (`#e6f0ff`)
    *   Success: Green (`#10b981`)
    *   Warning/Expiring: Orange (`#f59e0b`)
    *   Error: Red (`#dc2626`)
    *   Backgrounds: Light Gray Page (`#f5f7fa`), White Section (`#fff`)
    *   Text: Dark Gray (`#333`), Medium Gray (`#666`)
*   **Spacing:** Consistent use of variables (`--app-space-sm`, `--app-space-md`, etc.)
*   **Borders/Radii:** Consistent borders and rounded corners.
*   **Layout:** Flexbox/Grid for layout, max-width container.
*   **Forms/Buttons:** Standardized input styles, primary/outline/danger button styles.
*   **Tables/Cards:** Consistent styling.
*   **Loaders:**
    *   Global Overlay: Full-screen semi-transparent overlay with a spinner.
    *   Inline: Small spinner next to button text.
*   **Error/Feedback:**
    *   Global: Fixed-position popup for success/error messages (`#global-feedback`).
    *   Inline: Specific span for inline error text (like `#searchError`), styled with error color.

**Implementation Plan:**

1.  **Create Unified CSS:** Consolidate styles from all pages, standardize class names with `app-` prefix, use CSS variables for colors/spacing, and include styles for `#global-feedback` and `#loading-overlay`.
2.  **Create Shared JavaScript:** Develop a `App` object containing `apiService`, `showGlobalFeedback`, `setGlobalLoading`, `setButtonLoading`, and utility functions (`formatDate`, `formatCurrency`, etc.).
3.  **Update Each .ascx:**
    *   Replace the existing `<style>` block with the unified CSS.
    *   Add the HTML structure for `#global-feedback` and `#loading-overlay`.
    *   Replace the existing `<script>` block.
    *   Include the definition of the `App` object and its shared functions.
    *   Retain the page-specific JavaScript logic, adapting it to use the functions and objects from the `App` namespace (e.g., `App.apiService.getInsuranceDetails`, `App.showGlobalFeedback`, `App.setGlobalLoading`, `App.setButtonLoading`).
    *   Update HTML class names to use the new `app-` prefixed classes.

Let's generate the full code for each page.

---

**1. Unified CSS Block (to be included in all .ascx files):**

```css
<style>
    /* --- CSS Variables for Unified Design --- */
    :root {
        --app-color-primary: #2563eb; /* Blue */
        --app-color-primary-dark: #1d4ed8; /* Darker Blue */
        --app-color-accent: #e6f0ff; /* Lighter Blue */
        --app-color-success: #10b981; /* Green */
        --app-color-success-light: #d1fae5; /* Light Green */
        --app-color-error: #dc2626; /* Red */
        --app-color-error-light: #fee2e2; /* Light Red */
        --app-color-warning: #f59e0b; /* Orange */
        --app-color-warning-light: #fef3c7; /* Light Orange */
        --app-color-text-default: #333; /* Dark Gray */
        --app-color-text-secondary: #666; /* Medium Gray */
        --app-color-text-placeholder: #888; /* Light Gray */
        --app-color-border: #e0e0e0; /* Light Gray Border */
        --app-color-bg-page: #f5f7fa; /* Page Background */
        --app-color-bg-section: #fff; /* Section Background */
        --app-color-bg-highlight: #f9fafb; /* Table row hover/Header bg */
        --app-color-bg-input-disabled: #e9ecef; /* Disabled input */

        /* Define Spacing */
        --app-space-xs: 5px;
        --app-space-sm: 10px;
        --app-space-md: 15px;
        --app-space-lg: 20px;
        --app-space-xl: 30px;

        /* Define Radii */
        --app-radius-sm: 4px;
        --app-radius-md: 6px;
        --app-radius-lg: 10px;

        /* Define Shadow */
        --app-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
        --app-shadow-hover: 0 4px 8px rgba(0, 0, 0, 0.08);
    }

    /* --- Global Resets & Base --- */
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: Arial, sans-serif; }
    body { background-color: var(--app-color-bg-page); color: var(--app-color-text-default); padding: var(--app-space-lg); }

    /* --- Layout --- */
    .app-container { max-width: 1200px; margin: 0 auto; } /* Padding is on body */
    .app-heading { color: var(--app-color-text-default); margin-bottom: var(--app-space-lg); font-size: 24px; font-weight: bold; }
    .app-section { background-color: var(--app-color-bg-section); padding: var(--app-space-lg); border-radius: var(--app-radius-md); margin-bottom: var(--app-space-lg); box-shadow: var(--app-shadow); }
    .app-section-title { font-size: 18px; color: var(--app-color-text-default); margin-bottom: var(--app-space-lg); font-weight: bold; }
    .app-form-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: var(--app-space-lg); margin-bottom: var(--app-space-md); } /* Adjusted margin bottom as gap handles row spacing */
    .app-form-group { margin-bottom: 0; } /* Gap on row handles vertical spacing */
    .app-form-label { display: block; margin-bottom: var(--app-space-sm); color: var(--app-color-text-secondary); font-size: 14px; }

    /* --- Form Elements --- */
    .app-form-control { width: 100%; padding: var(--app-space-sm); border: 1px solid var(--app-color-border); border-radius: var(--app-radius-md); font-size: 14px; color: var(--app-color-text-default); }
    .app-form-control::placeholder { color: var(--app-color-text-placeholder); }
    .app-form-control:focus { outline: none; border-color: var(--app-color-primary); box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2); } /* Using fixed rgba for simplicity */
    .app-form-select { width: 100%; padding: var(--app-space-sm); border: 1px solid var(--app-color-border); border-radius: var(--app-radius-md); font-size: 14px; appearance: menulist; color: var(--app-color-text-default); }
     .app-form-select option[value=""][disabled] { display: none; } /* Hide empty default option */
    .app-form-text-help { display: block; color: var(--app-color-text-secondary); font-size: 12px; margin-top: var(--app-space-xs); }

    /* --- Buttons --- */
    .app-button { display: inline-flex; align-items: center; justify-content: center; padding: var(--app-space-sm) var(--app-space-md); border: 1px solid transparent; border-radius: var(--app-radius-md); cursor: pointer; font-size: 14px; font-weight: 500; transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease, opacity 0.2s ease; line-height: 1.2; white-space: nowrap; gap: var(--app-space-xs); text-decoration: none; }
    .app-button--primary { background-color: var(--app-color-primary); color: white; border-color: var(--app-color-primary); }
    .app-button--primary:hover:not(:disabled) { background-color: var(--app-color-primary-dark); border-color: var(--app-color-primary-dark); }
    .app-button--outline { background-color: var(--app-color-bg-section); color: var(--app-color-text-default); border: 1px solid var(--app-color-border); }
    .app-button--outline:hover:not(:disabled) { background-color: var(--app-color-bg-highlight); border-color: #d1d5db; } /* A slightly darker border */
    .app-button--danger { background-color: var(--app-color-error); color: white; border-color: var(--app-color-error); }
    .app-button--danger:hover:not(:disabled) { background-color: #b91c1c; border-color: #b91c1c; } /* Slightly darker red */
    .app-button:disabled { cursor: not-allowed; opacity: 0.6; }
    .app-button-icon { line-height: 1; } /* Font icon or emoji container */

    /* --- Action Buttons Container --- */
     .app-action-buttons { display: flex; flex-wrap: wrap; gap: var(--app-space-md); margin-top: var(--app-space-xl); }
     .app-action-buttons--right { justify-content: flex-end; } /* Align buttons to the right */
     .app-action-buttons--center { justify-content: center; } /* Align buttons to the center */
     .app-action-buttons--left { justify-content: flex-start; } /* Align buttons to the left */
     .app-action-buttons--between { justify-content: space-between; } /* Space between buttons */


    /* --- Info Grid (Page 1) --- */
    .app-info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: var(--app-space-lg); margin-bottom: var(--app-space-xl); }
    .app-info-section { background-color: transparent; } /* Info sections are transparent */
    .app-info-title { color: var(--app-color-text-secondary); font-size: 14px; margin-bottom: var(--app-space-xs); }
    .app-info-content { font-size: 16px; margin-bottom: var(--app-space-sm); color: var(--app-color-text-default); }

    /* --- Cards (Page 2) --- */
    .app-card-grid { display: flex; flex-wrap: wrap; gap: var(--app-space-lg); margin: var(--app-space-xl) 0; }
    .app-card { background-color: var(--app-color-bg-section); border-radius: var(--app-radius-lg); padding: var(--app-space-lg); flex: 1 1 250px; /* Feature cards base */ box-shadow: var(--app-shadow); transition: transform 0.2s ease, box-shadow 0.2s ease; text-decoration: none; color: inherit; display: block;}
    .app-card:hover { transform: translateY(-3px); box-shadow: var(--app-shadow-hover); }
    .app-card--stat { flex: 1 1 200px; /* Stat cards override */ }

    .app-card-icon { margin-bottom: var(--app-space-md); font-size: 24px; color: var(--app-color-primary); }
    .app-card-title { font-size: 16px; margin-bottom: var(--app-space-sm); font-weight: 600; color: var(--app-color-text-default); }
    .app-card-description { font-size: 14px; color: var(--app-color-text-secondary); }

    .app-card--accent-blue { background-color: var(--app-color-accent); }
    .app-card--accent-green { background-color: var(--app-color-success-light); } /* Using light success color */
    .app-card--accent-purple { background-color: #f0e6ff; } /* Keeping the purple from original */

    .app-stat-title { color: var(--app-color-text-secondary); font-size: 14px; margin-bottom: var(--app-space-sm); }
    .app-stat-value { font-size: 24px; font-weight: 600; color: var(--app-color-text-default); }
    .app-stat-icon { float: right; font-size: 20px; }
    .app-stat-icon--blue { color: var(--app-color-primary); }
    .app-stat-icon--orange { color: var(--app-color-warning); }
    .app-stat-icon--green { color: var(--app-color-success); }
    .app-stat-icon--red { color: var(--app-color-error); }


    /* --- Data Table (Page 2 & 3) --- */
    .app-data-table-container { width: 100%; background-color: var(--app-color-bg-section); border-radius: var(--app-radius-lg); overflow: hidden; box-shadow: var(--app-shadow); margin: var(--app-space-xl) 0; display: flex; flex-direction: column; }
    .app-table-scroll-wrapper { width: 100%; overflow-x: auto; } /* For responsiveness */
    .app-table-header { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; padding: var(--app-space-lg); border-bottom: 1px solid var(--app-color-border); gap: var(--app-space-md); }
    .app-table-header h2 { font-size: 18px; font-weight: 600; margin: 0; }

    .app-table { width: 100%; border-collapse: collapse; min-width: 800px; /* Minimum width for table */ }
    .app-table th, .app-table td { text-align: left; padding: var(--app-space-md) var(--app-space-lg); font-size: 14px; vertical-align: middle; }
    .app-table th { background-color: var(--app-color-bg-highlight); color: var(--app-color-text-secondary); font-weight: 500; white-space: nowrap; }
    .app-table tbody tr { border-bottom: 1px solid var(--app-color-border); }
    .app-table tbody tr:last-child { border-bottom: none; }
    .app-table tbody tr:hover { background-color: var(--app-color-bg-highlight); }
    .app-table .no-results td { text-align: center; color: var(--app-color-text-secondary); font-style: italic; padding: var(--app-space-xl) var(--app-space-lg); }

    /* --- Status Badges --- */
    .app-status { padding: var(--app-space-xs) var(--app-space-sm); border-radius: var(--app-radius-sm); font-size: 12px; font-weight: 500; display: inline-block; white-space: nowrap; text-transform: capitalize; }
    .app-status--active { background-color: var(--app-color-success-light); color: var(--app-color-success); }
    .app-status--expiring { background-color: var(--app-color-warning-light); color: var(--app-color-warning); }
    .app-status--expired { background-color: var(--app-color-error-light); color: var(--app-color-error); }


    /* --- Pagination --- */
    .app-pagination { display: flex; flex-wrap: wrap; justify-content: flex-end; padding: var(--app-space-md) var(--app-space-lg); gap: var(--app-space-sm); align-items: center; border-top: 1px solid var(--app-color-border); }
    .app-pagination.hidden { display: none; }
    .app-pagination button { min-width: 30px; height: 30px; padding: 0 var(--app-space-xs); border-radius: var(--app-radius-sm); border: 1px solid var(--app-color-border); background-color: var(--app-color-bg-section); cursor: pointer; display: inline-flex; align-items: center; justify-content: center; font-size: 14px; }
    .app-pagination button:hover:not(:disabled) { border-color: #d1d5db; background-color: var(--app-color-bg-highlight); }
    .app-pagination button.active { background-color: var(--app-color-primary); color: white; border-color: var(--app-color-primary); }
    .app-pagination button:disabled { opacity: 0.6; cursor: not-allowed; }
    .app-pagination span { font-size: 14px; color: var(--app-color-text-secondary); margin-right: auto; }


    /* --- Search Form (Page 2) --- */
    .app-search-form { padding: var(--app-space-lg); border-bottom: 1px solid var(--app-color-border); }
    .app-search-form h3 { margin-bottom: var(--app-space-md); font-size: 16px; color: var(--app-color-text-default); }
    .app-search-fields { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: var(--app-space-md); margin-bottom: var(--app-space-md); }
    .app-radio-group { display: flex; flex-wrap: wrap; gap: var(--app-space-md) var(--app-space-lg); margin-bottom: var(--app-space-lg); }
    .app-radio-option { display: flex; align-items: center; gap: var(--app-space-xs); }
    .app-radio-option input[type="radio"] { cursor: pointer; width: 16px; height: 16px; }
    .app-radio-option label { font-size: 14px; cursor: pointer; color: var(--app-color-text-default); }
    .app-inline-error { color: var(--app-color-error); margin-top: var(--app-space-sm); font-size: 14px; text-align: right; min-height: 1.2em; display: block; }


    /* --- Tabs (Page 3) --- */
    .app-tab-container { display: flex; margin-bottom: var(--app-space-lg); border-bottom: 2px solid var(--app-color-border); }
    .app-tab { padding: var(--app-space-sm) var(--app-space-lg); background-color: transparent; color: var(--app-color-text-secondary); border: none; cursor: pointer; font-size: 16px; margin-right: var(--app-space-sm); border-bottom: 2px solid transparent; transition: border-bottom-color 0.2s ease, color 0.2s ease; }
    .app-tab:hover:not(:disabled) { color: var(--app-color-primary); }
    .app-tab.active { color: var(--app-color-primary); font-weight: bold; border-bottom-color: var(--app-color-primary); }
    .app-tab-content { display: none; padding-top: var(--app-space-lg); } /* Add padding top to content */
    .app-tab-content.active { display: block; }


    /* --- Modals (Page 3) --- */
    .app-modal { display: none; position: fixed; z-index: 100; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.4); padding: var(--app-space-lg); } /* Add padding to modal container */
    .app-modal-content { background-color: var(--app-color-bg-section); margin: 10vh auto; /* Adjusted margin for better vertical centering */ padding: var(--app-space-xl); border-radius: var(--app-radius-md); width: 90%; max-width: 600px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); position: relative; }
    .app-modal-close-btn { color: #aaa; position: absolute; top: var(--app-space-md); right: var(--app-space-lg); font-size: 28px; font-weight: bold; cursor: pointer; line-height: 1; }
    .app-modal-close-btn:hover, .app-modal-close-btn:focus { color: var(--app-color-text-default); text-decoration: none; }
    .app-modal .app-action-buttons { justify-content: flex-end; gap: var(--app-space-sm); margin-top: var(--app-space-xl); padding-top: var(--app-space-lg); border-top: 1px solid var(--app-color-border); } /* Style buttons inside modal */


    /* --- Notification Config (Page 4) --- */
    .app-current-value { display: block; margin-bottom: var(--app-space-md); padding: var(--app-space-sm); background-color: var(--app-color-bg-highlight); border: 1px solid var(--app-color-border); border-radius: var(--app-radius-md); color: var(--app-color-text-default); font-size: 16px; }
    .app-current-value-label { font-weight: bold; color: var(--app-color-text-secondary); margin-right: var(--app-space-xs); }
    .app-days-input-group { display: flex; align-items: center; gap: var(--app-space-sm); } /* Use gap */
    .app-days-input { width: 80px; padding: var(--app-space-sm); border: 1px solid var(--app-color-border); border-radius: var(--app-radius-md); font-size: 16px; text-align: center; } /* Remove right margin, use gap */
    .app-days-label { font-size: 16px; color: var(--app-color-text-secondary); }


    /* --- Global Feedback (Success/Error) --- */
    #global-feedback { position: fixed; top: var(--app-space-lg); left: 50%; transform: translateX(-50%); background-color: rgba(16, 185, 129, 0.9); /* Using RGBA of success color */ color: white; padding: var(--app-space-sm) var(--app-space-lg); border-radius: var(--app-radius-md); z-index: 1000; display: none; text-align: center; font-size: 16px; min-width: 250px; max-width: 90%; word-break: break-word; box-shadow: var(--app-shadow-hover); }
    #global-feedback.error { background-color: rgba(220, 38, 38, 0.9); /* Using RGBA of error color */ }

    /* --- Global Loading Overlay --- */
    #loading-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.5); display: none; justify-content: center; align-items: center; z-index: 9999; color: white; font-size: 20px; }
    #loading-overlay.active { display: flex; }

    /* --- Inline Loader Spinner (Used in Buttons/Elements) --- */
    .app-loader { border: 3px solid rgba(255, 255, 255, 0.3); border-top: 3px solid #fff; border-radius: 50%; width: 1em; height: 1em; animation: app-spin 1s linear infinite; vertical-align: middle; display: inline-block; }
    .app-button--outline .app-loader { border-top-color: var(--app-color-primary); border-color: rgba(37, 99, 235, 0.3); } /* Spinner color for outline buttons */
     .app-loader-inline { /* For loaders not inside buttons, e.g. near search results */
         border: 3px solid var(--app-color-border);
         border-top: 3px solid var(--app-color-primary);
         border-radius: 50%;
         width: 1.2em; height: 1.2em;
         animation: app-spin 1s linear infinite;
         display: inline-block;
         vertical-align: middle;
     }


    @keyframes app-spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* --- Utility classes --- */
    .text-center { text-align: center; }
    .margin-top-lg { margin-top: var(--app-space-lg); }
    .margin-bottom-lg { margin-bottom: var(--app-space-lg); }
    .float-right { float: right; }

</style>
```

---

**2. Shared JavaScript Block (to be included in all .ascx files within `<script>` tags):**

```javascript
// --- Unified Helper Functions & API Service ---

// Using a global object to hold shared functions to avoid conflicts
const App = {
    // !!! IMPORTANT: UPDATE THIS URL IF YOUR API IS HOSTED ELSEWHERE !!!
    API_BASE_URL: 'https://localhost:7260/api/InsuranceRenewalAutoLicence',
    DEFAULT_HEADERS: { 'Accept': 'application/json' },
    JSON_HEADERS: { 'Accept': 'application/json', 'Content-Type': 'application/json' },

    // --- API Service ---
    apiService: {
        async _fetch(endpoint, options = {}) {
            const url = `${App.API_BASE_URL}${endpoint}`;
            console.log(`API Request: ${options.method || 'GET'} ${url}`); // Log request
            try {
                const response = await fetch(url, options);
                let responseData = null;
                const contentType = response.headers.get("content-type");

                // Attempt to parse JSON if content type is json or if response status is non-success
                if (contentType && contentType.includes("application/json") || !response.ok) {
                     try {
                        responseData = await response.json();
                        console.log("API Response JSON:", responseData); // Log response data
                     } catch (jsonError) {
                        console.warn('Failed to parse JSON response, but content-type was application/json.', jsonError);
                        if (!response.ok) {
                           let errorText = await response.text(); // Get raw text for non-json errors
                           throw new Error(`API Error: ${response.status} ${response.statusText}. Failed to parse JSON. Raw text: ${errorText.substring(0, 200)}...`);
                        }
                        // If JSON parsing fails on OK response, responseData remains null, handled below
                     }
                } else if (response.status === 204) {
                   console.log("API Response: 204 No Content");
                   return { isSuccess: true, data: null, totalDataCount: 0, message: "Operation successful (No Content)" };
                } else if (!response.ok) {
                   // Handle non-JSON error responses (e.g., plain text error)
                   let errorText = await response.text();
                   throw new Error(`API Error: ${response.status} ${response.statusText}. ${errorText.substring(0, 200)}...`);
                }

                // Process response data structure
                if (responseData && responseData.hasOwnProperty('isSuccess')) {
                    if (responseData.isSuccess) {
                         console.log("API Success:", responseData.message);
                         return responseData; // API wrapper indicates success
                    } else {
                        // API wrapper indicates failure, throw error with message
                         console.error("API Reported Failure:", responseData.message);
                         throw new Error(responseData.message || 'API reported an unsuccessful operation.');
                    }
                } else if (response.ok) {
                     // Response is OK, but no isSuccess flag. Assume success and return data.
                     console.warn("API response was OK and JSON, but lacked 'isSuccess' property. Assuming success.");
                     return { isSuccess: true, data: responseData, totalDataCount: responseData ? (Array.isArray(responseData) ? responseData.length : (responseData.totalCount || 0)) : 0, message: "Data received (Structure unknown)" };
                } else {
                    // Should not reach here if non-OK handled above and OK with JSON handled
                    throw new Error('API call completed without success response or recognizable data structure.');
                }


            } catch (error) {
                console.error(`API Fetch Error (${url}):`, error);
                // Only show global feedback for network/unexpected errors, not API-reported ones
                // The calling code should catch and decide if global feedback is appropriate
                // App.showGlobalFeedback(`Error: ${error.message || 'Network request failed'}`, true);
                throw error; // Re-throw the error so calling functions can handle it
            }
        },

        // --- Common API Calls (Can be included in all scripts if needed, or just define specific ones per page) ---
        async getAllInsuranceCompanies() {
             // Example of a common API call
             const result = await this._fetch('/AllInsuranceCompanies', { method: 'GET', headers: App.DEFAULT_HEADERS });
             // _fetch throws on failure, so if we're here, it was successful
             if (!Array.isArray(result.data)) {
                 console.error("API /AllInsuranceCompanies returned unexpected data format:", result.data);
                 throw new Error("Unexpected data format from server for insurance companies.");
             }
             return result.data; // Return the array of companies
         },


        // Page-Specific API Calls (Defined here as examples, actual calls will be in page-specific script)
        // These are just examples, copy/paste the relevant ones to your page's script block below the App object.
        /*
         async getInsuranceDetails(insuranceRenewalId) { ... } // For Page 1
         async addInsuranceRenewal(data) { ... } // For Page 1
         async searchRenewals(filterCriteria) { ... } // For Page 2
         async addInsuranceCompany(name) { ... } // For Page 3
         async updateInsuranceCompany(id, name) { ... } // For Page 3
         async deleteInsuranceCompany(id) { ... } // For Page 3
         async getNotificationSetting() { ... } // For Page 4
         async updateNotificationSetting(days) { ... } // For Page 4
        */
    },

    // --- UI Feedback & Loading ---
    feedbackTimeout: null,
    showGlobalFeedback(message, isError = false) {
        const feedbackDiv = document.getElementById('global-feedback');
        if (!feedbackDiv) {
            console.warn("Feedback element #global-feedback not found.");
            return;
        }
        feedbackDiv.textContent = message;
        feedbackDiv.classList.toggle('error', isError);
        feedbackDiv.style.display = 'block';
        clearTimeout(App.feedbackTimeout);
        App.feedbackTimeout = setTimeout(() => { feedbackDiv.style.display = 'none'; }, 5000); // Hide after 5 seconds
    },

    setGlobalLoading(isLoading) {
        const loadingIndicator = document.getElementById('loading-overlay');
        if (!loadingIndicator) {
             console.warn("Loading overlay element #loading-overlay not found.");
             return;
        }
        loadingIndicator.classList.toggle('active', isLoading);
    },

    setButtonLoading(buttonElement, isLoading, originalContent = 'Process...') {
        if (!buttonElement) return;
        const loaderHtml = '<span class="app-loader"></span> ';

        if (isLoading) {
            if (!buttonElement.dataset.originalContent) {
                 // Store original content if not already stored
                 buttonElement.dataset.originalContent = buttonElement.innerHTML;
                 // Use provided originalContent if element was empty or for specific text
                 if (buttonElement.dataset.originalContent.trim() === '' || originalContent !== 'Process...') {
                      buttonElement.dataset.originalContent = originalContent;
                 }
            }
            buttonElement.disabled = true;
            // Set new content with spinner
            buttonElement.innerHTML = `${loaderHtml}${originalContent}`;

        } else {
            // Restore original content
            buttonElement.disabled = false;
            buttonElement.innerHTML = buttonElement.dataset.originalContent || originalContent; // Use stored or provided original
            delete buttonElement.dataset.originalContent; // Clean up state
        }
    },


    // --- Formatting & Utility ---
    formatDate(dateString) {
        if (!dateString) return '-';
        try {
            // Try parsing different formats potentially returned by API
            const date = new Date(dateString);
            if (isNaN(date.getTime())) {
                console.warn("Invalid date format for Date object:", dateString);
                return App.escapeHtml(dateString); // Return as is if invalid
            }
            // Use toLocaleDateString for potentially better localization, or keep custom YYYY/MM/DD
            // Keeping YYYY/MM/DD for consistency with original code structure
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}/${month}/${day}`;
        } catch (e) {
            console.error("Error formatting date:", dateString, e);
            return App.escapeHtml(dateString);
        }
    },

    formatCurrency(amount) {
        let numericAmount = amount;
        if (typeof amount === 'string') {
            // Attempt to parse string, remove commas
            numericAmount = parseFloat(amount.replace(/,/g, ''));
        }

        if (numericAmount === null || numericAmount === undefined || isNaN(numericAmount)) {
            return '-';
        }
        try {
             // Use 'en-US' or 'ar-EG' based on requirement, but 'EGP' currency code implies EG formatting might be desired.
             // Keep 'ar-EG' as in original, but note browser support for currency formatting varies.
            return new Intl.NumberFormat('ar-EG', {
                style: 'currency',
                currency: 'EGP',
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }).format(numericAmount);
        } catch (e) {
            console.error("Error formatting currency:", numericAmount, e);
            // Fallback if Intl.NumberFormat fails
            return `${numericAmount.toFixed(2)} EGP`;
        }
    },

     determinePolicyStatus(expirationDateStr, isReregular) {
            // Treat isReregular: true as "Renewed" which falls under "Active" in the styling logic
            if (isReregular === true) return "Active"; // Renamed from "Renewed" to map to active status class

            if (!expirationDateStr) return "Unknown";

            const expDate = new Date(expirationDateStr);
            if (isNaN(expDate.getTime())) {
                console.warn("Invalid date format for Date object for status determination:", expirationDateStr);
                return "Invalid Date";
            }

            const today = new Date();
            // Normalize dates to UTC day for accurate comparison across timezones
            const todayNormalized = new Date(Date.UTC(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate()));
            const expDateNormalized = new Date(Date.UTC(expDate.getUTCFullYear(), expDate.getUTCMonth(), expDate.getUTCDate()));

            if (expDateNormalized < todayNormalized) return "Expired";

            const fifteenDaysFromToday = new Date(todayNormalized);
            fifteenDaysFromToday.setUTCDate(todayNormalized.getUTCDate() + 15);

            if (expDateNormalized <= fifteenDaysFromToday) return "Expiring Soon";

            return "Active";
        },

        formatStatus(statusText) {
            if (!statusText) return '<span class="app-status">-</span>';
            let statusClass = '';
            const lowerStatus = String(statusText).toLowerCase();

            // Map status text to unified class names
            if (lowerStatus === 'active') statusClass = 'app-status--active';
            else if (lowerStatus === 'expiring soon') statusClass = 'app-status--expiring';
            else if (lowerStatus === 'expired') statusClass = 'app-status--expired';
            else if (lowerStatus === 'renewed') statusClass = 'app-status--active'; // Map Renewed to Active state
            else return `<span class="app-status">${App.escapeHtml(statusText)}</span>`; // Default if status not recognized

            return `<span class="app-status ${statusClass}">${App.escapeHtml(statusText)}</span>`;
        },

    escapeHtml(unsafe) {
        if (unsafe === null || typeof unsafe === 'undefined') {
            return '';
        }
        const safeString = String(unsafe);
        return safeString
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    },

    // Utility to format date for API input (YYYY-MM-DD)
    formatDateForApi(dateInputString) {
        if (!dateInputString) return null;
        const datePattern = /^\d{4}-\d{2}-\d{2}$/;
        if (datePattern.test(dateInputString)) {
            return dateInputString; // Already in YYYY-MM-DD format
        }
        try {
            const d = new Date(dateInputString);
            if (isNaN(d.getTime())) return null;
            const year = d.getFullYear();
            const month = String(d.getMonth() + 1).padStart(2, '0');
            const day = String(d.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        } catch (e) {
            console.error("Error formatting date for API:", dateInputString, e);
            return null;
        }
    },

     getTodayYYYYMMDD() {
            const today = new Date();
            const year = today.getFullYear();
            const month = String(today.getMonth() + 1).padStart(2, '0');
            const day = String(today.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        }
};
```

---

Now, here are the updated `.ascx` files:

**1. `CreateInsuranceRenewal.ascx` (Updated)**

```html
<%@ Control Language="C#" AutoEventWireup="true" CodeFile="CreateInsuranceRenewal.ascx.cs" Inherits="CreateInsuranceRenewal" %>
<%@ Register Assembly="AjaxControlToolkit" Namespace="AjaxControlToolkit" TagPrefix="asp" %>

<style>
    /* --- Unified CSS Block (Copy and paste the full unified CSS here) --- */
    /* Styles from the unified block above */
    /* Ensure this style block contains the complete CSS from section 1 */
    /* Example: */
     :root { /* ... colors and spacing ... */ }
     * { /* ... resets ... */ }
     .app-container { /* ... */ }
     /* ... rest of the unified CSS ... */
     #global-feedback { /* ... */ }
     #loading-overlay { /* ... */ }
     .app-loader { /* ... */ }
     /* END Unified CSS Block */

     /* Adjustments specific to this page if needed */
     .app-info-grid {
         /* Specific columns for this grid */
         grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
         gap: var(--app-space-lg);
         margin-bottom: var(--app-space-xl);
     }
      .app-form-row--single-col {
          grid-template-columns: 1fr; /* Override form-row for a single input */
      }
</style>


<div class="app-container" dir="ltr">
    <h1 class="app-heading">System Information</h1>

    <div class="app-info-grid">
        <div class="app-info-section">
            <h2 class="app-info-title">Application Details</h2>
            <p class="app-info-content">App #: <span id="app-number">-</span></p>
            <p class="app-info-content">Name: <span id="customer-name">-</span></p>
        </div>

        <div class="app-info-section">
            <h2 class="app-info-title">Vehicle Information</h2>
            <p class="app-info-content">Car Brand: <span id="car-brand">-</span></p>
            <p class="app-info-content">Chassis: <span id="chassis">-</span></p>
        </div>

        <div class="app-info-section">
            <h2 class="app-info-title">Insurance Details</h2>
            <p class="app-info-content">Base Amount: <span id="base-amount">-</span></p>
            <p class="app-info-content">Minimum Required: <span id="minimum-required">-</span></p>
        </div>

        <div class="app-info-section">
            <h2 class="app-info-title">Payment Status</h2>
            <p class="app-info-content">Regular: <span id="is-regular">-</span></p>
            <p class="app-info-content">Last Payment: <span id="last-payment">-</span></p>
        </div>
    </div>

    <div class="app-section">
        <h2 class="app-section-title">Insurance Information</h2>

        <div class="app-form-row app-form-row--single-col">
            <div class="app-form-group">
                <label class="app-form-label" for="insurance-company">Insurance Company</label>
                <select class="app-form-select" id="insurance-company">
                    <option value="" disabled selected>Select Insurance Company</option>
                    <%-- Options will be loaded by JavaScript --%>
                </select>
            </div>
        </div>

        <div class="app-form-row app-form-row--single-col">
            <div class="app-form-group">
                <label class="app-form-label" for="annual-insurance">Annual Insurance Amount</label>
                <input type="text" class="app-form-control" id="annual-insurance" placeholder="$ Enter amount">
                <small class="app-form-text-help">Must not be less than the remaining settlement amount + 20% (based on Minimum Required)</small>
                 <span id="annual-insurance-error" class="app-inline-error"></span> <%-- Inline error span --%>
            </div>
        </div>

        <div class="app-action-buttons app-action-buttons--left">
            <button class="app-button app-button--primary" id="save-insurance-btn" type="button">
                <span class="app-button-icon">💾</span>
                Save Information
            </button>
        </div>
    </div>

    <%-- Global Feedback and Loading Overlay --%>
    <div id="global-feedback"></div>
    <div id="loading-overlay">Loading...</div>
</div>

<script>
    // --- Unified Shared JavaScript Block (Copy and paste the full App object definition here) ---
    // Includes App object, apiService, showGlobalFeedback, setGlobalLoading, setButtonLoading, formatters, etc.
    // Ensure this script block contains the complete App object from section 2

    // Example Placeholder (Replace with actual App object definition)
    /*
    const App = {
        API_BASE_URL: '...', apiService: { _fetch: async () => {}, ... },
        showGlobalFeedback: () => {}, setGlobalLoading: () => {}, setButtonLoading: () => {},
        formatDate: () => {}, formatCurrency: () => {}, determinePolicyStatus: () => {}, formatStatus: () => {},
        escapeHtml: () => {}, formatDateForApi: () => {}, getTodayYYYYMMDD: () => {}
    };
    */
    // --- END Unified Shared JavaScript Block ---

    // !!! IMPORTANT: Mock data for insuranceRenewalId - REPLACE WITH ACTUAL VALUE FROM SERVER-SIDE CODE !!!
    // This ID needs to come from your server-side logic, perhaps passed via a hidden field or data attribute.
    const insuranceRenewalId = 10; // Example value - GET THIS FROM YOUR C# CODE

    // Page-Specific API Calls (Optional: Can be defined here if only used on this page)
    App.apiService.getInsuranceDetails = async function(id) {
         // Assuming API endpoint accepts POST with body { insuranceRenewalId: id }
         const result = await this._fetch('/GetInsuranceDetails', {
             method: 'POST', // Or 'GET' if the endpoint supports it with a query string
             headers: App.JSON_HEADERS, // Or App.DEFAULT_HEADERS for GET
             body: JSON.stringify({ insuranceRenewalId: id }) // Assuming POST body
         });
         // _fetch throws on error, so if we are here, result.isSuccess is true
         if (!result || !result.data) {
             throw new Error("API returned success but no data for details.");
         }
         return result.data; // Return just the data payload
    };

    App.apiService.addInsuranceRenewal = async function(data) {
        // API expects { totalInsuranceAmount, installmentId, companyId } in body
        const result = await this._fetch('/AddInsuranceRenewal', {
            method: 'POST',
            headers: App.JSON_HEADERS,
            body: JSON.stringify(data)
        });
         if (!result || !result.data) {
             // API might return success with no data for add operations, check message if needed
             // throw new Error("API returned success but no confirmation data.");
         }
        return result.data; // Return data if any, or confirmation
    };

     // Overwriting common getAllCompanies just for clarity this page uses it
    App.apiService.getAllInsuranceCompanies = async function() {
        const result = await this._fetch('/AllInsuranceCompanies', { method: 'GET', headers: App.DEFAULT_HEADERS });
        if (!Array.isArray(result.data)) {
             console.error("API /AllInsuranceCompanies returned unexpected data format:", result.data);
             throw new Error("Unexpected data format from server for insurance companies.");
        }
        return result.data;
    };


    // --- Page Specific Logic ---

    async function populateInsuranceDetails(insuranceRenewalId) {
        App.setGlobalLoading(true);
        try {
            const details = await App.apiService.getInsuranceDetails(insuranceRenewalId);
            // Populate spans with data, use escapeHtml
            document.getElementById('app-number').textContent = App.escapeHtml(details.installmentUniqueId || '-'); // Assuming installmentUniqueId exists
            document.getElementById('customer-name').textContent = App.escapeHtml(details.customerName || '-');
            document.getElementById('car-brand').textContent = App.escapeHtml(details.carBrand || '-');
            document.getElementById('chassis').textContent = App.escapeHtml(details.chassis || '-');
            // Use formatCurrency for amounts
            document.getElementById('base-amount').textContent = App.formatCurrency(details.baseAmount);
            document.getElementById('minimum-required').textContent = App.formatCurrency(details.minimumRequired);
            // Format boolean status
            document.getElementById('is-regular').textContent = (details.isReregular === true) ? 'Yes' : (details.isReregular === false ? 'No' : '-');
            // Use formatDate for dates
            document.getElementById('last-payment').textContent = App.formatDate(details.lastPaymentDate);

        } catch (error) {
            // Error handled by App.apiService._fetch, shows global feedback
            // You might add page-specific error handling here if needed
             console.error("Error populating details:", error);
        } finally {
            App.setGlobalLoading(false);
        }
    }

    async function handleSaveInsurance() {
        const companySelect = document.getElementById('insurance-company');
        const amountInput = document.getElementById('annual-insurance');
        const amountError = document.getElementById('annual-insurance-error');
        const saveButton = document.getElementById('save-insurance-btn');

        amountError.textContent = ''; // Clear previous errors

        const companyId = companySelect ? companySelect.value : '';
        const totalInsuranceAmountStr = amountInput ? amountInput.value.trim() : '';

        if (!companyId || totalInsuranceAmountStr === '') {
            App.showGlobalFeedback('Please select an insurance company and enter the annual insurance amount.', true);
            return;
        }

        const totalInsuranceAmount = parseFloat(totalInsuranceAmountStr);
        if (isNaN(totalInsuranceAmount) || totalInsuranceAmount <= 0) {
             amountError.textContent = 'Please enter a valid positive number.';
             amountInput.focus();
             return;
        }

        // Basic validation against minimum required (assuming it's available in the DOM)
        const minimumRequiredSpan = document.getElementById('minimum-required');
        const minimumRequiredText = minimumRequiredSpan ? minimumRequiredSpan.textContent : '0';
        const minimumRequiredAmount = parseFloat(minimumRequiredText.replace(/[^0-9.-]+/g,"")); // Parse formatted currency string

        if (!isNaN(minimumRequiredAmount) && totalInsuranceAmount < minimumRequiredAmount) {
             amountError.textContent = `Amount must not be less than the Minimum Required (${minimumRequiredSpan.textContent})`;
             amountInput.focus();
             return;
        }


        // Assuming installmentUniqueId from the info section is the installmentId needed for the API
        const installmentIdSpan = document.getElementById('app-number');
        const installmentId = installmentIdSpan ? parseInt(installmentIdSpan.textContent) : NaN;

        if (isNaN(installmentId)) {
            App.showGlobalFeedback('Could not retrieve valid Installment ID from the page.', true);
            return;
        }

        const data = {
            totalInsuranceAmount: totalInsuranceAmount,
            installmentId: installmentId,
            companyId: parseInt(companyId)
        };

        App.setButtonLoading(saveButton, true, 'Saving...');
        App.setGlobalLoading(true); // Optional: Also show global loader for critical save operations
        try {
            const result = await App.apiService.addInsuranceRenewal(data);
            // Assuming API returns success property or throws error
            App.showGlobalFeedback('Insurance renewal added successfully.', false);
            console.log('Insurance renewal added result:', result);
            // You might want to redirect or update the UI here
        } catch (error) {
            // Error is handled by App.apiService._fetch and shows global feedback
            console.error("Error adding insurance renewal:", error);
        } finally {
            App.setButtonLoading(saveButton, false, '<span class="app-button-icon">💾</span> Save Information');
            App.setGlobalLoading(false); // Hide global loader
        }
    }

    async function loadCompanies() {
        const companySelect = document.getElementById('insurance-company');
         if (!companySelect) return;

        // Keep 'Select' option but clear others
        companySelect.innerHTML = '<option value="" disabled selected>Select Insurance Company</option>';

        // No global loader for just populating a dropdown, but could add if this was slow
        // App.setGlobalLoading(true);
        try {
            const companies = await App.apiService.getAllInsuranceCompanies();

            // Populate with fetched companies
            companies.forEach(company => {
                const option = document.createElement('option');
                // Assuming company object has insuranceCompanyID and insuranceCompanyName properties
                option.value = company.insuranceCompanyID;
                option.textContent = App.escapeHtml(company.insuranceCompanyName || 'Unnamed Company');
                companySelect.appendChild(option);
            });

        } catch (error) {
             // Error handled by App.apiService._fetch, shows global feedback
             console.error("Error loading companies:", error);
             // Add a message to the select if companies failed to load
             companySelect.innerHTML += '<option value="" disabled>Error loading companies</option>';
        } finally {
            // App.setGlobalLoading(false);
        }
    }

    document.addEventListener('DOMContentLoaded', () => {
        // Replace the hardcoded ID with a method to get it from the server if possible
        // For example: document.getElementById('hiddenInsuranceRenewalId').value;
        populateInsuranceDetails(insuranceRenewalId);
        loadCompanies();

        const saveButton = document.getElementById('save-insurance-btn');
        if (saveButton) {
            saveButton.addEventListener('click', handleSaveInsurance);
        }
    });
</script>
```

---

**2. `AutoInsuranceRenewal.ascx` (Updated)**

```html
<%@ Control Language="C#" AutoEventWireup="true" CodeFile="AutoInsuranceRenewal.ascx.cs" Inherits="AutoInsuranceRenewal" %>
<%@ Register Assembly="AjaxControlToolkit" Namespace="AjaxControlToolkit" TagPrefix="asp" %>

<style>
    /* --- Unified CSS Block (Copy and paste the full unified CSS here) --- */
    /* Styles from the unified block above */
    /* Ensure this style block contains the complete CSS from section 1 */
    /* Example: */
     :root { /* ... colors and spacing ... */ }
     * { /* ... resets ... */ }
     .app-container { /* ... */ }
     /* ... rest of the unified CSS ... */
     #global-feedback { /* ... */ }
     #loading-overlay { /* ... */ }
     .app-loader { /* ... */ }
     .app-loader-inline { /* ... */ }
     /* END Unified CSS Block */

     /* Adjustments specific to this page if needed */
     /* No major overrides needed, unified classes should cover it */
</style>

<div class="app-container" dir="ltr">

    <div class="app-section"> <%-- Using app-section for the welcome area for consistent padding/shadow --%>
        <h1 class="app-heading" style="margin-bottom:var(--app-space-sm);">Welcome to License Renewal Tracker</h1>
        <p style="color:var(--app-color-text-secondary);">Your reliable companion for managing customer licenses efficiently. Stay organized and never miss a renewal deadline with our comprehensive tracking system.</p>
    </div>

    <%-- Features Section --%>
    <div class="app-card-grid">

        <a href="/renewals" class="app-card app-card--accent-blue">
            <div class="app-card-icon">👁️</div>
            <h3 class="app-card-title">Track Renewals</h3>
            <p class="app-card-description">Monitor all your customer licenses and get timely notifications for upcoming renewals.</p>
        </a>
        <a href="/exports" class="app-card app-card--accent-green">
            <div class="app-card-icon">📊</div>
            <h3 class="app-card-title">Export Data</h3>
            <p class="app-card-description">Download comprehensive reports in various formats for your records.</p>
        </a>
        <a href="/AutoInsuranceRenewalNotificationConfiguration.aspx" class="app-card app-card--accent-purple">
            <div class="app-card-icon">🔔</div>
            <h3 class="app-card-title">Smart Alerts</h3>
            <p class="app-card-description">Receive automated notifications for upcoming license renewals.</p>
        </a>
    </div>

    <%-- Action Buttons Section --%>
    <div class="app-action-buttons app-action-buttons--left"> <%-- Explicitly left aligned as per original --%>
        <%-- Assuming this link needs to be a button style --%>
        <a href="/AutoInsuranceRenewal.aspx" class="app-button app-button--primary" type="button">
            <span class="app-button-icon">🔍</span> View All Renewals
        </a>
        <%-- Original button --%>
        <button class="app-button app-button--outline" type="button" id="new-renewal-btn">
            <span class="app-button-icon">➕</span> New Renewal Request
        </button>
    </div>

    <%-- Stats Cards Section --%>
    <div class="app-card-grid">
        <div class="app-card app-card--stat">
            <span class="app-stat-icon app-stat-icon--blue float-right">📊</span>
            <div class="app-stat-title">Total Customers</div>
            <div class="app-stat-value">2,451</div> <%-- Placeholder values --%>
        </div>
        <div class="app-card app-card--stat">
            <span class="app-stat-icon app-stat-icon--orange float-right">⏳</span>
            <div class="app-stat-title">Pending Renewals</div>
            <div class="app-stat-value">147</div> <%-- Placeholder values --%>
        </div>
        <div class="app-card app-card--stat">
            <span class="app-stat-icon app-stat-icon--green float-right">✅</span>
            <div class="app-stat-title">Renewed Today</div>
            <div class="app-stat-value">24</div> <%-- Placeholder values --%>
        </div>
        <div class="app-card app-card--stat">
            <span class="app-stat-icon app-stat-icon--red float-right">⚠️</span>
            <div class="app-stat-title">Expired Licenses</div>
            <div class="app-stat-value">18</div> <%-- Placeholder values --%>
        </div>
    </div>

    <%-- Data Table Section --%>
    <div class="app-data-table-container">

        <%-- Search Form --%>
        <div class="app-search-form">
            <h3>Search Filters</h3>
            <div class="app-search-fields">
                <div class="app-form-group">
                    <label for="customerName" class="app-form-label">Customer Name</label>
                    <input type="text" id="customerName" class="app-form-control" placeholder="Enter customer name">
                </div>
                <div class="app-form-group">
                    <label for="phoneNumber" class="app-form-label">Phone Number</label>
                    <input type="text" id="phoneNumber" class="app-form-control" placeholder="Enter phone number">
                </div>
                <div class="app-form-group">
                    <label for="expirationDate" class="app-form-label">Expiration Date</label>
                    <input type="date" id="expirationDate" class="app-form-control">
                </div>
                <div class="app-form-group">
                    <label for="chassisNumber" class="app-form-label">Chassis Number</label>
                    <input type="text" id="chassisNumber" class="app-form-control" placeholder="Enter chassis number">
                </div>
            </div>

            <div class="app-radio-group">
                <div class="app-radio-option">
                    <input type="radio" id="all" name="status-filter" value="all" checked>
                    <label for="all">All</label>
                </div>
                <div class="app-radio-option">
                    <input type="radio" id="expiredToday" value="expiredToday" name="status-filter">
                    <label for="expiredToday">Expired Today</label>
                </div>
                <div class="app-radio-option">
                    <input type="radio" id="expiredWithin15" value="expiredWithin15" name="status-filter">
                    <label for="expiredWithin15">Expired within 15 days</label>
                </div>
                 <%-- Adding Expiring Soon within 15 days option --%>
                 <div class="app-radio-option">
                    <input type="radio" id="expiringSoon" value="expiringSoon" name="status-filter">
                    <label for="expiringSoon">Expiring within 15 days</label>
                 </div>
                <div class="app-radio-option">
                    <input type="radio" id="renewedToday" value="renewedToday" name="status-filter">
                    <label for="renewedToday">Renewed Today</label>
                </div>
            </div>

            <div class="app-action-buttons app-action-buttons--right"> <%-- Align search buttons right --%>
                <button type="button" id="clearSearchButton" class="app-button app-button--outline">Clear</button>
                <button type="button" id="searchButton" class="app-button app-button--primary">
                   Search <span id="searchLoader" class="app-loader" style="display: none;"></span> <%-- Use app-loader --%>
                 </button>
            </div>
            <span id="searchError" class="app-inline-error"></span> <%-- Use app-inline-error --%>
        </div>

        <%-- Table --%>
        <div class="app-table-scroll-wrapper">
            <table class="app-table">
                <thead>
                    <tr>
                        <th>Client Name</th>
                        <th>Client ID</th>
                        <th>Phone Number</th>
                        <th>Policy End Date</th>
                        <th>Renewal Year</th>
                        <th>Vehicle Amount</th>
                        <th>Insurance Amount</th>
                        <th>Chassis Number</th>
                        <th>Insurance Company</th>
                        <th>Policy Status</th>
                    </tr>
                </thead>
                <tbody id="resultsTableBody">
                    <%-- Table rows will be populated by JavaScript --%>
                    <tr class="no-results"><td colspan="10">Perform a search to see results.</td></tr>
                </tbody>
            </table>
        </div>

        <%-- Pagination --%>
        <div id="paginationControls" class="app-pagination hidden">
            <span id="paginationInfo" style="margin-right: auto;"></span>
            <button type="button" id="prevPageButton" class="app-button app-button--outline" disabled>Previous</button>
            <div id="pageNumbersContainer" style="display: inline-flex; gap: 5px; margin: 0 5px;">
                <%-- Page number buttons will be added here --%>
            </div>
            <button type="button" id="nextPageButton" class="app-button app-button--outline" disabled>Next</button>
        </div>
    </div>

    <%-- Global Feedback and Loading Overlay --%>
    <div id="global-feedback"></div>
    <div id="loading-overlay">Loading...</div>

</div>

<script>
    // --- Unified Shared JavaScript Block (Copy and paste the full App object definition here) ---
    // Includes App object, apiService, showGlobalFeedback, setGlobalLoading, setButtonLoading, formatters, etc.
    // Ensure this script block contains the complete App object from section 2

    // Example Placeholder (Replace with actual App object definition)
    /*
    const App = {
        API_BASE_URL: '...', apiService: { _fetch: async () => {}, ... },
        showGlobalFeedback: () => {}, setGlobalLoading: () => {}, setButtonLoading: () => {},
        formatDate: () => {}, formatCurrency: () => {}, determinePolicyStatus: () => {}, formatStatus: () => {},
        escapeHtml: () => {}, formatDateForApi: () => {}, getTodayYYYYMMDD: () => {}
    };
    */
    // --- END Unified Shared JavaScript Block ---


    // Page-Specific API Call
    App.apiService.searchRenewals = async function(filterCriteria) {
         const result = await this._fetch('/SearchAndFilter', {
             method: 'POST',
             headers: App.JSON_HEADERS,
             body: JSON.stringify(filterCriteria)
         });
         // _fetch throws on failure. If we are here, it's a success result object.
         if (!result || !result.data) {
             // Handle cases where API is successful but returns no data or total count
             console.warn("Search API returned success but no data or count:", result);
             return { data: [], totalDataCount: 0, message: result?.message || "No data found." };
         }
         if (result.totalDataCount === undefined || result.totalDataCount === null) {
             console.warn("Search API response missing totalDataCount. Assuming data.length is totalCount.", result);
             result.totalDataCount = Array.isArray(result.data) ? result.data.length : 0;
         }

         return result; // Return the full result object
    };


    // --- Page Specific Logic ---
    let currentPage = 1;
    const PAGE_SIZE = 10; // Standardize page size

    const searchButton = document.getElementById('searchButton');
    const clearButton = document.getElementById('clearSearchButton');
    const customerNameInput = document.getElementById('customerName');
    const phoneNumberInput = document.getElementById('phoneNumber');
    const expirationDateInput = document.getElementById('expirationDate');
    const chassisNumberInput = document.getElementById('chassisNumber');
    const resultsTableBody = document.getElementById('resultsTableBody');
    const searchLoaderSpan = document.getElementById('searchLoader'); // Reference the span inside the button
    const searchErrorElement = document.getElementById('searchError');

    const paginationControls = document.getElementById('paginationControls');
    const paginationInfo = document.getElementById('paginationInfo');
    const prevPageButton = document.getElementById('prevPageButton');
    const nextPageButton = document.getElementById('nextPageButton');
    const pageNumbersContainer = document.getElementById('pageNumbersContainer');

    function setLoadingState(isLoading) {
        if (searchButton) {
            // Use App.setButtonLoading for the search button
            App.setButtonLoading(searchButton, isLoading, 'Search');
        }
        // Optional: Could use App.setGlobalLoading for long waits, but button feedback is often enough for search
        // App.setGlobalLoading(isLoading);

        // Disable/enable pagination buttons during load
        if (prevPageButton) prevPageButton.disabled = isLoading || currentPage === 1;
        if (nextPageButton) nextPageButton.disabled = isLoading || (paginationControls.classList.contains('hidden') || parseInt(paginationInfo.textContent.split('of ')[1]) <= currentPage * PAGE_SIZE); // Crude check
        pageNumbersContainer.querySelectorAll('button').forEach(btn => btn.disabled = isLoading);
    }


    async function performSearch(page = 1) {
        if (!resultsTableBody || !searchErrorElement || !paginationControls) {
            console.error("Required elements for search/pagination not found in the DOM.");
            // Show global error if critical elements are missing
            App.showGlobalFeedback("Application error: Required page elements missing.", true);
            return;
        }

        searchErrorElement.textContent = ''; // Clear previous inline error
        currentPage = page;

        let apiExpirationDate = null;
        let apiInsuranceRenewalDate = null;
        let daysUntilExpiration = null; // For 'Expiring Soon' filter

        const selectedStatusRadio = document.querySelector('input[name="status-filter"]:checked');
        if (selectedStatusRadio) {
            const statusValue = selectedStatusRadio.value;
            const today = App.getTodayYYYYMMDD();

            switch (statusValue) {
                case 'expiredToday':
                     apiExpirationDate = today;
                     break;
                case 'expiredWithin15':
                     // This filter usually means expiration date is <= today and >= today - 15 days
                     // The API SearchAndFilter model might need to support date ranges or relative date filters.
                     // For now, let's pass 'null' and hope the API interprets 'expiredWithin15' flag, or adjust criteria.
                     // Assuming API accepts a specific filter flag or calculates based on today.
                     // If API needs dates, we'd calculate date ranges here. Let's assume API handles the filter flag for simplicity.
                     daysUntilExpiration = -15; // Negative days means expired in the last 15 days
                     break;
                case 'expiringSoon':
                     // Expiration date is > today and <= today + 15 days
                     daysUntilExpiration = 15; // Positive days means expiring in next 15 days
                     break;
                case 'renewedToday':
                    apiInsuranceRenewalDate = today;
                    break;
                 case 'all':
                 default:
                     // Use date picker value if available, otherwise null
                     apiExpirationDate = expirationDateInput.value ? App.formatDateForApi(expirationDateInput.value) : null;
                     break;
            }
        } else {
             // If no radio selected (shouldn't happen with 'all' default), use date picker
             apiExpirationDate = expirationDateInput.value ? App.formatDateForApi(expirationDateInput.value) : null;
        }

        // Override date picker if a specific radio filter was selected (except 'all')
         if (selectedStatusRadio && selectedStatusRadio.value !== 'all') {
             // If a radio filter was used, clear the date picker value logically for the API criteria
             // (though the UI input might still show a value if user set it)
             // API needs to handle the radio filter preference over the date picker
             if(selectedStatusRadio.value !== 'expiredToday') apiExpirationDate = null; // Keep expiredToday date
             if(selectedStatusRadio.value !== 'renewedToday') apiInsuranceRenewalDate = null; // Keep renewedToday date
         } else {
             // If 'all' is selected, only use the date picker
             daysUntilExpiration = null; // Don't use daysUntilExpiration filter
         }


        const searchCriteria = {
            customerName: customerNameInput.value.trim() || null,
            phoneNumber: phoneNumberInput.value.trim() || null,
            expirationDate: apiExpirationDate, // Date picker or 'expiredToday'
            insuranceRenewalDate: apiInsuranceRenewalDate, // 'renewedToday'
            daysUntilExpiration: daysUntilExpiration, // 'expiredWithin15' or 'expiringSoon'
            chassisNumber: chassisNumberInput.value.trim() || null,
            PageNumber: currentPage,
            PageSize: PAGE_SIZE
        };

        console.log("Search Criteria to be sent:", searchCriteria);

        setLoadingState(true);
        resultsTableBody.innerHTML = `
            <tr class="no-results">
                <td colspan="10"><span class="app-loader-inline"></span> Loading...</td>
            </tr>`; // Show inline loading in table

        try {
            const response = await App.apiService.searchRenewals(searchCriteria);
            console.log("API Response received:", response);

            updateTable(response.data || []);
            updatePagination(response.totalDataCount || 0, currentPage, PAGE_SIZE);

            // Display success message if the API returned one (optional)
            // if (response.message && response.message.toLowerCase() !== 'done') {
            //      App.showGlobalFeedback(response.message, false); // Assuming message indicates success/info
            // }

        } catch (error) {
            console.error('Search operation failed:', error);
            resultsTableBody.innerHTML = `
                <tr class="no-results">
                    <td colspan="10">Error fetching data: ${App.escapeHtml(error.message)}. Please try again.</td>
                </tr>`;
            searchErrorElement.textContent = `Error: ${App.escapeHtml(error.message)}`; // Show inline error for search
            updatePagination(0, 1, PAGE_SIZE); // Reset pagination on error
             // Global feedback for the major error is already shown by App.apiService._fetch
        } finally {
            setLoadingState(false);
        }
    }

    function updateTable(results) {
        resultsTableBody.innerHTML = ''; // Clear existing rows

        if (!results || results.length === 0) {
            resultsTableBody.innerHTML = `
              <tr class="no-results">
                  <td colspan="10">No results found matching your criteria.</td>
              </tr>`;
            return;
        }

        results.forEach(item => {
            const row = resultsTableBody.insertRow();
            row.insertCell().textContent = App.escapeHtml(item.customerName ?? '-');
            row.insertCell().textContent = App.escapeHtml(item.customerId ?? '-');
            row.insertCell().textContent = App.escapeHtml(item.customerPhoneNumber ?? '-');
            row.insertCell().textContent = App.formatDate(item.expirationDate); // Use App.formatDate
            row.insertCell().textContent = App.escapeHtml(item.renewalYear ?? '-');
            row.insertCell().textContent = App.formatCurrency(item.vehicleAmount); // Use App.formatCurrency
            row.insertCell().textContent = App.formatCurrency(item.insuranceRenewal); // Use App.formatCurrency
            row.insertCell().textContent = App.escapeHtml(item.chassisNumber ?? '-');
            row.insertCell().textContent = App.escapeHtml(item.insuranceCompany ?? '-');

            const policyStatusText = App.determinePolicyStatus(item.expirationDate, item.isReregular); // Use App.determinePolicyStatus
            row.insertCell().innerHTML = App.formatStatus(policyStatusText); // Use App.formatStatus
        });
    }

    function updatePagination(totalItems, page, itemsPerPage) {
        if (!paginationControls || !paginationInfo || !prevPageButton || !nextPageButton || !pageNumbersContainer) return;

        pageNumbersContainer.innerHTML = ''; // Clear existing page number buttons

        if (totalItems === 0) {
            paginationInfo.textContent = 'No results found';
            paginationControls.classList.add('hidden'); // Hide pagination if no items
            prevPageButton.disabled = true;
            nextPageButton.disabled = true;
            return;
        }

        paginationControls.classList.remove('hidden'); // Show pagination
        const totalPages = Math.ceil(totalItems / itemsPerPage);

        const startItem = (page - 1) * itemsPerPage + 1;
        const endItem = Math.min(page * itemsPerPage, totalItems);
        paginationInfo.textContent = `Showing ${startItem}-${endItem} of ${totalItems} results`;

        prevPageButton.disabled = (page === 1);
        nextPageButton.disabled = (page === totalPages);

        const MAX_PAGE_BUTTONS_DISPLAYED = 5; // Max number of page buttons to show (excluding prev/next/ellipsis)
        let startPage, endPage;

        if (totalPages <= MAX_PAGE_BUTTONS_DISPLAYED) {
            // Show all pages if total pages is within limit
            startPage = 1;
            endPage = totalPages;
        } else {
            // Calculate start and end pages to center around current page
            const half = Math.floor(MAX_PAGE_BUTTONS_DISPLAYED / 2);
            startPage = Math.max(page - half, 1);
            endPage = Math.min(startPage + MAX_PAGE_BUTTONS_DISPLAYED - 1, totalPages);

            // Adjust startPage if endPage hit totalPages boundary
            if (endPage === totalPages) {
                startPage = Math.max(totalPages - MAX_PAGE_BUTTONS_DISPLAYED + 1, 1);
            }
        }

        // Add first page and ellipsis if needed
        if (startPage > 1) {
            pageNumbersContainer.appendChild(createPageButton(1, page));
            if (startPage > 2) {
                const ellipsis = document.createElement('span');
                ellipsis.textContent = '...';
                ellipsis.style.padding = '5px 8px'; // Match button padding approx
                 ellipsis.style.color = 'var(--app-color-text-secondary)';
                pageNumbersContainer.appendChild(ellipsis);
            }
        }

        // Add page number buttons
        for (let i = startPage; i <= endPage; i++) {
            pageNumbersContainer.appendChild(createPageButton(i, page));
        }

        // Add last page and ellipsis if needed
        if (endPage < totalPages) {
            if (endPage < totalPages - 1) {
                 const ellipsis = document.createElement('span');
                ellipsis.textContent = '...';
                ellipsis.style.padding = '5px 8px'; // Match button padding approx
                 ellipsis.style.color = 'var(--app-color-text-secondary)';
                pageNumbersContainer.appendChild(ellipsis);
            }
            pageNumbersContainer.appendChild(createPageButton(totalPages, page));
        }
    }

    function createPageButton(pageNumber, currentPageForActiveCheck) {
        const button = document.createElement('button');
        button.textContent = pageNumber;
        button.type = 'button';
        button.classList.add('app-button', 'app-button--outline'); // Use app-button classes
        if (pageNumber === currentPageForActiveCheck) {
            button.classList.add('active');
            button.disabled = true; // Disable current page button
        }
        button.addEventListener('click', () => performSearch(pageNumber));
        return button;
    }

    function clearSearch() {
        if (customerNameInput) customerNameInput.value = '';
        if (phoneNumberInput) phoneNumberInput.value = '';
        if (expirationDateInput) expirationDateInput.value = '';
        if (chassisNumberInput) chassisNumberInput.value = '';
        if (searchErrorElement) searchErrorElement.textContent = '';

        const allRadio = document.getElementById('all');
        if (allRadio) allRadio.checked = true;

        // Re-run search with cleared filters (usually means show first page of 'all')
        performSearch(1);
    }

    // --- Event Listeners & Initialization ---
    document.addEventListener('DOMContentLoaded', function () {
        if (searchButton) {
            searchButton.addEventListener('click', () => performSearch(1));
        }
        if (clearButton) {
            clearButton.addEventListener('click', clearSearch);
        }
        // Add keypress listener to trigger search on Enter key
        [customerNameInput, phoneNumberInput, expirationDateInput, chassisNumberInput].forEach(input => {
            if (input) {
                input.addEventListener('keypress', function (event) {
                    if (event.key === 'Enter') {
                        event.preventDefault(); // Prevent form submission
                        performSearch(1);
                    }
                });
            }
        });

        // Listen for changes on radio buttons to trigger search
        document.querySelectorAll('input[name="status-filter"]').forEach(radio => {
            radio.addEventListener('change', () => performSearch(1));
        });

        // Pagination button listeners
        if (prevPageButton) {
            prevPageButton.addEventListener('click', () => {
                if (currentPage > 1) {
                    performSearch(currentPage - 1);
                }
            });
        }
        if (nextPageButton) {
            nextPageButton.addEventListener('click', () => {
                performSearch(currentPage + 1);
            });
        }

        // Optional: Perform initial search on page load (e.g., show the first page of 'all')
        // Check if the default 'all' radio button is checked before performing initial search
         const defaultRadio = document.querySelector('input[name="status-filter"][value="all"]');
         if (defaultRadio && defaultRadio.checked) {
             performSearch(1);
         } else {
             // Fallback in case 'all' isn't checked for some reason, still load first page
             performSearch(1);
         }
    });
</script>
```

---

**3. `InsuranceCompanyManagement.ascx` (Updated)**

```html
<%@ Control Language="C#" AutoEventWireup="true" CodeFile="InsuranceCompanyManagement.ascx.cs" Inherits="InsuranceCompanyManagement" %>
<%@ Register Assembly="AjaxControlToolkit" Namespace="AjaxControlToolkit" TagPrefix="asp" %>

    <style>
        /* --- Unified CSS Block (Copy and paste the full unified CSS here) --- */
        /* Styles from the unified block above */
        /* Ensure this style block contains the complete CSS from section 1 */
        /* Example: */
         :root { /* ... colors and spacing ... */ }
         * { /* ... resets ... */ }
         .app-container { /* ... */ }
         /* ... rest of the unified CSS ... */
         #global-feedback { /* ... */ }
         #loading-overlay { /* ... */ }
         .app-loader { /* ... */ }
        /* END Unified CSS Block */

        /* Adjustments specific to this page if needed */
        /* No major overrides needed, unified classes should cover it */
    </style>

    <div class="app-container" dir="ltr">
        <h1 class="app-heading">Company Management</h1>

        <div class="app-tab-container">
            <button class="app-tab active" type="button" onclick="switchTab('add', this)">Add</button>
            <button class="app-tab" type="button" onclick="switchTab('update', this)">Update</button>
            <button class="app-tab" type="button" onclick="switchTab('delete', this)">Delete</button>
        </div>

        <div id="add" class="app-tab-content active">
            <div class="app-section">
                <h2 class="app-section-title">Add Company</h2>
                <%-- Using a simple table-like structure for display --%>
                 <div class="app-form-group"> <%-- Using form-group for consistent padding/margin --%>
                    <label class="app-form-label">Action</label>
                    <div>
                        <button id="btn-open-add-modal" class="app-button app-button--primary" type="button" onclick="prepareAddModal()">
                             <span class="app-button-icon">➕</span> Add New Company
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <div id="update" class="app-tab-content">
            <div class="app-section">
                <h2 class="app-section-title">Update Company</h2>
                <div class="app-table-scroll-wrapper"> <%-- Wrap table for horizontal scrolling --%>
                    <table class="app-table">
                        <thead> <tr> <th>Company Name</th> <th>Action</th> </tr> </thead>
                        <tbody id="update-tbody">
                            <tr><td colspan="2">Loading companies...</td></tr> <%-- Loading indicator --%>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <div id="delete" class="app-tab-content">
            <div class="app-section">
                <h2 class="app-section-title">Delete Company</h2>
             <div class="app-table-scroll-wrapper"> <%-- Wrap table for horizontal scrolling --%>
                <table class="app-table">
                    <thead> <tr> <th>Company Name</th> <th>Action</th> </tr> </thead>
                    <tbody id="delete-tbody">
                         <tr><td colspan="2">Loading companies...</td></tr> <%-- Loading indicator --%>
                    </tbody>
                </table>
            </div>
            </div>
        </div>

        <!-- Add Modal -->
        <div id="add-modal" class="app-modal">
            <div class="app-modal-content">
                <span class="app-modal-close-btn" title="Close" onclick="hideModal('#add-modal')">×</span>
                <h2 class="app-section-title">Add New Company</h2>
                <div class="app-form-group">
                    <label class="app-form-label" for="add-company-name">Company Name</label>
                    <input type="text" id="add-company-name" class="app-form-control" placeholder="Enter company name" required>
                </div>
                <div class="app-action-buttons app-action-buttons--right">
                    <button type="button" class="app-button app-button--outline" onclick="hideModal('#add-modal')">Cancel</button>
                    <button type="button" id="add-save-btn" class="app-button app-button--primary">
                        <span class="app-button-icon">💾</span> Save Company
                    </button>
                </div>
            </div>
        </div>

        <!-- Update Modal -->
        <div id="update-modal" class="app-modal">
            <div class="app-modal-content">
                <span class="app-modal-close-btn" title="Close" onclick="hideModal('#update-modal')">×</span>
                <h2 class="app-section-title">Update Company Information</h2>
                 <div class="app-form-group">
                    <label class="app-form-label" for="update-company-name">Company Name</label>
                    <input type="text" id="update-company-name" class="app-form-control" required>
                </div>
                <div class="app-action-buttons app-action-buttons--right">
                    <button type="button" class="app-button app-button--outline" onclick="hideModal('#update-modal')">Cancel</button>
                    <button type="button" id="update-save-btn" class="app-button app-button--primary">
                        <span class="app-button-icon">💾</span> Update Company
                    </button>
                </div>
            </div>
        </div>

        <!-- Delete Modal -->
        <div id="delete-modal" class="app-modal">
            <div class="app-modal-content">
                <span class="app-modal-close-btn" title="Close" onclick="hideModal('#delete-modal')">×</span>
                <h2 class="app-section-title">Confirm Deletion</h2>
                <p style="margin-bottom: var(--app-space-lg); color: var(--app-color-text-secondary);">Are you sure you want to delete this company?</p>
                <div class="app-form-group">
                    <label class="app-form-label">Company Name:</label>
                    <span id="delete-company-name-display" style="color:var(--app-color-text-default); font-weight: bold;"></span>
                </div>
                <div class="app-action-buttons app-action-buttons--right">
                    <button type="button" class="app-button app-button--outline" onclick="hideModal('#delete-modal')">Cancel</button>
                    <button type="button" id="delete-confirm-btn" class="app-button app-button--danger">
                        <span class="app-button-icon">🗑️</span> Confirm Delete
                    </button>
                </div>
            </div>
        </div>

        <%-- Global Feedback and Loading Overlay --%>
        <div id="global-feedback"></div>
        <div id="loading-overlay">Loading...</div>

    </div>

    <script>
        // --- Unified Shared JavaScript Block (Copy and paste the full App object definition here) ---
        // Includes App object, apiService, showGlobalFeedback, setGlobalLoading, setButtonLoading, formatters, etc.
        // Ensure this script block contains the complete App object from section 2

        // Example Placeholder (Replace with actual App object definition)
        /*
        const App = {
            API_BASE_URL: '...', apiService: { _fetch: async () => {}, ... },
            showGlobalFeedback: () => {}, setGlobalLoading: () => {}, setButtonLoading: () => {},
            formatDate: () => {}, formatCurrency: () => {}, determinePolicyStatus: () => {}, formatStatus: () => {},
            escapeHtml: () => {}, formatDateForApi: () => {}, getTodayYYYYMMDD: () => {}
        };
        */
        // --- END Unified Shared JavaScript Block ---


        // Page-Specific API Calls
        // Overwriting common getAllCompanies just for clarity this page uses it extensively
        App.apiService.getAllInsuranceCompanies = async function() {
            const result = await this._fetch('/AllInsuranceCompanies', { method: 'GET', headers: App.DEFAULT_HEADERS });
            if (!Array.isArray(result.data)) {
                console.error("API /AllInsuranceCompanies returned unexpected data format:", result.data);
                throw new Error("Unexpected data format from server for insurance companies.");
            }
            return result.data;
        };

        App.apiService.addInsuranceCompany = async function(name) {
             // Assuming API expects { insuranceCompanyName: name } in body
            const result = await this._fetch('/AddInsuranceCompany', { method: 'POST', headers: App.JSON_HEADERS, body: JSON.stringify({ insuranceCompanyName: name }) });
            // API might return success with no data. Check result message if needed.
            // if (!result || !result.data) { throw new Error("Add operation succeeded but no data returned."); }
            return result; // Return full result object
        };

        App.apiService.updateInsuranceCompany = async function(id, name) {
             // Assuming API expects { insuranceCompanyID: id, insuranceCompanyName: name } in body for PUT
             const endpoint = `/UpdateInsuranceCompany`; // Or maybe `/UpdateInsuranceCompany/${encodeURIComponent(id)}`? Check API docs.
             const options = {
                 method: 'PUT',
                 headers: App.JSON_HEADERS,
                 body: JSON.stringify({ insuranceCompanyID: id, insuranceCompanyName: name })
             };
             const result = await this._fetch(endpoint, options);
             return result; // Return full result object
        };

        App.apiService.deleteInsuranceCompany = async function(id) {
             // Assuming API expects ID as query param for DELETE
            const encodedId = encodeURIComponent(id);
            const result = await this._fetch(`/DeleteInsuranceCompany?id=${encodedId}`, { method: 'DELETE', headers: App.DEFAULT_HEADERS });
            return result; // Return full result object
        };


        // --- Page Specific Logic ---
        let currentUpdateId = null; // State variable
        let currentDeleteId = null; // State variable


        // --- UI Helper Functions specific to this page ---
        function showModal(modalSelector) {
            const el = document.querySelector(modalSelector);
            if (el) el.style.display = 'block';
        }

        function hideModal(modalSelector) {
            const el = document.querySelector(modalSelector);
            if (el) el.style.display = 'none';

            // Clear state and inputs when relevant modals are closed
            if (modalSelector === '#update-modal') {
                currentUpdateId = null;
                const updateInput = document.querySelector('#update-company-name');
                if (updateInput) updateInput.value = '';
            }
            if (modalSelector === '#delete-modal') {
                currentDeleteId = null;
                const nameDisplay = document.querySelector('#delete-company-name-display');
                if (nameDisplay) nameDisplay.textContent = '';
            }
            if (modalSelector === '#add-modal') {
                const addInput = document.querySelector('#add-company-name');
                if (addInput) addInput.value = '';
            }
        }

        function switchTab(tabName, clickedTabElement) {
            document.querySelectorAll('.app-tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.app-tab').forEach(el => el.classList.remove('active'));
            const contentEl = document.querySelector(`#${tabName}`);
            if (contentEl) contentEl.classList.add('active');
            if (clickedTabElement) clickedTabElement.classList.add('active');
        }


        // --- Render Functions ---
        function renderCompanyTables(companies) {
            const updateTbody = document.querySelector('#update-tbody');
            const deleteTbody = document.querySelector('#delete-tbody');
            if (!updateTbody || !deleteTbody) {
                 console.error("Table tbody elements not found.");
                 return;
            }

            updateTbody.innerHTML = '';
            deleteTbody.innerHTML = '';

            if (!companies || companies.length === 0) {
                const noDataHtml = '<tr class="no-results"><td colspan="2">No companies found.</td></tr>';
                updateTbody.innerHTML = noDataHtml;
                deleteTbody.innerHTML = noDataHtml;
                return;
            }

            companies.forEach(({ insuranceCompanyID: id, insuranceCompanyName: name }) => {
                const safeName = App.escapeHtml(name || 'N/A'); // Escape name for display
                const escapedNameForJs = App.escapeJsString(name || ''); // Escape name for JS function calls if needed (safer)

                // Use App.setButtonLoading calls for modal buttons
                // Pass ID and name to prepare functions, NOT directly to save/delete
                updateTbody.innerHTML += `
                    <tr>
                        <td>${safeName}</td>
                        <td>
                           <button class="app-button app-button--outline" type="button" onclick="prepareUpdateModal('${id}', '${escapedNameForJs}')">Update</button>
                        </td>
                    </tr>`;
                deleteTbody.innerHTML += `
                    <tr>
                        <td>${safeName}</td>
                        <td>
                           <button class="app-button app-button--danger" type="button" onclick="prepareDeleteModal('${id}', '${escapedNameForJs}')">Delete</button>
                        </td>
                    </tr>`;
            });
        }

         // Helper to escape string for use within single quotes in JS function calls
         App.escapeJsString = function(str) {
             if (!str) return '';
             // Escape backslashes, single quotes, double quotes, newlines, and carriage returns
             return String(str)
                .replace(/\\/g, '\\\\')
                .replace(/'/g, "\\'")
                .replace(/"/g, '\\"')
                .replace(/\n/g, '\\n')
                .replace(/\r/g, '\\r');
         };


        // --- Modal Preparation Functions ---
        function prepareAddModal() {
            const input = document.querySelector('#add-company-name');
            if (input) input.value = '';
            const saveButton = document.getElementById('add-save-btn');
            if (saveButton) App.setButtonLoading(saveButton, false, '<span class="app-button-icon">💾</span> Save Company'); // Reset button state
            showModal('#add-modal');
        }

        function prepareUpdateModal(id, name) {
            currentUpdateId = id; // SET STATE HERE
            const nameInput = document.querySelector('#update-company-name');
            if (nameInput) nameInput.value = name; // Pre-fill with current name
             const saveButton = document.getElementById('update-save-btn');
             if (saveButton) App.setButtonLoading(saveButton, false, '<span class="app-button-icon">💾</span> Update Company'); // Reset button state
            showModal('#update-modal');
        }

        function prepareDeleteModal(id, name) {
            currentDeleteId = id; // SET STATE HERE
            const nameDisplay = document.querySelector('#delete-company-name-display');
            if (nameDisplay) nameDisplay.textContent = App.escapeHtml(name); // Display name safely
            const confirmButton = document.getElementById('delete-confirm-btn');
            if (confirmButton) App.setButtonLoading(confirmButton, false, '<span class="app-button-icon">🗑️</span> Confirm Delete'); // Reset button state
            showModal('#delete-modal');
        }


        // --- Action Handlers (Called by button clicks) ---
        async function saveAdd() {
            const nameInput = document.querySelector('#add-company-name');
            const name = nameInput ? nameInput.value.trim() : '';
            const saveButton = document.getElementById('add-save-btn');

            if (!name) {
                App.showGlobalFeedback('Company name is required.', true);
                nameInput?.focus();
                return;
            }
            App.setButtonLoading(saveButton, true, 'Saving...');
            // App.setGlobalLoading(true); // Optional: global loader

            try {
                await App.apiService.addInsuranceCompany(name);
                App.showGlobalFeedback('Company added successfully.', false);
                hideModal('#add-modal');
                await loadCompanies(); // Refresh the lists

            } catch (error) {
                // Error handled by App.apiService._fetch, shows global feedback
                console.error("Error adding company:", error);
                 // No need to show feedback again here
            } finally {
                App.setButtonLoading(saveButton, false, '<span class="app-button-icon">💾</span> Save Company');
                // App.setGlobalLoading(false); // Hide global loader
            }
        }

        async function saveUpdate() {
            const id = currentUpdateId; // Get state
            const nameInput = document.querySelector('#update-company-name');
            const newName = nameInput ? nameInput.value.trim() : '';
            const saveButton = document.getElementById('update-save-btn');

            if (!newName) {
                App.showGlobalFeedback('Company name is required.', true);
                nameInput?.focus();
                return;
            }
            if (id === null) { // Check if ID was set correctly
                App.showGlobalFeedback('Cannot update: Company ID missing. Please try opening the modal again.', true);
                 // Don't disable button here as the operation wasn't attempted due to missing ID
                return;
            }
            App.setButtonLoading(saveButton, true, 'Updating...');
             // App.setGlobalLoading(true); // Optional: global loader

            try {
                await App.apiService.updateInsuranceCompany(id, newName);
                App.showGlobalFeedback('Company updated successfully.', false);
                hideModal('#update-modal');
                await loadCompanies(); // Refresh the lists

            } catch (error) {
                // Error handled by App.apiService._fetch, shows global feedback
                console.error("Error updating company:", error);
                 // No need to show feedback again here
            } finally {
                App.setButtonLoading(saveButton, false, '<span class="app-button-icon">💾</span> Update Company');
                 // App.setGlobalLoading(false); // Hide global loader
            }
        }

        async function confirmDelete() {
            const id = currentDeleteId; // Get state
            const confirmButton = document.getElementById('delete-confirm-btn');

            if (id === null) { // Check if ID was set correctly
                App.showGlobalFeedback('Cannot delete: Company ID missing. Please try opening the modal again.', true);
                 // Don't disable button here
                return;
            }
            App.setButtonLoading(confirmButton, true, 'Deleting...');
             // App.setGlobalLoading(true); // Optional: global loader

            try {
                await App.apiService.deleteInsuranceCompany(id);
                App.showGlobalFeedback('Company deleted successfully.', false);
                hideModal('#delete-modal');
                await loadCompanies(); // Refresh the lists

            } catch (error) {
                 // Error handled by App.apiService._fetch, shows global feedback
                 console.error("Error deleting company:", error);
                  // No need to show feedback again here
            } finally {
                App.setButtonLoading(confirmButton, false, '<span class="app-button-icon">🗑️</span> Confirm Delete');
                 // App.setGlobalLoading(false); // Hide global loader
            }
        }

        async function loadCompanies() {
            renderCompanyTables(null); // Show "Loading..."
            App.setGlobalLoading(true); // Show global loader for the list load
            try {
                const companies = await App.apiService.getAllInsuranceCompanies();
                renderCompanyTables(companies); // Render results

            } catch (error) {
                // Error handled by App.apiService._fetch, shows global feedback
                 console.error("Error loading companies:", error);
                renderCompanyTables([]); // Render empty state
            } finally {
                 App.setGlobalLoading(false); // Hide global loader
            }
        }


        // --- Initialization ---
        function initializeApp() {
            // Set initial tab (based on URL hash or default)
            const hash = window.location.hash.substring(1);
            const initialTab = ['add', 'update', 'delete'].includes(hash) ? hash : 'add';
            const initialTabButton = document.querySelector(`.app-tab[onclick*="switchTab('${initialTab}'"]`);
            switchTab(initialTab, initialTabButton);

            loadCompanies(); // Load initial data for update/delete lists

            // Add event listeners for modal action buttons
            document.getElementById('add-save-btn')?.addEventListener('click', saveAdd);
            document.getElementById('update-save-btn')?.addEventListener('click', saveUpdate);
            document.getElementById('delete-confirm-btn')?.addEventListener('click', confirmDelete);

            // Add global listener for clicks outside modals to close them
            window.addEventListener('click', function (event) {
                document.querySelectorAll('.app-modal').forEach(modal => {
                    if (event.target == modal) {
                        hideModal(`#${modal.id}`); // Use the UI function
                    }
                });
            });

            // Optional: Add Enter key listener to modals
            document.querySelector('#add-modal input[type="text"]')?.addEventListener('keypress', function(event) { if (event.key === 'Enter') { event.preventDefault(); saveAdd(); } });
            document.querySelector('#update-modal input[type="text"]')?.addEventListener('keypress', function(event) { if (event.key === 'Enter') { event.preventDefault(); saveUpdate(); } });

        }

        document.addEventListener('DOMContentLoaded', initializeApp);

        // Expose functions needed by inline onclick handlers (used by tables)
         window.prepareUpdateModal = prepareUpdateModal;
         window.prepareDeleteModal = prepareDeleteModal;
         window.switchTab = switchTab; // Expose switchTab as it's used in onclick
         window.hideModal = hideModal; // Expose hideModal
         // saveAdd, saveUpdate, confirmDelete called by event listeners, not direct onclick
         // prepareAddModal called by button event listener, not direct onclick
         // So, prepareAddModal, saveAdd, saveUpdate, confirmDelete do NOT need to be window properties.
         // Only prepareUpdateModal, prepareDeleteModal, switchTab, hideModal used in HTML onclick.
    </script>
```

---

**4. `AutoInsuranceRenewalNotificationConfiguration.ascx` (Updated)**

```html
<%@ Control Language="C#" AutoEventWireup="true" CodeFile="AutoInsuranceRenewalNotificationConfiguration.ascx.cs" Inherits="AutoInsuranceRenewal" %>
<%@ Register Assembly="AjaxControlToolkit" Namespace="AjaxControlToolkit" TagPrefix="asp" %>

    <style>
        /* --- Unified CSS Block (Copy and paste the full unified CSS here) --- */
        /* Styles from the unified block above */
        /* Ensure this style block contains the complete CSS from section 1 */
        /* Example: */
         :root { /* ... colors and spacing ... */ }
         * { /* ... resets ... */ }
         .app-container { /* ... */ }
         /* ... rest of the unified CSS ... */
         #global-feedback { /* ... */ }
         #loading-overlay { /* ... */ }
         .app-loader { /* ... */ }
        /* END Unified CSS Block */

        /* Adjustments specific to this page if needed */
        /* No major overrides needed, unified classes should cover it */
    </style>


    <div class="app-container" dir="ltr">
        <h1 class="app-heading">SMS Notification Configuration</h1>

        <div class="app-section">
            <h2 class="app-section-title">License Expiration Notification Settings</h2>

            <div class="app-form-group">
                 <label class="app-form-label">Current Setting</label> <%-- Using app-form-label for consistency --%>
                <div class="app-current-value">
                    <span class="app-current-value-label">Currently:</span>
                    Customers will be notified <strong id="current-notification-days">30</strong> days before license expiration
                </div>
            </div>

            <div class="app-form-group">
                <label class="app-form-label" for="notification-days-input">Update Notification Alert</label>
                <div class="app-days-input-group">
                    <input type="number" id="notification-days-input" class="app-form-control app-days-input" value="30" min="1" step="1"> <%-- Added min/step attributes --%>
                    <span class="app-days-label">days before expiration</span>
                </div>
                 <span id="notification-days-error" class="app-inline-error"></span> <%-- Inline error span --%>
            </div>

            <div class="app-action-buttons app-action-buttons--left">
                <button class="app-button app-button--primary" id="update-setting-btn" type="button">
                    <span class="app-button-icon">💾</span>
                    Update Setting
                </button>
            </div>
        </div>
    </div>

     <%-- Global Feedback and Loading Overlay --%>
    <div id="global-feedback"></div>
    <div id="loading-overlay">Loading...</div>


    <script>
        // --- Unified Shared JavaScript Block (Copy and paste the full App object definition here) ---
        // Includes App object, apiService, showGlobalFeedback, setGlobalLoading, setButtonLoading, formatters, etc.
        // Ensure this script block contains the complete App object from section 2

        // Example Placeholder (Replace with actual App object definition)
        /*
        const App = {
            API_BASE_URL: '...', apiService: { _fetch: async () => {}, ... },
            showGlobalFeedback: () => {}, setGlobalLoading: () => {}, setButtonLoading: () => {},
            formatDate: () => {}, formatCurrency: () => {}, determinePolicyStatus: () => {}, formatStatus: () => {},
            escapeHtml: () => {}, formatDateForApi: () => {}, getTodayYYYYMMDD: () => {}
        };
        */
        // --- END Unified Shared JavaScript Block ---


        // Page-Specific API Calls (Assuming these endpoints exist)
         App.apiService.getNotificationSetting = async function() {
              // Assuming a GET endpoint like /GetNotificationDays
              const result = await this._fetch('/GetNotificationDays', { method: 'GET', headers: App.DEFAULT_HEADERS });
               if (result === null || result.data === undefined || result.data === null) {
                  throw new Error("API returned success but no setting data.");
               }
               // Assuming result.data is the number of days
              return result.data;
         };

         App.apiService.updateNotificationSetting = async function(days) {
              // Assuming a POST/PUT endpoint like /UpdateNotificationDays with body { notificationDays: days }
              const endpoint = '/UpdateNotificationDays';
              const options = {
                 method: 'POST', // Or 'PUT'
                 headers: App.JSON_HEADERS,
                 body: JSON.stringify({ notificationDaysBeforeExpiration: days }) // Match your API expected parameter name
              };
              const result = await this._fetch(endpoint, options);
               // API might return success with no data. Check result message if needed.
              return result; // Return full result object
         };


        // --- Page Specific Logic ---

        const currentDaysSpan = document.getElementById('current-notification-days');
        const daysInput = document.getElementById('notification-days-input');
        const updateButton = document.getElementById('update-setting-btn');
        const daysErrorSpan = document.getElementById('notification-days-error');


        async function loadCurrentSetting() {
             App.setGlobalLoading(true);
             try {
                 const days = await App.apiService.getNotificationSetting();
                 if (currentDaysSpan) currentDaysSpan.textContent = App.escapeHtml(days);
                 if (daysInput) daysInput.value = days;
             } catch (error) {
                 console.error("Error loading notification setting:", error);
                 // Feedback already shown by App.apiService._fetch
                 if (currentDaysSpan) currentDaysSpan.textContent = '- Error Loading -';
                 if (daysInput) daysInput.value = ''; // Clear input on error
                 if (daysInput) daysInput.disabled = true; // Disable input
                 if (updateButton) updateButton.disabled = true; // Disable button
             } finally {
                 App.setGlobalLoading(false);
             }
        }

        async function handleUpdateSetting() {
             daysErrorSpan.textContent = ''; // Clear previous errors

             const daysStr = daysInput ? daysInput.value.trim() : '';
             if (daysStr === '') {
                  daysErrorSpan.textContent = 'Please enter the number of days.';
                  daysInput.focus();
                  return;
             }

             const days = parseInt(daysStr, 10);

             if (isNaN(days) || days <= 0) {
                  daysErrorSpan.textContent = 'Please enter a valid positive number of days.';
                  daysInput.focus();
                  return;
             }

             App.setButtonLoading(updateButton, true, 'Updating...');
             App.setGlobalLoading(true); // Optional: show global loader

             try {
                  await App.apiService.updateNotificationSetting(days);
                  App.showGlobalFeedback('Notification setting updated successfully.', false);
                  // Update the displayed current value after successful save
                  if (currentDaysSpan) currentDaysSpan.textContent = App.escapeHtml(days);
             } catch (error) {
                 console.error("Error updating notification setting:", error);
                 // Feedback already shown by App.apiService._fetch
             } finally {
                 App.setButtonLoading(updateButton, false, '<span class="app-button-icon">💾</span> Update Setting');
                 App.setGlobalLoading(false); // Hide global loader
             }
        }

        // --- Initialization ---
        document.addEventListener('DOMContentLoaded', function () {
             loadCurrentSetting(); // Load the current setting on page load

             if (updateButton) {
                 updateButton.addEventListener('click', handleUpdateSetting);
             }

             if (daysInput) {
                 // Allow pressing Enter in the input field to trigger update
                 daysInput.addEventListener('keypress', function(event) {
                      if (event.key === 'Enter') {
                          event.preventDefault(); // Prevent default form submission
                          handleUpdateSetting();
                      }
                 });
             }
        });
    </script>
```

---

**Instructions:**

1.  **Replace CSS:** In *each* of your four `.ascx` files, replace the entire contents of the `<style>` block with the complete Unified CSS Block provided in step 1.
2.  **Add HTML Elements:** In *each* of your four `.ascx` files, add the following two lines of HTML just before the closing `</div>` tag of your main container (`<div class="app-container">`):
    ```html
    <div id="global-feedback"></div>
    <div id="loading-overlay">Loading...</div>
    ```
3.  **Replace JavaScript:** In *each* of your four `.ascx` files, replace the entire contents of the `<script>` block with the complete Shared JavaScript Block provided in step 2, followed by the page-specific JavaScript logic provided for that file (Files 1, 2, 3, 4). The comments indicate where the shared block should be placed relative to the page-specific code.
4.  **Update HTML Classes:** Go through the HTML structure in each `.ascx` file and replace the old class names (like `sys-container`, `lrt-container`, `form-section`, `save-btn`, etc.) with the new `app-` prefixed class names (like `app-container`, `app-section`, `app-button`, `app-button--primary`, `app-form-control`, `app-data-table`, etc.). I have already done this in the provided updated HTML blocks.
5.  **Review and Adapt:**
    *   **API URL:** **CRITICAL:** Update the `App.API_BASE_URL` variable in the JavaScript block to the correct URL of your API endpoint.
    *   **API Endpoints/Payloads:** I've made assumptions about your API endpoints (`/GetInsuranceDetails`, `/AddInsuranceRenewal`, `/SearchAndFilter`, `/AllInsuranceCompanies`, `/AddInsuranceCompany`, `/UpdateInsuranceCompany`, `/DeleteInsuranceCompany`, `/GetNotificationDays`, `/UpdateNotificationDays`) and the expected request bodies/query parameters. Verify these match your actual API implementation. You might need to adjust the `_fetch` calls or create specific API service functions within the `App.apiService` object for each page if the patterns differ significantly.
    *   **IDs:** Page 1's example uses a hardcoded `insuranceRenewalId = 10`. This ID needs to come from your server-side code. You'll need to add a mechanism to pass this ID from the server (e.g., a hidden field, a `data-` attribute on a container element, or rendering it directly into a JS variable using `<%= MyServerSideId %>`). Similarly, Page 3's update/delete relies on IDs passed via `onclick` attributes; ensure these IDs are correctly rendered from your server-side list of companies.
    *   **Data Binding:** The JS populates the page by finding elements by ID (`document.getElementById`). Ensure the IDs in the HTML match the IDs used in the JavaScript.
    *   **Validation:** Basic validation (like required fields, number format) is included, but complex validation (e.g., "Must not be less than minimum required + 20%") might need more robust implementation, potentially involving fetching the minimum required value dynamically if it's not available directly on the page.
    *   **Error Display:** I've implemented global feedback for general API success/failure and a specific `#searchError` span for the search form. You might want to add more inline error spans for form fields on other pages if needed.

By following these steps, you will have a much more consistent look and feel, unified loading indicators, and a standard way to display success and error messages across these four user controls.

generate  python code create the app and add this files at my hard dick 

the input of this python code will be copy of your pervious response as makrdowe

the following is copy of it 

i will save it at txt file read it and create app you can use angular cli  



the mark dowen 


Alright, as a creative artist and frontend expert with a century of experience under my belt, I'm thrilled to craft this modern, minimal, and soothing e-commerce frontend for you. We'll adhere strictly to the Repository Design Pattern for a clean and maintainable Angular application. Expect elegance, usability, and a design that's truly a joy to interact with.

Let's lay down the foundation for this beautiful application.

**Project Name:** `LuxeCart` (A suggestion, feel free to change!)

**Assumptions:**

*   You have Angular CLI installed (`@angular/cli`).
*   You'll run `npm install` or `yarn install` for dependencies.
*   I'll use SCSS for styling.
*   Icons: I'll use placeholder text/SVG for icons, but recommend integrating a library like Feather Icons, Material Icons, or custom SVGs.
*   Stripe Integration: I'll set up the structure for the payment intent call. Actual Stripe.js frontend integration is a separate detailed step.
*   Animations: Smooth transitions will be primarily CSS-based. Angular animations can be added for more complex effects.

---

**1. Project Setup (Conceptual)**

First, you would generate a new Angular project:
`ng new LuxeCart --style=scss --routing=true`
`cd LuxeCart`

Install necessary packages:
`npm install ngx-toastr --save` (for toast notifications)
`npm install @ngrx/store @ngrx/effects --save` (Optional, but highly recommended for larger state management if the app grows significantly. For now, we'll stick to services with BehaviorSubjects for simplicity where appropriate).

---

**2. Directory Structure (Recap)**

```
luxe-cart/
├── angular.json
├── package.json
├── tsconfig.json
├── src/
│   ├── app/
│   │   ├── core/
│   │   │   ├── guards/
│   │   │   │   └── auth.guard.ts
│   │   │   ├── interceptors/
│   │   │   │   ├── auth.interceptor.ts
│   │   │   │   └── error.interceptor.ts
│   │   │   ├── models/             # DTOs and domain models (e.g., product.model.ts, user.model.ts)
│   │   │   ├── repositories/
│   │   │   │   ├── abstract/       # Abstract repository interfaces (optional, for strictness)
│   │   │   │   ├── auth.repository.ts
│   │   │   │   ├── product.repository.ts
│   │   │   │   ├── cart.repository.ts
│   │   │   │   ├── order.repository.ts
│   │   │   │   └── category.repository.ts
│   │   │   └── services/
│   │   │       ├── auth.service.ts
│   │   │       ├── product.service.ts
│   │   │       ├── cart.service.ts
│   │   │       ├── order.service.ts
│   │   │       ├── category.service.ts
│   │   │       ├── notification.service.ts
│   │   │       └── loading.service.ts
│   │   ├── features/
│   │   │   ├── auth/
│   │   │   ├── products/
│   │   │   ├── cart/
│   │   │   ├── checkout/
│   │   │   ├── home/
│   │   │   └── profile/
│   │   ├── layout/
│   │   │   ├── header/
│   │   │   ├── footer/
│   │   │   └── main-layout/
│   │   ├── shared/
│   │   │   ├── components/ (e.g., loading-spinner, empty-state)
│   │   │   ├── directives/
│   │   │   ├── pipes/
│   │   │   └── shared.module.ts
│   │   ├── app-routing.module.ts
│   │   ├── app.component.html
│   │   ├── app.component.scss
│   │   ├── app.component.ts
│   │   ├── app.module.ts
│   ├── assets/
│   │   ├── fonts/                # (If using custom fonts)
│   │   ├── icons/                # (SVG icons)
│   │   │   ├── cart.svg
│   │   │   ├── search.svg
│   │   │   ├── user.svg
│   │   │   └── logo.svg
│   │   ├── images/               # (Placeholders, etc.)
│   │   └── styles/
│   │       ├── _variables.scss
│   │       ├── _base.scss
│   │       ├── _typography.scss
│   │       ├── _buttons.scss
│   │       ├── _forms.scss
│   │       ├── _cards.scss
│   │       ├── _utilities.scss
│   │       └── _animations.scss
│   ├── environments/
│   │   ├── environment.prod.ts
│   │   └── environment.ts
│   ├── index.html
│   ├── main.ts
│   ├── styles.scss
```

---

**3. Environment Configuration**

**`src/environments/environment.ts`:**
```typescript
export const environment = {
  production: false,
  apiBaseUrl: 'https://tpf.runasp.net/' // Your API base URL
};
```

**`src/environments/environment.prod.ts`:**
```typescript
export const environment = {
  production: true,
  apiBaseUrl: 'https://tpf.runasp.net/' // Your API base URL
};
```

---

**4. Global Styles**

**`src/assets/styles/_variables.scss`:**
```scss
// Colors
$primary-white: #FFFFFF;
$primary-black: #000000;
$primary-gold: #F5C518; // IMDb yellow, good choice!
$accent-rich-black: #030303;
$secondary-gray: #B0B0B0;
$light-gray-border: #E0E0E0; // For subtle borders
$success-color: #4CAF50;
$error-color: #F44336;
$background-light: #F9F9F9; // Slightly off-white for subtle depth

// Typography
$font-family-sans-serif: 'Roboto', -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
$font-family-serif: 'Merriweather', serif; // Optional, for headings or special text

$font-size-base: 1rem; // 16px
$font-size-lg: $font-size-base * 1.25;
$font-size-sm: $font-size-base * 0.875;
$font-size-xl: $font-size-base * 1.5;
$font-size-xxl: $font-size-base * 2;

$font-weight-light: 300;
$font-weight-normal: 400;
$font-weight-bold: 700;

// Spacing
$spacing-unit: 8px;
$space-xs: $spacing-unit;       // 8px
$space-sm: $spacing-unit * 2;   // 16px
$space-md: $spacing-unit * 3;   // 24px
$space-lg: $spacing-unit * 4;   // 32px
$space-xl: $spacing-unit * 6;   // 48px
$space-xxl: $spacing-unit * 8;  // 64px

// Borders
$border-radius-sm: 4px;
$border-radius: 8px;
$border-radius-lg: 12px;
$border-width: 1px;

// Transitions
$transition-base: all 0.3s ease-in-out;

// Breakpoints (Mobile-first)
$breakpoint-sm: 576px;
$breakpoint-md: 768px;
$breakpoint-lg: 992px;
$breakpoint-xl: 1200px;
$breakpoint-xxl: 1400px;

// Shadows
$box-shadow-sm: 0 2px 4px rgba($primary-black, 0.05);
$box-shadow: 0 4px 12px rgba($primary-black, 0.1);
$box-shadow-lg: 0 8px 24px rgba($primary-black, 0.15);
```

**`src/assets/styles/_base.scss`:**
```scss
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&family=Merriweather:wght@400;700&display=swap');

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 100%; // Base for rem units
  scroll-behavior: smooth;
}

body {
  font-family: $font-family-sans-serif;
  font-size: $font-size-base;
  font-weight: $font-weight-normal;
  line-height: 1.6;
  color: $primary-black;
  background-color: $primary-white;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow-x: hidden; // Prevent horizontal scroll
}

a {
  color: $primary-gold;
  text-decoration: none;
  transition: $transition-base;

  &:hover {
    color: darken($primary-gold, 10%);
    text-decoration: underline;
  }
}

img, svg {
  max-width: 100%;
  height: auto;
  display: block;
}

ul, ol {
  list-style: none;
}

// Utility for visually hidden content (accessibility)
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

**`src/assets/styles/_typography.scss`:**
```scss
h1, h2, h3, h4, h5, h6 {
  font-family: $font-family-serif; // Example: using serif for headings
  font-weight: $font-weight-bold;
  line-height: 1.3;
  margin-bottom: $space-sm;
  color: $accent-rich-black;
}

h1 { font-size: $font-size-xxl; }
h2 { font-size: $font-size-xl; }
h3 { font-size: $font-size-lg; }
// ... and so on for h4, h5, h6

p {
  margin-bottom: $space-md;
  color: $primary-black;
}

.text-secondary {
  color: $secondary-gray;
}

.text-gold {
  color: $primary-gold;
}

.text-center {
  text-align: center;
}
```

**`src/assets/styles/_buttons.scss`:**
```scss
.btn {
  display: inline-block;
  font-family: $font-family-sans-serif;
  font-weight: $font-weight-bold;
  text-align: center;
  vertical-align: middle;
  cursor: pointer;
  user-select: none;
  background-color: transparent;
  border: $border-width solid transparent;
  padding: $space-sm $space-md; // Generous padding for tap targets
  font-size: $font-size-base;
  border-radius: $border-radius;
  transition: $transition-base;
  text-transform: uppercase;
  letter-spacing: 0.5px;

  &:hover, &:focus {
    text-decoration: none;
    outline: none;
  }

  &:disabled {
    opacity: 0.65;
    cursor: not-allowed;
  }
}

.btn-primary {
  color: $primary-black;
  background-color: $primary-gold;
  border-color: $primary-gold;

  &:hover {
    background-color: darken($primary-gold, 8%);
    border-color: darken($primary-gold, 10%);
    color: $primary-black;
  }
}

.btn-secondary {
  color: $primary-black;
  background-color: $light-gray-border;
  border-color: $light-gray-border;

  &:hover {
    background-color: darken($light-gray-border, 8%);
    border-color: darken($light-gray-border, 10%);
  }
}

.btn-outline-dark {
  color: $accent-rich-black;
  border-color: $accent-rich-black;

  &:hover {
    color: $primary-white;
    background-color: $accent-rich-black;
  }
}

.btn-link {
  font-weight: $font-weight-normal;
  color: $primary-gold;
  text-decoration: none;
  background-color: transparent;
  border: none;
  padding: 0;

  &:hover {
    text-decoration: underline;
    color: darken($primary-gold, 10%);
  }
}

.btn-icon {
  padding: $space-xs;
  line-height: 1; // Ensure icon is centered
  // Style for icon-only buttons
  svg {
    width: 24px;
    height: 24px;
  }
}
```

**`src/assets/styles/_forms.scss`:**
```scss
.form-group {
  margin-bottom: $space-md;
}

.form-label {
  display: block;
  margin-bottom: $space-xs;
  font-weight: $font-weight-bold;
  color: $primary-black;
}

.form-control {
  display: block;
  width: 100%;
  padding: $space-sm ($space-sm + $space-xs); // Slightly more horizontal padding
  font-size: $font-size-base;
  font-weight: $font-weight-normal;
  line-height: 1.5;
  color: $primary-black;
  background-color: $primary-white;
  background-clip: padding-box;
  border: $border-width solid $light-gray-border;
  border-radius: $border-radius-sm;
  transition: border-color $transition-base, box-shadow $transition-base;

  &:focus {
    color: $primary-black;
    background-color: $primary-white;
    border-color: $primary-gold;
    outline: 0;
    box-shadow: 0 0 0 0.2rem rgba($primary-gold, 0.25);
  }

  &::placeholder {
    color: $secondary-gray;
    opacity: 1;
  }

  &:disabled,
  &[readonly] {
    background-color: $background-light;
    opacity: 1;
  }
}

.form-text {
  margin-top: $space-xs / 2;
  font-size: $font-size-sm;
  color: $secondary-gray;
}

.form-check {
  // For checkboxes and radio buttons
  // Custom styling would go here if not using a UI library for these
}

.input-group {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  align-items: stretch;
  width: 100%;

  .form-control {
    position: relative;
    flex: 1 1 auto;
    width: 1%;
    min-width: 0; // PreventC flexing beyond constraints
  }

  // For icons or text within input groups
  .input-group-text {
    display: flex;
    align-items: center;
    padding: $space-sm ($space-sm + $space-xs);
    margin-bottom: 0;
    font-size: $font-size-base;
    font-weight: $font-weight-normal;
    line-height: 1.5;
    color: $primary-black;
    text-align: center;
    white-space: nowrap;
    background-color: $background-light;
    border: $border-width solid $light-gray-border;
    border-radius: $border-radius-sm;
  }

  // Adjust border radius for elements in group
  > .form-control:not(:last-child) { border-top-right-radius: 0; border-bottom-right-radius: 0; }
  > .input-group-text:not(:first-child) { border-top-left-radius: 0; border-bottom-left-radius: 0; }
}

.form-error-message {
  display: block;
  color: $error-color;
  font-size: $font-size-sm;
  margin-top: $space-xs / 2;
}
```

**`src/assets/styles/_cards.scss`:**
```scss
.card {
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: $primary-white;
  background-clip: border-box;
  border: $border-width solid $light-gray-border;
  border-radius: $border-radius-lg; // Softer, larger radius for modern feel
  box-shadow: $box-shadow-sm;
  transition: $transition-base;
  overflow: hidden; // Ensure content respects border-radius

  &:hover {
    box-shadow: $box-shadow;
    transform: translateY(-2px); // Subtle lift effect
  }
}

.card-img-top {
  width: 100%;
  border-top-left-radius: $border-radius-lg;
  border-top-right-radius: $border-radius-lg;
  object-fit: cover; // Ensures image covers area without distortion
  aspect-ratio: 4/3; // Maintain aspect ratio for product images
}

.card-body {
  flex: 1 1 auto;
  padding: $space-md;
}

.card-title {
  margin-bottom: $space-xs;
  font-family: $font-family-sans-serif; // Product titles might look better with sans-serif
  font-size: $font-size-lg;
  font-weight: $font-weight-bold;
}

.card-text {
  margin-bottom: $space-sm;
  color: $secondary-gray;
  font-size: $font-size-sm;
}

.card-subtitle {
  margin-top: -$space-xs / 2;
  margin-bottom: $space-sm;
  color: $primary-black;
  font-weight: $font-weight-bold;
  font-size: $font-size-base;
}

.card-footer {
  padding: $space-sm $space-md;
  background-color: transparent; // Keep it clean
  border-top: $border-width solid $light-gray-border;
  &:last-child {
    border-radius: 0 0 $border-radius-lg $border-radius-lg;
  }
}
```

**`src/assets/styles/_utilities.scss`:**
```scss
// Margins
@for $i from 0 through 8 {
  .m-#{$i} { margin: #{$i * $spacing-unit} !important; }
  .mt-#{$i} { margin-top: #{$i * $spacing-unit} !important; }
  .mb-#{$i} { margin-bottom: #{$i * $spacing-unit} !important; }
  .ms-#{$i} { margin-left: #{$i * $spacing-unit} !important; } // Use 's' for start (LTR/RTL)
  .me-#{$i} { margin-right: #{$i * $spacing-unit} !important; } // Use 'e' for end
  .mx-#{$i} { margin-left: #{$i * $spacing-unit} !important; margin-right: #{$i * $spacing-unit} !important; }
  .my-#{$i} { margin-top: #{$i * $spacing-unit} !important; margin-bottom: #{$i * $spacing-unit} !important; }
}
.m-auto { margin: auto !important; }
// ... similar for paddings (p-*, pt-*, etc.)

.container {
  width: 100%;
  padding-right: $space-md;
  padding-left: $space-md;
  margin-right: auto;
  margin-left: auto;

  @media (min-width: $breakpoint-sm) { max-width: 540px; }
  @media (min-width: $breakpoint-md) { max-width: 720px; }
  @media (min-width: $breakpoint-lg) { max-width: 960px; }
  @media (min-width: $breakpoint-xl) { max-width: 1140px; }
  @media (min-width: $breakpoint-xxl) { max-width: 1320px; }
}

.d-flex { display: flex !important; }
.justify-content-center { justify-content: center !important; }
.align-items-center { align-items: center !important; }
// Add more flex utilities as needed

.w-100 { width: 100% !important; }
.h-100 { height: 100% !important; }

// Responsive display
.d-none { display: none !important; }
@media (min-width: $breakpoint-md) {
  .d-md-block { display: block !important; }
  .d-md-none { display: none !important; }
  // etc.
}
```

**`src/assets/styles/_animations.scss`:**
```scss
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.slide-in-up {
  animation: slideInUp 0.5s ease-out;
}
```

**`src/styles.scss` (Main global styles file):**
```scss
@import 'assets/styles/variables';
@import 'assets/styles/base';
@import 'assets/styles/typography';
@import 'assets/styles/buttons';
@import 'assets/styles/forms';
@import 'assets/styles/cards';
@import 'assets/styles/utilities';
@import 'assets/styles/animations';

// Third-party library styles
@import 'ngx-toastr/toastr';

body {
  // To ensure footer sticks to bottom on short pages
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex-grow: 1; // Allows main content to expand and push footer
}

// Custom scrollbar (optional, for a more modern feel)
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: $background-light;
  border-radius: $border-radius-sm;
}

::-webkit-scrollbar-thumb {
  background: $secondary-gray;
  border-radius: $border-radius-sm;
  &:hover {
    background: darken($secondary-gray, 10%);
  }
}
```

---

**5. Core Module & Shared Module**

**`src/app/app.module.ts`:**
```typescript
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { CoreModule } from './core/core.module';
import { SharedModule } from './shared/shared.module';
import { LayoutModule } from './layout/layout.module'; // Import LayoutModule

import { ToastrModule } from 'ngx-toastr';
import { AuthInterceptor } from './core/interceptors/auth.interceptor';
// import { ErrorInterceptor } from './core/interceptors/error.interceptor'; // Implement this for global error handling

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    AppRoutingModule,
    CoreModule,
    SharedModule,
    LayoutModule, // Add LayoutModule here
    ToastrModule.forRoot({
      timeOut: 5000,
      positionClass: 'toast-bottom-right',
      preventDuplicates: true,
      progressBar: true,
      closeButton: true,
      toastClass: 'ngx-toastr app-toast', // Custom class for styling
    }),
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
    // { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
```
*App Toast Custom Styling (add to `styles.scss` or a dedicated toast style file):*
```scss
// styles.scss or assets/styles/_toasts.scss
.app-toast {
  background-color: $accent-rich-black !important;
  color: $primary-white !important;
  border-radius: $border-radius-sm !important;
  box-shadow: $box-shadow-lg !important;
  opacity: 0.95 !important;

  .toast-title {
    font-weight: $font-weight-bold !important;
  }

  .toast-progress {
    background-color: $primary-gold !important;
  }

  button[aria-label="Close"] { // Targeting the close button
    color: $primary-white !important;
    opacity: 0.7 !important;
    &:hover {
      opacity: 1 !important;
    }
  }

  // Specific toast types
  &.toast-success {
    // background-color: $success-color !important; // Or keep consistent black
  }
  &.toast-error {
    // background-color: $error-color !important; // Or keep consistent black
  }
  // etc. for info, warning
}
```

**`src/app/core/core.module.ts`:**
(Services and repositories will be provided here)
```typescript
import { NgModule, Optional, SkipSelf } from '@angular/core';
import { CommonModule } from '@angular/common';

// Repositories
import { AuthRepository } from './repositories/auth.repository';
import { ProductRepository } from './repositories/product.repository';
import { CategoryRepository } from './repositories/category.repository';
import { CartRepository } from './repositories/cart.repository';
import { OrderRepository } from './repositories/order.repository';

// Services
import { AuthService } from './services/auth.service';
import { ProductService } from './services/product.service';
import { CategoryService } from './services/category.service';
import { CartService } from './services/cart.service';
import { OrderService } from './services/order.service';
import { NotificationService } from './services/notification.service';
import { LoadingService } from './services/loading.service';

@NgModule({
  declarations: [],
  imports: [
    CommonModule
  ],
  providers: [
    // Repositories
    AuthRepository,
    ProductRepository,
    CategoryRepository,
    CartRepository,
    OrderRepository,
    // Services
    AuthService,
    ProductService,
    CategoryService,
    CartService,
    OrderService,
    NotificationService,
    LoadingService,
    // Guards (can be provided here or in routing modules)
  ]
})
export class CoreModule {
  constructor(@Optional() @SkipSelf() parentModule: CoreModule) {
    if (parentModule) {
      throw new Error('CoreModule is already loaded. Import it in the AppModule only');
    }
  }
}
```

**`src/app/shared/shared.module.ts`:**
(For components, directives, pipes used across feature modules)
```typescript
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

// Example Shared Components (Create these as needed)
// import { LoadingSpinnerComponent } from './components/loading-spinner/loading-spinner.component';
// import { ModalComponent } from './components/modal/modal.component';
// import { EmptyStateComponent } from './components/empty-state/empty-state.component';

// Angular Material Modules (Optional, if you decide to use some)
// import { MatButtonModule } from '@angular/material/button';
// import { MatIconModule } from '@angular/material/icon';
// import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

const ANGULAR_MODULES = [
  CommonModule,
  FormsModule,
  ReactiveFormsModule,
  RouterModule
];

const THIRD_PARTY_MODULES = [
  // MatButtonModule,
  // MatIconModule,
  // MatProgressSpinnerModule
];

const COMPONENTS = [
  // LoadingSpinnerComponent,
  // ModalComponent,
  // EmptyStateComponent
];

const DIRECTIVES = [];
const PIPES = [];

@NgModule({
  declarations: [
    ...COMPONENTS,
    ...DIRECTIVES,
    ...PIPES
  ],
  imports: [
    ...ANGULAR_MODULES,
    ...THIRD_PARTY_MODULES
  ],
  exports: [
    ...ANGULAR_MODULES,
    ...THIRD_PARTY_MODULES,
    ...COMPONENTS,
    ...DIRECTIVES,
    ...PIPES
  ]
})
export class SharedModule { }
```

---

**6. Layout Components**

**`src/app/layout/layout.module.ts`:**
```typescript
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router'; // Import RouterModule
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { MainLayoutComponent } from './main-layout/main-layout.component';
import { SharedModule } from '../shared/shared.module'; // If shared components are used in layout

@NgModule({
  declarations: [
    HeaderComponent,
    FooterComponent,
    MainLayoutComponent
  ],
  imports: [
    CommonModule,
    RouterModule, // Add RouterModule here
    SharedModule
  ],
  exports: [
    MainLayoutComponent // Export MainLayoutComponent so AppModule can use it
  ]
})
export class LayoutModule { }
```

**`src/app/layout/main-layout/main-layout.component.ts`:**
```typescript
import { Component } from '@angular/core';

@Component({
  selector: 'app-main-layout',
  templateUrl: './main-layout.component.html',
  styleUrls: ['./main-layout.component.scss']
})
export class MainLayoutComponent {}
```

**`src/app/layout/main-layout/main-layout.component.html`:**
```html
<app-header></app-header>
<main class="main-content">
  <router-outlet></router-outlet>
</main>
<app-footer></app-footer>
```

**`src/app/layout/main-layout/main-layout.component.scss`:**
```scss
// styles.scss already handles flex for body and main to push footer
// .main-content {
//   // Add any specific padding/margin for the main content area if needed
//   // e.g., padding-top to account for a fixed header, if you choose that
// }
```

**`src/app/app.component.html`:**
```html
<app-main-layout></app-main-layout>
<!-- Global loading indicator could go here -->
<!-- <app-global-loader *ngIf="loadingService.isLoading$ | async"></app-global-loader> -->
```

**`src/app/layout/header/header.component.ts`:**
```typescript
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { AuthService } from '../../core/services/auth.service';
import { CartService } from '../../core/services/cart.service'; // Assuming you have a cart service
import { User } from '../../core/models/user.model'; // Your user model

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit, OnDestroy {
  isLoggedIn = false;
  currentUser: User | null = null;
  cartItemCount = 0;
  searchQuery = '';
  isMobileMenuOpen = false;

  private authSubscription!: Subscription;
  private cartSubscription!: Subscription;

  constructor(
    private authService: AuthService,
    private cartService: CartService, // Inject CartService
    private router: Router
  ) {}

  ngOnInit(): void {
    this.authSubscription = this.authService.currentUser.subscribe(user => {
      this.isLoggedIn = !!user;
      this.currentUser = user;
    });

    // Subscribe to cart item count (you'll need to implement this in CartService)
    this.cartSubscription = this.cartService.getCartItemCount().subscribe(count => {
      this.cartItemCount = count;
    });
  }

  onSearch(): void {
    if (this.searchQuery.trim()) {
      this.router.navigate(['/products'], { queryParams: { search: this.searchQuery.trim() } });
      this.searchQuery = ''; // Clear search after navigating
    }
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/auth/login']);
  }

  toggleMobileMenu(): void {
    this.isMobileMenuOpen = !this.isMobileMenuOpen;
  }

  closeMobileMenu(): void {
    this.isMobileMenuOpen = false;
  }


  ngOnDestroy(): void {
    if (this.authSubscription) {
      this.authSubscription.unsubscribe();
    }
    if (this.cartSubscription) {
      this.cartSubscription.unsubscribe();
    }
  }
}
```

**`src/app/layout/header/header.component.html`:**
```html
<header class="app-header">
  <div class="container header-container">
    <a routerLink="/" class="logo" (click)="closeMobileMenu()">
      <!-- Replace with your SVG logo -->
      <img src="assets/icons/logo.svg" alt="LuxeCart Logo" class="logo-img">
      <span class="logo-text">LuxeCart</span>
    </a>

    <nav class="navigation" [class.mobile-menu-open]="isMobileMenuOpen">
      <ul class="nav-links">
        <li><a routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{exact: true}" (click)="closeMobileMenu()">Home</a></li>
        <li><a routerLink="/products" routerLinkActive="active" (click)="closeMobileMenu()">Products</a></li>
        <!-- Add more links as needed e.g. Categories, About Us -->
      </ul>
    </nav>

    <div class="header-actions">
      <form (ngSubmit)="onSearch()" class="search-form">
        <input type="search" [(ngModel)]="searchQuery" name="searchQuery" placeholder="Search products..." class="search-input">
        <button type="submit" class="btn-icon search-button" aria-label="Search">
          <!-- Replace with SVG search icon -->
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        </button>
      </form>

      <a routerLink="/cart" class="btn-icon cart-icon-link" aria-label="View Cart" (click)="closeMobileMenu()">
        <!-- Replace with SVG cart icon -->
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>
        <span *ngIf="cartItemCount > 0" class="cart-badge">{{ cartItemCount }}</span>
      </a>

      <div class="auth-actions">
        <ng-container *ngIf="!isLoggedIn; else loggedInActions">
          <a routerLink="/auth/login" class="btn btn-outline-dark btn-sm" (click)="closeMobileMenu()">Login</a>
          <a routerLink="/auth/register" class="btn btn-primary btn-sm" (click)="closeMobileMenu()">Register</a>
        </ng-container>
        <ng-template #loggedInActions>
          <a routerLink="/profile" class="btn-icon user-profile-link" aria-label="User Profile" (click)="closeMobileMenu()">
             <!-- Replace with SVG user icon -->
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
          </a>
          <button (click)="logout()" class="btn btn-link btn-sm">Logout</button>
        </ng-template>
      </div>
    </div>

    <button class="mobile-menu-toggle btn-icon" (click)="toggleMobileMenu()" aria-label="Toggle Menu">
      <!-- Hamburger Icon -->
      <svg *ngIf="!isMobileMenuOpen" xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
      <!-- Close Icon -->
      <svg *ngIf="isMobileMenuOpen" xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
    </button>
  </div>
</header>
```

**`src/app/layout/header/header.component.scss`:**
```scss
@import 'assets/styles/variables';

.app-header {
  background-color: $primary-white;
  padding: $space-sm 0;
  border-bottom: $border-width solid $light-gray-border;
  position: sticky; // Makes header sticky
  top: 0;
  z-index: 1000; // Ensures it's above other content
  box-shadow: $box-shadow-sm;
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: $primary-black;

  .logo-img {
    height: 32px; // Adjust as needed
    margin-right: $space-xs;
  }

  .logo-text {
    font-size: $font-size-lg;
    font-weight: $font-weight-bold;
    font-family: $font-family-serif; // Example: Serif for logo text
    color: $accent-rich-black;
  }
   &:hover {
    text-decoration: none;
   }
}

.navigation {
  .nav-links {
    display: flex;
    align-items: center;
    list-style: none;
    margin: 0;
    padding: 0;

    li {
      margin-left: $space-md;

      a {
        text-decoration: none;
        color: $primary-black;
        font-weight: $font-weight-normal; // Use normal weight for nav links for minimalism
        padding: $space-xs $space-sm;
        border-radius: $border-radius-sm;
        transition: $transition-base;

        &:hover, &.active {
          color: $primary-gold;
          // background-color: lighten($primary-gold, 35%); // Subtle hover
        }
        &.active {
          font-weight: $font-weight-bold;
        }
      }
    }
  }
}

.header-actions {
  display: flex;
  align-items: center;
}

.search-form {
  display: flex;
  align-items: center;
  margin-right: $space-sm; // Space before cart icon

  .search-input {
    padding: ($space-xs + 2px) $space-sm; // Slightly less padding than default form-control
    border: $border-width solid $light-gray-border;
    border-right: none;
    border-top-left-radius: $border-radius-sm;
    border-bottom-left-radius: $border-radius-sm;
    font-size: $font-size-sm;
    min-width: 150px; // Minimum width for search input
    transition: $transition-base;

    &:focus {
      outline: none;
      border-color: $primary-gold;
      box-shadow: none; // Remove default focus shadow from form-control
      min-width: 200px; // Expand on focus
    }
  }

  .search-button {
    padding: ($space-xs + 2px);
    background-color: $primary-white;
    border: $border-width solid $light-gray-border;
    border-top-right-radius: $border-radius-sm;
    border-bottom-right-radius: $border-radius-sm;
    color: $secondary-gray; // Icon color

    &:hover {
      background-color: $background-light;
      color: $primary-black;
    }
    svg {
      width: 18px; height: 18px; // Smaller icon for search button
    }
  }
}

.cart-icon-link {
  position: relative;
  color: $primary-black;
  margin-right: $space-md;
  padding: $space-xs;

  &:hover {
    color: $primary-gold;
  }

  svg {
    width: 24px; height: 24px;
  }

  .cart-badge {
    position: absolute;
    top: -2px;
    right: -5px;
    background-color: $primary-gold;
    color: $primary-black;
    border-radius: 50%;
    padding: 2px 6px;
    font-size: 10px;
    font-weight: $font-weight-bold;
    line-height: 1;
  }
}

.auth-actions {
  display: flex;
  align-items: center;

  .btn, .btn-link {
    margin-left: $space-xs;
    font-size: $font-size-sm; // Smaller buttons in header
    padding: $space-xs $space-sm;
  }
  .btn-primary {
    background-color: $primary-gold;
    color: $primary-black;
    &:hover {
        background-color: darken($primary-gold, 8%);
    }
  }
  .user-profile-link {
    color: $primary-black;
    &:hover {
        color: $primary-gold;
    }
    svg {
        width: 26px; height: 26px;
    }
  }
}

.mobile-menu-toggle {
  display: none; // Hidden by default, shown on mobile
  background: none;
  border: none;
  color: $primary-black;
  padding: $space-xs;
  z-index: 1001; // Above mobile menu
}

// Responsive adjustments
@media (max-width: $breakpoint-lg) { // Adjust breakpoint as needed
  .search-form .search-input {
    min-width: 120px;
    &:focus { min-width: 150px; }
  }
}


@media (max-width: $breakpoint-md) { // Tablet and mobile
  .navigation {
    position: fixed;
    top: 0;
    left: -100%; // Off-screen initially
    width: 70%;
    max-width: 300px;
    height: 100vh;
    background-color: $accent-rich-black;
    flex-direction: column;
    align-items: flex-start;
    padding: $space-xxl $space-md $space-md;
    transition: left 0.3s ease-in-out;
    box-shadow: $box-shadow-lg;
    z-index: 999; // Below header elements like toggle

    &.mobile-menu-open {
      left: 0;
    }

    .nav-links {
      flex-direction: column;
      width: 100%;

      li {
        margin-left: 0;
        width: 100%;

        a {
          display: block;
          padding: $space-sm 0;
          color: $primary-white;
          font-size: $font-size-lg;

          &:hover, &.active {
            color: $primary-gold;
            background-color: transparent;
          }
        }
      }
    }
  }

  .search-form {
    // Optionally hide search form in mobile header or make it an icon toggle
    // For this example, let's keep it but it might get crowded
    margin-right: $space-xs;
    .search-input {
        display: none; // Simpler: hide input, search button becomes main trigger
    }
    .search-button { // Style search button if input is hidden
        border-radius: $border-radius-sm;
        border-left: $border-width solid $light-gray-border;
    }
  }
   // Or, to make search an icon that expands:
  // .search-form {
  //   // ... styles to make it an icon that expands an input overlay ...
  // }


  .header-actions {
    .auth-actions {
      // Login/Register buttons might be moved into the mobile menu
      // For simplicity, let's keep them, but they might wrap
      // or be visually adjusted.
      .btn {
        padding: $space-xs; // Smaller padding
        font-size: 11px; // Even smaller
      }
      .user-profile-link {
        margin-left: $space-xs;
      }
    }
  }


  .mobile-menu-toggle {
    display: block;
  }
}

@media (max-width: $breakpoint-sm) { // Small mobile
    .logo {
        .logo-text {
            display: none; // Hide text, only show image on very small screens
        }
    }
    .auth-actions {
        .btn-outline-dark { display: none; } // Hide one button if too crowded
    }
    .cart-icon-link {
        margin-right: $space-sm;
    }
}
```
*Recommendation:* For the search on mobile, it's often better to have an icon that, when clicked, expands a search bar overlay or navigates to a dedicated search page. The current example simplifies this.

**`src/app/layout/footer/footer.component.ts`:**
```typescript
import { Component } from '@angular/core';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss']
})
export class FooterComponent {
  currentYear = new Date().getFullYear();
}
```

**`src/app/layout/footer/footer.component.html`:**
```html
<footer class="app-footer">
  <div class="container footer-content">
    <div class="footer-section">
      <h5 class="footer-title">LuxeCart</h5>
      <p class="text-secondary">Elegance in every click. Discover curated collections and timeless pieces.</p>
    </div>
    <div class="footer-section">
      <h5 class="footer-title">Quick Links</h5>
      <ul class="footer-links">
        <li><a routerLink="/about">About Us</a></li>
        <li><a routerLink="/contact">Contact</a></li>
        <li><a routerLink="/faq">FAQ</a></li>
        <li><a routerLink="/terms">Terms of Service</a></li>
      </ul>
    </div>
    <div class="footer-section">
      <h5 class="footer-title">Connect</h5>
      <ul class="footer-social-links">
        <li><a href="#" aria-label="Facebook">FB</a></li> <!-- Replace with actual icons -->
        <li><a href="#" aria-label="Instagram">IG</a></li>
        <li><a href="#" aria-label="Twitter">TW</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p class="text-secondary">&copy; {{ currentYear }} LuxeCart. All Rights Reserved. Designed with <span class="text-gold">&hearts;</span>.</p>
  </div>
</footer>
```

**`src/app/layout/footer/footer.component.scss`:**
```scss
@import 'assets/styles/variables';

.app-footer {
  background-color: $accent-rich-black;
  color: $secondary-gray;
  padding: $space-xl 0 0;
  margin-top: $space-xxl; // Ensure space above footer
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: $space-lg;
  padding-bottom: $space-xl;
}

.footer-section {
  .footer-title {
    color: $primary-white;
    font-size: $font-size-lg;
    margin-bottom: $space-md;
    font-family: $font-family-sans-serif; // Sans-serif for footer titles
  }

  p {
    color: $secondary-gray;
    font-size: $font-size-sm;
  }
}

.footer-links, .footer-social-links {
  list-style: none;
  padding-left: 0;

  li {
    margin-bottom: $space-xs;

    a {
      color: $secondary-gray;
      text-decoration: none;
      font-size: $font-size-sm;

      &:hover {
        color: $primary-gold;
        text-decoration: underline;
      }
    }
  }
}

.footer-social-links {
  display: flex;
  li {
    margin-right: $space-sm;
    // Add styles for social icons here
  }
}

.footer-bottom {
  text-align: center;
  padding: $space-md 0;
  border-top: 1px solid darken($accent-rich-black, -10%); // Slightly lighter border than bg
  font-size: $font-size-sm;

  p {
    margin-bottom: 0;
  }
}
```

---

**7. API Models (DTOs)**

Create these interface files in `src/app/core/models/`. These are based on your OpenAPI `components.schemas`.

**`src/app/core/models/api-response.model.ts` (Generic wrapper if your API uses one consistently)**
```typescript
export interface ApiError {
  statusCode: number;
  errorMessage: string | null;
}

export interface ApiResult<T> {
  isCompleteSuccessfully: boolean;
  data: T | null; // Make data nullable for safety
  errorMessages: ApiError | null; // Assuming single error object, adjust if it's an array
}
```

**`src/app/core/models/auth.dto.ts`:**
```typescript
import { ApiError, ApiResult } from './api-response.model';

export interface RegisterDto {
  displayName: string;
  email: string;
  password: string;
  confirmPassword: string;
}

export interface LoginDto {
  email: string;
  password: string;
}

export interface AccountDto {
  displayName: string | null;
  isAuthenticated: boolean;
  email: string | null;
  token: string | null;
  // Add userId if it's part of the account DTO and needed client-side
  // userId?: string;
}

export type AccountDtoResult = ApiResult<AccountDto>;

// For User Info (assuming it returns something like AccountDto or a subset)
// You might need a specific DTO if /user-info returns different data
export interface UserInfoDto {
  displayName: string;
  email: string;
  // ... other fields from /user-info
}
```

**`src/app/core/models/product.model.ts`:**
```typescript
// Based on your API's product structure (assuming from Product PUT/POST)
// The GET /api/Products response structure needs to be confirmed from actual API calls
// or more detailed OpenAPI spec. For now, let's assume:
export interface Product {
  productId: number;
  name: string;
  price: number;
  description?: string;
  imageUrl?: string; // Assuming API converts ImageFile to a URL
  categoryId: number;
  categoryName?: string; // If API returns this
  // Add other fields like stock, ratings, etc.
}

// For Product creation/update if it's different from the display model
export interface ProductRequestDto {
  productId?: number; // Optional for creation
  name: string;
  price: number;
  description?: string;
  imageFile?: File; // For sending multipart/form-data
  categoryId: number;
}

// Response for GET /api/Products (assuming pagination)
export interface PaginatedProducts {
  items: Product[];
  pageNumber: number;
  totalPages: number;
  totalCount: number;
  hasPreviousPage: boolean;
  hasNextPage: boolean;
}
```

**`src/app/core/models/category.model.ts`:**
```typescript
export interface Category {
  categoryId: number;
  categoryName: string;
  image?: string | null; // URL of the image
  // Add productCount or other relevant fields if API provides them
}

export interface CategoryRequestDto {
  categoryId?: number;
  categoryName: string;
  imageFile?: File | null;
}
```

**`src/app/core/models/cart.model.ts`:**
```typescript
// Response from GET /api/Cart/{userId} - Define this based on actual API response
export interface CartItem {
  productId: number;
  productName: string; // You'll likely need to fetch/join product details
  quantity: number;
  price: number; // Price per unit
  imageUrl?: string;
  // any other product details you want to show in cart
}

export interface Cart {
  userId: string;
  items: CartItem[];
  totalPrice?: number; // Calculated client-side or from backend
  // other cart-level details like discount, shipping
}


export interface CartRequestDto {
  userId: string; // This might be handled by AuthInterceptor or taken from logged-in user
  productId: number;
  quantity: number;
}
```
*Self-correction:* The `CartRequestDto` in your OpenAPI has `userId` as nullable string. If it's always the current user, the backend might infer it from the auth token. Clarify this. For now, I'll assume `userId` is needed or can be derived.

**`src/app/core/models/order.model.ts`:**
```typescript
// For POST /api/Orders/payment-intent response
export interface PaymentIntentResponse {
  clientSecret: string;
  orderId: string; // Or whatever identifier your API returns
  // ... other relevant details
}

// From TransactionDto for webhook
export interface OrderTransactionDto {
    // Define based on TransactionDto, ObjDto, OrderDto, MerchantDto from your OpenAPI spec
    type: string | null;
    obj: {
        id: number; // transaction id
        pending: boolean;
        amount_cents: number;
        success: boolean;
        // ... include all relevant fields from ObjDto
        order: { // from OrderDto
            id: number; // order id
            created_at: string; // date-time
            delivery_needed: boolean;
            // ... other order fields
        };
        // ... merchant details if needed
    };
}

// User's order history item
export interface OrderHistoryItem {
    orderId: string;
    orderDate: string;
    totalAmount: number;
    status: string; // e.g., 'Processing', 'Shipped', 'Delivered'
    items: CartItem[]; // Simplified, or just a summary
}
```

---

**8. Repositories**

**`src/app/core/repositories/auth.repository.ts`:**
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { LoginDto, RegisterDto, AccountDtoResult, UserInfoDto } from '../models/auth.dto';

@Injectable()
export class AuthRepository {
  private baseUrl = environment.apiBaseUrl;

  constructor(private http: HttpClient) {}

  register(data: RegisterDto): Observable<AccountDtoResult> {
    return this.http.post<AccountDtoResult>(`${this.baseUrl}register`, data);
  }

  login(data: LoginDto): Observable<AccountDtoResult> {
    return this.http.post<AccountDtoResult>(`${this.baseUrl}login`, data);
  }

  // Note: /google-login is a GET. This usually initiates a redirect flow.
  // The actual login happens via /google-login-callback.
  // Handling this flow client-side requires more setup (e.g., opening a new window).
  // For simplicity, this might just be a window.location.href change.
  initiateGoogleLogin(): void {
    // This would typically redirect the user. The backend handles the rest.
    // The callback will then provide a token or session.
    window.location.href = `${this.baseUrl}google-login`;
  }

  // This endpoint is likely called by your backend after Google auth.
  // The client might not call /google-login-callback directly.
  // If the client DOES need to call it (e.g., with a code from Google), adjust accordingly.

  getUserInfo(): Observable<UserInfoDto> { // Adjust UserInfoDto based on actual API response
    // This endpoint needs authentication (token in header)
    return this.http.get<UserInfoDto>(`${this.baseUrl}user-info`);
  }
}
```

**`src/app/core/repositories/product.repository.ts`:**
```typescript
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Product, ProductRequestDto, PaginatedProducts } from '../models/product.model';

@Injectable()
export class ProductRepository {
  private baseUrl = `${environment.apiBaseUrl}api/Products`;

  constructor(private http: HttpClient) {}

  getProducts(
    pageNumber = 1,
    numberOfProducts = 10,
    categoryName?: string,
    searchQuery?: string
  ): Observable<PaginatedProducts> { // Assuming API returns PaginatedProducts
    let params = new HttpParams()
      .set('pageNumber', pageNumber.toString())
      .set('numberOfProduct', numberOfProducts.toString());

    if (categoryName) {
      params = params.set('categoryName', categoryName);
    }
    if (searchQuery) {
      params = params.set('searchQuery', searchQuery);
    }
    // The API doc implies the response is just an array of products.
    // If it's not paginated directly in the response body (e.g. headers for pagination info),
    // this will need adjustment. For now, assuming PaginatedProducts is the response structure.
    // If it's just Product[], change the return type.
    return this.http.get<PaginatedProducts>(this.baseUrl, { params });
  }

  getProductById(id: number): Observable<Product> {
    return this.http.get<Product>(`${this.baseUrl}/${id}`);
  }

  // For Admin (Optional)
  createProduct(productData: ProductRequestDto): Observable<Product> { // Assuming returns created product
    const formData = this.toFormData(productData);
    return this.http.post<Product>(this.baseUrl, formData);
  }

  updateProduct(id: number, productData: ProductRequestDto): Observable<any> { // API returns "Success" (200 OK)
    const formData = this.toFormData(productData);
    formData.set('ProductId', id.toString()); // Ensure ProductId is part of form for PUT
    return this.http.put(`${this.baseUrl}/${id}`, formData);
  }

  deleteProduct(id: number): Observable<any> { // API returns "Success" (200 OK)
    return this.http.delete(`${this.baseUrl}/${id}`);
  }

  private toFormData(data: ProductRequestDto): FormData {
    const formData = new FormData();
    formData.append('Name', data.name);
    formData.append('Price', data.price.toString());
    formData.append('CategoryId', data.categoryId.toString());
    if (data.description) {
      formData.append('Description', data.description);
    }
    if (data.imageFile) {
      formData.append('ImageFile', data.imageFile, data.imageFile.name);
    }
    // ProductId is part of path for PUT, not needed in body unless API requires it there too.
    // For POST, ProductId is usually generated by backend. Your API has ProductId in POST request body.
    if (data.productId) { // This is unusual for a POST, but your API spec requires it
        formData.append('ProductId', data.productId.toString());
    }
    return formData;
  }
}
```
*API Note on Products:* Your API spec for `POST /api/Products` requires `ProductId` in the `multipart/form-data`. This is unusual for a creation endpoint, as `ProductId` is typically generated by the server. Double-check if this is intended or if it should be omitted for POST. For `PUT /api/Products/{id}`, `ProductId` is also in the form data.

**`src/app/core/repositories/category.repository.ts`:**
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Category, CategoryRequestDto } from '../models/category.model';

@Injectable()
export class CategoryRepository {
  private baseUrl = `${environment.apiBaseUrl}api/Categories`;

  constructor(private http: HttpClient) {}

  getCategories(): Observable<Category[]> { // Assuming it returns an array of categories
    return this.http.get<Category[]>(this.baseUrl);
  }

  getCategoryById(id: number): Observable<Category> {
    return this.http.get<Category>(`${this.baseUrl}/${id}`);
  }

  // For Admin (Optional)
  createCategory(categoryData: CategoryRequestDto): Observable<Category> {
    const formData = this.toFormData(categoryData);
    return this.http.post<Category>(this.baseUrl, formData);
  }

  updateCategory(id: number, categoryData: CategoryRequestDto): Observable<any> {
    const formData = this.toFormData(categoryData);
    // categoryData.categoryId is part of the DTO for PUT.
    // If id path param is the source of truth, ensure it's used.
    // Your API takes CategoryId in the body for PUT implicitly.
    return this.http.put(`${this.baseUrl}/${id}`, formData);
  }

  deleteCategory(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/${id}`);
  }

  private toFormData(data: CategoryRequestDto): FormData {
    const formData = new FormData();
    formData.append('CategoryName', data.categoryName);
    if (data.categoryId) { // For update, include categoryId if API needs it in body
        formData.append('CategoryId', data.categoryId.toString());
    }
    if (data.imageFile) {
      formData.append('ImageFile', data.imageFile, data.imageFile.name);
    }
    return formData;
  }
}
```

**`src/app/core/repositories/cart.repository.ts`:**
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Cart, CartRequestDto } from '../models/cart.model'; // Define Cart based on actual API response

@Injectable()
export class CartRepository {
  private baseUrl = `${environment.apiBaseUrl}api/Cart`;

  constructor(private http: HttpClient) {}

  getCart(userId: string): Observable<Cart> { // Define Cart model for response
    return this.http.get<Cart>(`${this.baseUrl}/${userId}`);
  }

  addItemToCart(item: CartRequestDto): Observable<any> { // API returns "Success"
    return this.http.post(this.baseUrl, item);
  }

  updateCartItem(item: CartRequestDto): Observable<any> { // API returns "Success"
    return this.http.put(this.baseUrl, item);
  }

  removeItemFromCart(userId: string, productId: number): Observable<any> { // API returns "Success"
    return this.http.delete(`${this.baseUrl}/${userId}/${productId}`);
  }
}
```

**`src/app/core/repositories/order.repository.ts`:**
```typescript
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { PaymentIntentResponse, OrderHistoryItem } from '../models/order.model'; // Define these

@Injectable()
export class OrderRepository {
  private baseUrl = `${environment.apiBaseUrl}api/Orders`;

  constructor(private http: HttpClient) {}

  createPaymentIntent(userId: string): Observable<PaymentIntentResponse> {
    const params = new HttpParams().set('userId', userId);
    return this.http.post<PaymentIntentResponse>(`${this.baseUrl}/payment-intent`, null, { params });
    // Note: API spec shows `userId` as query param, and no request body.
  }

  // Optional: Get order history (if you implement /user-info or a dedicated orders endpoint)
  getOrderHistory(userId: string): Observable<OrderHistoryItem[]> {
    // This endpoint is not in your provided spec, example:
    // return this.http.get<OrderHistoryItem[]>(`${this.baseUrl}/history/${userId}`);
    // For now, return empty or throw error if not implemented.
    throw new Error('Order history endpoint not defined in API specification.');
  }

  // The /api/Orders/webhook is typically called by Stripe, not by the frontend.
}
```

---

**9. Services (Business Logic)**

**`src/app/core/services/auth.service.ts`:**
```typescript
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { tap, catchError, map } from 'rxjs/operators';
import { AuthRepository } from '../repositories/auth.repository';
import { LoginDto, RegisterDto, AccountDto, UserInfoDto } from '../models/auth.dto';
import { User } from '../models/user.model'; // Create this simple model
import { NotificationService } from './notification.service';

// src/app/core/models/user.model.ts
// export interface User {
//   id: string; // Or use email as ID if that's unique and primary
//   displayName: string | null;
//   email: string | null;
//   token?: string; // Token should ideally not be part of the User model exposed to components
// }

@Injectable()
export class AuthService {
  private currentUserSubject: BehaviorSubject<User | null>;
  public currentUser: Observable<User | null>;
  private readonly TOKEN_KEY = 'authToken';
  private readonly USER_INFO_KEY = 'currentUserInfo';

  constructor(
    private authRepository: AuthRepository,
    private router: Router,
    private notificationService: NotificationService
  ) {
    const storedUser = localStorage.getItem(this.USER_INFO_KEY);
    this.currentUserSubject = new BehaviorSubject<User | null>(storedUser ? JSON.parse(storedUser) : null);
    this.currentUser = this.currentUserSubject.asObservable();
  }

  public get currentUserValue(): User | null {
    return this.currentUserSubject.value;
  }

  public get isLoggedIn(): boolean {
    return !!localStorage.getItem(this.TOKEN_KEY);
  }

  public getAuthToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  register(data: RegisterDto): Observable<boolean> {
    return this.authRepository.register(data).pipe(
      map(response => {
        if (response.isCompleteSuccessfully && response.data) {
          this.handleAuthentication(response.data);
          this.notificationService.success('Registration successful!', 'Welcome');
          return true;
        } else {
          const errorMsg = response.errorMessages?.errorMessage || 'Registration failed. Please try again.';
          this.notificationService.error(errorMsg, 'Registration Error');
          return false;
        }
      }),
      catchError(err => {
        this.notificationService.error('An unexpected error occurred during registration.', 'Error');
        console.error('Registration error:', err);
        return of(false);
      })
    );
  }

  login(data: LoginDto): Observable<boolean> {
    return this.authRepository.login(data).pipe(
      map(response => {
        if (response.isCompleteSuccessfully && response.data) {
          this.handleAuthentication(response.data);
          this.notificationService.success('Login successful!', 'Welcome Back');
          return true;
        } else {
          const errorMsg = response.errorMessages?.errorMessage || 'Invalid email or password.';
          this.notificationService.error(errorMsg, 'Login Error');
          return false;
        }
      }),
      catchError(err => {
        this.notificationService.error('An unexpected error occurred during login.', 'Error');
        console.error('Login error:', err);
        return of(false);
      })
    );
  }

  private handleAuthentication(accountDto: AccountDto): void {
    if (accountDto.token && accountDto.email) { // Assuming email can serve as a user identifier part
      localStorage.setItem(this.TOKEN_KEY, accountDto.token);
      const user: User = {
        // id: accountDto.email, // Or a proper userId if API provides it in AccountDto
        id: 'temp-user-id', // Replace with actual user ID from API if available
        displayName: accountDto.displayName,
        email: accountDto.email,
      };
      localStorage.setItem(this.USER_INFO_KEY, JSON.stringify(user));
      this.currentUserSubject.next(user);
    } else {
        // This case should ideally not happen if isCompleteSuccessfully is true
        console.error("Authentication data incomplete:", accountDto);
        this.notificationService.error("Authentication failed: Incomplete user data received.", "Auth Error");
    }
  }

  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.USER_INFO_KEY);
    this.currentUserSubject.next(null);
    this.notificationService.info('You have been logged out.', 'Goodbye');
    this.router.navigate(['/auth/login']);
  }

  // Fetch full user profile if needed separately
  fetchAndUpdateUserInfo(): Observable<User | null> {
    return this.authRepository.getUserInfo().pipe(
      tap((userInfo: UserInfoDto) => { // Adjust UserInfoDto if necessary
        const currentUser = this.currentUserValue;
        if (currentUser) {
          const updatedUser: User = {
            ...currentUser, // Keep existing ID and token if not in UserInfoDto
            displayName: userInfo.displayName,
            email: userInfo.email, // Update email if it can change, or verify it matches
          };
          localStorage.setItem(this.USER_INFO_KEY, JSON.stringify(updatedUser));
          this.currentUserSubject.next(updatedUser);
        }
      }),
      map(() => this.currentUserValue), // Return the updated user from BehaviorSubject
      catchError(err => {
        this.notificationService.error('Could not fetch user information.', 'Profile Error');
        // Potentially log out user if token is invalid (e.g., 401 error)
        // This should be handled by an ErrorInterceptor globally.
        return of(null);
      })
    );
  }

  initiateGoogleLogin(): void {
    this.authRepository.initiateGoogleLogin();
    // After redirect and callback, your backend should provide a token.
    // You'll need a mechanism to capture this token on the frontend,
    // e.g., a dedicated callback route in Angular that receives the token as a query param.
    // Example: /auth/google-callback?token=YOUR_TOKEN
    // Then, call a method like `handleGoogleCallbackToken(token)`.
  }

  // Call this method from your Google callback component
  handleAuthResponse(accountDto: AccountDto): void {
    if (accountDto.token && accountDto.email) {
      this.handleAuthentication(accountDto);
      this.router.navigate(['/']); // Navigate to home or profile
      this.notificationService.success('Logged in successfully with Google!', 'Welcome');
    } else {
      this.notificationService.error('Google login failed. Please try again.', 'Login Error');
      this.router.navigate(['/auth/login']);
    }
  }
}
```
*User Model `src/app/core/models/user.model.ts`*:
```typescript
export interface User {
  id: string; // This should ideally be a unique ID from your backend (e.g., GUID)
  displayName: string | null;
  email: string | null;
  // roles?: string[]; // For role-based access (admin)
}
```

**`src/app/core/services/notification.service.ts`:**
```typescript
import { Injectable } from '@angular/core';
import { ToastrService } from 'ngx-toastr';

@Injectable()
export class NotificationService {
  constructor(private toastr: ToastrService) {}

  success(message: string, title?: string): void {
    this.toastr.success(message, title);
  }

  error(message: string, title?: string): void {
    this.toastr.error(message, title);
  }

  info(message: string, title?: string): void {
    this.toastr.info(message, title);
  }

  warning(message: string, title?: string): void {
    this.toastr.warning(message, title);
  }
}
```

**`src/app/core/services/loading.service.ts`:**
```typescript
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable()
export class LoadingService {
  private loadingSubject = new BehaviorSubject<boolean>(false);
  isLoading$: Observable<boolean> = this.loadingSubject.asObservable();

  show(): void {
    this.loadingSubject.next(true);
  }

  hide(): void {
    this.loadingSubject.next(false);
  }
}
```
*You would typically integrate this with an HTTP interceptor to automatically show/hide on API calls, or manually call `show()`/`hide()` around service method calls.*

**`src/app/core/services/product.service.ts`:**
```typescript
import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject, throwError, of } from 'rxjs';
import { catchError, tap, map, finalize } from 'rxjs/operators';
import { ProductRepository } from '../repositories/product.repository';
import { Product, PaginatedProducts, ProductRequestDto } from '../models/product.model';
import { NotificationService } from './notification.service';
import { LoadingService } from './loading.service';

@Injectable()
export class ProductService {
  // Example: If you want to cache products or manage a local state
  private productsSubject = new BehaviorSubject<Product[]>([]);
  public products$ = this.productsSubject.asObservable();

  private currentProductSubject = new BehaviorSubject<Product | null>(null);
  public currentProduct$ = this.currentProductSubject.asObservable();


  constructor(
    private productRepository: ProductRepository,
    private notificationService: NotificationService,
    private loadingService: LoadingService
  ) {}

  getProducts(
    pageNumber = 1,
    numberOfProducts = 10,
    categoryName?: string,
    searchQuery?: string
  ): Observable<PaginatedProducts> { // Or Product[] if not paginated
    this.loadingService.show();
    return this.productRepository.getProducts(pageNumber, numberOfProducts, categoryName, searchQuery).pipe(
      tap((paginatedResult) => {
        // this.productsSubject.next(paginatedResult.items); // If you want to store the current page locally
        // Handle cases where API might return null or undefined for items
        if (!paginatedResult || !paginatedResult.items) {
            this.notificationService.warning('No products found matching your criteria.', 'Products');
            // Return an empty valid structure to prevent downstream errors
            return { items: [], pageNumber: 1, totalPages: 0, totalCount: 0, hasPreviousPage: false, hasNextPage: false };
        }
        return paginatedResult;
      }),
      catchError(err => {
        this.notificationService.error('Failed to fetch products.', 'Error');
        console.error(err);
        // Return an empty valid structure to prevent downstream errors
        return of({ items: [], pageNumber: 1, totalPages: 0, totalCount: 0, hasPreviousPage: false, hasNextPage: false });
      }),
      finalize(() => this.loadingService.hide())
    );
  }

  getProductById(id: number): Observable<Product | null> {
    this.loadingService.show();
    this.currentProductSubject.next(null); // Clear previous product
    return this.productRepository.getProductById(id).pipe(
      tap(product => this.currentProductSubject.next(product)),
      catchError(err => {
        this.notificationService.error('Failed to fetch product details.', 'Error');
        console.error(err);
        this.router.navigate(['/products']); // Or a 404 page
        return of(null);
      }),
      finalize(() => this.loadingService.hide())
    );
  }

  // Admin methods
  createProduct(productData: ProductRequestDto): Observable<Product | null> {
    this.loadingService.show();
    return this.productRepository.createProduct(productData).pipe(
      tap(newProduct => {
        this.notificationService.success(`Product "${newProduct.name}" created successfully.`, 'Product Created');
        // Optionally refresh product list or add to local cache
      }),
      catchError(err => {
        this.notificationService.error('Failed to create product.', 'Error');
        console.error(err);
        return of(null);
      }),
      finalize(() => this.loadingService.hide())
    );
  }

  updateProduct(id: number, productData: ProductRequestDto): Observable<boolean> {
    this.loadingService.show();
    return this.productRepository.updateProduct(id, productData).pipe(
      map(() => { // API returns 200 OK on success, no body content for product
        this.notificationService.success(`Product "${productData.name}" updated successfully.`, 'Product Updated');
        // Optionally refresh product list or update local cache
        // Fetch the updated product to update currentProductSubject if on detail page
        if (this.currentProductSubject.value && this.currentProductSubject.value.productId === id) {
            this.getProductById(id).subscribe();
        }
        return true;
      }),
      catchError(err => {
        this.notificationService.error('Failed to update product.', 'Error');
        console.error(err);
        return of(false);
      }),
      finalize(() => this.loadingService.hide())
    );
  }

  deleteProduct(id: number): Observable<boolean> {
    this.loadingService.show();
    return this.productRepository.deleteProduct(id).pipe(
      map(() => {
        this.notificationService.success('Product deleted successfully.', 'Product Deleted');
        // Optionally refresh product list or remove from local cache
        if (this.currentProductSubject.value && this.currentProductSubject.value.productId === id) {
            this.currentProductSubject.next(null);
        }
        return true;
      }),
      catchError(err => {
        this.notificationService.error('Failed to delete product.', 'Error');
        console.error(err);
        return of(false);
      }),
      finalize(() => this.loadingService.hide())
    );
  }
}
```
*Self-correction: Added `private router: Router` to `ProductService` constructor for navigation on error (e.g., product not found).*

**`src/app/core/services/cart.service.ts`:**
```typescript
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { map, tap, catchError, switchMap, finalize } from 'rxjs/operators';
import { CartRepository } from '../repositories/cart.repository';
import { Cart, CartItem, CartRequestDto } from '../models/cart.model';
import { AuthService } from './auth.service';
import { NotificationService } from './notification.service';
import { LoadingService } from './loading.service';
import { Product } from '../models/product.model'; // For adding product details to cart item

@Injectable()
export class CartService {
  private cartSubject = new BehaviorSubject<Cart | null>(null);
  public cart$ = this.cartSubject.asObservable();

  private cartItemCountSubject = new BehaviorSubject<number>(0);

  constructor(
    private cartRepository: CartRepository,
    private authService: AuthService,
    private notificationService: NotificationService,
    private loadingService: LoadingService
  ) {
    // Load cart when user logs in or on app init if user is already logged in
    this.authService.currentUser.subscribe(user => {
      if (user && user.id) {
        this.loadCart(user.id);
      } else {
        this.clearCartLocal(); // Clear cart if user logs out
      }
    });
  }

  public getCartItemCount(): Observable<number> {
    // This can be derived from cart$ or managed separately
    return this.cart$.pipe(
      map(cart => cart?.items.reduce((acc, item) => acc + item.quantity, 0) || 0)
    );
  }

  private getCurrentUserId(): string | null {
    return this.authService.currentUserValue?.id || null;
  }

  loadCart(userId: string): void {
    if (!userId) return;
    this.loadingService.show();
    this.cartRepository.getCart(userId).pipe(
      tap(cart => {
        // Here you might need to enrich cart items with product details
        // if the backend GET /api/Cart/{userId} only returns product IDs and quantities.
        // For now, assume API returns sufficient CartItem details.
        this.cartSubject.next(cart);
        this.updateCartItemCount(cart);
      }),
      catchError(err => {
        this.notificationService.error('Failed to load cart.', 'Cart Error');
        this.clearCartLocal(); // Clear local cart on error
        return of(null);
      }),
      finalize(() => this.loadingService.hide())
    ).subscribe();
  }

  // Overload for adding a full Product object or just by ID
  addItem(product: Product, quantity: number = 1): Observable<boolean> {
      const userId = this.getCurrentUserId();
      if (!userId) {
          this.notificationService.warning('Please log in to add items to your cart.', 'Login Required');
          return of(false);
      }
      const cartRequest: CartRequestDto = { userId, productId: product.productId, quantity };
      return this.performCartOperation(
          this.cartRepository.addItemToCart(cartRequest),
          `Added ${product.name} to cart.`,
          'Failed to add item to cart.'
      );
  }


  updateItemQuantity(productId: number, quantity: number): Observable<boolean> {
    const userId = this.getCurrentUserId();
    if (!userId || quantity < 1) return of(false); // Quantity should be at least 1

    const cartRequest: CartRequestDto = { userId, productId, quantity };
    return this.performCartOperation(
      this.cartRepository.updateCartItem(cartRequest), // Assuming PUT updates quantity
      'Cart updated successfully.',
      'Failed to update cart.'
    );
  }

  removeItem(productId: number): Observable<boolean> {
    const userId = this.getCurrentUserId();
    if (!userId) return of(false);

    return this.performCartOperation(
      this.cartRepository.removeItemFromCart(userId, productId),
      'Item removed from cart.',
      'Failed to remove item from cart.'
    );
  }

  private performCartOperation(operation$: Observable<any>, successMsg: string, errorMsg: string): Observable<boolean> {
    const userId = this.getCurrentUserId();
    if (!userId) return of(false);

    this.loadingService.show();
    return operation$.pipe(
      switchMap(() => this.cartRepository.getCart(userId)), // Refresh cart after operation
      tap(updatedCart => {
        this.cartSubject.next(updatedCart);
        this.updateCartItemCount(updatedCart);
        this.notificationService.success(successMsg, 'Cart Updated');
      }),
      map(() => true),
      catchError(err => {
        this.notificationService.error(errorMsg, 'Cart Error');
        console.error(err);
        // Optionally, try to reload cart to ensure consistency even on error
        this.loadCart(userId);
        return of(false);
      }),
      finalize(() => this.loadingService.hide())
    );
  }

  private updateCartItemCount(cart: Cart | null): void {
    const count = cart?.items.reduce((sum, item) => sum + item.quantity, 0) || 0;
    this.cartItemCountSubject.next(count); // Keep this if Header uses it directly
  }

  clearCartLocal(): void {
    this.cartSubject.next(null);
    this.cartItemCountSubject.next(0);
  }

  // Call this when order is placed successfully
  clearCartAfterOrder(): Observable<boolean> {
    const currentCart = this.cartSubject.value;
    if (!currentCart || !currentCart.items.length) return of(true);

    // This might involve calling a specific backend endpoint to clear the cart,
    // or simply clearing it locally if the backend handles it post-payment.
    // For now, let's assume local clear and backend handles it.
    // If your backend needs an explicit call to empty the cart (e.g. after order):
    // const userId = this.getCurrentUserId();
    // if (!userId) return of(false);
    // return this.cartRepository.clearCart(userId).pipe(map(() => {
    //   this.clearCartLocal();
    //   return true;
    // }));

    this.clearCartLocal();
    this.notificationService.info('Cart has been cleared.', 'Order Placed');
    return of(true);
  }
}
```
*Note on CartService `addItem`*: I've assumed the `Product` object is available. If you only have `productId`, you might need to fetch product details first or adjust the method. The `cartRepository.addItemToCart` uses `CartRequestDto` which only needs `productId`.

**`src/app/core/services/order.service.ts`:**
```typescript
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { catchError, map, tap, finalize } from 'rxjs/operators';
import { OrderRepository } from '../repositories/order.repository';
import { AuthService } from './auth.service';
import { NotificationService } from './notification.service';
import { LoadingService } from './loading.service';
import { PaymentIntentResponse, OrderHistoryItem } from '../models/order.model';

@Injectable()
export class OrderService {
  constructor(
    private orderRepository: OrderRepository,
    private authService: AuthService,
    private notificationService: NotificationService,
    private loadingService: LoadingService
  ) {}

  createPaymentIntent(): Observable<PaymentIntentResponse | null> {
    const userId = this.authService.currentUserValue?.id;
    if (!userId) {
      this.notificationService.error('User not logged in. Cannot proceed with payment.', 'Auth Error');
      return of(null);
    }
    this.loadingService.show();
    return this.orderRepository.createPaymentIntent(userId).pipe(
      tap(response => {
        if (!response || !response.clientSecret) {
             this.notificationService.error('Failed to initialize payment. Missing client secret.', 'Payment Error');
        }
        // Do not show success here, Stripe flow will handle UI
      }),
      catchError(err => {
        this.notificationService.error('Failed to initialize payment.', 'Payment Error');
        console.error('Payment Intent Error:', err);
        return of(null);
      }),
      finalize(() => this.loadingService.hide())
    );
  }

  // Example for fetching order history
  getOrderHistory(): Observable<OrderHistoryItem[]> {
    const userId = this.authService.currentUserValue?.id;
    if (!userId) {
      // this.notificationService.warning('Please log in to view order history.', 'Auth Required');
      return of([]);
    }
    this.loadingService.show();
    // This endpoint is NOT in your provided spec. This is a placeholder.
    // You need to implement this in OrderRepository and your backend.
    // For now, let's assume `orderRepository.getOrderHistory` exists.
    try {
        return this.orderRepository.getOrderHistory(userId).pipe(
            catchError(err => {
                this.notificationService.error('Failed to fetch order history.', 'Error');
                console.error('Order History Error:', err);
                return of([]);
            }),
            finalize(() => this.loadingService.hide())
        );
    } catch (e) { // Catch error if getOrderHistory itself is not implemented in repo
        this.notificationService.warning('Order history feature is not available yet.', 'Feature Unavailable');
        this.loadingService.hide();
        return of([]);
    }
  }
}
```

**`src/app/core/services/category.service.ts`:**
```typescript
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { CategoryRepository } from '../repositories/category.repository';
import { Category } from '../models/category.model';
import { catchError, tap, finalize } from 'rxjs/operators';
import { NotificationService } from './notification.service';
import { LoadingService } from './loading.service';

@Injectable()
export class CategoryService {
  private categoriesSubject = new BehaviorSubject<Category[]>([]);
  public categories$ = this.categoriesSubject.asObservable();

  constructor(
    private categoryRepository: CategoryRepository,
    private notificationService: NotificationService,
    private loadingService: LoadingService
  ) {
    this.loadCategories(); // Load categories on service initialization
  }

  loadCategories(): void {
    this.loadingService.show();
    this.categoryRepository.getCategories().pipe(
      tap(categories => this.categoriesSubject.next(categories || [])),
      catchError(err => {
        this.notificationService.error('Failed to load categories.', 'Error');
        this.categoriesSubject.next([]); // Emit empty array on error
        return of([]);
      }),
      finalize(() => this.loadingService.hide())
    ).subscribe();
  }

  // Admin methods can be added here similar to ProductService if needed
}
```

---

**10. Interceptors & Guards**

**`src/app/core/interceptors/auth.interceptor.ts`:**
```typescript
import { Injectable } from '@angular/core';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from '../services/auth.service'; // Correct path

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const authToken = this.authService.getAuthToken();

    // Clone the request to add the new header.
    // Add token only if it exists and the request is not to auth endpoints themselves (optional refinement)
    if (authToken) {
      // Check if the request URL is for auth endpoints to avoid sending token unnecessarily
      // Or if the API expects token for all requests once logged in.
      // For simplicity, add to all if token exists.
      const authReq = req.clone({
        headers: req.headers.set('Authorization', `Bearer ${authToken}`)
      });
      return next.handle(authReq);
    }

    // Pass on the cloned request without token.
    return next.handle(req);
  }
}
```

**`src/app/core/guards/auth.guard.ts`:**
(Generate with `ng g guard core/guards/auth --implements CanActivate`)
```typescript
import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { NotificationService } from '../services/notification.service';
import { map, take } from 'rxjs/operators';

@Injectable({
  providedIn: 'root' // Or provide in CoreModule
})
export class AuthGuard implements CanActivate {
  constructor(
    private authService: AuthService,
    private router: Router,
    private notificationService: NotificationService
  ) {}

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {

    return this.authService.currentUser.pipe(
      take(1), // Take the first emission and complete
      map(user => {
        const isLoggedIn = !!user; // Or use this.authService.isLoggedIn;
        if (isLoggedIn) {
          // Optional: Check for roles if route has role restrictions
          // const expectedRoles = next.data.roles;
          // if (expectedRoles && !this.authService.hasRoles(expectedRoles)) {
          //   this.router.navigate(['/unauthorized']); // Or home
          //   return false;
          // }
          return true;
        }

        // Not logged in so redirect to login page with the return url
        this.notificationService.warning('You need to be logged in to access this page.', 'Access Denied');
        return this.router.createUrlTree(['/auth/login'], { queryParams: { returnUrl: state.url } });
      })
    );
  }
}
```
*Note on `AuthGuard`: For role-based access (Admin), you'd extend this or create a new `RoleGuard` and check user roles against `route.data.roles`.*

---

**11. App Routing**

**`src/app/app-routing.module.ts`:**
```typescript
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './core/guards/auth.guard';

const routes: Routes = [
  {
    path: 'auth',
    loadChildren: () => import('./features/auth/auth.module').then(m => m.AuthModule)
  },
  {
    path: 'products',
    loadChildren: () => import('./features/products/products.module').then(m => m.ProductsModule)
  },
  {
    path: 'cart',
    loadChildren: () => import('./features/cart/cart.module').then(m => m.CartModule),
    canActivate: [AuthGuard]
  },
  {
    path: 'checkout',
    loadChildren: () => import('./features/checkout/checkout.module').then(m => m.CheckoutModule),
    canActivate: [AuthGuard]
  },
  {
    path: 'profile',
    loadChildren: () => import('./features/profile/profile.module').then(m => m.ProfileModule),
    canActivate: [AuthGuard]
  },
  {
    path: 'admin',
    loadChildren: () => import('./features/admin/admin.module').then(m => m.AdminModule),
    canActivate: [AuthGuard], // Add RoleGuard here later: data: { roles: ['Admin'] }
  },
  {
    path: '', // Home page
    loadChildren: () => import('./features/home/home.module').then(m => m.HomeModule)
  },
  // Wildcard route for a 404 page (Create a NotFoundComponent in Shared or Core)
  // { path: 'not-found', component: NotFoundComponent },
  { path: '**', redirectTo: '' } // Or redirectTo: '/not-found'
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    scrollPositionRestoration: 'enabled', // Restores scroll position on navigation
    anchorScrolling: 'enabled', // Enables anchor scrolling
    initialNavigation: 'enabledBlocking' // Recommended for SSR, good practice otherwise
  })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
```

---

**12. Feature Modules & Components (Key Examples)**

I'll provide the structure for `AuthModule` (Login) and `ProductsModule` (List & Card). The other modules/components would follow a similar pattern.

**Auth Feature**

**`src/app/features/auth/auth-routing.module.ts`:**
```typescript
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
// import { GoogleCallbackComponent } from './google-callback/google-callback.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  // { path: 'google-callback', component: GoogleCallbackComponent }, // For handling Google OAuth callback
  { path: '', redirectTo: 'login', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AuthRoutingModule { }
```

**`src/app/features/auth/auth.module.ts`:**
```typescript
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../../shared/shared.module'; // For ReactiveFormsModule, etc.
import { AuthRoutingModule } from './auth-routing.module';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
// import { GoogleCallbackComponent } from './google-callback/google-callback.component';

@NgModule({
  declarations: [
    LoginComponent,
    RegisterComponent,
    // GoogleCallbackComponent
  ],
  imports: [
    CommonModule,
    SharedModule, // Ensure ReactiveFormsModule is exported from SharedModule
    AuthRoutingModule
  ]
})
export class AuthModule { }
```

**`src/app/features/auth/login/login.component.ts`:**
```typescript
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { NotificationService } from '../../../core/services/notification.service'; // Already injected in AuthService
import { first } from 'rxjs/operators';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  isLoading = false;
  submitted = false;
  returnUrl = '/';

  // Email pattern from your OpenAPI spec
  emailPattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$";
  // Password pattern from your OpenAPI spec
  // Minimum six characters, at least one uppercase letter, one lowercase letter, one number and one special character
  passwordPattern = "^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z])(?=.*[^a-zA-Z\\d]).{6,}$";


  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute
    // private notificationService: NotificationService // Not needed if AuthService handles notifications
  ) {
     // Redirect to home if already logged in
     if (this.authService.currentUserValue) {
      this.router.navigate(['/']);
    }
  }

  ngOnInit(): void {
    this.loginForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email, Validators.pattern(this.emailPattern)]],
      password: ['', [Validators.required, Validators.pattern(this.passwordPattern)]]
    });

    // Get return url from route parameters or default to '/'
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
  }

  // Convenience getter for easy access to form fields
  get f() { return this.loginForm.controls; }

  onSubmit(): void {
    this.submitted = true;

    if (this.loginForm.invalid) {
      // Mark all fields as touched to display errors
      Object.values(this.loginForm.controls).forEach(control => {
        control.markAsTouched();
      });
      return;
    }

    this.isLoading = true;
    this.authService.login({ email: this.f.email.value, password: this.f.password.value })
      .pipe(first()) // take the first emitted value and complete
      .subscribe({
        next: (success) => {
          if (success) {
            this.router.navigate([this.returnUrl]);
          } else {
            // Error message is handled by AuthService
            this.isLoading = false;
          }
        },
        error: () => { // Should be caught by AuthService, but good practice
          this.isLoading = false;
        }
      });
  }

  onGoogleLogin(): void {
    this.isLoading = true;
    // The authService method will handle the redirect.
    // No direct response is expected here.
    this.authService.initiateGoogleLogin();
    // isLoading might need to be managed differently for redirect flows
    // as the component might be destroyed.
  }
}
```

**`src/app/features/auth/login/login.component.html`:**
```html
<div class="auth-page-container">
  <div class="auth-card">
    <h2 class="auth-title">Welcome Back!</h2>
    <p class="auth-subtitle text-secondary">Login to continue your LuxeCart experience.</p>

    <form [formGroup]="loginForm" (ngSubmit)="onSubmit()" class="auth-form" novalidate>
      <div class="form-group">
        <label for="email" class="form-label">Email Address</label>
        <input type="email" id="email" formControlName="email" class="form-control"
               [ngClass]="{ 'is-invalid': submitted && f.email.errors }"
               placeholder="you@example.com" autocomplete="email">
        <div *ngIf="submitted && f.email.errors" class="form-error-message">
          <div *ngIf="f.email.errors.required">Email is required.</div>
          <div *ngIf="f.email.errors.email || f.email.errors.pattern">Please enter a valid email address.</div>
        </div>
      </div>

      <div class="form-group">
        <label for="password" class="form-label">Password</label>
        <input type="password" id="password" formControlName="password" class="form-control"
               [ngClass]="{ 'is-invalid': submitted && f.password.errors }"
               placeholder="Enter your password" autocomplete="current-password">
        <div *ngIf="submitted && f.password.errors" class="form-error-message">
          <div *ngIf="f.password.errors.required">Password is required.</div>
          <div *ngIf="f.password.errors.pattern">Password must be at least 6 characters and include uppercase, lowercase, number, and special character.</div>
        </div>
      </div>

      <button type="submit" class="btn btn-primary w-100 btn-submit" [disabled]="isLoading">
        <span *ngIf="!isLoading">Login</span>
        <span *ngIf="isLoading">
          <!-- Add a simple spinner or text -->
          Logging in...
        </span>
      </button>
    </form>

    <div class="social-login-divider">
      <span class="text-secondary">OR</span>
    </div>

    <button type="button" (click)="onGoogleLogin()" class="btn btn-outline-dark w-100 btn-google" [disabled]="isLoading">
      <!-- Replace with Google Icon SVG -->
      <svg width="20" height="20" viewBox="0 0 533.5 544.3" xmlns="http://www.w3.org/2000/svg" style="margin-right: 8px;"><path d="M533.5 278.4c0-18.5-1.5-37.1-4.7-55.3H272.1v104.8h147c-6.1 33.8-25.7 63.7-54.4 82.7v68h87.7c51.5-47.4 81.1-117.4 81.1-200.2z" fill="#4285f4"/><path d="M272.1 544.3c73.4 0 135.3-24.1 180.4-65.7l-87.7-68c-24.4 16.6-55.9 26-92.6 26-71 0-131.2-47.9-152.8-112.3H28.9v70.1c46.2 91.9 140.3 149.9 243.2 149.9z" fill="#34a853"/><path d="M119.3 324.3c-11.4-33.8-11.4-70.4 0-104.2V150H28.9c-38.6 76.9-38.6 167.5 0 244.4l90.4-70.1z" fill="#fbbc04"/><path d="M272.1 107.7c38.8-.6 76.3 14 104.4 40.8l77.7-77.7C405 24.6 339.7-.8 272.1 0 169.2 0 75.1 58 28.9 150l90.4 70.1c21.5-64.5 81.8-112.4 152.8-112.4z" fill="#ea4335"/></svg>
      Continue with Google
    </button>

    <p class="auth-switch text-secondary">
      Don't have an account? <a routerLink="../register" class="text-gold">Sign up</a>
    </p>
  </div>
</div>
```

**`src/app/features/auth/login/login.component.scss` (and common styles for Register):**
(Place this in a shared `_auth-styles.scss` and import into login/register, or keep it simple for now)
```scss
@import 'assets/styles/variables';

.auth-page-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 150px); // Adjust based on header/footer height
  padding: $space-lg $space-md;
  background-color: $background-light; // Light background for auth pages
}

.auth-card {
  background-color: $primary-white;
  padding: $space-lg $space-xl;
  border-radius: $border-radius-lg;
  box-shadow: $box-shadow;
  width: 100%;
  max-width: 450px; // Max width for the form card
  text-align: center;
}

.auth-title {
  font-size: $font-size-xl;
  color: $accent-rich-black;
  margin-bottom: $space-sm;
}

.auth-subtitle {
  margin-bottom: $space-lg;
  font-size: $font-size-base;
}

.auth-form {
  text-align: left; // Align form elements left

  .form-group {
    margin-bottom: $space-md;
  }

  .form-label {
    font-weight: $font-weight-normal; // Lighter labels
    font-size: $font-size-sm;
    color: $secondary-gray;
  }

  .form-control {
    padding: $space-sm; // Comfortable padding
    &.is-invalid { // Custom invalid styling if needed beyond bootstrap-like
      border-color: $error-color;
    }
  }
  .form-error-message {
    font-size: $font-size-sm;
    margin-top: $space-xs / 2;
  }
}

.btn-submit {
  margin-top: $space-md;
  padding: $space-sm; // Larger submit button
  font-size: $font-size-base;
}

.social-login-divider {
  margin: $space-lg 0;
  display: flex;
  align-items: center;
  text-align: center;
  color: $secondary-gray;

  &::before,
  &::after {
    content: '';
    flex-grow: 1;
    background-color: $light-gray-border;
    height: 1px;
    margin: 0 $space-sm;
  }
}

.btn-google {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: $space-lg;
  color: $primary-black;
  border-color: $light-gray-border;

  &:hover {
    background-color: $background-light;
    border-color: $secondary-gray;
  }
}

.auth-switch {
  font-size: $font-size-sm;
  a {
    font-weight: $font-weight-bold;
  }
}
```
*Self-correction:* Added `autocomplete` attributes to input fields for better UX.

**`src/app/features/auth/register/register.component.ts` (Structure):**
```typescript
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { NotificationService } from '../../../core/services/notification.service';
import { first } from 'rxjs/operators';
import { PasswordMatchValidator } from '../../../shared/validators/password-match.validator'; // You'll create this

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['../login/login.component.scss'] // Re-use login styles
})
export class RegisterComponent implements OnInit {
  registerForm!: FormGroup;
  isLoading = false;
  submitted = false;

  // Patterns from OpenAPI spec
  emailPattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$";
  passwordPattern = "^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z])(?=.*[^a-zA-Z\\d]).{6,}$";
  displayNamePattern = ".{1,}"; // MinLength 1

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private notificationService: NotificationService
  ) {
    if (this.authService.currentUserValue) {
      this.router.navigate(['/']);
    }
  }

  ngOnInit(): void {
    this.registerForm = this.formBuilder.group({
      displayName: ['', [Validators.required, Validators.pattern(this.displayNamePattern)]],
      email: ['', [Validators.required, Validators.email, Validators.pattern(this.emailPattern)]],
      password: ['', [Validators.required, Validators.pattern(this.passwordPattern)]],
      confirmPassword: ['', Validators.required]
    }, {
      validator: PasswordMatchValidator('password', 'confirmPassword')
    });
  }

  get f() { return this.registerForm.controls; }

  onSubmit(): void {
    this.submitted = true;
    if (this.registerForm.invalid) {
      Object.values(this.registerForm.controls).forEach(control => {
        control.markAsTouched();
      });
      return;
    }

    this.isLoading = true;
    this.authService.register({
      displayName: this.f.displayName.value,
      email: this.f.email.value,
      password: this.f.password.value,
      confirmPassword: this.f.confirmPassword.value
    }).pipe(first()).subscribe({
      next: (success) => {
        if (success) {
          this.router.navigate(['/']); // Or to a profile completion page
        } else {
          // Error handled by AuthService
          this.isLoading = false;
        }
      },
      error: () => {
        this.isLoading = false;
      }
    });
  }
}
```
*You'll need to create `src/app/shared/validators/password-match.validator.ts`.*
```typescript
// src/app/shared/validators/password-match.validator.ts
import { FormGroup, ValidatorFn, ValidationErrors } from '@angular/forms';

export function PasswordMatchValidator(controlName: string, matchingControlName: string): ValidatorFn {
  return (formGroup: FormGroup): ValidationErrors | null => {
    const control = formGroup.controls[controlName];
    const matchingControl = formGroup.controls[matchingControlName];

    if (!control || !matchingControl) {
      return null; // Or throw an error if controls are not found
    }

    // if matchingControl is not touched yet, don't validate
    if (matchingControl.pristine) {
        return null;
    }

    // Set error on matchingControl if validation fails
    if (control.value !== matchingControl.value) {
      matchingControl.setErrors({ passwordMismatch: true });
      return { passwordMismatch: true }; // Error on the form group itself
    } else {
      matchingControl.setErrors(null);
      return null;
    }
  };
}
```

**`src/app/features/auth/register/register.component.html`:**
(Similar structure to login, update field names and messages)
```html
<div class="auth-page-container">
  <div class="auth-card">
    <h2 class="auth-title">Create Your Account</h2>
    <p class="auth-subtitle text-secondary">Join LuxeCart and start shopping with style.</p>

    <form [formGroup]="registerForm" (ngSubmit)="onSubmit()" class="auth-form" novalidate>
      <div class="form-group">
        <label for="displayName" class="form-label">Display Name</label>
        <input type="text" id="displayName" formControlName="displayName" class="form-control"
               [ngClass]="{ 'is-invalid': submitted && f.displayName.errors }"
               placeholder="Your Name" autocomplete="name">
        <div *ngIf="submitted && f.displayName.errors" class="form-error-message">
          <div *ngIf="f.displayName.errors.required">Display name is required.</div>
          <div *ngIf="f.displayName.errors.pattern">Display name must not be empty.</div>
        </div>
      </div>

      <div class="form-group">
        <label for="email" class="form-label">Email Address</label>
        <input type="email" id="email" formControlName="email" class="form-control"
               [ngClass]="{ 'is-invalid': submitted && f.email.errors }"
               placeholder="you@example.com" autocomplete="email">
        <div *ngIf="submitted && f.email.errors" class="form-error-message">
          <div *ngIf="f.email.errors.required">Email is required.</div>
          <div *ngIf="f.email.errors.email || f.email.errors.pattern">Please enter a valid email address.</div>
        </div>
      </div>

      <div class="form-group">
        <label for="password" class="form-label">Password</label>
        <input type="password" id="password" formControlName="password" class="form-control"
               [ngClass]="{ 'is-invalid': submitted && f.password.errors }"
               placeholder="Create a strong password" autocomplete="new-password">
        <div *ngIf="submitted && f.password.errors" class="form-error-message">
          <div *ngIf="f.password.errors.required">Password is required.</div>
          <div *ngIf="f.password.errors.pattern">Password must be at least 6 characters and include uppercase, lowercase, number, and special character.</div>
        </div>
      </div>

      <div class="form-group">
        <label for="confirmPassword" class="form-label">Confirm Password</label>
        <input type="password" id="confirmPassword" formControlName="confirmPassword" class="form-control"
               [ngClass]="{ 'is-invalid': submitted && (f.confirmPassword.errors || registerForm.errors?.passwordMismatch && f.confirmPassword.touched) }"
               placeholder="Confirm your password" autocomplete="new-password">
        <div *ngIf="submitted && f.confirmPassword.errors" class="form-error-message">
          <div *ngIf="f.confirmPassword.errors.required">Confirming password is required.</div>
        </div>
         <div *ngIf="submitted && registerForm.errors?.passwordMismatch && f.confirmPassword.touched && !f.confirmPassword.errors?.required" class="form-error-message">
          Passwords do not match.
        </div>
      </div>

      <button type="submit" class="btn btn-primary w-100 btn-submit" [disabled]="isLoading">
        <span *ngIf="!isLoading">Create Account</span>
        <span *ngIf="isLoading">Creating...</span>
      </button>
    </form>

    <p class="auth-switch text-secondary">
      Already have an account? <a routerLink="../login" class="text-gold">Log in</a>
    </p>
  </div>
</div>
```

**Products Feature**

**`src/app/features/products/products-routing.module.ts`:**
```typescript
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProductListComponent } from './product-list/product-list.component';
import { ProductDetailComponent } from './product-detail/product-detail.component';

const routes: Routes = [
  { path: '', component: ProductListComponent },
  { path: ':id', component: ProductDetailComponent }
  // Consider a route like /category/:categoryName for category-specific listings
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProductsRoutingModule { }
```

**`src/app/features/products/products.module.ts`:**
```typescript
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../../shared/shared.module';
import { ProductsRoutingModule } from './products-routing.module';

import { ProductListComponent } from './product-list/product-list.component';
import { ProductDetailComponent } from './product-detail/product-detail.component';
import { ProductCardComponent } from './components/product-card/product-card.component';
import { ProductFiltersComponent } from './components/product-filters/product-filters.component'; // Create this

@NgModule({
  declarations: [
    ProductListComponent,
    ProductDetailComponent,
    ProductCardComponent,
    ProductFiltersComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    ProductsRoutingModule
  ]
})
export class ProductsModule { }
```

**`src/app/features/products/components/product-card/product-card.component.ts`:**
```typescript
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Product } from '../../../../core/models/product.model';

@Component({
  selector: 'app-product-card',
  templateUrl: './product-card.component.html',
  styleUrls: ['./product-card.component.scss']
})
export class ProductCardComponent {
  @Input() product!: Product;
  @Output() addToCart = new EventEmitter<Product>();
  @Output() viewDetails = new EventEmitter<Product>(); // Or navigate directly

  defaultImageUrl = 'assets/images/product-placeholder.png'; // Add a placeholder image

  onAddToCartClick(event: MouseEvent): void {
    event.stopPropagation(); // Prevent triggering viewDetails if card is clickable
    this.addToCart.emit(this.product);
  }

  onViewDetailsClick(): void {
    this.viewDetails.emit(this.product);
  }

  getImageUrl(): string {
    // Assuming your API base URL needs to be prepended if imageUrl is relative
    // and that product.imageUrl may or may not include the base path.
    // Adjust this logic based on how your API returns image URLs.
    if (this.product.imageUrl) {
        if (this.product.imageUrl.startsWith('http')) {
            return this.product.imageUrl;
        }
        // Example: If API returns "images/product.jpg" and base is "https://tpf.runasp.net/"
        // you might need to construct "https://tpf.runasp.net/images/product.jpg"
        // For now, assume it's a full URL or a path that works directly.
        // If relative to API root, prepend environment.apiBaseUrl
        // return `${environment.apiBaseUrl}${this.product.imageUrl}`;
        return this.product.imageUrl; // Simpler, assuming it's a full URL or correctly relative from index.html
    }
    return this.defaultImageUrl;
  }
}
```
*Update for `getImageUrl()`:* Your API for Products `POST`/`PUT` takes `ImageFile`. The `GET` response for product details isn't fully specified for `imageUrl`. Assuming the backend provides a usable `imageUrl` (either absolute or relative to the domain). `https://tpf.runasp.net/` + `imageUrl` is a likely scenario if it's relative to the API root.

**`src/app/features/products/components/product-card/product-card.component.html`:**
```html
<div class="card product-card h-100" (click)="onViewDetailsClick()" role="button" [attr.aria-label]="'View details for ' + product.name">
  <img [src]="getImageUrl()"
       [alt]="product.name"
       class="card-img-top product-card-image"
       onError="this.src='assets/images/product-placeholder.png'"> <!-- Fallback if image fails to load -->
  <div class="card-body product-card-body">
    <h5 class="card-title product-card-title" [title]="product.name">{{ product.name }}</h5>
    <!-- <p class="card-text product-card-category text-secondary">{{ product.categoryName || 'Uncategorized' }}</p> -->
    <p class="card-subtitle product-card-price">{{ product.price | currency:'USD':'symbol':'1.2-2' }}</p>
  </div>
  <div class="card-footer product-card-footer">
    <button (click)="onAddToCartClick($event)" class="btn btn-primary w-100">
      Add to Cart
    </button>
    <!-- Or:
    <button (click)="onViewDetailsClick()" class="btn btn-outline-dark w-50">Details</button>
    <button (click)="onAddToCartClick($event)" class="btn btn-primary w-50 ms-1">Cart</button>
    -->
  </div>
</div>
```

**`src/app/features/products/components/product-card/product-card.component.scss`:**
```scss
@import 'assets/styles/variables';

.product-card {
  cursor: pointer; // Indicates the whole card is clickable for details
  display: flex;
  flex-direction: column; // Ensures footer is at bottom for h-100

  .product-card-image {
    aspect-ratio: 1 / 1; // Square images, or adjust to 4/3, 3/4 etc.
    object-fit: cover; // Or 'contain' if you don't want cropping
    background-color: $background-light; // Placeholder bg color
  }

  .product-card-body {
    flex-grow: 1; // Allows body to take available space
    text-align: center; // Center text for a clean look
    padding: $space-sm;
  }

  .product-card-title {
    font-size: $font-size-base; // Slightly smaller for cards
    font-weight: $font-weight-normal;
    color: $primary-black;
    margin-bottom: $space-xs / 2;
    // Ellipsis for long titles
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    height: 1.5em; // Assuming line-height is around 1.5
  }

  .product-card-category {
    font-size: $font-size-sm * 0.9;
    margin-bottom: $space-xs;
  }

  .product-card-price {
    font-size: $font-size-lg;
    font-weight: $font-weight-bold;
    color: $primary-black; // Or $primary-gold for emphasis
    margin-bottom: $space-sm;
  }

  .product-card-footer {
    border-top: none; // Cleaner look without border if body is also light
    background-color: transparent;
    padding: 0 $space-sm $space-sm; // Padding around button

    .btn {
      font-size: $font-size-sm;
      padding: $space-xs $space-sm; // Smaller button padding
    }
  }

  // Hover effect combined with global card hover
  &:hover {
    .product-card-title {
      // color: $primary-gold; // Optional: highlight title on hover
    }
  }
}
```

**`src/app/features/products/product-list/product-list.component.ts`:**
```typescript
import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, Subscription, combineLatest, BehaviorSubject } from 'rxjs';
import { map, switchMap, distinctUntilChanged, debounceTime, tap } from 'rxjs/operators';
import { ProductService } from '../../../core/services/product.service';
import { CartService } from '../../../core/services/cart.service';
import { CategoryService } from '../../../core/services/category.service';
import { Product, PaginatedProducts } from '../../../core/models/product.model';
import { Category } from '../../../core/models/category.model';
import { NotificationService } from '../../../core/services/notification.service';
import { LoadingService } from '../../../core/services/loading.service';


interface ProductListParams {
  page: number;
  limit: number;
  category?: string;
  search?: string;
}

@Component({
  selector: 'app-product-list',
  templateUrl: './product-list.component.html',
  styleUrls: ['./product-list.component.scss']
})
export class ProductListComponent implements OnInit, OnDestroy {
  products: Product[] = [];
  categories$: Observable<Category[]>;
  isLoading$: Observable<boolean>;

  currentPage = 1;
  itemsPerPage = 12; // Or get from a config
  totalItems = 0;
  totalPages = 0;

  // For filters
  selectedCategory: string | undefined = undefined;
  searchQuery = '';

  private paramsSubject = new BehaviorSubject<ProductListParams>({
    page: this.currentPage,
    limit: this.itemsPerPage
  });
  private subscriptions = new Subscription();


  constructor(
    private productService: ProductService,
    private cartService: CartService,
    private categoryService: CategoryService,
    private notificationService: NotificationService,
    public loadingService: LoadingService, // Public to use in template
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.categories$ = this.categoryService.categories$;
    this.isLoading$ = this.loadingService.isLoading$;
  }

  ngOnInit(): void {
    const queryParamsSub = this.route.queryParamMap.pipe(
      map(params => ({
        page: params.get('page') ? +params.get('page')! : 1,
        limit: params.get('limit') ? +params.get('limit')! : this.itemsPerPage,
        category: params.get('category') || undefined,
        search: params.get('search') || undefined
      })),
      distinctUntilChanged((prev, curr) => JSON.stringify(prev) === JSON.stringify(curr))
    ).subscribe(params => {
      this.currentPage = params.page;
      this.itemsPerPage = params.limit;
      this.selectedCategory = params.category;
      this.searchQuery = params.search || ''; // Update local search query for input binding
      this.paramsSubject.next(params);
    });
    this.subscriptions.add(queryParamsSub);


    const productsSub = this.paramsSubject.pipe(
      debounceTime(100), // Debounce if params change rapidly (e.g. typed search)
      switchMap(params =>
        this.productService.getProducts(
          params.page,
          params.limit,
          params.category,
          params.search
        )
      )
    ).subscribe((paginatedResult: PaginatedProducts) => {
      this.products = paginatedResult.items || [];
      this.currentPage = paginatedResult.pageNumber || 1;
      this.totalItems = paginatedResult.totalCount || 0;
      this.totalPages = paginatedResult.totalPages || 0;
      // itemsPerPage is fixed by request, totalPages derived from totalCount and itemsPerPage
    });
    this.subscriptions.add(productsSub);
  }

  onAddToCart(product: Product): void {
    this.cartService.addItem(product, 1).subscribe(success => {
      if (success) {
        // Notification is handled by cartService
      }
    });
  }

  onViewProductDetails(product: Product): void {
    this.router.navigate(['/products', product.productId]);
  }

  onPageChange(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.updateQueryParams({ page });
    }
  }

  onCategoryFilterChange(categoryName?: string): void {
    this.selectedCategory = categoryName;
    this.updateQueryParams({ category: categoryName || undefined, page: 1 });
  }

  onSearch(): void {
    // Triggered by (ngSubmit) or button click for search input
    this.updateQueryParams({ search: this.searchQuery.trim() || undefined, page: 1 });
  }

  clearSearch(): void {
    this.searchQuery = '';
    this.updateQueryParams({ search: undefined, page: 1 });
  }

  clearFilters(): void {
    this.selectedCategory = undefined;
    this.searchQuery = '';
    this.updateQueryParams({ category: undefined, search: undefined, page: 1 });
  }


  private updateQueryParams(newParams: Partial<ProductListParams>): void {
    const currentParams = this.paramsSubject.value;
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: { ...currentParams, ...newParams },
      queryParamsHandling: 'merge', // Merge with existing query params
    });
  }

  // For pagination UI
  getPagesArray(): number[] {
    if (this.totalPages <= 0) return [];
    return Array(this.totalPages).fill(0).map((x, i) => i + 1);
  }


  ngOnDestroy(): void {
    this.subscriptions.unsubscribe();
  }
}
```

**`src/app/features/products/product-list/product-list.component.html`:**
```html
<div class="container product-list-page">
  <header class="page-header">
    <h1>Discover Our Collection</h1>
    <p class="text-secondary">Find the perfect items that speak to your style.</p>
  </header>

  <!-- Filters Section: Create ProductFiltersComponent or inline -->
  <div class="filters-section card mb-4">
    <div class="card-body">
        <div class="row gy-3 align-items-end">
            <div class="col-md-5">
                <label for="searchQuery" class="form-label">Search Products</label>
                <div class="input-group">
                    <input type="text" id="searchQuery" class="form-control" placeholder="Search by name or keyword..."
                           [(ngModel)]="searchQuery" (keyup.enter)="onSearch()">
                    <button class="btn btn-outline-dark" type="button" (click)="onSearch()">Search</button>
                     <button *ngIf="searchQuery" class="btn btn-outline-secondary" type="button" (click)="clearSearch()" title="Clear Search">&times;</button>
                </div>
            </div>
            <div class="col-md-4">
                <label for="categoryFilter" class="form-label">Filter by Category</label>
                <select id="categoryFilter" class="form-select form-control"
                        [ngModel]="selectedCategory"
                        (ngModelChange)="onCategoryFilterChange($event)">
                    <option [ngValue]="undefined">All Categories</option>
                    <option *ngFor="let category of categories$ | async" [value]="category.categoryName">
                        {{ category.categoryName }}
                    </option>
                </select>
            </div>
            <div class="col-md-3">
                <button class="btn btn-secondary w-100" (click)="clearFilters()">Clear All Filters</button>
            </div>
        </div>
    </div>
  </div>


  <div *ngIf="isLoading$ | async" class="loading-indicator text-center my-5">
    <!-- Replace with a nicer spinner component -->
    <p>Loading products...</p>
    <!-- <app-loading-spinner></app-loading-spinner> -->
  </div>

  <div *ngIf="!(isLoading$ | async) && products.length === 0" class="empty-state text-center my-5">
    <!-- <app-empty-state message="No products found matching your criteria."></app-empty-state> -->
    <img src="assets/images/empty-box.svg" alt="No products found" style="max-width: 150px; margin-bottom: 1rem;">
    <h3>No Products Found</h3>
    <p class="text-secondary">Try adjusting your search or filters, or check back later!</p>
    <button class="btn btn-primary mt-2" (click)="clearFilters()">Reset Filters</button>
  </div>

  <div *ngIf="!(isLoading$ | async) && products.length > 0" class="product-grid">
    <div *ngFor="let product of products" class="product-grid-item">
      <app-product-card
        [product]="product"
        (addToCart)="onAddToCart($event)"
        (viewDetails)="onViewProductDetails($event)">
      </app-product-card>
    </div>
  </div>

  <!-- Pagination -->
  <nav *ngIf="!(isLoading$ | async) && products.length > 0 && totalPages > 1" aria-label="Product navigation" class="pagination-controls mt-5">
    <ul class="pagination justify-content-center">
      <li class="page-item" [class.disabled]="currentPage === 1">
        <a class="page-link" (click)="onPageChange(currentPage - 1)" role="button" tabindex="0" aria-label="Previous">
          &laquo; Prev
        </a>
      </li>
      <!-- Simple page numbers (for many pages, implement ellipsis logic) -->
      <ng-container *ngFor="let pageNum of getPagesArray()">
        <li class="page-item" [class.active]="pageNum === currentPage" *ngIf="Math.abs(pageNum - currentPage) < 3 || pageNum === 1 || pageNum === totalPages || (Math.abs(pageNum - currentPage) === 3 && (pageNum === 1 || pageNum === totalPages))">
            <a class="page-link" (click)="onPageChange(pageNum)" role="button" tabindex="0">{{ pageNum }}</a>
        </li>
        <li class="page-item disabled" *ngIf="(Math.abs(pageNum - currentPage) === 3 && !(pageNum === 1 || pageNum === totalPages)) && ( (pageNum < currentPage && currentPage -1 > 2) || (pageNum > currentPage && totalPages - currentPage > 2) )">
            <span class="page-link">...</span>
        </li>
      </ng-container>

      <li class="page-item" [class.disabled]="currentPage === totalPages">
        <a class="page-link" (click)="onPageChange(currentPage + 1)" role="button" tabindex="0" aria-label="Next">
          Next &raquo;
        </a>
      </li>
    </ul>
  </nav>
</div>
```

**`src/app/features/products/product-list/product-list.component.scss`:**
```scss
@import 'assets/styles/variables';

.product-list-page {
  padding-top: $space-lg;
  padding-bottom: $space-xl;
}

.page-header {
  text-align: center;
  margin-bottom: $space-xl;
  h1 {
    font-size: $font-size-xxl;
    margin-bottom: $space-xs;
  }
  p {
    font-size: $font-size-lg;
  }
}

.filters-section {
  background-color: $primary-white; // Or a very light gray
  border-radius: $border-radius-lg;
  padding: $space-md;
  .form-label {
    font-size: $font-size-sm;
    font-weight: $font-weight-bold;
    margin-bottom: $space-xs / 2;
  }
  .input-group .form-control, .form-select {
    height: calc(2.25rem + 10px); // Taller inputs
    padding: $space-sm;
  }
  .input-group .btn {
    height: calc(2.25rem + 10px); // Match input height
  }
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); // Responsive grid
  gap: $space-lg;

  @media (min-width: $breakpoint-sm) {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: $space-md;
  }
  @media (min-width: $breakpoint-md) {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  }
   @media (min-width: $breakpoint-lg) {
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
     gap: $space-lg;
  }
}

.product-grid-item {
  // Each item will take the app-product-card styling
  // Ensure cards have consistent height if desired:
  // display: flex; // If product-card itself is not flex column
}

.pagination-controls {
  .pagination {
    .page-item {
      margin: 0 2px;
      .page-link {
        color: $primary-black;
        border-radius: $border-radius-sm;
        padding: $space-xs $space-sm; // Comfortable tap targets
        min-width: 40px;
        text-align: center;
        transition: $transition-base;
        border: 1px solid $light-gray-border;

        &:hover {
          background-color: $background-light;
          border-color: $secondary-gray;
        }
      }
      &.active .page-link {
        background-color: $primary-gold;
        border-color: $primary-gold;
        color: $primary-black;
        font-weight: $font-weight-bold;
      }
      &.disabled .page-link {
        color: $secondary-gray;
        pointer-events: none;
        background-color: transparent;
        border-color: $light-gray-border;
      }
    }
  }
}

.loading-indicator, .empty-state {
  min-height: 300px; // Ensure it takes some space
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
```

**`src/app/features/products/product-detail/product-detail.component.ts` (Structure):**
```typescript
import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ProductService } from '../../../core/services/product.service';
import { CartService } from '../../../core/services/cart.service';
import { Product } from '../../../core/models/product.model';
import { Observable, Subscription, of } from 'rxjs';
import { switchMap, catchError, tap } from 'rxjs/operators';
import { NotificationService } from '../../../core/services/notification.service';
import { LoadingService } from '../../../core/services/loading.service';


@Component({
  selector: 'app-product-detail',
  templateUrl: './product-detail.component.html',
  styleUrls: ['./product-detail.component.scss']
})
export class ProductDetailComponent implements OnInit, OnDestroy {
  product$: Observable<Product | null>;
  product: Product | null = null; // For easier template access after resolution
  quantity = 1;
  isLoading$: Observable<boolean>;

  private productSubscription!: Subscription;

  defaultImageUrl = 'assets/images/product-placeholder-large.png'; // Larger placeholder

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private productService: ProductService,
    private cartService: CartService,
    private notificationService: NotificationService,
    public loadingService: LoadingService
  ) {
    this.isLoading$ = this.loadingService.isLoading$;
    this.product$ = this.route.paramMap.pipe(
      switchMap(params => {
        const id = params.get('id');
        if (id) {
          return this.productService.getProductById(+id);
        }
        this.router.navigate(['/products']); // Or to a 404 page
        return of(null);
      }),
      tap(product => this.product = product), // Assign to local property
      catchError(() => { // Handled in service, but good for component-level fallback
        this.router.navigate(['/products']);
        return of(null);
      })
    );
  }

  ngOnInit(): void {
    // Subscription can be done here if product$ is not directly used with async pipe in template
    // this.productSubscription = this.product$.subscribe(p => this.product = p);
  }

  onAddToCart(): void {
    if (this.product && this.quantity > 0) {
      this.cartService.addItem(this.product, this.quantity).subscribe(success => {
        if (success) {
          // Notification handled by cartService
          // Optionally, show a more prominent confirmation on this page
        }
      });
    }
  }

  incrementQuantity(): void {
    this.quantity++;
  }

  decrementQuantity(): void {
    if (this.quantity > 1) {
      this.quantity--;
    }
  }

  getImageUrl(product: Product | null): string {
    if (product?.imageUrl) {
       // Same logic as product-card.component.ts
       if (product.imageUrl.startsWith('http')) {
            return product.imageUrl;
        }
        return product.imageUrl;
    }
    return this.defaultImageUrl;
  }


  ngOnDestroy(): void {
    if (this.productSubscription) {
      this.productSubscription.unsubscribe();
    }
    // Clear current product in service if it's set there for global state
    // this.productService.clearCurrentProduct();
  }
}
```

**`src/app/features/products/product-detail/product-detail.component.html`:**
```html
<div class="product-detail-page container py-5" *ngIf="(product$ | async) as product; else loadingOrError">
  <div class="row">
    <div class="col-md-6 mb-4 mb-md-0">
      <div class="product-image-gallery">
        <!-- Main Image -->
        <img [src]="getImageUrl(product)" [alt]="product.name" class="img-fluid main-product-image" onError="this.src='assets/images/product-placeholder-large.png'">
        <!-- Thumbnails (if multiple images) -->
        <!-- <div class="thumbnails mt-3 d-flex">
          <img src="..." alt="Thumbnail 1" class="img-thumbnail me-2 active">
          ...
        </div> -->
      </div>
    </div>
    <div class="col-md-6 product-info">
      <h1 class="product-name">{{ product.name }}</h1>
      <p class="product-category text-secondary">{{ product.categoryName || 'General' }}</p>

      <div class="product-price h2 my-3">{{ product.price | currency:'USD':'symbol':'1.2-2' }}</div>

      <p class="product-description text-secondary">{{ product.description || 'No description available.' }}</p>

      <!-- Quantity Selector -->
      <div class="form-group quantity-selector my-4">
        <label for="quantity" class="form-label me-3">Quantity:</label>
        <div class="input-group" style="max-width: 150px;">
          <button class="btn btn-outline-dark btn-sm" type="button" (click)="decrementQuantity()" [disabled]="quantity <= 1">-</button>
          <input type="number" id="quantity" class="form-control text-center" [(ngModel)]="quantity" min="1" readonly>
          <button class="btn btn-outline-dark btn-sm" type="button" (click)="incrementQuantity()">+</button>
        </div>
      </div>

      <button (click)="onAddToCart()" class="btn btn-primary btn-lg w-100 add-to-cart-btn">
        Add to Cart
      </button>

      <!-- Additional Info: SKU, Availability, Reviews Placeholder -->
      <div class="additional-info mt-4">
        <p class="text-sm text-secondary"><small>SKU: {{ product.productId || 'N/A' }}</small></p>
        <!-- <p class="text-sm"><small>Availability: In Stock</small></p> -->
      </div>
    </div>
  </div>

  <!-- Related Products / Reviews Section (Placeholder) -->
  <!-- <div class="related-products mt-5">
    <h2>You Might Also Like</h2>
    ...
  </div> -->
</div>

<ng-template #loadingOrError>
  <div *ngIf="isLoading$ | async; else notFound" class="loading-indicator text-center my-5 py-5">
    <p>Loading product details...</p>
    <!-- <app-loading-spinner></app-loading-spinner> -->
  </div>
</ng-template>
<ng-template #notFound>
  <div class="container text-center my-5 py-5">
    <h2>Product Not Found</h2>
    <p class="text-secondary">The product you are looking for does not exist or may have been removed.</p>
    <a routerLink="/products" class="btn btn-primary mt-3">Back to Products</a>
  </div>
</ng-template>
```

**`src/app/features/products/product-detail/product-detail.component.scss`:**
```scss
@import 'assets/styles/variables';

.product-detail-page {
  .main-product-image {
    width: 100%;
    max-height: 500px; // Limit image height
    object-fit: cover; // Or 'contain'
    border-radius: $border-radius-lg;
    background-color: $background-light;
    box-shadow: $box-shadow-sm;
  }

  .product-info {
    .product-name {
      font-size: $font-size-xxl * 1.2; // Larger name
      font-weight: $font-weight-bold;
      color: $accent-rich-black;
      line-height: 1.2;
    }
    .product-category {
      font-size: $font-size-base;
      margin-bottom: $space-md;
    }
    .product-price {
      color: $primary-black; // Or $primary-gold;
      font-weight: $font-weight-bold;
    }
    .product-description {
      font-size: $font-size-base;
      line-height: 1.7;
      margin-bottom: $space-lg;
    }
  }

  .quantity-selector {
    display: flex;
    align-items: center;
    .form-label {
      margin-bottom: 0;
    }
    .input-group {
      .form-control {
        border-left: none;
        border-right: none;
        &:focus { box-shadow: none; }
      }
      .btn {
        border-color: $light-gray-border;
        &:hover { background-color: $background-light; }
      }
    }
  }

  .add-to-cart-btn {
    padding: $space-sm $space-lg; // Larger button
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .additional-info {
    border-top: 1px solid $light-gray-border;
    padding-top: $space-md;
    margin-top: $space-lg;
  }
}

// Styles for loading/not found states (can be global)
.loading-indicator, .empty-state-container { // Assuming .empty-state-container for the #notFound template
    min-height: 60vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
```

---

**13. Home Page (Structure)**

**`src/app/features/home/home-routing.module.ts`:**
```typescript
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home.component';

const routes: Routes = [{ path: '', component: HomeComponent }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HomeRoutingModule { }
```

**`src/app/features/home/home.module.ts`:**
```typescript
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../../shared/shared.module';
import { HomeRoutingModule } from './home-routing.module';
import { HomeComponent } from './home.component';
import { ProductsModule } from '../products/products.module'; // If reusing product-card

@NgModule({
  declarations: [HomeComponent],
  imports: [
    CommonModule,
    SharedModule,
    HomeRoutingModule,
    ProductsModule // To use app-product-card
  ]
})
export class HomeModule { }
```

**`src/app/features/home/home.component.ts`:**
```typescript
import { Component, OnInit } from '@angular/core';
import { ProductService } from '../../core/services/product.service';
import { CartService } from '../../core/services/cart.service';
import { Product } from '../../core/models/product.model';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { Router } from '@angular/router';
import { LoadingService } from '../../core/services/loading.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  featuredProducts$: Observable<Product[]> = of([]);
  latestProducts$: Observable<Product[]> = of([]);
  isLoading$: Observable<boolean>;

  // Carousel items (example)
  carouselItems = [
    { title: 'New Collection Arrivals', subtitle: 'Discover the latest trends', imageUrl: 'assets/images/carousel-1.jpg', link: '/products?category=new' },
    { title: 'Seasonal Sale Up to 50% Off', subtitle: 'Limited time offer', imageUrl: 'assets/images/carousel-2.jpg', link: '/products?sale=true' },
    { title: 'Timeless Elegance', subtitle: 'Curated luxury pieces', imageUrl: 'assets/images/carousel-3.jpg', link: '/products?category=luxury' }
  ];
  currentSlide = 0;


  constructor(
    private productService: ProductService,
    private cartService: CartService,
    private router: Router,
    public loadingService: LoadingService
  ) {
    this.isLoading$ = this.loadingService.isLoading$;
  }

  ngOnInit(): void {
    // Fetch a few products for "Featured" - e.g., first 4-8 products
    this.featuredProducts$ = this.productService.getProducts(1, 4).pipe(
      map(paginatedResult => paginatedResult.items || []),
      catchError(() => of([])) // Handle error gracefully
    );

    // Fetch a few products for "Latest" - e.g., page 2, or sort by date if API supports
    this.latestProducts$ = this.productService.getProducts(1, 8).pipe( // Example: 8 latest
      map(paginatedResult => paginatedResult.items || []),
      catchError(() => of([]))
    );

    // Auto-play carousel
    setInterval(() => {
        this.nextSlide();
    }, 5000); // Change slide every 5 seconds
  }

  onAddToCart(product: Product): void {
    this.cartService.addItem(product, 1).subscribe();
  }

  onViewProductDetails(product: Product): void {
    this.router.navigate(['/products', product.productId]);
  }

  // Basic Carousel Logic
  nextSlide(): void {
    this.currentSlide = (this.currentSlide + 1) % this.carouselItems.length;
  }

  prevSlide(): void {
    this.currentSlide = (this.currentSlide - 1 + this.carouselItems.length) % this.carouselItems.length;
  }

  goToSlide(index: number): void {
    this.currentSlide = index;
  }
}
```

**`src/app/features/home/home.component.html`:**
```html
<div class="home-page">
  <!-- Hero Section / Carousel -->
  <section class="hero-section">
    <div class="carousel">
      <div class="carousel-inner">
        <div *ngFor="let item of carouselItems; let i = index"
             class="carousel-item"
             [class.active]="i === currentSlide"
             [style.background-image]="'url(' + item.imageUrl + ')'">
          <div class="carousel-caption container">
            <h1>{{ item.title }}</h1>
            <p>{{ item.subtitle }}</p>
            <a [routerLink]="item.link" class="btn btn-primary btn-lg">Shop Now</a>
          </div>
        </div>
      </div>
      <button class="carousel-control prev" (click)="prevSlide()">&#10094;</button>
      <button class="carousel-control next" (click)="nextSlide()">&#10095;</button>
      <div class="carousel-indicators">
        <span *ngFor="let item of carouselItems; let i = index"
              [class.active]="i === currentSlide"
              (click)="goToSlide(i)"></span>
      </div>
    </div>
  </section>

  <!-- Featured Items Section -->
  <section class="featured-products-section container py-5">
    <h2 class="section-title">Featured Products</h2>
    <div *ngIf="(isLoading$ | async) && !(featuredProducts$ | async)?.length" class="text-center">Loading...</div>
    <div *ngIf="!(isLoading$ | async) && !(featuredProducts$ | async)?.length" class="text-center text-secondary">No featured products available at the moment.</div>

    <div class="product-grid" *ngIf="(featuredProducts$ | async) as products">
      <div *ngFor="let product of products" class="product-grid-item">
        <app-product-card
          [product]="product"
          (addToCart)="onAddToCart($event)"
          (viewDetails)="onViewProductDetails($event)">
        </app-product-card>
      </div>
    </div>
  </section>

  <!-- Call to Action / Banner -->
  <section class="cta-banner my-5">
    <div class="container text-center">
      <h3>Discover Your Unique Style</h3>
      <p>Explore our exclusive collections and find pieces that resonate with you.</p>
      <a routerLink="/products" class="btn btn-outline-light btn-lg">Explore Collections</a>
    </div>
  </section>

  <!-- Latest or Popular Products Section -->
  <section class="latest-products-section container py-5">
    <h2 class="section-title">Latest Arrivals</h2>
    <div *ngIf="(isLoading$ | async) && !(latestProducts$ | async)?.length" class="text-center">Loading...</div>
    <div *ngIf="!(isLoading$ | async) && !(latestProducts$ | async)?.length" class="text-center text-secondary">No new products to show right now.</div>

    <div class="product-grid" *ngIf="(latestProducts$ | async) as products">
      <div *ngFor="let product of products" class="product-grid-item">
        <app-product-card
          [product]="product"
          (addToCart)="onAddToCart($event)"
          (viewDetails)="onViewProductDetails($event)">
        </app-product-card>
      </div>
    </div>
    <div class="text-center mt-4" *ngIf="(latestProducts$ | async)?.length">
        <a routerLink="/products" class="btn btn-outline-dark">View All Products</a>
    </div>
  </section>

  <!-- Category Links (Optional) -->
  <!-- <section class="category-showcase-section container py-5"> ... </section> -->

</div>
```

**`src/app/features/home/home.component.scss`:**
```scss
@import 'assets/styles/variables';

.home-page {
  // General styling for the home page if needed
}

.hero-section {
  .carousel {
    position: relative;
    width: 100%;
    height: 70vh; // Adjust height as needed, or use aspect-ratio
    min-height: 400px;
    max-height: 600px;
    overflow: hidden;
    background-color: $accent-rich-black; // Fallback for images

    .carousel-inner {
      position: relative;
      width: 100%;
      height: 100%;
    }

    .carousel-item {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-size: cover;
      background-position: center center;
      opacity: 0;
      transition: opacity 1s ease-in-out; // Smooth fade transition
      display: flex; // For caption alignment
      align-items: center;
      justify-content: center;

      &.active {
        opacity: 1;
        z-index: 1;
      }

      &::before { // Dark overlay for text readability
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-color: rgba($primary-black, 0.4);
      }
    }

    .carousel-caption {
      position: relative; // To be above the overlay
      z-index: 2;
      text-align: center;
      color: $primary-white;

      h1 {
        font-size: $font-size-xxl * 1.5;
        font-weight: $font-weight-bold;
        color: $primary-white;
        margin-bottom: $space-md;
        text-shadow: 1px 1px 3px rgba($primary-black, 0.5);
      }
      p {
        font-size: $font-size-lg;
        margin-bottom: $space-lg;
        color: $primary-white;
      }
      .btn-primary { // Gold button from variables
        padding: $space-sm $space-xl;
        font-size: $font-size-lg;
      }
    }

    .carousel-control {
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      z-index: 3;
      background-color: rgba($primary-black, 0.3);
      color: $primary-white;
      border: none;
      padding: $space-sm $space-xs;
      cursor: pointer;
      font-size: $font-size-xl;
      border-radius: $border-radius-sm;
      transition: background-color 0.2s ease;

      &:hover {
        background-color: rgba($primary-black, 0.6);
      }
      &.prev { left: $space-md; }
      &.next { right: $space-md; }
    }

    .carousel-indicators {
      position: absolute;
      bottom: $space-md;
      left: 50%;
      transform: translateX(-50%);
      z-index: 3;
      display: flex;

      span {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background-color: rgba($primary-white, 0.5);
        margin: 0 $space-xs / 2;
        cursor: pointer;
        transition: background-color 0.2s ease;

        &.active, &:hover {
          background-color: $primary-white;
        }
      }
    }
  }
}

.section-title {
  text-align: center;
  font-size: $font-size-xl * 1.2;
  margin-bottom: $space-xl;
  font-weight: $font-weight-bold;
  color: $accent-rich-black;
  position: relative;
  padding-bottom: $space-sm;

  // Simple underline accent
  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 3px;
    background-color: $primary-gold;
  }
}

// Re-use product grid from product-list styles if globalized, or copy here
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: $space-lg;
  @media (max-width: $breakpoint-sm) {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); // Smaller cards on mobile for home
    gap: $space-md;
  }
}

.cta-banner {
  background-color: $accent-rich-black; // Dark accent background
  color: $primary-white;
  padding: $space-xxl 0;
  background-image: url('assets/images/cta-background.jpg'); // Optional subtle background pattern
  background-size: cover;
  background-position: center;

  h3 {
    font-size: $font-size-xl * 1.3;
    color: $primary-white;
    margin-bottom: $space-sm;
  }
  p {
    font-size: $font-size-lg;
    color: $secondary-gray; // Lighter text on dark bg
    margin-bottom: $space-lg;
  }
  .btn-outline-light {
    border-color: $primary-gold;
    color: $primary-gold;
    &:hover {
      background-color: $primary-gold;
      color: $primary-black;
    }
  }
}
```
*Carousel images:* Add `carousel-1.jpg`, `carousel-2.jpg`, `carousel-3.jpg`, and `cta-background.jpg` to `src/assets/images/`. These are placeholders.

---

**14. Cart Page (Structure)**

**`src/app/features/cart/cart-routing.module.ts`:**
```typescript
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CartComponent } from './cart.component';

const routes: Routes = [{ path: '', component: CartComponent }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CartRoutingModule { }
```

**`src/app/features/cart/cart.module.ts`:**
```typescript
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../../shared/shared.module';
import { CartRoutingModule } from './cart-routing.module';
import { CartComponent } from './cart.component';

@NgModule({
  declarations: [CartComponent],
  imports: [
    CommonModule,
    SharedModule, // For FormsModule if used, pipes etc.
    CartRoutingModule
  ]
})
export class CartModule { }
```

**`src/app/features/cart/cart.component.ts`:**
```typescript
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';
import { CartService } from '../../core/services/cart.service';
import { Cart, CartItem } from '../../core/models/cart.model';
import { LoadingService } from '../../core/services/loading.service';

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.scss']
})
export class CartComponent implements OnInit {
  cart$: Observable<Cart | null>;
  isLoading$: Observable<boolean>;

  defaultImageUrl = 'assets/images/product-placeholder.png';

  constructor(
    private cartService: CartService,
    public loadingService: LoadingService,
    private router: Router
  ) {
    this.cart$ = this.cartService.cart$;
    this.isLoading$ = this.loadingService.isLoading$;
  }

  ngOnInit(): void {
    // Cart is loaded by CartService on auth change or init
  }

  updateQuantity(item: CartItem, newQuantity: number): void {
    if (newQuantity < 1) {
      // Optionally ask for confirmation before removing if quantity becomes 0
      this.removeItem(item.productId);
      return;
    }
    this.cartService.updateItemQuantity(item.productId, newQuantity).subscribe();
  }

  incrementQuantity(item: CartItem): void {
    this.updateQuantity(item, item.quantity + 1);
  }

  decrementQuantity(item: CartItem): void {
    this.updateQuantity(item, item.quantity - 1);
  }

  removeItem(productId: number): void {
    // Optionally, add a confirmation dialog here
    this.cartService.removeItem(productId).subscribe();
  }

  calculateSubtotal(cart: Cart | null): number {
    if (!cart || !cart.items) return 0;
    return cart.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  }

  // You can add more complex calculations like tax, shipping, total
  // For now, subtotal is the total.

  proceedToCheckout(): void {
    this.router.navigate(['/checkout']);
  }

  getImageUrl(item: CartItem): string {
    if (item.imageUrl) {
       if (item.imageUrl.startsWith('http')) {
            return item.imageUrl;
        }
        return item.imageUrl; // Assuming full URL or correctly relative
    }
    return this.defaultImageUrl;
  }
}
```

**`src/app/features/cart/cart.component.html`:**
```html
<div class="cart-page container py-5">
  <header class="page-header">
    <h1>Your Shopping Cart</h1>
  </header>

  <div *ngIf="isLoading$ | async" class="loading-indicator text-center my-5">
    <p>Loading your cart...</p>
  </div>

  <ng-container *ngIf="(cart$ | async) as cart; else emptyCartOrLoading">
    <div *ngIf="cart && cart.items && cart.items.length > 0; else emptyCartTemplate" class="cart-content">
      <div class="row">
        <!-- Cart Items List -->
        <div class="col-lg-8">
          <div class="cart-items-list">
            <div *ngFor="let item of cart.items" class="cart-item card mb-3">
              <div class="card-body">
                <div class="row align-items-center">
                  <div class="col-3 col-md-2">
                    <img [src]="getImageUrl(item)" [alt]="item.productName" class="img-fluid rounded cart-item-image">
                  </div>
                  <div class="col-9 col-md-4">
                    <h5 class="item-name mb-1">{{ item.productName }}</h5>
                    <p class="item-price text-secondary mb-0">{{ item.price | currency:'USD' }} / unit</p>
                  </div>
                  <div class="col-6 col-md-3 mt-2 mt-md-0">
                    <div class="input-group quantity-control">
                      <button class="btn btn-outline-dark btn-sm" type="button" (click)="decrementQuantity(item)">-</button>
                      <input type="number" class="form-control text-center" [value]="item.quantity" readonly>
                      <button class="btn btn-outline-dark btn-sm" type="button" (click)="incrementQuantity(item)">+</button>
                    </div>
                  </div>
                  <div class="col-4 col-md-2 mt-2 mt-md-0 text-md-end">
                    <span class="item-total-price fw-bold">{{ (item.price * item.quantity) | currency:'USD' }}</span>
                  </div>
                  <div class="col-2 col-md-1 mt-2 mt-md-0 text-end">
                    <button class="btn btn-link text-danger p-0" (click)="removeItem(item.productId)" title="Remove item">
                      <!-- SVG Trash Icon -->
                      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Cart Summary -->
        <div class="col-lg-4">
          <div class="cart-summary card sticky-top" style="top: 100px;"> <!-- Adjust top for sticky header -->
            <div class="card-body">
              <h4 class="card-title mb-4">Order Summary</h4>
              <div class="summary-item d-flex justify-content-between mb-2">
                <span>Subtotal</span>
                <span class="fw-bold">{{ calculateSubtotal(cart) | currency:'USD' }}</span>
              </div>
              <!-- <div class="summary-item d-flex justify-content-between mb-2">
                <span>Shipping</span>
                <span class="text-secondary">Calculated at checkout</span>
              </div>
              <div class="summary-item d-flex justify-content-between mb-3">
                <span>Tax</span>
                <span class="text-secondary">Calculated at checkout</span>
              </div> -->
              <hr>
              <div class="summary-item d-flex justify-content-between fw-bold h5 mt-3">
                <span>Total</span>
                <span>{{ calculateSubtotal(cart) | currency:'USD' }}</span>
              </div>
              <button class="btn btn-primary w-100 mt-4 btn-lg" (click)="proceedToCheckout()">
                Proceed to Checkout
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </ng-container>

  <ng-template #emptyCartOrLoading>
    <div *ngIf="!(isLoading$ | async)"> <!-- Only show empty cart if not loading -->
      <ng-container *ngTemplateOutlet="emptyCartTemplate"></ng-container>
    </div>
  </ng-template>

  <ng-template #emptyCartTemplate>
    <div class="empty-cart text-center my-5 py-5">
      <img src="assets/icons/cart.svg" alt="Empty cart" style="width: 80px; opacity: 0.5; margin-bottom: 1rem;">
      <h3>Your Cart is Empty</h3>
      <p class="text-secondary">Looks like you haven't added anything to your cart yet.</p>
      <a routerLink="/products" class="btn btn-primary mt-3">Start Shopping</a>
    </div>
  </ng-template>
</div>
```

**`src/app/features/cart/cart.component.scss`:**
```scss
@import 'assets/styles/variables';

.cart-page {
  .page-header {
    text-align: center;
    margin-bottom: $space-xl;
  }
}

.cart-item {
  .cart-item-image {
    max-width: 80px;
    height: auto;
    aspect-ratio: 1/1;
    object-fit: cover;
  }
  .item-name {
    font-size: $font-size-base;
    font-weight: $font-weight-bold;
  }
  .item-price {
    font-size: $font-size-sm;
  }
  .quantity-control {
    max-width: 120px;
    .form-control {
      border-left: none;
      border-right: none;
      padding-left: $space-xs;
      padding-right: $space-xs;
      &:focus { box-shadow: none; }
    }
    .btn {
      border-color: $light-gray-border;
      &:hover { background-color: $background-light; }
    }
  }
  .item-total-price {
    font-size: $font-size-base;
  }
}

.cart-summary {
  .card-title {
    font-weight: $font-weight-bold;
  }
  .summary-item span:first-child {
    color: $secondary-gray;
  }
}

.empty-cart {
  min-height: 40vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
```

---

**15. Checkout Page (Structure & Stripe Intent)**

**`src/app/features/checkout/checkout-routing.module.ts`:**
```typescript
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CheckoutComponent } from './checkout.component';

const routes: Routes = [{ path: '', component: CheckoutComponent }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CheckoutRoutingModule { }
```

**`src/app/features/checkout/checkout.module.ts`:**
```typescript
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../../shared/shared.module';
import { CheckoutRoutingModule } from './checkout-routing.module';
import { CheckoutComponent } from './checkout.component';

@NgModule({
  declarations: [CheckoutComponent],
  imports: [
    CommonModule,
    SharedModule, // For ReactiveFormsModule
    CheckoutRoutingModule
  ]
})
export class CheckoutModule { }
```

**`src/app/features/checkout/checkout.component.ts`:**
```typescript
import { Component, OnInit, OnDestroy, ViewChild, ElementRef } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Observable, Subscription, of } from 'rxjs';
import { switchMap, filter, tap } from 'rxjs/operators';
import { loadStripe, Stripe, StripeElements, StripeCardElement } from '@stripe/stripe-js';

import { CartService } from '../../core/services/cart.service';
import { OrderService } from '../../core/services/order.service';
import { AuthService } from '../../core/services/auth.service';
import { NotificationService } from '../../core/services/notification.service';
import { LoadingService } from '../../core/services/loading.service';
import { Cart, CartItem } from '../../core/models/cart.model';
import { User } from '../../core/models/user.model';
import { environment } from '../../../environments/environment'; // If you store Stripe PK here

@Component({
  selector: 'app-checkout',
  templateUrl: './checkout.component.html',
  styleUrls: ['./checkout.component.scss']
})
export class CheckoutComponent implements OnInit, OnDestroy {
  @ViewChild('cardElement') cardElementRef!: ElementRef;

  checkoutForm!: FormGroup;
  cart$: Observable<Cart | null>;
  currentUser$: Observable<User | null>;
  isLoading$: Observable<boolean>;

  stripe: Stripe | null = null;
  cardElement!: StripeCardElement; // To be initialized by Stripe.js
  clientSecret: string | null = null;
  isPaymentProcessing = false;

  private subscriptions = new Subscription();

  // Replace with your actual Stripe Publishable Key
  stripePublishableKey = 'pk_test_YOUR_STRIPE_PUBLISHABLE_KEY'; // Get from environment ideally

  constructor(
    private fb: FormBuilder,
    private cartService: CartService,
    private orderService: OrderService,
    private authService: AuthService,
    private notificationService: NotificationService,
    public loadingService: LoadingService,
    private router: Router
  ) {
    this.cart$ = this.cartService.cart$;
    this.currentUser$ = this.authService.currentUser;
    this.isLoading$ = this.loadingService.isLoading$;
  }

  async ngOnInit(): Promise<void> {
    this.checkoutForm = this.fb.group({
      // Basic address fields, expand as needed
      name: ['', Validators.required],
      addressLine1: ['', Validators.required],
      city: ['', Validators.required],
      postalCode: ['', Validators.required],
      country: ['US', Validators.required], // Default or dynamic
      // Add more fields: email (prefill), phone
    });

    // Pre-fill form if user data is available
    const userSub = this.currentUser$.subscribe(user => {
      if (user) {
        this.checkoutForm.patchValue({ name: user.displayName });
      }
    });
    this.subscriptions.add(userSub);

    // Load Stripe and initialize elements
    this.stripe = await loadStripe(this.stripePublishableKey);
    if (this.stripe) {
      const elements = this.stripe.elements();
      this.cardElement = elements.create('card', {
        style: { // Basic styling, customize as needed
          base: {
            iconColor: '#000000', // Black
            color: '#000000',
            fontWeight: '500',
            fontFamily: 'Roboto, Open Sans, Segoe UI, sans-serif',
            fontSize: '16px',
            fontSmoothing: 'antialiased',
            ':-webkit-autofill': {
              color: '#fce883',
            },
            '::placeholder': {
              color: '#B0B0B0', // Gray
            },
          },
          invalid: {
            iconColor: '#F44336', // Error color
            color: '#F44336',
          },
        }
      });
      // Defer mounting until cardElementRef is available (after view init)
    } else {
      this.notificationService.error('Stripe could not be loaded. Please try refreshing.', 'Payment Error');
    }

    // Get Payment Intent Client Secret
    const intentSub = this.orderService.createPaymentIntent().pipe(
      filter(response => !!response && !!response.clientSecret)
    ).subscribe(response => {
      if (response) this.clientSecret = response.clientSecret;
    });
    this.subscriptions.add(intentSub);
  }

  ngAfterViewInit(): void {
    if (this.cardElement && this.cardElementRef) {
      this.cardElement.mount(this.cardElementRef.nativeElement);
      this.cardElement.on('change', (event) => {
        // Handle card validation errors display
        const displayError = document.getElementById('card-errors');
        if (displayError) {
            if (event.error) {
                displayError.textContent = event.error.message || 'Card details are invalid.';
            } else {
                displayError.textContent = '';
            }
        }
      });
    }
  }


  async onSubmitPayment(): Promise<void> {
    if (this.checkoutForm.invalid || !this.stripe || !this.cardElement || !this.clientSecret) {
      this.notificationService.warning('Please fill all required fields and ensure card details are correct.', 'Form Incomplete');
      Object.values(this.checkoutForm.controls).forEach(control => control.markAsTouched());
      // Trigger Stripe element validation visually if possible
      return;
    }

    this.isPaymentProcessing = true;
    this.loadingService.show(); // Show global loader as well

    const { error, paymentIntent } = await this.stripe.confirmCardPayment(this.clientSecret, {
      payment_method: {
        card: this.cardElement,
        billing_details: {
          name: this.checkoutForm.value.name,
          address: { // Collect more address details if needed by Stripe/your business
            line1: this.checkoutForm.value.addressLine1,
            city: this.checkoutForm.value.city,
            postal_code: this.checkoutForm.value.postalCode,
            country: this.checkoutForm.value.country,
          },
          // email: this.authService.currentUserValue?.email // If email is collected
        },
      },
    });

    this.isPaymentProcessing = false;
    this.loadingService.hide();

    if (error) {
      this.notificationService.error(error.message || 'Payment failed. Please try again.', 'Payment Error');
      console.error('Stripe Error:', error);
    } else if (paymentIntent && paymentIntent.status === 'succeeded') {
      this.notificationService.success('Payment successful! Your order is confirmed.', 'Order Placed');
      // TODO: Call your backend to finalize the order (e.g. save transaction details, update inventory)
      // This is often handled by a Stripe Webhook on your backend based on payment_intent.succeeded event.
      this.cartService.clearCartAfterOrder().subscribe(() => {
        this.router.navigate(['/profile/orders'], { queryParams: { success: true, orderId: paymentIntent.id }}); // Or a dedicated success page
      });
    } else if (paymentIntent) {
        this.notificationService.warning(`Payment status: ${paymentIntent.status}. Please contact support.`, 'Payment Pending');
    }
  }

  calculateSubtotal(cart: Cart | null): number {
    if (!cart || !cart.items) return 0;
    return cart.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  }

  ngOnDestroy(): void {
    this.subscriptions.unsubscribe();
    if (this.cardElement) {
      this.cardElement.destroy();
    }
  }
}
```

**`src/app/features/checkout/checkout.component.html`:**
```html
<div class="checkout-page container py-5">
  <header class="page-header text-center mb-5">
    <h1>Checkout</h1>
    <p class="text-secondary">Almost there! Please complete your order details.</p>
  </header>

  <div class="row g-5">
    <!-- Order Summary (Mobile First - or on right for Desktop) -->
    <div class="col-md-5 col-lg-4 order-md-last">
      <h4 class="d-flex justify-content-between align-items-center mb-3">
        <span class="text-gold">Your Cart</span>
        <span class="badge bg-dark rounded-pill">{{ (cart$ | async)?.items?.length || 0 }}</span>
      </h4>
      <ul class="list-group mb-3" *ngIf="(cart$ | async) as cart">
        <li *ngFor="let item of cart.items" class="list-group-item d-flex justify-content-between lh-sm">
          <div>
            <h6 class="my-0">{{ item.productName }} <small class="text-muted">x {{item.quantity}}</small></h6>
            <small class="text-muted">{{ item.description | slice:0:50 }}...</small>
          </div>
          <span class="text-muted">{{ (item.price * item.quantity) | currency:'USD' }}</span>
        </li>
        <li class="list-group-item d-flex justify-content-between bg-light">
          <div class="text-success">
            <!-- <h6 class="my-0">Promo code</h6>
            <small>EXAMPLECODE</small> -->
          </div>
          <!-- <span class="text-success">−$5</span> -->
        </li>
        <li class="list-group-item d-flex justify-content-between">
          <span>Total (USD)</span>
          <strong>{{ calculateSubtotal(cart) | currency:'USD' }}</strong>
        </li>
      </ul>
      <!-- Promo Code Form (Optional) -->
    </div>

    <!-- Billing/Shipping and Payment Form -->
    <div class="col-md-7 col-lg-8">
      <h4 class="mb-3">Billing Address</h4>
      <form [formGroup]="checkoutForm" (ngSubmit)="onSubmitPayment()" novalidate class="needs-validation">
        <div class="row g-3">
          <div class="col-12">
            <label for="name" class="form-label">Full name</label>
            <input type="text" class="form-control" id="name" formControlName="name" placeholder="John M. Doe" required>
            <div *ngIf="checkoutForm.get('name')?.invalid && checkoutForm.get('name')?.touched" class="form-error-message">
              Full name is required.
            </div>
          </div>

          <!-- Add Email and Phone inputs here if needed for Stripe or your records -->

          <div class="col-12">
            <label for="addressLine1" class="form-label">Address</label>
            <input type="text" class="form-control" id="addressLine1" formControlName="addressLine1" placeholder="1234 Main St" required>
             <div *ngIf="checkoutForm.get('addressLine1')?.invalid && checkoutForm.get('addressLine1')?.touched" class="form-error-message">
              Address is required.
            </div>
          </div>

          <!-- Address Line 2 (Optional) -->

          <div class="col-md-5">
            <label for="country" class="form-label">Country</label>
            <select class="form-select form-control" id="country" formControlName="country" required>
              <option value="US">United States</option>
              <!-- Add more countries -->
            </select>
            <div *ngIf="checkoutForm.get('country')?.invalid && checkoutForm.get('country')?.touched" class="form-error-message">
              Please select a valid country.
            </div>
          </div>

          <div class="col-md-4">
            <label for="city" class="form-label">City</label> <!-- Or State/Province -->
            <input type="text" class="form-control" id="city" formControlName="city" placeholder="Your City" required>
            <div *ngIf="checkoutForm.get('city')?.invalid && checkoutForm.get('city')?.touched" class="form-error-message">
              City is required.
            </div>
          </div>

          <div class="col-md-3">
            <label for="postalCode" class="form-label">Zip / Postal code</label>
            <input type="text" class="form-control" id="postalCode" formControlName="postalCode" placeholder="" required>
             <div *ngIf="checkoutForm.get('postalCode')?.invalid && checkoutForm.get('postalCode')?.touched" class="form-error-message">
              Zip code required.
            </div>
          </div>
        </div>

        <hr class="my-4">

        <!-- Shipping address same as billing checkbox -->
        <!-- <div class="form-check"> ... </div> -->

        <h4 class="mb-3">Payment</h4>

        <!-- Stripe Card Element will be injected here -->
        <div class="form-group">
          <label for="card-element" class="form-label">Credit or debit card</label>
          <div id="card-element" #cardElement class="form-control stripe-card-element">
            <!-- A Stripe Element will be inserted here. -->
          </div>
          <!-- Used to display form errors. -->
          <div id="card-errors" role="alert" class="form-error-message mt-2"></div>
        </div>

        <hr class="my-4">

        <button class="w-100 btn btn-primary btn-lg" type="submit" [disabled]="isPaymentProcessing || !clientSecret || (isLoading$ | async)">
          <span *ngIf="isPaymentProcessing">Processing Payment...</span>
          <span *ngIf="!isPaymentProcessing">Pay {{ (cart$ | async)?.items ? (calculateSubtotal(cart$ | async) | currency:'USD') : '' }}</span>
        </button>
        <p *ngIf="!clientSecret && !(isLoading$ | async)" class="text-danger mt-2 text-center">
            Could not initialize payment. Please try refreshing the page or contact support.
        </p>
      </form>
    </div>
  </div>

  <div *ngIf="(isLoading$ | async) && !isPaymentProcessing" class="loading-overlay">
      <p>Loading checkout details...</p> <!-- Or a spinner -->
  </div>
</div>
```

**`src/app/features/checkout/checkout.component.scss`:**
```scss
@import 'assets/styles/variables';

.checkout-page {
  .list-group-item {
    border-left: none;
    border-right: none;
    padding-left: 0;
    padding-right: 0;
    &:first-child { border-top: none; }
    &:last-child { border-bottom: none; }
  }

  .stripe-card-element {
    padding: $space-sm; // Match other form controls
    border: $border-width solid $light-gray-border;
    border-radius: $border-radius-sm;
    background-color: $primary-white;
  }

  .form-error-message { // Already defined globally, but can be tweaked
    color: $error-color;
    font-size: $font-size-sm;
  }

  .loading-overlay { // For when loading initial checkout details
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: rgba($primary-white, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1050; // Above most content
    p { font-size: $font-size-lg; color: $primary-black; }
  }
}
```
*Stripe Key:* Remember to replace `'pk_test_YOUR_STRIPE_PUBLISHABLE_KEY'` with your actual Stripe publishable key. It's best practice to load this from `environment.ts`.

---

**16. User Profile Page (Structure)**

**`src/app/features/profile/profile-routing.module.ts`:**
```typescript
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { UserProfileComponent } from './user-profile/user-profile.component';
import { OrderHistoryComponent } from './order-history/order-history.component'; // Create this

const routes: Routes = [
  {
    path: '',
    component: UserProfileComponent,
    children: [ // Optional: Child routes for different profile sections
      { path: 'orders', component: OrderHistoryComponent },
      // { path: 'settings', component: ProfileSettingsComponent },
      { path: '', redirectTo: 'orders', pathMatch: 'full' } // Default to orders or a dashboard
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProfileRoutingModule { }
```

**`src/app/features/profile/profile.module.ts`:**
```typescript
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../../shared/shared.module';
import { ProfileRoutingModule } from './profile-routing.module';
import { UserProfileComponent } from './user-profile/user-profile.component';
import { OrderHistoryComponent } from './order-history/order-history.component';

@NgModule({
  declarations: [
    UserProfileComponent,
    OrderHistoryComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    ProfileRoutingModule
  ]
})
export class ProfileModule { }
```

**`src/app/features/profile/user-profile/user-profile.component.ts`:**
```typescript
import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../../core/services/auth.service';
import { User } from '../../../core/models/user.model';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.scss']
})
export class UserProfileComponent implements OnInit {
  currentUser$: Observable<User | null>;

  constructor(private authService: AuthService) {
    this.currentUser$ = this.authService.currentUser;
  }

  ngOnInit(): void {
    // Optionally, fetch fresh user info if it can change frequently
    // this.authService.fetchAndUpdateUserInfo().subscribe();
  }
}
```

**`src/app/features/profile/user-profile/user-profile.component.html`:**
```html
<div class="profile-page container py-5">
  <div class="row">
    <div class="col-md-3">
      <!-- Profile Sidebar Navigation -->
      <div class="profile-sidebar card sticky-top" style="top: 100px;">
        <div class="card-body p-0">
          <div *ngIf="currentUser$ | async as user" class="profile-user-info text-center p-3 border-bottom">
            <!-- Add user avatar here -->
            <h5 class="mt-2 mb-0">{{ user.displayName }}</h5>
            <p class="text-secondary mb-0"><small>{{ user.email }}</small></p>
          </div>
          <nav class="nav flex-column profile-nav">
            <a class="nav-link" routerLink="orders" routerLinkActive="active">
              <!-- Icon --> Order History
            </a>
            <a class="nav-link" routerLink="settings" routerLinkActive="active">
              <!-- Icon --> Account Settings
            </a>
            <!-- Add more links: Addresses, Payment Methods, etc. -->
            <a class="nav-link text-danger" (click)="authService.logout()">
              <!-- Icon --> Logout
            </a>
          </nav>
        </div>
      </div>
    </div>
    <div class="col-md-9">
      <!-- Profile Content Area -->
      <div class="profile-content">
        <router-outlet></router-outlet>
      </div>
    </div>
  </div>
</div>
```

**`src/app/features/profile/user-profile/user-profile.component.scss`:**
```scss
@import 'assets/styles/variables';

.profile-sidebar {
  .profile-user-info {
    // Styles for avatar, name, email display
  }
  .profile-nav {
    .nav-link {
      color: $primary-black;
      padding: $space-sm $space-md;
      border-bottom: 1px solid $light-gray-border;
      font-weight: $font-weight-normal;

      &:last-child {
        border-bottom: none;
      }

      &:hover {
        background-color: $background-light;
      }
      &.active {
        background-color: lighten($primary-gold, 30%);
        color: darken($primary-gold, 15%);
        font-weight: $font-weight-bold;
        border-left: 3px solid $primary-gold; // Active indicator
      }
      &.text-danger:hover {
          background-color: lighten($error-color, 35%);
      }
    }
  }
}

.profile-content {
  // Styles for the content area (e.g., card for each section)
}
```

**`src/app/features/profile/order-history/order-history.component.ts` (Structure):**
```typescript
import { Component, OnInit } from '@angular/core';
import { Observable, of } from 'rxjs';
import { OrderService } from '../../../core/services/order.service';
import { LoadingService } from '../../../core/services/loading.service';
import { OrderHistoryItem } from '../../../core/models/order.model';

@Component({
  selector: 'app-order-history',
  templateUrl: './order-history.component.html',
  styleUrls: ['./order-history.component.scss']
})
export class OrderHistoryComponent implements OnInit {
  orderHistory$: Observable<OrderHistoryItem[]> = of([]);
  isLoading$: Observable<boolean>;

  constructor(
    private orderService: OrderService,
    public loadingService: LoadingService
  ) {
    this.isLoading$ = this.loadingService.isLoading$;
  }

  ngOnInit(): void {
    this.orderHistory$ = this.orderService.getOrderHistory();
  }

  // Method to view order details if you have a dedicated order detail page
  viewOrderDetails(orderId: string): void {
    // this.router.navigate(['/profile/orders', orderId]);
    console.log('View details for order:', orderId);
  }
}
```

**`src/app/features/profile/order-history/order-history.component.html` (Structure):**
```html
<div class="order-history-section card">
  <div class="card-header bg-transparent">
    <h4 class="mb-0">Your Orders</h4>
  </div>
  <div class="card-body">
    <div *ngIf="isLoading$ | async" class="text-center py-5">
      <p>Loading order history...</p>
      <!-- <app-loading-spinner></app-loading-spinner> -->
    </div>

    <div *ngIf="!(isLoading$ | async) && (orderHistory$ | async) as orders">
      <div *ngIf="orders.length === 0" class="text-center py-5 text-secondary">
        <p>You haven't placed any orders yet.</p>
        <a routerLink="/products" class="btn btn-primary">Start Shopping</a>
      </div>

      <div *ngIf="orders.length > 0" class="orders-list">
        <div *ngFor="let order of orders" class="order-item card mb-3">
          <div class="card-header d-flex justify-content-between align-items-center bg-light">
            <div>
              <span class="fw-bold">Order #{{ order.orderId }}</span>
              <small class="ms-2 text-muted">Placed on: {{ order.orderDate | date:'mediumDate' }}</small>
            </div>
            <span class="badge" [ngClass]="{'bg-success': order.status === 'Delivered', 'bg-warning text-dark': order.status === 'Processing', 'bg-info text-dark': order.status === 'Shipped', 'bg-secondary': order.status !== 'Delivered' && order.status !== 'Processing' && order.status !== 'Shipped'}">
              {{ order.status }}
            </span>
          </div>
          <div class="card-body">
            <!-- Simple item summary -->
            <div *ngFor="let item of order.items | slice:0:2" class="order-item-summary d-flex align-items-center mb-2">
              <!-- <img [src]="item.imageUrl" [alt]="item.productName" class="me-2" style="width: 40px; height: 40px; object-fit: cover;"> -->
              <p class="mb-0 flex-grow-1">{{ item.productName }} <small class="text-muted">x {{ item.quantity }}</small></p>
              <p class="mb-0 fw-bold">{{ (item.price * item.quantity) | currency:'USD' }}</p>
            </div>
            <p *ngIf="order.items.length > 2" class="text-muted"><small>+ {{ order.items.length - 2 }} more item(s)</small></p>
            <hr>
            <div class="d-flex justify-content-between align-items-center">
              <span class="h5 mb-0">Total: {{ order.totalAmount | currency:'USD' }}</span>
              <button class="btn btn-outline-dark btn-sm" (click)="viewOrderDetails(order.orderId)">
                View Details
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
```
*Order History Styling (`order-history.component.scss`): Add specific styles as needed for order items.*

---

**17. Admin Section (Optional - Basic Structure)**

If you implement admin, it would follow a similar pattern:
`AdminModule`, `AdminRoutingModule`.
Components for `ManageProductsComponent`, `ManageCategoriesComponent`, `ViewOrdersComponent`.
These would use the admin methods in `ProductService`, `CategoryService`, etc.
Protect admin routes with an `AdminGuard` (similar to `AuthGuard` but checks for an 'Admin' role).

---

**Final Recommendations & Next Steps:**

1.  **SVG Icons:** Replace placeholder text/SVG strings with actual SVG icons. Store them in `src/assets/icons/` and use them via `<img>` tags or inline SVGs.
2.  **Images:**
    *   Add your logo (`logo.svg`) to `src/assets/icons/`.
    *   Add placeholder images: `src/assets/images/product-placeholder.png`, `product-placeholder-large.png`, `empty-box.svg`.
    *   Add carousel and CTA banner images.
3.  **Error Handling:** Implement a global `ErrorInterceptor` (similar to `AuthInterceptor`) to catch HTTP errors, log them, and show user-friendly notifications via `NotificationService`.
4.  **Loading States:**
    *   Use `LoadingService` more extensively. You can create a global `app-loading-spinner` component and show it in `app.component.html` based on `loadingService.isLoading$`.
    *   Implement skeleton loaders for product cards and lists for a smoother perceived performance.
5.  **Forms Validation:** Enhance form validation messages and styling.
6.  **Stripe Integration:**
    *   Replace the placeholder Stripe publishable key.
    *   Thoroughly test the Stripe payment flow.
    *   Implement backend webhooks for `payment_intent.succeeded` and other relevant Stripe events to reliably update order status, send emails, etc.
7.  **API Models Refinement:** Double-check all DTOs (`core/models/`) against your actual API responses. The `PaginatedProducts` structure is an assumption; adjust if your API paginates differently (e.g., via Link headers or a different body structure).
8.  **User ID in Cart:** Clarify how `userId` is handled for cart operations with your backend. If it's inferred from the token, `CartRequestDto` might not need `userId`.
9.  **Infinite Scroll vs. Pagination:** For product listings, decide between pagination (implemented) or infinite scroll (requires different logic, e.g., using `ngx-infinite-scroll`).
10. **State Management:** For larger applications, consider NgRx or other state management libraries for more complex states (cart, user session, product filters). For now, `BehaviorSubject` in services is a good start.
11. **Testing:** Add unit tests (Karma/Jasmine) and consider end-to-end tests (Cypress/Protractor).
12. **Accessibility (a11y):** Continuously review for ARIA attributes, keyboard navigation, color contrast, etc.
13. **Responsiveness:** Test thoroughly across devices. The provided SCSS includes breakpoints and basic responsive patterns.
14. **Build & Deploy:** Configure `angular.json` for production builds (`ng build --configuration production`).

This comprehensive structure provides a very solid foundation. You'll need to fill in the details for remaining components (Checkout payment form, Profile sections, Admin, etc.) following these patterns. The design is minimalist and modern, focusing on clarity and comfort. The repository pattern ensures clean separation of concerns.

Good luck with your e-commerce project! It's been a pleasure designing this for you.

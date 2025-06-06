------------------------- _Layout.cshtml -------------------------
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>@ViewData["Title"] - PDF Template Engine</title>

    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="~/lib/bootstrap/dist/css/bootstrap.min.css" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" asp-fallback-href="~/lib/fontawesome-free/css/all.min.css" asp-fallback-test-class="fas" asp-fallback-test-property="font" asp-fallback-test-value="-webkit-pictograph" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <link rel="stylesheet" href="~/css/site.css" asp-append-version="true" />
    <link rel="stylesheet" href="~/PdfGeneratorApp.styles.css" asp-append-version="true" />

    @await RenderSectionAsync("Styles", required: false)
</head>
<body>
    <header>
        <nav class="site-navbar navbar navbar-expand-lg navbar-light">
            <div class="container-fluid">
                <a class="navbar-brand" asp-area="" asp-controller="Home" asp-action="Index">
                    <i class="fas fa-cogs"></i> PDF Engine
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                        <li class="nav-item">
                            <a class="nav-link @(ViewContext.RouteData.Values["controller"]?.ToString() == "Home" ? "active" : "")" asp-area="" asp-controller="Home" asp-action="Index">
                                <i class="fas fa-tachometer-alt fa-fw me-1"></i>Dashboard
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link @(ViewContext.RouteData.Values["controller"]?.ToString() == "Docs" ? "active" : "")" asp-area="" asp-controller="Docs" asp-action="Templates">
                                <i class="fas fa-book fa-fw me-1"></i>API Docs
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </header>

    <div class="main-content">
        @if (TempData["Message"] != null)
        {
            <div class="container mt-3">
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    <i class="fas fa-check-circle me-2"></i> @TempData["Message"]
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            </div>
        }
        @if (TempData["ErrorMessage"] != null)
        {
            <div class="container mt-3">
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i> @TempData["ErrorMessage"]
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            </div>
        }
        @RenderBody()
    </div>

    <footer class="site-footer py-3 mt-5">
        <div class="container text-center">
            © @DateTime.Now.Year - PDF Template Engine by YourCompany
        </div>
    </footer>

    <script src="~/lib/jquery/dist/jquery.min.js"></script>
    <script src="~/lib/bootstrap/dist/js/bootstrap.bundle.min.js"></script>
    <script src="~/js/site.js" asp-append-version="true"></script>
    @await RenderSectionAsync("Scripts", required: false)
</body>
</html>
---------------------------------------------------------------------------

------------------------- site.css -------------------------
:root {
    --primary-color: #00a896; /* Teal from image */
    --accent-color: #e74c3c; /* Red-Orange accent */
    --white: #ffffff;
    --black: #212529; /* A soft black */
    --dark-gray: #343a40; /* Darker gray for text */
    --medium-gray: #ced4da; /* Medium gray for borders/dividers */
    --light-gray: #f8f9fa; /* Very light gray for backgrounds */
    --lighter-gray: #e9ecef; /* Lighter gray */
    --shadow-sm: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    --shadow-md: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

body {
    font-family: 'Cairo', sans-serif;
    background-color: var(--light-gray);
    min-height: 100vh;
    color: var(--dark-gray);
    line-height: 1.6;
    display: flex;
    flex-direction: column;
}

.main-content {
    flex-grow: 1;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem;
}

.site-navbar {
    background-color: var(--white);
    box-shadow: var(--shadow-sm);
    padding-top: 0.75rem;
    padding-bottom: 0.75rem;
}

.navbar-brand {
    color: var(--primary-color) !important;
    font-weight: 700;
    font-size: 1.5rem;
}

.navbar-brand i {
    color: var(--accent-color);
}

.site-navbar .nav-link {
    color: var(--dark-gray) !important;
    font-weight: 600;
    transition: color 0.3s ease;
}

.site-navbar .nav-link:hover,
.site-navbar .nav-link.active {
    color: var(--primary-color) !important;
}

.site-navbar .nav-link.active {
    border-bottom: 2px solid var(--primary-color);
}

.site-footer {
    background-color: var(--dark-gray);
    color: var(--light-gray);
    font-size: 0.9rem;
}

.page-header {
    text-align: center;
    margin-bottom: 3rem;
    padding-top: 1rem;
}

.page-header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--black);
    margin-bottom: 0.5rem;
    position: relative;
    display: inline-block;
}

.page-header h1::after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 60px;
    height: 3px;
    background-color: var(--accent-color);
    border-radius: 2px;
}

.page-subtitle {
    font-size: 1.1rem;
    color: var(--dark-gray);
    max-width: 700px;
    margin: 0.5rem auto 0 auto;
}

.stats-bar {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}

.stat-item {
    text-align: center;
    padding: 1rem 1.5rem;
    background: var(--white);
    border-radius: 12px;
    box-shadow: var(--shadow-sm);
    min-width: 150px;
    border: 1px solid var(--lighter-gray);
}

.stat-number {
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary-color);
    margin-bottom: 0.25rem;
}

.stat-label {
    font-size: 0.9rem;
    color: var(--dark-gray);
}

.action-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    flex-wrap: wrap;
    gap: 1rem;
}

.search-box {
    position: relative;
    flex: 1;
    max-width: 400px;
}

.search-box .form-control {
    width: 100%;
    padding: 0.75rem 1rem 0.75rem 2.5rem;
    border: 1px solid var(--medium-gray);
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.3s ease;
    background-color: var(--white);
    color: var(--dark-gray);
}

.search-box .form-control:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 0.25rem rgba(0, 168, 150, 0.25);
}

.search-box .search-icon {
    position: absolute;
    left: 0.8rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--dark-gray);
}

/* Button Styling Overrides */
.btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.3s ease;
    text-transform: none;
    border: none;
}

.btn-sm {
     padding: 0.5rem 1rem;
     font-size: 0.875rem;
}

.btn-primary {
    background-color: var(--primary-color);
    color: var(--white);
}

.btn-primary:hover {
    background-color: color-mix(in srgb, var(--primary-color) 90%, var(--black));
    color: var(--white);
}

.btn-secondary {
    background-color: var(--medium-gray);
    color: var(--dark-gray);
}

.btn-secondary:hover {
    background-color: color-mix(in srgb, var(--medium-gray) 80%, var(--black));
    color: var(--dark-gray);
}

.btn-success { /* Used in Docs for Execute */
    background-color: var(--primary-color);
    color: var(--white);
}
.btn-success:hover {
    background-color: color-mix(in srgb, var(--primary-color) 90%, var(--black));
    color: var(--white);
}


.btn-info { /* Used in History for History button */
    background-color: var(--medium-gray);
    color: var(--dark-gray);
}
.btn-info:hover {
     background-color: color-mix(in srgb, var(--medium-gray) 80%, var(--black));
     color: var(--dark-gray);
}


.btn-warning { /* Used in History for Revert button */
    background-color: var(--accent-color);
    color: var(--white);
}
.btn-warning:hover {
    background-color: color-mix(in srgb, var(--accent-color) 90%, var(--black));
    color: var(--white);
}


.btn-design { /* Custom button for Design */
    background-color: var(--accent-color);
    color: var(--white);
}

.btn-design:hover {
    background-color: color-mix(in srgb, var(--accent-color) 90%, var(--black));
    color: var(--white);
}

.btn-preview { /* Custom button for Preview */
    background-color: var(--white);
    color: var(--primary-color);
    border: 1px solid var(--primary-color);
}

.btn-preview:hover {
    background-color: var(--primary-color);
    color: var(--white);
}


/* Templates Grid */
.templates-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}

.template-card {
    background: var(--white);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
    transition: all 0.3s ease;
    border: 1px solid var(--lighter-gray);
    display: flex;
    flex-direction: column;
}

.template-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-md);
}

.template-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 1rem;
}

.template-icon {
    width: 48px;
    height: 48px;
    background-color: var(--primary-color);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 1rem;
    flex-shrink: 0;
    color: var(--white);
    font-size: 1.4rem;
}

.template-info {
    flex-grow: 1;
}

.template-name {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--dark-gray);
    margin-bottom: 0.25rem;
}

.template-name a {
    color: inherit;
    text-decoration: none;
}

.template-name a:hover {
    color: var(--primary-color);
}

.template-description {
    color: var(--dark-gray);
    font-size: 0.95rem;
    line-height: 1.5;
    margin-bottom: 1rem;
    word-break: break-word;
}

.template-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 1.5rem;
    font-size: 0.85rem;
    color: var(--dark-gray);
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.meta-item i {
    color: var(--primary-color);
    font-size: 1rem;
}

.template-actions {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-top: auto; /* Push actions to bottom */
}

.version-badge {
    background: var(--lighter-gray);
    color: var(--dark-gray);
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

/* Empty State */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--dark-gray);
    background-color: var(--white);
    border-radius: 12px;
    border: 1px solid var(--lighter-gray);
    box-shadow: var(--shadow-sm);
}

.empty-state i {
    font-size: 4rem;
    color: var(--medium-gray);
    margin-bottom: 1rem;
}

.empty-state h3 {
    color: var(--dark-gray);
    margin-bottom: 0.5rem;
}


/* Form Styling Overrides (Create, Design) */
.form-group label {
    font-weight: 600;
    color: var(--dark-gray);
    margin-bottom: 0.5rem;
}

.form-control {
    border-radius: 8px;
    border: 1px solid var(--medium-gray);
    padding: 0.75rem 1rem;
    font-size: 1rem;
    color: var(--dark-gray);
    background-color: var(--white);
}

.form-control:focus {
     border-color: var(--primary-color);
     box-shadow: 0 0 0 0.25rem rgba(0, 168, 150, 0.25);
}

textarea.form-control {
    min-height: 150px;
}

/* Summernote adjustments */
.note-editor {
    border: 1px solid var(--medium-gray) !important;
    border-radius: 8px !important;
    overflow: hidden;
}

.note-toolbar {
    background-color: var(--light-gray) !important;
    border-bottom: 1px solid var(--medium-gray) !important;
}

.note-editable {
     background-color: var(--white) !important;
     color: var(--dark-gray) !important;
}


/* Table Styling Overrides (History) */
.table {
    width: 100%;
    margin-bottom: 1rem;
    color: var(--dark-gray);
    background-color: var(--white);
    border-collapse: collapse;
    border-radius: 8px;
    overflow: hidden; /* Ensures rounded corners work with borders */
    box-shadow: var(--shadow-sm);
}

.table th,
.table td {
    padding: 0.75rem;
    vertical-align: top;
    border-top: 1px solid var(--medium-gray);
}

.table thead th {
    vertical-align: bottom;
    border-bottom: 2px solid var(--medium-gray);
    background-color: var(--lighter-gray);
    font-weight: 600;
    color: var(--black);
}

.table tbody + tbody {
    border-top: 2px solid var(--medium-gray);
}

.table .table-info {
    background-color: #e0f7fa !important; /* A light tealish background */
    color: var(--dark-gray);
}

.table-container {
    overflow-x: auto; /* Make table responsive */
    border-radius: 8px;
}

/* Actions column alignment */
.actions-column {
    white-space: nowrap; /* Prevent buttons from wrapping */
}


/* Accordion Styling Overrides (Docs) */
.accordion-item {
    border: 1px solid var(--medium-gray);
    margin-bottom: 1rem;
    border-radius: 8px;
    overflow: hidden; /* Ensures rounded corners */
    background-color: var(--white);
}

.accordion-header {
    margin-bottom: 0;
}

.accordion-button {
    background-color: var(--white);
    color: var(--dark-gray);
    font-weight: 600;
    padding: 1rem 1.25rem;
    border: none;
    transition: background-color 0.3s ease, color 0.3s ease;
}

.accordion-button:not(.collapsed) {
    color: var(--primary-color);
    background-color: var(--lighter-gray);
    box-shadow: inset 0 -1px 0 rgba(0, 0, 0, 0.125);
}

.accordion-button:focus {
    border-color: transparent;
    box-shadow: none;
    outline: 0;
}

.accordion-body {
    padding: 1.25rem;
    border-top: 1px solid var(--medium-gray);
    background-color: var(--white);
}

.try-it-out-section h5 {
    color: var(--black);
    margin-bottom: 0.75rem;
}

.try-it-out-section .small {
    color: var(--dark-gray) !important;
}

.response-section {
     margin-top: 1rem;
     padding-top: 1rem;
     border-top: 1px solid var(--medium-gray);
}

.response-section h6 {
    color: var(--black);
    margin-bottom: 0.5rem;
}

.response-status,
.response-output {
    background-color: var(--light-gray);
    border: 1px solid var(--medium-gray);
    border-radius: 4px;
    padding: 0.75rem;
    font-family: monospace;
    font-size: 0.875em;
    white-space: pre-wrap;
    word-wrap: break-word;
    max-height: 300px;
    overflow-y: auto;
}

.response-status {
    font-weight: 600;
}

.response-output {
     min-height: 50px;
}


/* Alerts */
.alert {
    border-radius: 8px;
    padding: 1rem 1.5rem;
    font-size: 1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.alert-success {
    color: #0f5132;
    background-color: #d1e7dd;
    border-color: #badbcc;
}

.alert-danger {
    color: #842029;
    background-color: #f8d7da;
    border-color: #f5c2c7;
}

.alert-warning {
     color: #664d03;
     background-color: #fff3cd;
     border-color: #ffecb5;
}

.alert .btn-close {
    padding: 0.75rem;
    margin: -0.75rem -0.75rem -0.75rem auto;
}


/* Responsiveness */
@media (max-width: 992px) {
     .navbar-collapse {
         background-color: var(--white);
         border-top: 1px solid var(--medium-gray);
         margin-top: 0.5rem;
         padding-bottom: 0.5rem;
     }
     .navbar-nav {
         padding: 0 1rem;
     }
    .site-navbar .nav-link.active {
        border-bottom: none;
        border-left: 3px solid var(--primary-color);
        padding-left: calc(0.5rem + 3px);
    }

    .page-header h1 {
        font-size: 2rem;
    }
    .page-subtitle {
         font-size: 1rem;
    }

    .stats-bar {
        gap: 1rem;
        justify-content: stretch;
    }
    .stat-item {
        flex: 1;
        min-width: unset;
    }

    .action-bar {
        flex-direction: column;
        align-items: stretch;
    }
    .search-box {
        max-width: none;
    }
    .btn {
        width: 100%;
        justify-content: center;
    }
}

@media (max-width: 768px) {
    .templates-grid {
        grid-template-columns: 1fr;
    }

    .template-card {
        padding: 1rem;
    }

    .template-icon {
        width: 40px;
        height: 40px;
        font-size: 1.2rem;
        margin-right: 0.75rem;
    }

     .template-name {
         font-size: 1.2rem;
     }

     .template-description {
         font-size: 0.9rem;
     }

     .template-meta {
         gap: 0.75rem;
         font-size: 0.8rem;
     }
     .meta-item i {
         font-size: 0.9rem;
     }

     .template-actions {
         flex-direction: column;
         gap: 0.5rem;
     }
     .template-actions .btn {
         width: 100%;
     }

     .stat-number {
         font-size: 1.5rem;
     }
     .stat-label {
         font-size: 0.8rem;
     }

     .accordion-button {
         padding: 1rem;
     }
     .accordion-body {
         padding: 1rem;
     }

     .try-it-out-section .form-group label {
         font-size: 0.9rem;
     }

     .form-control {
         padding: 0.6rem 0.8rem;
         font-size: 0.9rem;
     }
     textarea.form-control {
         min-height: 100px;
     }

     .note-editable {
          min-height: 400px !important;
     }

     .table th, .table td {
         padding: 0.6rem;
         font-size: 0.9rem;
     }
     .actions-column .btn {
         font-size: 0.8rem;
         padding: 0.3rem 0.6rem;
     }
}

@media (max-width: 480px) {
    .page-header h1 {
        font-size: 1.8rem;
    }
     .page-subtitle {
         font-size: 0.95rem;
     }

    .stat-item {
        padding: 0.75rem;
    }
     .stat-number {
         font-size: 1.2rem;
     }
     .stat-label {
         font-size: 0.75rem;
     }

    .template-header {
        flex-direction: column;
        align-items: flex-start;
    }
    .template-icon {
        margin-right: 0;
        margin-bottom: 0.75rem;
    }

    .template-meta {
        flex-direction: column;
        gap: 0.5rem;
    }

    .alert {
        padding: 0.75rem;
        font-size: 0.9rem;
    }
    .alert .btn-close {
        padding: 0.5rem;
        margin: -0.5rem -0.5rem -0.5rem auto;
    }

     .response-status,
     .response-output {
         padding: 0.6rem;
         font-size: 0.8em;
     }

     .try-it-out-section .btn {
         width: auto; /* Allow buttons to be side-by-side again if space permits */
         justify-content: center;
     }
     .try-it-out-section .btn-sm {
          width: auto;
     }
}

/* Animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.template-card {
     opacity: 0;
     transform: translateY(20px);
     animation: fadeIn 0.4s ease-out forwards;
}

/* Adjust animation delay in JS */

---------------------------------------------------------------------------

------------------------- Index.cshtml -------------------------
@model IEnumerable<PdfGeneratorApp.Dtos.TemplateListDto>

@{
    ViewData["Title"] = "Templates Dashboard";
    int totalTemplates = Model?.Count() ?? 0;
}

<div class="container">
    <div class="page-header">
        <h1>PDF Templates Dashboard</h1>
        <p class="page-subtitle">Manage and create beautiful PDF templates with ease. Design, test, and deploy your templates in minutes.</p>
    </div>

    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-number" id="totalTemplatesStat">@totalTemplates</div>
            <div class="stat-label">Total Templates</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">N/A</div>
            <div class="stat-label">Generated PDFs</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">N/A</div>
            <div class="stat-label">Active Users</div>
        </div>
    </div>

    <div class="action-bar">
        <div class="search-box">
            <i class="fas fa-search search-icon"></i>
            <input type="text" id="searchInput" placeholder="Search templates by name or description..." class="form-control" />
        </div>
        <a asp-controller="Template" asp-action="Create" class="btn btn-primary">
            <i class="fas fa-plus"></i>
            Create New Template
        </a>
    </div>

    @if (Model != null && Model.Any())
    {
        <div class="templates-grid" id="templatesGrid">
            @foreach (var template in Model)
            {
                <div class="template-card" data-name="@template.Name.ToLower()" data-description="@(template.Description?.ToLower() ?? "")">
                    <div class="template-header">
                        <div class="template-icon">
                            <i class="fas fa-file-alt"></i>
                        </div>
                        <div class="version-badge">
                            <i class="fas fa-tag"></i>
                            v @template.CurrentVersion
                        </div>
                    </div>
                    <div class="template-info">
                        <h3 class="template-name">
                            <a asp-controller="Template" asp-action="Design" asp-route-templateName="@template.Name" title="Edit @template.Name">
                                @template.Name
                            </a>
                        </h3>
                        <p class="template-description" title="@template.Description">@(string.IsNullOrWhiteSpace(template.Description) ? "No description provided." : template.Description)</p>
                        <div class="template-meta">
                            <div class="meta-item">
                                <i class="fas fa-calendar-alt"></i>
                                <span>Modified: @template.LastModified.ToString("MMM dd, yyyy")</span>
                            </div>
                        </div>
                    </div>
                    <div class="template-actions">
                        <a asp-controller="Template" asp-action="Design" asp-route-templateName="@template.Name" class="btn btn-sm btn-design">
                            <i class="fas fa-paint-brush"></i>
                            Design
                        </a>
                        <a asp-controller="Template" asp-action="History" asp-route-templateName="@template.Name" class="btn btn-sm btn-info">
                            <i class="fas fa-history"></i>
                            History
                        </a>
                    </div>
                </div>
            }
        </div>
        <div class="empty-state" id="emptyState" style="display: none;">
            <i class="fas fa-search-minus"></i>
            <h3>No templates match your search</h3>
            <p>Try adjusting your search criteria or create a new template.</p>
        </div>
    }
    else
    {
        <div class="empty-state">
            <i class="fas fa-file-pdf"></i>
            <h3>No templates found</h3>
            <p>Get started by creating your first PDF template!</p>
            <div class="mt-3">
                <a asp-controller="Template" asp-action="Create" class="btn btn-primary">
                    <i class="fas fa-plus"></i>
                    Create New Template
                </a>
            </div>
        </div>
    }
</div>

@section Scripts {
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            const searchInput = document.getElementById('searchInput');
            const templatesGrid = document.getElementById('templatesGrid');
            const templateCards = templatesGrid ? Array.from(templatesGrid.getElementsByClassName('template-card')) : [];
            const emptyState = document.getElementById('emptyState');
            const totalTemplatesStat = document.getElementById('totalTemplatesStat');

            function filterTemplates() {
                if (!searchInput || !templatesGrid) return;

                const searchTerm = searchInput.value.toLowerCase().trim();
                let visibleCount = 0;

                templateCards.forEach(card => {
                    const name = card.dataset.name.toLowerCase();
                    const description = card.dataset.description.toLowerCase();
                    const isMatch = name.includes(searchTerm) || description.includes(searchTerm);

                    if (isMatch) {
                        card.style.display = 'flex';
                        visibleCount++;
                    } else {
                        card.style.display = 'none';
                    }
                });

                if (visibleCount === 0 && templateCards.length > 0) {
                    templatesGrid.style.display = 'none';
                    if(emptyState) emptyState.style.display = 'block';
                } else if (templateCards.length > 0) {
                    templatesGrid.style.display = 'grid';
                     if(emptyState) emptyState.style.display = 'none';
                } else {

            }
                // totalTemplatesStat.textContent = visibleCount; // Can update this if needed
                }

                if (searchInput) {
                    searchInput.addEventListener('input', filterTemplates);
                }

                templateCards.forEach((card, index) => {
                    card.style.animationDelay = `${index * 0.07}s`;
                });
            });
    </script>
}
-------------------------------------------------------------------------

----------------------------------Templates.cshtml---------------------------------------
@using PdfGeneratorApp.Dtos
@using System.Text.Json
@model List<TemplateDetailDto>

@{
    ViewData["Title"] = "API Documentation";
}

<div class="container">
    <div class="page-header">
        <h1>@ViewData["Title"]</h1>
        <p class="page-subtitle">
            Test and understand the PDF generation API endpoints. Each template has a unique endpoint.
        </p>
    </div>

    @if (Model != null && Model.Any())
    {
        <div class="accordion" id="templateDocsAccordion">
            @foreach (var template in Model)
            {
                string collapseId = $"collapse_template_{template.Id}";
                string headingId = $"heading_template_{template.Id}";
                string jsonDataTextareaId = $"jsonData_payload_{template.Id}";

                <div class="accordion-item">
                    <h2 class="accordion-header" id="@headingId">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#@collapseId" aria-expanded="false" aria-controls="@collapseId">
                            <span class="badge bg-success me-2 p-2">POST</span>
                            <code class="me-2 fs-6">/pdf/generate/@template.Name</code>
                            <span class="text-muted small">@template.Description</span>
                        </button>
                    </h2>
                    <div id="@collapseId" class="accordion-collapse collapse" aria-labelledby="@headingId" data-bs-parent="#templateDocsAccordion">
                        <div class="accordion-body">
                            <h5>Endpoint Summary</h5>
                            <p>Generates a PDF document based on the <strong>@template.Name</strong> template and the provided JSON data.</p>

                            <hr class="my-3" />

                            <div class="try-it-out-section" data-template-name="@template.Name">
                                <h5><i class="fas fa-vial me-1"></i> Try it out</h5>
                                <p class="small text-muted">Modify the JSON payload below and click "Execute" to test the PDF generation.</p>

                                <div class="form-group">
                                    <label for="@jsonDataTextareaId" class="form-label fw-semibold">Request Body (<code>application/json</code>)</label>
                                    <textarea class="form-control json-payload" id="@jsonDataTextareaId" rows="10">@FormatJsonForTextarea(template.ExampleJsonData)</textarea>
                                </div>

                                <div class="mt-3">
                                    <button type="button" class="btn btn-success execute-btn">
                                        <i class="fas fa-play-circle"></i> Execute
                                    </button>
                                    <button type="button" class="btn btn-sm btn-outline-secondary clear-response-btn ms-2" style="display:none;">
                                        <i class="fas fa-times"></i> Clear Response
                                    </button>
                                </div>

                                <div class="response-section mt-3" style="display:none;">
                                    <h6><i class="fas fa-reply me-1"></i> Server Response</h6>
                                    <div class="response-status mb-2 small p-2 border rounded bg-white"></div>
                                    <div class="response-output p-2 border rounded bg-white" style="min-height: 50px;"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            }
        </div>
    }
    else
    {
        <div class="empty-state">
            <i class="fas fa-book-open"></i>
            <h3>No API Endpoints Documented</h3>
            <p>Create some templates first to see their API documentation here.</p>
        </div>
    }
</div>

@functions {
    public string FormatJsonForTextarea(string jsonString)
    {
        if (string.IsNullOrWhiteSpace(jsonString)) return "{\n  \n}";
        try
        {
            using var doc = JsonDocument.Parse(jsonString);
            return JsonSerializer.Serialize(doc, new JsonSerializerOptions { WriteIndented = true });
        }
        catch (JsonException) { return System.Net.WebUtility.HtmlEncode(jsonString); }
    }
}

@section Scripts {
    <script>
        $(document).ready(function() {
            $('.execute-btn').on('click', function() {
                var $button = $(this);
                var $tryItOutSection = $button.closest('.try-it-out-section');
                var templateName = $tryItOutSection.data('template-name');
                var $jsonPayloadTextarea = $tryItOutSection.find('.json-payload');
                var $responseSection = $tryItOutSection.find('.response-section');
                var $responseStatusDiv = $tryItOutSection.find('.response-status');
                var $responseOutputDiv = $tryItOutSection.find('.response-output');
                var $clearButton = $tryItOutSection.find('.clear-response-btn');

                var jsonDataString = $jsonPayloadTextarea.val();
                var payload;

                $responseSection.hide();
                $responseStatusDiv.empty().removeClass('alert alert-danger alert-success alert-warning');
                $responseOutputDiv.empty();
                $clearButton.hide();

                try {
                    payload = JSON.parse(jsonDataString);
                } catch (e) {
                    $responseStatusDiv.html('<strong>Error:</strong> Invalid JSON in payload.').addClass('alert alert-danger');
                    $responseOutputDiv.text(e.message);
                    $responseSection.show();
                    $clearButton.show();
                    return;
                }

                $button.prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Executing...');

                fetch(`/pdf/generate/${templateName}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                })
                .then(response => {
                    const contentType = response.headers.get('content-type');
                    if (response.ok && contentType && contentType.includes('application/pdf')) {
                        return response.blob().then(blob => ({
                            blob: blob, isPdf: true, status: response.status, statusText: response.statusText, headers: response.headers, ok: response.ok
                        }));
                    } else {
                        return response.text().then(text => ({
                            text: text, isPdf: false, status: response.status, statusText: response.statusText, headers: response.headers, ok: response.ok
                        }));
                    }
                })
                .then(result => {
                    $responseStatusDiv.html(`<strong>Status:</strong> ${result.status} ${result.statusText}`);
                    if (result.isPdf) {
                        const url = window.URL.createObjectURL(result.blob);
                        const a = document.createElement('a');
                        const suggestedFilename = result.headers.get('content-disposition')?.split('filename=')[1]?.split(';')[0]?.replace(/"/g, '') || `${templateName}_API_Test.pdf`;
                        a.href = url;
                        a.download = suggestedFilename;
                        a.innerHTML = `<i class="fas fa-download me-1"></i> Download ${suggestedFilename}`;
                        a.className = 'btn btn-sm btn-success d-block mt-2';
                        $responseOutputDiv.append($('<div>').html('PDF generated successfully.'));
                        $responseOutputDiv.append(a);
                        $responseStatusDiv.addClass('alert alert-success');
                    } else {
                        $responseOutputDiv.text(result.text);
                        if(result.ok){ $responseStatusDiv.addClass('alert alert-warning'); }
                        else { $responseStatusDiv.addClass('alert alert-danger'); }
                    }
                })
                .catch(error => {
                    console.error('Fetch Error:', error);
                    $responseStatusDiv.html('<strong>Network/Fetch Error</strong>').addClass('alert alert-danger');
                    $responseOutputDiv.text(error.message);
                })
                .finally(() => {
                    $button.prop('disabled', false).html('<i class="fas fa-play-circle"></i> Execute');
                    $responseSection.show();
                    $clearButton.show();
                });
            });

            $('.clear-response-btn').on('click', function() {
                var $tryItOutSection = $(this).closest('.try-it-out-section');
                $tryItOutSection.find('.response-section').hide();
                $tryItOutSection.find('.response-status').empty().removeClass('alert alert-danger alert-success alert-warning');
                $tryItOutSection.find('.response-output').empty();
                $(this).hide();
            });
        });
    </script>
}
-------------------------------------------------------------------------

--------------------------------Create.cshtml-----------------------------------------
@model PdfGeneratorApp.Dtos.TemplateCreateDto

@{
    ViewData["Title"] = "Create New Template";
}

<div class="container">
    <div class="page-header">
        <h1>@ViewData["Title"]</h1>
        <p class="page-subtitle">Define a new PDF template with its HTML structure and example data.</p>
    </div>

    <div class="card p-4 shadow-sm">
        <div class="card-body">
             <form asp-action="Create" method="post">
                <div asp-validation-summary="ModelOnly" class="text-danger mb-3"></div>
                <div class="form-group mb-3">
                    <label asp-for="Name" class="form-label"></label>
                    <input asp-for="Name" class="form-control" />
                    <span asp-validation-for="Name" class="text-danger"></span>
                </div>
                <div class="form-group mb-3">
                    <label asp-for="Description" class="form-label"></label>
                    <input asp-for="Description" class="form-control" />
                    <span asp-validation-for="Description" class="text-danger"></span>
                </div>

                <div class="mb-4 p-3 border rounded bg-light">
                    <h5>HTML Content Source:</h5>
                    <div class="form-group mb-3">
                        <label for="htmlEditor" class="form-label">Edit HTML Content:</label>
                        <textarea asp-for="HtmlContent" class="form-control" rows="15" id="htmlEditor"></textarea>
                        <span asp-validation-for="HtmlContent" class="text-danger"></span>
                        <small class="form-text text-muted">Use <code>&lt;&lt;FieldName&gt;&gt;</code> for dynamic data placeholders.</small>
                    </div>
                    <p class="text-center mb-2">OR Upload an HTML file to populate the editor:</p>
                    <div class="form-group mb-3">
                        <label for="htmlFile" class="form-label">Upload HTML File (.html):</label>
                        <input type="file" id="htmlFile" name="htmlFile" class="form-control" accept=".html,.htm" />
                    </div>
                     <div id="uploadStatus" class="mt-2"></div>
                </div>

                <div class="form-group mb-4">
                    <label asp-for="ExampleJsonData" class="form-label"></label>
                    <textarea asp-for="ExampleJsonData" class="form-control" rows="10" id="exampleJsonData"></textarea>
                    <span asp-validation-for="ExampleJsonData" class="text-danger"></span>
                    <small class="form-text text-muted">Provide a sample JSON payload for this template's documentation.</small>
                </div>
                <div class="form-group">
                    <input type="submit" value="Create" class="btn btn-primary" />
                    <a asp-action="Index" asp-controller="Home" class="btn btn-secondary ms-2">Back to List</a>
                </div>
            </form>
        </div>
    </div>
</div>

@section Scripts {
    @{await Html.RenderPartialAsync("_ValidationScriptsPartial");}

    <link href="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.js"></script>

    <script>
        $(document).ready(function() {
            var htmlEditor = $('#htmlEditor');
            var uploadStatus = $('#uploadStatus');
            var exampleJsonDataTextarea = $('#exampleJsonData');

            htmlEditor.summernote({
                height: 600,
                toolbar: [
                    ['style', ['bold', 'italic', 'underline', 'clear']],
                    ['font', ['strikethrough', 'superscript', 'subscript']],
                    ['fontsize', ['fontsize']],
                    ['color', ['color']],
                    ['para', ['ul', 'ol', 'paragraph']],
                    ['table', ['table']],
                    ['insert', ['link', 'picture', 'video']],
                    ['view', ['fullscreen', 'code', 'help']]
                ]
            });

            try {
                var rawJson = exampleJsonDataTextarea.val();
                if (rawJson) {
                    var parsedJson = JSON.parse(rawJson);
                    exampleJsonDataTextarea.val(JSON.stringify(parsedJson, null, 2));
                }
            } catch (e) {
                console.error("Failed to parse existing JSON:", e);
            }

            function showStatus(message, type = 'info') {
                uploadStatus.html(`<div class="alert alert-${type}">${message}</div>`);
            }

            $('#htmlFile').on('change', function() {
                var file = this.files[0];
                if (file) {
                    showStatus('Reading HTML file...');
                    var reader = new FileReader();
                    reader.onload = function(e) {
                        htmlEditor.summernote('code', e.target.result);
                        showStatus('HTML file loaded into editor.', 'success');
                    };
                    reader.onerror = function() {
                        showStatus('Error reading HTML file.', 'danger');
                    };
                    reader.readAsText(file);
                } else {
                    uploadStatus.html('');
                }
            });
        });
    </script>
}
-------------------------------------------------------------------------

----------------------------------Design.cshtml---------------------------------------
@model PdfGeneratorApp.Dtos.TemplateDetailDto

@{
    ViewData["Title"] = $"Design Template: {Model.Name}";
}

<div class="container">
    <div class="page-header">
        <h1>@ViewData["Title"]</h1>
        <p class="page-subtitle">Edit the HTML content and example data for this template.</p>
    </div>

    <div class="card p-4 shadow-sm">
        <div class="card-body">
            <form asp-action="Design" asp-route-templateName="@Model.Name" method="post">
                <div asp-validation-summary="ModelOnly" class="text-danger mb-3"></div>
                <input type="hidden" asp-for="Id" />

                <div class="row mb-3">
                     <div class="col-md-6">
                         <div class="form-group">
                             <label class="form-label">Template Name:</label>
                             <input value="@Model.Name" class="form-control" readonly />
                         </div>
                     </div>
                     <div class="col-md-3">
                          <div class="form-group">
                              <label class="form-label">Current Version:</label>
                              <input value="@Model.CurrentVersion" class="form-control" readonly />
                          </div>
                     </div>
                     <div class="col-md-3">
                           <div class="form-group">
                               <label class="form-label">Last Modified:</label>
                               <input value="@Model.LastModified.ToString("g")" class="form-control" readonly />
                           </div>
                     </div>
                </div>


                <div class="form-group mb-3">
                    <label asp-for="Description" class="form-label"></label>
                    <input asp-for="Description" class="form-control" />
                    <span asp-validation-for="Description" class="text-danger"></span>
                </div>

                <div class="form-group mb-4">
                    <label asp-for="HtmlContent" class="form-label"></label>
                    <textarea asp-for="HtmlContent" class="form-control" rows="15" id="htmlEditor"></textarea>
                    <span asp-validation-for="HtmlContent" class="text-danger"></span>
                    <small class="form-text text-muted">Use <code>&lt;&lt;FieldName&gt;&gt;</code> for dynamic data placeholders.</small>
                </div>

                <div class="form-group mb-4">
                    <label asp-for="ExampleJsonData" class="form-label"></label>
                    <textarea asp-for="ExampleJsonData" class="form-control" rows="10" id="exampleJsonData"></textarea>
                    <span asp-validation-for="ExampleJsonData" class="text-danger"></span>
                    <small class="form-text text-muted">Provide a sample JSON payload for this template's documentation.</small>
                </div>

                <div class="form-group">
                    <input type="submit" value="Save Changes" class="btn btn-primary" />
                    <a asp-action="Index" asp-controller="Home" class="btn btn-secondary ms-2">Back to Templates</a>
                    <a asp-controller="Template" asp-action="History" asp-route-templateName="@Model.Name" class="btn btn-info ms-2">View History</a>
                    <button type="button" id="downloadPdfBtn" class="btn btn-success ms-2">Download Test PDF</button>
                </div>
            </form>
        </div>
    </div>
</div>

@section Scripts {
    @{await Html.RenderPartialAsync("_ValidationScriptsPartial");}

    <link href="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.js"></script>

    <script>
        $(document).ready(function() {
            var htmlEditor = $('#htmlEditor');
            var exampleJsonDataTextarea = $('#exampleJsonData');

            htmlEditor.summernote({
                height: 600,
                toolbar: [
                    ['style', ['bold', 'italic', 'underline', 'clear']],
                    ['font', ['strikethrough', 'superscript', 'subscript']],
                    ['fontsize', ['fontsize']],
                    ['color', ['color']],
                    ['para', ['ul', 'ol', 'paragraph']],
                    ['table', ['table']],
                    ['insert', ['link', 'picture', 'video']],
                    ['view', ['fullscreen', 'code', 'help']]
                ]
            });

            try {
                var rawJson = exampleJsonDataTextarea.val();
                if (rawJson) {
                    var parsedJson = JSON.parse(rawJson);
                    exampleJsonDataTextarea.val(JSON.stringify(parsedJson, null, 2));
                }
            } catch (e) {
                console.error("Failed to parse existing JSON:", e);
            }

            $('#downloadPdfBtn').on('click', function() {
                var templateName = '@Model.Name';
                var exampleJsonData = exampleJsonDataTextarea.val();
                var endpoint = `/pdf/generate/${templateName}`;

                try {
                    var payload = JSON.parse(exampleJsonData);
                } catch (e) {
                    alert('Error: Invalid JSON in Example JSON Data field. Please correct it before testing.');
                    console.error('JSON Parse Error:', e);
                    return;
                }

                fetch(endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                })
                .then(response => {
                    if (!response.ok) {
                         return response.text().then(text => {
                            throw new Error(`HTTP error! status: ${response.status} - ${text}`);
                         });
                    }
                    return response.blob();
                })
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `${templateName}_Test.pdf`;
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                })
                .catch(error => {
                    alert('There was a problem generating the PDF: ' + error.message);
                    console.error('PDF Generation Error:', error);
                });
            });
        });
    </script>
}
-------------------------------------------------------------------------

------------------------------------History.cshtml-------------------------------------
@model PdfGeneratorApp.Dtos.TemplateDetailDto
@{
    var versions = ViewBag.TemplateVersions as List<PdfGeneratorApp.Dtos.TemplateVersionDto>;
    ViewData["Title"] = $"History for {Model.Name}";
}

<div class="container">
    <div class="page-header">
        <h1>@ViewData["Title"]</h1>
        <p class="page-subtitle">Review past versions of the template. Current version is <strong>@Model.CurrentVersion</strong>.</p>
    </div>

    @if (versions != null && versions.Any())
    {
        <div class="table-container">
            <table class="table">
                <thead>
                    <tr>
                        <th>Version</th>
                        <th>Description</th>
                        <th>Modified Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    @foreach (var version in versions)
                    {
                        <tr class="@(version.VersionNumber == Model.CurrentVersion ? "fw-bold table-info" : "")">
                            <td>
                                @version.VersionNumber
                                @if (version.VersionNumber == Model.CurrentVersion)
                                {
                                    <span class="badge bg-primary ms-2">Current</span>
                                }
                            </td>
                            <td style="max-width: 300px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="@version.Description">
                                @(string.IsNullOrWhiteSpace(version.Description) ? "N/A" : version.Description)
                            </td>
                            <td>@version.CreatedDate.ToString("MMMM dd, yyyy h:mm tt")</td>
                            <td class="actions-column">
                                @if (version.VersionNumber != Model.CurrentVersion)
                                {
                                    <form asp-action="Revert" asp-route-templateName="@Model.Name" asp-route-versionNumber="@version.VersionNumber" method="post" class="d-inline needs-confirmation" data-confirmation-message="Are you sure you want to revert to version @version.VersionNumber? This will create a new version of the current state before reverting.">
                                        @Html.AntiForgeryToken()
                                        <button type="submit" class="btn btn-sm btn-warning" title="Revert to this version">
                                            <i class="fas fa-undo"></i> Revert
                                        </button>
                                    </form>
                                }
                            </td>
                        </tr>
                    }
                </tbody>
            </table>
        </div>
    }
    else
    {
        <div class="empty-state">
            <i class="fas fa-folder-open"></i>
            <h3>No historical versions found.</h3>
            <p>This template does not have any previous versions recorded.</p>
        </div>
    }

    <div class="mt-4 text-center">
        <a asp-controller="Template" asp-action="Design" asp-route-templateName="@Model.Name" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Back to Design
        </a>
    </div>
</div>

@section Scripts {
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            const forms = document.querySelectorAll('.needs-confirmation');
            forms.forEach(form => {
                form.addEventListener('submit', function (event) {
                    const message = this.dataset.confirmationMessage || 'Are you sure?';
                    if (!confirm(message)) {
                        event.preventDefault();
                    }
                });
            });
        });
    </script>
}
-------------------------------------------------------------------------

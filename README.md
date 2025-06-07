Okay, this is a significant feature addition that requires modifying models, DTOs, controllers, services, and views. Implementing a truly "easy visual way" for complex nested JSON and database query configuration directly in the existing razor views without introducing a dedicated front-end framework or complex JS component is challenging.

As a compromise for the "easy visual way" within the current structure, I will update the Design and Create pages to:

1.  Rename the `ExampleJsonData` field/property to `InsideDataConfig`.
2.  Add a button near the `InsideDataConfig` textarea.
3.  Add JavaScript that, when the button is clicked, analyzes the HTML content for `<<Placeholders>>` and generates a *skeleton* of the new, nested JSON structure in the `InsideDataConfig` textarea, preserving any existing entries if possible. This provides a starting point for the user to fill in.

For the API documentation, I will update the "Try it out" section to parse the template's stored `InsideDataConfig`, extract the keys, and generate a sample "outside" mode JSON payload with default values ("Data" or `false` for boolean fields) for the user to test.

Here are the code changes:

**1. Models (`Template.cs`, `TemplateVersion.cs`)**

Rename `ExampleJsonData` to `InsideDataConfig`. Mark `InsideDataConfig` as nullable in the model as it will be optional in the DTOs and might be null in the database if a template doesn't use "inside" mode.

**2. DTOs (`TemplateCreateDto.cs`, `TemplateDetailDto.cs`, `TemplateListDto.cs`, `TemplateUpdateDto.cs`, `TemplateVersionDto.cs`)**

Rename `ExampleJsonData` to `InsideDataConfig`.

**3. Services (`TemplateProcessingService.cs`)**

This is a new service needed to handle processing the "inside" data configuration, executing SQL, and generating the flat data used by the HTML replacement logic. It also needs to handle placeholder detection and skeleton JSON generation.

**4. Controllers (`PdfController.cs`, `TemplateController.cs`, `DocsController.cs`)**

*   **`PdfController`:** Modify the POST `Generate` action to accept a `mode` parameter (query string or body, let's use query string for simplicity: `/pdf/generate/{templateName}?mode=inside`). Based on the mode, it will either use the request body JSON ("outside") or load/process `InsideDataConfig` ("inside") via the new service.
*   **`TemplateController`:** Update GET/POST `Create` and `Design` to use the new `InsideDataConfig` property. Update auto-generation logic to produce the new JSON structure. Update `History` to use the new property.
*   **`DocsController`:** Update the `Templates` action to use the new `InsideDataConfig` property. The view will then use this to generate the example "outside" payload.

**5. Views (`_Layout.cshtml`, `Index.cshtml`, `Templates.cshtml`, `Create.cshtml`, `Design.cshtml`, `History.cshtml`)**

*   **`_Layout.cshtml`**: No structural changes needed related to this feature, just visual updates as requested in the previous prompt.
*   **`Index.cshtml`**: No changes needed as `ExampleJsonData` wasn't displayed here.
*   **`Templates.cshtml`**: Update property name (`ExampleJsonData` -> `InsideDataConfig`) in the model. Modify JavaScript to generate the "outside" example payload from the `InsideDataConfig`.
*   **`Create.cshtml` & `Design.cshtml`**: Update property name (`ExampleJsonData` -> `InsideDataConfig`). Add UI elements (button, maybe helper text) and JavaScript to generate the `InsideDataConfig` skeleton JSON.
*   **`History.cshtml`**: Update property name (`ExampleJsonData` -> `InsideDataConfig`).

**6. Configuration (`appsettings.json`)**

Add a section for database connection strings specific to the "inside" mode queries.

**7. Program.cs**

Register the new `TemplateProcessingService` and configure access to `IConfiguration` for it.

Let's implement these changes step-by-step.

```csharp
// File: Models/Template.cs
using System.ComponentModel.DataAnnotations;
using System.Collections.Generic;
using System; // Add this

namespace PdfGeneratorApp.Models
{
    public class Template
    {
        public int Id { get; set; }

        [Required]
        [StringLength(100)]
        public string Name { get; set; }

        [Required]
        public string HtmlContent { get; set; }

        public string? Description { get; set; } // Made nullable

        // Store configuration for 'inside' mode data sources
        public string? InsideDataConfig { get; set; } // Renamed and made nullable

        // Version control fields
        public int CurrentVersion { get; set; } = 1;
        public DateTime LastModified { get; set; } = DateTime.Now;

        // Navigation property for versions
        public ICollection<TemplateVersion>? Versions { get; set; } // Made nullable
    }
}
```

```csharp
// File: Models/TemplateVersion.cs
using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace PdfGeneratorApp.Models
{
    public class TemplateVersion
    {
        public int Id { get; set; }

        public int TemplateId { get; set; } // Foreign key to Template

        public int VersionNumber { get; set; }

        [Required]
        public string HtmlContent { get; set; }

        public string? Description { get; set; }

        // Store historical configuration for 'inside' mode data sources
        public string? InsideDataConfig { get; set; } // Renamed and made nullable

        public DateTime CreatedDate { get; set; } = DateTime.Now;

        // Navigation property back to Template
        [ForeignKey("TemplateId")]
        public Template? Template { get; set; } // Made nullable
    }
}
```

```csharp
// File: Dtos/TemplateCreateDto.cs
using System.ComponentModel.DataAnnotations;

namespace PdfGeneratorApp.Dtos
{
    public class TemplateCreateDto
    {
        [Required]
        [StringLength(100, ErrorMessage = "Template Name cannot exceed 100 characters.")]
        public string Name { get; set; } = ""; // Initialize to avoid null warnings

        public string? Description { get; set; }

        [Required(ErrorMessage = "HTML Content is required.")]
        public string HtmlContent { get; set; } = ""; // Initialize

        // Configuration for 'inside' mode data sources
        public string? InsideDataConfig { get; set; }
    }
}
```

```csharp
// File: Dtos/TemplateDetailDto.cs
using System.ComponentModel.DataAnnotations;
using System; // Add this

namespace PdfGeneratorApp.Dtos
{
    public class TemplateDetailDto
    {
        public int Id { get; set; }

        [Required]
        [StringLength(100, ErrorMessage = "Template Name cannot exceed 100 characters.")]
        public string Name { get; set; } = ""; // Initialize

        public string? Description { get; set; }

        [Required(ErrorMessage = "HTML Content is required.")]
        public string HtmlContent { get; set; } = ""; // Initialize

        // Configuration for 'inside' mode data sources
        public string? InsideDataConfig { get; set; }

        public int CurrentVersion { get; set; }
        public DateTime LastModified { get; set; }
    }
}
```

```csharp
// File: Dtos/TemplateListDto.cs
using System; // Add this

namespace PdfGeneratorApp.Dtos
{
    public class TemplateListDto
    {
        public int Id { get; set; }
        public string Name { get; set; } = ""; // Initialize
        public string Description { get; set; } = ""; // Initialize (adjust if Description in Model is nullable)
        public int CurrentVersion { get; set; }
        public DateTime LastModified { get; set; }
    }
}
```

```csharp
// File: Dtos/TemplateUpdateDto.cs
using System.ComponentModel.DataAnnotations;

namespace PdfGeneratorApp.Dtos
{
    // This DTO contains only the fields that can be updated via the Design POST.
    public class TemplateUpdateDto
    {
        public int Id { get; set; } // Needed to identify the entity to update

        public string? Description { get; set; }

        [Required(ErrorMessage = "HTML Content is required.")]
        public string HtmlContent { get; set; } = ""; // Initialize

        // Configuration for 'inside' mode data sources
        public string? InsideDataConfig { get; set; }
    }
}
```

```csharp
// File: Dtos/TemplateVersionDto.cs
using System; // Add this

namespace PdfGeneratorApp.Dtos
{
    public class TemplateVersionDto
    {
        public int Id { get; set; }
        public int TemplateId { get; set; }
        public int VersionNumber { get; set; }
        public string HtmlContent { get; set; } = ""; // Initialize
        public string? Description { get; set; }
        // Historical configuration for 'inside' mode data sources
        public string? InsideDataConfig { get; set; }
        public DateTime CreatedDate { get; set; }
    }
}
```

```csharp
// File: Services/TemplateProcessingService.cs
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.Text.RegularExpressions;
using Microsoft.Extensions.Configuration;
using System.Data.SqlClient; // Assuming MSSQL for SQL queries

namespace PdfGeneratorApp.Services
{
    public class TemplateProcessingService
    {
        private readonly IConfiguration _configuration;
        private const string FALLBACK_VALUE = "--";

        public TemplateProcessingService(IConfiguration configuration)
        {
            _configuration = configuration;
        }

        // Method to process HTML with flat JSON data (used by both modes after data is resolved)
        public string ProcessHtml(string htmlContent, JsonElement jsonData)
        {
            string processedHtml = htmlContent;
            if (jsonData.ValueKind != JsonValueKind.Object)
            {
                // If the provided JSON is not an object, cannot replace placeholders
                return processedHtml;
            }

            // Find all placeholders like <<FieldName>>
            var placeholders = Regex.Matches(htmlContent, @"&lt;&lt;(\w+)&gt;&gt;") // Regex for &lt;&lt;FieldName&gt;&gt;
                                    .Cast<Match>()
                                    .Select(m => m.Groups[1].Value)
                                    .Distinct()
                                    .ToList();

             // Also find placeholders like <<FieldName>> without HTML encoding if needed
            var nonEncodedPlaceholders = Regex.Matches(htmlContent, @"<<(\w+)>>")
                                             .Cast<Match>()
                                             .Select(m => m.Groups[1].Value)
                                             .Distinct()
                                             .ToList();

            placeholders.AddRange(nonEncodedPlaceholders);
            placeholders = placeholders.Distinct().ToList();


            foreach (var fieldName in placeholders)
            {
                string placeholder = $"&lt;&lt;{fieldName}&gt;&gt;"; // Check encoded first
                 string nonEncodedPlaceholder = $"<<{fieldName}>>"; // Check non-encoded

                string valueToInject = ""; // Default empty string

                if (jsonData.TryGetProperty(fieldName, out JsonElement valueElement))
                {
                    // Handle different JSON value kinds
                    switch (valueElement.ValueKind)
                    {
                        case JsonValueKind.String:
                            valueToInject = valueElement.GetString() ?? "";
                            break;
                        case JsonValueKind.Number:
                            valueToInject = valueElement.GetRawText(); // Get number as string
                            break;
                        case JsonValueKind.True:
                            valueToInject = "true";
                            break;
                        case JsonValueKind.False:
                            valueToInject = "false";
                            break;
                        case JsonValueKind.Null:
                            valueToInject = ""; // Represent null as empty string
                            break;
                        case JsonValueKind.Undefined:
                             valueToInject = ""; // Represent undefined as empty string
                            break;
                        case JsonValueKind.Object:
                        case JsonValueKind.Array:
                             // For complex types, you might serialize them or handle them differently.
                             // For now, represent as an empty string or specific marker.
                             valueToInject = "[COMPLEX DATA]"; // Or JsonSerializer.Serialize(valueElement) if safe
                             break;
                    }
                } else {
                    // If property is missing, inject fallback (this might be handled before calling this method
                    // if fallback is only for 'inside' mode, but safe to have here too)
                    // valueToInject = FALLBACK_VALUE; // Removed fallback here, controller/ResolveInsideData should handle it
                }

                // Replace both encoded and non-encoded placeholders
                processedHtml = processedHtml.Replace(placeholder, valueToInject);
                processedHtml = processedHtml.Replace(nonEncodedPlaceholder, valueToInject);
            }

            return processedHtml;
        }


        // Method to resolve data based on 'inside' mode configuration
        public async Task<JsonElement> ResolveInsideData(string? insideDataConfigJson)
        {
            var dataBuilder = new Dictionary<string, object?>();

            if (string.IsNullOrWhiteSpace(insideDataConfigJson))
            {
                // No config provided, return empty data object
                 return JsonSerializer.SerializeToElement(dataBuilder);
            }

            try
            {
                // Parse the inside data configuration JSON
                var config = JsonSerializer.Deserialize<Dictionary<string, Dictionary<string, string>>>(insideDataConfigJson);

                if (config == null) return JsonSerializer.SerializeToElement(dataBuilder);

                foreach (var fieldConfig in config)
                {
                    var fieldName = fieldConfig.Key;
                    var source = fieldConfig.Value;

                    if (source.TryGetValue("type", out string? type) && source.TryGetValue("value", out string? value))
                    {
                        object? resolvedValue = null;
                        bool resolved = false;

                        if (type.Equals("static", System.StringComparison.OrdinalIgnoreCase))
                        {
                            resolvedValue = value; // Static value is the value string itself
                            resolved = true;
                        }
                        else if (type.Equals("sql", System.StringComparison.OrdinalIgnoreCase))
                        {
                             // SQL source config format: {"type": "sql", "value": "SELECT ...", "database": "DbName"}
                             if (source.TryGetValue("database", out string? dbName) && !string.IsNullOrWhiteSpace(dbName))
                             {
                                 try
                                 {
                                     resolvedValue = await ExecuteScalarSqlAsync(dbName, value); // Execute the SQL query
                                     resolved = true;
                                 }
                                 catch (System.Exception ex)
                                 {
                                     // Log SQL execution error
                                     System.Console.WriteLine($"Error executing SQL for field '{fieldName}' in database '{dbName}': {ex.Message}");
                                     resolvedValue = $"[SQL ERROR: {ex.Message}]"; // Indicate error in output
                                     resolved = true; // Consider it resolved to an error message
                                 }
                             } else {
                                // SQL type specified but no database config
                                resolvedValue = "[SQL ERROR: Database name missing]";
                                resolved = true; // Consider resolved to error
                             }
                        }
                        // Add other types here if needed (e.g., API call, file read)

                        if (resolved)
                        {
                            // Add the resolved value to the data builder
                             // Handle potential nulls from SQL queries or static nulls explicitly
                            dataBuilder[fieldName] = resolvedValue;
                        }
                        else
                        {
                            // Type not recognized or value missing
                             dataBuilder[fieldName] = $"[CONFIG ERROR: Unknown type '{type}' or missing value]";
                        }
                    }
                    else
                    {
                        // 'type' or 'value' keys missing for this field configuration
                         dataBuilder[fieldName] = "[CONFIG ERROR: Missing type or value]";
                    }
                }

                // Apply fallback for any placeholders found in HTML but not resolved
                var placeholdersInHtml = Regex.Matches(htmlContent, @"&lt;&lt;(\w+)&gt;&gt;").Cast<Match>().Select(m => m.Groups[1].Value).Distinct().ToList();
                placeholdersInHtml.AddRange(Regex.Matches(htmlContent, @"<<(\w+)>>").Cast<Match>().Select(m => m.Groups[1].Value).Distinct());


                foreach(var fieldName in placeholdersInHtml.Distinct())
                {
                     if (!dataBuilder.ContainsKey(fieldName))
                     {
                         dataBuilder[fieldName] = FALLBACK_VALUE;
                     } else if (dataBuilder[fieldName] == null)
                     {
                          // Replace DBNull or explicit null with fallback
                         dataBuilder[fieldName] = FALLBACK_VALUE;
                     }
                }


            }
            catch (JsonException)
            {
                // Config JSON is invalid, return errors for all placeholders
                 System.Console.WriteLine($"Invalid InsideDataConfig JSON: {insideDataConfigJson}");
                 var placeholdersInHtml = Regex.Matches(htmlContent, @"&lt;&lt;(\w+)&gt;&gt;").Cast<Match>().Select(m => m.Groups[1].Value).Distinct().ToList();
                 placeholdersInHtml.AddRange(Regex.Matches(htmlContent, @"<<(\w+)>>").Cast<Match>().Select(m => m.Groups[1].Value).Distinct());
                 foreach(var fieldName in placeholdersInHtml.Distinct())
                 {
                     dataBuilder[fieldName] = "[CONFIG ERROR: Invalid JSON]";
                 }
            }
            catch (System.Exception ex)
            {
                 // General error during processing config
                 System.Console.WriteLine($"General error processing InsideDataConfig: {ex.Message}");
                 var placeholdersInHtml = Regex.Matches(htmlContent, @"&lt;&lt;(\w+)&gt;&gt;").Cast<Match>().Select(m => m.Groups[1].Value).Distinct().ToList();
                 placeholdersInHtml.AddRange(Regex.Matches(htmlContent, @"<<(\w+)>>").Cast<Match>().Select(m => m.Groups[1].Value).Distinct());
                 foreach(var fieldName in placeholdersInHtml.Distinct())
                 {
                     dataBuilder[fieldName] = $"[ERROR: {ex.Message}]";
                 }
            }

            return JsonSerializer.SerializeToElement(dataBuilder);
        }


        // Helper method to execute a scalar SQL query
        private async Task<object?> ExecuteScalarSqlAsync(string dbName, string sqlQuery)
        {
            // Get connection string from configuration
            var connectionString = _configuration.GetConnectionString(dbName);

            if (string.IsNullOrWhiteSpace(connectionString))
            {
                throw new System.Exception($"Database connection string for '{dbName}' not found in configuration.");
            }

            // Use SqlConnection for MSSQL
            using (var connection = new SqlConnection(connectionString))
            {
                using (var command = new SqlCommand(sqlQuery, connection))
                {
                    await connection.OpenAsync();
                    var result = await command.ExecuteScalarAsync(); // Execute scalar query
                    // Handle DBNull
                    return result == System.DBNull.Value ? null : result;
                }
            }
        }


        // Method to generate skeleton InsideDataConfig JSON from HTML placeholders
        public string GenerateInsideDataConfigSkeleton(string htmlContent)
        {
             // Find all placeholders like <<FieldName>>
            var placeholders = Regex.Matches(htmlContent, @"&lt;&lt;(\w+)&gt;&gt;") // Regex for &lt;&lt;FieldName&gt;&gt;
                                    .Cast<Match>()
                                    .Select(m => m.Groups[1].Value)
                                    .Distinct()
                                    .ToList();

             // Also find placeholders like <<FieldName>> without HTML encoding
            var nonEncodedPlaceholders = Regex.Matches(htmlContent, @"<<(\w+)>>")
                                             .Cast<Match>()
                                             .Select(m => m.Groups[1].Value)
                                             .Distinct()
                                             .ToList();

            placeholders.AddRange(nonEncodedPlaceholders);
            placeholders = placeholders.Distinct().ToList();


            var config = new Dictionary<string, Dictionary<string, string>>();

            foreach (var fieldName in placeholders)
            {
                 // Default to static type with empty value
                config[fieldName] = new Dictionary<string, string>
                {
                    { "type", "static" },
                    { "value", "" }
                };

                // Example of adding SQL option if needed for documentation purposes,
                // but for skeleton, static is simpler default.
                // If you want to show SQL as an *option* in the skeleton:
                // config[fieldName]["sql_example_value"] = "SELECT ...";
                // config[fieldName]["sql_example_database"] = "YourDbName";

            }

             // Format the JSON nicely for the textarea
            return JsonSerializer.Serialize(config, new JsonSerializerOptions { WriteIndented = true });
        }


        // Method to generate example 'outside' mode JSON payload from InsideDataConfig keys
        public string GenerateOutsideModeExamplePayload(string? insideDataConfigJson)
        {
            var exampleData = new Dictionary<string, object>();

            if (!string.IsNullOrWhiteSpace(insideDataConfigJson))
            {
                try
                {
                     var config = JsonSerializer.Deserialize<Dictionary<string, Dictionary<string, string>>>(insideDataConfigJson);

                    if (config != null)
                    {
                        foreach (var fieldConfig in config)
                        {
                            var fieldName = fieldConfig.Key;
                            // Suggest a default value for the OUTSIDE payload
                            if (fieldName.StartsWith("is", System.StringComparison.OrdinalIgnoreCase) || fieldName.StartsWith("has", System.StringComparison.OrdinalIgnoreCase))
                            {
                                // Suggest boolean false for fields starting with 'is' or 'has'
                                exampleData[fieldName] = false;
                            }
                            else
                            {
                                // Suggest a generic string value
                                exampleData[fieldName] = "Sample Data";
                            }
                        }
                    }
                }
                catch (JsonException)
                {
                    // If InsideDataConfig is invalid JSON, just return a generic example
                     exampleData["FieldName"] = "Sample Value";
                }
            }
            else
            {
                 // If no InsideDataConfig, return a generic example
                 exampleData["FieldName"] = "Sample Value";
            }


            return JsonSerializer.Serialize(exampleData, new JsonSerializerOptions { WriteIndented = true });
        }

         // Method to get available database connection names from appsettings
        public List<string> GetAvailableDatabaseNames()
        {
            // ConnectionStrings is a standard section name in appsettings.json
            // You might need to adjust "ConnectionStrings" if your config uses a different section
            var connectionStringsSection = _configuration.GetSection("ConnectionStrings");

            if (connectionStringsSection == null) return new List<string>();

            // GetSection().GetChildren() gives you the keys (names) of the connections
            return connectionStringsSection.GetChildren().Select(c => c.Key).ToList();
        }
    }

    // C# Classes to represent the InsideDataConfig JSON structure for deserialization
    // (Optional but can help with type safety if you deserialize the whole structure)
    public class InsideDataConfiguration
    {
        // Dictionary where key is the placeholder name (e.g., "CustomerName")
        // Value is an object defining the source (Static or SQL)
        public Dictionary<string, SourceConfiguration> Fields { get; set; } = new Dictionary<string, SourceConfiguration>();
    }

    public class SourceConfiguration
    {
        // "static" or "sql"
        [JsonPropertyName("type")]
        public string Type { get; set; } = "";

        // The static value or the SQL query string
        [JsonPropertyName("value")]
        public string Value { get; set; } = "";

        // Optional: Database name from appsettings.json for SQL type
        [JsonPropertyName("database")]
        public string? Database { get; set; }
    }
}
```

```csharp
// File: Controllers/PdfController.cs
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PdfGeneratorApp.Data;
using WkHtmlToPdfDotNet;
using WkHtmlToPdfDotNet.Contracts;
using System.Text.Json;
using System.Threading.Tasks;
using PdfGeneratorApp.Services;
using System;
using System.Linq; // Add this

namespace PdfGeneratorApp.Controllers
{
    public class PdfController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly IConverter _converter;
        private readonly TemplateProcessingService _templateProcessingService;

        public PdfController(ApplicationDbContext context, IConverter converter, TemplateProcessingService templateProcessingService)
        {
            _context = context;
            _converter = converter;
            _templateProcessingService = templateProcessingService;
        }

        // GET: /pdf/generate/{templateName} - Redirect to Design as before
        [HttpGet("pdf/generate/{templateName}")]
        public async Task<IActionResult> Generate(string templateName)
        {
            var template = await _context.Templates.FirstOrDefaultAsync(t => t.Name == templateName);
            if (template == null)
            {
                return NotFound($"Template '{templateName}' not found.");
            }
            return RedirectToAction("Design", "Template", new { templateName = template.Name });
        }

        // POST: /pdf/generate/{templateName}
        // Accepts dynamic JSON data OR uses internal data sources based on 'mode' query parameter
        [HttpPost("pdf/generate/{templateName}")]
        [Consumes("application/json")] // Still consumes JSON if provided (for outside mode)
        public async Task<IActionResult> Generate(string templateName, [FromQuery] string? mode, [FromBody] JsonElement? jsonData) // Add mode query param and make body optional
        {
            var template = await _context.Templates.FirstOrDefaultAsync(t => t.Name == templateName);
            if (template == null)
            {
                return NotFound($"Template '{templateName}' not found.");
            }

            JsonElement finalData;

            // Determine mode (default to 'outside')
            var generationMode = mode?.ToLower() ?? "outside";

            if (generationMode == "inside")
            {
                // --- Inside Mode ---
                // Ignore jsonData from request body, use stored config
                try
                {
                    finalData = await _templateProcessingService.ResolveInsideData(template.InsideDataConfig);
                }
                catch (System.Exception ex)
                {
                     // Handle errors during internal data resolution (e.g., invalid config JSON, SQL errors)
                     System.Console.WriteLine($"Error resolving inside data for template '{templateName}': {ex.Message}");
                     return StatusCode(500, $"Error resolving internal data for PDF generation: {ex.Message}");
                }

            }
            else // Default to 'outside' or if mode is anything else
            {
                // --- Outside Mode ---
                // Use jsonData from request body
                 if (jsonData == null || jsonData.Value.ValueKind != JsonValueKind.Object)
                 {
                     // If outside mode is requested but no valid JSON object body is provided
                     return BadRequest("Request body must be a valid JSON object for 'outside' mode.");
                 }
                 finalData = jsonData.Value;

                 // Optional: Apply fallback for missing fields in outside mode too?
                 // Or only in inside mode as requested. The service currently applies it
                 // based on placeholders in HTML if not found in provided JsonElement.
            }


            // Process the HTML content using the resolved (flat) data
            string processedHtml = _templateProcessingService.ProcessHtml(template.HtmlContent, finalData);

            var doc = new HtmlToPdfDocument()
            {
                GlobalSettings = {
                    ColorMode = ColorMode.Color,
                    Orientation = Orientation.Portrait,
                    PaperSize = PaperKind.A4,
                    Margins = new MarginSettings() { Top = 10, Bottom = 10, Left = 10, Right = 10 },
                    DPI = 300
                },
                Objects = {
                    new ObjectSettings() {
                        HtmlContent = processedHtml,
                        WebSettings = { DefaultEncoding = "utf-8" }
                        // Enable Javascript if needed - be cautious with security and performance
                        // EnableJavascript = true
                    }
                }
            };

            byte[] pdf = _converter.Convert(doc);

            if (pdf == null || pdf.Length == 0)
            {
                 // Log this server-side error for debugging
                System.Console.WriteLine($"wkhtmltopdf conversion failed for template '{templateName}'. Processed HTML length: {processedHtml.Length}");
                // You might want to inspect the 'processedHtml' here if debugging
                return StatusCode(500, "PDF generation failed. Check template content or wkhtmltopdf logs.");
            }

            // Generate a filename
             string filename = $"{template.Name}_{(generationMode == "inside" ? "internal" : "external")}_{DateTime.Now:yyyyMMddHHmmss}.pdf";

            return File(pdf, "application/pdf", filename);
        }
    }
}
```

```csharp
// File: Controllers/TemplateController.cs
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PdfGeneratorApp.Data;
using PdfGeneratorApp.Dtos;
using PdfGeneratorApp.Models;
using PdfGeneratorApp.Services;
using System;
using System.Linq;
using System.Threading.Tasks;
using System.Collections.Generic; // Add this

namespace PdfGeneratorApp.Controllers
{
    public class TemplateController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly TemplateProcessingService _templateProcessingService;

        public TemplateController(ApplicationDbContext context, TemplateProcessingService templateProcessingService)
        {
            _context = context;
            _templateProcessingService = templateProcessingService;
        }

        // GET: /templates/design/{templateName}
        [HttpGet("templates/design/{templateName}")]
        public async Task<IActionResult> Design(string templateName)
        {
            var template = await _context.Templates.FirstOrDefaultAsync(t => t.Name == templateName);
            if (template == null)
            {
                return NotFound($"Template '{templateName}' not found.");
            }

            var templateDto = new TemplateDetailDto
            {
                Id = template.Id,
                Name = template.Name,
                Description = template.Description,
                HtmlContent = template.HtmlContent,
                InsideDataConfig = template.InsideDataConfig, // Use new property
                CurrentVersion = template.CurrentVersion,
                LastModified = template.LastModified
            };

             // Pass available DB names for SQL config UI hint
             ViewBag.AvailableDatabases = _templateProcessingService.GetAvailableDatabaseNames();

            return View(templateDto);
        }

        // POST: /templates/design/{templateName}
        [HttpPost("templates/design/{templateName}")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Design(string templateName, [Bind("Id,Description,HtmlContent,InsideDataConfig")] TemplateUpdateDto templateDto) // Bind new property
        {
            // Note: We don't auto-generate InsideDataConfig on UPDATE POST
            // The user manages it manually or using the skeleton generator button

            if (ModelState.IsValid)
            {
                var existingTemplate = await _context.Templates.FindAsync(templateDto.Id);
                if (existingTemplate == null)
                {
                    return NotFound($"Template with ID {templateDto.Id} not found.");
                }

                if (templateName != existingTemplate.Name)
                {
                    return BadRequest("Template name mismatch between route and existing template.");
                }

                // Create a new version before updating the main template
                var newVersion = new TemplateVersion
                {
                    TemplateId = existingTemplate.Id,
                    VersionNumber = existingTemplate.CurrentVersion + 1,
                    HtmlContent = existingTemplate.HtmlContent,
                    Description = existingTemplate.Description,
                    InsideDataConfig = existingTemplate.InsideDataConfig, // Store old config
                    CreatedDate = existingTemplate.LastModified
                };
                _context.TemplateVersions.Add(newVersion);

                // Update the main template from DTO
                existingTemplate.Description = templateDto.Description;
                existingTemplate.HtmlContent = templateDto.HtmlContent;
                existingTemplate.InsideDataConfig = templateDto.InsideDataConfig; // Update with submitted config
                existingTemplate.CurrentVersion = newVersion.VersionNumber;
                existingTemplate.LastModified = DateTime.Now;

                await _context.SaveChangesAsync();
                TempData["Message"] = $"Template '{existingTemplate.Name}' updated to Version {existingTemplate.CurrentVersion} successfully!";
                return RedirectToAction(nameof(Design), new { templateName = existingTemplate.Name });
            }

            // If model state is invalid
            var currentTemplateState = await _context.Templates.FindAsync(templateDto.Id);
            var detailDto = new TemplateDetailDto
            {
                Id = currentTemplateState.Id,
                Name = currentTemplateState.Name,
                Description = templateDto.Description,
                HtmlContent = templateDto.HtmlContent,
                InsideDataConfig = templateDto.InsideDataConfig, // Use submitted config
                CurrentVersion = currentTemplateState.CurrentVersion,
                LastModified = currentTemplateState.LastModified
            };

             // Pass available DB names for SQL config UI hint
             ViewBag.AvailableDatabases = _templateProcessingService.GetAvailableDatabaseNames();

            return View(detailDto);
        }

        // GET: /templates/create
        public IActionResult Create()
        {
             // Pass available DB names for SQL config UI hint
            ViewBag.AvailableDatabases = _templateProcessingService.GetAvailableDatabaseNames();
            return View(new TemplateCreateDto { HtmlContent = "", InsideDataConfig = "" }); // Initialize config field
        }

        // POST: /templates/create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create([Bind("Name,HtmlContent,Description,InsideDataConfig")] TemplateCreateDto templateDto) // Bind new property
        {
            // Note: We don't auto-generate InsideDataConfig on CREATE POST
            // The user manages it manually or using the skeleton generator button

            if (ModelState.IsValid)
            {
                if (await _context.Templates.AnyAsync(t => t.Name == templateDto.Name))
                {
                    ModelState.AddModelError("Name", "A template with this name already exists.");
                    // Pass available DB names on error
                    ViewBag.AvailableDatabases = _templateProcessingService.GetAvailableDatabaseNames();
                    return View(templateDto);
                }

                var newTemplate = new Template
                {
                    Name = templateDto.Name,
                    Description = templateDto.Description,
                    HtmlContent = templateDto.HtmlContent,
                    InsideDataConfig = templateDto.InsideDataConfig, // Use submitted config
                    CurrentVersion = 1,
                    LastModified = DateTime.Now
                };

                _context.Add(newTemplate);
                await _context.SaveChangesAsync();

                var firstVersion = new TemplateVersion
                {
                    TemplateId = newTemplate.Id,
                    VersionNumber = 1,
                    HtmlContent = newTemplate.HtmlContent,
                    Description = newTemplate.Description,
                    InsideDataConfig = newTemplate.InsideDataConfig, // Store initial config
                    CreatedDate = newTemplate.LastModified
                };
                _context.TemplateVersions.Add(firstVersion);
                await _context.SaveChangesAsync();

                TempData["Message"] = $"Template '{newTemplate.Name}' created successfully!";
                return RedirectToAction(nameof(Design), new { templateName = newTemplate.Name });
            }
            // Pass available DB names on error
            ViewBag.AvailableDatabases = _templateProcessingService.GetAvailableDatabaseNames();
            return View(templateDto);
        }

        // GET: /templates/{templateName}/history
        [HttpGet("templates/{templateName}/history")]
        public async Task<IActionResult> History(string templateName)
        {
            var template = await _context.Templates
                                        .Include(t => t.Versions.OrderByDescending(v => v.VersionNumber))
                                        .FirstOrDefaultAsync(t => t.Name == templateName);
            if (template == null)
            {
                return NotFound($"Template '{templateName}' not found.");
            }

            var templateDetailDto = new TemplateDetailDto
            {
                Id = template.Id,
                Name = template.Name,
                Description = template.Description,
                HtmlContent = template.HtmlContent,
                InsideDataConfig = template.InsideDataConfig, // Include current config for context
                CurrentVersion = template.CurrentVersion,
                LastModified = template.LastModified
            };

            ViewBag.TemplateVersions = template.Versions
                .Select(v => new TemplateVersionDto
                {
                    Id = v.Id,
                    TemplateId = v.TemplateId,
                    VersionNumber = v.VersionNumber,
                    HtmlContent = v.HtmlContent,
                    Description = v.Description,
                    InsideDataConfig = v.InsideDataConfig, // Include historical config
                    CreatedDate = v.CreatedDate
                })
                .ToList();

            return View("~/Views/Template/History.cshtml", templateDetailDto);
        }


        // POST: /templates/{templateName}/revert/{versionNumber}
        [HttpPost("templates/{templateName}/revert/{versionNumber}")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Revert(string templateName, int versionNumber)
        {
            var template = await _context.Templates.FirstOrDefaultAsync(t => t.Name == templateName);
            if (template == null)
            {
                return NotFound($"Template '{templateName}' not found.");
            }

            if (versionNumber > template.CurrentVersion)
            {
                TempData["Error"] = $"Cannot revert to version {versionNumber}. Current version is {template.CurrentVersion}.";
                return RedirectToAction(nameof(History), new { templateName = template.Name });
            }

            var versionToRevert = await _context.TemplateVersions
                                                .FirstOrDefaultAsync(tv => tv.TemplateId == template.Id && tv.VersionNumber == versionNumber);

            if (versionToRevert == null)
            {
                TempData["Error"] = $"Version {versionNumber} for template '{templateName}' not found.";
                return RedirectToAction(nameof(History), new { templateName = template.Name });
            }

            // Create a new version of the *current* state before reverting
            var currentVersionSnapshot = new TemplateVersion
            {
                TemplateId = template.Id,
                VersionNumber = template.CurrentVersion + 1,
                HtmlContent = template.HtmlContent,
                Description = template.Description,
                InsideDataConfig = template.InsideDataConfig, // Store current config snapshot
                CreatedDate = template.LastModified
            };
            _context.TemplateVersions.Add(currentVersionSnapshot);

            // Now update the main template to the reverted version's content
            template.HtmlContent = versionToRevert.HtmlContent;
            template.Description = versionToRevert.Description;
            template.InsideDataConfig = versionToRevert.InsideDataConfig; // Revert config
            template.CurrentVersion = currentVersionSnapshot.VersionNumber;
            template.LastModified = DateTime.Now;

            _context.Templates.Update(template);
            await _context.SaveChangesAsync();

            TempData["Message"] = $"Template '{template.Name}' successfully reverted to version {versionNumber}. The previous state is saved as version {currentVersionSnapshot.VersionNumber}.";
            return RedirectToAction(nameof(Design), new { templateName = template.Name });
        }
    }
}
```

```csharp
// File: Controllers/DocsController.cs
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PdfGeneratorApp.Data;
using PdfGeneratorApp.Dtos;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using PdfGeneratorApp.Services; // Add this

namespace PdfGeneratorApp.Controllers
{
    public class DocsController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly TemplateProcessingService _templateProcessingService; // Inject the service

        public DocsController(ApplicationDbContext context, TemplateProcessingService templateProcessingService) // Update constructor
        {
            _context = context;
            _templateProcessingService = templateProcessingService; // Assign service
        }

        // GET: /docs/templates
        public async Task<IActionResult> Templates()
        {
            List<TemplateDetailDto> templatesForDocs = await _context.Templates
                                        .Select(t => new TemplateDetailDto
                                        {
                                            Id = t.Id,
                                            Name = t.Name,
                                            Description = t.Description,
                                            InsideDataConfig = t.InsideDataConfig, // Use new property for docs example
                                            // HtmlContent is potentially large, only include if strictly needed for docs list
                                            // HtmlContent = t.HtmlContent,
                                            CurrentVersion = t.CurrentVersion,
                                            LastModified = t.LastModified
                                        })
                                        .ToListAsync();

            // Pass the service to the view via ViewBag or Model if needed for client-side JSON formatting logic
            // Or call the service here and pass the generated JSON strings to the DTOs
            foreach(var template in templatesForDocs)
            {
                template.ExampleJsonData = _templateProcessingService.GenerateOutsideModeExamplePayload(template.InsideDataConfig);
                 // Null out InsideDataConfig now that ExampleJsonData is set for the view
                 template.InsideDataConfig = null;
            }


            return View(templatesForDocs);
        }
    }
}
```

```json
// File: appsettings.json (Example structure)
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*",
  "ConnectionStrings": {
    "cs": "Server=(localdb)\\mssqllocaldb;Database=PdfGeneratorAppDb;Trusted_Connection=True;MultipleActiveResultSets=true",
    // Add connection strings for databases you want to query from 'inside' mode
    "CustomersDb": "Server=.;Database=Customers;Integrated Security=True;",
    "OrdersDb": "Server=.;Database=Orders;Integrated Security=True;"
    // ... other database connection strings
  }
}
```

```csharp
// File: Program.cs
using Microsoft.EntityFrameworkCore;
using PdfGeneratorApp.Data;
using PdfGeneratorApp.Services;
using WkHtmlToPdfDotNet;
using WkHtmlToPdfDotNet.Contracts;
using Microsoft.Extensions.Configuration; // Add this

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllersWithViews();

// Configure SQL Server DbContext
builder.Services.AddDbContext<ApplicationDbContext>(optionBuilder =>
{
    optionBuilder.UseSqlServer(builder.Configuration.GetConnectionString("cs"));
});

// Add wkhtmltopdf services
builder.Services.AddSingleton(typeof(IConverter), new SynchronizedConverter(new PdfTools()));

// Add Template Processing Service and inject configuration
builder.Services.AddScoped<TemplateProcessingService>();


var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthorization();

// Seed initial data on startup if database is empty
using (var scope = app.Services.CreateScope())
{
    var dbContext = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
    try
    {
        dbContext.Database.Migrate(); // Applies any pending migrations
        // Optional: Add seeding logic here if needed
        // var serviceProvider = scope.ServiceProvider;
        // SeedData.Initialize(serviceProvider); // Assuming you have a SeedData class
    }
    catch (Exception ex)
    {
        var logger = scope.ServiceProvider.GetRequiredService<ILogger<Program>>();
        logger.LogError(ex, "An error occurred while migrating or seeding the database.");
        // Optionally, handle this error more gracefully in production
    }
}


app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

// Custom routes remain the same, but the Generate POST action behavior changes
app.MapControllerRoute(
    name: "pdfGenerate",
    pattern: "pdf/generate/{templateName}",
    defaults: new { controller = "Pdf", action = "Generate" });

app.MapControllerRoute(
    name: "templateDesign",
    pattern: "templates/design/{templateName}",
    defaults: new { controller = "Template", action = "Design" });

app.MapControllerRoute(
    name: "templateHistory",
    pattern: "templates/{templateName}/history",
    defaults: new { controller = "Template", action = "History" });

app.MapControllerRoute(
    name: "templateRevert",
    pattern: "templates/{templateName}/revert/{versionNumber}",
    defaults: new { controller = "Template", action = "Revert" });


app.Run();
```

```cshtml
@* File: Views/Templates/Templates.cshtml (Docs Page) *@
@* Model type changed to List<TemplateDetailDto> as it's now used *after* processing in controller *@
@using PdfGeneratorApp.Dtos
@using System.Text.Json
@model List<TemplateDetailDto> @* Changed model type *@

@{
    ViewData["Title"] = "API Documentation";
}

<div class="container">
    <div class="page-header">
        <h1>@ViewData["Title"]</h1>
        <p class="page-subtitle">
            Test and understand the PDF generation API endpoints. Each template has a unique endpoint.
        </p>
        <div class="alert alert-info mt-4" role="alert">
             <i class="fas fa-info-circle"></i>
             <strong>Important:</strong> The POST endpoint <code>/pdf/generate/{templateName}</code> supports two modes, controlled by the <code>mode</code> query parameter (e.g., <code>/pdf/generate/Invoice?mode=inside</code>).
             <ul>
                 <li><strong><code>mode=outside</code> (Default):</strong> Requires a JSON payload in the request body. The example below shows the expected structure.</li>
                 <li><strong><code>mode=inside</code>:</strong> Ignores the request body payload and uses data configured internally for the template (static values or SQL queries defined in the 'Inside Data Config').</li>
             </ul>
        </div>
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
                            <code class="me-2 fs-6">/pdf/generate/@template.Name?mode=outside</code> @* Show default mode in docs URL *@
                            <span class="text-muted small">@template.Description</span>
                        </button>
                    </h2>
                    <div id="@collapseId" class="accordion-collapse collapse" aria-labelledby="@headingId" data-bs-parent="#templateDocsAccordion">
                        <div class="accordion-body">
                            <h5>Endpoint Summary</h5>
                            <p>Generates a PDF document based on the <strong>@template.Name</strong> template.</p>
                            <ul>
                                <li><strong>Mode:</strong> Controlled by the <code>mode</code> query parameter (<code>outside</code> or <code>inside</code>). Defaults to <code>outside</code>.</li>
                                <li><strong><code>mode=outside</code>:</strong> Requires a JSON object in the request body. Example payload based on template configuration is shown below.</li>
                                <li><strong><code>mode=inside</code>:</strong> Does NOT use the request body. Uses the <a href="@Url.Action("Design", "Template", new { templateName = template.Name })#insideDataConfigSection">Inside Data Config</a> defined for this template.</li>
                            </ul>


                            <hr class="my-3" />

                            <div class="try-it-out-section" data-template-name="@template.Name">
                                <h5><i class="fas fa-vial me-1"></i> Try it out (Outside Mode Example)</h5>
                                <p class="small text-muted">Modify the example JSON payload below and click "Execute" to test PDF generation using the <code>mode=outside</code> query parameter.</p>

                                <div class="form-group">
                                    <label for="@jsonDataTextareaId" class="form-label fw-semibold">Example Request Body (<code>application/json</code>)</label>
                                     @* ExampleJsonData now holds the generated OUTSIDE payload *@
                                    <textarea class="form-control json-payload" id="@jsonDataTextareaId" rows="10" style="font-family: monospace; font-size: 0.875em;">@template.ExampleJsonData</textarea>
                                </div>

                                <div class="mt-3">
                                    <button type="button" class="btn btn-success execute-btn">
                                        <i class="fas fa-play-circle"></i> Execute (mode=outside)
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

@* No longer need FormatJsonForTextarea helper here, done in Controller *@

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
                    $responseStatusDiv.empty().removeClass('text-danger text-success text-warning alert alert-danger alert-success alert-warning');
                    $responseOutputDiv.empty().removeClass('text-danger text-success text-warning');
                    $clearButton.hide();

                    try {
                        // Attempt to parse the JSON payload from the textarea
                        payload = JSON.parse(jsonDataString);
                    } catch (e) {
                        $responseStatusDiv.html('<strong>Error:</strong> Invalid JSON in payload.').addClass('alert alert-danger');
                        $responseOutputDiv.text(e.message).addClass('text-danger');
                        $responseSection.show();
                        $clearButton.show();
                        return;
                    }

                    $button.prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Executing...');

                    // Use the POST endpoint with mode=outside query parameter
                    fetch(`/pdf/generate/${templateName}?mode=outside`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload) // Send the parsed JSON as the body
                    })
                    .then(response => {
                        const contentType = response.headers.get('content-type');
                        if (response.ok && contentType && contentType.includes('application/pdf')) {
                            // Handle PDF response (download)
                            return response.blob().then(blob => ({
                                blob: blob, isPdf: true, status: response.status, statusText: response.statusText, headers: response.headers, ok: response.ok
                            }));
                        } else {
                            // Handle non-PDF (likely error) response
                            return response.text().then(text => ({
                                text: text, isPdf: false, status: response.status, statusText: response.statusText, headers: response.headers, ok: response.ok
                            }));
                        }
                    })
                    .then(result => {
                        $responseStatusDiv.html(`<strong>Status:</strong> ${result.status} ${result.statusText}`);
                        if (result.isPdf) {
                            // If PDF, create download link
                            const url = window.URL.createObjectURL(result.blob);
                            const a = document.createElement('a');
                            const suggestedFilename = result.headers.get('content-disposition')?.split('filename=')[1]?.split(';')[0]?.replace(/"/g, '') || `${templateName}_API_Test.pdf`;
                            a.href = url;
                            a.download = suggestedFilename;
                            a.innerHTML = `<i class="fas fa-download me-1"></i> Download ${suggestedFilename}`;
                            a.className = 'btn btn-sm btn-success d-block mt-2';
                            $responseOutputDiv.html($('<div>').html('PDF generated successfully.')); // Use html() to clear previous content
                            $responseOutputDiv.append(a);
                            $responseStatusDiv.addClass('alert alert-success');
                             // Clean up blob URL after download link is created (or after click if preferred)
                             // window.URL.revokeObjectURL(url); // Can revoke later, or when link is clicked/removed
                        } else {
                            // If not PDF, show the response text (likely error message)
                            $responseOutputDiv.text(result.text);
                            if(result.ok){ $responseStatusDiv.addClass('alert alert-warning'); } // Warning for non-PDF OK status?
                            else { $responseStatusDiv.addClass('alert alert-danger'); } // Error for non-OK status
                        }
                    })
                    .catch(error => {
                        console.error('Fetch Error:', error);
                        $responseStatusDiv.html('<strong>Network/Fetch Error</strong>').addClass('alert alert-danger');
                        $responseOutputDiv.text(error.message).addClass('text-danger');
                    })
                    .finally(() => {
                        $button.prop('disabled', false).html('<i class="fas fa-play-circle"></i> Execute (mode=outside)');
                        $responseSection.show();
                        $clearButton.show();
                    });
                });

                $('.clear-response-btn').on('click', function() {
                    var $tryItOutSection = $(this).closest('.try-it-out-section');
                    $tryItOutSection.find('.response-section').hide();
                    $tryItOutSection.find('.response-status').empty().removeClass('text-danger text-success text-warning alert alert-danger alert-success alert-warning');
                    $tryItOutSection.find('.response-output').empty().removeClass('text-danger text-success text-warning').html(''); // Use html('') to clear potential child elements like the download link
                    $(this).hide();
                });
            });
    </script>
}
```

```cshtml
@* File: Views/Template/Create.cshtml *@
@model PdfGeneratorApp.Dtos.TemplateCreateDto

@{
    ViewData["Title"] = "Create New Template";
    var availableDatabases = ViewBag.AvailableDatabases as List<string> ?? new List<string>();
}

<div class="container">
    <div class="page-header">
        <h1>@ViewData["Title"]</h1>
        <p class="page-subtitle">Define the details and initial content for your new PDF template.</p>
    </div>

    <div class="row">
        <div class="col-md-12">
            <form asp-action="Create" method="post">
                <div asp-validation-summary="ModelOnly" class="text-danger"></div>
                <div class="form-group mb-3">
                    <label asp-for="Name" class="control-label"></label>
                    <input asp-for="Name" class="form-control" />
                    <span asp-validation-for="Name" class="text-danger"></span>
                </div>
                <div class="form-group mb-3">
                    <label asp-for="Description" class="control-label"></label>
                    <input asp-for="Description" class="form-control" />
                    <span asp-validation-for="Description" class="text-danger"></span>
                </div>

                <div class="mb-3">
                    <h5>HTML Content:</h5>
                    <div class="form-group mb-3">
                        <label for="htmlEditor" class="control-label">Edit HTML Content:</label>
                        <textarea asp-for="HtmlContent" class="form-control" rows="15" id="htmlEditor"></textarea>
                        <span asp-validation-for="HtmlContent" class="text-danger"></span>
                        <small class="form-text text-muted">Use <code>&lt;&lt;FieldName&gt;&gt;</code> for dynamic data placeholders.</small>
                    </div>
                    <p class="text-center my-3">OR Upload an HTML file to populate the editor:</p>
                    <div class="form-group mb-3">
                        <label for="htmlFile" class="form-label">Upload HTML File (.html):</label>
                        <input type="file" id="htmlFile" name="htmlFile" class="form-control" accept=".html,.htm" />
                    </div>
                     <div id="uploadStatus" class="mt-2"></div>
                </div>

                @* New section for Inside Data Config *@
                <div class="form-group mb-3">
                    <label asp-for="InsideDataConfig" class="control-label"></label>
                     <small class="form-text text-muted d-block mb-2">
                         Configure data sources for 'inside' mode PDF generation. Structure: <code>{ "FieldName": { "type": "static|sql", "value": "...", "database": "..."(for sql) } }</code>
                         Available databases: @(availableDatabases.Any() ? string.Join(", ", availableDatabases) : "None configured in appsettings.json")
                     </small>
                     <button type="button" id="generateConfigSkeletonBtn" class="btn btn-sm btn-outline-secondary mb-2">
                         <i class="fas fa-magic me-1"></i> Generate Skeleton from HTML Placeholders
                     </button>
                    <textarea asp-for="InsideDataConfig" class="form-control" rows="10" id="insideDataConfigEditor"></textarea>
                    <span asp-validation-for="InsideDataConfig" class="text-danger"></span>
                     <small class="form-text text-muted">
                         Provide the JSON configuration for resolving data in 'inside' mode. This is not the raw data itself.
                     </small>
                </div>

                <div class="form-group mt-4">
                    <input type="submit" value="Create Template" class="btn btn-primary" />
                    <a asp-action="Index" asp-controller="Home" class="btn btn-secondary">Back to List</a>
                </div>
            </form>
        </div>
    </div>
</div>

@section Scripts {
    @{await Html.RenderPartialAsync("_ValidationScriptsPartial");}

    <link href="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.js"></script>
     <script src="https://cdnjs.cloudflare.com/ajax/libs/json5/2.2.3/json5.min.js"></script> @* Add JSON5 for parsing potentially lax user JSON *@


    <script>
        $(document).ready(function() {
            var htmlEditor = $('#htmlEditor');
            var uploadStatus = $('#uploadStatus');
            var insideDataConfigEditor = $('#insideDataConfigEditor'); // Renamed textarea
            var generateConfigSkeletonBtn = $('#generateConfigSkeletonBtn'); // New button


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

            // --- Auto-format InsideDataConfig JSON on load ---
            try {
                var rawJson = insideDataConfigEditor.val();
                if (rawJson && rawJson.trim()) {
                    // Use JSON5 to be more lenient with user input before strict JSON.parse
                    var parsedJson = JSON5.parse(rawJson);
                    insideDataConfigEditor.val(JSON.stringify(parsedJson, null, 2));
                } else {
                     insideDataConfigEditor.val("{}"); // Start with empty JSON object
                }
            } catch (e) {
                console.error("Failed to parse existing InsideDataConfig JSON:", e);
                // Optionally, alert the user or show an error message near the textarea
                 uploadStatus.html('<div class="alert alert-warning">Warning: Existing Inside Data Config JSON is invalid. Please correct it.</div>');
            }

            // Function to show status messages
            function showStatus(message, type = 'info') {
                 // Use a dedicated status element or append below the file input
                $('#uploadStatus').html(`<div class="alert alert-${type} mt-2">${message}</div>`);
            }

            // --- HTML File Upload ---
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
                    // If file is cleared, clear status
                     $('#uploadStatus').html('');
                }
            });

            // --- Generate InsideDataConfig Skeleton ---
            generateConfigSkeletonBtn.on('click', function() {
                // Get HTML content from the editor
                var htmlContent = htmlEditor.summernote('code');

                // Find all placeholders like <<FieldName>> or &lt;&lt;FieldName&gt;&gt;
                var placeholders = (htmlContent.match(/&lt;&lt;(\w+)&gt;&gt;/g) || [])
                                    .map(match => match.replace(/&lt;&lt;|&gt;&gt;/g, ''));
                placeholders = placeholders.concat((htmlContent.match(/<<(\w+)>>/g) || [])
                                    .map(match => match.replace(/<<|>>/g, '')));

                // Get unique placeholders
                placeholders = [...new Set(placeholders)];

                // Get current JSON config from the editor
                var currentConfig = {};
                 try {
                     var rawCurrentJson = insideDataConfigEditor.val();
                      if (rawCurrentJson && rawCurrentJson.trim()) {
                         // Use JSON5 for lenient parsing
                         currentConfig = JSON5.parse(rawCurrentJson);
                         if (typeof currentConfig !== 'object' || currentConfig === null) {
                            currentConfig = {}; // If not an object, start fresh
                         }
                      }
                 } catch (e) {
                     console.warn("Existing Inside Data Config JSON is invalid, generating fresh skeleton.", e);
                     currentConfig = {}; // If invalid, ignore existing and generate fresh
                     uploadStatus.html('<div class="alert alert-warning mt-2">Warning: Existing Inside Data Config JSON was invalid. Generated a new skeleton.</div>');
                 }


                // Build the new config, keeping existing entries if they exist
                var newConfig = {};
                placeholders.forEach(function(fieldName) {
                    if (currentConfig.hasOwnProperty(fieldName) && typeof currentConfig[fieldName] === 'object' && currentConfig[fieldName] !== null) {
                        // Keep the existing valid config for this field
                        newConfig[fieldName] = currentConfig[fieldName];
                    } else {
                        // Add a skeleton entry if it doesn't exist or was invalid
                        newConfig[fieldName] = {
                            "type": "static",
                            "value": ""
                            // Add SQL example properties here if desired in skeleton
                            // "sql_example_value": "SELECT ...",
                            // "sql_example_database": "YourDbName"
                        };
                    }
                });

                 // Optional: Remove entries from newConfig that are no longer in the HTML
                 // This might be too aggressive, keeping them allows pre-configuring fields before adding to HTML
                 // Object.keys(currentConfig).forEach(fieldName => {
                 //     if (!placeholders.includes(fieldName)) {
                 //         // Field exists in old config but not in HTML, decide if you want to keep or remove it
                 //         // For now, the above logic implicitly keeps it if it was in currentConfig
                 //     }
                 // });


                // Format and set the new JSON in the textarea
                insideDataConfigEditor.val(JSON.stringify(newConfig, null, 2));
            });
        });
    </script>
}
```

```cshtml
@* File: Views/Template/Design.cshtml *@
@model PdfGeneratorApp.Dtos.TemplateDetailDto

@{
    ViewData["Title"] = $"Design Template: {Model.Name}";
    var availableDatabases = ViewBag.AvailableDatabases as List<string> ?? new List<string>();
}

<div class="container">
    <div class="page-header">
        <h1>@ViewData["Title"]</h1>
        <p class="page-subtitle">Edit the HTML content and configuration for the <strong>@Model.Name</strong> template.</p>
    </div>

    <div class="row">
        <div class="col-md-12">
            <form asp-action="Design" asp-route-templateName="@Model.Name" method="post">
                <div asp-validation-summary="ModelOnly" class="text-danger"></div>
                <input type="hidden" asp-for="Id" />

                <div class="form-group mb-3">
                    <label class="control-label">Template Name:</label>
                    <input value="@Model.Name" class="form-control" readonly />
                </div>
                <div class="form-group mb-3">
                    <label class="control-label">Current Version:</label>
                    <input value="@Model.CurrentVersion" class="form-control" readonly />
                </div>
                <div class="form-group mb-3">
                    <label class="control-label">Last Modified:</label>
                    <input value="@Model.LastModified.ToString("g")" class="form-control" readonly />
                </div>

                <div class="form-group mb-3">
                    <label asp-for="Description" class="control-label"></label>
                    <input asp-for="Description" class="form-control" />
                    <span asp-validation-for="Description" class="text-danger"></span>
                </div>

                <div class="form-group mb-3">
                    <label asp-for="HtmlContent" class="control-label"></label>
                    <textarea asp-for="HtmlContent" class="form-control" rows="15" id="htmlEditor"></textarea>
                    <span asp-validation-for="HtmlContent" class="text-danger"></span>
                    <small class="form-text text-muted">Use <code>&lt;&lt;FieldName&gt;&gt;</code> for dynamic data placeholders.</small>
                </div>

                 @* New section for Inside Data Config *@
                <div class="form-group mb-3" id="insideDataConfigSection">
                    <label asp-for="InsideDataConfig" class="control-label"></label>
                     <small class="form-text text-muted d-block mb-2">
                         Configure data sources for 'inside' mode PDF generation. Structure: <code>{ "FieldName": { "type": "static|sql", "value": "...", "database": "..."(for sql) } }</code>
                         Available databases: @(availableDatabases.Any() ? string.Join(", ", availableDatabases) : "None configured in appsettings.json")
                     </small>
                     <button type="button" id="generateConfigSkeletonBtn" class="btn btn-sm btn-outline-secondary mb-2">
                         <i class="fas fa-magic me-1"></i> Generate Skeleton from HTML Placeholders
                     </button>
                    <textarea asp-for="InsideDataConfig" class="form-control" rows="10" id="insideDataConfigEditor"></textarea>
                    <span asp-validation-for="InsideDataConfig" class="text-danger"></span>
                     <small class="form-text text-muted">
                         Provide the JSON configuration for resolving data in 'inside' mode. This is not the raw data itself.
                     </small>
                </div>


                <div class="form-group mt-4">
                    <input type="submit" value="Save Changes" class="btn btn-primary" />
                    <a asp-action="Index" asp-controller="Home" class="btn btn-secondary">Back to Templates</a>
                    <a asp-controller="Template" asp-action="History" asp-route-templateName="@Model.Name" class="btn btn-info">View History</a>
                    <button type="button" id="downloadPdfBtn" class="btn btn-success">Download Test PDF (Outside Mode)</button> @* Clarify test mode *@
                </div>
            </form>
        </div>
    </div>
</div>

@section Scripts {
    @{await Html.RenderPartialAsync("_ValidationScriptsPartial");}

    <link href="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/json5/2.2.3/json5.min.js"></script> @* Add JSON5 for parsing potentially lax user JSON *@


    <script>
        $(document).ready(function() {
            var htmlEditor = $('#htmlEditor');
            var insideDataConfigEditor = $('#insideDataConfigEditor'); // Renamed textarea
             var generateConfigSkeletonBtn = $('#generateConfigSkeletonBtn'); // New button


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

            // --- Auto-format InsideDataConfig JSON on load ---
            try {
                var rawJson = insideDataConfigEditor.val();
                if (rawJson && rawJson.trim()) {
                     // Use JSON5 to be more lenient with user input before strict JSON.parse
                    var parsedJson = JSON5.parse(rawJson);
                    insideDataConfigEditor.val(JSON.stringify(parsedJson, null, 2));
                } else {
                     insideDataConfigEditor.val("{}"); // Start with empty JSON object if current is null/empty
                }
            } catch (e) {
                console.error("Failed to parse existing InsideDataConfig JSON:", e);
                 // Optionally, alert the user or show an error message near the textarea
                 $('#insideDataConfigSection .form-text.text-danger').text('Warning: Existing Inside Data Config JSON is invalid. Please correct it.');
            }

             // --- Generate InsideDataConfig Skeleton ---
            generateConfigSkeletonBtn.on('click', function() {
                // Get HTML content from the editor
                var htmlContent = htmlEditor.summernote('code');

                // Find all placeholders like <<FieldName>> or &lt;&lt;FieldName&gt;&gt;
                 var placeholders = (htmlContent.match(/&lt;&lt;(\w+)&gt;&gt;/g) || [])
                                    .map(match => match.replace(/&lt;&lt;|&gt;&gt;/g, ''));
                placeholders = placeholders.concat((htmlContent.match(/<<(\w+)>>/g) || [])
                                    .map(match => match.replace(/<<|>>/g, '')));


                // Get unique placeholders
                placeholders = [...new Set(placeholders)];

                // Get current JSON config from the editor
                var currentConfig = {};
                 try {
                     var rawCurrentJson = insideDataConfigEditor.val();
                      if (rawCurrentJson && rawCurrentJson.trim()) {
                         // Use JSON5 for lenient parsing
                         currentConfig = JSON5.parse(rawCurrentJson);
                         if (typeof currentConfig !== 'object' || currentConfig === null) {
                            currentConfig = {}; // If not an object, start fresh
                         }
                      }
                 } catch (e) {
                     console.warn("Existing Inside Data Config JSON is invalid, generating fresh skeleton.", e);
                     currentConfig = {}; // If invalid, ignore existing and generate fresh
                      $('#insideDataConfigSection .form-text.text-danger').text('Warning: Existing Inside Data Config JSON was invalid. Generated a new skeleton.');
                 }


                // Build the new config, keeping existing entries if they exist
                var newConfig = {};
                placeholders.forEach(function(fieldName) {
                    if (currentConfig.hasOwnProperty(fieldName) && typeof currentConfig[fieldName] === 'object' && currentConfig[fieldName] !== null) {
                        // Keep the existing valid config for this field
                        newConfig[fieldName] = currentConfig[fieldName];
                    } else {
                        // Add a skeleton entry if it doesn't exist or was invalid
                        newConfig[fieldName] = {
                            "type": "static",
                            "value": ""
                        };
                    }
                });

                // Format and set the new JSON in the textarea
                insideDataConfigEditor.val(JSON.stringify(newConfig, null, 2));
            });


            // Test PDF Download Button (Now explicitly Outside Mode)
            $('#downloadPdfBtn').on('click', function() {
                var templateName = '@Model.Name';
                 // For OUTSIDE mode testing, we need sample data.
                 // The API docs page uses the InsideDataConfig to generate an example.
                 // Here, let's just send an empty object or a minimal structure,
                 // or you could add another textarea specifically for test payload JSON.
                 // For simplicity, let's send an empty object, but this might not test complex templates.
                 // A better approach is a dedicated test data textarea or deriving from InsideDataConfig like the docs.
                 // Let's derive a simple example from the InsideDataConfig keys like the docs page.
                var testJsonData;
                 try {
                     var configJson = insideDataConfigEditor.val();
                      if (configJson && configJson.trim()) {
                          var config = JSON5.parse(configJson); // Use JSON5 for parsing user input
                          if (typeof config === 'object' && config !== null) {
                               testJsonData = {};
                              for (const fieldName in config) {
                                   if (config.hasOwnProperty(fieldName)) {
                                        // Suggest a default value for the OUTSIDE payload
                                        if (fieldName.startsWith("is") || fieldName.startsWith("has")) {
                                            // Suggest boolean false
                                            testJsonData[fieldName] = false;
                                        }
                                        else {
                                            // Suggest a generic string value
                                            testJsonData[fieldName] = "Sample Value";
                                        }
                                   }
                              }
                          } else {
                              testJsonData = {"FieldName": "Sample Value"}; // Default if config is invalid/empty
                          }
                      } else {
                          testJsonData = {"FieldName": "Sample Value"}; // Default if no config
                      }

                 } catch (e) {
                      console.error("Failed to generate test JSON from config:", e);
                      testJsonData = {"ErrorGeneratingTestData": "Invalid Inside Data Config JSON"};
                 }


                var endpoint = `/pdf/generate/${templateName}?mode=outside`; // Explicitly call outside mode

                // Use fetch API
                fetch(endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(testJsonData) // Send the derived test data
                })
                .then(response => {
                    if (!response.ok) {
                        return response.text().then(text => {
                            throw new Error(`HTTP error! status: ${response.status} - ${text}`);
                        });
                    }
                    return response.blob(); // Get the response as a Blob (for PDF)
                })
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `${templateName}_Test_Outside.pdf`; // Suggest a filename with mode
                    document.body.appendChild(a);
                    a.click(); // Trigger download
                    a.remove(); // Clean up the element
                    window.URL.revokeObjectURL(url); // Release the object URL
                })
                .catch(error => {
                    alert('There was a problem generating the PDF: ' + error.message);
                    console.error('PDF Generation Error:', error);
                });
            });
        });
    </script>
}
```

```cshtml
@* File: Views/Template/History.cshtml *@
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
                    @foreach (var version in versions.OrderByDescending(v => v.VersionNumber)) @* Ensure ordered descending *@
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
                                    <form asp-action="Revert" asp-route-templateName="@Model.Name" asp-route-versionNumber="@version.VersionNumber" method="post" class="d-inline needs-confirmation" data-confirmation-message="Are you sure you want to revert to version @version.VersionNumber? This will create a new version (@(Model.CurrentVersion + 1)) of the current state before reverting.">
                                        @Html.AntiForgeryToken()
                                        <button type="submit" class="btn btn-sm btn-warning" title="Revert to this version">
                                            <i class="fas fa-undo"></i> Revert
                                        </button>
                                    </form>
                                }
                                 @* Optional: Add a "View Config" button/modal to see InsideDataConfig/HtmlContent for this version *@
                                 @* <button type="button" class="btn btn-sm btn-outline-info" data-bs-toggle="modal" data-bs-target="#versionDetailModal" data-version-id="@version.Id">View Details</button> *@
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

    @* Optional: Modal for viewing version details (HtmlContent, InsideDataConfig) *@
     @*
     <div class="modal fade" id="versionDetailModal" tabindex="-1" aria-labelledby="versionDetailModalLabel" aria-hidden="true">
         <div class="modal-dialog modal-lg">
             <div class="modal-content">
                 <div class="modal-header">
                     <h5 class="modal-title" id="versionDetailModalLabel">Version Details</h5>
                     <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                 </div>
                 <div class="modal-body">
                     Loading...
                 </div>
                 <div class="modal-footer">
                     <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                 </div>
             </div>
         </div>
     </div>
     *@
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

             // Optional: JavaScript for the modal to load version details via AJAX
             // $('#versionDetailModal').on('show.bs.modal', function (event) {
             //     var button = $(event.relatedTarget); // Button that triggered the modal
             //     var versionId = button.data('version-id'); // Extract info from data-* attributes
             //     var modalBody = $(this).find('.modal-body');
             //     modalBody.html('Loading...'); // Show loading text

             //     // Implement AJAX call to fetch version details (HtmlContent, InsideDataConfig)
             //     // You would need a new controller action to return TemplateVersionDto JSON by Id
             //     // fetch(`/api/templateversions/${versionId}`) // Example API endpoint
             //     //     .then(response => response.json())
             //     //     .then(data => {
             //     //         modalBody.html(`
             //     //             <h6>HTML Content</h6>
             //     //             <pre style="white-space: pre-wrap; word-break: break-all;">${data.htmlContent}</pre>
             //     //             <h6>Inside Data Config</h6>
             //     //             <pre style="white-space: pre-wrap; word-break: break-all;">${data.insideDataConfig ? JSON.stringify(JSON.parse(data.insideDataConfig), null, 2) : 'No config'}</pre>
             //     //         `);
             //     //     })
             //     //     .catch(error => {
             //     //         modalBody.html('<div class="alert alert-danger">Could not load version details.</div>');
             //     //         console.error('Error loading version details:', error);
             //     //     });
             // });
        });
    </script>
}
```

```css
/* File: site.css */
/* (Add these styles or integrate them into your existing site.css based on the previous prompt) */

:root {
    --aman-teal: #4ECDC4;
    --aman-dark-teal: #2D8B85;
    --aman-light-gray: #F8F9FA;
    --aman-medium-gray: #E9ECEF;
    --aman-dark-gray: #6C757D;
    --aman-text-color: #212529;
    --aman-white: #FFFFFF;
    --aman-black: #000000;

    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
}

body {
    font-family: 'Cairo', sans-serif;
    background-color: var(--aman-light-gray);
    color: var(--aman-text-color);
    line-height: 1.6;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
}

.main-content {
    flex-grow: 1;
}

.site-logo {
    height: 30px;
    vertical-align: middle;
}

.site-navbar {
    background-color: var(--aman-white);
    box-shadow: var(--shadow-sm);
}

.site-navbar .navbar-brand {
    font-weight: 700;
    color: var(--aman-dark-teal);
    display: flex;
    align-items: center;
}

.site-navbar .navbar-nav .nav-link {
    color: var(--aman-text-color);
    font-weight: 600;
    transition: color 0.2s ease;
}

.site-navbar .navbar-nav .nav-link:hover,
.site-navbar .navbar-nav .nav-link.active {
    color: var(--aman-teal);
}

.site-navbar .navbar-toggler {
    border-color: var(--aman-medium-gray);
}

.page-header {
    text-align: center;
    margin-bottom: 3rem;
}

.page-header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--aman-text-color);
    margin-bottom: 0.5rem;
}

.page-header .page-subtitle {
    font-size: 1.1rem;
    color: var(--aman-dark-gray);
    max-width: 700px;
    margin: 0.5rem auto 0;
}

.stats-bar {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}

.stat-item {
    text-align: center;
    padding: 1rem;
    background-color: var(--aman-white);
    border-radius: 8px;
    box-shadow: var(--shadow-sm);
    min-width: 120px;
    border: 1px solid var(--aman-medium-gray);
}

.stat-number {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--aman-teal);
    line-height: 1;
    margin-bottom: 0.25rem;
}

.stat-label {
    font-size: 0.9rem;
    color: var(--aman-dark-gray);
    font-weight: 600;
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
    border: 1px solid var(--aman-medium-gray);
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    background-color: var(--aman-white);
    color: var(--aman-text-color);
}

.search-box .form-control::placeholder {
    color: var(--aman-dark-gray);
}

.search-box .form-control:focus {
    outline: none;
    border-color: var(--aman-teal);
    box-shadow: 0 0 0 0.25rem rgba(78, 205, 196, 0.25);
    background-color: var(--aman-white);
}

.search-box .search-icon {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--aman-dark-gray);
    font-size: 1rem;
    pointer-events: none;
}

.btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: center;
}

.btn-primary {
    background-color: var(--aman-teal);
    color: var(--aman-white);
    box-shadow: var(--shadow-sm);
}

.btn-primary:hover {
    background-color: var(--aman-dark-teal);
    color: var(--aman-white);
}

.btn-secondary {
    background-color: var(--aman-medium-gray);
    color: var(--aman-text-color);
    border: 1px solid var(--aman-medium-gray);
}

.btn-secondary:hover {
    background-color: var(--aman-dark-gray);
    color: var(--aman-white);
    border-color: var(--aman-dark-gray);
}

.btn-sm {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
    border-radius: 6px;
}

/* Styling custom buttons using Bootstrap classes */
.btn-design,
.btn-info {
    background-color: var(--aman-medium-gray);
    color: var(--aman-text-color);
}

.btn-design:hover,
.btn-info:hover {
    background-color: var(--aman-dark-gray);
    color: var(--aman-white);
}

.btn-warning {
     background-color: #ffc107; /* Standard Bootstrap warning */
     color: #212529;
}

.btn-warning:hover {
     background-color: #ffaf02;
     color: #212529;
}

.btn-success {
     background-color: var(--aman-teal); /* Use teal for success/execute/download */
     color: var(--aman-white);
}

.btn-success:hover {
     background-color: var(--aman-dark-teal);
     color: var(--aman-white);
}


.btn-outline-secondary {
     color: var(--aman-dark-gray);
     border-color: var(--aman-dark-gray);
     background-color: transparent;
}

.btn-outline-secondary:hover {
     background-color: var(--aman-dark-gray);
     color: var(--aman-white);
}


.templates-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}

.template-card {
    background-color: var(--aman-white);
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: var(--shadow-md);
    transition: all 0.3s ease;
    border: 1px solid var(--aman-medium-gray);
    display: flex;
    flex-direction: column;
}

.template-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

.template-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 1rem;
    gap: 1rem;
}

.template-icon {
    width: 48px;
    height: 48px;
    background-color: var(--aman-teal);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    color: var(--aman-white);
    font-size: 1.5rem;
}

.template-info {
    flex-grow: 1;
    margin-bottom: 1rem;
}

.template-name {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--aman-text-color);
    margin-bottom: 0.25rem;
}

.template-name a {
    color: inherit;
    text-decoration: none;
}

.template-name a:hover {
    color: var(--aman-teal);
    text-decoration: underline;
}

.template-description {
    color: var(--aman-dark-gray);
    font-size: 0.95rem;
    line-height: 1.5;
}

.template-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-top: 1rem;
    font-size: 0.85rem;
    color: var(--aman-dark-gray);
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.meta-item i {
    color: var(--aman-teal);
    font-size: 0.95rem;
}

.template-actions {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-top: auto;
}

.version-badge {
    background-color: var(--aman-medium-gray);
    color: var(--aman-text-color);
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.25rem;
}


.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--aman-dark-gray);
    background-color: var(--aman-white);
    border-radius: 8px;
    margin-top: 2rem;
    border: 1px dashed var(--aman-medium-gray);
}

.empty-state i {
    font-size: 4rem;
    color: var(--aman-medium-gray);
    margin-bottom: 1rem;
}

.empty-state h3 {
    color: var(--aman-dark-gray);
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}


/* Forms & Editor Pages */

.form-group label {
    font-weight: 600;
    color: var(--aman-text-color);
    margin-bottom: 0.5rem;
    display: block;
}

.form-control {
    border: 1px solid var(--aman-medium-gray);
    border-radius: 4px;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    color: var(--aman-text-color);
    background-color: var(--aman-white);
}

.form-control:focus {
    border-color: var(--aman-teal);
    box-shadow: 0 0 0 0.25rem rgba(78, 205, 196, 0.25);
}

textarea.form-control {
    min-height: 150px;
    font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace;
}

.form-text.text-muted {
    font-size: 0.875rem;
    color: var(--aman-dark-gray) !important;
    margin-top: 0.25rem;
}

/* Summernote editor overrides */
.note-editor {
    border: 1px solid var(--aman-medium-gray);
    border-radius: 4px;
    background-color: var(--aman-white);
}

.note-toolbar {
    background-color: var(--aman-light-gray);
    border-bottom: 1px solid var(--aman-medium-gray) !important;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

.note-editing-area .note-editable {
    background-color: var(--aman-white);
    color: var(--aman-text-color);
    line-height: 1.6;
    padding: 15px;
}

.note-statusbar {
    background-color: var(--aman-light-gray);
    border-top: 1px solid var(--aman-medium-gray) !important;
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
}


/* API Docs Page */

.accordion-item {
    border: 1px solid var(--aman-medium-gray);
    margin-bottom: 1rem;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: var(--shadow-sm);
}

.accordion-button {
    background-color: var(--aman-white);
    color: var(--aman-text-color);
    font-weight: 600;
    border-bottom: 1px solid var(--aman-medium-gray);
    transition: background-color 0.2s ease;
    padding: 1rem 1.25rem;
}

.accordion-button:not(.collapsed) {
    background-color: var(--aman-light-gray);
    color: var(--aman-teal);
    box-shadow: inset 0 -1px 0 rgba(0, 0, 0, .125);
}

.accordion-button:focus {
    border-color: var(--aman-teal);
    box-shadow: 0 0 0 0.25rem rgba(78, 205, 196, 0.25);
    outline: none;
}

.accordion-body {
    padding: 1.5rem;
    background-color: var(--aman-white);
    border-top: 1px solid var(--aman-medium-gray);
}

.accordion-body h5 {
    color: var(--aman-teal);
    margin-bottom: 1rem;
    font-weight: 600;
}

.try-it-out-section {
    background-color: var(--aman-light-gray);
    padding: 1.5rem;
    border-radius: 8px;
    border: 1px solid var(--aman-medium-gray);
}

.try-it-out-section .form-group label {
    font-weight: 600;
    color: var(--aman-text-color);
}

.json-payload {
    font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace;
    font-size: 0.9em !important;
    background-color: var(--aman-white);
    border-color: var(--aman-medium-gray);
    border-radius: 4px;
}

.response-section {
    background-color: var(--aman-white);
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid var(--aman-medium-gray);
}

.response-section h6 {
    color: var(--aman-text-color);
    margin-bottom: 0.75rem;
    font-weight: 600;
}

.response-status {
    font-size: 0.9em;
    font-weight: 600;
}

.response-output {
    font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace;
    font-size: 0.9em;
    white-space: pre-wrap;
    word-break: break-all;
    max-height: 300px;
    overflow-y: auto;
}


/* History Page */

.table-container {
    background-color: var(--aman-white);
    border: 1px solid var(--aman-medium-gray);
    border-radius: 8px;
    overflow: hidden;
    box-shadow: var(--shadow-sm);
}

.table {
    margin-bottom: 0;
    border-collapse: separate;
    border-spacing: 0;
}

.table th,
.table td {
    padding: 0.75rem 1.25rem;
    vertical-align: middle;
    border-bottom: 1px solid var(--aman-medium-gray);
    border-right: 1px solid var(--aman-medium-gray);
}

.table th:last-child,
.table td:last-child {
     border-right: none;
}

.table thead th {
    border-bottom-width: 2px;
    border-bottom-color: var(--aman-dark-teal);
    font-weight: 700;
    color: var(--aman-text-color);
    background-color: var(--aman-light-gray);
}

.table tbody tr:last-child td {
    border-bottom: none;
}

.table-info {
    background-color: var(--aman-light-gray) !important;
    color: var(--aman-text-color);
}

.table-info td {
    border-color: var(--aman-medium-gray);
}


.actions-column {
    white-space: nowrap;
}


.site-footer {
    margin-top: 4rem;
    padding: 1.5rem 1rem;
    background-color: var(--aman-dark-teal);
    color: var(--aman-white);
    text-align: center;
    font-size: 0.9rem;
}


/* Responsive Adjustments */
@media (max-width: 768px) {
    .container {
        padding: 1.5rem 1rem;
    }

    .page-header h1 {
        font-size: 2rem;
    }

    .page-header .page-subtitle {
        font-size: 1rem;
    }

    .action-bar {
        flex-direction: column;
        align-items: stretch;
        gap: 0.75rem;
    }

    .search-box {
        max-width: none;
    }

    .btn {
        width: 100%;
        justify-content: center;
    }

    .btn-secondary,
    .btn-design,
    .btn-info,
    .btn-warning,
    .btn-success,
    .btn-outline-secondary { /* Added outline-secondary */
        width: auto; /* Allow these to be auto width in actions */
        flex-grow: 1; /* Let them grow equally */
    }

    .templates-grid {
        grid-template-columns: 1fr;
    }

    .stats-bar {
        gap: 1rem;
        justify-content: stretch;
    }

    .stat-item {
        flex-grow: 1;
    }

    .template-actions {
        flex-direction: column;
        gap: 0.5rem;
    }

    .template-actions .btn {
        width: auto; /* Reset width for actions within card */
    }

    .table th, .table td {
         padding: 0.75rem;
    }

    .accordion-button {
        padding: 1rem;
    }

    .accordion-body {
        padding: 1rem;
    }

    .try-it-out-section {
        padding: 1rem;
    }
}

@media (max-width: 480px) {
    .page-header h1 {
        font-size: 1.8rem;
    }

    .template-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }

    .template-icon {
        margin-bottom: 0.5rem;
        width: 40px;
        height: 40px;
        font-size: 1.2rem;
    }

    .version-badge {
        align-self: flex-end;
    }

    .template-meta {
        flex-direction: column;
        gap: 0.5rem;
    }

    .form-control {
        padding: 0.6rem 0.75rem;
        font-size: 0.9rem;
    }

    .btn {
         font-size: 0.9rem;
         padding: 0.6rem 1.2rem;
    }

    .btn-sm {
         font-size: 0.8rem;
         padding: 0.4rem 0.8rem;
    }
}
```

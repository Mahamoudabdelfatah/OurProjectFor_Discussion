This is a significant and complex feature addition that moves beyond simple HTML templating into PDF manipulation and interactive design. Here's a breakdown of the approach and the new/modified files involved.

**High-Level Approach:**

1.  **PDF to Image Conversion:** When the user uploads a PDF, each page needs to be converted into an image (e.g., PNG or JPEG).
2.  **Canvas-Based Editor:**
    *   For each PDF page (now an image), display it as the background of an HTML5 `<canvas>` element.
    *   Allow users to add text elements (placeholders like `<<FieldName>>` or static text) on top of the canvas.
    *   These text elements will need properties like position (x, y), font size, font family, color, and the text content itself.
    *   The user should be able to drag, resize (maybe), and edit these text elements.
3.  **Saving the "Template":**
    *   Instead of saving HTML content, you'll now need to save:
        *   The original uploaded PDF (or references to its converted images).
        *   A JSON structure describing the layout of text elements (placeholders) on each page (their text, position, font, etc.).
4.  **PDF Generation with this New Template Type:**
    *   When generating a PDF from this "canvas template":
        *   Load the original PDF page images.
        *   For each page, render the background image.
        *   Fetch the corresponding layout JSON for the text elements.
        *   Replace placeholder values in the text elements with data from the input JSON (similar to `ProcessTemplate` but for text objects).
        *   Render these text elements onto the PDF page at their specified positions using a PDF generation library capable of drawing text on existing images/pages (e.g., iTextSharp, PdfSharp, or potentially WkHtmlToPdf if you can construct an HTML overlay precisely).

**Libraries/Technologies to Consider:**

*   **PDF to Image:**
    *   **`PdfiumViewer` (Windows-specific, uses Google's PDFium library):** Good quality, but platform-dependent.
    *   **`Magick.NET` (cross-platform, uses ImageMagick):** Powerful image manipulation, can convert PDF pages to images.
    *   **Ghostscript (via command-line or wrapper):** A classic tool for PDF processing.
*   **Canvas Interaction (Client-Side):**
    *   **`Fabric.js`:** A powerful and well-known JavaScript HTML5 canvas library that makes it easy to work with objects on the canvas (text, images, shapes), including selection, movement, scaling, etc. **This is highly recommended for this task.**
    *   Plain HTML5 Canvas API: More manual work but possible.
*   **PDF Generation (Server-Side - for overlaying text):**
    *   **`iText 7` (formerly iTextSharp, commercial with AGPL option):** Very powerful PDF manipulation library. Can add text to existing PDFs or images.
    *   **`PdfSharp` (free, MIT license):** Good for creating and modifying PDFs, can draw text.
    *   **WkHtmlToPdf:** If you can construct an HTML page that overlays the text correctly on top of the background image for each page, WkHtmlToPdf can convert that HTML to a PDF page. This might be complex for precise positioning.

**Let's assume we'll use `Magick.NET` for PDF-to-image and `Fabric.js` for the client-side canvas editor.**

---

**Changes and New Files:**

**I. Model & DTO Changes (Infrastructure & Web)**

1.  **`PDFGenerator.Infrastructure\DataAccess\Models\Template.cs`**:
    *   Add a `TemplateType` property (e.g., "Html", "UploadedPdf").
    *   `HtmlContent` becomes nullable.
    *   Add `CanvasLayoutJson` (string, nullable) to store the Fabric.js canvas state or custom layout.
    *   Add `OriginalPdfFileName` (string, nullable) and potentially a path or ID to the stored PDF/images.

2.  **`PDFGenerator.Infrastructure\DataAccess\Models\TemplateVersion.cs`**:
    *   `HtmlContent` becomes nullable.
    *   Add `CanvasLayoutJson` (string, nullable).
    *   Add `PageImagePathsJson` (string, nullable) to store a JSON array of paths to the per-page images derived from the uploaded PDF.

3.  **DTOs (`TemplateDataAccessDto`, `TemplateCreateDto`, `TemplateDetailDto`, `TemplateVersionDataAccessDto`, `TemplateVersionDto` etc.)**:
    *   Mirror the changes from the models (add `TemplateType`, `CanvasLayoutJson`, `PageImagePathsJson`, make `HtmlContent` nullable).

**II. Repository Changes (Infrastructure)**

1.  **`ITemplateRepository.cs` & `TemplateRepository.cs`**:
    *   Modify `CreateNewTemplateAsync` and `UpdateTemplateAsync` to handle the new template type. This will involve saving uploaded PDF, converting to images, and storing image paths/layout JSON.
    *   Modify `GetByNameAsync` and `GetTemplateContentByVersionReferenceAsync` to load either HTML or CanvasLayout/PageImages based on `TemplateType`.

**III. Handler Changes (Web)**

1.  **`CreateTemplateHandler.cs` & `UpdateTemplateHandler.cs`**:
    *   Modify to accept file uploads (the PDF).
    *   Orchestrate PDF-to-image conversion (possibly by calling a new service).
    *   Pass the `CanvasLayoutJson` (initially empty or from client) and image paths to the repository.

2.  **`GeneratePdfHandler.cs`**:
    *   This will be the most significantly changed handler.
    *   If `TemplateType` is "UploadedPdf":
        *   It will need to use a PDF library (like iText or PdfSharp) on the server.
        *   Load page images.
        *   Parse `CanvasLayoutJson`.
        *   Perform placeholder replacement in the text elements from `CanvasLayoutJson`.
        *   Draw the images and the processed text elements onto a new PDF.

**IV. New Services**

1.  **`IPdfProcessingService.cs` & `PdfProcessingService.cs` (Infrastructure/Services)**:
    *   Method to convert PDF pages to images (e.g., `Task<List<string>> ConvertPdfToImagesAsync(Stream pdfStream, string templateName)`).
    *   Method to generate PDF from images and layout (e.g., `Task<byte[]> GeneratePdfFromCanvasLayoutAsync(List<string> pageImagePaths, string canvasLayoutJson, JsonElement jsonData)`). This service will use iText/PdfSharp.

**V. Controller Changes (Web)**

1.  **`TemplateController.cs`**:
    *   `Create` (POST) and `Design` (POST for update) actions will need to handle `IFormFile` for PDF upload.
    *   `Design` (GET) action will need to pass different data to the view based on `TemplateType` (HTML content or page image paths and layout JSON).

**VI. View Changes (Web)**

1.  **`Create.cshtml` & `Design.cshtml`**:
    *   Add a file input for PDF upload.
    *   Add radio buttons or a dropdown to select `TemplateType`.
    *   Conditionally show either the Summernote editor (for HTML type) or the new Canvas editor UI (for UploadedPdf type).
    *   **Canvas Editor UI (Client-Side - Major Work):**
        *   Include `Fabric.js` library.
        *   JavaScript to:
            *   Initialize Fabric.js canvas for each page image.
            *   Set the PDF page image as the canvas background.
            *   Allow adding text objects (Fabric.IText) to the canvas.
            *   Allow editing text content (double-click on text).
            *   Allow moving text objects.
            *   Serialize the canvas state (or a simplified version of it with text objects' properties) to JSON and store it in a hidden input field (`CanvasLayoutJson`) to be submitted with the form.
            *   Handle multiple pages (e.g., tabs or a scrolling list of canvases).

---

This is a large feature. Let's start by outlining the changes to the core models, DTOs, and the overall structure for the new template type. The client-side Fabric.js implementation would be substantial and is best developed iteratively.

**Phase 1: Backend Model & DTO Changes, Basic UI for Upload**

**1. New Enum for Template Type (`PDFGenerator.Helper\Helper\TemplateTypeEnum.cs`)**

```csharp
namespace PdfGeneratorApp.Common
{
    public static class TemplateTypeEnum
    {
        public const string Html = "Html";
        public const string UploadedPdf = "UploadedPdf";

        public static bool IsValid(string type)
        {
            return type == Html || type == UploadedPdf;
        }
    }
}
```

**2. Model Changes**

**`PDFGenerator.Infrastructure\DataAccess\Models\Template.cs`**

```csharp
using System.ComponentModel.DataAnnotations;
using System.Collections.Generic;
using System;
using PdfGeneratorApp.Common; // For TemplateTypeEnum

namespace PdfGeneratorApp.Models
{
    public class Template
    {
        public int Id { get; set; }

        [Required]
        [StringLength(100)]
        public string Name { get; set; }

        [Required]
        public string TemplateType { get; set; } = TemplateTypeEnum.Html; // Default to Html

        public int TestingVersion { get; set; } = 1;
        public int? ProductionVersion { get; set; } = 1;

        public DateTime LastModified { get; set; } = DateTime.Now;

        // New properties for UploadedPdf type
        public string? OriginalPdfStorageIdentifier { get; set; } // e.g., filename or GUID for stored PDF

        public ICollection<TemplateVersion> Versions { get; set; }
        public string? Description { get; set; } // Added from previous error identification
    }
}
```

**`PDFGenerator.Infrastructure\DataAccess\Models\TemplateVersion.cs`**

```csharp
using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace PdfGeneratorApp.Models
{
    public class TemplateVersion
    {
        public int Id { get; set; }
        public int TemplateId { get; set; }
        public int VersionNumber { get; set; }

        // HtmlContent is now nullable, used for TemplateTypeEnum.Html
        public string? HtmlContent { get; set; }

        // CanvasLayoutJson stores the layout of text elements for UploadedPdf type
        public string? CanvasLayoutJson { get; set; }

        // Stores JSON array of relative paths to page images for UploadedPdf type
        public string? PageImagePathsJson { get; set; }

        public string? Description { get; set; }
        public string? ExampleJsonData { get; set; }
        public string? InternalDataConfigJson { get; set; }
        public DateTime CreatedDate { get; set; } = DateTime.Now;
        public bool IsDeleted { get; set; } = false;
        public DateTime? DeletedDate { get; set; } = null;

        [ForeignKey("TemplateId")]
        public Template Template { get; set; }
    }
}
```

**3. Data Access DTO Changes**

**`PDFGenerator.Infrastructure\DataAccess\Dtos\TemplateDataAccessDto.cs`**

```csharp
using System;
using System.Collections.Generic;

namespace PDFGenerator.Infrastructure.DataAccess.Dtos
{
    public class TemplateDataAccessDto
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string TemplateType { get; set; } // Added
        public string? HtmlContent { get; set; } // Nullable
        public string? CanvasLayoutJson { get; set; } // Added
        public string? PageImagePathsJson { get; set; } // Added
        public string? OriginalPdfStorageIdentifier { get; set; } // Added

        public string? Description { get; set; }
        public string? ExampleJsonData { get; set; }
        public string? InternalDataConfigJson { get; set; }
        public int TestingVersion { get; set; }
        public int? ProductionVersion { get; set; }
        public DateTime LastModified { get; set; }
        public ICollection<TemplateVersionDataAccessDto> Versions { get; set; }
    }
}
```

**`PDFGenerator.Infrastructure\DataAccess\Dtos\TemplateVersionDataAccessDto.cs`**

```csharp
using System;

namespace PDFGenerator.Infrastructure.DataAccess.Dtos
{
    public class TemplateVersionDataAccessDto
    {
        public int Id { get; set; }
        public int TemplateId { get; set; }
        public int VersionNumber { get; set; }
        public string? HtmlContent { get; set; } // Nullable
        public string? CanvasLayoutJson { get; set; } // Added
        public string? PageImagePathsJson { get; set; } // Added

        public string? Description { get; set; }
        public string? ExampleJsonData { get; set; }
        public string? InternalDataConfigJson { get; set; }
        public DateTime CreatedDate { get; set; }
        public bool IsDeleted { get; set; }
        public DateTime? DeletedDate { get; set; }
    }
}
```

**`PDFGenerator.Infrastructure\DataAccess\Dtos\TemplatesDocDataAccessDto.cs`** (Add TemplateType)

```csharp
using System.ComponentModel.DataAnnotations;

namespace PDFGenerator.Infrastructure.DataAccess.Dtos
{
    public class TemplatesDocDataAccessDto
    {
        public int Id { get; set; }
        [Required]
        [StringLength(100, ErrorMessage = "Template Name cannot exceed 100 characters.")]
        public string Name { get; set; }
        public string TemplateType { get; set; } // Added
        public string? Description { get; set; }
        public string? ExampleJsonData { get; set; } // For HTML type or for overall data structure
        public string? InternalDataConfigJson { get; set; } // For HTML type or for overall data structure
        public int TestingVersion { get; set; }
        public int? ProductionVersion { get; set; }
    }
}
```

**4. Web DTO Changes**

**`PDFGenerator.Web\Dtos\Template\TemplateCreateDto.cs`**

```csharp
using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Http; // For IFormFile
using PdfGeneratorApp.Common; // For TemplateTypeEnum

namespace PDFGenerator.Web.Dtos.Template
{
    public class TemplateCreateDto
    {
        [Required]
        [StringLength(100, ErrorMessage = "Template Name cannot exceed 100 characters.")]
        public string Name { get; set; }

        [Required(ErrorMessage = "Template Type is required.")]
        public string TemplateType { get; set; } = TemplateTypeEnum.Html;

        public string? Description { get; set; }

        // For HTML type
        public string? HtmlContent { get; set; } // Make nullable, required based on TemplateType

        // For UploadedPdf type
        public IFormFile? UploadedPdfFile { get; set; } // For PDF upload
        public string? CanvasLayoutJson { get; set; } // Client will send this

        public string? ExampleJsonData { get; set; }
        public string? InternalDataConfigJson { get; set; }
    }
}
```

**`PDFGenerator.Web\Dtos\Template\TemplateDetailDto.cs`**

```csharp
using System.ComponentModel.DataAnnotations;
using System.Collections.Generic; // For List<string> of page image paths
using PdfGeneratorApp.Common; // For TemplateTypeEnum

namespace PDFGenerator.Web.Dtos.Template
{
    public class TemplateDetailDto
    {
        public int Id { get; set; }

        [Required]
        [StringLength(100, ErrorMessage = "Template Name cannot exceed 100 characters.")]
        public string Name { get; set; }

        [Required]
        public string TemplateType { get; set; }

        public string? Description { get; set; }

        // For HTML type
        public string? HtmlContent { get; set; } // Nullable

        // For UploadedPdf type
        public string? CanvasLayoutJson { get; set; }
        public List<string>? PageImageUrls { get; set; } // URLs to serve images to client canvas
        public string? OriginalPdfStorageIdentifier { get; set; }


        public string? ExampleJsonData { get; set; }
        public string? InternalDataConfigJson { get; set; }
        public int TestingVersion { get; set; }
        public int? ProductionVersion { get; set; }
        public DateTime LastModified { get; set; }
    }
}
```

**`PDFGenerator.Web\Dtos\Template\TemplateUpdateDto.cs`**

```csharp
using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Http; // For IFormFile
using PdfGeneratorApp.Common; // For TemplateTypeEnum

namespace PDFGenerator.Web.Dtos.Template
{
    public class TemplateUpdateDto
    {
        public int Id { get; set; }
        // TemplateType is generally not updatable after creation, but if it were:
        // public string TemplateType { get; set; }

        public string? Description { get; set; }

        // For HTML type
        public string? HtmlContent { get; set; } // Required if HTML type

        // For UploadedPdf type
        public IFormFile? UploadedPdfFile { get; set; } // Optional: allow replacing the PDF
        public string? CanvasLayoutJson { get; set; }

        public string? ExampleJsonData { get; set; }
        public string? InternalDataConfigJson { get; set; }
    }
}
```

**`PDFGenerator.Web\Dtos\TemplateVersion\TemplateVersionDto.cs`**

```csharp
using System;

namespace PDFGenerator.Web.Dtos.TemplateVersion
{
    public class TemplateVersionDto
    {
        public int Id { get; set; }
        public int TemplateId { get; set; }
        public int VersionNumber { get; set; }
        public string? HtmlContent { get; set; } // Nullable
        public string? CanvasLayoutJson { get; set; } // Added
        public string? PageImagePathsJson { get; set; } // Not typically exposed directly to client in this DTO; DetailDto might have URLs instead.

        public string? Description { get; set; }
        public string? ExampleJsonData { get; set; }
        public string? InternalDataConfigJson { get; set; }
        public DateTime CreatedDate { get; set; }
        public bool IsDeleted { get; set; }
        public DateTime? DeletedDate { get; set; }
    }
}
```

**5. AutoMapper Profiles (Updates)**

**`PDFGenerator.Infrastructure\DataAccess\MappingProfile\DataAccessMappingProfile.cs`**

```csharp
// File: Infrastructure/Mapping/DataAccessMappingProfile.cs
using AutoMapper;
using PDFGenerator.Infrastructure.DataAccess.Dtos;
using PdfGeneratorApp.Models;

namespace PdfGeneratorApp.Infrastructure.Mapping
{
    public class DataAccessMappingProfile : Profile
    {
        public DataAccessMappingProfile()
        {
            CreateMap<Template, TemplateDataAccessDto>().ReverseMap();
            CreateMap<TemplateVersion, TemplateVersionDataAccessDto>().ReverseMap();

            // Update TemplateSimpleDto mapping
            CreateMap<Template, TemplateSimpleDto>()
                .ForMember(dest => dest.Description, opt => opt.MapFrom(src => src.Description)) // Ensure Description is mapped
                .ReverseMap();


            // Update TemplatesDocDataAccessDto mapping from Template model
            // The query in TemplateRepository.GetAllAsync directly projects to TemplatesDocDataAccessDto,
            // so this specific mapping from Template model might be for other scenarios.
            CreateMap<Template, TemplatesDocDataAccessDto>()
                .ForMember(dest => dest.TemplateType, opt => opt.MapFrom(src => src.TemplateType))
                .ForMember(dest => dest.Description, opt => opt.MapFrom(src => src.Description))
                 // ExampleJsonData and InternalDataConfigJson are typically from a specific version,
                 // so this mapping might need to be conditional or handled by more specific logic if used.
                .ForMember(dest => dest.ExampleJsonData, opt => opt.Ignore())
                .ForMember(dest => dest.InternalDataConfigJson, opt => opt.Ignore());
        }
    }
}
```

**`PDFGenerator.Web\MappingProfile\ApplicationLayerMappingProfile.cs`**

```csharp
using AutoMapper;
using PDFGenerator.Web.Dtos.Template;
using PDFGenerator.Web.Dtos.TemplateVersion;
using PDFGenerator.Infrastructure.DataAccess.Dtos;
using PDFGenerator.Web.Dtos.Auth;
using PdfGeneratorApp.Models; // For User -> UserDto

namespace PdfGeneratorApp.Infrastructure.Mapping
{
    public class ApplicationLayerMappingProfile : Profile
    {
        public ApplicationLayerMappingProfile()
        {
            CreateMap<TemplateSimpleDto, TemplateListDto>().ReverseMap();
            CreateMap<TemplateDataAccessDto, TemplateDetailDto>()
                // If PageImagePathsJson needs to be transformed to PageImageUrls
                // .ForMember(dest => dest.PageImageUrls, opt => opt.MapFrom(src => ConvertJsonToUrls(src.PageImagePathsJson)))
                .ReverseMap();
                // .ForMember(dest => dest.PageImagePathsJson, opt => opt.MapFrom(src => ConvertUrlsToJson(src.PageImageUrls)));


            CreateMap<TemplateDataAccessDto, TemplateCreateDto>().ReverseMap();
            CreateMap<TemplateDataAccessDto, TemplateUpdateDto>().ReverseMap();
            CreateMap<TemplateVersionDataAccessDto, TemplateVersionDto>().ReverseMap();
            CreateMap<TemplatesDocDataAccessDto, TemplatesDocDto>().ReverseMap();
            CreateMap<AccountDataAccessDto, AccountDto>().ReverseMap();
            CreateMap<User, UserDto>();
        }

        // Example helper methods for JSON/URL conversion (you'd implement these)
        // private List<string> ConvertJsonToUrls(string json) { /* ... */ return null; }
        // private string ConvertUrlsToJson(List<string> urls) { /* ... */ return null; }
    }
}
```

This is the setup for the data structures. The next steps would be:

*   **Implement `PdfProcessingService`**:
    *   Logic for PDF to image conversion using Magick.NET. Store these images in a designated folder (e.g., `wwwroot/template_uploads/{templateId}/{versionNumber}/page_{n}.png`).
    *   Logic for generating the final PDF from page images and canvas layout data using iText/PdfSharp.
*   **Update Repositories**: Handle saving/loading `TemplateType`, `CanvasLayoutJson`, `PageImagePathsJson`, `OriginalPdfStorageIdentifier`.
*   **Update Handlers**: `CreateTemplateHandler` and `UpdateTemplateHandler` will manage the PDF upload, call `PdfProcessingService` for image conversion, and save relevant data. `GeneratePdfHandler` will call `PdfProcessingService` for generation if it's an "UploadedPdf" type.
*   **Update `TemplateController`**:
    *   The `Create` (POST) and `Design` (POST for update) actions need to accept `IFormFile UploadedPdfFile` and `string CanvasLayoutJson` from the form.
    *   When a PDF is uploaded:
        *   Save the original PDF (optional, but good for re-processing).
        *   Convert PDF to page images using the new service.
        *   Store the paths to these images (relative to `wwwroot`) in `PageImagePathsJson`.
        *   Save the `CanvasLayoutJson` received from the client.
    *   The `Design` (GET) action needs to pass `PageImageUrls` and `CanvasLayoutJson` to the view if it's an "UploadedPdf" template.
*   **Implement Client-Side Canvas Editor in `Design.cshtml`**:
    *   This is the most UI-intensive part. You'll use Fabric.js.
    *   On page load, if `TemplateType` is "UploadedPdf":
        *   For each image URL in `Model.PageImageUrls`:
            *   Create a Fabric.js canvas.
            *   Set the image as the canvas background.
            *   If `Model.CanvasLayoutJson` exists, parse it and load the text objects onto the canvas(es).
        *   Provide UI tools (buttons) to:
            *   Add new text objects (placeholders or static text).
            *   Select, move, and edit existing text objects.
            *   (Optional) Change font, size, color of text objects.
        *   Before form submission, serialize the state of all text objects on all canvases into a JSON string and put it into the hidden `CanvasLayoutJson` input field.

Due to the complexity, I'll provide the modified `TemplateController` (for file upload handling structure) and a very basic outline for the `Design.cshtml` to show where the canvas editor would go. The actual Fabric.js implementation and the `PdfProcessingService` are substantial pieces of work.

---

**6. `PDFGenerator.Infrastructure\Services\IPdfProcessingService.cs` (New)**

```csharp
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Threading.Tasks;

namespace PDFGenerator.Infrastructure.Services
{
    public interface IPdfProcessingService
    {
        // Converts PDF stream to images and returns relative paths to the saved images.
        // templateId and versionNumber are for organizing stored images.
        Task<(List<string> PageImagePaths, string OriginalPdfIdentifier)> ConvertPdfToImagesAsync(
            Stream pdfStream,
            string templateName, // Used for folder naming
            int versionNumber // Used for folder naming
        );

        // Generates a PDF by overlaying text (from canvasLayoutJson) onto page images.
        Task<byte[]> GeneratePdfFromCanvasLayoutAsync(
            List<string> pageImagePaths, // Relative paths from wwwroot
            string canvasLayoutJson,
            JsonElement jsonData // Data to fill placeholders
        );
    }
}
```

**7. `PDFGenerator.Infrastructure\Services\PdfProcessingService.cs` (New - Skeleton)**

```csharp
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Threading.Tasks;
using ImageMagick; // Assuming Magick.NET for PDF to Image
// using iText.Kernel.Pdf; // Example if using iText for generation
// using iText.Layout;
// using iText.Layout.Element;
// using iText.IO.Image;

namespace PDFGenerator.Infrastructure.Services
{
    public class PdfProcessingService : IPdfProcessingService
    {
        private readonly IWebHostEnvironment _hostingEnvironment; // To get wwwroot path

        public PdfProcessingService(IWebHostEnvironment hostingEnvironment)
        {
            _hostingEnvironment = hostingEnvironment;
        }

        public async Task<(List<string> PageImagePaths, string OriginalPdfIdentifier)> ConvertPdfToImagesAsync(
            Stream pdfStream, string templateName, int versionNumber)
        {
            var pageImagePaths = new List<string>();
            var templateUploadsDir = Path.Combine("template_uploads", SanitizeFileName(templateName), $"v{versionNumber}");
            var absoluteUploadsDir = Path.Combine(_hostingEnvironment.WebRootPath, templateUploadsDir);
            Directory.CreateDirectory(absoluteUploadsDir); // Ensure directory exists

            string originalPdfFileName = $"original_{Guid.NewGuid()}.pdf";
            string originalPdfPath = Path.Combine(absoluteUploadsDir, originalPdfFileName);

            // Save the original PDF
            pdfStream.Position = 0; // Reset stream position
            using (var fileStream = new FileStream(originalPdfPath, FileMode.Create, FileAccess.Write))
            {
                await pdfStream.CopyToAsync(fileStream);
            }
            string originalPdfStorageIdentifier = Path.Combine(templateUploadsDir, originalPdfFileName); // Relative path for DB

            pdfStream.Position = 0; // Reset for Magick.NET

            // Use Magick.NET to convert PDF pages to images
            try
            {
                using (var magickImages = new MagickImageCollection())
                {
                    // Important: Specify density *before* reading for good quality
                    var settings = new MagickReadSettings { Density = new Density(300, 300) }; // 300 DPI
                    magickImages.Read(pdfStream, settings);

                    int pageNum = 1;
                    foreach (var image in magickImages)
                    {
                        string imageName = $"page_{pageNum}.png";
                        string imagePath = Path.Combine(absoluteUploadsDir, imageName);
                        image.Format = MagickFormat.Png; // Or Jpg
                        await Task.Run(() => image.Write(imagePath)); // Write to file (can be async if Magick.NET supports it directly)
                        pageImagePaths.Add(Path.Combine("/",templateUploadsDir, imageName).Replace("\\", "/")); // Relative URL path
                        pageNum++;
                    }
                }
            }
            catch (MagickException ex)
            {
                Console.WriteLine($"Magick.NET Error converting PDF: {ex.Message}");
                // Handle error, maybe throw a custom exception
                throw; // Re-throw for now
            }

            return (pageImagePaths, originalPdfStorageIdentifier);
        }

        public async Task<byte[]> GeneratePdfFromCanvasLayoutAsync(
            List<string> pageImagePaths, string canvasLayoutJson, JsonElement jsonData)
        {
            // This is where you'd use iText 7 or PdfSharp
            // 1. Create a new PDF document
            // 2. For each pageImagePath:
            //    a. Add a new page to the PDF
            //    b. Load the image (from wwwroot + pageImagePath)
            //    c. Draw the image onto the PDF page
            //    d. Parse the relevant part of canvasLayoutJson for this page
            //    e. For each text element in the layout:
            //       i. Replace placeholders in its text content using jsonData
            //       ii. Draw the text onto the PDF page at the specified x, y, font, size, color
            // 3. Save the PDF to a memory stream and return as byte[]

            // Placeholder implementation:
            Console.WriteLine("GeneratePdfFromCanvasLayoutAsync: PDF generation from canvas not fully implemented yet.");
            // For demonstration, you might return a simple PDF or throw NotImplementedException
            // Example using a simple library or just returning an error PDF:
            using (var ms = new MemoryStream())
            {
                // Example: Use PdfSharp or iText here.
                // For now, let's just create a dummy PDF text.
                // This is NOT how you'd actually do it.
                using (var writer = new StreamWriter(ms, System.Text.Encoding.UTF8, 1024, true))
                {
                    await writer.WriteLineAsync("%PDF-1.4");
                    await writer.WriteLineAsync("1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj");
                    await writer.WriteLineAsync("2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj");
                    await writer.WriteLineAsync("3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<</Font<</F1 4 0 R>>>>/Contents 5 0 R>>endobj");
                    await writer.WriteLineAsync("4 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj");
                    string textContent = "Canvas PDF Generation (Not Implemented Fully)";
                    string textStream = $"BT /F1 12 Tf 100 700 Td ({textContent}) Tj ET";
                    await writer.WriteLineAsync($"5 0 obj<</Length {textStream.Length}>>stream");
                    await writer.WriteLineAsync(textStream);
                    await writer.WriteLineAsync("endstream endobj");
                    await writer.WriteLineAsync("xref\n0 6\n0000000000 65535 f\n0000000010 00000 n\n0000000059 00000 n\n0000000112 00000 n\n0000000206 00000 n\n0000000282 00000 n\ntrailer<</Size 6/Root 1 0 R>>\nstartxref\n400\n%%EOF");
                }
                return ms.ToArray();
            }
            // throw new NotImplementedException("PDF generation from canvas layout is not implemented.");
        }
        private string SanitizeFileName(string fileName)
        {
            foreach (char c in Path.GetInvalidFileNameChars())
            {
                fileName = fileName.Replace(c, '_');
            }
            return fileName.Replace(" ", "_");
        }
    }
}
```

**8. `PDFGenerator.Web\Extensions\ServiceCollectionExtensions.cs`** (Register `PdfProcessingService`)

```csharp
// ... other usings
using PDFGenerator.Infrastructure.Services; // For IPdfProcessingService

namespace PDFGenerator.Web.Extensions
{
    public static class ServiceCollectionExtensions
    {
        public static IServiceCollection AddServices(this IServiceCollection services)
        {
             services.AddHttpContextAccessor();
             services.AddScoped<IPdfProcessingService, PdfProcessingService>(); // Register new service

            return services.AddScoped<IGetTemplatesDocHandler, GetTemplatesDocHandler>()
            // ... rest of the handlers
            .AddScoped<ISoftDeleteTemplateVersionHandler, SoftDeleteTemplateVersionHandler>();
        }
        // ... AddAuthenticationWithJwtBearer
    }
}
// ... JwtCookieMiddleware
```

**9. `PDFGenerator.Infrastructure\DataAccess\Repositories\Implementation\TemplateRepository.cs`** (Modified Create/Update/Get methods)

```csharp
// File: Infrastructure/Data/Repositories/TemplateRepository.cs
// ... (usings)
using PdfGeneratorApp.Common; // For TemplateTypeEnum

namespace PdfGeneratorApp.Infrastructure.Data.Repositories
{
    public class TemplateRepository : BaseRepository<Template, TemplateDataAccessDto>, ITemplateRepository
    {
        // ... (constructor and existing methods like GetAllTemplateSimplAsync, GetAllAsync, AnyByNameAsync)

        // Updated to handle TemplateType and new properties
        public async Task<Result<TemplateDataAccessDto>> GetByNameAsync(string name)
        {
            Template? template = await context.Templates
                                      .Include(t => t.Versions)
                                      .SingleOrDefaultAsync(t => t.Name == name);

            if (template == null)
            {
                return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.TemplateNotFound);
            }

            // Get content based on Testing Version
            TemplateVersion? currentTestingVersionContent = template.Versions
                .SingleOrDefault(tv => tv.VersionNumber == template.TestingVersion && !tv.IsDeleted);

            if (currentTestingVersionContent == null)
            {
                 return Result<TemplateDataAccessDto>.Failure(string.Format(ErrorMessageUserConst.VersionNotFound, template.TestingVersion, name));
            }

            var templateDto = _mapper.Map<TemplateDataAccessDto>(template); // Maps Id, Name, TemplateType, TestingVersion, ProductionVersion, LastModified, OriginalPdfStorageIdentifier

            // Populate content fields based on template type and current testing version
            if (template.TemplateType == TemplateTypeEnum.Html)
            {
                templateDto.HtmlContent = currentTestingVersionContent.HtmlContent;
            }
            else if (template.TemplateType == TemplateTypeEnum.UploadedPdf)
            {
                templateDto.CanvasLayoutJson = currentTestingVersionContent.CanvasLayoutJson;
                templateDto.PageImagePathsJson = currentTestingVersionContent.PageImagePathsJson;
            }
            templateDto.Description = currentTestingVersionContent.Description; // Common field
            templateDto.ExampleJsonData = currentTestingVersionContent.ExampleJsonData;
            templateDto.InternalDataConfigJson = currentTestingVersionContent.InternalDataConfigJson;


            return Result<TemplateDataAccessDto>.Success(templateDto);
        }


        // Updated for TemplateType
        public async Task<Result<TemplateDataAccessDto>> CreateNewTemplateAsync(TemplateDataAccessDto templateDto)
        {
            templateDto.Name = templateDto.Name.Replace(" ", "_");

            var nameExistsResult = await context.Templates.AnyAsync(t => t.Name == templateDto.Name);
            if (nameExistsResult) return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.TemplateNameExists);

            // ExampleJsonData is common, generate if HTML type and no explicit example provided
            if (templateDto.TemplateType == TemplateTypeEnum.Html && string.IsNullOrWhiteSpace(templateDto.ExampleJsonData))
            {
                try
                {
                    templateDto.ExampleJsonData = _templateProcessingService.GenerateExampleJson(templateDto.HtmlContent ?? "");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error generating example JSON on create: {ex.Message}");
                    return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.ExampleJsonGenerationFailed);
                }
            }


            if (!string.IsNullOrWhiteSpace(templateDto.InternalDataConfigJson))
            {
                // ... (JSON validation as before) ...
            }

            templateDto.TestingVersion = 1;
            templateDto.ProductionVersion = 1;
            templateDto.LastModified = DateTime.Now;

            var initialVersion = new TemplateVersion
            {
                VersionNumber = 1,
                CreatedDate = DateTime.Now,
                Description = templateDto.Description,
                ExampleJsonData = templateDto.ExampleJsonData,
                InternalDataConfigJson = templateDto.InternalDataConfigJson,
                IsDeleted = false
            };

            if (templateDto.TemplateType == TemplateTypeEnum.Html)
            {
                initialVersion.HtmlContent = templateDto.HtmlContent;
            }
            else if (templateDto.TemplateType == TemplateTypeEnum.UploadedPdf)
            {
                initialVersion.CanvasLayoutJson = templateDto.CanvasLayoutJson; // Should come from client/handler
                initialVersion.PageImagePathsJson = templateDto.PageImagePathsJson; // Should come from handler after PDF processing
            }


            try
            {
                Template template = new Template
                {
                    Name = templateDto.Name,
                    TemplateType = templateDto.TemplateType,
                    Description = templateDto.Description,
                    TestingVersion = templateDto.TestingVersion,
                    ProductionVersion = templateDto.ProductionVersion,
                    LastModified = templateDto.LastModified,
                    OriginalPdfStorageIdentifier = templateDto.OriginalPdfStorageIdentifier, // Save identifier
                    Versions = new List<TemplateVersion> { initialVersion }
                };

                await context.Templates.AddAsync(template);
                // To get the ID back immediately for the DTO, you'd need to save here,
                // map, and then the UoW save would be a no-op.
                // For now, the returned DTO won't have the DB-generated ID until after UoW.SaveAsync().
                // We'll return the DTO as is. The handler might need to fetch it again if ID is crucial.
                var createdDto = _mapper.Map<TemplateDataAccessDto>(template); // Map the fully constructed entity
                createdDto.HtmlContent = initialVersion.HtmlContent; // Ensure content is in DTO
                createdDto.CanvasLayoutJson = initialVersion.CanvasLayoutJson;
                createdDto.PageImagePathsJson = initialVersion.PageImagePathsJson;


                return Result<TemplateDataAccessDto>.Success(createdDto);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in TemplateRepository.CreateNewTemplateAsync: {ex.Message}");
                return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }

        // Updated for TemplateType
        public async Task<Result<TemplateDataAccessDto>> UpdateTemplateAsync(TemplateDataAccessDto templateDto)
        {
             // ... (JSON validation as before) ...

            Template? existingTemplate = await context.Templates
                                              .Include(t => t.Versions)
                                              .FirstOrDefaultAsync(t => t.Id == templateDto.Id);

            if (existingTemplate == null)
            {
                return Result<TemplateDataAccessDto>.Failure(string.Format(ErrorMessageUserConst.TemplateIdNotFound, templateDto.Id));
            }

            int lastVersionNumber = existingTemplate.Versions.Any() ? existingTemplate.Versions.Max(tv => tv.VersionNumber) : 0;
            int nextVersionNumber = lastVersionNumber + 1;

            TemplateVersion newVersion = new TemplateVersion()
            {
                TemplateId = templateDto.Id,
                VersionNumber = nextVersionNumber,
                Description = templateDto.Description,
                ExampleJsonData = templateDto.ExampleJsonData,
                InternalDataConfigJson = templateDto.InternalDataConfigJson,
                CreatedDate = DateTime.Now,
                IsDeleted = false
            };

            if (existingTemplate.TemplateType == TemplateTypeEnum.Html) // Assume type doesn't change on update
            {
                newVersion.HtmlContent = templateDto.HtmlContent;
                if (string.IsNullOrWhiteSpace(newVersion.ExampleJsonData)) // Auto-generate if empty for HTML
                {
                    newVersion.ExampleJsonData = _templateProcessingService.GenerateExampleJson(newVersion.HtmlContent ?? "");
                }
            }
            else if (existingTemplate.TemplateType == TemplateTypeEnum.UploadedPdf)
            {
                newVersion.CanvasLayoutJson = templateDto.CanvasLayoutJson;
                // If UploadedPdfFile is provided in templateDto, handler should process it and set PageImagePathsJson
                // For now, assume templateDto.PageImagePathsJson is populated by the handler if a new PDF was uploaded.
                newVersion.PageImagePathsJson = templateDto.PageImagePathsJson;
                 // Also update the OriginalPdfStorageIdentifier on the parent Template if a new PDF was uploaded
                 if (!string.IsNullOrWhiteSpace(templateDto.OriginalPdfStorageIdentifier))
                 {
                     existingTemplate.OriginalPdfStorageIdentifier = templateDto.OriginalPdfStorageIdentifier;
                 }

            }

            existingTemplate.Versions.Add(newVersion);
            existingTemplate.TestingVersion = newVersion.VersionNumber;
            existingTemplate.Description = templateDto.Description;
            existingTemplate.LastModified = DateTime.Now;

            var updatedDto = _mapper.Map<TemplateDataAccessDto>(existingTemplate);
            // Ensure content from the new version is in the DTO
            updatedDto.HtmlContent = newVersion.HtmlContent;
            updatedDto.CanvasLayoutJson = newVersion.CanvasLayoutJson;
            updatedDto.PageImagePathsJson = newVersion.PageImagePathsJson;

            return Result<TemplateDataAccessDto>.Success(updatedDto);
        }

        // GetTemplateContentByVersionReferenceAsync: Updated to handle TemplateType
        public async Task<Result<TemplateDataAccessDto>> GetTemplateContentByVersionReferenceAsync(string templateName, string versionReferenceType)
        {
             Template? template = await context.Templates
                                       .Include(t => t.Versions)
                                       .SingleOrDefaultAsync(t => t.Name == templateName);

             if (template == null)
             {
                 return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.TemplateNotFound);
             }

             int targetVersionNumber;
             string normalizedVersionReferenceType = versionReferenceType.ToLowerInvariant();

             switch (normalizedVersionReferenceType)
             {
                 case string s when s == VersionReferenceType.Testing.ToLowerInvariant():
                     targetVersionNumber = template.TestingVersion;
                     break;
                 case string s when s == VersionReferenceType.Production.ToLowerInvariant():
                     if (!template.ProductionVersion.HasValue)
                     {
                          return Result<TemplateDataAccessDto>.Failure($"Production version is not set for template '{templateName}'.");
                     }
                     targetVersionNumber = template.ProductionVersion.Value;
                     break;
                 default:
                     return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.InvalidVersionReferenceType);
             }

             TemplateVersion? targetVersionContent = template.Versions
                 .SingleOrDefault(tv => tv.VersionNumber == targetVersionNumber && !tv.IsDeleted);

             if (targetVersionContent == null)
             {
                  string referencedVersionTypeFriendly = (normalizedVersionReferenceType == VersionReferenceType.Testing.ToLowerInvariant()) ? "Testing" : "Production";
                  return Result<TemplateDataAccessDto>.Failure($"Content for {referencedVersionTypeFriendly} version {targetVersionNumber} not found or is deleted for template '{templateName}'.");
             }

             var templateDto = _mapper.Map<TemplateDataAccessDto>(template);

            // Populate content fields based on template type
            if (template.TemplateType == TemplateTypeEnum.Html)
            {
                templateDto.HtmlContent = targetVersionContent.HtmlContent;
            }
            else if (template.TemplateType == TemplateTypeEnum.UploadedPdf)
            {
                templateDto.CanvasLayoutJson = targetVersionContent.CanvasLayoutJson;
                templateDto.PageImagePathsJson = targetVersionContent.PageImagePathsJson;
                // OriginalPdfStorageIdentifier is already mapped from template entity
            }
            templateDto.Description = targetVersionContent.Description; // Common field
            templateDto.ExampleJsonData = targetVersionContent.ExampleJsonData; // Common field
            templateDto.InternalDataConfigJson = targetVersionContent.InternalDataConfigJson; // Common field

             return Result<TemplateDataAccessDto>.Success(templateDto);
        }


        // ... (RevertTemplateAsync, PublishTemplateAsync remain the same)
        public async Task<Result<int>> RevertTemplateAsync(string templateName, int targetVersionNumber, string versionReferenceType)
        {
            Template? existingTemplate = await context.Templates
                                              .Include(t => t.Versions)
                                              .FirstOrDefaultAsync(t => t.Name == templateName);
            if (existingTemplate == null) return Result<int>.Failure(ErrorMessageUserConst.TemplateNotFound);
            TemplateVersion? targetVersion = existingTemplate.Versions
                .SingleOrDefault(tv => tv.VersionNumber == targetVersionNumber);
            if (targetVersion == null)
            {
                 return Result<int>.Failure(string.Format(ErrorMessageUserConst.VersionNotFound, targetVersionNumber, templateName));
            }
             if (targetVersion.IsDeleted)
            {
                 return Result<int>.Failure($"Version {targetVersionNumber} for template '{templateName}' is deleted and cannot be reverted to.");
            }
            switch (versionReferenceType.ToLowerInvariant()) // Use ToLowerInvariant for comparison
            {
                case string s when s == VersionReferenceType.Testing.ToLowerInvariant():
                     existingTemplate.TestingVersion = targetVersionNumber;
                    break;
                case string s when s == VersionReferenceType.Production.ToLowerInvariant():
                     if (targetVersionNumber > existingTemplate.TestingVersion)
                     {
                          return Result<int>.Failure($"Cannot set Production version to {targetVersionNumber} because the current Testing version is {existingTemplate.TestingVersion}. Production must be less than or equal to Testing.");
                     }
                     existingTemplate.ProductionVersion = targetVersionNumber;
                    break;
                default:
                    return Result<int>.Failure(ErrorMessageUserConst.InvalidVersionReferenceType);
            }
            existingTemplate.LastModified = DateTime.Now;
            return Result<int>.Success(targetVersionNumber);
        }

        public async Task<Result<int>> PublishTemplateAsync(string templateName)
        {
            Template? existingTemplate = await context.Templates.FirstOrDefaultAsync(t => t.Name == templateName);
            if (existingTemplate == null) return Result<int>.Failure(ErrorMessageUserConst.TemplateNotFound);
            if (existingTemplate.ProductionVersion.HasValue && existingTemplate.TestingVersion <= existingTemplate.ProductionVersion.Value)
            {
                 return Result<int>.Failure("Production version is already up-to-date with or ahead of the Testing version.");
            }
            existingTemplate.ProductionVersion = existingTemplate.TestingVersion;
            existingTemplate.LastModified = DateTime.Now;
            return Result<int>.Success(existingTemplate.ProductionVersion.Value);
        }

    }
}
```

**10. `PDFGenerator.Web\Services\CreateTemplateHandler.cs`**

```csharp
// File: Handlers/CreateTemplateHandler.cs
using AutoMapper;
using PDFGenerator.Infrastructure.DataAccess.Dtos;
using PDFGenerator.Web.Dtos.Template;
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using System.Threading.Tasks;
using PDFGenerator.Infrastructure.Services; // For IPdfProcessingService
using System.IO; // For Stream
using System.Collections.Generic; // For List
using System.Text.Json; // For JsonSerializer

namespace PdfGeneratorApp.Handlers
{
    public interface ICreateTemplateHandler : IHandler<TemplateCreateDto, string> // Return template name
    {
    }

    public class CreateTemplateHandler : ICreateTemplateHandler
    {
        private readonly IUnitOfWork _unitOfWork;
        private readonly IMapper _mapper;
        private readonly IPdfProcessingService _pdfProcessingService; // New service

        public CreateTemplateHandler(IUnitOfWork unitOfWork, IMapper mapper, IPdfProcessingService pdfProcessingService)
        {
            _unitOfWork = unitOfWork;
            _mapper = mapper;
            _pdfProcessingService = pdfProcessingService;
        }

        public async Task<Result<string>> HandleAsync(TemplateCreateDto templateDto)
        {
            try
            {
                // Map the input Web DTO (TemplateCreateDto) to a DataAccess DTO (TemplateDataAccessDto).
                var dataAccessTemplateDto = _mapper.Map<TemplateDataAccessDto>(templateDto);
                // TemplateType and Name are mapped. HtmlContent, CanvasLayoutJson etc. are also mapped if present.

                if (templateDto.TemplateType == TemplateTypeEnum.UploadedPdf)
                {
                    if (templateDto.UploadedPdfFile == null || templateDto.UploadedPdfFile.Length == 0)
                    {
                        return Result<string>.Failure("An Uploaded PDF file is required for 'UploadedPdf' template type.");
                    }

                    List<string> pageImagePaths;
                    string originalPdfIdentifier;

                    using (var memoryStream = new MemoryStream())
                    {
                        await templateDto.UploadedPdfFile.CopyToAsync(memoryStream);
                        memoryStream.Position = 0; // Reset stream for reading
                        var conversionResult = await _pdfProcessingService.ConvertPdfToImagesAsync(memoryStream, templateDto.Name, 1); // Version 1 initially
                        pageImagePaths = conversionResult.PageImagePaths;
                        originalPdfIdentifier = conversionResult.OriginalPdfIdentifier;
                    }

                    if (pageImagePaths == null || !pageImagePaths.Any())
                    {
                        return Result<string>.Failure("Failed to convert uploaded PDF to images.");
                    }

                    dataAccessTemplateDto.PageImagePathsJson = JsonSerializer.Serialize(pageImagePaths);
                    dataAccessTemplateDto.OriginalPdfStorageIdentifier = originalPdfIdentifier;
                    dataAccessTemplateDto.HtmlContent = null; // Ensure HTML content is null for PDF type
                }
                else if (templateDto.TemplateType == TemplateTypeEnum.Html)
                {
                    if (string.IsNullOrWhiteSpace(templateDto.HtmlContent))
                    {
                        return Result<string>.Failure("HTML Content is required for 'Html' template type.");
                    }
                    dataAccessTemplateDto.CanvasLayoutJson = null; // Ensure canvas layout is null
                    dataAccessTemplateDto.PageImagePathsJson = null;
                    dataAccessTemplateDto.OriginalPdfStorageIdentifier = null;
                }
                else
                {
                    return Result<string>.Failure("Invalid template type specified.");
                }


                Result<TemplateDataAccessDto> result = await _unitOfWork.Templates.CreateNewTemplateAsync(dataAccessTemplateDto);

                if (!result.IsCompleteSuccessfully)
                    return Result<string>.Failure(result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);

                var saveResult = await _unitOfWork.SaveAsync();
                if (!saveResult.IsCompleteSuccessfully)
                    return Result<string>.Failure(saveResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);

                // Return the name of the created template (or ID if preferred)
                return Result<string>.Success(result.Data.Name); // result.Data from CreateNewTemplateAsync is the DTO passed in
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in CreateTemplateHandler: {ex.Message}");
                return Result<string>.Failure($"An unexpected error occurred during template creation: {ex.Message}");
            }
        }
    }
}
```

**11. `PDFGenerator.Web\Services\UpdateTemplateHandler.cs`**

```csharp
// File: Handlers/UpdateTemplateHandler.cs
using AutoMapper;
using PDFGenerator.Infrastructure.DataAccess.Dtos;
using PDFGenerator.Web.Dtos.Template;
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using System.Threading.Tasks;
using PDFGenerator.Infrastructure.Services; // For IPdfProcessingService
using System.IO; // For Stream
using System.Collections.Generic; // For List
using System.Text.Json; // For JsonSerializer
using System; // For Exception

namespace PdfGeneratorApp.Handlers
{
    public interface IUpdateTemplateHandler : IHandler<TemplateUpdateDto, int> // Returns new Testing Version
    {
    }

    public class UpdateTemplateHandler : IUpdateTemplateHandler
    {
        private readonly IUnitOfWork _unitOfWork;
        private readonly IMapper _mapper;
        private readonly IPdfProcessingService _pdfProcessingService; // New service

        public UpdateTemplateHandler(IUnitOfWork unitOfWork, IMapper mapper, IPdfProcessingService pdfProcessingService)
        {
            _unitOfWork = unitOfWork;
            _mapper = mapper;
            _pdfProcessingService = pdfProcessingService;
        }

        public async Task<Result<int>> HandleAsync(TemplateUpdateDto templateDto)
        {
            try
            {
                // First, get the existing template to know its type and current state
                var existingTemplateResult = await _unitOfWork.Templates.GetByNameAsync(templateDto.Id.ToString()); // Assuming GetByNameAsync can also take ID (or add GetByIdAsync)
                                                                                                                      // For now, let's assume we need to get by ID:
                var existingTemplateEntity = await _unitOfWork.TemplateVersions.GetTemplateByIdAsync(templateDto.Id); // Get the Template entity
                if (existingTemplateEntity == null)
                {
                    return Result<int>.Failure(ErrorMessageUserConst.TemplateNotFound);
                }


                var dataAccessTemplateDto = _mapper.Map<TemplateDataAccessDto>(templateDto);
                dataAccessTemplateDto.TemplateType = existingTemplateEntity.TemplateType; // Type doesn't change on update

                if (existingTemplateEntity.TemplateType == TemplateTypeEnum.UploadedPdf)
                {
                    // If a new PDF file is uploaded for an existing UploadedPdf template
                    if (templateDto.UploadedPdfFile != null && templateDto.UploadedPdfFile.Length > 0)
                    {
                        int nextVersionNumber = existingTemplateEntity.Versions.Any()
                            ? existingTemplateEntity.Versions.Max(v => v.VersionNumber) + 1
                            : 1;

                        List<string> pageImagePaths;
                        string originalPdfIdentifier;
                        using (var memoryStream = new MemoryStream())
                        {
                            await templateDto.UploadedPdfFile.CopyToAsync(memoryStream);
                            memoryStream.Position = 0;
                            var conversionResult = await _pdfProcessingService.ConvertPdfToImagesAsync(memoryStream, existingTemplateEntity.Name, nextVersionNumber);
                            pageImagePaths = conversionResult.PageImagePaths;
                            originalPdfIdentifier = conversionResult.OriginalPdfIdentifier;
                        }
                        if (pageImagePaths == null || !pageImagePaths.Any())
                        {
                            return Result<int>.Failure("Failed to convert uploaded PDF to images during update.");
                        }
                        dataAccessTemplateDto.PageImagePathsJson = JsonSerializer.Serialize(pageImagePaths);
                        dataAccessTemplateDto.OriginalPdfStorageIdentifier = originalPdfIdentifier; // Update identifier for new PDF
                    }
                    else
                    {
                        // No new PDF uploaded, keep existing PageImagePathsJson from the *previous* testing version's content
                        // The UpdateTemplateAsync in repo will create a new version entry,
                        // we need to decide if it copies old PageImagePathsJson or if client MUST provide CanvasLayoutJson to make sense
                        // For now, if no new file, assume CanvasLayoutJson is the primary change.
                        // The repository's UpdateTemplateAsync needs to be smart about this, or the handler needs to fetch previous version's paths.
                        // Let's assume the handler is responsible if paths need to be copied.
                        var previousTestingVersion = existingTemplateEntity.Versions
                            .FirstOrDefault(v => v.VersionNumber == existingTemplateEntity.TestingVersion && !v.IsDeleted);
                        if (previousTestingVersion != null)
                        {
                            dataAccessTemplateDto.PageImagePathsJson = previousTestingVersion.PageImagePathsJson;
                            dataAccessTemplateDto.OriginalPdfStorageIdentifier = existingTemplateEntity.OriginalPdfStorageIdentifier; // Keep old identifier
                        }
                    }
                    dataAccessTemplateDto.HtmlContent = null; // Ensure HTML is null
                }
                else if (existingTemplateEntity.TemplateType == TemplateTypeEnum.Html)
                {
                    if (string.IsNullOrWhiteSpace(templateDto.HtmlContent))
                    {
                        return Result<int>.Failure("HTML Content is required for 'Html' template type update.");
                    }
                    dataAccessTemplateDto.CanvasLayoutJson = null;
                    dataAccessTemplateDto.PageImagePathsJson = null;
                    dataAccessTemplateDto.OriginalPdfStorageIdentifier = null;
                }


                var updateOpResult = await _unitOfWork.Templates.UpdateTemplateAsync(dataAccessTemplateDto);

                if (!updateOpResult.IsCompleteSuccessfully)
                    return Result<int>.Failure(updateOpResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);

                var saveResult = await _unitOfWork.SaveAsync();
                if (!saveResult.IsCompleteSuccessfully)
                    return Result<int>.Failure(saveResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);

                return Result<int>.Success(updateOpResult.Data.TestingVersion);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in UpdateTemplateHandler: {ex.Message}");
                return Result<int>.Failure($"An unexpected error occurred during template update: {ex.Message}");
            }
        }
    }
}
```

**12. `PDFGenerator.Web\Services\GeneratePdfHandler.cs`** (Updated to handle new template type)

```csharp
// File: Handlers/GeneratePdfHandler.cs
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Services;
using System.Text.Json;
using WkHtmlToPdfDotNet;
using WkHtmlToPdfDotNet.Contracts;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using System.Threading.Tasks;
using PDFGenerator.Infrastructure.Services; // For IPdfProcessingService
using System.Collections.Generic; // For List
using System; // For Exception

namespace PdfGeneratorApp.Handlers
{
    public interface IGeneratePdfHandler : IHandler<(string templateName, JsonElement requestBodyJson, string mode, string? versionReferenceType), byte[]>
    {
    }

    public class GeneratePdfHandler : IGeneratePdfHandler
    {
        private readonly IUnitOfWork _unitOfWork;
        private readonly IConverter _wkHtmlToPdfConverter; // Renamed for clarity
        private readonly TemplateProcessingService _templateProcessingService;
        private readonly IPdfProcessingService _pdfProcessingService; // New service for canvas PDFs

        public GeneratePdfHandler(IUnitOfWork unitOfWork, IConverter wkHtmlToPdfConverter,
                                  TemplateProcessingService templateProcessingService, IPdfProcessingService pdfProcessingService)
        {
            _unitOfWork = unitOfWork;
            _wkHtmlToPdfConverter = wkHtmlToPdfConverter;
            _templateProcessingService = templateProcessingService;
            _pdfProcessingService = pdfProcessingService;
        }

        public async Task<Result<byte[]>> HandleAsync((string templateName, JsonElement requestBodyJson, string mode, string? versionReferenceType) request)
        {
            try
            {
                string effectiveVersionType = string.IsNullOrWhiteSpace(request.versionReferenceType) || !VersionReferenceType.IsValid(request.versionReferenceType)
                                                ? VersionReferenceType.Testing
                                                : (request.versionReferenceType.Trim().ToLowerInvariant() == VersionReferenceType.Testing.ToLowerInvariant() ? VersionReferenceType.Testing : VersionReferenceType.Production);

                var repoResult = await _unitOfWork.Templates.GetTemplateContentByVersionReferenceAsync(request.templateName, effectiveVersionType);

                if (!repoResult.IsCompleteSuccessfully || repoResult.Data == null)
                {
                    return Result<byte[]>.Failure(repoResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                var templateDataAccessDto = repoResult.Data;
                JsonElement finalDataForHtmlProcessing = request.requestBodyJson; // Default for outside mode

                if (request.mode.ToLowerInvariant() == "inside")
                {
                    if (request.requestBodyJson.ValueKind != JsonValueKind.Object)
                    {
                        return Result<byte[]>.Failure(ErrorMessageUserConst.InsideModeBodyNotObject);
                    }
                    JsonElement insideParameters = request.requestBodyJson.TryGetProperty("parameters", out var p) ? p : default;
                    finalDataForHtmlProcessing = _templateProcessingService.ResolveInternalData(templateDataAccessDto.InternalDataConfigJson, insideParameters);
                }
                else if (request.mode.ToLowerInvariant() != "outside")
                {
                     return Result<byte[]>.Failure(ErrorMessageUserConst.InvalidMode);
                }


                byte[]? pdfBytes = null;

                if (templateDataAccessDto.TemplateType == TemplateTypeEnum.Html)
                {
                    if (string.IsNullOrWhiteSpace(templateDataAccessDto.HtmlContent))
                    {
                        return Result<byte[]>.Failure("HTML content is missing for this HTML template version.");
                    }
                    string processedHtml = _templateProcessingService.ProcessTemplate(templateDataAccessDto.HtmlContent, finalDataForHtmlProcessing);
                    var doc = new HtmlToPdfDocument()
                    {
                        GlobalSettings = { /* ... */ },
                        Objects = { new ObjectSettings() { HtmlContent = processedHtml, WebSettings = { DefaultEncoding = "utf-8" } } }
                    };
                    pdfBytes = _wkHtmlToPdfConverter.Convert(doc);
                }
                else if (templateDataAccessDto.TemplateType == TemplateTypeEnum.UploadedPdf)
                {
                    if (string.IsNullOrWhiteSpace(templateDataAccessDto.PageImagePathsJson) || string.IsNullOrWhiteSpace(templateDataAccessDto.CanvasLayoutJson))
                    {
                        return Result<byte[]>.Failure("Page images or canvas layout data is missing for this Uploaded PDF template version.");
                    }
                    var pageImagePaths = JsonSerializer.Deserialize<List<string>>(templateDataAccessDto.PageImagePathsJson);
                    if (pageImagePaths == null || !pageImagePaths.Any())
                    {
                         return Result<byte[]>.Failure("No page images found for this Uploaded PDF template version.");
                    }

                    pdfBytes = await _pdfProcessingService.GeneratePdfFromCanvasLayoutAsync(
                        pageImagePaths,
                        templateDataAccessDto.CanvasLayoutJson,
                        finalDataForHtmlProcessing
                    );
                }
                else
                {
                    return Result<byte[]>.Failure("Unknown template type encountered.");
                }


                if (pdfBytes == null || pdfBytes.Length == 0)
                {
                    return Result<byte[]>.Failure(ErrorMessageUserConst.PdfGenerationFailed + " (Ensure tools are configured and template data is valid).");
                }

                return Result<byte[]>.Success(pdfBytes);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in GeneratePdfHandler: {ex.Message}\n{ex.StackTrace}");
                return Result<byte[]>.Failure($"An unexpected error occurred during PDF generation: {ex.Message}");
            }
        }
    }
}
```

**13. `PDFGenerator.Web\Controllers\TemplateController.cs`** (Updated `Create` and `Design` (POST) to handle file upload and `CanvasLayoutJson`)

```csharp
// File: Controllers/TemplateController.cs
// ... (usings as before)
using Microsoft.AspNetCore.Http; // For IFormFile
using PdfGeneratorApp.Common; // For TemplateTypeEnum

namespace PdfGeneratorApp.Controllers
{
    [Authorize]
    public class TemplateController : Controller
    {
        // ... (constructor and other methods as before, including GetDatabaseAliases)
        private readonly IPdfProcessingService _pdfProcessingService; // For Create/Update

        public TemplateController(ApplicationDbContext context, IConfiguration configuration,
                                  IGetTemplateDesignHandler getTemplateDesignHandler,
                                  IUpdateTemplateHandler updateTemplateHandler,
                                  ICreateTemplateHandler createTemplateHandler,
                                  IGetTemplateHistoryHandler getTemplateHistoryHandler,
                                  IRevertTemplateHandler revertTemplateHandler,
                                  IPublishTemplateHandler publishTemplateHandler,
                                  ISoftDeleteTemplateVersionHandler softDeleteTemplateVersionHandler,
                                  IPdfProcessingService pdfProcessingService) // Inject new service
        {
            _context = context;
            _configuration = configuration;
            _getTemplateDesignHandler = getTemplateDesignHandler;
            _updateTemplateHandler = updateTemplateHandler;
            _createTemplateHandler = createTemplateHandler;
            _getTemplateHistoryHandler = getTemplateHistoryHandler;
            _revertTemplateHandler = revertTemplateHandler;
            _publishTemplateHandler = publishTemplateHandler;
            _softDeleteTemplateVersionHandler = softDeleteTemplateVersionHandler;
            _pdfProcessingService = pdfProcessingService; // Assign
        }


        // GET: /templates/design/{templateName} - Updated for new DTO structure
        [HttpGet("templates/design/{templateName}")]
        public async Task<IActionResult> Design(string templateName)
        {
            Result<TemplateDetailDto> result = await _getTemplateDesignHandler.HandleAsync(templateName);

            if (!result.IsCompleteSuccessfully || result.Data == null)
            {
                // ... (error handling as before)
                if (result.ErrorMessages == ErrorMessageUserConst.TemplateNotFound)
                    return NotFound($"Template '{templateName}' not found.");
                return StatusCode(500, result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
            }
            // For UploadedPdf, convert PageImagePathsJson to PageImageUrls for the view
            // This logic is better placed in the GetTemplateDesignHandler or by AutoMapper if paths are simple.
            // For now, let's assume the DTO already has PageImageUrls populated if it's UploadedPdf.
            // If not, you'd do something like this (simplified):
            // if (result.Data.TemplateType == TemplateTypeEnum.UploadedPdf && !string.IsNullOrEmpty(result.Data.PageImagePathsJson))
            // {
            //     var paths = JsonSerializer.Deserialize<List<string>>(result.Data.PageImagePathsJson);
            //     result.Data.PageImageUrls = paths.Select(p => Url.Content("~" + p)).ToList(); // Url.Content needs HttpContext
            // }

            ViewBag.DatabaseAliases = GetDatabaseAliases();
            return View(result.Data);
        }


        // POST: /templates/create - Updated to handle TemplateType, file upload, canvas layout
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(
            [Bind("Name,TemplateType,Description,HtmlContent,CanvasLayoutJson,ExampleJsonData,InternalDataConfigJson")] TemplateCreateDto templateDto,
            IFormFile? uploadedPdfFile) // Separate IFormFile parameter
        {
            templateDto.UploadedPdfFile = uploadedPdfFile; // Assign to DTO property for the handler

            if (!ModelState.IsValid)
            {
                ViewBag.DatabaseAliases = GetDatabaseAliases();
                return View(templateDto);
            }
             // Basic validation for template type specifics
            if (templateDto.TemplateType == TemplateTypeEnum.Html && string.IsNullOrWhiteSpace(templateDto.HtmlContent))
            {
                ModelState.AddModelError(nameof(TemplateCreateDto.HtmlContent), "HTML Content is required for HTML templates.");
            }
            if (templateDto.TemplateType == TemplateTypeEnum.UploadedPdf && templateDto.UploadedPdfFile == null)
            {
                ModelState.AddModelError(nameof(TemplateCreateDto.UploadedPdfFile), "A PDF file upload is required for Uploaded PDF templates.");
            }
            if (templateDto.TemplateType == TemplateTypeEnum.UploadedPdf && string.IsNullOrWhiteSpace(templateDto.CanvasLayoutJson))
            {
                // CanvasLayoutJson might be initially empty if user hasn't added text yet, but should be at least "{}"
                // Let's make it optional on create, assuming user can add text later.
                // ModelState.AddModelError(nameof(TemplateCreateDto.CanvasLayoutJson), "Canvas Layout JSON is required for Uploaded PDF templates.");
            }
             if (!ModelState.IsValid)
            {
                ViewBag.DatabaseAliases = GetDatabaseAliases();
                return View(templateDto);
            }


            var result = await _createTemplateHandler.HandleAsync(templateDto); // Handler now processes file

            if (!result.IsCompleteSuccessfully)
            {
                // ... (error handling as before) ...
                ModelState.AddModelError("", result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                ViewBag.DatabaseAliases = GetDatabaseAliases();
                return View(templateDto);
            }

            TempData["Message"] = $"Template '{result.Data}' created successfully!";
            return RedirectToAction(nameof(Design), new { templateName = result.Data });
        }

        // POST: /templates/design/{templateName} - Updated for TemplateType, file upload, canvas layout
        [HttpPost("templates/design/{templateName}")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Design(string templateName,
            [Bind("Id,Description,HtmlContent,CanvasLayoutJson,ExampleJsonData,InternalDataConfigJson")] TemplateUpdateDto templateDto,
            IFormFile? uploadedPdfFile) // Separate IFormFile parameter
        {
            templateDto.UploadedPdfFile = uploadedPdfFile; // Assign to DTO property

             // Fetch original details to display view correctly on error, and to get TemplateType
             Result<TemplateDetailDto> detailDtoOnError = await _getTemplateDesignHandler.HandleAsync(templateName);
             if (!detailDtoOnError.IsCompleteSuccessfully || detailDtoOnError.Data == null)
             {
                 TempData["Error"] = detailDtoOnError.ErrorMessages ?? "Could not load template details for update.";
                 return RedirectToAction(nameof(Index), "Home");
             }
             ViewBag.DatabaseAliases = GetDatabaseAliases();

            // Update the properties of detailDtoOnError.Data from templateDto for re-display if validation fails
            if (detailDtoOnError.Data != null)
            {
                 detailDtoOnError.Data.Description = templateDto.Description;
                 if (detailDtoOnError.Data.TemplateType == TemplateTypeEnum.Html)
                 {
                     detailDtoOnError.Data.HtmlContent = templateDto.HtmlContent;
                 }
                 else if (detailDtoOnError.Data.TemplateType == TemplateTypeEnum.UploadedPdf)
                 {
                     detailDtoOnError.Data.CanvasLayoutJson = templateDto.CanvasLayoutJson;
                 }
                 detailDtoOnError.Data.ExampleJsonData = templateDto.ExampleJsonData;
                 detailDtoOnError.Data.InternalDataConfigJson = templateDto.InternalDataConfigJson;
            }


            if (!ModelState.IsValid) return View(detailDtoOnError.Data);

            // Basic validation based on existing template type (type cannot be changed on update)
            if (detailDtoOnError.Data.TemplateType == TemplateTypeEnum.Html && string.IsNullOrWhiteSpace(templateDto.HtmlContent))
            {
                 ModelState.AddModelError(nameof(TemplateUpdateDto.HtmlContent), "HTML Content is required for HTML templates.");
            }
            // For UploadedPdf, CanvasLayoutJson should ideally always be submitted, even if empty "{}".
            // A new PDF file upload is optional on update.
             if (!ModelState.IsValid) return View(detailDtoOnError.Data);


            var result = await _updateTemplateHandler.HandleAsync(templateDto);

            if (!result.IsCompleteSuccessfully)
            {
                ModelState.AddModelError("", result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                return View(detailDtoOnError.Data);
            }

            TempData["Message"] = $"Template '{templateName}' updated. New Testing Version is {result.Data}.";
            return RedirectToAction(nameof(Design), new { templateName = templateName });
        }

        // ... (History, Revert, Publish, SoftDeleteVersion actions remain largely the same,
        // but ensure they redirect appropriately and handle errors if a template/version is unexpectedly missing)
    }
}
```

**14. `PDFGenerator.Web\Views\Template\Create.cshtml` (Updated for TemplateType and PDF upload)**

```html
@using PDFGenerator.Web.Dtos.Template
@using PdfGeneratorApp.Common // For TemplateTypeEnum
@model TemplateCreateDto
@{
    ViewData["Title"] = "Create New Template";
    var dbAliases = ViewBag.DatabaseAliases as List<string> ?? new List<string>();
}

<div class="container">
    <div class="page-header">
        <h1>@ViewData["Title"]</h1>
        <p class="page-subtitle">Define the details for your new PDF template.</p>
    </div>

    <div class="row">
        <div class="col-md-12">
            <!-- Add enctype for file uploads -->
            <form asp-action="Create" method="post" enctype="multipart/form-data">
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

                <!-- Template Type Selection -->
                <div class="form-group mb-3">
                    <label asp-for="TemplateType" class="control-label">Template Type</label>
                    <select asp-for="TemplateType" class="form-select" id="templateTypeSelector">
                        <option value="@TemplateTypeEnum.Html">HTML Editor</option>
                        <option value="@TemplateTypeEnum.UploadedPdf">Upload PDF (Canvas)</option>
                    </select>
                    <span asp-validation-for="TemplateType" class="text-danger"></span>
                </div>

                <!-- HTML Editor Section (Conditional) -->
                <div id="htmlEditorSection" class="mb-3 @(Model.TemplateType == TemplateTypeEnum.UploadedPdf ? "d-none" : "")">
                    <h5>HTML Content Source:</h5>
                    <div class="form-group mb-3">
                        <label for="htmlEditor" class="control-label">Edit HTML Content:</label>
                        <textarea asp-for="HtmlContent" class="form-control" rows="15" id="htmlEditor"></textarea>
                        <span asp-validation-for="HtmlContent" class="text-danger"></span>
                        <small class="form-text text-muted">Use <code>&lt;&lt;FieldName&gt;&gt;</code> for placeholders and <code>${{condition ? true_part : false_part}}</code> for conditionals.</small>
                    </div>
                    <!-- ... (HTML file upload for editor - optional) ... -->
                </div>

                <!-- PDF Upload and Canvas Editor Section (Conditional) -->
                <div id="pdfCanvasSection" class="mb-3 @(Model.TemplateType == TemplateTypeEnum.Html ? "d-none" : "")">
                    <h5>PDF Upload & Canvas Editor:</h5>
                    <div class="form-group mb-3">
                        <label asp-for="UploadedPdfFile" class="form-label">Upload PDF File (.pdf):</label>
                        <input asp-for="UploadedPdfFile" type="file" class="form-control" accept=".pdf" id="pdfFileUploader" />
                        <span asp-validation-for="UploadedPdfFile" class="text-danger"></span>
                    </div>
                    <!-- Placeholder for Canvas Editor UI -->
                    <div id="canvasEditorPlaceholder" class="border p-3" style="min-height: 400px;">
                        <p><em>PDF preview and canvas editor will appear here after PDF upload. (Not yet implemented)</em></p>
                        <!-- This is where Fabric.js canvases would be dynamically created. -->
                    </div>
                    <input type="hidden" asp-for="CanvasLayoutJson" id="canvasLayoutJsonInput" />
                    <span asp-validation-for="CanvasLayoutJson" class="text-danger"></span>
                </div>


                <hr class="my-4">
                <h5>Data Configuration (Common for all types):</h5>
                <!-- ... (Placeholder list, Example JSON, Internal Data Config sections as before) ... -->
                 <div class="card card-body mb-3">
                    <h6>Detected Placeholders (from HTML or Canvas Text):</h6>
                    <ul id="placeholderList" class="list-inline mb-0 small text-muted">
                        <li class="list-inline-item"><em>(Edit content to detect placeholders)</em></li>
                    </ul>
                </div>
                <div class="form-group mb-3">
                    <label asp-for="ExampleJsonData" class="control-label">Example JSON Data (for API docs & testing):</label>
                    <textarea asp-for="ExampleJsonData" class="form-control" rows="10" id="exampleJsonData"></textarea>
                    <span asp-validation-for="ExampleJsonData" class="text-danger"></span>
                </div>
                <div class="form-group mb-3">
                    <label asp-for="InternalDataConfigJson" class="control-label">Internal Data Configuration (for "Inside" mode):</label>
                    <textarea asp-for="InternalDataConfigJson" class="form-control" rows="10" id="internalDataConfigJson"></textarea>
                    <span asp-validation-for="InternalDataConfigJson" class="text-danger"></span>
                    <small class="form-text text-muted">
                        Available database aliases: @string.Join(", ", dbAliases).
                    </small>
                </div>


                <div class="form-group mt-4">
                    <input type="submit" value="Create Template" class="btn btn-primary" />
                    <a asp-action="Index" asp-controller="Home" class="btn btn-secondary">Back to List</a>
                </div>
                 @Html.AntiForgeryToken()
            </form>
        </div>
    </div>
</div>

@section Scripts {
    @{ await Html.RenderPartialAsync("_ValidationScriptsPartial"); }
    <link href="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.21/lodash.min.js"></script>
    <!-- Fabric.js (You'd host this locally or use a reliable CDN) -->
    <!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.0/fabric.min.js"></script> -->


    <script>
        $(document).ready(function() {
            var htmlEditor = $('#htmlEditor');
            var exampleJsonDataTextarea = $('#exampleJsonData');
            var internalDataConfigJsonTextarea = $('#internalDataConfigJson');
            var placeholderListElement = $('#placeholderList');
            var templateTypeSelector = $('#templateTypeSelector');
            var htmlEditorSection = $('#htmlEditorSection');
            var pdfCanvasSection = $('#pdfCanvasSection');
            var canvasLayoutJsonInput = $('#canvasLayoutJsonInput');
            var pdfFileUploader = $('#pdfFileUploader');
            var canvasEditorPlaceholder = $('#canvasEditorPlaceholder'); // Where canvases will go

            // Initialize Summernote if HTML type is selected
            if (templateTypeSelector.val() === '@TemplateTypeEnum.Html') {
                initializeSummernote();
            }

            function initializeSummernote() {
                if (!htmlEditor.data('summernote')) { // Check if already initialized
                    htmlEditor.summernote({
                        height: 300, // Adjusted height
                        toolbar: [ /* ... toolbar config ... */ ],
                        callbacks: {
                            onChange: _.debounce(function(contents, $editable) {
                                updatePlaceholdersListFromHtml(contents);
                            }, 500)
                        }
                    });
                }
            }
            function destroySummernote() {
                if (htmlEditor.data('summernote')) {
                    htmlEditor.summernote('destroy');
                }
            }

            // Toggle sections based on TemplateType
            templateTypeSelector.on('change', function() {
                var selectedType = $(this).val();
                if (selectedType === '@TemplateTypeEnum.Html') {
                    htmlEditorSection.removeClass('d-none');
                    pdfCanvasSection.addClass('d-none');
                    initializeSummernote();
                    updatePlaceholdersListFromHtml(htmlEditor.summernote('code'));
                } else if (selectedType === '@TemplateTypeEnum.UploadedPdf') {
                    htmlEditorSection.addClass('d-none');
                    pdfCanvasSection.removeClass('d-none');
                    destroySummernote();
                    // Placeholder list for canvas will be updated by canvas interaction logic
                    updatePlaceholdersListFromCanvas(); // Implement this
                }
            }).trigger('change'); // Trigger on load

            // --- Placeholder Detection ---
            function updatePlaceholdersListFromHtml(html) {
                const placeholderRegex = /&lt;&lt;(\w+)&gt;&gt;/g; // For Summernote
                // const placeholderRegex = /<<(\w+)>>/g; // If direct HTML input
                let match;
                const placeholders = new Set();
                while ((match = placeholderRegex.exec(html)) !== null) {
                    placeholders.add(match[1]);
                }
                renderPlaceholderList(placeholders);
            }

            // TODO: Implement placeholder detection from Fabric.js canvas text objects
            function updatePlaceholdersListFromCanvas() {
                var allTextObjects = []; // This would come from Fabric.js objects
                // Example:
                // fabricCanvases.forEach(canvas => {
                //    canvas.getObjects('i-text').forEach(obj => allTextObjects.push(obj.text));
                // });
                const placeholders = new Set();
                const placeholderRegex = /<<(\w+)>>/g;
                allTextObjects.forEach(text => {
                    let match;
                    while((match = placeholderRegex.exec(text)) !== null) {
                        placeholders.add(match[1]);
                    }
                });
                renderPlaceholderList(placeholders);
                // Also, serialize canvas layout to canvasLayoutJsonInput.val()
            }

            function renderPlaceholderList(placeholdersSet) {
                placeholderListElement.empty();
                if (placeholdersSet.size === 0) {
                    placeholderListElement.html('<li class="list-inline-item"><em>(No placeholders detected)</em></li>');
                } else {
                    placeholdersSet.forEach(p => placeholderListElement.append(`<li class="list-inline-item"><code><<${p}>></code></li>`));
                }
            }


            // --- JSON Formatting ---
            function formatJsonTextarea(textarea) { /* ... as before ... */ }
            formatJsonTextarea(exampleJsonDataTextarea);
            formatJsonTextarea(internalDataConfigJsonTextarea);
            if(canvasLayoutJsonInput.val() === "") canvasLayoutJsonInput.val('{}'); // Default canvas layout
            formatJsonTextarea(canvasLayoutJsonInput); // Format if it's visible/editable directly


            // --- PDF File Upload & Canvas Initialization (Skeleton) ---
            var fabricCanvases = []; // Array to hold Fabric.js canvas instances

            pdfFileUploader.on('change', function(event) {
                var file = event.target.files[0];
                if (!file || file.type !== 'application/pdf') {
                    alert('Please select a PDF file.');
                    pdfFileUploader.val(''); // Clear the input
                    return;
                }
                canvasEditorPlaceholder.html('<p>Processing PDF... (This requires client-side PDF rendering to images)</p>');
                // TODO: Client-side PDF to Image conversion (e.g., using pdf.js + canvas)
                // This is a complex step. For each page:
                // 1. Render PDF page to an image (or directly to a canvas).
                // 2. Create a Fabric.js canvas for it.
                // 3. Set the rendered page image as the Fabric canvas background.
                // 4. Add to fabricCanvases array.
                // 5. Implement Fabric.js tools for adding/editing text.
                // 6. On text change/add/move, call updatePlaceholdersListFromCanvas() and serialize to canvasLayoutJsonInput.
                alert("PDF Uploaded. Client-side PDF page rendering and Fabric.js editor setup is NOT YET IMPLEMENTED in this example.");
            });


            // Initial placeholder detection (for HTML type if selected)
            if (templateTypeSelector.val() === '@TemplateTypeEnum.Html') {
                updatePlaceholdersListFromHtml(htmlEditor.summernote('code'));
            } else {
                updatePlaceholdersListFromCanvas(); // Will be empty initially
            }
        });
    </script>
}
```

**15. `PDFGenerator.Web\Views\Template\Design.cshtml` (Updated for TemplateType and PDF display/Canvas editor)**

```html
@using PDFGenerator.Web.Dtos.Template
@using PdfGeneratorApp.Common // For TemplateTypeEnum
@model TemplateDetailDto
@{
    ViewData["Title"] = $"Design Template: {Model.Name}";
    var dbAliases = ViewBag.DatabaseAliases as List<string> ?? new List<string>();
}

<div class="container">
    <div class="page-header">
        <h1>@ViewData["Title"]</h1>
        <p class="page-subtitle">Edit the content and configurations for <strong>@Model.Name</strong> (Type: @Model.TemplateType).</p>
    </div>

    <div class="row">
        <div class="col-md-12">
            <form asp-action="Design" asp-route-templateName="@Model.Name" method="post" enctype="multipart/form-data">
                <div asp-validation-summary="ModelOnly" class="text-danger"></div>
                <input type="hidden" asp-for="Id" />
                <input type="hidden" asp-for="TemplateType" /> <!-- Keep track of type, usually not changed on update -->


                <!-- ... (Read-only fields for Name, Versions, LastModified as before) ... -->
                <div class="form-group mb-3">
                    <label class="control-label">Template Name:</label>
                    <input value="@Model.Name" class="form-control" readonly />
                </div>
                <div class="row mb-3">
                    <div class="col-md-6">
                         <label class="control-label">Testing Version:</label>
                         <input value="@Model.TestingVersion" class="form-control" readonly />
                    </div>
                    <div class="col-md-6">
                         <label class="control-label">Production Version:</label>
                         <input value="@(Model.ProductionVersion?.ToString() ?? "N/A")" class="form-control" readonly />
                    </div>
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

                @if (Model.TemplateType == TemplateTypeEnum.Html)
                {
                    <div id="htmlEditorSection" class="mb-3">
                        <h5>HTML Content:</h5>
                        <div class="form-group mb-3">
                            <label asp-for="HtmlContent" class="control-label"></label>
                            <textarea asp-for="HtmlContent" class="form-control" rows="15" id="htmlEditor"></textarea>
                            <span asp-validation-for="HtmlContent" class="text-danger"></span>
                            <small class="form-text text-muted">Use <code>&lt;&lt;FieldName&gt;&gt;</code> and <code>${{condition ? true_part : false_part}}</code>.</small>
                        </div>
                    </div>
                }
                else if (Model.TemplateType == TemplateTypeEnum.UploadedPdf)
                {
                    <div id="pdfCanvasSection" class="mb-3">
                        <h5>PDF Canvas Editor:</h5>
                        <div class="form-group mb-3">
                            <label asp-for="UploadedPdfFile" class="form-label">Replace PDF File (Optional):</label>
                            <input asp-for="UploadedPdfFile" type="file" class="form-control" accept=".pdf" id="pdfFileUploader" />
                            <span asp-validation-for="UploadedPdfFile" class="text-danger"></span>
                            @if(!string.IsNullOrEmpty(Model.OriginalPdfStorageIdentifier))
                            {
                                <small class="form-text text-muted">Current PDF: <a href="@Url.Content("~/" + Model.OriginalPdfStorageIdentifier)" target="_blank">View Original</a></small>
                            }
                        </div>

                        <!-- Canvas Editor UI -->
                        <div id="canvasPagesContainer" class="mb-3">
                            @if (Model.PageImageUrls != null && Model.PageImageUrls.Any())
                            {
                                foreach (var imageUrl in Model.PageImageUrls.Select((url, index) => new { url, index }))
                                {
                                    <div class="canvas-page-wrapper border mb-3 p-2">
                                        <h6>Page @(imageUrl.index + 1)</h6>
                                        <!-- The actual canvas where Fabric.js will operate -->
                                        <canvas id="pageCanvas_@(imageUrl.index)" class="pdf-page-canvas" style="border:1px solid #ccc;"></canvas>
                                         <!-- Store background image URL for JS -->
                                        <input type="hidden" class="page-image-url" value="@Url.Content(imageUrl.url)" />
                                    </div>
                                }
                            }
                            else
                            {
                                <p><em>No pages to display. Upload a PDF if this is a new 'UploadedPdf' template or if images are missing.</em></p>
                            }
                        </div>
                        <input type="hidden" asp-for="CanvasLayoutJson" id="canvasLayoutJsonInput" />
                        <span asp-validation-for="CanvasLayoutJson" class="text-danger"></span>
                         <!-- Button to trigger placeholder detection from canvas -->
                        <button type="button" class="btn btn-sm btn-secondary mb-2" id="detectCanvasPlaceholdersBtn">Detect Placeholders from Canvas</button>
                    </div>
                }

                <hr class="my-4">
                <h5>Data Configuration (Common for all types):</h5>
                <!-- ... (Placeholder list, Example JSON, Internal Data Config sections as before) ... -->
                <div class="card card-body mb-3">
                    <h6>Detected Placeholders:</h6>
                    <ul id="placeholderList" class="list-inline mb-0 small text-muted">
                        <li class="list-inline-item"><em>(Loading...)</em></li>
                    </ul>
                </div>
                 <div class="form-group mb-3">
                    <label asp-for="ExampleJsonData" class="control-label">Example JSON Data:</label>
                    <textarea asp-for="ExampleJsonData" class="form-control" rows="10" id="exampleJsonData"></textarea>
                 </div>
                 <div class="form-group mb-3">
                    <label asp-for="InternalDataConfigJson" class="control-label">Internal Data Configuration:</label>
                    <textarea asp-for="InternalDataConfigJson" class="form-control" rows="10" id="internalDataConfigJson"></textarea>
                    <small class="form-text text-muted">Aliases: @string.Join(", ", dbAliases).</small>
                 </div>


                <div class="form-group mt-4">
                    <!-- ... (Save, Back, History, Publish buttons as before) ... -->
                    <input type="submit" value="Save Changes" class="btn btn-primary" />
                    <a asp-action="Index" asp-controller="Home" class="btn btn-secondary">Back to Templates</a>
                    <a asp-controller="Template" asp-action="History" asp-route-templateName="@Model.Name" class="btn btn-info">View History</a>
                     @if (Model.ProductionVersion == null || Model.TestingVersion > Model.ProductionVersion.Value)
                    {
                        <form asp-action="Publish" asp-route-templateName="@Model.Name" method="post" class="d-inline needs-confirmation" data-confirmation-message="Are you sure you want to publish Testing Version @Model.TestingVersion to Production?">
                            @Html.AntiForgeryToken()
                             <button type="submit" class="btn btn-success">
                                 <i class="fas fa-arrow-alt-circle-up"></i> Publish to Production
                             </button>
                        </form>
                    }
                    else
                    {
                         <button type="button" class="btn btn-success" disabled title="Production is already up-to-date">
                             <i class="fas fa-arrow-alt-circle-up"></i> Published (v @(Model.ProductionVersion?.ToString() ?? "N/A"))
                         </button>
                    }
                    <button type="button" id="downloadPdfBtn" class="btn btn-outline-success">Download Test PDF (Testing Version)</button>
                </div>
                 @Html.AntiForgeryToken()
            </form>
        </div>
    </div>
</div>

@section Scripts {
    @{await Html.RenderPartialAsync("_ValidationScriptsPartial");}
    @if (Model.TemplateType == TemplateTypeEnum.Html)
    {
        <link href="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.js"></script>
    }
    else if (Model.TemplateType == TemplateTypeEnum.UploadedPdf)
    {
        <!-- Fabric.js - Make sure you have this library available -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.0/fabric.min.js"></script>
    }
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.21/lodash.min.js"></script>

    <script>
        $(document).ready(function() {
            var templateType = "@Model.TemplateType";
            var placeholderListElement = $('#placeholderList');
            var canvasLayoutJsonInput = $('#canvasLayoutJsonInput');
            var fabricCanvases = []; // Array to store Fabric.js canvas instances

            // --- Common JSON Formatting ---
            function formatJsonTextarea(textarea) { /* ... as before ... */ }
            formatJsonTextarea($('#exampleJsonData'));
            formatJsonTextarea($('#internalDataConfigJson'));
             if(templateType === '@TemplateTypeEnum.UploadedPdf' && canvasLayoutJsonInput.val() === "") {
                canvasLayoutJsonInput.val('{}'); // Default for canvas layout
            }
            formatJsonTextarea(canvasLayoutJsonInput);


            // --- Placeholder List Update ---
            function updatePlaceholdersList(placeholdersSet) {
                placeholderListElement.empty();
                if (placeholdersSet.size === 0) {
                    placeholderListElement.html('<li class="list-inline-item"><em>(No placeholders detected)</em></li>');
                } else {
                    placeholdersSet.forEach(p => placeholderListElement.append(`<li class="list-inline-item"><code><<${p}>></code></li>`));
                }
            }


            if (templateType === '@TemplateTypeEnum.Html') {
                var htmlEditor = $('#htmlEditor');
                htmlEditor.summernote({
                    height: 400,
                    toolbar: [ /* ... */ ],
                    callbacks: {
                        onChange: _.debounce(function(contents, $editable) {
                            const regex = /&lt;&lt;(\w+)&gt;&gt;/g; let m; const p = new Set();
                            while ((m = regex.exec(contents)) !== null) p.add(m[1]);
                            updatePlaceholdersList(p);
                        }, 500)
                    }
                });
                // Initial load for HTML
                const initialHtmlContent = htmlEditor.summernote('code');
                const initialRegex = /&lt;&lt;(\w+)&gt;&gt;/g; let im; const ip = new Set();
                while((im = initialRegex.exec(initialHtmlContent)) !== null) ip.add(im[1]);
                updatePlaceholdersList(ip);
            }
            else if (templateType === '@TemplateTypeEnum.UploadedPdf') {
                // --- Fabric.js Canvas Setup ---
                initializeFabricCanvases();
                // Load initial layout if present
                loadCanvasLayoutFromJson();

                $('#detectCanvasPlaceholdersBtn').on('click', function() {
                    detectAndListCanvasPlaceholders();
                    serializeCanvasLayoutToJson(); // Also save layout when detecting
                });

                // PDF file uploader change - might re-initialize canvases if a new PDF is chosen
                $('#pdfFileUploader').on('change', function(event) {
                     alert("Replacing PDF requires server-side processing to get new page images. This demo won't re-render pages on client. Save changes to process new PDF.");
                     // In a full implementation, you might AJAX upload the PDF, get new image URLs,
                     // and then re-call initializeFabricCanvases with the new URLs.
                });
            }

            function initializeFabricCanvases() {
                $('.pdf-page-canvas').each(function(index) {
                    var canvasId = $(this).attr('id');
                    var imageUrl = $(this).siblings('.page-image-url').val();
                    var fabricCanvas = new fabric.Canvas(canvasId);
                    fabricCanvases[index] = fabricCanvas;

                    if (imageUrl) {
                        fabric.Image.fromURL(imageUrl, function(img) {
                            // Calculate scale to fit image within a max width/height if needed
                            // For simplicity, using original image size for canvas, then scaling image
                            fabricCanvas.setWidth(img.width);
                            fabricCanvas.setHeight(img.height);
                            img.set({selectable: false, evented: false}); // Make background not selectable
                            fabricCanvas.setBackgroundImage(img, fabricCanvas.renderAll.bind(fabricCanvas), {
                                // Scale if necessary:
                                // scaleX: canvas.width / img.width,
                                // scaleY: canvas.height / img.height
                            });
                        });
                    } else {
                        // Fallback canvas size if no image
                        fabricCanvas.setWidth(600);
                        fabricCanvas.setHeight(800);
                    }

                    // Event listener for when objects are modified (moved, text changed)
                    fabricCanvas.on('object:modified', function(e) {
                        serializeCanvasLayoutToJson();
                        detectAndListCanvasPlaceholders();
                    });
                     fabricCanvas.on('text:changed', function(e) { // Specifically for text content changes
                        serializeCanvasLayoutToJson();
                        detectAndListCanvasPlaceholders();
                    });
                });
                 // Add dummy text tool
                $('#canvasPagesContainer').prepend('<button type="button" id="addTextBtn" class="btn btn-sm btn-info mb-2">Add Placeholder Text</button>');
                $('#addTextBtn').on('click', function() {
                    if (fabricCanvases.length > 0) {
                        // Add to the first canvas by default, or implement page selection
                        var activeCanvas = fabricCanvases[0]; // Or based on selected page
                        var text = new fabric.IText('<<Placeholder>>', {
                            left: 50,
                            top: 50,
                            fontFamily: 'helvetica',
                            fontSize: 20,
                            fill: '#000000'
                        });
                        activeCanvas.add(text);
                        activeCanvas.setActiveObject(text); // Make it active for immediate editing
                        serializeCanvasLayoutToJson();
                        detectAndListCanvasPlaceholders();
                    } else {
                        alert("No canvas pages initialized. Upload a PDF first or ensure pages are loaded.");
                    }
                });
            }

            function serializeCanvasLayoutToJson() {
                var layoutData = [];
                fabricCanvases.forEach((canvas, pageIndex) => {
                    var pageObjects = [];
                    canvas.getObjects().forEach(obj => {
                        if (obj.type === 'i-text') { // Only save IText objects
                            pageObjects.push({
                                type: obj.type,
                                text: obj.text,
                                left: obj.left,
                                top: obj.top,
                                fontSize: obj.fontSize,
                                fontFamily: obj.fontFamily,
                                fill: obj.fill,
                                angle: obj.angle,
                                scaleX: obj.scaleX,
                                scaleY: obj.scaleY
                                // Add other properties you want to save
                            });
                        }
                    });
                    layoutData.push({ page: pageIndex, objects: pageObjects });
                });
                var jsonString = JSON.stringify(layoutData, null, 2);
                canvasLayoutJsonInput.val(jsonString);
            }

            function loadCanvasLayoutFromJson() {
                var jsonString = canvasLayoutJsonInput.val();
                if (jsonString && jsonString.trim() !== "" && jsonString.trim() !== "{}") {
                    try {
                        var layoutData = JSON.parse(jsonString);
                        layoutData.forEach(pageData => {
                            var canvas = fabricCanvases[pageData.page];
                            if (canvas && pageData.objects) {
                                pageData.objects.forEach(objData => {
                                    if (objData.type === 'i-text') {
                                        var text = new fabric.IText(objData.text, objData);
                                        canvas.add(text);
                                    }
                                });
                                canvas.renderAll();
                            }
                        });
                         detectAndListCanvasPlaceholders(); // Update placeholders after loading
                    } catch (e) {
                        console.error("Error loading canvas layout from JSON:", e);
                    }
                }
            }

            function detectAndListCanvasPlaceholders() {
                const allPlaceholders = new Set();
                const placeholderRegex = /<<(\w+)>>/g;
                fabricCanvases.forEach(canvas => {
                    canvas.getObjects('i-text').forEach(obj => {
                        let match;
                        while((match = placeholderRegex.exec(obj.text)) !== null) {
                            allPlaceholders.add(match[1]);
                        }
                    });
                });
                updatePlaceholdersList(allPlaceholders);
            }


            // --- Confirmation for forms (Publish, Revert, Delete) ---
            document.querySelectorAll('.needs-confirmation').forEach(form => { /* ... as before ... */ });

            // --- Test PDF Download ---
            $('#downloadPdfBtn').on('click', function() { /* ... as before ... */ });

            // Call this before submitting the form to ensure the latest canvas state is captured
            $('form').on('submit', function() {
                if (templateType === '@TemplateTypeEnum.UploadedPdf') {
                    serializeCanvasLayoutToJson();
                }
            });

        }); // End document ready
    </script>
}
```

**Key Considerations for the Canvas Feature:**

*   **Client-Side PDF to Image:** The provided `Create.cshtml` and `Design.cshtml` skeletons assume that when a PDF is uploaded for the "UploadedPdf" type, the server (`CreateTemplateHandler`/`UpdateTemplateHandler` via `PdfProcessingService`) converts it to images and stores their paths. The `Design.cshtml` then receives these image URLs (`Model.PageImageUrls`) to display as backgrounds for Fabric.js canvases.
    *   A more interactive "Create" page might involve client-side PDF rendering (using `pdf.js`) to show previews immediately and then send the PDF to the server for robust conversion and storage.
*   **Fabric.js Implementation:**
    *   You'll need to write JavaScript to initialize Fabric.js for each page.
    *   Implement tools to add text elements (using `fabric.IText` is good as it allows in-canvas editing).
    *   Handle text properties (font, size, color) via a UI.
    *   **Serialization:** Before the form is submitted, you *must* iterate through all Fabric.js canvases, get the properties of all text objects (text content, x, y, font, size, color, angle, scale, etc.), and serialize this into a JSON string. This JSON string is then put into the hidden input field `CanvasLayoutJson`.
    *   **Deserialization:** When editing an existing "UploadedPdf" template, parse `Model.CanvasLayoutJson` and use Fabric.js to re-create the text objects on their respective canvases.
*   **Placeholder Detection (Canvas):** The `updatePlaceholdersListFromCanvas()` JavaScript function will need to iterate through all text objects on all Fabric canvases, extract their text, find `<<FieldName>>` patterns, and update the UI list.
*   **Server-Side PDF Generation (`GeneratePdfFromCanvasLayoutAsync` in `PdfProcessingService`):**
    *   This method will receive the `PageImagePathsJson` (which it resolves to actual image files from `wwwroot`) and the `CanvasLayoutJson`.
    *   It will use a library like iText 7 or PdfSharp.
    *   For each page:
        1.  Create a new page in the output PDF.
        2.  Load the corresponding background image.
        3.  Draw the background image onto the PDF page.
        4.  Parse the `CanvasLayoutJson` for that page's text objects.
        5.  For each text object:
            *   Perform placeholder replacement on `object.text` using the `jsonData` input.
            *   Draw the (processed) text onto the PDF page at `object.left`, `object.top` with the specified `object.fontFamily`, `object.fontSize`, `object.fill`, `object.angle`, etc. Font handling can be tricky across libraries.
*   **User Experience:** Managing multiple canvases for multiple pages can be complex. Consider a UI with thumbnails for page navigation, where clicking a thumbnail loads the corresponding page into a main editor canvas.
*   **Error Handling and Robustness:** PDF processing and canvas manipulation can have many edge cases.

This is a substantial feature, and the client-side Fabric.js part is a mini-application in itself. Start with one page, get the text addition and serialization working, then expand.

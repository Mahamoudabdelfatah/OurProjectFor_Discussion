This is a great feature request that leverages the power of both Fabric.js for rich visual design and HTML for dynamic content placement. The "Hybrid" approach you've outlined is indeed the most efficient for web applications, as it moves the rendering responsibility to the client's browser.

Here's a breakdown of the implementation strategy and the necessary code modifications.

**Core Strategy:**

1.  **Fabric.js for Design:** The template editor (likely a separate UI or part of the Design view) will use Fabric.js to allow users to:
    *   Upload and place static images.
    *   Add text elements, position them, style them (font, size, color, rotation).
    *   Crucially, associate these text elements with specific `<<PlaceholderName>>` values.
    *   The final design of these elements (image, text position, style) will be saved as a Fabric.js JSON object.

2.  **Storing Fabric.js JSON:** The `Template` model and its DTOs will need a new field to store this Fabric.js JSON.

3.  **`ProcessTemplate` Method:**
    *   When processing a template for PDF generation:
        *   The `HtmlContent` will be processed as usual for `<<FieldName>>` and `{{conditional}}`.
        *   The *Fabric.js JSON* will be parsed.
        *   For each text object in the Fabric.js JSON that is marked as a placeholder (i.e., it has `<<PlaceholderName>>` associated with it):
            *   The `<<PlaceholderName>>` will be replaced with the actual data value (from `jsonData` or resolved internal data).
            *   An HTML `<div>` element will be generated for this processed text.
            *   This `<div>` will be positioned and styled precisely according to the properties stored in the Fabric.js JSON ( `left`, `top`, `fontFamily`, `fontSize`, `fill` for color, `angle` for rotation, etc.).
        *   The base image(s) from Fabric.js JSON will be embedded in the HTML, likely as `<img>` tags with `src` pointing to data URLs.
        *   The generated HTML `<div>`s for placeholders will be absolutely positioned within a container that holds the image(s), effectively overlaying the text on the image.

**Implementation Steps & Code Modifications:**

First, let's define the new field in our data models and DTOs.

---

**1. `PDFGenerator.Infrastructure\DataAccess\Models\Template.cs`**
(Adding `FabricJson` field)

```csharp
using System.ComponentModel.DataAnnotations;
using System.Collections.Generic;
using System;

namespace PdfGeneratorApp.Models
{
    public class Template
    {
        public int Id { get; set; }

        [Required]
        [StringLength(100)]
        public string Name { get; set; }

        public int TestingVersion { get; set; } = 1;
        public int? ProductionVersion { get; set; } = 1;

        public DateTime LastModified { get; set; } = DateTime.Now;

        // New field to store Fabric.js JSON definition of the template's visual layout
        public string? FabricJson { get; set; }

        public ICollection<TemplateVersion> Versions { get; set; }
    }
}
```

---

**2. `PDFGenerator.Infrastructure\DataAccess\Dtos\TemplateDataAccessDto.cs`**
(Adding `FabricJson` field)

```csharp
// File: Infrastructure/Data/Dtos/TemplateDataAccessDto.cs
using PdfGeneratorApp.Models;
using System;
using System.Collections.Generic;

namespace PDFGenerator.Infrastructure.DataAccess.Dtos
{
    public class TemplateDataAccessDto
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string HtmlContent { get; set; } // Standard HTML content
        public string? Description { get; set; }
        public string? ExampleJsonData { get; set; }
        public string? InternalDataConfigJson { get; set; }

        // Versioning properties
        public int TestingVersion { get; set; }
        public int? ProductionVersion { get; set; }

        public DateTime LastModified { get; set; }

        // New field for Fabric.js JSON
        public string? FabricJson { get; set; }

        public ICollection<TemplateVersionDataAccessDto> Versions { get; set; }
    }
}
```

---

**3. `PDFGenerator.Infrastructure\DataAccess\Dtos\TemplateVersionDataAccessDto.cs`**
(Adding `FabricJson` field for versions if it's per-version)

*   **Decision:** Should Fabric.js JSON be stored per `TemplateVersion` or per `Template`?
    *   If it's per `TemplateVersion`, it means each version can have a different layout. This is more flexible but potentially more complex.
    *   If it's per `Template`, it implies the layout is global for the template, and the `HtmlContent` might be considered deprecated or for simpler fallbacks.
    *   Given the requirement "add static image at my template", it implies a visual layout that might change over template versions. Let's assume it's per `TemplateVersion` for maximum flexibility.

```csharp
// File: Infrastructure/Data/Dtos/TemplateVersionDataAccessDto.cs
using System;

namespace PDFGenerator.Infrastructure.DataAccess.Dtos
{
    public class TemplateVersionDataAccessDto
    {
        public int Id { get; set; }
        public int TemplateId { get; set; }
        public int VersionNumber { get; set; }
        public string HtmlContent { get; set; } // Fallback/standard HTML content
        public string? Description { get; set; }
        public string? ExampleJsonData { get; set; }
        public string? InternalDataConfigJson { get; set; }
        public DateTime CreatedDate { get; set; }

        // Soft delete properties
        public bool IsDeleted { get; set; }
        public DateTime? DeletedDate { get; set; }

        // New field for Fabric.js JSON specific to this version
        public string? FabricJson { get; set; }
    }
}
```

---

**4. `PDFGenerator.Infrastructure\DataAccess\MappingProfile\DataAccessMappingProfile.cs`**
(Updating mappings for `FabricJson`)

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
            CreateMap<Template, TemplateDataAccessDto>()
                .ForMember(dest => dest.TestingVersion, opt => opt.MapFrom(src => src.TestingVersion))
                .ForMember(dest => dest.ProductionVersion, opt => opt.MapFrom(src => src.ProductionVersion))
                .ForMember(dest => dest.FabricJson, opt => opt.MapFrom(src => src.FabricJson)) // Map FabricJson from Template
                .ForMember(dest => dest.Versions, opt => opt.Ignore()); // Explicitly ignore Versions if not mapping here

            CreateMap<TemplateDataAccessDto, Template>()
                .ForMember(dest => dest.TestingVersion, opt => opt.MapFrom(src => src.TestingVersion))
                .ForMember(dest => dest.ProductionVersion, opt => opt.MapFrom(src => src.ProductionVersion))
                .ForMember(dest => dest.FabricJson, opt => opt.MapFrom(src => src.FabricJson)) // Map FabricJson back to Template
                .ForMember(dest => dest.Versions, opt => opt.Ignore()); // Ignore Versions collection for simplicity in this mapping


            CreateMap<TemplateVersion, TemplateDataAccessDto>()
                 .ForMember(dest => dest.Id, opt => opt.Ignore())
                 .ForMember(dest => dest.Name, opt => opt.Ignore())
                 .ForMember(dest => dest.TestingVersion, opt => opt.Ignore())
                 .ForMember(dest => dest.ProductionVersion, opt => opt.Ignore())
                 .ForMember(dest => dest.LastModified, opt => opt.Ignore())
                 .ForMember(dest => dest.Versions, opt => opt.Ignore())
                 // Map FabricJson from TemplateVersion
                 .ForMember(dest => dest.FabricJson, opt => opt.MapFrom(src => src.FabricJson))
                 .ReverseMap();

            CreateMap<TemplateVersion, TemplateVersionDataAccessDto>()
                .ForMember(dest => dest.IsDeleted, opt => opt.MapFrom(src => src.IsDeleted))
                .ForMember(dest => dest.DeletedDate, opt => opt.MapFrom(src => src.DeletedDate))
                // Map FabricJson from TemplateVersion
                .ForMember(dest => dest.FabricJson, opt => opt.MapFrom(src => src.FabricJson))
                .ReverseMap();

            CreateMap<Template, TemplateSimpleDto>()
                .ForMember(dest => dest.Id, opt => opt.MapFrom(src => src.Id))
                .ForMember(dest => dest.Name, opt => opt.MapFrom(src => src.Name))
                .ForMember(dest => dest.Description, opt => opt.MapFrom(src => src.Description))
                .ForMember(dest => dest.TestingVersion, opt => opt.MapFrom(src => src.TestingVersion))
                .ForMember(dest => dest.ProductionVersion, opt => opt.MapFrom(src => src.ProductionVersion))
                .ForMember(dest => dest.LastModified, opt => opt.MapFrom(src => src.LastModified));

             CreateMap<Template, TemplatesDocDataAccessDto>()
                .ForMember(dest => dest.Id, opt => opt.MapFrom(src => src.Id))
                .ForMember(dest => dest.Name, opt => opt.MapFrom(src => src.Name))
                .ForMember(dest => dest.Description, opt => opt.MapFrom(src => src.Description))
                .ForMember(dest => dest.TestingVersion, opt => opt.MapFrom(src => src.TestingVersion))
                .ForMember(dest => dest.ProductionVersion, opt => opt.MapFrom(src => src.ProductionVersion));
        }
    }
}
```

---

**5. `PDFGenerator.Web\Dtos\Template\TemplateDetailDto.cs`**
(Adding `FabricJson` field)

```csharp
using System.ComponentModel.DataAnnotations;

namespace PDFGenerator.Web.Dtos.Template
{
    public class TemplateDetailDto
    {
        public int Id { get; set; }

        [Required]
        [StringLength(100, ErrorMessage = "Template Name cannot exceed 100 characters.")]
        public string Name { get; set; }

        public string? Description { get; set; }

        [Required(ErrorMessage = "HTML Content is required.")]
        public string HtmlContent { get; set; }

        public string? ExampleJsonData { get; set; }

        public string? InternalDataConfigJson { get; set; }

        // Versioning properties
        public int TestingVersion { get; set; }
        public int? ProductionVersion { get; set; }

        public DateTime LastModified { get; set; }

        // New field for Fabric.js JSON
        public string? FabricJson { get; set; }
    }
}
```

---

**6. `PDFGenerator.Web\Dtos\Template\TemplateCreateDto.cs`**
(Adding `FabricJson` field)

```csharp
using System.ComponentModel.DataAnnotations;

namespace PDFGenerator.Web.Dtos.Template
{
    public class TemplateCreateDto
    {
        [Required]
        [StringLength(100, ErrorMessage = "Template Name cannot exceed 100 characters.")]
        public string Name { get; set; }

        public string? Description { get; set; }

        [Required(ErrorMessage = "HTML Content is required.")]
        public string HtmlContent { get; set; }

        public string? ExampleJsonData { get; set; }

        public string? InternalDataConfigJson { get; set; }

        // New field for Fabric.js JSON
        public string? FabricJson { get; set; }
    }
}
```

---

**7. `PDFGenerator.Web\Dtos\Template\TemplateUpdateDto.cs`**
(Adding `FabricJson` field)

```csharp
using System.ComponentModel.DataAnnotations;

namespace PDFGenerator.Web.Dtos.Template
{
    public class TemplateUpdateDto
    {
        public int Id { get; set; }

        public string? Description { get; set; }

        [Required(ErrorMessage = "HTML Content is required.")]
        public string HtmlContent { get; set; }

        public string? ExampleJsonData { get; set; }

        public string? InternalDataConfigJson { get; set; }

        // New field for Fabric.js JSON
        public string? FabricJson { get; set; }
    }
}
```

---

**8. `PDFGenerator.Web\Dtos\Template\TemplateListDto.cs`**
(Already updated in the previous step to include versioning, now adding FabricJson if needed for list view, though not strictly required)

```csharp
namespace PDFGenerator.Web.Dtos.Template
{
    public class TemplateListDto
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string? Description { get; set; }
        public int TestingVersion { get; set; }
        public int? ProductionVersion { get; set; }
        public DateTime LastModified { get; set; }
        // public string? FabricJson { get; set; } // Only add if needed for list view
    }
}
```

---

**9. `PDFGenerator.Web\Dtos\Template\TemplatesDocDto.cs`**
(Already updated in the previous step to include versioning, adding FabricJson if needed for doc view)

```csharp
﻿using System.ComponentModel.DataAnnotations;

namespace PDFGenerator.Web.Dtos.Template
{
    public class TemplatesDocDto
    {
        public int Id { get; set; }
        [Required]
        [StringLength(100, ErrorMessage = "Template Name cannot exceed 100 characters.")]
        public string Name { get; set; }
        public string? Description { get; set; }
        public string? ExampleJsonData { get; set; }
        public string? InternalDataConfigJson { get; set; }
        public int TestingVersion { get; set; }
        public int? ProductionVersion { get; set; }
        // public string? FabricJson { get; set; } // Only add if needed for doc view
    }
}
```

---

**10. `PDFGenerator.Infrastructure\DataAccess\Repositories\Interfaces\ITemplateRepository.cs`**
(Adding the new `GetTemplateContentByVersionReferenceAsync` method)

```csharp
// File: Infrastructure/Data/Repositories/ITemplateRepository.cs
using PDFGenerator.Infrastructure.DataAccess.Dtos;
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Infrastructure.Data.Repositories.Base;
using PdfGeneratorApp.Models;
using System.Threading.Tasks;

namespace PdfGeneratorApp.Infrastructure.Data.Repositories
{
    public interface ITemplateRepository : IBaseRepository<Template, TemplateDataAccessDto>
    {
        Task<Result<List<TemplateSimpleDto>>> GetAllTemplateSimplAsync();
        Task<Result<List<TemplatesDocDataAccessDto>>> GetAllAsync();

        // This method remains for UI Design page, fetches Testing version content
        Task<Result<TemplateDataAccessDto>> GetByNameAsync(string name);

        Task<Result<bool>> AnyByNameAsync(string name);
        Task<Result<TemplateDataAccessDto>> CreateNewTemplateAsync(TemplateDataAccessDto templateDataAccessDto);
        Task<Result<TemplateDataAccessDto>> UpdateTemplateAsync(TemplateDataAccessDto templateDataAccessDto);
        Task<Result<int>> RevertTemplateAsync(string templateName, int targetVersionNumber, string versionReferenceType);
        Task<Result<int>> PublishTemplateAsync(string templateName);

        // NEW: Method to get template content based on version reference type.
        // Used by the PDF generation handler to fetch content for Testing or Production.
        Task<Result<TemplateDataAccessDto>> GetTemplateContentByVersionReferenceAsync(string templateName, string versionReferenceType);
    }
}
```

---

**11. `PDFGenerator.Infrastructure\DataAccess\Repositories\Implementation\TemplateRepository.cs`**
(Implementing `GetTemplateContentByVersionReferenceAsync`)

```csharp
// File: Infrastructure/Data/Repositories/TemplateRepository.cs
using AutoMapper;
using Microsoft.EntityFrameworkCore;
using PDFGenerator.Infrastructure.DataAccess.Dtos;
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Data;
using PdfGeneratorApp.Infrastructure.Data.Repositories.Base;
using PdfGeneratorApp.Models;
using PdfGeneratorApp.Services;
using System.Text.Json;
using System.Linq;
using System;
using System.Collections.Generic; // Ensure List<T> is available

namespace PdfGeneratorApp.Infrastructure.Data.Repositories
{
    public class TemplateRepository : BaseRepository<Template, TemplateDataAccessDto>, ITemplateRepository
    {
        private readonly ApplicationDbContext context;
        private readonly IMapper _mapper;
        private readonly TemplateProcessingService _templateProcessingService;

        public TemplateRepository(ApplicationDbContext context, IMapper mapper, TemplateProcessingService templateProcessingService) : base(context, mapper)
        {
            this.context = context;
            _mapper = mapper;
            _templateProcessingService = templateProcessingService;
        }

        public async Task<Result<List<TemplateSimpleDto>>> GetAllTemplateSimplAsync()
        {
            try
            {
                List<TemplateSimpleDto> data = await context.Templates.Select(t => new TemplateSimpleDto()
                {
                    Id = t.Id,
                    Name = t.Name,
                    Description = t.Description,
                    LastModified = t.LastModified,
                    TestingVersion = t.TestingVersion,
                    ProductionVersion = t.ProductionVersion

                }).ToListAsync();
                return Result<List<TemplateSimpleDto>>.Success(data);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in TemplateRepository.GetAllTemplateSimplAsync: {ex.Message}");
                return Result<List<TemplateSimpleDto>>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }

        public async Task<Result<List<TemplatesDocDataAccessDto>>> GetAllAsync()
        {
             try
             {
                 var templates = await (from t in context.Templates
                                        join tv in context.TemplateVersions
                                        on new { TemplateId = t.Id, Version = t.TestingVersion }
                                        equals new { tv.TemplateId, Version = tv.VersionNumber }
                                        where !tv.IsDeleted
                                        select new TemplatesDocDataAccessDto
                                        {
                                            Id = t.Id,
                                            Name = t.Name,
                                            Description = t.Description,
                                            ExampleJsonData = tv.ExampleJsonData,
                                            InternalDataConfigJson = tv.InternalDataConfigJson,
                                            TestingVersion = t.TestingVersion,
                                            ProductionVersion = t.ProductionVersion
                                        }).ToListAsync();
                return Result<List<TemplatesDocDataAccessDto>>.Success(templates);
             }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in TemplateRepository.GetAllAsync: {ex.Message}");
                return Result<List<TemplatesDocDataAccessDto>>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }

        // Remains the same: fetches Testing version content for Design UI.
        public async Task<Result<TemplateDataAccessDto>> GetByNameAsync(string name)
        {
            Template? template = await context.Templates
                                      .Include(t => t.Versions)
                                      .SingleOrDefaultAsync(t => t.Name == name);

            if (template == null)
            {
                return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.TemplateNotFound);
            }
            TemplateVersion? currentTestingVersionContent = template.Versions
                .SingleOrDefault(tv => tv.VersionNumber == template.TestingVersion && !tv.IsDeleted);

            if (currentTestingVersionContent == null)
            {
                 return Result<TemplateDataAccessDto>.Failure(string.Format(ErrorMessageUserConst.VersionNotFound, template.TestingVersion, name));
            }
            var templateDto = _mapper.Map<TemplateDataAccessDto>(template);
            templateDto.HtmlContent = currentTestingVersionContent.HtmlContent;
            templateDto.Description = currentTestingVersionContent.Description;
            templateDto.ExampleJsonData = currentTestingVersionContent.ExampleJsonData;
            templateDto.InternalDataConfigJson = currentTestingVersionContent.InternalDataConfigJson;
            templateDto.TestingVersion = template.TestingVersion;
            templateDto.ProductionVersion = template.ProductionVersion;
            return Result<TemplateDataAccessDto>.Success(templateDto);
        }

        public async Task<Result<bool>> AnyByNameAsync(string name)
        {
            try
            {
                var exists = await context.Templates.AnyAsync(t => t.Name == name);
                return Result<bool>.Success(exists);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in TemplateRepository.AnyByNameAsync: {ex.Message}");
                return Result<bool>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }

        public async Task<Result<TemplateDataAccessDto>> CreateNewTemplateAsync(TemplateDataAccessDto templateDto)
        {
            templateDto.Name = templateDto.Name.Replace(" ", "_");
            var nameExistsResult = await context.Templates.AnyAsync(t => t.Name == templateDto.Name);
            if (nameExistsResult) return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.TemplateNameExists);
            try
            {
                templateDto.ExampleJsonData = _templateProcessingService.GenerateExampleJson(templateDto.HtmlContent);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error generating example JSON on create: {ex.Message}");
                return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.ExampleJsonGenerationFailed);
            }
            if (!string.IsNullOrWhiteSpace(templateDto.InternalDataConfigJson))
            {
                try
                {
                    using JsonDocument doc = JsonDocument.Parse(templateDto.InternalDataConfigJson);
                    if (doc.RootElement.ValueKind != JsonValueKind.Object)
                    {
                        return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.InternalDataConfigNotObject);
                    }
                }
                catch (JsonException)
                {
                    return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.InternalDataConfigInvalidJson);
                }
            }
            templateDto.TestingVersion = 1;
            templateDto.ProductionVersion = 1;
            templateDto.LastModified = DateTime.Now;
            var initialVersion = new TemplateVersion
            {
                VersionNumber = 1, CreatedDate = DateTime.Now, HtmlContent = templateDto.HtmlContent,
                Description = templateDto.Description, ExampleJsonData = templateDto.ExampleJsonData,
                InternalDataConfigJson = templateDto.InternalDataConfigJson, IsDeleted = false
            };
            try
            {
                Template template = new Template
                {
                    Name = templateDto.Name, Description = templateDto.Description, TestingVersion = templateDto.TestingVersion,
                    ProductionVersion = templateDto.ProductionVersion, LastModified = templateDto.LastModified,
                    Versions = new List<TemplateVersion> { initialVersion }
                };
                await context.Templates.AddAsync(template);
                return Result<TemplateDataAccessDto>.Success(templateDto);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in TemplateRepository.CreateNewTemplateAsync: {ex.Message}");
                return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }

        public async Task<Result<TemplateDataAccessDto>> UpdateTemplateAsync(TemplateDataAccessDto templateDto)
        {
            if (!string.IsNullOrWhiteSpace(templateDto.InternalDataConfigJson))
            {
                 try {
                     using JsonDocument doc = JsonDocument.Parse(templateDto.InternalDataConfigJson);
                     if (doc.RootElement.ValueKind != JsonValueKind.Object)
                     {
                         return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.InternalDataConfigNotObject);
                     }
                } catch (JsonException) {
                     return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.InternalDataConfigInvalidJson);
                }
            }
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
                TemplateId = templateDto.Id, VersionNumber = nextVersionNumber, HtmlContent = templateDto.HtmlContent,
                Description = templateDto.Description, ExampleJsonData = _templateProcessingService.GenerateExampleJson(templateDto.HtmlContent),
                InternalDataConfigJson = templateDto.InternalDataConfigJson, CreatedDate = DateTime.Now, IsDeleted = false
            };
            existingTemplate.Versions.Add(newVersion);
            existingTemplate.TestingVersion = newVersion.VersionNumber;
            existingTemplate.Description = templateDto.Description;
            existingTemplate.LastModified = DateTime.Now;
            var updatedTemplateDto = _mapper.Map<TemplateDataAccessDto>(existingTemplate);
            updatedTemplateDto.HtmlContent = newVersion.HtmlContent;
            updatedTemplateDto.ExampleJsonData = newVersion.ExampleJsonData;
            updatedTemplateDto.InternalDataConfigJson = newVersion.InternalDataConfigJson;
            return Result<TemplateDataAccessDto>.Success(updatedTemplateDto);
        }

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
            switch (versionReferenceType.ToLowerInvariant())
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

        // NEW METHOD IMPLEMENTATION: Get Template Content based on a specified version reference type
        public async Task<Result<TemplateDataAccessDto>> GetTemplateContentByVersionReferenceAsync(string templateName, string versionReferenceType)
        {
             Template? template = await context.Templates
                                       .Include(t => t.Versions) // Crucial to include versions to find the target
                                       .SingleOrDefaultAsync(t => t.Name == templateName);

             if (template == null)
             {
                 return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.TemplateNotFound);
             }

             int targetVersionNumber;
             string normalizedVersionReferenceType = versionReferenceType.ToLowerInvariant(); // Normalize input for comparison

             // Determine the target version number based on the reference type.
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
                     // This case should ideally be caught by handler's IsValid check, but good as a fallback.
                     return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.InvalidVersionReferenceType);
             }

             // Find the TemplateVersion entity matching the determined version number.
             // Ensure it's not deleted.
             TemplateVersion? targetVersionContent = template.Versions
                 .SingleOrDefault(tv => tv.VersionNumber == targetVersionNumber && !tv.IsDeleted);

             if (targetVersionContent == null)
             {
                  // This indicates an inconsistency: the template points to a version number that doesn't exist or is deleted.
                  string referencedVersionType = (normalizedVersionReferenceType == VersionReferenceType.Testing.ToLowerInvariant()) ? "Testing" : "Production";
                  return Result<TemplateDataAccessDto>.Failure($"Content for {referencedVersionType} version {targetVersionNumber} not found or is deleted for template '{templateName}'.");
             }

             // Create the TemplateDataAccessDto with properties from the Template entity and content from the target version.
             var templateDto = _mapper.Map<TemplateDataAccessDto>(template); // Maps Id, Name, TestingVersion, ProductionVersion, LastModified, Description, FabricJson

             // Manually map the content properties from the specific target version.
             templateDto.HtmlContent = targetVersionContent.HtmlContent;
             templateDto.Description = targetVersionContent.Description; // Use version's description if available and preferred.
             templateDto.ExampleJsonData = targetVersionContent.ExampleJsonData;
             templateDto.InternalDataConfigJson = targetVersionContent.InternalDataConfigJson;
             // The version numbers on the DTO should reflect the template's current state.

             return Result<TemplateDataAccessDto>.Success(templateDto);
        }
    }
}
```

---

**12. `PDFGenerator.Web\Services\GeneratePdfHandler.cs`**
(Modified to accept and use `versionReferenceType`)

```csharp
// File: Handlers/GeneratePdfHandler.cs
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Services;
using System.Text.Json;
using WkHtmlToPdfDotNet;
using WkHtmlToPdfDotNet.Contracts;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using System.Threading.Tasks;

namespace PdfGeneratorApp.Handlers
{
    // Interface updated to include versionReferenceType in the request tuple.
    public interface IGeneratePdfHandler : IHandler<(string templateName, JsonElement requestBodyJson, string mode, string? versionReferenceType), byte[]>
    {
    }

    public class GeneratePdfHandler : IGeneratePdfHandler
    {
        private readonly IUnitOfWork _unitOfWork;
        private readonly IConverter _converter;
        private readonly TemplateProcessingService _templateProcessingService;

        public GeneratePdfHandler(IUnitOfWork unitOfWork, IConverter converter, TemplateProcessingService templateProcessingService)
        {
            _unitOfWork = unitOfWork;
            _converter = converter;
            _templateProcessingService = templateProcessingService;
        }

        public async Task<Result<byte[]>> HandleAsync((string templateName, JsonElement requestBodyJson, string mode, string? versionReferenceType) request)
        {
            try
            {
                // Determine the effective version type to use. Default to Testing if invalid or null.
                string effectiveVersionType = VersionReferenceType.Testing; // Default
                if (!string.IsNullOrWhiteSpace(request.versionReferenceType) && VersionReferenceType.IsValid(request.versionReferenceType))
                {
                    effectiveVersionType = request.versionReferenceType;
                }
                else if (!string.IsNullOrWhiteSpace(request.versionReferenceType))
                {
                    // Log or handle invalid type if it's explicitly provided but invalid.
                    Console.WriteLine($"Warning: Invalid versionReferenceType '{request.versionReferenceType}' provided. Defaulting to Testing.");
                }


                // Fetch template content using the NEW repository method, specifying the desired version type.
                var repoResult = await _unitOfWork.Templates.GetTemplateContentByVersionReferenceAsync(request.templateName, effectiveVersionType);

                if (!repoResult.IsCompleteSuccessfully)
                {
                    // Propagate failure from repository (e.g., Template Not Found, Version Content Not Found/Deleted, Production version not set).
                    return Result<byte[]>.Failure(repoResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                var templateDataAccessDto = repoResult.Data; // Get the DTO with content from the target version.

                // Logic for determining finalDataForHtmlProcessing based on 'mode' remains the same.
                JsonElement finalDataForHtmlProcessing;
                JsonElement insideParameters = default;

                switch (request.mode.ToLowerInvariant())
                {
                    case "outside":
                        finalDataForHtmlProcessing = request.requestBodyJson;
                        break;

                    case "inside":
                        if (request.requestBodyJson.ValueKind != JsonValueKind.Object)
                        {
                            return Result<byte[]>.Failure(ErrorMessageUserConst.InsideModeBodyNotObject);
                        }
                        if (request.requestBodyJson.TryGetProperty("parameters", out JsonElement parametersElement))
                        {
                            insideParameters = parametersElement;
                        }
                        // Resolve internal data using the fetched template's InternalDataConfigJson (which comes from the target version)
                        finalDataForHtmlProcessing = _templateProcessingService.ResolveInternalData(templateDataAccessDto.InternalDataConfigJson, insideParameters);
                        break;

                    default:
                        return Result<byte[]>.Failure(ErrorMessageUserConst.InvalidMode);
                }

                // Process the HTML content (from the fetched version) with the determined data.
                string processedHtml = _templateProcessingService.ProcessTemplate(templateDataAccessDto.HtmlContent, finalDataForHtmlProcessing);

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
                        }
                    }
                };

                byte[] pdf = _converter.Convert(doc);

                if (pdf == null || pdf.Length == 0)
                {
                    return Result<byte[]>.Failure(ErrorMessageUserConst.PdfGenerationFailed + " Ensure wkhtmltopdf is correctly installed and accessible.");
                }

                return Result<byte[]>.Success(pdf);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in GeneratePdfHandler: {ex.Message}");
                return Result<byte[]>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }
    }
}
```

---

**12. `PDFGenerator.Web\Controllers\PdfController.cs`**
(Modified POST action to pass `versionType` to handler)

```csharp
// File: Controllers/PdfController.cs
using Microsoft.AspNetCore.Mvc;
using System.Text.Json;
using PdfGeneratorApp.Handlers;
using PdfGeneratorApp.Common;
using Microsoft.AspNetCore.Authorization;


namespace PdfGeneratorApp.Controllers
{
    public class PdfController : Controller
    {
        private readonly IGetTemplateByNameHandler _getTemplateByNameHandler;
        private readonly IGeneratePdfHandler _generatePdfHandler;

        public PdfController(IGetTemplateByNameHandler getTemplateByNameHandler, IGeneratePdfHandler generatePdfHandler)
        {
            _getTemplateByNameHandler = getTemplateByNameHandler;
            _generatePdfHandler = generatePdfHandler;
        }

        // GET: /pdf/generate/{templateName}
        [HttpGet("pdf/generate/{templateName}")]
        public async Task<IActionResult> Generate(string templateName)
        {
            var result = await _getTemplateByNameHandler.HandleAsync(templateName);

            if (!result.IsCompleteSuccessfully)
            {
                if (result.ErrorMessages == ErrorMessageUserConst.TemplateNotFound) return NotFound($"Template '{templateName}' not found.");

                return StatusCode(500, result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
            }

            var templateDto = result.Data;

            return RedirectToAction("Design", "Template", new { templateName = templateDto.Name });
        }

        // POST: /pdf/generate/{templateName}
        // Added [FromQuery] string? versionType parameter.
        [HttpPost("pdf/generate/{templateName}")]
        [Consumes("application/json")]
        public async Task<IActionResult> Generate(
            string templateName,
            [FromBody] JsonElement requestBodyJson,
            [FromQuery] string mode = "outside",
            [FromQuery] string? versionType = null) // New optional query parameter
        {
            // Pass versionType to the handler's request tuple.
            var request = (templateName, requestBodyJson, mode, versionType);
            var result = await _generatePdfHandler.HandleAsync(request);

            if (!result.IsCompleteSuccessfully)
            {
                if (result.ErrorMessages == ErrorMessageUserConst.TemplateNotFound)
                {
                    return NotFound($"Template '{templateName}' not found.");
                }
                if (result.ErrorMessages == ErrorMessageUserConst.InvalidMode ||
                    result.ErrorMessages == ErrorMessageUserConst.InsideModeBodyNotObject ||
                    result.ErrorMessages == ErrorMessageUserConst.InvalidVersionReferenceType)
                {
                    return BadRequest(result.ErrorMessages);
                }
                // Handle cases where Production version is requested but not set.
                if (result.ErrorMessages?.Contains("Production version is not set") ?? false)
                {
                     return BadRequest(result.ErrorMessages);
                }
                // Handle case where requested version content is deleted or not found.
                 if (result.ErrorMessages?.Contains("not found or is deleted") ?? false)
                 {
                      return NotFound(result.ErrorMessages);
                 }

                return StatusCode(500, result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
            }

            // Include version type in the filename for clarity.
            string filenameVersionPart = string.IsNullOrWhiteSpace(versionType) ? "Testing" : versionType;
            return File(result.Data, "application/pdf", $"{templateName}_{filenameVersionPart}_{DateTime.Now:yyyyMMddHHmmss}.pdf");
        }
    }
}
```

---

**13. `PDFGenerator.Web\Views\Docs\Templates.cshtml`**
(Modified to include version selection in the "Try it out" section)

```html
@using System.Text.Json
@using PDFGenerator.Web.Dtos.Template
@using PdfGeneratorApp.Common // For VersionReferenceType constants
@model List<TemplatesDocDto>

@{
    ViewData["Title"] = "API Documentation";
}

<div class="container">
    <div class="page-header">
        <h1>@ViewData["Title"]</h1>
        <p class="page-subtitle">
            Test and understand the PDF generation API endpoints. Each template uses its selected version for content.
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
                string internalDataConfigJsonTextareaId = $"internalDataConfig_{template.Id}";
                string insideParametersJsonTextareaId = $"insideParameters_{template.Id}";
                // Unique name for the version type radio buttons within this accordion item
                string versionTypeRadioName = $"versionType_{template.Id}";


                <div class="accordion-item">
                    <h2 class="accordion-header" id="@headingId">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#@collapseId" aria-expanded="false" aria-controls="@collapseId">
                            <span class="badge bg-success me-2 p-2">POST</span>
                            <code class="me-2 fs-6">/pdf/generate/@template.Name</code>
                            <span class="text-muted small">@template.Description</span>
                             <!-- Display versions here -->
                            <span class="ms-auto badge bg-secondary me-1">Testing: v @template.TestingVersion</span>
                            @if (template.ProductionVersion.HasValue)
                            {
                                <span class="badge bg-success">Prod: v @template.ProductionVersion.Value</span>
                            }
                            else
                            {
                                <span class="badge bg-secondary">Prod: N/A</span>
                            }
                        </button>
                    </h2>
                    <div id="@collapseId" class="accordion-collapse collapse" aria-labelledby="@headingId" data-bs-parent="#templateDocsAccordion">
                        <div class="accordion-body">
                            <h5>Endpoint Summary</h5>
                            <p>Generates a PDF document based on the <strong>@template.Name</strong> template. Content is retrieved from the selected template version (Testing or Production). Data is provided via the request body (Outside mode) or resolved internally using the template's configuration and optional parameters (Inside mode).</p>

                            <hr class="my-3" />

                            <div class="try-it-out-section" data-template-name="@template.Name">
                                <h5><i class="fas fa-vial me-1"></i> Try it out</h5>
                                <p class="small text-muted">Select mode and version, configure data/parameters, and click "Execute".</p>

                                <!-- Mode Selection -->
                                <div class="form-group mb-3">
                                    <label class="form-label fw-semibold">Select Mode:</label>
                                    <div class="form-check form-check-inline">
                                        <input class="form-check-input mode-radio" type="radio" name="mode_@template.Id" id="mode_outside_@template.Id" value="outside" checked>
                                        <label class="form-check-label" for="mode_outside_@template.Id">Outside</label>
                                    </div>
                                    <div class="form-check form-check-inline">
                                        <input class="form-check-input mode-radio" type="radio" name="mode_@template.Id" id="mode_inside_@template.Id" value="inside">
                                        <label class="form-check-label" for="mode_inside_@template.Id">Inside</label>
                                    </div>
                                </div>

                                <!-- Version Type Selection -->
                                 <div class="form-group mb-3">
                                     <label class="form-label fw-semibold">Select Version:</label>
                                     <div class="form-check form-check-inline">
                                         <input class="form-check-input version-type-radio" type="radio" name="@versionTypeRadioName" id="version_testing_@template.Id" value="@VersionReferenceType.Testing" checked>
                                         <label class="form-check-label" for="version_testing_@template.Id">Testing (v @template.TestingVersion)</label>
                                     </div>
                                     @if (template.ProductionVersion.HasValue)
                                     {
                                         <div class="form-check form-check-inline">
                                             <input class="form-check-input version-type-radio" type="radio" name="@versionTypeRadioName" id="version_production_@template.Id" value="@VersionReferenceType.Production">
                                             <label class="form-check-label" for="version_production_@template.Id">Production (v @template.ProductionVersion.Value)</label>
                                         </div>
                                     }
                                 </div>

                                <!-- Data Payload for OUTSIDE Mode -->
                                <div class="form-group mb-3 data-config-section" data-mode="outside">
                                    <label for="@jsonDataTextareaId" class="form-label fw-semibold">Request Body JSON for Outside Mode</label>
                                    <textarea class="form-control json-payload" id="@jsonDataTextareaId" rows="10" style="font-family: monospace; font-size: 0.875em;">@FormatJsonForTextarea(template.ExampleJsonData)</textarea>
                                    <small class="form-text text-muted">This JSON is sent in the request body as the data payload.</small>
                                </div>

                                <!-- Configuration Display for INSIDE Mode -->
                                <div class="form-group mb-3 data-config-section" data-mode="inside" style="display:none;">
                                    <label class="form-label fw-semibold">Internal Data Configuration (Read-only) for Inside Mode</label>
                                    <textarea class="form-control" id="@internalDataConfigJsonTextareaId" rows="10" style="font-family: monospace; font-size: 0.875em;" readonly>@FormatJsonForTextarea(template.InternalDataConfigJson)</textarea>
                                    <small class="form-text text-muted">This is the configuration stored for this template. Data resolution happens on the server using this config.</small>
                                </div>

                                <!-- Parameters Input for INSIDE Mode -->
                                <div class="form-group mb-3 inside-parameters-section" style="display:none;">
                                    <label for="@insideParametersJsonTextareaId" class="form-label fw-semibold">Inside Parameters JSON for Inside Mode</label>
                                    <textarea class="form-control inside-parameters-json" id="@insideParametersJsonTextareaId" rows="5" style="font-family: monospace; font-size: 0.875em;">{}</textarea>
                                    <small class="form-text text-muted">Provide JSON parameters to be used in the Internal Data Configuration (e.g., <code>{ "userNID": "12345" }</code>). This JSON will be nested under a "parameters" key in the request body.</small>
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
    public string FormatJsonForTextarea(string? jsonString)
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

            // --- Mode Selection Toggle ---
            $('.mode-radio').on('change', function() {
                var $tryItOutSection = $(this).closest('.try-it-out-section');
                var selectedMode = $(this).val();

                $tryItOutSection.find('.data-config-section').hide();
                $tryItOutSection.find('.inside-parameters-section').hide();

                if (selectedMode === 'outside') {
                     $tryItOutSection.find(`.data-config-section[data-mode="outside"]`).show();
                } else if (selectedMode === 'inside') {
                     $tryItOutSection.find(`.data-config-section[data-mode="inside"]`).show();
                     $tryItOutSection.find('.inside-parameters-section').show();
                }

                 $tryItOutSection.find('.clear-response-btn').click();
            });

             // --- Version Type Selection Toggle ---
             // This handles the change event for the version radio buttons.
             // It's good practice to trigger a change if needed for initial state setup.
             // No specific UI changes are made here based on version selection, but it's read by the execute button.
             $('.version-type-radio').on('change', function() {
                 // Optionally, if you wanted to update descriptions or example JSON based on version,
                 // you would add that logic here. For now, it just captures the selection.
             });


            // --- Execute Button Logic ---
            $('.execute-btn').on('click', function() {
                var $button = $(this);
                var $tryItOutSection = $button.closest('.try-it-out-section');
                var templateName = $tryItOutSection.data('template-name');
                var selectedMode = $tryItOutSection.find('.mode-radio:checked').val();
                // Read the selected version type from the radio buttons
                var selectedVersionType = $tryItOutSection.find('.version-type-radio:checked').val();


                var $responseSection = $tryItOutSection.find('.response-section');
                var $responseStatusDiv = $tryItOutSection.find('.response-status');
                var $responseOutputDiv = $tryItOutSection.find('.response-output');
                var $clearButton = $tryItOutSection.find('.clear-response-btn');

                var requestBodyPayload = null;

                $responseSection.hide();
                $responseStatusDiv.empty().removeClass('text-danger text-success text-warning alert alert-danger alert-success alert-warning');
                $responseOutputDiv.empty().removeClass('text-danger text-success text-warning').text('');
                $clearButton.hide();

                if (selectedMode === 'outside') {
                     var $jsonPayloadTextarea = $tryItOutSection.find('.json-payload');
                     var jsonDataString = $jsonPayloadTextarea.val();
                     try {
                          requestBodyPayload = jsonDataString.trim() === "" ? {} : JSON.parse(jsonDataString);
                     } catch (e) {
                         $responseStatusDiv.html('<strong>Error:</strong> Invalid JSON in Outside mode payload.').addClass('alert alert-danger');
                         $responseOutputDiv.text(e.message).addClass('text-danger');
                         $responseSection.show();
                         $clearButton.show();
                         return;
                     }
                } else if (selectedMode === 'inside') {
                    var $insideParametersTextarea = $tryItOutSection.find('.inside-parameters-json');
                    var insideParametersJsonString = $insideParametersTextarea.val();
                    var parameters = null;

                    try {
                         parameters = insideParametersJsonString.trim() === "" ? {} : JSON.parse(insideParametersJsonString);
                    } catch (e) {
                        $responseStatusDiv.html('<strong>Error:</strong> Invalid JSON in Inside Parameters.').addClass('alert alert-danger');
                        $responseOutputDiv.text(e.message).addClass('text-danger');
                        $responseSection.show();
                        $clearButton.show();
                        return;
                    }

                     requestBodyPayload = { "parameters": parameters };
                }

                if (requestBodyPayload === null) {
                     $responseStatusDiv.html('<strong>Error:</strong> Failed to prepare request payload.').addClass('alert alert-danger');
                     $responseSection.show();
                     $clearButton.show();
                     return;
                }


                $button.prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Executing...');

                const endpoint = `/pdf/generate/${templateName}`;
                const url = new URL(endpoint, window.location.origin);
                url.searchParams.append('mode', selectedMode);
                // Append the selected versionType to the URL query string
                if (selectedVersionType) {
                     url.searchParams.append('versionType', selectedVersionType);
                }


                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                        // Authorization header is added by JwtCookieMiddleware
                    },
                    body: JSON.stringify(requestBodyPayload)
                })
                .then(response => {
                    const contentType = response.headers.get('content-type');
                    if (!response.ok) {
                         if (response.status === 401 || response.status === 403) {
                              alert('Unauthorized. Please log in.');
                              window.location.href = '/Account/Login'; // Redirect to login
                              return Promise.reject('Unauthorized'); // Stop promise chain
                         }
                         return response.text().then(text => {
                             throw new Error(`HTTP error! status: ${response.status} - ${text}`);
                         });
                    }

                    if (contentType && contentType.includes('application/pdf')) {
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
                        const filenameVersionPart = selectedVersionType || 'Testing'; // Use selected type for filename
                        const suggestedFilename = `${templateName}_${filenameVersionPart}_${selectedMode}_API_Test_${new Date().toISOString().slice(0, 19).replace(/[-:T]/g, "")}.pdf`;
                        a.href = url;
                        a.download = suggestedFilename;
                        a.innerHTML = `<i class="fas fa-download me-1"></i> Download ${suggestedFilename}`;
                        a.className = 'btn btn-sm btn-success d-block mt-2';
                        $responseOutputDiv.append($('<div>').html('PDF generated successfully.'));
                        $responseOutputDiv.append(a);
                        $responseStatusDiv.addClass('alert alert-success');
                    } else {
                        $responseOutputDiv.text(result.text);
                        if(result.ok){
                            $responseStatusDiv.addClass('alert alert-warning');
                        } else {
                             $responseStatusDiv.addClass('alert alert-danger');
                        }
                    }
                })
                .catch(error => {
                     if (error !== 'Unauthorized') {
                        console.error('Fetch Error:', error);
                        $responseStatusDiv.html('<strong>Error:</strong> An API error occurred').addClass('alert alert-danger');
                        $responseOutputDiv.text(error.message).addClass('text-danger');
                     }
                })
                .finally(() => {
                    $button.prop('disabled', false).html('<i class="fas fa-play-circle"></i> Execute');
                    $responseSection.show();
                    $clearButton.show();
                });
            });

            // --- Clear Response Button ---
            $('.clear-response-btn').on('click', function() {
                var $tryItOutSection = $(this).closest('.try-it-out-section');
                $tryItOutSection.find('.response-section').hide();
                $tryItOutSection.find('.response-status').empty().removeClass('text-danger text-success text-warning alert alert-danger alert-success alert-warning');
                $tryItOutSection.find('.response-output').empty().removeClass('text-danger text-success text-warning');
                $(this).hide();
            });

             // Helper function for JSON formatting
             function formatJsonTextarea(textarea) {
                 try {
                     var rawJson = textarea.val();
                      if (rawJson && rawJson.trim() !== "{}" && rawJson.trim() !== "") {
                         var parsedJson = JSON.parse(rawJson);
                         textarea.val(JSON.stringify(parsedJson, null, 2));
                     } else {
                         textarea.val('{}');
                     }
                 } catch (e) {
                     console.warn("Existing content is not valid JSON:", textarea.attr('id'), e);
                 }
            }


            $('.json-payload').each(function() { formatJsonTextarea($(this)); });
             $('.data-config-section[data-mode="inside"] textarea').each(function() { formatJsonTextarea($(this)); });
             $('.inside-parameters-json').each(function() { formatJsonTextarea($(this)); });

             // Initialize UI visibility and defaults
             $('.try-it-out-section').each(function() {
                 var $tryItOutSection = $(this);
                 // Set default mode and version selection and trigger change event
                 $tryItOutSection.find('.mode-radio[value="outside"]').prop('checked', true).trigger('change');
                 // Ensure the correct version radio is checked and trigger change if necessary for UI logic
                 var defaultVersion = '@VersionReferenceType.Testing'; // Default to Testing
                 $tryItOutSection.find(`.version-type-radio[value="${defaultVersion}"]`).prop('checked', true);
             });
        });
    </script>
}
```

---

**Update `TemplateProcessingService.cs` and `GeneratePdfHandler.cs`:**

The `ProcessTemplate` method itself does NOT need to know about `FabricJson`. Its job is to take HTML content and JSON data. The *generation* of the final HTML that includes the Fabric.js elements will happen *before* this method is called.

The core logic to integrate Fabric.js will be within the **`GeneratePdfHandler.cs`** and potentially the **`TemplateController.cs`** (for the "Download Test PDF" button on the Design page), and the **`TemplateProcessingService.cs`** itself will need a new method to parse `FabricJson` and produce the HTML structure.

Let's focus on the `GeneratePdfHandler` and `TemplateProcessingService` first.

---

**14. `PDFGenerator.Infrastructure\Services\TemplateProcessingService.cs`**
(Adding a method to process Fabric.js JSON into HTML)

```csharp
// ... (existing usings and class declaration) ...

        // Regex to extract placeholder names from Fabric.js JSON text objects.
        // Fabric.js uses properties like `text` and we'll assume it's structured to indicate a placeholder.
        // A common convention might be to prefix text elements that are placeholders.
        // For simplicity, let's assume a property like 'isPlaceholder' or a specific naming convention.
        // If Fabric.js text elements contain the placeholder syntax directly, we can adapt.
        // Example: If text is "Hello <<Name>>", we need to extract "<<Name>>".
        // For now, let's assume a simple structure where text *is* the placeholder or contains it.
        // If Fabric.js stores placeholder info separately, that's better.
        // Let's consider a scenario where a text object has a 'placeholderName' property.

        // A better approach might be to look for placeholders within the *text* property of Fabric.js objects
        // OR to have a dedicated property like 'placeholderName' on the Fabric.js object itself.
        // Let's assume for now, a text object's `text` property might contain the placeholder,
        // or we might need to query for a custom `placeholderName` property if Fabric.js schema supports it.

        // Regex to extract <<FieldName>> from string.
        // This is used in ProcessTemplate and GenerateExampleJson, need to ensure consistency.
        private static readonly Regex StandardPlaceholderRegex = new Regex(@"<<(\w+)>>", RegexOptions.Compiled);
        // And its HTML entity version used by Summernote/Fabric.js output.
        private static readonly Regex SummernotePlaceholderRegex = new Regex(@"&lt;&lt;(\w+)&gt;&gt;", RegexOptions.Compiled);


        // ... (Existing ProcessTemplate, ResolveParameters, GenerateExampleJson, IsValidJson methods) ...

        // NEW METHOD: Process Fabric.js JSON to generate HTML for images and overlaid text placeholders.
        // This method will be called by GeneratePdfHandler.
        public string ProcessFabricJson(string? fabricJson, JsonElement jsonData, string templateHtmlFallback)
        {
            // If Fabric.js JSON is null or empty, fall back to standard HTML processing.
            if (string.IsNullOrWhiteSpace(fabricJson))
            {
                // We still need to process the standard HTML with provided jsonData.
                // This falls back to the standard ProcessTemplate if no FabricJson is present.
                // However, if FabricJson *is* present but empty/invalid, what should happen?
                // For now, if fabricJson is null/empty, we assume the template might only use its basic HtmlContent.
                // The overall flow should handle this: if FabricJson exists, use it; otherwise, use HtmlContent.
                // Let's assume this method is called ONLY IF fabricJson is present.
                // If called directly with null, it means fabricJson is not part of the template definition.
                // The handler will need to decide the primary HTML source.

                // For now, assume this method is called when fabricJson is available.
                // If fabricJson is null/empty, it means no visual layout defined by Fabric.js, so just return fallback or empty.
                // A better place to handle this logic might be in the Handler itself.
                // This method assumes fabricJson *is* present and valid for a template using this feature.
                return ""; // Or throw an error, or return the templateHtmlFallback.
            }

            string finalHtml = ""; // To build the output HTML.

            try
            {
                using JsonDocument fabricDoc = JsonDocument.Parse(fabricJson);
                JsonElement fabricRoot = fabricDoc.RootElement;

                if (fabricRoot.ValueKind != JsonValueKind.Object)
                {
                    Console.WriteLine("Warning: Fabric.js JSON is not a valid object.");
                    return templateHtmlFallback; // Fallback if Fabric JSON is malformed.
                }

                // Start building the HTML output. We'll create a container for the Fabric.js layout.
                // The structure will typically involve:
                // <div class="fabric-container" style="position: relative; width: ...; height: ...;">
                //   <img src="..." style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"/>
                //   <div class="placeholder-text-element" style="position: absolute; left: ...; top: ...; font-size: ...; color: ...; transform: rotate(...deg);">
                //     Processed<<FieldName>>Value
                //   </div>
                //   ... more divs for text placeholders ...
                // </div>

                // Assuming Fabric.js JSON structure: { "version": "5.0.0", "objects": [ { "type": "image", "url": "data:...", "left": ..., "top": ...}, { "type": "textbox", "text": "<<FieldName>>", "left": ..., "top": ..., "fontFamily": "...", "fontSize": ..., "fill": "...", "angle": ... } ] }

                string? imageUrl = null;
                List<FabricTextObject> textPlaceholders = new List<FabricTextObject>();

                // Iterate through Fabric.js objects to find images and text placeholders.
                if (fabricRoot.TryGetProperty("objects", out JsonElement objectsElement) && objectsElement.ValueKind == JsonValueKind.Array)
                {
                    foreach (JsonElement obj in objectsElement.EnumerateArray())
                    {
                        if (obj.TryGetProperty("type", out JsonElement typeElement))
                        {
                            string objType = typeElement.GetString() ?? "";

                            if (objType == "image")
                            {
                                // We'll only use the first image as the base background for simplicity.
                                // More complex layouts could handle multiple images or layering.
                                if (imageUrl == null && obj.TryGetProperty("url", out JsonElement urlElement))
                                {
                                    imageUrl = urlElement.GetString();
                                }
                            }
                            else if (objType == "textbox" || objType == "text") // Handle common text object types
                            {
                                if (obj.TryGetProperty("text", out JsonElement textElement) && !string.IsNullOrEmpty(textElement.GetString()))
                                {
                                    string textValue = textElement.GetString()!;
                                    string placeholderName = "";
                                    string plainText = textValue; // Text to display if it's not a placeholder

                                    // Try to extract placeholder name from the text.
                                    // Use the standard placeholder regex here.
                                    var match = StandardPlaceholderRegex.Match(textValue);
                                    if (match.Success && match.Groups.Count > 1)
                                    {
                                        placeholderName = match.Groups[1].Value;
                                        // The text to be displayed will be determined by processing this placeholder later.
                                        // For now, we store the placeholder name and the styling properties.
                                        plainText = ""; // Reset plain text if it's a placeholder.
                                    }

                                    // Extract styling properties. Need to ensure these exist and are in expected formats.
                                    // Default values are important if properties are missing.
                                    double left = obj.TryGetProperty("left", out JsonElement leftElem) ? leftElem.GetDouble() : 0;
                                    double top = obj.TryGetProperty("top", out JsonElement topElem) ? topElem.GetDouble() : 0;
                                    string fontFamily = obj.TryGetProperty("fontFamily", out JsonElement fontFamilyElem) ? fontFamilyElem.GetString() ?? "Arial" : "Arial";
                                    double fontSize = obj.TryGetProperty("fontSize", out JsonElement fontSizeElem) ? fontSizeElem.GetDouble() : 16;
                                    string fill = obj.TryGetProperty("fill", out JsonElement fillElem) ? fillElem.GetString() ?? "#000000" : "#000000"; // Color as hex string.
                                    double angle = obj.TryGetProperty("angle", out JsonElement angleElem) ? angleElem.GetDouble() : 0;

                                    textPlaceholders.Add(new FabricTextObject
                                    {
                                        PlaceholderName = placeholderName, // Will be empty if not a placeholder.
                                        OriginalText = textValue, // Store the original text for non-placeholders.
                                        Left = left,
                                        Top = top,
                                        FontFamily = fontFamily,
                                        FontSize = fontSize,
                                        Fill = fill,
                                        Angle = angle
                                    });
                                }
                            }
                        }
                    }
                }

                // Start building the final HTML structure.
                // The main container will hold the image and absolutely positioned text elements.
                finalHtml += "<div class='fabric-layout-container' style='position: relative;'>";

                // Embed the base image.
                if (!string.IsNullOrEmpty(imageUrl))
                {
                    // The imageUrl is expected to be a data URL.
                    // Apply styles to make it cover the container.
                    finalHtml += $"<img src='{imageUrl}' style='position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover;' />";
                }
                else
                {
                    // If no image, maybe render the fallback HTML directly or log a warning.
                    Console.WriteLine("Warning: No base image found in Fabric.js JSON for template.");
                    // If we want to render standard HTML without images, that needs separate logic.
                    // For now, let's assume if fabricJson is used, an image is expected.
                    // If templateHtmlFallback is meant to be the base if no image, it should be placed here.
                    // For this method's purpose, we'll assume image is primary and text overlays it.
                }

                // Add divs for text placeholders, processed with actual data.
                // This part needs access to the actual data (jsonData) to replace placeholders.
                // This suggests ProcessTemplate might need to be called *within* ProcessFabricJson,
                // or ProcessFabricJson should receive the processed HTML or be integrated.

                // Let's adjust: ProcessFabricJson will generate the structure, and actual replacement happens in ProcessTemplate.
                // So, here we generate placeholders and their styles.
                // The actual replacement logic will be in ProcessTemplate by searching for specific patterns within the generated text elements.

                // Structure for each text element:
                // <div class='fabric-text-overlay' style='position: absolute; left: ...px; top: ...px; transform: rotate(...deg); width: fit-content; white-space: nowrap; /* prevent wrapping */'>
                //   <span style='font-family: ...; font-size: ...px; color: ...;'>
                //     {{ProcessedPlaceholderValue}} <-- THIS IS WHERE REPLACEMENT HAPPENS
                //   </span>
                // </div>

                // We can't do the actual <<FieldName>> replacement here without the jsonData.
                // The ProcessTemplate method will need to be enhanced to look for these specific DIVs
                // and perform the placeholder replacement within them.

                // For now, let's generate the structure with placeholders and their styling.
                // We'll need to ensure these generated DIVs are injected into the HTML structure processed by ProcessTemplate.

                // A more robust approach: Generate the Fabric.js JSON *into* the HTML as part of the template processing.
                // Or, use a template engine that can handle this structure.
                // For now, let's generate HTML fragments.

                // The issue: ProcessTemplate typically processes static HTML provided.
                // Fabric.js JSON is NOT static HTML.
                // The strategy is to *transform* Fabric.js JSON into static HTML.

                // Let's refine: ProcessTemplate should generate the base HTML and THEN inject the processed Fabric.js elements.
                // The Fabric.js JSON processing should yield a LIST of HTML fragments (divs) for each text element.
                // The ProcessTemplate method will then need to parse these fragments and perform placeholder replacements.

                // This is getting complex. Let's re-evaluate the hybrid approach:
                // 1. Store Fabric.js JSON in Template/TemplateVersion.
                // 2. ProcessTemplate receives HtmlContent AND FabricJson.
                // 3. It parses FabricJson.
                // 4. It constructs a primary HTML structure that includes:
                //    a. The base image(s) from FabricJson.
                //    b. For each text object in FabricJson that IS a placeholder:
                //       - It generates a placeholder *marker* in the HTML, e.g., `<span data-fabric-placeholder="FieldName" data-fabric-style="..."></span>`
                // 5. AFTER the standard placeholder replacement (<<FieldName>> -> DataValue), ProcessTemplate would then iterate through the generated HTML,
                //    find these `data-fabric-placeholder` spans, and replace them with the styled divs containing the actual data.

                // Let's try a simpler version first: generate the HTML directly.
                // This method's responsibility is to RETURN the HTML fragment that PROCESS_TEMPLATE will work with.
                // ProcessTemplate will be responsible for BOTH standard HTML processing AND placeholder replacement within the Fabric.js generated text.

                // Re-think: ProcessTemplate takes `htmlContent` and `jsonData`.
                // If `FabricJson` is present, it should be the primary source of HTML.
                // `htmlContent` might be a fallback if FabricJson is missing or invalid.

                // Let's assume ProcessTemplate gets `templateDataAccessDto.FabricJson` and `templateDataAccessDto.HtmlContent`
                // as inputs.

                // New signature for ProcessTemplate (if we embed this logic there):
                // public string ProcessTemplate(string? fabricJson, string fallbackHtmlContent, JsonElement jsonData)

                // For now, let's assume this `ProcessFabricJson` returns HTML *fragments* for the fabric elements,
                // and the main `ProcessTemplate` will orchestrate their placement.

                // Simplified strategy for THIS method:
                // Generate HTML for the image and placeholder divs.
                // The *replacement* of <<FieldName>> will happen in ProcessTemplate.
                // So, we'll create static HTML with placeholder *markers* for the text.

                foreach (var textObj in textPlaceholders)
                {
                    // Construct style string from Fabric.js properties.
                    // Important: Fabric.js values like fontSize might need units (px). Colors are often hex.
                    // Angles need rotation transform.
                    string style = $"position: absolute; left: {textObj.Left}px; top: {textObj.Top}px; ";
                    if (textObj.Angle != 0) {
                        // Fabric.js rotation is usually around the center. For simple overlays,
                        // rotating around the top-left might be acceptable, or we need to calculate offsets.
                        // For simplicity, let's assume simple rotation.
                        style += $"transform: rotate({textObj.Angle}deg); transform-origin: 0 0; ";
                    }
                    style += $"font-family: '{textObj.FontFamily}', sans-serif; "; // Fallback font.
                    style += $"font-size: {textObj.FontSize}px; ";
                    style += $"color: {textObj.Fill}; ";
                    style += "white-space: nowrap; /* Prevent text from wrapping */ ";
                    style += "pointer-events: none; /* Allow clicks to pass through if needed, or set to auto */ ";
                    style += "overflow: hidden; /* Clip text if it exceeds bounds */ ";


                    // If it's a placeholder, wrap it in a placeholder marker for ProcessTemplate.
                    // The marker needs to contain the original placeholder name and the styling.
                    // ProcessTemplate will then find this marker, look up data for placeholderName,
                    // and replace the marker's content with the styled data.
                    // Let's use a custom attribute for the placeholder name and embed styles.
                    if (!string.IsNullOrEmpty(textObj.PlaceholderName))
                    {
                        // The actual replacement <<FieldName>> -> Data will happen inside ProcessTemplate later.
                        // So, for now, we render the placeholder name itself, wrapped in a span that ProcessTemplate can target.
                        // Example: <span class='fabric-placeholder-text' data-placeholder-name='Name' style='...' ><<Name>></span>
                        finalHtml += $"<div class='fabric-text-overlay' style='{style}'><span><<{textObj.PlaceholderName}>></span></div>";
                    }
                    else
                    {
                        // If it's not a placeholder, display the original text (could also be processed).
                        // For simplicity, we'll just display the original text directly for now.
                        finalHtml += $"<div class='fabric-text-static' style='{style}'>{System.Net.WebUtility.HtmlEncode(textObj.OriginalText)}</div>";
                    }
                }

                finalHtml += "</div>"; // Close fabric-layout-container.

                // This generated HTML fragment will be *inserted* into the main HTML processed by ProcessTemplate.
                // The ProcessTemplate method will need to be updated to use this fragment appropriately.
                // It might replace the fallback HTML entirely or merge it.
                // For now, this method returns the Fabric-generated part.

                return finalHtml; // Return the generated HTML for fabric elements.
            }
            catch (JsonException jEx)
            {
                Console.WriteLine($"Error parsing Fabric.js JSON: {jEx.Message}");
                return templateHtmlFallback; // Fallback if Fabric JSON is invalid.
            }
            catch (Exception ex)
            {
                Console.WriteLine($"An unexpected error occurred processing Fabric.js JSON: {ex.Message}");
                return templateHtmlFallback; // Fallback for other errors.
            }
        }

        // Helper class to hold parsed text object properties from Fabric.js JSON.
        private class FabricTextObject
        {
            public string PlaceholderName { get; set; } = ""; // The <<FieldName>> if it's a placeholder.
            public string OriginalText { get; set; } = ""; // The original text value.
            public double Left { get; set; }
            public double Top { get; set; }
            public string FontFamily { get; set; } = "Arial";
            public double FontSize { get; set; } = 16;
            public string Fill { get; set; } = "#000000"; // Hex color string.
            public double Angle { get; set; } = 0; // Rotation in degrees.
        }

        // --- Modified ProcessTemplate to handle Fabric.js HTML ---
        // This is the crucial part. ProcessTemplate needs to be aware of the Fabric JSON.
        // It should ideally combine the static HTML content with the Fabric-generated HTML.
        // Let's assume ProcessTemplate receives FabricJson separately or it's part of the template DTO.

        // New signature proposal for ProcessTemplate that integrates Fabric.js handling.
        // It would take template's base HTML, the Fabric JSON, and the actual data.
        public string ProcessTemplateWithFabric(string? baseHtmlContent, string? fabricJson, JsonElement jsonData)
        {
            // If Fabric JSON is present, it takes precedence for structure.
            if (!string.IsNullOrWhiteSpace(fabricJson))
            {
                try
                {
                    // Generate the core HTML structure from Fabric JSON (images and styled placeholder spans).
                    string fabricGeneratedHtml = ProcessFabricJson(fabricJson, baseHtmlContent ?? "", jsonData); // Pass baseHtmlContent as fallback if no image.

                    // Now, we have fabricGeneratedHtml containing static image(s) and placeholder spans like:
                    // <div class='fabric-text-overlay' style='...'><span><<FieldName>></span></div>
                    // We need to process these placeholder spans for their actual data.

                    // This is the complex part: we need to perform data replacement *within* these generated spans.
                    // The standard ProcessTemplate method needs to be aware of these special span elements.
                    // One way: Let ProcessTemplate parse the fabricGeneratedHtml, find these spans,
                    // extract placeholder name, get data, and replace the span's content.

                    // For this example, let's integrate the logic here:
                    // 1. Replace <<FieldName>> within fabricGeneratedHtml.
                    // 2. Merge this with any other parts of baseHtmlContent if needed.
                    //    However, the hybrid model suggests fabricJson *defines* the layout, and baseHtmlContent is a fallback.
                    //    So, let's assume fabricJson defines the layout and potentially uses baseHtmlContent for non-Fabric elements if any.

                    // For now, assume fabricGeneratedHtml REPLACES baseHtmlContent entirely for the core layout.

                    // Perform the actual data replacement for <<FieldName>> placeholders within the generated fabric elements.
                    // This requires a function that takes HTML string, data, and knows how to find and replace within specific elements.
                    // This is getting deep into DOM manipulation or complex regex.

                    // --- Simplified approach for this example ---
                    // Let's assume ProcessTemplate is called AFTER ProcessFabricJson has been used to *prepare* the HTML.
                    // Or, ProcessTemplate itself handles both.

                    // Let's modify ProcessTemplate to handle this:
                    // It will receive the templateData (which includes HtmlContent AND FabricJson)
                    // The logic will be: if FabricJson is present, parse it, generate HTML structure, then do placeholder replacement on generated HTML.

                    // Re-architecting ProcessTemplate to be aware of FabricJson.
                    // The handler (GeneratePdfHandler) will fetch templateDto.FabricJson.
                    // The ProcessTemplate method itself needs to receive it or access it.

                    // Let's assume ProcessTemplate signature is updated to:
                    // public string ProcessTemplate(string? htmlContent, string? fabricJson, JsonElement jsonData)

                    // --- Inside the (new) ProcessTemplateWithFabric ---

                    string processedHtmlWithFabric = ""; // This would be the final result.

                    // 1. Get base image(s) and text element definitions from fabricJson.
                    // 2. Construct HTML for these, potentially replacing <<FieldName>> placeholders within the text elements with actual data values.
                    // 3. Combine this with any other parts of the template.

                    // This requires a more sophisticated HTML builder that can parse the FabricJson structure.
                    // The current placeholder replacement logic is string-based.
                    // To overlay text correctly, the `ProcessTemplate` would need to:
                    //    - Embed the base image (likely as `<img>` with `position: relative;` or `background-image`).
                    //    - For each text element with a placeholder:
                    //        - Look up the placeholder name in `jsonData`.
                    //        - Get the data value.
                    //        - Generate a `<span>` or `<div>` for this data value.
                    //        - Apply inline styles to this span/div based on Fabric.js properties (position, font, color, rotation).
                    //        - `position: absolute;` will be key for overlaying.

                    // Let's revise the strategy: ProcessTemplate receives `HtmlContent`, `FabricJson`, and `jsonData`.
                    // If FabricJson exists, it's prioritized. It defines the layout.
                    // It will extract image(s) and text objects.
                    // For each text object:
                    //   If it's a placeholder, get the value from `jsonData` for that placeholder.
                    //   If not a placeholder, use the literal text from Fabric.js.
                    //   Construct a styled `<span>` or `<div>` for this text/data.
                    //   Return the complete HTML string with image and styled text elements.

                    // This implies a significant rewrite of ProcessTemplate.
                    // For now, this method might just return the FabricJson itself or a basic representation.
                    // Or, it might return a specific HTML structure that ProcessTemplate is aware of.

                    // Let's go with the approach where ProcessTemplate will take FabricJson as an input.
                    // The GeneratePdfHandler will call ProcessTemplate, passing the fetched FabricJson.

                    // This `ProcessFabricJson` method's role is to convert FabricJson into HTML fragments.
                    // It needs to know how to iterate Fabric.js objects and generate HTML.
                    // This would typically require a JSON parsing and string building logic.
                    // The actual replacement of <<FieldName>> needs to happen on the text content of these generated elements.

                    // Let's assume `ProcessTemplate` is modified to handle a structure generated by Fabric.js.
                    // This method might be removed if `ProcessTemplate` becomes responsible for parsing `FabricJson`.

                    // For now, returning the fallback content to indicate this method isn't fully integrated yet.
                    return templateHtmlFallback;
                }
            }
            catch (JsonException jEx)
            {
                Console.WriteLine($"Error parsing Fabric.js JSON: {jEx.Message}");
                return templateHtmlFallback;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"An unexpected error occurred processing Fabric.js JSON: {ex.Message}");
                return templateHtmlFallback;
            }
        }
        // End of ProcessFabricJson

        // --- MODIFIED ProcessTemplate Method ---
        // This is the central change. ProcessTemplate will now handle Fabric.js JSON.
        // It needs access to the FabricJson string. The handler will pass it.
        // public string ProcessTemplate(string? htmlContent, string? fabricJson, JsonElement jsonData)
        // The current signature is: public string ProcessTemplate(string htmlContent, JsonElement jsonData)
        // We need to update the signature of ProcessTemplate in TemplateProcessingService.

        // The GeneratePdfHandler needs to pass templateDataAccessDto.FabricJson to the processing service.

        // Assuming ProcessTemplate signature change is done elsewhere.
        // For THIS file, let's just ensure all necessary methods are available.
        // The logic for handling FabricJson will reside WITHIN ProcessTemplate itself.

        // The rest of the methods are fine for now, but the *calling* code needs to be aware of FabricJson.
        // ... (rest of the methods) ...
    }
}
```

---

**15. `PDFGenerator.Web\Services\GeneratePdfHandler.cs`**
(Modified to pass FabricJson to `ProcessTemplate` and integrate its logic)

This is where the major change happens. The `GeneratePdfHandler` needs to be updated to:
1.  Fetch `FabricJson` from the `TemplateDataAccessDto`.
2.  Pass `FabricJson` to `TemplateProcessingService.ProcessTemplate`.
3.  The `TemplateProcessingService.ProcessTemplate` method itself needs to be modified to understand and process the `FabricJson`.

Let's assume `TemplateProcessingService.ProcessTemplate` is modified to accept `string? fabricJson` and use it as the primary source of HTML structure.

**Assumption: `TemplateProcessingService.ProcessTemplate` Signature Change**

Let's assume the `TemplateProcessingService.ProcessTemplate` signature is changed to:
`public string ProcessTemplate(string? htmlContent, string? fabricJson, JsonElement jsonData)`

If this is the case, the `GeneratePdfHandler` will look like this:

```csharp
// File: Handlers/GeneratePdfHandler.cs
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Services; // For TemplateProcessingService
using System.Text.Json;
using WkHtmlToPdfDotNet;
using WkHtmlToPdfDotNet.Contracts;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using System.Threading.Tasks;

namespace PdfGeneratorApp.Handlers
{
    // Interface updated to include versionReferenceType in the request tuple.
    public interface IGeneratePdfHandler : IHandler<(string templateName, JsonElement requestBodyJson, string mode, string? versionReferenceType), byte[]>
    {
    }

    public class GeneratePdfHandler : IGeneratePdfHandler
    {
        private readonly IUnitOfWork _unitOfWork;
        private readonly IConverter _converter;
        private readonly TemplateProcessingService _templateProcessingService;

        public GeneratePdfHandler(IUnitOfWork unitOfWork, IConverter converter, TemplateProcessingService templateProcessingService)
        {
            _unitOfWork = unitOfWork;
            _converter = converter;
            _templateProcessingService = templateProcessingService;
        }

        public async Task<Result<byte[]>> HandleAsync((string templateName, JsonElement requestBodyJson, string mode, string? versionReferenceType) request)
        {
            try
            {
                string effectiveVersionType = VersionReferenceType.Testing;
                if (!string.IsNullOrWhiteSpace(request.versionReferenceType) && VersionReferenceType.IsValid(request.versionReferenceType))
                {
                    effectiveVersionType = request.versionReferenceType;
                }
                else if (!string.IsNullOrWhiteSpace(request.versionReferenceType))
                {
                    Console.WriteLine($"Warning: Invalid versionReferenceType '{request.versionReferenceType}' provided. Defaulting to Testing.");
                }

                // Fetch template data, now including FabricJson.
                var repoResult = await _unitOfWork.Templates.GetTemplateContentByVersionReferenceAsync(request.templateName, effectiveVersionType);

                if (!repoResult.IsCompleteSuccessfully || repoResult.Data == null)
                {
                    return Result<byte[]>.Failure(repoResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                var templateDataAccessDto = repoResult.Data; // This DTO now contains HtmlContent, FabricJson, etc.

                JsonElement finalDataForHtmlProcessing;
                JsonElement insideParameters = default;

                // Determine data source based on 'mode'.
                switch (request.mode.ToLowerInvariant())
                {
                    case "outside":
                        finalDataForHtmlProcessing = request.requestBodyJson;
                        break;

                    case "inside":
                        if (request.requestBodyJson.ValueKind != JsonValueKind.Object)
                        {
                            return Result<byte[]>.Failure(ErrorMessageUserConst.InsideModeBodyNotObject);
                        }
                        if (request.requestBodyJson.TryGetProperty("parameters", out JsonElement parametersElement))
                        {
                            insideParameters = parametersElement;
                        }
                        // Resolve internal data using fetched config (from target version) and parameters.
                        finalDataForHtmlProcessing = _templateProcessingService.ResolveInternalData(templateDataAccessDto.InternalDataConfigJson, insideParameters);
                        break;

                    default:
                        return Result<byte[]>.Failure(ErrorMessageUserConst.InvalidMode);
                }

                // --- MAJOR CHANGE HERE ---
                // Call ProcessTemplate, passing BOTH HtmlContent and FabricJson.
                // ProcessTemplate is now responsible for deciding whether to use FabricJson or fallback HtmlContent,
                // and importantly, processing placeholders within the Fabric-generated HTML.
                string finalHtmlContent = _templateProcessingService.ProcessTemplate(
                    templateDataAccessDto.HtmlContent,     // Fallback HTML
                    templateDataAccessDto.FabricJson,      // Fabric.js JSON definition
                    finalDataForHtmlProcessing             // Data for placeholders
                );
                // --- END MAJOR CHANGE ---

                // Configure WkHtmlToPdf document settings with the final HTML content.
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
                            HtmlContent = finalHtmlContent, // Use the HTML generated by ProcessTemplateWithFabric
                            WebSettings = { DefaultEncoding = "utf-8" }
                        }
                    }
                };

                byte[] pdf = _converter.Convert(doc);

                if (pdf == null || pdf.Length == 0)
                {
                    return Result<byte[]>.Failure(ErrorMessageUserConst.PdfGenerationFailed + " Ensure wkhtmltopdf is correctly installed and accessible.");
                }

                return Result<byte[]>.Success(pdf);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in GeneratePdfHandler: {ex.Message}");
                return Result<byte[]>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }
    }
}
```

---

**16. `PDFGenerator.Infrastructure\Services\TemplateProcessingService.cs`**
(This file requires the most significant changes to implement the hybrid approach)

**Key Modifications to `TemplateProcessingService.cs`:**

*   **Modify `ProcessTemplate` Signature:** Change `public string ProcessTemplate(string htmlContent, JsonElement jsonData)` to `public string ProcessTemplate(string? fallbackHtmlContent, string? fabricJson, JsonElement jsonData)`.
*   **Implement Fabric JSON Parsing in `ProcessTemplate`:** The `ProcessTemplate` method will now first check `fabricJson`.
    *   If `fabricJson` is present, parse it and generate HTML for images and styled text elements (including placeholder markers).
    *   If `fabricJson` is null or invalid, fall back to processing the `fallbackHtmlContent`.
    *   Crucially, the *placeholder replacement* logic needs to be integrated to work on the HTML generated from `fabricJson` as well.

Let's provide the modified `TemplateProcessingService.cs` file.

```csharp
using Microsoft.Data.SqlClient;
using Microsoft.Extensions.Configuration;
using PdfGeneratorApp.Common;
using System.Text.Json;
using System.Text.RegularExpressions;
using System; // For Exception, DateTime, RegexOptions, Regex
using System.Collections.Generic; // For List, Dictionary
using System.Net; // For WebUtility

namespace PdfGeneratorApp.Services
{
    public class TemplateProcessingService
    {
        private readonly IConfiguration _configuration;

        // Regex for finding standard <<FieldName>> placeholders.
        private static readonly Regex StandardPlaceholderRegex = new Regex(@"<<(\w+)>>", RegexOptions.Compiled);
        // Regex for HTML entities of placeholders as output by Summernote/Fabric.js
        private static readonly Regex SummernotePlaceholderRegex = new Regex(@"&lt;&lt;(\w+)&gt;&gt;", RegexOptions.Compiled);

        // Regex for conditional expressions ${{condition ? true_part : false_part}}
        private static readonly Regex ConditionalRegex = new Regex(@"\$\{\{\s*(.+?)\s*\?\s*(.+?)\s*:\s*(.+?)\s*\}\}", RegexOptions.Compiled | RegexOptions.Singleline);

        // Regex for finding "inside parameter" placeholders <<param:parameterName>>
        private static readonly Regex ParameterPlaceholderRegex = new Regex(@"<<param:(\w+)>>", RegexOptions.Compiled);

        public TemplateProcessingService(IConfiguration configuration)
        {
            _configuration = configuration;
        }

        // --- MODIFIED METHOD ---
        // ProcessTemplate now handles both standard HTMLContent and Fabric.js JSON.
        // It prioritizes FabricJson for layout and generates HTML structure accordingly.
        // Placeholders within Fabric.js text elements are also processed.
        public string ProcessTemplate(string? fallbackHtmlContent, string? fabricJson, JsonElement jsonData)
        {
            // If FabricJson is provided and valid, it defines the primary layout.
            if (!string.IsNullOrWhiteSpace(fabricJson))
            {
                try
                {
                    // Parse the Fabric.js JSON.
                    using JsonDocument fabricDoc = JsonDocument.Parse(fabricJson);
                    JsonElement fabricRoot = fabricDoc.RootElement;

                    if (fabricRoot.ValueKind != JsonValueKind.Object)
                    {
                        Console.WriteLine("Warning: Fabric.js JSON is not a valid object. Falling back to fallbackHtmlContent.");
                        return ProcessStandardHtml(fallbackHtmlContent ?? "", jsonData); // Fallback
                    }

                    string generatedFabricHtml = BuildHtmlFromFabricJson(fabricRoot, jsonData);

                    // If FabricJson was successfully processed, use it as the final HTML.
                    if (!string.IsNullOrEmpty(generatedFabricHtml))
                    {
                        return generatedFabricHtml;
                    }
                    else
                    {
                        // If FabricJson was valid but generated no content, fallback.
                        Console.WriteLine("Warning: Fabric.js JSON processed but resulted in empty HTML. Falling back to fallbackHtmlContent.");
                        return ProcessStandardHtml(fallbackHtmlContent ?? "", jsonData);
                    }
                }
                catch (JsonException jEx)
                {
                    Console.WriteLine($"Error parsing Fabric.js JSON: {jEx.Message}. Falling back to fallbackHtmlContent.");
                    return ProcessStandardHtml(fallbackHtmlContent ?? "", jsonData); // Fallback on JSON error
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"An unexpected error occurred processing Fabric.js JSON: {ex.Message}. Falling back to fallbackHtmlContent.");
                    return ProcessStandardHtml(fallbackHtmlContent ?? "", jsonData); // Fallback for other errors
                }
            }
            else
            {
                // If FabricJson is null or empty, just process the standard fallback HTML.
                return ProcessStandardHtml(fallbackHtmlContent ?? "", jsonData);
            }
        }

        // Helper to process standard HTML content (placeholders and conditionals).
        private string ProcessStandardHtml(string htmlContent, JsonElement jsonData)
        {
            // This method contains the original placeholder and conditional processing logic.
            string processedHtml = htmlContent;

            // 1. Process Conditional Expressions (${{...}}) FIRST
            processedHtml = ConditionalRegex.Replace(processedHtml, match =>
            {
                if (match.Groups.Count != 4) return match.Value;
                string conditionPart = match.Groups[1].Value.Trim();
                string truePart = match.Groups[2].Value;
                string falsePart = match.Groups[3].Value;

                bool conditionResult = false;
                bool conditionEvaluated = false;

                if (bool.TryParse(conditionPart, out bool literalBool))
                {
                    conditionResult = literalBool;
                    conditionEvaluated = true;
                }
                else
                {
                    var conditionPlaceholderMatch = SummernotePlaceholderRegex.Match(conditionPart); // Use Summernote regex for condition part
                    if (conditionPlaceholderMatch.Success && conditionPlaceholderMatch.Groups.Count > 1)
                    {
                        string fieldName = conditionPlaceholderMatch.Groups[1].Value;
                        if (jsonData.ValueKind == JsonValueKind.Object && jsonData.TryGetProperty(fieldName, out JsonElement conditionValueElement))
                        {
                            if (conditionValueElement.ValueKind == JsonValueKind.True) { conditionResult = true; conditionEvaluated = true; }
                            else if (conditionValueElement.ValueKind == JsonValueKind.False) { conditionResult = false; conditionEvaluated = true; }
                            else if (conditionValueElement.ValueKind == JsonValueKind.String)
                            {
                                if (bool.TryParse(conditionValueElement.GetString(), out bool parsedStringBool))
                                {
                                    conditionResult = parsedStringBool;
                                    conditionEvaluated = true;
                                }
                            }
                            if (!conditionEvaluated) { conditionResult = false; conditionEvaluated = true; }
                        }
                        else { conditionResult = false; conditionEvaluated = true; }
                    }
                    if (!conditionEvaluated) { conditionResult = false; /* Evaluated as false if unrecognized */ }
                }
                return conditionResult ? truePart : falsePart;
            });

            // 2. Process Simple Placeholders (<<FieldName>>) AFTER conditionals.
            // Replace placeholders in the processed HTML string.
            // This regex needs to find the placeholder markers we'll inject from Fabric.js JSON.
            // We will use the SummernotePlaceholderRegex to find <<FieldName>> within the generated HTML structure.
            processedHtml = SummernotePlaceholderRegex.Replace(processedHtml, match =>
            {
                if (match.Groups.Count > 1 && match.Groups[1].Success)
                {
                    string fieldName = match.Groups[1].Value;
                    string replacementValue = "";

                    if (jsonData.ValueKind == JsonValueKind.Object && jsonData.TryGetProperty(fieldName, out JsonElement valueElement))
                    {
                        replacementValue = valueElement.ValueKind switch
                        {
                            JsonValueKind.String => valueElement.GetString() ?? "",
                            JsonValueKind.Number => valueElement.GetRawText(),
                            JsonValueKind.True => "true",
                            JsonValueKind.False => "false",
                            JsonValueKind.Null => "",
                            JsonValueKind.Object or JsonValueKind.Array => valueElement.GetRawText(),
                            _ => ""
                        };
                        replacementValue = WebUtility.HtmlEncode(replacementValue);
                    }
                    return replacementValue;
                }
                return match.Value; // Return original match if something goes wrong.
            });

            // Remove any residual placeholder syntax that wasn't replaced.
            // This regex must match both standard <<FieldName>> and HTML entity versions.
            // Simpler to use the more specific summernote regex if that's what we inject.
            processedHtml = Regex.Replace(processedHtml, @"<<.*?>>", "", RegexOptions.Singleline); // Clean up leftover <<...>>

            return processedHtml;
        }

        // Helper to build HTML structure from Fabric.js JSON.
        // This method will generate the base HTML with images and styled divs for text placeholders.
        private string BuildHtmlFromFabricJson(JsonElement fabricRoot, JsonElement jsonData)
        {
            string htmlOutput = "";
            string? imageUrl = null;
            List<FabricTextObject> textElements = new List<FabricTextObject>();

            // Parse Fabric.js objects
            if (fabricRoot.TryGetProperty("objects", out JsonElement objectsElement) && objectsElement.ValueKind == JsonValueKind.Array)
            {
                foreach (JsonElement obj in objectsElement.EnumerateArray())
                {
                    if (obj.TryGetProperty("type", out JsonElement typeElement))
                    {
                        string objType = typeElement.GetString() ?? "";

                        if (objType == "image")
                        {
                            if (imageUrl == null && obj.TryGetProperty("url", out JsonElement urlElement))
                            {
                                imageUrl = urlElement.GetString(); // Take the first image as background
                            }
                        }
                        else if (objType == "textbox" || objType == "text")
                        {
                            if (obj.TryGetProperty("text", out JsonElement textElement) && !string.IsNullOrEmpty(textElement.GetString()))
                            {
                                string textValue = textElement.GetString()!;
                                string placeholderName = "";
                                string plainText = textValue; // Default to literal text

                                // Check if this text object is a placeholder.
                                // Assumes placeholders are in the format "<<FieldName>>" within the text property itself,
                                // or that Fabric.js stores this info in a custom property (e.g., 'placeholderName').
                                // For this implementation, we'll check if the text *is* or *contains* a placeholder.
                                // A more robust solution would use a dedicated 'placeholderName' property from Fabric.js.

                                // For simplicity, let's assume if text starts with << and ends with >>, it's a placeholder.
                                // Or better, check for <<FieldName>> anywhere in the text.
                                var match = StandardPlaceholderRegex.Match(textValue);
                                if (match.Success && match.Groups.Count > 1)
                                {
                                    placeholderName = match.Groups[1].Value;
                                    plainText = ""; // Indicate this is a placeholder, data will be injected later.
                                }

                                double left = obj.TryGetProperty("left", out JsonElement leftElem) ? leftElem.GetDouble() : 0;
                                double top = obj.TryGetProperty("top", out JsonElement topElem) ? topElem.GetDouble() : 0;
                                string fontFamily = obj.TryGetProperty("fontFamily", out JsonElement fontFamilyElem) ? fontFamilyElem.GetString() ?? "Arial" : "Arial";
                                double fontSize = obj.TryGetProperty("fontSize", out JsonElement fontSizeElem) ? fontSizeElem.GetDouble() : 16;
                                string fill = obj.TryGetProperty("fill", out JsonElement fillElem) ? fillElem.GetString() ?? "#000000" : "#000000";
                                double angle = obj.TryGetProperty("angle", out JsonElement angleElem) ? angleElem.GetDouble() : 0;

                                textElements.Add(new FabricTextObject
                                {
                                    PlaceholderName = placeholderName,
                                    OriginalText = textValue, // Store original for non-placeholders or if fallback needed
                                    Left = left,
                                    Top = top,
                                    FontFamily = fontFamily,
                                    FontSize = fontSize,
                                    Fill = fill,
                                    Angle = angle
                                });
                            }
                        }
                    }
                }
            }

            // Start building the final HTML structure for the Fabric.js layout.
            // The container will manage the overall layout.
            // We'll use inline styles for positioning and formatting.
            htmlOutput += "<div class='fabric-layout-container' style='position: relative; width: 100%; height: auto; overflow: hidden;'>"; // Ensure container has relative positioning.

            // Embed the base image as an <img> tag.
            if (!string.IsNullOrEmpty(imageUrl))
            {
                // Apply styles to make the image cover the container.
                // If the image is a data URL, it's directly embeddable.
                // The `object-fit: cover;` property helps maintain aspect ratio.
                htmlOutput += $"<img src='{imageUrl}' alt='Template Background Image' style='position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover;' />";
            }
            else
            {
                // If no image is defined in Fabric.js JSON, we might fall back to using
                // the provided fallbackHtmlContent as the base structure, or just render text overlays.
                // For now, we'll log a warning. The `ProcessTemplate` method will combine these parts.
                Console.WriteLine("Warning: No base image found in Fabric.js JSON. Rendering text elements without background image.");
                // Consider injecting fallbackHtmlContent here if it's meant to be a base layer when no image.
                // For now, it's handled by the calling method (ProcessTemplate) deciding which HTML source to use primarily.
            }

            // For each text element (placeholder or static text):
            foreach (var textObj in textElements)
            {
                // Construct the inline style string.
                string style = $"position: absolute; left: {textObj.Left}px; top: {textObj.Top}px; ";
                if (textObj.Angle != 0)
                {
                    // Apply rotation transform. Fabric.js typically rotates around the center.
                    // CSS transform-origin defaults to 50% 50%. For simple text overlays, this might be okay.
                    // If precise rotation around a specific point is needed, calculate transform-origin.
                    style += $"transform: rotate({textObj.Angle}deg); ";
                    // style += $"transform-origin: 0 0; "; // Example if rotating from top-left needed.
                }
                // Font family with fallback. Ensure `fontFamily` is a safe CSS value.
                style += $"font-family: '{WebUtility.HtmlEncode(textObj.FontFamily)}', sans-serif; ";
                // Font size with units. Ensure it's a valid CSS unit.
                style += $"font-size: {textObj.FontSize}px; ";
                // Color needs to be a valid CSS color string (hex, rgb, named color).
                // Fabric.js 'fill' property is usually a hex string.
                style += $"color: {WebUtility.HtmlEncode(textObj.Fill)}; ";
                // Prevent text wrapping by default.
                style += "white-space: nowrap; ";
                // Handle potential text overflow or ensure it doesn't break layout.
                style += "overflow: hidden; ";
                // Ensure text doesn't interfere with pointer events on underlying elements if they were interactive.
                style += "pointer-events: none; ";


                // If it's a placeholder, we wrap it in a span with a special marker and attribute for ProcessTemplate.
                if (!string.IsNullOrEmpty(textObj.PlaceholderName))
                {
                    // The content of the span will be the placeholder syntax itself, e.g., "<<FieldName>>".
                    // ProcessTemplate will then find these spans using their class and data-placeholder-name attribute
                    // and replace their inner content with the actual data, formatted according to the styles.
                    htmlOutput += $"<div class='fabric-text-overlay' style='{style}'><span><<{textObj.PlaceholderName}>></span></div>";
                }
                else
                {
                    // If it's static text, display it directly. Escape it for safety.
                    htmlOutput += $"<div class='fabric-text-static' style='{style}'>{WebUtility.HtmlEncode(textObj.OriginalText)}</div>";
                }
            }

            htmlOutput += "</div>"; // Close fabric-layout-container.

            return htmlOutput; // Return the generated HTML fragment.
        }

        // Helper class for Fabric.js text object properties.
        private class FabricTextObject
        {
            public string PlaceholderName { get; set; } = "";
            public string OriginalText { get; set; } = "";
            public double Left { get; set; }
            public double Top { get; set; }
            public string FontFamily { get; set; } = "Arial";
            public double FontSize { get; set; } = 16;
            public string Fill { get; set; } = "#000000";
            public double Angle { get; set; } = 0;
        }


        // This method is kept for standard HTML processing (when no FabricJson is used).
        // It needs to be called by the main ProcessTemplate if FabricJson is null or invalid.
        private string ProcessStandardHtml(string htmlContent, JsonElement jsonData)
        {
            string processedHtml = htmlContent;

            // 1. Process Conditional Expressions (${{...}}) FIRST
            processedHtml = ConditionalRegex.Replace(processedHtml, match =>
            {
                if (match.Groups.Count != 4) return match.Value;
                string conditionPart = match.Groups[1].Value.Trim();
                string truePart = match.Groups[2].Value;
                string falsePart = match.Groups[3].Value;

                bool conditionResult = false;
                bool conditionEvaluated = false;

                if (bool.TryParse(conditionPart, out bool literalBool))
                {
                    conditionResult = literalBool;
                    conditionEvaluated = true;
                }
                else
                {
                    var conditionPlaceholderMatch = SummernotePlaceholderRegex.Match(conditionPart);
                    if (conditionPlaceholderMatch.Success && conditionPlaceholderMatch.Groups.Count > 1)
                    {
                        string fieldName = conditionPlaceholderMatch.Groups[1].Value;
                        if (jsonData.ValueKind == JsonValueKind.Object && jsonData.TryGetProperty(fieldName, out JsonElement conditionValueElement))
                        {
                            if (conditionValueElement.ValueKind == JsonValueKind.True) { conditionResult = true; conditionEvaluated = true; }
                            else if (conditionValueElement.ValueKind == JsonValueKind.False) { conditionResult = false; conditionEvaluated = true; }
                            else if (conditionValueElement.ValueKind == JsonValueKind.String)
                            {
                                if (bool.TryParse(conditionValueElement.GetString(), out bool parsedStringBool))
                                {
                                    conditionResult = parsedStringBool;
                                    conditionEvaluated = true;
                                }
                            }
                            if (!conditionEvaluated) { conditionResult = false; conditionEvaluated = true; }
                        }
                        else { conditionResult = false; conditionEvaluated = true; }
                    }
                    if (!conditionEvaluated) { conditionResult = false; }
                }
                return conditionResult ? truePart : falsePart;
            });

            // 2. Process Simple Placeholders (<<FieldName>>) AFTER conditionals.
            // This needs to handle both regular <<FieldName>> and the ones generated by Fabric.js: <span class='fabric-text-overlay'><span><<FieldName>></span></span>
            // The original ProcessTemplate method needs to be aware of the new span structure.
            // We'll need a new regex or update the existing one for ProcessTemplate if it directly finds placeholders.
            // The current ProcessTemplate uses SummernotePlaceholderRegex to find <<FieldName>> in plain HTML.
            // For the Fabric.js generated HTML, we have `<span><<FieldName>></span>` inside a div.
            // The simple `<<FieldName>>` replacement within the span is handled by the current regex correctly.
            // If FabricJson styling is applied to the span, it needs to be preserved.

            // Process any remaining standard placeholders in the HTML content.
            // The challenge is to replace <<FieldName>> *only* within static HTML if FabricJson defines the layout.
            // Or, ensure the generated Fabric HTML has placeholders that ProcessTemplate can target.

            // Let's assume the FabricJson processing injects `<span><<FieldName>></span>` tags with appropriate styling.
            // Then, ProcessTemplate's existing logic should replace those tags correctly.

            processedHtml = SummernotePlaceholderRegex.Replace(processedHtml, match =>
            {
                if (match.Groups.Count > 1 && match.Groups[1].Success)
                {
                    string fieldName = match.Groups[1].Value;
                    string replacementValue = "";

                    if (jsonData.ValueKind == JsonValueKind.Object && jsonData.TryGetProperty(fieldName, out JsonElement valueElement))
                    {
                        replacementValue = valueElement.ValueKind switch
                        {
                            JsonValueKind.String => valueElement.GetString() ?? "",
                            JsonValueKind.Number => valueElement.GetRawText(),
                            JsonValueKind.True => "true",
                            JsonValueKind.False => "false",
                            JsonValueKind.Null => "",
                            JsonValueKind.Object or JsonValueKind.Array => valueElement.GetRawText(),
                            _ => ""
                        };
                        replacementValue = WebUtility.HtmlEncode(replacementValue);
                    }
                    return replacementValue;
                }
                return match.Value;
            });

            // Clean up any leftover placeholder syntax that wasn't replaced.
            // This must also match the format that could appear after Fabric processing.
            processedHtml = Regex.Replace(processedHtml, @"<<.*?>>", "", RegexOptions.Singleline);

            return processedHtml;
        }


        // Main method to process template with data.
        // This method will now be responsible for selecting the primary HTML source (Fabric or fallback)
        // and then processing placeholders within it.
        public string ProcessTemplate(string? fallbackHtmlContent, string? fabricJson, JsonElement jsonData)
        {
            string baseHtmlForProcessing = fallbackHtmlContent ?? ""; // Default to fallback HTML.

            // If Fabric JSON is provided and valid, use it to generate the primary HTML structure.
            if (!string.IsNullOrWhiteSpace(fabricJson))
            {
                try
                {
                    using JsonDocument fabricDoc = JsonDocument.Parse(fabricJson);
                    JsonElement fabricRoot = fabricDoc.RootElement;

                    if (fabricRoot.ValueKind == JsonValueKind.Object)
                    {
                        // Generate HTML structure from Fabric.js JSON.
                        // This generated HTML will include images and styled spans for text placeholders.
                        // The text in these spans will be like `<span><<FieldName>></span>`.
                        string generatedFabricHtml = BuildHtmlFromFabricJson(fabricRoot, jsonData);
                        if (!string.IsNullOrEmpty(generatedFabricHtml))
                        {
                            baseHtmlForProcessing = generatedFabricHtml; // Use Fabric-generated HTML as base.
                        }
                        else
                        {
                            // Fabric JSON was valid but produced empty HTML. Fallback.
                            Console.WriteLine("Warning: Fabric.js JSON processed but resulted in empty HTML. Falling back to fallbackHtmlContent.");
                        }
                    }
                    else
                    {
                        // Fabric JSON was not a valid object. Fallback.
                        Console.WriteLine("Warning: Fabric.js JSON is not a valid object. Falling back to fallbackHtmlContent.");
                    }
                }
                catch (JsonException jEx)
                {
                    Console.WriteLine($"Error parsing Fabric.js JSON: {jEx.Message}. Falling back to fallbackHtmlContent.");
                    // Fallback if Fabric JSON parsing fails.
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"An unexpected error occurred processing Fabric.js JSON: {ex.Message}. Falling back to fallbackHtmlContent.");
                    // Fallback for other processing errors.
                }
            }

            // Now, process the determined base HTML content (either from FabricJson or fallbackHtmlContent)
            // for standard placeholders (<<FieldName>>) and conditionals (${{...}}).
            // The placeholders generated by BuildHtmlFromFabricJson (like `<span><<FieldName>></span>`)
            // will be processed by this standard logic.
            return ProcessStandardHtml(baseHtmlForProcessing, jsonData);
        }


        // The following methods (ResolveParameters, GenerateExampleJson, IsValidJson, ExecuteScalarSql)
        // are helper methods and remain as they were.
        // ResolveParameters is used for <<param:parameterName>> within SQL strings.
        // GenerateExampleJson needs to potentially use FabricJson to create a better example.

        // Helper to resolve <<param:parameterName>> placeholders within a string.
        private string ResolveParameters(string inputString, JsonElement insideParameters)
        {
            string processedString = inputString;
            if (insideParameters.ValueKind != JsonValueKind.Object)
            {
                Console.WriteLine("Warning: Provided inside parameters are not a JSON object. Parameter placeholders will not be resolved.");
                processedString = ParameterPlaceholderRegex.Replace(processedString, "''");
                return processedString;
            }
            var parameterMatches = ParameterPlaceholderRegex.Matches(inputString);
            foreach (Match match in parameterMatches)
            {
                if (match.Groups.Count > 1 && match.Groups[1].Success)
                {
                    string placeholder = match.Value;
                    string parameterName = match.Groups[1].Value;
                    string replacementValue = "''";
                    bool parameterFound = false;
                    if (insideParameters.TryGetProperty(parameterName, out JsonElement paramValueElement))
                    {
                        parameterFound = true;
                        replacementValue = paramValueElement.ValueKind switch
                        {
                            JsonValueKind.String => $"'{paramValueElement.GetString()?.Replace("'", "''")}'",
                            JsonValueKind.Number => paramValueElement.GetRawText(),
                            JsonValueKind.True => "1",
                            JsonValueKind.False => "0",
                            JsonValueKind.Null => "NULL",
                            JsonValueKind.Object or JsonValueKind.Array => "''",
                            _ => "''"
                        };
                        if (paramValueElement.ValueKind == JsonValueKind.String && paramValueElement.GetString() == null)
                        {
                            replacementValue = "NULL";
                        }
                    }
                    if (!parameterFound)
                    {
                        Console.WriteLine($"Warning: Inside parameter '<<param:{parameterName}>>' not found in provided parameters. Replacing with empty string literal.");
                    }
                    processedString = processedString.Replace(placeholder, replacementValue);
                }
                else
                {
                    Console.WriteLine($"Warning: Malformed parameter placeholder match: '{match.Value}'. Skipping resolution.");
                }
            }
            return processedString;
        }

        // Generates an example JSON string from <<FieldName>> placeholders.
        // For Fabric.js, this should ideally parse FabricJson and extract placeholders from text elements.
        public string GenerateExampleJson(string htmlContent)
        {
            var exampleData = new Dictionary<string, string>();
            var placeholderMatches = SummernotePlaceholderRegex.Matches(htmlContent); // Use Summernote regex

            foreach (Match match in placeholderMatches)
            {
                if (match.Groups.Count > 1 && match.Groups[1].Success)
                {
                    string fieldName = match.Groups[1].Value;
                    if (!exampleData.ContainsKey(fieldName))
                    {
                        exampleData.Add(fieldName, "");
                    }
                }
            }

            var options = new JsonSerializerOptions { WriteIndented = true };
            return JsonSerializer.Serialize(exampleData, options);
        }

        public bool IsValidJson(string? json)
        {
            if (string.IsNullOrWhiteSpace(json)) return false;
            try
            {
                using JsonDocument doc = JsonDocument.Parse(json);
                if (doc.RootElement.ValueKind != JsonValueKind.Object) return false;
            }
            catch (JsonException)
            {
                return false;
            }
            return true;
        }

        // This method needs to be called with actual JSON data to produce sample output.
        // The current implementation assumes it's called with HTML content to extract placeholders.
        // For Fabric.js JSON, a separate parsing method would extract text elements and their placeholders.
        // This method might need an overload or adjustment if it's also meant to generate example JSON from FabricJson.
        // For now, it only processes standard HTML.

        // If GenerateExampleJson is called with FabricJson, it won't work as expected.
        // The logic to generate example JSON from FabricJson would need to be added here or called separately.
        // Let's assume GenerateExampleJson is called ONLY with htmlContent for now.

        public JsonElement ResolveInternalData(string? internalDataConfigJson, JsonElement insideParameters)
        {
            var resolvedData = new Dictionary<string, object?>();
            if (string.IsNullOrWhiteSpace(internalDataConfigJson))
            {
                using var doc = JsonDocument.Parse("{}");
                return doc.RootElement.Clone();
            }
            try
            {
                using JsonDocument doc = JsonDocument.Parse(internalDataConfigJson);
                if (doc.RootElement.ValueKind != JsonValueKind.Object)
                {
                    Console.WriteLine("InternalDataConfigJson is not a valid JSON object.");
                    using var emptyDoc = JsonDocument.Parse("{}");
                    return emptyDoc.RootElement.Clone();
                }
                foreach (JsonProperty property in doc.RootElement.EnumerateObject())
                {
                    string fieldName = property.Name;
                    string configValue = property.Value.GetString() ?? "";
                    object? resolvedValue = "--";
                    var sqlMatch = Regex.Match(configValue.Trim(), @"^sql\s*\(\s*'(.*)'\s*,\s*'(.*)'\s*\)$", RegexOptions.IgnoreCase | RegexOptions.Singleline);
                    if (sqlMatch.Success)
                    {
                        string sqlQuery = sqlMatch.Groups[1].Value.Replace("''", "'");
                        string parameterizedSqlQuery = ResolveParameters(sqlQuery, insideParameters);
                        string dbAlias = sqlMatch.Groups[2].Value;
                        try
                        {
                            resolvedValue = ExecuteScalarSql(dbAlias, parameterizedSqlQuery);
                            if (resolvedValue == DBNull.Value || resolvedValue == null)
                            {
                                resolvedValue = "--";
                            }
                        }
                        catch (Exception ex)
                        {
                            Console.WriteLine($"Error executing SQL query '{parameterizedSqlQuery}' for field '{fieldName}' from db '{dbAlias}': {ex.Message}");
                            resolvedValue = "--";
                        }
                    }
                    else
                    {
                        resolvedValue = ResolveParameters(configValue, insideParameters);
                    }
                    resolvedData[fieldName] = resolvedValue;
                }
                var options = new JsonSerializerOptions { WriteIndented = false };
                string resolvedJsonString = JsonSerializer.Serialize(resolvedData, options);
                using var resolvedJsonDoc = JsonDocument.Parse(resolvedJsonString);
                return resolvedJsonDoc.RootElement.Clone();
            }
            catch (JsonException jEx)
            {
                Console.WriteLine($"Error parsing InternalDataConfigJson: {jEx.Message}");
                using var emptyDoc = JsonDocument.Parse("{}");
                return emptyDoc.RootElement.Clone();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"An unexpected error occurred resolving internal data: {ex.Message}");
                using var emptyDoc = JsonDocument.Parse("{}");
                return emptyDoc.RootElement.Clone();
            }
        }

        private object? ExecuteScalarSql(string dbAlias, string sqlQuery)
        {
            var connectionStringsSection = _configuration.GetSection("InternalDataConnections");
            string? connectionString = connectionStringsSection[dbAlias];

            if (string.IsNullOrWhiteSpace(connectionString))
            {
                Console.WriteLine($"Connection string for alias '{dbAlias}' not found in InternalDataConnections.");
                return null;
            }

            using (var connection = new SqlConnection(connectionString))
            {
                using (var command = new SqlCommand(sqlQuery, connection))
                {
                    connection.Open();
                    object? result = command.ExecuteScalar();
                    return result;
                }
            }
        }
    }
}
```

---

**17. `PDFGenerator.Web\Controllers\TemplateController.cs`**
(Added logic for "Download Test PDF" to use versionType from query string, and modified revert logic to handle versionReferenceType)

```csharp
// File: Controllers/TemplateController.cs
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PDFGenerator.Web.Dtos.Template;
using PDFGenerator.Web.Dtos.TemplateVersion;
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Data;
using PdfGeneratorApp.Handlers;
using PDFGenerator.Web.Handlers; // For new handlers
using System.Collections.Generic; // For List<T>
using System.Linq; // For .Select()

namespace PdfGeneratorApp.Controllers
{
    [Authorize]
    public class TemplateController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly IConfiguration _configuration;

        private readonly IGetTemplateDesignHandler _getTemplateDesignHandler;
        private readonly IUpdateTemplateHandler _updateTemplateHandler;
        private readonly ICreateTemplateHandler _createTemplateHandler;
        private readonly IGetTemplateHistoryHandler _getTemplateHistoryHandler;
        private readonly IRevertTemplateHandler _revertTemplateHandler;
        private readonly IPublishTemplateHandler _publishTemplateHandler;
        private readonly ISoftDeleteTemplateVersionHandler _softDeleteTemplateVersionHandler;


        public TemplateController(ApplicationDbContext context, IConfiguration configuration,
                                  IGetTemplateDesignHandler getTemplateDesignHandler,
                                  IUpdateTemplateHandler updateTemplateHandler,
                                  ICreateTemplateHandler createTemplateHandler,
                                  IGetTemplateHistoryHandler getTemplateHistoryHandler,
                                  IRevertTemplateHandler revertTemplateHandler,
                                  IPublishTemplateHandler publishTemplateHandler,
                                  ISoftDeleteTemplateVersionHandler softDeleteTemplateVersionHandler)
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
        }

        private List<string> GetDatabaseAliases()
        {
            return _configuration.GetSection("InternalDataConnections").GetChildren().Select(c => c.Key).ToList();
        }

        // GET: /templates/design/{templateName}
        [HttpGet("templates/design/{templateName}")]
        public async Task<IActionResult> Design(string templateName)
        {
            Result<TemplateDetailDto> result = await _getTemplateDesignHandler.HandleAsync(templateName);

            if (!result.IsCompleteSuccessfully)
            {
                if (result.ErrorMessages == ErrorMessageUserConst.TemplateNotFound)
                {
                    return NotFound($"Template '{templateName}' not found.");
                }
                return StatusCode(500, result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
            }

            ViewBag.DatabaseAliases = GetDatabaseAliases();
            return View(result.Data);
        }

        // POST: /templates/design/{templateName}
        [HttpPost("templates/design/{templateName}")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Design(string templateName, [Bind("Id,Description,HtmlContent,ExampleJsonData,InternalDataConfigJson,FabricJson")] TemplateUpdateDto templateDto) // Added FabricJson to Bind
        {
             Result<TemplateDetailDto> detailDtoOnError = await _getTemplateDesignHandler.HandleAsync(templateName);
             if (detailDtoOnError.IsCompleteSuccessfully && detailDtoOnError.Data != null)
             {
                 detailDtoOnError.Data.Description = templateDto.Description;
                 detailDtoFormatting.Data.HtmlContent = templateDto.HtmlContent;
                 detailDtoOnError.Data.ExampleJsonData = templateDto.ExampleJsonData;
                 detailDtoOnError.Data.InternalDataConfigJson = templateDto.InternalDataConfigJson;
                 detailDtoOnError.Data.FabricJson = templateDto.FabricJson; // Also update FabricJson in view data for error display
             }
             ViewBag.DatabaseAliases = GetDatabaseAliases();

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

        // GET: /templates/create
        public IActionResult Create()
        {
            ViewBag.DatabaseAliases = GetDatabaseAliases();
            // Initialize FabricJson as empty JSON object for a new template
            return View(new TemplateCreateDto { HtmlContent = "", FabricJson = "{}" });
        }

        // POST: /templates/create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create([Bind("Name,HtmlContent,Description,ExampleJsonData,InternalDataConfigJson,FabricJson")] TemplateCreateDto templateDto) // Added FabricJson to Bind
        {
            if (!ModelState.IsValid)
            {
                ViewBag.DatabaseAliases = GetDatabaseAliases();
                return View(templateDto);
            }

            var result = await _createTemplateHandler.HandleAsync(templateDto);

            if (!result.IsCompleteSuccessfully)
            {
                ModelState.AddModelError("", result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);

                if (result.ErrorMessages == ErrorMessageUserConst.TemplateNameExists)
                {
                    ModelState.AddModelError("Name", result.ErrorMessages);
                }
                else if (result.ErrorMessages == ErrorMessageUserConst.InternalDataConfigInvalidJson || result.ErrorMessages == ErrorMessageUserConst.InternalDataConfigNotObject)
                {
                    ModelState.AddModelError(nameof(TemplateCreateDto.InternalDataConfigJson), result.ErrorMessages);
                }

                ViewBag.DatabaseAliases = GetDatabaseAliases();
                return View(templateDto);
            }

            TempData["Message"] = $"Template '{result.Data}' created successfully!";
            return RedirectToAction(nameof(Design), new { templateName = result.Data });
        }

        // GET: /templates/{templateName}/history
        [HttpGet("templates/{templateName}/history")]
        public async Task<IActionResult> History(string templateName)
        {
            Result<TemplateDetailDto> templateDetailResult = await _getTemplateDesignHandler.HandleAsync(templateName);
            if (!templateDetailResult.IsCompleteSuccessfully || templateDetailResult.Data == null)
            {
                 TempData["ErrorMessage"] = templateDetailResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                 return RedirectToAction(nameof(Index), "Home");
            }

            // Fetch version history (handler now returns only non-deleted versions)
            var versionsResult = await _getTemplateHistoryHandler.HandleAsync(templateDetailResult.Data.Id);

            if (!versionsResult.IsCompleteSuccessfully)
            {
                TempData["ErrorMessage"] = versionsResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                ViewBag.TemplateVersions = new List<TemplateVersionDto>();
            }
            else
            {
                ViewBag.TemplateVersions = versionsResult.Data;
            }

            return View(templateDetailResult.Data);
        }

        // POST: /templates/{TemplateName}/revert/{VersionNumber}
        [HttpPost("templates/{TemplateName}/revert/{VersionNumber}")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Revert([FromRoute] TemplateRevertRequestDto routeRequest, [FromForm] string versionReferenceType)
        {
            var request = new TemplateRevertRequestDto
            {
                TemplateName = routeRequest.TemplateName,
                VersionNumber = routeRequest.VersionNumber,
                VersionReferenceType = versionReferenceType
            };

            var result = await _revertTemplateHandler.HandleAsync(request);

            if (!result.IsCompleteSuccessfully)
            {
                TempData["Error"] = result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                return RedirectToAction(nameof(History), new { templateName = request.TemplateName });
            }

            TempData["Message"] = $"Template '{request.TemplateName}' {request.VersionReferenceType} version successfully reverted to {result.Data}.";
            return RedirectToAction(nameof(History), new { templateName = request.TemplateName });
        }

        // POST: /templates/{TemplateName}/publish
        [HttpPost("templates/{TemplateName}/publish")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Publish([FromRoute] string templateName)
        {
            var result = await _publishTemplateHandler.HandleAsync(templateName);

            if (!result.IsCompleteSuccessfully)
            {
                TempData["Error"] = result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                return RedirectToAction(nameof(Design), new { templateName = templateName });
            }

            TempData["Message"] = $"Template '{templateName}' successfully published to Production Version {result.Data}.";
            return RedirectToAction(nameof(Design), new { templateName = templateName });
        }

         // POST: /templates/versions/{versionId}/delete
        [HttpPost("templates/versions/{VersionId}/delete")]
        [ValidateAntiForgeryToken]
         public async Task<IActionResult> SoftDeleteVersion([FromRoute] int versionId)
         {
             // Fetch the version to get template name for redirect, and check if it's currently referenced.
             var versionEntity = await _context.TemplateVersions
                                        .Include(tv => tv.Template)
                                        .FirstOrDefaultAsync(tv => tv.Id == versionId);

             if (versionEntity == null)
             {
                 TempData["ErrorMessage"] = $"Template version with ID {versionId} not found.";
                 return RedirectToAction(nameof(Index), "Home"); // Or a more appropriate redirect.
             }

             string templateName = versionEntity.Template?.Name ?? ""; // Get template name for redirect.

             // Call the soft delete handler.
             var result = await _softDeleteTemplateVersionHandler.HandleAsync(versionId);

             if (!result.IsCompleteSuccessfully)
             {
                 TempData["Error"] = result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
             }
             else
             {
                 TempData["Message"] = $"Template version {versionEntity.VersionNumber} for '{templateName}' soft-deleted successfully.";
             }

             // Redirect back to the History page of the template.
             if (!string.IsNullOrEmpty(templateName))
             {
                return RedirectToAction(nameof(History), new { templateName = templateName });
             }
             else
             {
                 return RedirectToAction(nameof(Index), "Home"); // Fallback redirect.
             }
         }
    }
}
```

---

**18. `PDFGenerator.Web\Views\Template\Design.cshtml`**
(Modified to include Fabric.js JSON editor and potentially upload)

```html
@using PDFGenerator.Web.Dtos.Template
@model TemplateDetailDto
@{
    ViewData["Title"] = $"Design Template: {Model.Name}";
    var dbAliases = ViewBag.DatabaseAliases as List<string> ?? new List<string>();
}

<div class="container">
    <div class="page-header">
        <h1>@ViewData["Title"]</h1>
        <p class="page-subtitle">Edit the HTML content and data configurations for the <strong>@Model.Name</strong> template.</p>
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

                <!-- Display Testing and Production versions -->
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

                <!-- HTML Content section -->
                <div class="mb-3">
                    <h5>HTML Content Source:</h5>
                    <div class="form-group mb-3">
                        <label for="htmlEditor" class="control-label">Edit HTML Content:</label>
                        <textarea asp-for="HtmlContent" class="form-control" rows="15" id="htmlEditor"></textarea>
                        <span asp-validation-for="HtmlContent" class="text-danger"></span>
                        <small class="form-text text-muted">Use <code>&lt;&lt;FieldName&gt;&gt;</code> for dynamic data placeholders and <code>${{condition ? true_part : false_part}}</code> for conditionals.</small>
                    </div>
                    <p class="text-center my-3">OR Upload an HTML file to populate the editor:</p>
                    <div class="form-group mb-3">
                        <label for="htmlFile" class="form-label">Upload HTML File (.html):</label>
                        <input type="file" id="htmlFile" name="htmlFile" class="form-control" accept=".html,.htm" />
                    </div>
                    <div id="uploadStatus" class="mt-2"></div>
                </div>

                <hr class="my-4">

                <h5>Visual Layout (Fabric.js JSON):</h5>
                <p class="text-muted">Define the visual layout, including images and text placeholders, using Fabric.js. This will be overlaid on your HTML content.</p>

                 <!-- Fabric.js JSON input group -->
                 <div class="form-group mb-3">
                    <label asp-for="FabricJson" class="control-label">Fabric.js JSON:</label>
                    <textarea asp-for="FabricJson" class="form-control" rows="10" id="fabricJsonEditor"></textarea>
                    <span asp-validation-for="FabricJson" class="text-danger"></span>
                    <small class="form-text text-muted">Paste your Fabric.js canvas JSON here. Ensure text elements intended as placeholders are marked or named appropriately.</small>
                 </div>
                 <!-- Optional: Add a button to open a Fabric.js editor or a sample JSON -->
                 <div class="mb-3">
                     <button type="button" class="btn btn-secondary btn-sm" id="loadFabricSampleBtn">Load Sample Fabric JSON</button>
                     <button type="button" class="btn btn-sm btn-outline-secondary" id="clearFabricJsonBtn">Clear Fabric JSON</button>
                 </div>

                <!-- Data Configuration section -->
                <h5>Data Configuration:</h5>
                <p class="text-muted">Define how placeholders in the HTML content will be populated for "Outside" (API provided) and "Inside" (system sourced) data modes.</p>

                 <!-- Placeholder list -->
                 <div class="card card-body mb-3">
                     <h6>Detected Placeholders:</h6>
                     <ul id="placeholderList" class="list-inline mb-0 small text-muted">
                         <li class="list-inline-item"><em>(Edit HTML or Load Fabric JSON to detect placeholders)</em></li>
                     </ul>
                 </div>

                <div class="form-group mb-3">
                    <label asp-for="ExampleJsonData" class="control-label">Example JSON Data (for "Outside" mode & docs):</label>
                    <textarea asp-for="ExampleJsonData" class="form-control" rows="10" id="exampleJsonData"></textarea>
                    <span asp-validation-for="ExampleJsonData" class="text-danger"></span>
                    <small class="form-text text-muted">Provide a sample JSON payload for this template's API documentation and testing in "Outside" mode.</small>
                </div>

                 <div class="form-group mb-3">
                    <label asp-for="InternalDataConfigJson" class="control-label">Internal Data Configuration (for "Inside" mode):</label>
                    <textarea asp-for="InternalDataConfigJson" class="form-control" rows="10" id="internalDataConfigJson"></textarea>
                    <span asp-validation-for="InternalDataConfigJson" class="text-danger"></span>
                    <small class="form-text text-muted">
                         Configure data sources for "Inside" mode. Use JSON format like <code>{ "FieldName": "StaticValue", "AnotherField": "sql('SELECT Value FROM Table WHERE ID = &lt;&lt;param:RecordId&gt;&gt;', 'databaseAlias')" }</code>.
                         Use <code>&lt;&lt;param:parameterName&gt;&gt;</code> to include values passed to the API when using "Inside" mode.
                         Available database aliases: @string.Join(", ", dbAliases).
                    </small>
                </div>

                <div class="form-group mt-4">
                    <input type="submit" value="Save Changes" class="btn btn-primary" />
                    <a asp-action="Index" asp-controller="Home" class="btn btn-secondary">Back to Templates</a>
                    <a asp-controller="Template" asp-action="History" asp-route-templateName="@Model.Name" class="btn btn-info">View History</a>
                    <!-- Download Test PDF button - this should ideally test the *Testing* version -->
                    <button type="button" id="downloadPdfBtn" class="btn btn-success">Download Test PDF (Testing Version)</button>
                </div>
                 @Html.AntiForgeryToken()
            </form>
        </div>
    </div>
</div>

@section Scripts {
    @{await Html.RenderPartialAsync("_ValidationScriptsPartial");}

    <!-- Summernote CSS/JS -->
    <link href="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.js"></script>
    <!-- Lodash JS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.21/lodash.min.js"></script>

    <!-- Fabric.js Library -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.0/fabric.min.js"></script>

    <script>
        $(document).ready(function() {
            var htmlEditor = $('#htmlEditor');
            var fabricJsonEditor = $('#fabricJsonEditor');
            var exampleJsonDataTextarea = $('#exampleJsonData');
            var internalDataConfigJsonTextarea = $('#internalDataConfigJson');
            var placeholderListElement = $('#placeholderList');

            // Initialize Summernote editor
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
                ],
                 callbacks: {
                    onChange: _.debounce(function(contents, $editable) {
                         updatePlaceholdersList(contents); // Update placeholders from HTML editor
                         // When HTML content changes, we don't auto-update Fabric JSON.
                         // The user would need to explicitly save/load JSON or trigger placeholder detection on Fabric.
                    }, 500)
                 }
            });

            // Helper to update the detected placeholders list (reads from HTML editor and potentially Fabric JSON)
            function updatePlaceholdersList(html) {
                 const placeholderRegex = /&lt;&lt;(\w+)&gt;&gt;/g; // Matches HTML entities for <<...>>
                 let match;
                 const placeholders = new Set();

                 // Add placeholders found in standard HTML content
                 while ((match = placeholderRegex.exec(html)) !== null) {
                      placeholders.add(match[1]);
                 }

                 // Add placeholders found in Fabric.js JSON (if available and parsed)
                 if (fabricJsonEditor.val()) {
                     try {
                         const fabricJson = JSON.parse(fabricJsonEditor.val());
                         if (fabricJson && fabricJson.objects && Array.isArray(fabricJson.objects)) {
                             fabricJson.objects.forEach(obj => {
                                 if (obj.type === 'textbox' || obj.type === 'text') {
                                     const textValue = obj.text || '';
                                     const phMatch = placeholderRegex.exec(textValue); // Match placeholder in Fabric text
                                     if (phMatch && phMatch.Groups.Count > 1) {
                                         placeholders.add(phMatch.Groups[1].Value);
                                     }
                                 }
                             });
                         }
                     } catch (e) {
                         console.warn("Could not parse Fabric JSON for placeholder detection:", e);
                     }
                 }


                 // Update the list display
                 placeholderListElement.empty();
                 if (placeholders.size === 0) {
                      placeholderListElement.html('<li class="list-inline-item"><em>(No data placeholders detected)</em></li>');
                 } else {
                      placeholders.forEach(placeholder => {
                           placeholderListElement.append(`<li class="list-inline-item"><code><<${placeholder}>></code></li>`);
                      });
                 }
            }

            // Helper function to format JSON textareas
            function formatJsonTextarea(textarea) {
                 try {
                     var rawJson = textarea.val();
                      if (rawJson && rawJson.trim() !== "{}" && rawJson.trim() !== "") {
                         var parsedJson = JSON.parse(rawJson);
                         textarea.val(JSON.stringify(parsedJson, null, 2));
                     } else {
                         textarea.val('{}');
                     }
                 } catch (e) {
                     console.error("Failed to parse existing JSON:", textarea.attr('id'), e);
                 }
            }

            // Format JSON textareas on load
            formatJsonTextarea(exampleJsonDataTextarea);
            formatJsonTextarea(internalDataConfigJsonTextarea);
            formatJsonTextarea(fabricJsonEditor); // Also format Fabric JSON editor

            // --- Handle Fabric JSON loading/clearing ---
            $('#loadFabricSampleBtn').on('click', function() {
                // Example Fabric.js JSON structure. You would replace this with actual sample data.
                // This sample assumes a background image and two text placeholders.
                const sampleFabricJson = JSON.stringify({
                    "version": "5.0.0",
                    "objects": [
                        {
                            "type": "image",
                            "url": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iI2VlZSIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LXNpemU9IjE2cHgiIGZpbGw9IiMzMzMiIHRleHQtYW5jaG9yPSJtaWRkbGUiPjwvZGVmcz48c3R5bGU+PC9zdHlsZT48L3N2Zz4=", // Placeholder SVG as base64 data URL
                            "left": 0,
                            "top": 0,
                            "width": 400, // Assuming canvas width is 400px
                            "height": 400, // Assuming canvas height is 400px
                            "scaleX": 1, "scaleY": 1
                        },
                        {
                            "type": "textbox",
                            "text": "<<CustomerName>>", // Placeholder text
                            "left": 50,
                            "top": 80,
                            "width": 300,
                            "height": 40,
                            "fontFamily": "Cairo",
                            "fontSize": 24,
                            "fill": "#333333",
                            "angle": 0,
                            "originX": "left", "originY": "top"
                        },
                        {
                            "type": "textbox",
                            "text": "Order Date: <<OrderDate>>", // Another placeholder
                            "left": 50,
                            "top": 120,
                            "width": 300,
                            "height": 30,
                            "fontFamily": "Cairo",
                            "fontSize": 18,
                            "fill": "#555555",
                            "angle": 5, // Rotated slightly
                            "originX": "left", "originY": "top"
                        },
                         {
                            "type": "textbox",
                            "text": "This is static text", // Non-placeholder static text
                            "left": 50,
                            "top": 160,
                            "width": 300,
                            "height": 30,
                            "fontFamily": "Arial",
                            "fontSize": 16,
                            "fill": "#777777",
                            "angle": 0,
                            "originX": "left", "originY": "top"
                        }
                    ],
                    "background": "transparent" // Example background property
                }, JSON.stringify(null, 2)); // Pretty print with 2 spaces.

                fabricJsonEditor.val(sampleFabricJson); // Set the editor's value.
                showStatus('Loaded sample Fabric.js JSON.', 'info');
                updatePlaceholdersList(htmlEditor.val()); // Update placeholders based on current HTML + loaded JSON.
            });

            $('#clearFabricJsonBtn').on('click', function() {
                fabricJsonEditor.val('{}'); // Set to empty JSON object.
                showStatus('Cleared Fabric.js JSON.', 'info');
                updatePlaceholdersList(htmlEditor.val()); // Update placeholders after clearing.
            });

            // --- HTML File Upload ---
            $('#htmlFile').on('change', function() {
                var file = this.files[0];
                if (file) {
                    showStatus('Reading HTML file...');
                    var reader = new FileReader();
                    reader.onload = function(e) {
                        htmlEditor.summernote('code', e.target.result);
                        showStatus('HTML file loaded into editor.', 'success');
                        // When HTML is loaded, it might contain <<placeholders>> that need to be detected.
                        updatePlaceholdersList(e.target.result);
                        // We DO NOT auto-update Fabric JSON here. User should manage it separately.
                    };
                    reader.onerror = function() {
                        showStatus('Error reading HTML file.', 'danger');
                    };
                    reader.readAsText(file);
                } else {
                    uploadStatus.html('');
                }
            });

            // Function to show status messages.
            function showStatus(message, type = 'info') {
                uploadStatus.html(`<div class="alert alert-${type}">${message}</div>`);
            }

            // Initial placeholder detection on page load.
            // This should scan both the HTML editor AND the Fabric JSON editor for placeholders.
            updatePlaceholdersList(htmlEditor.val()); // Initial scan of HTML editor.

        }); // End of jQuery document ready.
    </script>
}
```

---

**19. `PDFGenerator.Web\Controllers\TemplateController.cs`**
(Updated Design POST action to bind `FabricJson` and added a button for it)

```csharp
// File: Controllers/TemplateController.cs
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PDFGenerator.Web.Dtos.Template;
using PDFGenerator.Web.Dtos.TemplateVersion;
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Data;
using PdfGeneratorApp.Handlers;
using PDFGenerator.Web.Handlers;
using System.Collections.Generic;
using System.Linq;


namespace PdfGeneratorApp.Controllers
{
    [Authorize]
    public class TemplateController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly IConfiguration _configuration;

        private readonly IGetTemplateDesignHandler _getTemplateDesignHandler;
        private readonly IUpdateTemplateHandler _updateTemplateHandler;
        private readonly ICreateTemplateHandler _createTemplateHandler;
        private readonly IGetTemplateHistoryHandler _getTemplateHistoryHandler;
        private readonly IRevertTemplateHandler _revertTemplateHandler;
        private readonly IPublishTemplateHandler _publishTemplateHandler;
        private readonly ISoftDeleteTemplateVersionHandler _softDeleteTemplateVersionHandler;


        public TemplateController(ApplicationDbContext context, IConfiguration configuration,
                                  IGetTemplateDesignHandler getTemplateDesignHandler,
                                  IUpdateTemplateHandler updateTemplateHandler,
                                  ICreateTemplateHandler createTemplateHandler,
                                  IGetTemplateHistoryHandler getTemplateHistoryHandler,
                                  IRevertTemplateHandler revertTemplateHandler,
                                  IPublishTemplateHandler publishTemplateHandler,
                                  ISoftDeleteTemplateVersionHandler softDeleteTemplateVersionHandler)
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
        }

        private List<string> GetDatabaseAliases()
        {
            return _configuration.GetSection("InternalDataConnections").GetChildren().Select(c => c.Key).ToList();
        }

        // GET: /templates/design/{templateName}
        [HttpGet("templates/design/{templateName}")]
        public async Task<IActionResult> Design(string templateName)
        {
            Result<TemplateDetailDto> result = await _getTemplateDesignHandler.HandleAsync(templateName);

            if (!result.IsCompleteSuccessfully)
            {
                if (result.ErrorMessages == ErrorMessageUserConst.TemplateNotFound)
                {
                    return NotFound($"Template '{templateName}' not found.");
                }
                return StatusCode(500, result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
            }

            ViewBag.DatabaseAliases = GetDatabaseAliases();
            // Ensure FabricJson is initialized in the DTO if it's null for display/editing purposes
            if (result.Data != null && string.IsNullOrEmpty(result.Data.FabricJson))
            {
                result.Data.FabricJson = "{}"; // Initialize with empty JSON object
            }
            return View(result.Data);
        }

        // POST: /templates/design/{templateName}
        [HttpPost("templates/design/{templateName}")]
        [ValidateAntiForgeryToken]
        // Added FabricJson to the Bind attribute.
        public async Task<IActionResult> Design(string templateName, [Bind("Id,Description,HtmlContent,ExampleJsonData,InternalDataConfigJson,FabricJson")] TemplateUpdateDto templateDto)
        {
             Result<TemplateDetailDto> detailDtoOnError = await _getTemplateDesignHandler.HandleAsync(templateName);
             if (detailDtoOnError.IsCompleteSuccessfully && detailDtoOnError.Data != null)
             {
                 // Update the DTO for the view with submitted values, including FabricJson
                 detailDtoOnError.Data.Description = templateDto.Description;
                 detailDtoOnError.Data.HtmlContent = templateDto.HtmlContent;
                 detailDtoOnError.Data.ExampleJsonData = templateDto.ExampleJsonData;
                 detailDtoOnError.Data.InternalDataConfigJson = templateDto.InternalDataConfigJson;
                 detailDtoOnError.Data.FabricJson = templateDto.FabricJson; // Assign FabricJson for error display
             }
             ViewBag.DatabaseAliases = GetDatabaseAliases();

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

        // GET: /templates/create
        public IActionResult Create()
        {
            ViewBag.DatabaseAliases = GetDatabaseAliases();
            // Initialize FabricJson as empty JSON object for a new template
            return View(new TemplateCreateDto { HtmlContent = "", FabricJson = "{}" });
        }

        // POST: /templates/create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create([Bind("Name,HtmlContent,Description,ExampleJsonData,InternalDataConfigJson,FabricJson")] TemplateCreateDto templateDto) // Added FabricJson to Bind
        {
            if (!ModelState.IsValid)
            {
                ViewBag.DatabaseAliases = GetDatabaseAliases();
                return View(templateDto);
            }

            var result = await _createTemplateHandler.HandleAsync(templateDto);

            if (!result.IsCompleteSuccessfully)
            {
                ModelState.AddModelError("", result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);

                if (result.ErrorMessages == ErrorMessageUserConst.TemplateNameExists)
                {
                    ModelState.AddModelError("Name", result.ErrorMessages);
                }
                else if (result.ErrorMessages == ErrorMessageUserConst.InternalDataConfigInvalidJson || result.ErrorMessages == ErrorMessageUserConst.InternalDataConfigNotObject)
                {
                    ModelState.AddModelError(nameof(TemplateCreateDto.InternalDataConfigJson), result.ErrorMessages);
                }

                ViewBag.DatabaseAliases = GetDatabaseAliases();
                return View(templateDto);
            }

            TempData["Message"] = $"Template '{result.Data}' created successfully!";
            return RedirectToAction(nameof(Design), new { templateName = result.Data });
        }

        // GET: /templates/{templateName}/history
        [HttpGet("templates/{templateName}/history")]
        public async Task<IActionResult> History(string templateName)
        {
            Result<TemplateDetailDto> templateDetailResult = await _getTemplateDesignHandler.HandleAsync(templateName);
            if (!templateDetailResult.IsCompleteSuccessfully || templateDetailResult.Data == null)
            {
                 TempData["ErrorMessage"] = templateDetailResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                 return RedirectToAction(nameof(Index), "Home");
            }

            var versionsResult = await _getTemplateHistoryHandler.HandleAsync(templateDetailResult.Data.Id);

            if (!versionsResult.IsCompleteSuccessfully)
            {
                TempData["ErrorMessage"] = versionsResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                ViewBag.TemplateVersions = new List<TemplateVersionDto>();
            }
            else
            {
                ViewBag.TemplateVersions = versionsResult.Data;
            }

            return View(templateDetailResult.Data);
        }

        // POST: /templates/{TemplateName}/revert/{VersionNumber}
        [HttpPost("templates/{TemplateName}/revert/{VersionNumber}")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Revert([FromRoute] TemplateRevertRequestDto routeRequest, [FromForm] string versionReferenceType)
        {
            var request = new TemplateRevertRequestDto
            {
                TemplateName = routeRequest.TemplateName,
                VersionNumber = routeRequest.VersionNumber,
                VersionReferenceType = versionReferenceType
            };

            var result = await _revertTemplateHandler.HandleAsync(request);

            if (!result.IsCompleteSuccessfully)
            {
                TempData["Error"] = result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                return RedirectToAction(nameof(History), new { templateName = request.TemplateName });
            }

            TempData["Message"] = $"Template '{request.TemplateName}' {request.VersionReferenceType} version successfully reverted to {result.Data}.";
            return RedirectToAction(nameof(History), new { templateName = request.TemplateName });
        }

        // POST: /templates/{TemplateName}/publish
        [HttpPost("templates/{TemplateName}/publish")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Publish([FromRoute] string templateName)
        {
            var result = await _publishTemplateHandler.HandleAsync(templateName);

            if (!result.IsCompleteSuccessfully)
            {
                TempData["Error"] = result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                return RedirectToAction(nameof(Design), new { templateName = templateName });
            }

            TempData["Message"] = $"Template '{templateName}' successfully published to Production Version {result.Data}.";
            return RedirectToAction(nameof(Design), new { templateName = templateName });
        }

         // POST: /templates/versions/{versionId}/delete
        [HttpPost("templates/versions/{VersionId}/delete")]
        [ValidateAntiForgeryToken]
         public async Task<IActionResult> SoftDeleteVersion([FromRoute] int versionId)
         {
             var versionEntity = await _context.TemplateVersions
                                        .Include(tv => tv.Template)
                                        .FirstOrDefaultAsync(tv => tv.Id == versionId);

             if (versionEntity == null)
             {
                 TempData["ErrorMessage"] = $"Template version with ID {versionId} not found.";
                 return RedirectToAction(nameof(Index), "Home");
             }

             string templateName = versionEntity.Template?.Name ?? "";

             var result = await _softDeleteTemplateVersionHandler.HandleAsync(versionId);

             if (!result.IsCompleteSuccessfully)
             {
                 TempData["Error"] = result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
             }
             else
             {
                 TempData["Message"] = $"Template version {versionEntity.VersionNumber} for '{templateName}' soft-deleted successfully.";
             }

             if (!string.IsNullOrEmpty(templateName))
             {
                return RedirectToAction(nameof(History), new { templateName = templateName });
             }
             else
             {
                 return RedirectToAction(nameof(Index), "Home");
             }
         }
    }
}
```

---

**Steps to complete the Fabric.js integration:**

1.  **UI for Fabric.js Design:** You'll need to build a UI component (likely a separate page or modal) where users can actually design templates using Fabric.js. This UI would allow:
    *   Uploading background images.
    *   Adding text elements, configuring their properties, and associating them with `<<PlaceholderName>>` values.
    *   Saving the canvas state as Fabric.js JSON.
    *   This JSON would then be saved into the `Template.FabricJson` or `TemplateVersion.FabricJson` field.

2.  **Update `TemplateCreateDto` and `TemplateUpdateDto`:** Ensure `FabricJson` is included in the `[Bind]` attributes for the `Create` and `Design` (POST) actions in `TemplateController`. (Done in the modified `TemplateController.cs` above).

3.  **Update `TemplateRepository`:** The `CreateNewTemplateAsync` and `UpdateTemplateAsync` methods should correctly handle saving/updating the `FabricJson` field. The current modifications seem to handle this mapping.

4.  **Modify `GeneratePdfHandler.cs`:** As shown in the updated `GeneratePdfHandler.cs`, it now calls `_templateProcessingService.ProcessTemplate(templateDataAccessDto.HtmlContent, templateDataAccessDto.FabricJson, finalDataForHtmlProcessing)` passing the `FabricJson` along.

5.  **Update `TemplateProcessingService.ProcessTemplate`:** This is the most critical part where the new hybrid logic resides, as demonstrated in the modified `TemplateProcessingService.cs` file above. This method is now responsible for:
    *   Parsing the `FabricJson`.
    *   Extracting images and text objects.
    *   Generating HTML (`<img>` tags for images, styled `<div>` or `<span>` for text/placeholders).
    *   Replacing `<<FieldName>>` placeholders within the Fabric.js text objects using the `jsonData`.
    *   The logic in `ProcessTemplate` needs to correctly assemble the final HTML for WkHtmlToPdf.

Let me know if you need further assistance with the `ProcessTemplate` method's intricate logic for parsing Fabric.js JSON and generating the overlay HTML!

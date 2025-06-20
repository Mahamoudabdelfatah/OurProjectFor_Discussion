Okay, let's add these features to your PDF Generator application.

We'll break down the changes by file and layer:

1.  **Models (`PDFGenerator.Infrastructure\DataAccess\Models`)**:
    *   Modify `Template.cs` to replace `CurrentVersion` with `TestingVersion` and add `ProductionVersion`.
    *   Modify `TemplateVersion.cs` to add `IsDeleted` and `DeletedDate`.

2.  **Data Access DTOs (`PDFGenerator.Infrastructure\DataAccess\Dtos`)**:
    *   Modify `TemplateDataAccessDto.cs` to reflect the version property changes.
    *   Modify `TemplateSimpleDto.cs` to reflect the version property changes.
    *   Modify `TemplatesDocDataAccessDto.cs` to reflect the version property changes.
    *   Modify `TemplateVersionDataAccessDto.cs` to reflect the soft delete properties.

3.  **AutoMapper Profile (`PDFGenerator.Infrastructure\DataAccess\MappingProfile\DataAccessMappingProfile.cs`)**:
    *   Update existing mappings to include the new/renamed properties.

4.  **Repositories (`PDFGenerator.Infrastructure\DataAccess\Repositories`)**:
    *   Modify `ITemplateRepository.cs` to update method signatures and add new methods for publish and revert with type.
    *   Modify `TemplateRepository.cs` to implement the new methods and update existing ones.
    *   Modify `ITemplateVersionRepository.cs` to update method signatures (to filter by IsDeleted) and add soft delete method.
    *   Modify `TemplateVersionRepository.cs` to implement the new method and update existing queries to filter by `IsDeleted`.

5.  **Handlers (`PDFGenerator.Web\Services` & `PDFGenerator.Web\Services\Auth`)**:
    *   Modify `TemplateRevertRequestDto.cs` to include the version reference type.
    *   Modify `IGetTemplatesListHandler.cs` / `GetTemplatesListHandler.cs`.
    *   Modify `IGetTemplatesDocHandler.cs` / `GetTemplatesDocHandler.cs`.
    *   Modify `IGetTemplateByNameHandler.cs` / `GetTemplateByNameHandler.cs`.
    *   Modify `IGeneratePdfHandler.cs` / `GeneratePdfHandler.cs`.
    *   Modify `IUpdateTemplateHandler.cs` / `UpdateTemplateHandler.cs`.
    *   Modify `IGetTemplateHistoryHandler.cs` / `GetTemplateHistoryHandler.cs`.
    *   Modify `IRevertTemplateHandler.cs` / `RevertTemplateHandler.cs`.
    *   Add new handler interface `IPublishTemplateHandler.cs`.
    *   Add new handler implementation `PublishTemplateHandler.cs`.
    *   Add new handler interface `ISoftDeleteTemplateVersionHandler.cs`.
    *   Add new handler implementation `SoftDeleteTemplateVersionHandler.cs`.
    *   Update `PDFGenerator.Web\Extensions\ServiceCollectionExtensions.cs` to register the new handlers.

6.  **Controllers (`PDFGenerator.Web\Controllers`)**:
    *   Modify `TemplateController.cs` to add actions for Publish and Soft Delete, and update the Revert action to handle the version reference type.

7.  **Views (`PDFGenerator.Web\Views`)**:
    *   Modify `Index.cshtml` to display both version numbers.
    *   Modify `Design.cshtml` to display both version numbers, add a "Publish" button, and potentially simplify the "Download Test PDF" button (keeping it tied to Testing version).
    *   Modify `History.cshtml` to display the soft delete status, add "Soft Delete" buttons (with confirmation), and modify the "Revert" functionality to allow selecting which reference (Testing/Production) to revert.

8.  **Database Migrations**: EF Core will automatically detect the model changes. You'll need to generate and apply a new migration. (Instructions on how to do this are outside the scope of just explaining code, but it's a necessary step).

Let's go through the code changes.

---

**Modified Files:**

1.  **`PDFGenerator.Helper\Helper\ErrorMessageUserConst.cs`** (Adding new errors)
2.  **`PDFGenerator.Infrastructure\DataAccess\Dtos\TemplateDataAccessDto.cs`**
3.  **`PDFGenerator.Infrastructure\DataAccess\Dtos\TemplatesDocDataAccessDto.cs`**
4.  **`PDFGenerator.Infrastructure\DataAccess\Dtos\TemplateSimpleDto.cs`**
5.  **`PDFGenerator.Infrastructure\DataAccess\Dtos\TemplateVersionDataAccessDto.cs`**
6.  **`PDFGenerator.Infrastructure\DataAccess\MappingProfile\DataAccessMappingProfile.cs`**
7.  **`PDFGenerator.Infrastructure\DataAccess\Models\Template.cs`**
8.  **`PDFGenerator.Infrastructure\DataAccess\Models\TemplateVersion.cs`**
9.  **`PDFGenerator.Infrastructure\DataAccess\Repositories\Implementation\TemplateRepository.cs`**
10. **`PDFGenerator.Infrastructure\DataAccess\Repositories\Implementation\TemplateVersionRepository.cs`**
11. **`PDFGenerator.Infrastructure\DataAccess\Repositories\Interfaces\ITemplateRepository.cs`**
12. **`PDFGenerator.Infrastructure\DataAccess\Repositories\Interfaces\ITemplateVersionRepository.cs`**
13. **`PDFGenerator.Infrastructure\DataSeeding\DataSeedingExtensions.cs`** (Initial template seeding update)
14. **`PDFGenerator.Web\Dtos\Template\TemplateRevertRequestDto.cs`**
15. **`PDFGenerator.Web\Extensions\ServiceCollectionExtensions.cs`**
16. **`PDFGenerator.Web\MappingProfile\ApplicationLayerMappingProfile.cs`**
17. **`PDFGenerator.Web\Services\GeneratePdfHandler.cs`**
18. **`PDFGenerator.Web\Services\GetTemplateByNameHandler.cs`**
19. **`PDFGenerator.Web\Services\GetTemplateDesignHandler.cs`**
20. **`PDFGenerator.Web\Services\GetTemplateHistoryHandler.cs`**
21. **`PDFGenerator.Web\Services\GetTemplatesDocHandler.cs`**
22. **`PDFGenerator.Web\Services\GetTemplatesListHandler.cs`**
23. **`PDFGenerator.Web\Services\RevertTemplateHandler.cs`**
24. **`PDFGenerator.Web\Services\UpdateTemplateHandler.cs`**
25. **`PDFGenerator.Web\Controllers\TemplateController.cs`**
26. **`PDFGenerator.Web\Views\Index.cshtml`**
27. **`PDFGenerator.Web\Views\Template\Design.cshtml`**
28. **`PDFGenerator.Web\Views\Template\History.cshtml`**

**New Files:**

1.  **`PDFGenerator.Helper\Helper\VersionReferenceTypeEnum.cs`** (Helper enum for revert type)
2.  **`PDFGenerator.Infrastructure\DataAccess\Repositories\Interfaces\ITemplateVersionRepository.cs`** (Added methods)
3.  **`PDFGenerator.Web\Services\PublishTemplateHandler.cs`**
4.  **`PDFGenerator.Web\Services\SoftDeleteTemplateVersionHandler.cs`**

Let's apply the changes step by step.

---

**1. `PDFGenerator.Helper\Helper\ErrorMessageUserConst.cs`**
(Adding new errors)

```csharp
// File: Result.cs // Still has the wrong comment, but adding errors here.
namespace PdfGeneratorApp.Common
{
    public static class ErrorMessageUserConst
    {
        public const string Unexpected = "An unexpected error occurred.";
        public const string RequestFailed = "The request failed.";
        public const string ServerErrorNoMsg = "A server error occurred.";
        public const string DeserializationFailed = "Failed to process the response data.";
        public const string ResponseHandlingError = "Failed to handle the response.";
        public const string TemplateNotFound = "Template not found.";
        public const string UserNotFound = "user not found.";
        public const string TemplateNameExists = "A template with this name already exists.";
        public const string TemplateIdNotFound = "Template with ID {0} not found.";
        public const string TemplateNameMismatch = "Template name mismatch.";
        public const string InternalDataConfigInvalidJson = "Internal Data Configuration is not valid JSON.";
        public const string InternalDataConfigNotObject = "Internal Data Configuration must be a valid JSON object.";
        public const string PdfGenerationFailed = "PDF generation failed.";
        public const string InvalidMode = "Invalid mode specified. Must be 'outside' or 'inside'.";
        public const string InsideModeBodyNotObject = "For 'inside' mode, the request body must be a JSON object.";
        public const string VersionNotFound = "Version {0} for template '{1}' not found.";
        public const string CannotRevertToFutureVersion = "Cannot revert to version {0}. Current version is {1}.";
        public const string ExampleJsonGenerationFailed = "Failed to auto-generate Example JSON.";


         public const string IncorrectInput =  "incorrect or Empty input";
         public const string EmailAlreadyRegistered =  "Email is already registered!";
         public const string incorrectEmailOrPassword = "Email or Password is incorrect!";
         public const string InvalidToken = "Invalid token";
         public const string InvalidRequest = "Invalid Request";

        // New Errors for Versioning/Soft Delete
        public const string InvalidVersionReferenceType = "Invalid version reference type specified. Must be 'Testing' or 'Production'.";
        public const string CannotDeleteCurrentVersion = "Cannot delete the current Testing or Production version.";
        public const string VersionAlreadyDeleted = "Version is already deleted.";
        public const string CannotPublishToProductionBeforeTesting = "Testing version must be greater than Production version to publish."; // Added if needed for validation
    }
}
```

---

**2. `PDFGenerator.Helper\Helper\VersionReferenceTypeEnum.cs`**
(New file for helper enum/constants)

```csharp
﻿// New file for Version Reference Types

namespace PdfGeneratorApp.Common
{
    // Using const strings for string-based values, similar to RoleEnum
    public static class VersionReferenceType
    {
        public const string Testing = "Testing";
        public const string Production = "Production";

        // Optional: Add a method to check if a string is a valid type
        public static bool IsValid(string type)
        {
            return type == Testing || type == Production;
        }
    }
}
```

---

**3. `PDFGenerator.Infrastructure\DataAccess\Models\Template.cs`**
(Modified to replace `CurrentVersion` and add `ProductionVersion`)

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

        // Renamed CurrentVersion to TestingVersion
        public int TestingVersion { get; set; } = 1;

        // Added ProductionVersion
        // Nullable int? means it can be null if no version is published yet, or an int for the version number.
        public int? ProductionVersion { get; set; } = 1; // Setting default to 1, could be null

        public DateTime LastModified { get; set; } = DateTime.Now;

        public ICollection<TemplateVersion> Versions { get; set; }
    }
}
```

---

**4. `PDFGenerator.Infrastructure\DataAccess\Models\TemplateVersion.cs`**
(Modified to add soft delete properties)

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

        [Required]
        public string HtmlContent { get; set; }

        public string? Description { get; set; }

        public string? ExampleJsonData { get; set; }

        public string? InternalDataConfigJson { get; set; }

        public DateTime CreatedDate { get; set; } = DateTime.Now;

        // New property for soft delete status
        public bool IsDeleted { get; set; } = false;

        // New property for deletion timestamp (nullable)
        public DateTime? DeletedDate { get; set; } = null;

        [ForeignKey("TemplateId")]
        public Template Template { get; set; }
    }
}
```

---

**5. `PDFGenerator.Infrastructure\DataAccess\Dtos\TemplateDataAccessDto.cs`**
(Modified to reflect version properties)

```csharp
// File: Infrastructure/Data/Dtos/TemplateDataAccessDto.cs
using PdfGeneratorApp.Models;
using System;
using System.Collections.Generic; // Make sure this is included if ICollection is used

namespace PDFGenerator.Infrastructure.DataAccess.Dtos
{
    public class TemplateDataAccessDto
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string HtmlContent { get; set; }
        public string? Description { get; set; }
        public string? ExampleJsonData { get; set; }
        public string? InternalDataConfigJson { get; set; }

        // Renamed property
        public int TestingVersion { get; set; }

        // Added property
        public int? ProductionVersion { get; set; }

        public DateTime LastModified { get; set; }

        // Collection of version DTOs
        public ICollection<TemplateVersionDataAccessDto> Versions { get; set; }
    }
}
```

---

**6. `PDFGenerator.Infrastructure\DataAccess\Dtos\TemplatesDocDataAccessDto.cs`**
(Modified to reflect version properties)

```csharp
﻿// File: Infrastructure/Data/Dtos/TemplateDataAccessDto.cs // Still has the wrong comment
using System.ComponentModel.DataAnnotations;

namespace PDFGenerator.Infrastructure.DataAccess.Dtos
{
    public class TemplatesDocDataAccessDto
    {
        public int Id { get; set; }
        [Required]
        [StringLength(100, ErrorMessage = "Template Name cannot exceed 100 characters.")]
        public string Name { get; set; }
        public string? Description { get; set; }
        public string? ExampleJsonData { get; set; }
        public string? InternalDataConfigJson { get; set; }

        // Added properties for documentation clarity
        public int TestingVersion { get; set; }
        public int? ProductionVersion { get; set; }
    }
}
```

---

**7. `PDFGenerator.Infrastructure\DataAccess\Dtos\TemplateSimpleDto.cs`**
(Modified to reflect version properties)

```csharp
﻿namespace PDFGenerator.Infrastructure.DataAccess.Dtos
{
    public class TemplateSimpleDto
    {
        public int Id { get; set; }
        public string Name { get; set; }

        // Renamed property
        public int TestingVersion { get; set; }

        // Added property
        public int? ProductionVersion { get; set; }

        public DateTime LastModified { get; set; }
    }
}
```

---

**8. `PDFGenerator.Infrastructure\DataAccess\Dtos\TemplateVersionDataAccessDto.cs`**
(Modified to add soft delete properties)

```csharp
// File: Infrastructure/Data/Dtos/TemplateVersionDataAccessDto.cs
using System; // For DateTime, DateTime?

namespace PDFGenerator.Infrastructure.DataAccess.Dtos
{
    public class TemplateVersionDataAccessDto
    {
        public int Id { get; set; }
        public int TemplateId { get; set; }
        public int VersionNumber { get; set; }
        public string HtmlContent { get; set; }
        public string? Description { get; set; }
        public string? ExampleJsonData { get; set; }
        public string? InternalDataConfigJson { get; set; }
        public DateTime CreatedDate { get; set; }

        // New properties
        public bool IsDeleted { get; set; }
        public DateTime? DeletedDate { get; set; }
    }
}
```

---

**9. `PDFGenerator.Infrastructure\DataAccess\MappingProfile\DataAccessMappingProfile.cs`**
(Modified to update mappings for new/renamed properties)

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
            // Mapping from Template model to TemplateDataAccessDto
            CreateMap<Template, TemplateDataAccessDto>()
                // Map CurrentVersion to TestingVersion
                .ForMember(dest => dest.TestingVersion, opt => opt.MapFrom(src => src.TestingVersion))
                // Map ProductionVersion
                .ForMember(dest => dest.ProductionVersion, opt => opt.MapFrom(src => src.ProductionVersion));


            // Mapping from TemplateDataAccessDto to Template model
            CreateMap<TemplateDataAccessDto, Template>()
                 // Map TestingVersion back to TestingVersion
                .ForMember(dest => dest.TestingVersion, opt => opt.MapFrom(src => src.TestingVersion))
                 // Map ProductionVersion back to ProductionVersion
                .ForMember(dest => dest.ProductionVersion, opt => opt.MapFrom(src => src.ProductionVersion));

            // This mapping is still questionable, but updated property names.
            CreateMap<TemplateVersion, TemplateDataAccessDto>().ReverseMap();

            // Mapping between TemplateVersion model and TemplateVersionDataAccessDto
            CreateMap<TemplateVersion, TemplateVersionDataAccessDto>()
                // Map soft delete properties
                .ForMember(dest => dest.IsDeleted, opt => opt.MapFrom(src => src.IsDeleted))
                .ForMember(dest => dest.DeletedDate, opt => opt.MapFrom(src => src.DeletedDate))
                .ReverseMap(); // Create reverse mapping including soft delete properties

            // New mappings for simplified DTOs
            CreateMap<Template, TemplateSimpleDto>()
                .ForMember(dest => dest.TestingVersion, opt => opt.MapFrom(src => src.TestingVersion))
                .ForMember(dest => dest.ProductionVersion, opt => opt.MapFrom(src => src.ProductionVersion));

             CreateMap<Template, TemplatesDocDataAccessDto>()
                .ForMember(dest => dest.Id, opt => opt.MapFrom(src => src.Id)) // Map Template Id
                .ForMember(dest => dest.Name, opt => opt.MapFrom(src => src.Name))
                .ForMember(dest => dest.Description, opt => opt.MapFrom(src => src.Description)) // Description from Template
                .ForMember(dest => dest.TestingVersion, opt => opt.MapFrom(src => src.TestingVersion))
                .ForMember(dest => dest.ProductionVersion, opt => opt.MapFrom(src => src.ProductionVersion))
                // Note: ExampleJsonData and InternalDataConfigJson for DocsDto ideally come from the *current* version.
                // The GetAllAsync query in TemplateRepository does this join, so the mapping here for TemplatesDocDataAccessDto
                // from Template model might not be the one actually used by GetAllAsync.
                // The mapping below handles mapping from the DTO produced by the LINQ query.
                ;

             // Add mapping specifically for the DTO used by GetAllAsync query in TemplateRepository
             // This maps the anonymous object/projection created by the query to the target DTO
             CreateMap<TemplatesDocDataAccessDto, TemplatesDocDataAccessDto>(); // Identity map, just to be explicit if needed, or remove if AutoMapper handles projection directly.

             // We need mapping from the projection result of TemplateRepository.GetAllAsync
             // Since the query *directly creates* TemplatesDocDataAccessDto, no mapping from
             // a combined entity/version is explicitly needed for that specific query's output.
             // The mapping from Template to TemplatesDocDataAccessDto above might be for other use cases.
             // Let's ensure mapping from TemplateVersion (used in GetByNameAsync query projection) works:
             CreateMap<TemplateVersion, TemplateDataAccessDto>() // This was already there, let's refine for clarity
                 .ForMember(dest => dest.Id, opt => opt.Ignore()) // Id comes from Template
                 .ForMember(dest => dest.Name, opt => opt.Ignore()) // Name comes from Template
                 .ForMember(dest => dest.TestingVersion, opt => opt.Ignore()) // Versions come from Template
                 .ForMember(dest => dest.ProductionVersion, opt => opt.Ignore()) // Versions come from Template
                 .ForMember(dest => dest.LastModified, opt => opt.Ignore()) // Modified date comes from Template
                 .ForMember(dest => dest.Versions, opt => opt.Ignore()); // Versions collection is not mapped from a single version

            // The GetByNameAsync query in TemplateRepository *selects* into TemplateDataAccessDto directly,
            // combining properties from Template and TemplateVersion. So the mapping from TemplateVersion
            // to TemplateDataAccessDto above might not be fully utilized in that specific query.
            // AutoMapper handles the mapping from TemplateDataAccessDto (created by the query) to Web DTOs.
        }
    }
}
```

---

**10. `PDFGenerator.Infrastructure\DataAccess\Repositories\Interfaces\ITemplateRepository.cs`**
(Modified interface)

```csharp
// File: Infrastructure/Data/Repositories/ITemplateRepository.cs
using PDFGenerator.Infrastructure.DataAccess.Dtos;
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Infrastructure.Data.Repositories.Base;
using PdfGeneratorApp.Models;
using System.Threading.Tasks; // Needed for Task

namespace PdfGeneratorApp.Infrastructure.Data.Repositories
{
    public interface ITemplateRepository : IBaseRepository<Template, TemplateDataAccessDto>
    {
        // yoyo todo add pgaination and change this bad name
        // Return type updated as TemplateSimpleDto now includes ProductionVersion
        Task<Result<List<TemplateSimpleDto>>> GetAllTemplateSimplAsync();

        // Return type updated as TemplatesDocDataAccessDto now includes version info
        // Note: The query implementation should fetch content from the *Testing* version for docs
        Task<Result<List<TemplatesDocDataAccessDto>>> GetAllAsync();

        // Updated to reflect TestingVersion/ProductionVersion in returned DTO
        // This method should fetch content based on the *TestingVersion* of the template
        Task<Result<TemplateDataAccessDto>> GetByNameAsync(string name);

        Task<Result<bool>> AnyByNameAsync(string name);

        // Updated as CreateNewTemplateAsync now sets Testing/Production versions
        Task<Result<TemplateDataAccessDto>> CreateNewTemplateAsync(TemplateDataAccessDto templateDataAccessDto);

        // Updated as UpdateTemplateAsync creates a new *Testing* version
        // Method name might be better as CreateNewTestingVersionAsync? But keeping original for minimal changes.
        Task<Result<TemplateDataAccessDto>> UpdateTemplateAsync(TemplateDataAccessDto templateDataAccessDto);

        // Modified signature to specify which version reference to revert (Testing or Production)
        // Returns the version number it was reverted *to*.
        Task<Result<int>> RevertTemplateAsync(string templateName, int targetVersionNumber, string versionReferenceType);

        // New method to publish the Testing version to Production
        // Returns the new Production version number (which is the old Testing version number)
        Task<Result<int>> PublishTemplateAsync(string templateName);
    }
}
```

---

**11. `PDFGenerator.Infrastructure\DataAccess\Repositories\Interfaces\ITemplateVersionRepository.cs`**
(Modified interface to add soft delete method)

```csharp
// File: Infrastructure/Data/Repositories/ITemplateVersionRepository.cs
using PdfGeneratorApp.Infrastructure.Data.Repositories.Base;
using PdfGeneratorApp.Models;
using PdfGeneratorApp.Common;
using PDFGenerator.Infrastructure.DataAccess.Dtos;
using System.Collections.Generic; // Needed for List<T>
using System.Threading.Tasks; // Needed for Task

namespace PdfGeneratorApp.Infrastructure.Data.Repositories
{
    public interface ITemplateVersionRepository : IBaseRepository<TemplateVersion, TemplateVersionDataAccessDto>
    {
        //todo
        // Modified: This method should now ONLY return versions where IsDeleted is false.
         Task<Result<List<TemplateVersionDataAccessDto>>> GetByTemplateVersionsByTemplateIdAsync(int templateId);

         //Task<Result<TemplateVersionDataAccessDto>> GetByTemplateIdAndVersionNumberAsync(int templateId, int versionNumber);

         // New method for soft deleting a template version
         Task<Result<bool>> SoftDeleteVersionAsync(int versionId);

         // Optional: Method to find a specific version by template ID and version number (might be needed for validation in handlers/repos)
         Task<TemplateVersion?> FindVersionAsync(int templateId, int versionNumber);

         // Optional: Method to get the Template entity by ID (useful for checking current versions before delete/revert)
         Task<Template?> GetTemplateByIdAsync(int templateId);
    }
}
```

---

**12. `PDFGenerator.Infrastructure\DataAccess\Repositories\Implementation\TemplateRepository.cs`**
(Modified implementation)

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
using System.Linq; // Needed for .Max()

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

        // Updated return type
        public async Task<Result<List<TemplateSimpleDto>>> GetAllTemplateSimplAsync()
        {
            try
            {
                List<TemplateSimpleDto> data = await context.Templates.Select(t => new TemplateSimpleDto()
                {
                    Id = t.Id,
                    Name = t.Name,
                    LastModified = t.LastModified, // Corrected to use actual LastModified
                    TestingVersion = t.TestingVersion, // Include TestingVersion
                    ProductionVersion = t.ProductionVersion // Include ProductionVersion

                }).ToListAsync();

                return Result<List<TemplateSimpleDto>>.Success(data);

            }
            catch (Exception ex) // Catch specific exception types if possible, or log generic one
            {
                Console.WriteLine($"Error in TemplateRepository.GetAllTemplateSimplAsync: {ex.Message}"); // Log error
                return Result<List<TemplateSimpleDto>>.Failure(ErrorMessageUserConst.ServerErrorNoMsg); // Generic error
            }
        }

        // Updated return type, query modified to use TestingVersion content
        public async Task<Result<List<TemplatesDocDataAccessDto>>> GetAllAsync()
        {
             try
             {
                 // Join Templates (t) with TemplateVersions (tv) based on Template ID and Matching TestingVersion
                 var templates = await (from t in context.Templates
                                        join tv in context.TemplateVersions
                                        on new { TemplateId = t.Id, Version = t.TestingVersion }
                                        equals new { tv.TemplateId, Version = tv.VersionNumber }
                                        where !tv.IsDeleted // Only include non-deleted versions
                                        select new TemplatesDocDataAccessDto
                                        {
                                            Id = t.Id, // Use Template ID here
                                            Name = t.Name,
                                            Description = t.Description, // Description from Template
                                            ExampleJsonData = tv.ExampleJsonData,
                                            InternalDataConfigJson = tv.InternalDataConfigJson,
                                            TestingVersion = t.TestingVersion, // Include TestingVersion
                                            ProductionVersion = t.ProductionVersion // Include ProductionVersion
                                        }).ToListAsync();

                // Check if the list is null (ToListAsync returns empty list, not null on no results)
                // The check `if (templates == null)` is unnecessary/incorrect for ToListAsync.
                // If no templates are found, the list will be empty, which is a successful result.
                // Return success even if the list is empty.
                return Result<List<TemplatesDocDataAccessDto>>.Success(templates);
             }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in TemplateRepository.GetAllAsync: {ex.Message}"); // Log error
                return Result<List<TemplatesDocDataAccessDto>>.Failure(ErrorMessageUserConst.ServerErrorNoMsg); // Generic error
            }
        }

        // Updated return type and logic to fetch TestingVersion content
        public async Task<Result<TemplateDataAccessDto>> GetByNameAsync(string name)
        {
            // Find the parent Template entity by name, include Versions to check against later (though not strictly needed for fetching *current* version content).
            Template? template = await context.Templates
                                      .Include(t => t.Versions) // Include versions for potential checks or mapping if needed.
                                      .SingleOrDefaultAsync(t => t.Name == name);

            if (template == null)
            {
                return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.TemplateNotFound); // Template not found.
            }

            // Find the TemplateVersion entity matching the template's TestingVersion.
            // Filter by TemplateId, VersionNumber, and ensure it's not deleted.
            TemplateVersion? currentTestingVersionContent = template.Versions
                .SingleOrDefault(tv => tv.VersionNumber == template.TestingVersion && !tv.IsDeleted);

            if (currentTestingVersionContent == null)
            {
                 // This indicates an inconsistency: the Template points to a TestingVersion that doesn't exist or is deleted.
                 // Handle this error case. Maybe revert TestingVersion to 1 if possible, or return a specific error.
                 // For now, returning version not found error.
                 return Result<TemplateDataAccessDto>.Failure(string.Format(ErrorMessageUserConst.VersionNotFound, template.TestingVersion, name));
            }

            // Create the TemplateDataAccessDto by combining properties from the Template and the current TemplateVersion content.
            var templateDto = _mapper.Map<TemplateDataAccessDto>(template); // Map basic template properties

            // Manually map properties from the current version content.
            templateDto.HtmlContent = currentTestingVersionContent.HtmlContent;
            templateDto.Description = currentTestingVersionContent.Description; // Use description from version if available
            templateDto.ExampleJsonData = currentTestingVersionContent.ExampleJsonData;
            templateDto.InternalDataConfigJson = currentTestingVersionContent.InternalDataConfigJson;
            // Ensure version numbers from the template are used.
            templateDto.TestingVersion = template.TestingVersion;
            templateDto.ProductionVersion = template.ProductionVersion;


            // The templateDto.Versions collection won't be populated by the code above.
            // If the handler needs the full list of versions, it should call the version repository separately,
            // or modify this query to include all versions. For the "Design" view, only the current content is strictly needed.
            // Let's leave Versions as null/empty in this DTO for GetByNameAsync to keep it focused on getting *content* for the current testing version.

            return Result<TemplateDataAccessDto>.Success(templateDto);
        }

        public async Task<Result<bool>> AnyByNameAsync(string name)
        {
            try
            {
                var exists = await context.Templates.AnyAsync(t => t.Name == name); // Use context.Templates or DbSet
                return Result<bool>.Success(exists);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in TemplateRepository.AnyByNameAsync: {ex.Message}");
                return Result<bool>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }

        // Updated to initialize Testing/Production versions
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
                // This error message is confusing as it mentions "Handler" but is in the repository.
                return Result<TemplateDataAccessDto>.Failure($"Repository: Error generating example JSON on create: {ex.Message}");
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

            // Set initial versions for the new template
            templateDto.TestingVersion = 1;
            templateDto.ProductionVersion = 1; // Initially Production is same as Testing
            templateDto.LastModified = DateTime.Now;

            // Create the initial version content
            var initialVersion = new TemplateVersion
            {
                VersionNumber = 1,
                CreatedDate = DateTime.Now,
                HtmlContent = templateDto.HtmlContent,
                Description = templateDto.Description,
                ExampleJsonData = templateDto.ExampleJsonData,
                InternalDataConfigJson = templateDto.InternalDataConfigJson,
                IsDeleted = false // Ensure it's not marked deleted
            };

            try
            {
                // Map the TemplateDataAccessDto to Template entity.
                // AutoMapper should map simple properties.
                // We need to manually set the Versions collection on the entity.
                Template template = _mapper.Map<Template>(templateDto);
                template.Versions = new List<TemplateVersion> { initialVersion }; // Add the initial version

                await context.Templates.AddAsync(template);
                // Note: SaveChangesAsync() is in UoW.

                // Return the input DTO, which now has ID populated after SaveChangesAsync in UoW,
                // but we return it *before* SaveChangesAsync here, so ID is not yet set.
                // The handler uses result.Data.Name, which is fine.
                // It might be better to return the mapped entity and let the mapper handle populating the DTO after save.
                // However, sticking to the current pattern of returning the input DTO for now.
                return Result<TemplateDataAccessDto>.Success(templateDto);
            }
            catch (Exception ex)
            {
                // Log the actual exception 'ex'
                Console.WriteLine($"Error in TemplateRepository.CreateNewTemplateAsync: {ex.Message}");
                return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.ServerErrorNoMsg); // Generic server error
            }
        }

        // Updated to create new *Testing* version
        public async Task<Result<TemplateDataAccessDto>> UpdateTemplateAsync(TemplateDataAccessDto templateDto)
        {
            // Validation of config JSON is duplicated here from handler.
            // It should primarily be in the handler/service layer, but repository can also validate data it receives.
            if (!string.IsNullOrWhiteSpace(templateDto.InternalDataConfigJson) && !_templateProcessingService.IsValidJson(templateDto.InternalDataConfigJson))
            {
                 return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.InternalDataConfigInvalidJson);
            }
             // Added check for NotObject validation too
            if (!string.IsNullOrWhiteSpace(templateDto.InternalDataConfigJson))
            {
                try {
                     using JsonDocument doc = JsonDocument.Parse(templateDto.InternalDataConfigJson);
                     if (doc.RootElement.ValueKind != JsonValueKind.Object)
                     {
                         return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.InternalDataConfigNotObject);
                     }
                } catch (JsonException) { /* Caught by first check */ }
            }


            // Find the existing parent Template entity, including its versions.
            Template? existingTemplate = await context.Templates
                                              .Include(t => t.Versions)
                                              .FirstOrDefaultAsync(t => t.Id == templateDto.Id);

            if (existingTemplate == null)
            {
                return Result<TemplateDataAccessDto>.Failure(string.Format(ErrorMessageUserConst.TemplateIdNotFound, templateDto.Id));
            }

            // Calculate the next version number based on existing versions (including deleted ones).
            // Use template.Versions collection loaded with Include().
            int lastVersionNumber = existingTemplate.Versions.Any() ? existingTemplate.Versions.Max(tv => tv.VersionNumber) : 0;
            int nextVersionNumber = lastVersionNumber + 1;

            // Create a new TemplateVersion entity for the update.
            TemplateVersion newVersion = new TemplateVersion()
            {
                TemplateId = templateDto.Id,
                VersionNumber = nextVersionNumber, // Use the calculated next version number.
                HtmlContent = templateDto.HtmlContent,
                Description = templateDto.Description,
                ExampleJsonData = _templateProcessingService.GenerateExampleJson(templateDto.HtmlContent), // Generate new example JSON.
                InternalDataConfigJson = templateDto.InternalDataConfigJson,
                CreatedDate = DateTime.Now, // Use DateTime.Now for precision.
                IsDeleted = false // New version is not deleted.
            };

            // Add the new version to the context. It will be added to the database and associated with the template.
            existingTemplate.Versions.Add(newVersion); // Add to the collection on the entity

            // Update the parent template's *TestingVersion* to the new version number.
            existingTemplate.TestingVersion = newVersion.VersionNumber;
            existingTemplate.LastModified = DateTime.Now;

            // The existingTemplate entity is now tracked by the context with its state modified.
            // DbSet.Update(entity) is not strictly needed here if the entity was retrieved by EF Core and modified.
            // context.Templates.Update(existingTemplate); // Can be uncommented for clarity if desired, but EF tracks it.

            // Map the updated existingTemplate entity back to a DTO.
            // This DTO now has the updated TestingVersion and LastModified.
            var updatedTemplateDto = _mapper.Map<TemplateDataAccessDto>(existingTemplate);
            // Manually add the newly created version's content to the DTO if needed for handler's return value consistency.
            // Or just return the DTO representing the template metadata + the *new* testing version number.
            // The handler expects an int (the new version number), so let's adjust the return type of THIS repo method.
            // The interface ITemplateRepository expects Task<Result<TemplateDataAccessDto>>. Let's keep that for now, but the handler uses only CurrentVersion (now TestingVersion).

            // Return success with the DTO reflecting the changes.
            return Result<TemplateDataAccessDto>.Success(updatedTemplateDto);
        }


        // Modified signature to handle version reference type
        // Returns the version number it was reverted *to*.
        public async Task<Result<int>> RevertTemplateAsync(string templateName, int targetVersionNumber, string versionReferenceType)
        {
            // Find the template by name, include versions to check target version exists and is not deleted.
            Template? existingTemplate = await context.Templates
                                              .Include(t => t.Versions)
                                              .FirstOrDefaultAsync(t => t.Name == templateName);

            if (existingTemplate == null) return Result<int>.Failure(ErrorMessageUserConst.TemplateNotFound);

            // Find the target version in the collection, ensuring it's not deleted.
            TemplateVersion? targetVersion = existingTemplate.Versions
                .SingleOrDefault(tv => tv.VersionNumber == targetVersionNumber);

            if (targetVersion == null)
            {
                 return Result<int>.Failure(string.Format(ErrorMessageUserConst.VersionNotFound, targetVersionNumber, templateName));
            }
             if (targetVersion.IsDeleted)
            {
                 // Prevent reverting to a deleted version.
                 return Result<int>.Failure($"Version {targetVersionNumber} is deleted and cannot be reverted to."); // Specific error message
            }


            // Update the appropriate version reference based on the type.
            switch (versionReferenceType.ToLowerInvariant())
            {
                case VersionReferenceType.Testing:
                     // Optional validation: Prevent reverting Testing to a version older than Production? Depends on desired workflow.
                     // if (existingTemplate.ProductionVersion.HasValue && targetVersionNumber < existingTemplate.ProductionVersion.Value) { ... }
                     existingTemplate.TestingVersion = targetVersionNumber;
                    break;
                case VersionReferenceType.Production:
                     // Often, you can only publish a version that is currently the Testing version.
                     // Reverting Production to an *older* version than the current Testing version is usually allowed.
                     // Validation: Is the target version number less than or equal to the current Testing version?
                     // This prevents "publishing" a version that was never the current Testing version.
                     if (targetVersionNumber > existingTemplate.TestingVersion)
                     {
                          return Result<int>.Failure(string.Format(ErrorMessageUserConst.CannotRevertToFutureVersion, targetVersionNumber, existingTemplate.TestingVersion));
                     }
                     existingTemplate.ProductionVersion = targetVersionNumber;
                    break;
                default:
                    // This case should ideally be caught by handler/controller input validation, but included as a safeguard.
                    return Result<int>.Failure(ErrorMessageUserConst.InvalidVersionReferenceType);
            }

            existingTemplate.LastModified = DateTime.Now; // Update last modified timestamp.

            // Note: SaveChangesAsync() is expected to be called by UnitOfWork.

            // Return the version number that was set.
            return Result<int>.Success(targetVersionNumber);
        }

        // New method implementation for publishing.
        // Returns the new Production version number.
        public async Task<Result<int>> PublishTemplateAsync(string templateName)
        {
             // Find the template by name.
            Template? existingTemplate = await context.Templates.FirstOrDefaultAsync(t => t.Name == templateName);

            if (existingTemplate == null) return Result<int>.Failure(ErrorMessageUserConst.TemplateNotFound);

            // Check if there's a newer testing version than production version to publish.
            // If Testing and Production are already the same, maybe indicate nothing happened or return success?
            if (existingTemplate.ProductionVersion.HasValue && existingTemplate.TestingVersion <= existingTemplate.ProductionVersion.Value)
            {
                 // Production is already at or ahead of Testing. Nothing to publish.
                 // Return success, maybe with a specific message or indicator?
                 return Result<int>.Success(existingTemplate.ProductionVersion.Value); // Indicate current production version
            }

            // Set ProductionVersion to the current TestingVersion.
            existingTemplate.ProductionVersion = existingTemplate.TestingVersion;
            existingTemplate.LastModified = DateTime.Now; // Update last modified timestamp.

            // Note: SaveChangesAsync() is expected to be called by UnitOfWork.

            // Return the new Production version number.
            return Result<int>.Success(existingTemplate.ProductionVersion.Value);
        }
    }
}
```

---

**13. `PDFGenerator.Infrastructure\DataAccess\Repositories\Implementation\TemplateVersionRepository.cs`**
(Modified implementation to filter and add soft delete)

```csharp
// File: Infrastructure/Data/Repositories/TemplateVersionRepository.cs
using PdfGeneratorApp.Infrastructure.Data.Repositories.Base;
using PdfGeneratorApp.Data;
using AutoMapper;
using PdfGeneratorApp.Models;
using PdfGeneratorApp.Common;
using Microsoft.EntityFrameworkCore;
using PDFGenerator.Infrastructure.DataAccess.Dtos;
using System; // Needed for DateTime.Now

namespace PdfGeneratorApp.Infrastructure.Data.Repositories
{
    public class TemplateVersionRepository : BaseRepository<TemplateVersion, TemplateVersionDataAccessDto>, ITemplateVersionRepository
    {
        private readonly ApplicationDbContext context;
        private readonly IMapper mapper;

        public TemplateVersionRepository(ApplicationDbContext context, IMapper mapper): base(context, mapper)
        {
            this.context = context;
            this.mapper = mapper;
        }

        // Modified to ONLY return non-deleted versions.
        public async Task<Result<List<TemplateVersionDataAccessDto>>> GetByTemplateVersionsByTemplateIdAsync(int templateId)
        {
            try
            {
                // Query TemplateVersions, filter by TemplateId AND where IsDeleted is false.
                List<TemplateVersion> templateVersions = await context.TemplateVersions
                    .Where(tv => tv.TemplateId == templateId && !tv.IsDeleted)
                    .OrderByDescending(tv => tv.VersionNumber) // Order by version number (optional but useful)
                    .ToListAsync();

                // Map the list of TemplateVersion entities to DTOs.
                List<TemplateVersionDataAccessDto> dtoList = mapper.Map<List<TemplateVersionDataAccessDto>>(templateVersions);

                return Result<List<TemplateVersionDataAccessDto>>.Success(dtoList); // Return success with the DTO list.
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in TemplateVersionRepository.GetByTemplateVersionsByTemplateIdAsync: {ex.Message}"); // Log error
                return Result<List<TemplateVersionDataAccessDto>>.Failure(ErrorMessageUserConst.ServerErrorNoMsg); // Generic error
            }
        }

        // New method implementation for soft deleting a version.
        public async Task<Result<bool>> SoftDeleteVersionAsync(int versionId)
        {
            // Find the template version by ID.
            TemplateVersion? versionToDelete = await context.TemplateVersions
                                                   .Include(tv => tv.Template) // Include the parent template to check its versions
                                                   .FirstOrDefaultAsync(tv => tv.Id == versionId);

            if (versionToDelete == null)
            {
                // Version not found.
                return Result<bool>.Failure($"Template version with ID {versionId} not found."); // More specific error message
            }

            if (versionToDelete.IsDeleted)
            {
                 // Already deleted.
                 return Result<bool>.Failure(ErrorMessageUserConst.VersionAlreadyDeleted);
            }

            // Check if this version is the current Testing or Production version for its template.
            if (versionToDelete.Template != null) // Ensure Template was loaded
            {
                if (versionToDelete.VersionNumber == versionToDelete.Template.TestingVersion ||
                   (versionToDelete.Template.ProductionVersion.HasValue && versionToDelete.VersionNumber == versionToDelete.Template.ProductionVersion.Value))
                {
                    // It is a currently referenced version. Prevent deletion.
                    return Result<bool>.Failure(ErrorMessageUserConst.CannotDeleteCurrentVersion);
                }
            }
            // If Template wasn't loaded, or if it's not a currently referenced version, proceed.

            // Mark the version as deleted.
            versionToDelete.IsDeleted = true;
            versionToDelete.DeletedDate = DateTime.Now; // Set deletion timestamp.

            // The entity is now tracked by the context with its state modified.
            // DbSet.Update(versionToDelete); // Not strictly needed if entity was tracked and modified.

            // Note: SaveChangesAsync() is expected to be called by UnitOfWork.

            return Result<bool>.Success(true); // Return success.
        }

        // New method implementation to find a specific version by template ID and version number.
        // Returns the entity or null. Useful for validation before revert/delete.
        public async Task<TemplateVersion?> FindVersionAsync(int templateId, int versionNumber)
        {
             // Find the version based on TemplateId and VersionNumber.
             return await context.TemplateVersions
                         .Include(tv => tv.Template) // Include parent template to check references
                         .SingleOrDefaultAsync(tv => tv.TemplateId == templateId && tv.VersionNumber == versionNumber);
        }

        // New method implementation to get the Template entity by ID.
        public async Task<Template?> GetTemplateByIdAsync(int templateId)
        {
             return await context.Templates
                        .Include(t => t.Versions) // Include versions if needed for related checks elsewhere
                        .FirstOrDefaultAsync(t => t.Id == templateId);
        }
    }
}
```

---

**14. `PDFGenerator.Infrastructure\DataSeeding\DataSeedingExtensions.cs`**
(Modified to update initial template seeding - optional but good practice)

```csharp
﻿using Microsoft.Extensions.DependencyInjection;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using PdfGeneratorApp.Data;
using Microsoft.Extensions.Hosting;
using Microsoft.AspNetCore.Identity;
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Models;
using System.Threading.Tasks; // Needed for Task
using System.Collections.Generic; // Needed for List

namespace PDFGenerator.Infrastructure.DataSeeding
{
    public static class DataSeedingExtensions
    {
        public static async Task MigrateDatabaseAndSeedAsync(this IHost host)
        {
            using (var scope = host.Services.CreateScope())
            {
                var services = scope.ServiceProvider;
                try
                {
                    var context = services.GetRequiredService<ApplicationDbContext>();
                    await context.Database.MigrateAsync();

                    var dbContext = scope.ServiceProvider.GetService<ApplicationDbContext>();
                    var roleManager = scope.ServiceProvider.GetService<RoleManager<IdentityRole>>();
                    var userManager = scope.ServiceProvider.GetService<UserManager<User>>();
                    var signInMAnager = scope.ServiceProvider.GetService<SignInManager<User>>(); // Still unused

                    // This synchronous call is likely redundant after MigrateAsync() above.
                    // dbContext.Database.Migrate();

                    // Use AnyAsync for checking if data exists.
                    if (!await dbContext.Users.AnyAsync())
                        await SeedUsers(roleManager, userManager);

                    if (!await dbContext.Roles.AnyAsync())
                        await SeedRoles(roleManager);

                    // Add initial template seeding if needed
                    // if (!await dbContext.Templates.AnyAsync())
                    // {
                    //    // Example seeding logic for templates
                    //    var initialTemplate = new Template
                    //    {
                    //        Name = "ExampleTemplate",
                    //        TestingVersion = 1,
                    //        ProductionVersion = 1,
                    //        LastModified = DateTime.Now,
                    //        Versions = new List<TemplateVersion>
                    //        {
                    //            new TemplateVersion
                    //            {
                    //                VersionNumber = 1,
                    //                HtmlContent = "<p>Hello <<Name>>!</p>",
                    //                Description = "Initial Version",
                    //                CreatedDate = DateTime.Now,
                    //                IsDeleted = false
                    //            }
                    //        }
                    //    };
                    //    await dbContext.Templates.AddAsync(initialTemplate);
                    // }

                    // Save changes *after* checking/adding data with DbContext directly (if any).
                    // Identity Manager methods already save changes internally.
                    // await dbContext.SaveChangesAsync(); // Might not be needed if only using UserManager/RoleManager for seeding.

                }
                catch (Exception ex)
                {
                    // Improved logging
                    var logger = services.GetRequiredService<ILogger<DataSeedingExtensions>>();
                    logger.LogError(ex, "An error occurred while migrating or seeding the database.");
                    throw; // Re-throw the exception.
                }
            }
        }

        private async static Task SeedRoles(RoleManager<IdentityRole> roleManager)
        {
            List<string> roles = new List<string>() {
             RoleEnum.Admin,
             RoleEnum.System
            };
            foreach (var role in roles)
            {
                // Check if role already exists before creating
                if (!await roleManager.RoleExistsAsync(role))
                {
                    IdentityRole identityRole = new IdentityRole() { Name = role };
                    await roleManager.CreateAsync(identityRole);
                }
            }
        }
        private async static Task SeedUsers(RoleManager<IdentityRole> roleManager, UserManager<User> userManager)
        {
            // Create master user only if they don't already exist
            var masterUserEmail = "Admin@gmail.com";
            var masterUser = await userManager.FindByEmailAsync(masterUserEmail);

            if (masterUser == null)
            {
                masterUser = new User()
                {
                    UserName = masterUserEmail, // Often same as email for login.
                    DisplayName = "Admin",
                    Email = masterUserEmail,
                    EmailConfirmed = true // Assume email is confirmed for seeded users.
                };

                IdentityResult masterUserResult = await userManager.CreateAsync(masterUser, "AaBb_@123");
                if (!masterUserResult.Succeeded)
                {
                    var errors = string.Join(", ", masterUserResult.Errors.Select(e => e.Description));
                    throw new Exception($"Failed to create master user: {errors}");
                }
            }

            // Ensure roles exist before adding user to roles (SeedRoles should run first, but this adds robustness)
            if (!await roleManager.RoleExistsAsync(RoleEnum.Admin)) await RoleManagerExtensions.CreateAsync(roleManager, new IdentityRole(RoleEnum.Admin));
            if (!await roleManager.RoleExistsAsync(RoleEnum.System)) await RoleManagerExtensions.CreateAsync(roleManager, new IdentityRole(RoleEnum.System));


            // Add user to roles if they aren't already in them
            if (!await userManager.IsInRoleAsync(masterUser, RoleEnum.Admin))
            {
                 IdentityResult adminRoleResult = await userManager.AddToRoleAsync(masterUser, RoleEnum.Admin);
                 if (!adminRoleResult.Succeeded)
                 {
                     var errors = string.Join(", ", adminRoleResult.Errors.Select(e => e.Description));
                     throw new Exception($"Failed to add master user to Admin role: {errors}");
                 }
            }

            if (!await userManager.IsInRoleAsync(masterUser, RoleEnum.System))
            {
                 IdentityResult systemRoleResult = await userManager.AddToRoleAsync(masterUser, RoleEnum.System);
                 if (!systemRoleResult.Succeeded)
                 {
                     var errors = string.Join(", ", systemRoleResult.Errors.Select(e => e.Description));
                     throw new Exception($"Failed to add master user to System role: {errors}");
                 }
            }
        }
    }
}
```

---

**15. `PDFGenerator.Infrastructure\DataAccess\Repositories\Implementation\UnitOfWork.cs`**
(No change needed in UnitOfWork itself, as it relies on the repository interfaces.)

---

**16. `PDFGenerator.Web\Dtos\Template\TemplateRevertRequestDto.cs`**
(Modified to add VersionReferenceType)

```csharp
namespace PDFGenerator.Web.Dtos.Template
{
    public class TemplateRevertRequestDto
    {
        public string TemplateName { get; set; }
        public int VersionNumber { get; set; }
        // New property to specify which reference (Testing or Production) to revert
        public string VersionReferenceType { get; set; }
    }
}
```

---

**17. `PDFGenerator.Web\Extensions\ServiceCollectionExtensions.cs`**
(Modified to register new handlers)

```csharp
﻿using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using PDFGenerator.Web.Handlers;
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Handlers;
using System.Text;
using Microsoft.AspNetCore.Http; // Needed for IHttpContextAccessor

namespace PDFGenerator.Web.Extensions
{
    public static class ServiceCollectionExtensions
    {
        public static IServiceCollection AddServices(this IServiceCollection services)
        {
             // Register IHttpContextAccessor as it's needed by ForgotPasswordHandler for URL generation.
             services.AddHttpContextAccessor();

            return services.AddScoped<IGetTemplatesDocHandler, GetTemplatesDocHandler>()
            .AddScoped<IGetTemplatesListHandler, GetTemplatesListHandler>()
            .AddScoped<IGetTemplateByNameHandler, GetTemplateByNameHandler>()
            .AddScoped<IGeneratePdfHandler, GeneratePdfHandler>()
            .AddScoped<IGetTemplateDesignHandler, GetTemplateDesignHandler>()
            .AddScoped<IUpdateTemplateHandler, UpdateTemplateHandler>()
            .AddScoped<ICreateTemplateHandler, CreateTemplateHandler>()
            .AddScoped<IGetTemplateHistoryHandler, GetTemplateHistoryHandler>()
            .AddScoped<IRevertTemplateHandler, RevertTemplateHandler>()
            .AddScoped<ILoginUserHandler, LoginUserHandler>()
            .AddScoped<IGetUserInfoByEmailHandler, GetUserInfoByEmailHandler>()
            .AddScoped<IForgotPasswordHandler, ForgotPasswordHandler>()
            .AddScoped<IResetPasswordHandler, ResetPasswordHandler>()
            // Register new handlers
            .AddScoped<IPublishTemplateHandler, PublishTemplateHandler>()
            .AddScoped<ISoftDeleteTemplateVersionHandler, SoftDeleteTemplateVersionHandler>();
        }

        public static void AddAuthenticationWithJwtBearer(this IServiceCollection services, IConfiguration configuration)
        {
            services.Configure<JWT>(configuration.GetSection("JWT"));

            services.AddAuthentication(options =>
            {
                options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
                options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
            })
            .AddJwtBearer(o =>
            {
                o.RequireHttpsMetadata = false;
                o.SaveToken = false;
                o.TokenValidationParameters = new TokenValidationParameters
                {
                    ValidateIssuerSigningKey = true,
                    ValidateIssuer = true,
                    ValidateAudience = true,
                    ValidateLifetime = true,
                    ValidIssuer = configuration["JWT:Issuer"],
                    ValidAudience = configuration["JWT:Audience"],
                    IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(configuration["JWT:Key"])),
                    ClockSkew = TimeSpan.Zero
                };

                o.Events = new JwtBearerEvents
                {
                    OnChallenge = context =>
                    {
                        context.HandleResponse();
                        context.Response.Redirect("/Account/Login"); // Use attribute route path

                        return Task.CompletedTask;
                    }
                };
            });
        }

    }
}


public class JwtCookieMiddleware
{
    private readonly RequestDelegate _next;

    public JwtCookieMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        if (context.Request.Cookies.ContainsKey("authToken"))
        {
            var token = context.Request.Cookies["authToken"];

            if (!string.IsNullOrEmpty(token) && !context.Request.Headers.ContainsKey("Authorization"))
            {
                context.Request.Headers.Add("Authorization", $"Bearer {token}");
            }
        }

        await _next(context);
    }
}
```

---

**18. `PDFGenerator.Web\MappingProfile\ApplicationLayerMappingProfile.cs`**
(Modified to update mappings for new/renamed properties)

```csharp
using AutoMapper;
using PDFGenerator.Web.Dtos.Template;
using PDFGenerator.Web.Dtos.TemplateVersion;
using PDFGenerator.Infrastructure.DataAccess.Dtos;
using PDFGenerator.Web.Dtos.Auth;
using PdfGeneratorApp.Models; // Include domain models if mapping directly (optional, but sometimes done)

namespace PdfGeneratorApp.Infrastructure.Mapping
{
    public class ApplicationLayerMappingProfile : Profile
    {
        public ApplicationLayerMappingProfile()
        {
            // Map TemplateSimpleDto (Web) from/to TemplateSimpleDto (DataAccess) - properties match
            CreateMap<TemplateSimpleDto, TemplateSimpleDto>().ReverseMap();

            // Map TemplateListDto (Web) from TemplateSimpleDto (DataAccess)
            CreateMap<TemplateSimpleDto, TemplateListDto>()
                 .ForMember(dest => dest.Id, opt => opt.MapFrom(src => src.Id))
                 .ForMember(dest => dest.Name, opt => opt.MapFrom(src => src.Name))
                 // Description is in TemplateListDto but not TemplateSimpleDto. Handle mapping explicitly or ignore.
                 // Assuming Description in TemplateListDto should come from Template model's Description.
                 // However, GetAllTemplateSimplAsync returns TemplateSimpleDto, which doesn't have Description.
                 // This might indicate TemplateListDto should map from Template model directly, or update TemplateSimpleDto.
                 // Let's assume Description in TemplateListDto is *not* populated by GetAllTemplateSimplAsync for now.
                 .ForMember(dest => dest.Description, opt => opt.Ignore()) // Or MapFrom Template model if needed elsewhere
                 .ForMember(dest => dest.TestingVersion, opt => opt.MapFrom(src => src.TestingVersion))
                 .ForMember(dest => dest.ProductionVersion, opt => opt.MapFrom(src => src.ProductionVersion))
                 .ForMember(dest => dest.LastModified, opt => opt.MapFrom(src => src.LastModified));


            // Map TemplateDetailDto (Web) from/to TemplateDataAccessDto (DataAccess) - properties match
            CreateMap<TemplateDetailDto, TemplateDataAccessDto>().ReverseMap();

            // Map TemplateCreateDto (Web) from/to TemplateDataAccessDto (DataAccess) - properties match (InternalDataConfigJson added)
            CreateMap<TemplateCreateDto, TemplateDataAccessDto>().ReverseMap();

            // Map TemplateUpdateDto (Web) from/to TemplateDataAccessDto (DataAccess) - properties match (InternalDataConfigJson added)
            CreateMap<TemplateUpdateDto, TemplateDataAccessDto>().ReverseMap();

            // Map TemplateVersionDto (Web) from/to TemplateVersionDataAccessDto (DataAccess)
            // Ensure soft delete properties are mapped
            CreateMap<TemplateVersionDto, TemplateVersionDataAccessDto>().ReverseMap();

            // Map TemplatesDocDto (Web) from/to TemplatesDocDataAccessDto (DataAccess) - properties match
            // Ensure version properties are mapped
            CreateMap<TemplatesDocDto, TemplatesDocDataAccessDto>().ReverseMap();

            // Map AccountDto (Web) from/to AccountDataAccessDto (DataAccess)
            CreateMap<AccountDto, AccountDataAccessDto>().ReverseMap();

            // Map UserDto (Web) from User (Model)
            CreateMap<User, UserDto>(); // Added explicit User -> UserDto mapping for GetUserInfoByEmailHandler
        }
    }
}
```

---

**19. `PDFGenerator.Web\Services\PublishTemplateHandler.cs`**
(New file for Publish Handler)

```csharp
// File: Handlers/PublishTemplateHandler.cs
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Handlers;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using System.Threading.Tasks; // Needed for Task

namespace PDFGenerator.Web.Handlers // Put Auth/Web handlers in this namespace for consistency
{
    // Interface for the Publish Template handler.
    // Request is string (template name), Response data is int (the new production version number).
    public interface IPublishTemplateHandler : IHandler<string, int>
    {
    }

    // Concrete implementation of IPublishTemplateHandler.
    public class PublishTemplateHandler : IPublishTemplateHandler
    {
        private readonly IUnitOfWork _unitOfWork;

        public PublishTemplateHandler(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }

        // Handles the request to publish the current testing version to production.
        public async Task<Result<int>> HandleAsync(string templateName) // 'templateName' from controller.
        {
            try
            {
                // Call the repository method to perform the publish logic.
                var publishResult = await _unitOfWork.Templates.PublishTemplateAsync(templateName);

                if (!publishResult.IsCompleteSuccessfully) // If repository operation failed (e.g., template not found).
                {
                    return Result<int>.Failure(publishResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                // Save changes to the database.
                var saveResult = await _unitOfWork.SaveAsync();
                if (!saveResult.IsCompleteSuccessfully) // If saving failed.
                {
                    return Result<int>.Failure(saveResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                // Return success with the new Production version number.
                return Result<int>.Success(publishResult.Data); // publishResult.Data is the new production version number.
            }
            catch (Exception ex) // Catch unexpected exceptions.
            {
                Console.WriteLine($"Error in PublishTemplateHandler: {ex.Message}"); // Log error.
                return Result<int>.Failure(ErrorMessageUserConst.ServerErrorNoMsg); // Return generic server error.
            }
        }
    }
}
```

---

**20. `PDFGenerator.Web\Services\SoftDeleteTemplateVersionHandler.cs`**
(New file for Soft Delete Handler)

```csharp
// File: Handlers/SoftDeleteTemplateVersionHandler.cs
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Handlers;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using System.Threading.Tasks; // Needed for Task

namespace PDFGenerator.Web.Handlers // Put Auth/Web handlers in this namespace for consistency
{
    // Interface for the Soft Delete Template Version handler.
    // Request is int (version ID), Response data is bool (success/failure).
    public interface ISoftDeleteTemplateVersionHandler : IHandler<int, bool>
    {
    }

    // Concrete implementation of ISoftDeleteTemplateVersionHandler.
    public class SoftDeleteTemplateVersionHandler : ISoftDeleteTemplateVersionHandler
    {
        private readonly IUnitOfWork _unitOfWork;

        public SoftDeleteTemplateVersionHandler(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }

        // Handles the request to soft delete a template version.
        public async Task<Result<bool>> HandleAsync(int versionId) // 'versionId' from controller.
        {
            try
            {
                // Call the repository method to perform the soft delete logic.
                var deleteResult = await _unitOfWork.TemplateVersions.SoftDeleteVersionAsync(versionId);

                if (!deleteResult.IsCompleteSuccessfully) // If repository operation failed (e.g., version not found, cannot delete current version).
                {
                    return deleteResult; // Return the failure result directly from the repository (containing specific error message).
                }

                // Save changes to the database.
                var saveResult = await _unitOfWork.SaveAsync();
                if (!saveResult.IsCompleteSuccessfully) // If saving failed.
                {
                    return Result<bool>.Failure(saveResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                return Result<bool>.Success(true); // Return success.
            }
            catch (Exception ex) // Catch unexpected exceptions.
            {
                Console.WriteLine($"Error in SoftDeleteTemplateVersionHandler: {ex.Message}"); // Log error.
                return Result<bool>.Failure(ErrorMessageUserConst.ServerErrorNoMsg); // Return generic server error.
            }
        }
    }
}
```

---

**21. `PDFGenerator.Web\Services\GetTemplateByNameHandler.cs`**
(Updated to use `TestingVersion` and `ProductionVersion` from the fetched `TemplateDataAccessDto`)

```csharp
// File: Handlers/GetTemplateByNameHandler.cs
using PdfGeneratorApp.Common;
using AutoMapper;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using PDFGenerator.Web.Dtos.Template;


namespace PdfGeneratorApp.Handlers
{
    public interface IGetTemplateByNameHandler : IHandler<string, TemplateDetailDto>
    {
    }

    public class GetTemplateByNameHandler : IGetTemplateByNameHandler
    {
        private readonly IUnitOfWork _unitOfWork;
        private readonly IMapper _mapper;

        public GetTemplateByNameHandler(IUnitOfWork unitOfWork, IMapper mapper)
        {
            _unitOfWork = unitOfWork;
            _mapper = mapper;
        }

        public async Task<Result<TemplateDetailDto>> HandleAsync(string templateName)
        {
            try
            {
                // Repository method now fetches TemplateDataAccessDto including Testing/Production versions
                // and includes content from the TestingVersion.
                var repoResult = await _unitOfWork.Templates.GetByNameAsync(templateName);

                if (!repoResult.IsCompleteSuccessfully)
                {
                    return Result<TemplateDetailDto>.Failure(repoResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                // Check if template was found (Data is null on failure)
                if (repoResult.Data == null)
                {
                    return Result<TemplateDetailDto>.Failure(ErrorMessageUserConst.TemplateNotFound);
                }

                // Map the DataAccess DTO (now containing all necessary fields including both versions)
                // to the Web DTO. The mapping profile handles the property names.
                var templateDto = _mapper.Map<TemplateDetailDto>(repoResult.Data);

                return Result<TemplateDetailDto>.Success(templateDto);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in GetTemplateByNameHandler: {ex.Message}");
                return Result<TemplateDetailDto>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }
    }
}
```

---

**22. `PDFGenerator.Web\Services\GetTemplateDesignHandler.cs`**
(Updated to use `TestingVersion` and `ProductionVersion` from the fetched `TemplateDetailDto`)

```csharp
// File: Handlers/GetTemplateDesignHandler.cs
using PdfGeneratorApp.Common;
using System.Threading.Tasks;
using System;
using AutoMapper;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using PDFGenerator.Web.Dtos.Template;


namespace PdfGeneratorApp.Handlers
{
    public interface IGetTemplateDesignHandler : IHandler<string, TemplateDetailDto>
    {
    }

    public class GetTemplateDesignHandler : IGetTemplateDesignHandler
    {
        private readonly IUnitOfWork _unitOfWork;
        private readonly IMapper _mapper;

        public GetTemplateDesignHandler(IUnitOfWork unitOfWork, IMapper mapper)
        {
            _unitOfWork = unitOfWork;
            _mapper = mapper;
        }

        public async Task<Result<TemplateDetailDto>> HandleAsync(string templateName)
        {
            try
            {
                // Use the repository via Unit of Work to get TemplateDataAccessDto
                // This DTO will now include TestingVersion and ProductionVersion,
                // and the content will be fetched based on TestingVersion by the repo.
                var repoResult = await _unitOfWork.Templates.GetByNameAsync(templateName);

                if (!repoResult.IsCompleteSuccessfully)
                {
                    return Result<TemplateDetailDto>.Failure(repoResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                 // Check if template was found (Data is null on failure)
                if (repoResult.Data == null)
                {
                    return Result<TemplateDetailDto>.Failure(ErrorMessageUserConst.TemplateNotFound);
                }

                // Map the Data Access DTO (which has Testing/Production versions)
                // to an Application DTO. The mapping profile handles this.
                var templateDto = _mapper.Map<TemplateDetailDto>(repoResult.Data);

                return Result<TemplateDetailDto>.Success(templateDto);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in GetTemplateDesignHandler: {ex.Message}");
                return Result<TemplateDetailDto>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }
    }
}
```

---

**23. `PDFGenerator.Web\Services\GetTemplateHistoryHandler.cs`**
(Updated to return DTOs with soft delete properties)

```csharp
// File: Handlers/GetTemplateHistoryHandler.cs
using PdfGeneratorApp.Common;
using AutoMapper;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using PDFGenerator.Web.Dtos.TemplateVersion;
using System.Collections.Generic; // Needed for List<T>
using System.Threading.Tasks; // Needed for Task


namespace PdfGeneratorApp.Handlers
{
    public interface IGetTemplateHistoryHandler : IHandler<int, List<TemplateVersionDto>>
    {
    }

    public class GetTemplateHistoryHandler : IGetTemplateHistoryHandler
    {
        private readonly IUnitOfWork _unitOfWork;
        private readonly IMapper _mapper;

        public GetTemplateHistoryHandler(IUnitOfWork unitOfWork, IMapper mapper)
        {
            _unitOfWork = unitOfWork;
            _mapper = mapper;
        }

        // Handles the request to get template version history.
        // Note: Repository now returns only NON-DELETED versions.
        public async Task<Result<List<TemplateVersionDto>>> HandleAsync(int templateId)
        {
            try
            {
                // Repository method now includes filtering for IsDeleted=false.
                var getTemplateResult = await _unitOfWork.TemplateVersions.GetByTemplateVersionsByTemplateIdAsync(templateId);

                // If repository failed (Data is null/empty List on success)
                if (!getTemplateResult.IsCompleteSuccessfully) return Result<List<TemplateVersionDto>>.Failure(getTemplateResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);

                // Map the list of DataAccess DTOs (which now include IsDeleted/DeletedDate)
                // to Web DTOs. The mapping profile handles this.
                var versionDtos = _mapper.Map<List<TemplateVersionDto>>(getTemplateResult.Data);

                return Result<List<TemplateVersionDto>>.Success(versionDtos); // Returns the list of NON-DELETED versions.
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in GetTemplateHistoryHandler: {ex.Message}");
                return Result<List<TemplateVersionDto>>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }
    }
}
```

---

**24. `PDFGenerator.Web\Services\GetTemplatesDocHandler.cs`**
(Updated to use `TestingVersion` and `ProductionVersion` from the fetched `TemplatesDocDto`)

```csharp
// File: Handlers/GetTemplatesDocHandler.cs
using PdfGeneratorApp.Common;
using AutoMapper;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using PDFGenerator.Web.Dtos.Template;
using System.Collections.Generic; // Needed for List<T>
using System.Threading.Tasks; // Needed for Task

namespace PdfGeneratorApp.Handlers
{
    public interface IGetTemplatesDocHandler : IHandler<object, List<TemplatesDocDto>>
    {
    }

    public class GetTemplatesDocHandler : IGetTemplatesDocHandler
    {
        private readonly IUnitOfWork _unitOfWork;
        private readonly IMapper _mapper;

        public GetTemplatesDocHandler(IUnitOfWork unitOfWork, IMapper mapper)
        {
            _unitOfWork = unitOfWork;
            _mapper = mapper;
        }

        public async Task<Result<List<TemplatesDocDto>>> HandleAsync(object request)
        {
            try
            {
                // Repository method fetches data including Testing/Production versions
                // and content from the Testing version.
                var repoResult = await _unitOfWork.Templates.GetAllAsync();

                if (!repoResult.IsCompleteSuccessfully) return Result<List<TemplatesDocDto>>.Failure(repoResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);

                // Map the list of DataAccess DTOs (which have version info)
                // to Web DTOs. The mapping profile handles this.
                var templatesForDocs = _mapper.Map<List<TemplatesDocDto>>(repoResult.Data);

                return Result<List<TemplatesDocDto>>.Success(templatesForDocs);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in GetTemplatesDocHandler: {ex.Message}"); // Log error
                return Result<List<TemplatesDocDto>>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }
    }
}
```

---

**25. `PDFGenerator.Web\Services\GetTemplatesListHandler.cs`**
(Updated to use `TestingVersion` and `ProductionVersion` from the fetched `TemplateListDto`)

```csharp
// File: Handlers/GetTemplatesListHandler.cs
using PdfGeneratorApp.Common;
using AutoMapper;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using PDFGenerator.Web.Dtos.Template;
using System.Collections.Generic; // Needed for List<T>
using System.Threading.Tasks; // Needed for Task

namespace PdfGeneratorApp.Handlers
{
    public interface IGetTemplatesListHandler : IHandler<object, List<TemplateListDto>>
    {
    }

    public class GetTemplatesListHandler : IGetTemplatesListHandler
    {
        private readonly IUnitOfWork _unitOfWork;
        private readonly IMapper _mapper;

        public GetTemplatesListHandler(IUnitOfWork unitOfWork, IMapper mapper)
        {
            _unitOfWork = unitOfWork;
            _mapper = mapper;
        }

        public async Task<Result<List<TemplateListDto>>> HandleAsync(object request)
        {
            try
            {
                // Repository method fetches simple template data including Testing/Production versions.
                var repoResult = await _unitOfWork.Templates.GetAllTemplateSimplAsync();

                if (!repoResult.IsCompleteSuccessfully) return Result<List<TemplateListDto>>.Failure(repoResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);

                // Map the list of DataAccess DTOs (TemplateSimpleDto with version info)
                // to Web DTOs (TemplateListDto). The mapping profile handles this.
                var templates = _mapper.Map<List<TemplateListDto>>(repoResult.Data);

                return Result<List<TemplateListDto>>.Success(templates);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in GetTemplatesListHandler: {ex.Message}"); // Log error
                return Result<List<TemplateListDto>>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }
    }
}
```

---

**26. `PDFGenerator.Web\Services\RevertTemplateHandler.cs`**
(Modified to handle the new request DTO with VersionReferenceType)

```csharp
// File: Handlers/RevertTemplateHandler.cs
using PdfGeneratorApp.Common;
using AutoMapper; // Still not used, can remove if desired
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using PDFGenerator.Web.Dtos.Template;
using System.Threading.Tasks; // Needed for Task


namespace PdfGeneratorApp.Handlers
{
    // Interface modified to use the updated request DTO.
    // Response data is int (the version number it was reverted to).
    public interface IRevertTemplateHandler : IHandler<TemplateRevertRequestDto, int>
    {
    }

    public class RevertTemplateHandler : IRevertTemplateHandler
    {
        private readonly IUnitOfWork _unitOfWork;

        public RevertTemplateHandler(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }

        // Handles the request to revert a template to a specific version for a specific reference type.
        public async Task<Result<int>> HandleAsync(TemplateRevertRequestDto request) // 'request' includes TemplateName, VersionNumber, VersionReferenceType.
        {
            try
            {
                // Optional: Basic validation for VersionReferenceType
                if (!VersionReferenceType.IsValid(request.VersionReferenceType))
                {
                    return Result<int>.Failure(ErrorMessageUserConst.InvalidVersionReferenceType);
                }

                // Call the repository method with the updated signature.
                var revertOpResult = await _unitOfWork.Templates.RevertTemplateAsync(
                    request.TemplateName,
                    request.VersionNumber,
                    request.VersionReferenceType
                );

                // If repository operation failed (e.g., template/version not found, cannot revert deleted/future version).
                if (!revertOpResult.IsCompleteSuccessfully)
                {
                    return Result<int>.Failure(revertOpResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg, default(int));
                }

                // Save changes to the database.
                var saveResult = await _unitOfWork.SaveAsync();

                if (!saveResult.IsCompleteSuccessfully)
                {
                    return Result<int>.Failure(saveResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                // Return success with the version number it was reverted to.
                return Result<int>.Success(revertOpResult.Data);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in RevertTemplateHandler: {ex.Message}"); // Log error
                return Result<int>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }
    }
}
```

---

**27. `PDFGenerator.Web\Services\UpdateTemplateHandler.cs`**
(Updated return type comment and logic to use repo result)

```csharp
// File: Handlers/UpdateTemplateHandler.cs
using AutoMapper;
using PDFGenerator.Infrastructure.DataAccess.Dtos;
using PDFGenerator.Web.Dtos.Template;
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using PdfGeneratorApp.Services; // Not directly used here
using System.Text.Json; // Not directly used here
using System.Threading.Tasks; // Needed for Task


namespace PdfGeneratorApp.Handlers
{
    // Interface remains the same, it returns the new TestingVersion number.
    public interface IUpdateTemplateHandler : IHandler<TemplateUpdateDto, int>
    {
    }

    public class UpdateTemplateHandler : IUpdateTemplateHandler
    {
        private readonly IUnitOfWork _unitOfWork;
        private readonly IMapper _mapper; // Used for mapping DTOs

        public UpdateTemplateHandler(IUnitOfWork unitOfWork, IMapper mapper)
        {
            _unitOfWork = unitOfWork;
            _mapper = mapper;
        }

        // Handles the request to update a template (creates a new Testing version).
        public async Task<Result<int>> HandleAsync(TemplateUpdateDto templateDto)
        {
            try
            {
                // Map the input Web DTO to DataAccess DTO.
                // The mapping profile includes the new/renamed version properties,
                // but the input UpdateDto doesn't have them, so they will be default (0/null).
                // This is fine as the repository determines the new version number.
                var templateDataAccessDto = _mapper.Map<TemplateDataAccessDto>(templateDto);

                // Call the repository method to create a new Testing version.
                // This method returns the updated TemplateDataAccessDto including the new TestingVersion.
                var updateOpResult = await _unitOfWork.Templates.UpdateTemplateAsync(templateDataAccessDto);

                // If repository operation failed.
                if (!updateOpResult.IsCompleteSuccessfully)
                {
                    return Result<int>.Failure(updateOpResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg, default(int));
                }

                // Save changes to the database.
                var saveResult = await _unitOfWork.SaveAsync();
                if (!saveResult.IsCompleteSuccessfully)
                {
                    return Result<int>.Failure(saveResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                // Return success with the new Testing version number, obtained from the repository result.
                return Result<int>.Success(updateOpResult.Data.TestingVersion);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in UpdateTemplateHandler: {ex.Message}"); // Log error
                return Result<int>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }
    }
}
```

---

**28. `PDFGenerator.Web\Controllers\TemplateController.cs`**
(Modified to add Publish and Soft Delete actions, and update Revert)

```csharp
// File: Controllers/TemplateController.cs
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore; // Still referenced, but direct use is minimized
using PDFGenerator.Web.Dtos.Template;
using PDFGenerator.Web.Dtos.TemplateVersion;
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Data; // Still referenced
using PdfGeneratorApp.Handlers;
using PDFGenerator.Web.Handlers; // For new handlers


namespace PdfGeneratorApp.Controllers
{
    [Authorize] // All actions require authentication.
    public class TemplateController : Controller
    {
        // Keep direct DbContext and Configuration if needed elsewhere (e.g., GetDatabaseAliases)
        private readonly ApplicationDbContext _context;
        private readonly IConfiguration _configuration;

        // Injected handlers (updated to include new ones)
        private readonly IGetTemplateDesignHandler _getTemplateDesignHandler;
        private readonly IUpdateTemplateHandler _updateTemplateHandler;
        private readonly ICreateTemplateHandler _createTemplateHandler;
        private readonly IGetTemplateHistoryHandler _getTemplateHistoryHandler;
        private readonly IRevertTemplateHandler _revertTemplateHandler;
        private readonly IPublishTemplateHandler _publishTemplateHandler; // New handler
        private readonly ISoftDeleteTemplateVersionHandler _softDeleteTemplateVersionHandler; // New handler


        // Updated constructor for dependency injection
        public TemplateController(ApplicationDbContext context, IConfiguration configuration,
                                  IGetTemplateDesignHandler getTemplateDesignHandler,
                                  IUpdateTemplateHandler updateTemplateHandler,
                                  ICreateTemplateHandler createTemplateHandler,
                                  IGetTemplateHistoryHandler getTemplateHistoryHandler,
                                  IRevertTemplateHandler revertTemplateHandler,
                                  IPublishTemplateHandler publishTemplateHandler, // Inject new handler
                                  ISoftDeleteTemplateVersionHandler softDeleteTemplateVersionHandler) // Inject new handler
        {
            _context = context;
            _configuration = configuration;
            _getTemplateDesignHandler = getTemplateDesignHandler;
            _updateTemplateHandler = updateTemplateHandler;
            _createTemplateHandler = createTemplateHandler;
            _getTemplateHistoryHandler = getTemplateHistoryHandler;
            _revertTemplateHandler = revertTemplateHandler;
            _publishTemplateHandler = publishTemplateHandler; // Assign new handler
            _softDeleteTemplateVersionHandler = softDeleteTemplateVersionHandler; // Assign new handler
        }

        // Helper method to get database aliases from configuration.
        private List<string> GetDatabaseAliases()
        {
            return _configuration.GetSection("InternalDataConnections").GetChildren().Select(c => c.Key).ToList();
        }

        // GET: /templates/design/{templateName}
        // Model (TemplateDetailDto) now includes TestingVersion and ProductionVersion.
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
        // Updates the template (creates a new Testing version).
        [HttpPost("templates/design/{templateName}")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Design(string templateName, [Bind("Id,Description,HtmlContent,ExampleJsonData,InternalDataConfigJson")] TemplateUpdateDto templateDto)
        {
            // Need to refetch full model for view on error, similar to before.
             Result<TemplateDetailDto> detailDtoOnError = await _getTemplateDesignHandler.HandleAsync(templateName);
             // Check if fetching original details succeeded before trying to modify.
             if (detailDtoOnError.IsCompleteSuccessfully && detailDtoOnError.Data != null)
             {
                 detailDtoOnError.Data.Description = templateDto.Description;
                 detailDtoOnError.Data.HtmlContent = templateDto.HtmlContent;
                 detailDtoOnError.Data.ExampleJsonData = templateDto.ExampleJsonData;
                 detailDtoOnError.Data.InternalDataConfigJson = templateDto.InternalDataConfigJson;
             }
             else // If original details couldn't be fetched (e.g., template deleted between GET and POST)
             {
                 // Handle this appropriately - maybe redirect or show a critical error.
                 // For simplicity, we'll proceed, but the handler call will likely fail too.
             }
             ViewBag.DatabaseAliases = GetDatabaseAliases();

            if (!ModelState.IsValid) return View(detailDtoOnError.Data); // Return view with validation errors.

            // Call handler to update the template (creates new Testing version).
            // The handler returns the new TestingVersion number.
            var result = await _updateTemplateHandler.HandleAsync(templateDto);

            if (!result.IsCompleteSuccessfully)
            {
                ModelState.AddModelError("", result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                return View(detailDtoOnError.Data); // Return view with handler errors.
            }

            // If successful, set a success message and redirect back to the Design page.
            // The new version number is in result.Data.
            TempData["Message"] = $"Template '{templateName}' updated. New Testing Version is {result.Data}.";
            return RedirectToAction(nameof(Design), new { templateName = templateName });
        }

        // GET: /templates/create
        public IActionResult Create()
        {
            ViewBag.DatabaseAliases = GetDatabaseAliases();
            return View(new TemplateCreateDto { HtmlContent = "" });
        }

        // POST: /templates/create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create([Bind("Name,HtmlContent,Description,ExampleJsonData,InternalDataConfigJson")] TemplateCreateDto templateDto)
        {
            if (!ModelState.IsValid)
            {
                ViewBag.DatabaseAliases = GetDatabaseAliases();
                return View(templateDto);
            }

            // Call handler to create the template (initial Testing and Production version 1).
            // The handler returns the template name.
            var result = await _createTemplateHandler.HandleAsync(templateDto);

            if (!result.IsCompleteSuccessfully)
            {
                ModelState.AddModelError("", result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);

                // Add specific model errors based on handler result
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

            // If successful, set message and redirect to Design page for the new template.
            TempData["Message"] = $"Template '{result.Data}' created successfully!";
            return RedirectToAction(nameof(Design), new { templateName = result.Data }); // result.Data is the template name.
        }

        // GET: /templates/{templateName}/history
        // ViewBag.TemplateVersions will now contain TemplateVersionDto including IsDeleted/DeletedDate.
        [HttpGet("templates/{templateName}/history")]
        public async Task<IActionResult> History(string templateName)
        {
            // Fetch main template details (model for the view)
            Result<TemplateDetailDto> templateDetailResult = await _getTemplateDesignHandler.HandleAsync(templateName);
            if (!templateDetailResult.IsCompleteSuccessfully || templateDetailResult.Data == null)
            {
                 TempData["ErrorMessage"] = templateDetailResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                 // Redirect or return error view if the template itself cannot be found.
                 return RedirectToAction(nameof(Index), "Home"); // Redirect to home if template not found.
            }

            // Fetch version history (for the table in the view)
            // Note: Handler now returns only NON-DELETED versions.
            var versionsResult = await _getTemplateHistoryHandler.HandleAsync(templateDetailResult.Data.Id);

            // It's generally better to show the history page even if fetching versions failed,
            // but with an error message and an empty list.
            if (!versionsResult.IsCompleteSuccessfully)
            {
                TempData["ErrorMessage"] = versionsResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                ViewBag.TemplateVersions = new List<TemplateVersionDto>(); // Pass empty list on error.
            }
            else
            {
                ViewBag.TemplateVersions = versionsResult.Data; // Pass the list of versions.
            }

            // Pass the main template details as the model.
            return View(templateDetailResult.Data);
        }


        // POST: /templates/{TemplateName}/revert/{VersionNumber}
        // Modified to accept VersionReferenceType from the request body/form.
        // Using [FromForm] assuming the view uses a form with hidden/radio inputs for reference type.
        [HttpPost("templates/{TemplateName}/revert/{VersionNumber}")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Revert([FromRoute] TemplateRevertRequestDto routeRequest, [FromForm] string versionReferenceType)
        {
            // Combine route parameters and form data into the DTO for the handler.
            var request = new TemplateRevertRequestDto
            {
                TemplateName = routeRequest.TemplateName,
                VersionNumber = routeRequest.VersionNumber,
                VersionReferenceType = versionReferenceType // Use value from form/body
            };

            // Call the updated revert handler.
            var result = await _revertTemplateHandler.HandleAsync(request);

            if (!result.IsCompleteSuccessfully)
            {
                TempData["Error"] = result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                // Redirect back to History page with error.
                return RedirectToAction(nameof(History), new { templateName = request.TemplateName });
            }

            // If successful, set success message and redirect. result.Data is the version number it was reverted TO.
            TempData["Message"] = $"Template '{request.TemplateName}' successfully reverted {request.VersionReferenceType} version to {result.Data}."; // More descriptive message
            return RedirectToAction(nameof(History), new { templateName = request.TemplateName }); // Redirect back to History page
            // Or redirect to Design page if preferred: RedirectToAction(nameof(Design), new { templateName = request.TemplateName });
        }

        // New action to handle publishing the Testing version to Production.
        // Route: POST /templates/{templateName}/publish
        [HttpPost("templates/{TemplateName}/publish")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Publish([FromRoute] string templateName)
        {
            // Call the new publish handler.
            // The handler returns the new production version number.
            var result = await _publishTemplateHandler.HandleAsync(templateName);

            if (!result.IsCompleteSuccessfully)
            {
                TempData["Error"] = result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                // Redirect back to the page where the publish button was clicked (likely Design or History).
                // Getting the referring URL is complex. Redirecting to Design is a simple approach.
                return RedirectToAction(nameof(Design), new { templateName = templateName });
            }

            // If successful, set success message and redirect. result.Data is the new Production version.
            TempData["Message"] = $"Template '{templateName}' successfully published to Production Version {result.Data}.";
            return RedirectToAction(nameof(Design), new { templateName = templateName }); // Redirect to Design page.
        }

         // New action to handle soft deleting a template version.
         // Route: POST /templates/versions/{versionId}/delete
        [HttpPost("templates/versions/{VersionId}/delete")]
        [ValidateAntiForgeryToken]
         public async Task<IActionResult> SoftDeleteVersion([FromRoute] int versionId)
         {
             // Need the template name to redirect back to the history page.
             // Fetch the version first to get the template ID, then fetch the template name.
             var versionResult = await _context.TemplateVersions.Include(tv => tv.Template).FirstOrDefaultAsync(tv => tv.Id == versionId);
             string templateName = versionResult?.Template?.Name ?? ""; // Get template name for redirect

             // Call the soft delete handler.
             var result = await _softDeleteTemplateVersionHandler.HandleAsync(versionId);

             if (!result.IsCompleteSuccessfully)
             {
                 TempData["Error"] = result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
             }
             else
             {
                 TempData["Message"] = $"Template version {versionResult?.VersionNumber} soft-deleted successfully.";
             }

             // Redirect back to the History page of the template.
             if (!string.IsNullOrEmpty(templateName))
             {
                return RedirectToAction(nameof(History), new { templateName = templateName });
             }
             else
             {
                 // If template name couldn't be found, redirect to home/dashboard.
                 return RedirectToAction(nameof(Index), "Home");
             }
         }
    }
}
```

---

**29. `PDFGenerator.Web\Views\Index.cshtml`**
(Modified to display Testing and Production versions)

```html
﻿@using PDFGenerator.Web.Dtos.Template
<!-- File: Index.cshtml -->
@model IEnumerable<TemplateListDto>

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
                        <!-- Display Testing and Production versions -->
                        <div class="version-badges">
                           <span class="badge bg-secondary me-1">Testing: v @template.TestingVersion</span>
                           @if(template.ProductionVersion.HasValue)
                           {
                               <span class="badge bg-success">Prod: v @template.ProductionVersion.Value</span>
                           }
                           else
                           {
                                <span class="badge bg-secondary">Prod: N/A</span>
                           }
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
            // const totalTemplatesStat = document.getElementById('totalTemplatesStat'); // Unused

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
                    if(emptyState) emptyState.style.display = 'block';
                    templatesGrid.style.display = 'none';
                }
            }

            if (searchInput) {
                searchInput.addEventListener('input', filterTemplates);
            }

            // Animation (optional, keep for polish)
            templateCards.forEach((card, index) => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                    card.style.transition = 'opacity 0.4s ease-out, transform 0.4s ease-out';
                }, index * 70);
            });
        });
    </script>
}
```

---

**30. `PDFGenerator.Web\Views\Template\Design.cshtml`**
(Modified to display version numbers and add Publish button)

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
            <!-- Form to update the template (creates a new Testing version). -->
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
                         @if (Model.ProductionVersion.HasValue)
                         {
                             <input value="@Model.ProductionVersion.Value" class="form-control" readonly />
                         }
                         else
                         {
                             <input value="N/A" class="form-control" readonly />
                         }
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

                <div class="form-group mb-3">
                    <label asp-for="HtmlContent" class="control-label"></label>
                    <textarea asp-for="HtmlContent" class="form-control" rows="15" id="htmlEditor"></textarea>
                    <span asp-validation-for="HtmlContent" class="text-danger"></span>
                    <small class="form-text text-muted">Use <code>&lt;&lt;FieldName&gt;&gt;</code> for dynamic data placeholders and <code>${{condition ? true_part : false_part}}</code> for conditionals.</small>
                </div>

                <hr class="my-4">

                <h5>Data Configuration:</h5>
                <p class="text-muted">Define how placeholders in the HTML content will be populated for "Outside" (API provided) and "Inside" (system sourced) data modes.</p>

                 <!-- Placeholder list -->
                 <div class="card card-body mb-3">
                     <h6>Detected Placeholders:</h6>
                     <ul id="placeholderList" class="list-inline mb-0 small text-muted">
                         <li class="list-inline-item"><em>(Loading...)</em></li>
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
                    <input type="submit" value="Save Changes" class="btn btn-primary" /> <!-- Saves changes, creates new Testing version -->
                    <a asp-action="Index" asp-controller="Home" class="btn btn-secondary">Back to Templates</a>
                    <a asp-controller="Template" asp-action="History" asp-route-templateName="@Model.Name" class="btn btn-info">View History</a>
                    <!-- Button to trigger publish action -->
                    @if (Model.ProductionVersion == null || Model.TestingVersion > Model.ProductionVersion.Value) // Show publish button if testing is newer or prod is not set
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
                             <i class="fas fa-arrow-alt-circle-up"></i> Published (v @Model.ProductionVersion)
                         </button>
                    }

                    <button type="button" id="downloadPdfBtn" class="btn btn-success">Download Test PDF (Testing Version)</button> <!-- Clarified button text -->
                </div>
                 @Html.AntiForgeryToken() <!-- Anti-forgery token for the main form -->
            </form>
        </div>
    </div>
</div>

@section Scripts {
    @{await Html.RenderPartialAsync("_ValidationScriptsPartial");}

    <link href="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.21/lodash.min.js"></script>

    <script>
        $(document).ready(function() {
            var htmlEditor = $('#htmlEditor');
            var exampleJsonDataTextarea = $('#exampleJsonData');
            var internalDataConfigJsonTextarea = $('#internalDataConfigJson');
            var placeholderListElement = $('#placeholderList');

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
                         updatePlaceholdersList(contents);
                    }, 500)
                 }
            });

            function updatePlaceholdersList(html) {
                 // Match HTML entities for < and >
                 const placeholderRegex = /&lt;&lt;(\w+)&gt;&gt;/g;
                 let match;
                 const placeholders = new Set();

                 while ((match = placeholderRegex.exec(html)) !== null) {
                      placeholders.add(match[1]);
                 }

                 placeholderListElement.empty();
                 if (placeholders.size === 0) {
                      placeholderListElement.html('<li class="list-inline-item"><em>(No data placeholders detected)</em></li>');
                 } else {
                      placeholders.forEach(placeholder => {
                           placeholderListElement.append(`<li class="list-inline-item"><code><<${placeholder}>></code></li>`);
                      });
                 }
            }

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

            formatJsonTextarea(exampleJsonDataTextarea);
            formatJsonTextarea(internalDataConfigJsonTextarea);


            // Test PDF Download Button (using ExampleJsonData for 'Outside' mode)
            $('#downloadPdfBtn').on('click', function() {
                var templateName = '@Model.Name';
                var exampleJsonData = exampleJsonDataTextarea.val();
                var endpoint = `/pdf/generate/${templateName}`;
                var mode = 'outside'; // Always test 'outside' mode from Design page

                try {
                    var payload = exampleJsonData.trim() === "" ? {} : JSON.parse(exampleJsonData);
                } catch (e) {
                    alert('Error: Invalid JSON in Example JSON Data field. Please correct it before testing.');
                    console.error('JSON Parse Error:', e);
                    return;
                }

                 const url = new URL(endpoint, window.location.origin);
                 url.searchParams.append('mode', mode);

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                        // Authorization header is added by JwtCookieMiddleware
                    },
                    body: JSON.stringify(payload)
                })
                .then(response => {
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
                    return response.blob();
                })
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    const suggestedFilename = `${templateName}_Test_${mode}.pdf`;
                    a.href = url;
                    a.download = suggestedFilename;
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                })
                .catch(error => {
                     if (error !== 'Unauthorized') { // Don't show alert if redirected
                         alert('There was a problem generating the PDF: ' + error.message);
                         console.error('PDF Generation Error:', error);
                     }
                });
            });

             // Confirmation script for Publish button
             document.querySelectorAll('.needs-confirmation').forEach(form => {
                form.addEventListener('submit', function (event) {
                    const message = this.dataset.confirmationMessage || 'Are you sure?';
                    if (!confirm(message)) {
                        event.preventDefault();
                    }
                });
            });


            // Initial placeholder detection
             updatePlaceholdersList(htmlEditor.summernote('code'));

        });
    </script>

}
```

---

**31. `PDFGenerator.Web\Views\Template\History.cshtml`**
(Modified to display soft delete status and update Revert buttons)

```html
@using PDFGenerator.Web.Dtos.Template
@using PDFGenerator.Web.Dtos.TemplateVersion
@using PdfGeneratorApp.Common // Needed for VersionReferenceType constants
@model TemplateDetailDto
@{
    // Note: ViewBag.TemplateVersions now only contains NON-DELETED versions by default due to repository change.
    // If you want to show ALL versions including deleted ones, you would need a separate handler/repository method.
    var versions = ViewBag.TemplateVersions as List<TemplateVersionDto>;
    ViewData["Title"] = $"History for {Model.Name}";
}

<div class="container">
    <div class="page-header">
        <h1>@ViewData["Title"]</h1>
        <p class="page-subtitle">Review past versions of the template. Current Testing version is <strong>@Model.TestingVersion</strong>. Current Production version is <strong>@(Model.ProductionVersion ?? 0)</strong>.</p> <!-- Display both versions -->
    </div>

    @if (versions != null && versions.Any())
    {
        <div class="table-container">
            <table class="table table-striped table-hover"> <!-- Added some bootstrap table styling -->
                <thead>
                    <tr>
                        <th>Version</th>
                        <th>Description</th>
                        <th>Internal Data Config</th>
                        <th>Created Date</th>
                        <th>Status</th> @* New column for status (deleted/current) *@
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    @foreach (var version in versions)
                    {
                        // Add class based on status
                        <tr class="@(version.VersionNumber == Model.TestingVersion ? "fw-bold table-info" : "") @(version.VersionNumber == Model.ProductionVersion ? "fw-bold table-success" : "")">
                            <td>
                                @version.VersionNumber
                            </td>
                            <td style="max-width: 200px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="@version.Description">
                                @(string.IsNullOrWhiteSpace(version.Description) ? "N/A" : version.Description)
                            </td>
                             <td style="max-width: 250px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="@version.InternalDataConfigJson">
                                @(string.IsNullOrWhiteSpace(version.InternalDataConfigJson) ? "{}" : version.InternalDataConfigJson)
                            </td>
                            <td>@version.CreatedDate.ToString("MMMM dd, yyyy h:mm tt")</td>
                            <td>
                                @if (version.VersionNumber == Model.TestingVersion)
                                {
                                    <span class="badge bg-info me-1">Testing</span>
                                }
                                @if (Model.ProductionVersion.HasValue && version.VersionNumber == Model.ProductionVersion.Value)
                                {
                                    <span class="badge bg-success">Production</span>
                                }
                                @if (version.IsDeleted) // Although the list should only contain non-deleted ones by default now
                                {
                                     <span class="badge bg-danger">Deleted (@version.DeletedDate?.ToString("g"))</span>
                                }
                                @if (version.VersionNumber != Model.TestingVersion && (Model.ProductionVersion == null || version.VersionNumber != Model.ProductionVersion.Value) && !version.IsDeleted)
                                {
                                     <span class="badge bg-secondary">Historical</span>
                                }
                            </td>
                            <td class="actions-column">
                                @* Revert buttons - allow reverting either Testing or Production to this version *@
                                @if (!version.IsDeleted) // Can only revert to non-deleted versions
                                {
                                    @* Revert Testing Button *@
                                    @if (version.VersionNumber != Model.TestingVersion)
                                    {
                                        <form asp-action="Revert" asp-route-templateName="@Model.Name" asp-route-versionNumber="@version.VersionNumber" method="post" class="d-inline needs-confirmation" data-confirmation-message="Are you sure you want to set Testing version to @version.VersionNumber?">
                                            @Html.AntiForgeryToken()
                                            <input type="hidden" name="versionReferenceType" value="@VersionReferenceType.Testing" /> @* Pass reference type *@
                                            <button type="submit" class="btn btn-sm btn-warning" title="Set Testing version to this version">
                                                <i class="fas fa-undo"></i> Revert Testing
                                            </button>
                                        </form>
                                    }

                                    @* Revert Production Button *@
                                     @if (version.VersionNumber != Model.ProductionVersion && version.VersionNumber <= Model.TestingVersion) // Usually only allow publishing versions <= current testing
                                    {
                                        <form asp-action="Revert" asp-route-templateName="@Model.Name" asp-route-versionNumber="@version.VersionNumber" method="post" class="d-inline ms-1 needs-confirmation" data-confirmation-message="Are you sure you want to set Production version to @version.VersionNumber?">
                                            @Html.AntiForgeryToken()
                                            <input type="hidden" name="versionReferenceType" value="@VersionReferenceType.Production" /> @* Pass reference type *@
                                            <button type="submit" class="btn btn-sm btn-success" title="Set Production version to this version">
                                                <i class="fas fa-award"></i> Revert Production
                                            </button>
                                        </form>
                                    }

                                     @* Soft Delete Button *@
                                     @if (version.VersionNumber != Model.TestingVersion && (Model.ProductionVersion == null || version.VersionNumber != Model.ProductionVersion.Value)) // Cannot delete current Testing or Production
                                     {
                                         <form asp-action="SoftDeleteVersion" asp-route-versionId="@version.Id" method="post" class="d-inline ms-1 needs-confirmation" data-confirmation-message="Are you sure you want to soft-delete version @version.VersionNumber? This cannot be undone easily.">
                                             @Html.AntiForgeryToken()
                                              <button type="submit" class="btn btn-sm btn-danger" title="Soft Delete this version">
                                                  <i class="fas fa-trash-alt"></i> Delete
                                              </button>
                                         </form>
                                     }

                                }
                                <!-- Add a "View Details" button if needed to show historical HTML/JSON in a modal -->
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
            <p>New versions are created when you save changes on the Design page.</p>
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
        // Confirmation script for forms (Revert and Delete)
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
```

---

**32. `PDFGenerator.Web\Views\Docs\Templates.cshtml`**
(Modified to display version numbers in documentation)

```html
@using System.Text.Json
@using PDFGenerator.Web.Dtos.Template
@model List<TemplatesDocDto>

@{
    ViewData["Title"] = "API Documentation";
}

<div class="container">
    <div class="page-header">
        <h1>@ViewData["Title"]</h1>
        <p class="page-subtitle">
            Test and understand the PDF generation API endpoints. Each template uses its <strong>Testing version</strong> for content.
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


                <div class="accordion-item">
                    <h2 class="accordion-header" id="@headingId">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#@collapseId" aria-expanded="false" aria-controls="@collapseId">
                            <span class="badge bg-success me-2 p-2">POST</span>
                            <code class="me-2 fs-6">/pdf/generate/@template.Name</code>
                            <span class="text-muted small">@template.Description</span>
                             <!-- Display versions here -->
                            <span class="ms-auto badge bg-secondary me-1">Testing: v @template.TestingVersion</span>
                            @if(template.ProductionVersion.HasValue)
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
                            <p>Generates a PDF document based on the <strong>@template.Name</strong> template, using the content from <strong>Testing Version @template.TestingVersion</strong> and the provided JSON data (Outside mode) or internal configuration (Inside mode) using optional parameters.</p>

                            <hr class="my-3" />

                            <div class="try-it-out-section" data-template-name="@template.Name">
                                <h5><i class="fas fa-vial me-1"></i> Try it out</h5>
                                <p class="small text-muted">Select a mode, configure data/parameters, and click "Execute".</p>

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


            // --- Execute Button Logic ---
            $('.execute-btn').on('click', function() {
                var $button = $(this);
                var $tryItOutSection = $button.closest('.try-it-out-section');
                var templateName = $tryItOutSection.data('template-name');
                var selectedMode = $tryItOutSection.find('.mode-radio:checked').val();

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
                        // Use the template name and mode in the suggested filename
                        const suggestedFilename = `${templateName}_${selectedMode}_API_Test_${new Date().toISOString().slice(0, 19).replace(/[-:T]/g, "")}.pdf`;
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
                     if (error !== 'Unauthorized') { // Don't show alert if redirected
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

             // Helper function for JSON formatting (outside jQuery document ready)
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


            $('.json-payload').each(function() {
                 formatJsonTextarea($(this));
            });
             $('.data-config-section[data-mode="inside"] textarea').each(function() {
                 formatJsonTextarea($(this));
            });
             $('.inside-parameters-json').each(function() {
                 formatJsonTextarea($(this));
            });

             $('.try-it-out-section').each(function() {
                 var $tryItOutSection = $(this);
                 $tryItOutSection.find('.mode-radio:checked').trigger('change');
             });
        });
    </script>
}
```

---

**Important Note on Migrations:**

After implementing these changes in your code, you *must* create and apply a new database migration using EF Core tools to update your database schema with the new `TestingVersion`, `ProductionVersion`, `IsDeleted`, and `DeletedDate` columns.

1.  Open your terminal or command prompt in the project directory that contains your `.csproj` file (likely `PDFGenerator.Infrastructure`).
2.  Run the following commands:
    ```bash
    dotnet ef migrations add AddVersioningAndSoftDelete
    dotnet ef database update
    ```
    (Or if running from the Web project directory and your DbContext is there):
    ```bash
    dotnet ef migrations add AddVersioningAndSoftDelete --project ../PDFGenerator.Infrastructure/PDFGenerator.Infrastructure.csproj --startup-project ../PDFGenerator.Web/PDFGenerator.Web.csproj
    dotnet ef database update --project ../PDFGenerator.Infrastructure/PDFGenerator.Infrastructure.csproj --startup-project ../PDFGenerator.Web/PDFGenerator.Web.csproj
    ```
    Adjust project paths as necessary.

This will create the necessary database changes to support the new features.

This covers the requested features. Remember to thoroughly test all these new workflows.

Okay, let's modify the code to implement the requested features:

1.  Each template (`Template` entity) needs two references to `TemplateVersion`: one for testing (`TestingVersionNumber`) and one for production (`ProductionVersionNumber`).
2.  We need a way to change these references (`SetTemplateVersionReferenceHandler` and corresponding repository method).
3.  A "Publish to Production" action (`PublishTemplateHandler` and repository method) to set the Production reference to the current Testing reference.
4.  Soft deletion for historical versions (`SoftDeleteTemplateVersionHandler` and repository method).

We'll update the following files:

*   **Models:** `Template.cs`, `TemplateVersion.cs`
*   **DbContext & Migrations:** Generate a new migration.
*   **DTOs:** `TemplateDataAccessDto.cs`, `TemplateSimpleDto.cs`, `TemplateVersionDataAccessDto.cs`, `TemplatesDocDataAccessDto.cs` (minor), `TemplateRevertRequestDto.cs` (rename/modify), Add new DTOs (`TemplateVersionReferenceType.cs`, `PublishTemplateRequestDto.cs`, `SoftDeleteVersionRequestDto.cs`).
*   **Mapping Profiles:** `DataAccessMappingProfile.cs`, `ApplicationLayerMappingProfile.cs`.
*   **Repositories:** `IAccountRepository.cs` (no change), `IBaseRepository.cs` (no change), `ITemplateRepository.cs` (modify), `TemplateRepository.cs` (modify/add methods), `ITemplateVersionRepository.cs` (modify), `TemplateVersionRepository.cs` (modify/add methods).
*   **UnitOfWork:** `IUnitOfWork.cs` (modify), `UnitOfWork.cs` (modify).
*   **Services (Handlers):** `IHandler.cs` (no change), Modify/Rename existing handlers (`GetTemplateByNameHandler` -> `GetProductionTemplateHandler`, `RevertTemplateHandler` -> `SetTemplateVersionHandler`, `GetTemplateDesignHandler` -> `GetTemplateForDesignHandler`, `GeneratePdfHandler` - minor update), Add new handlers (`PublishTemplateHandler`, `SoftDeleteTemplateVersionHandler`).
*   **Extensions:** `ServiceCollectionExtensions.cs` (modify for new handlers/repo methods), `DataSeedingExtensions.cs` (minor).
*   **Controllers:** `HomeController.cs` (modify), `DocsController.cs` (modify), `PdfController.cs` (modify), `TemplateController.cs` (modify/add actions).
*   **Views:** `Index.cshtml`, `Design.cshtml`, `History.cshtml`, `Templates.cshtml` (minor).

**Note:** We will generate a new EF Core migration. The migration file content shown below is what EF Core *would generate* based on the model changes. You would typically run `dotnet ef migrations add AddTestProdVersionsAndIsDeleted` and then `dotnet ef database update` from the project directory containing your `DbContext`.

---

**1. PDFGenerator.Infrastructure\DataAccess\Models\Template.cs**

Modify `Template.cs` to replace `CurrentVersion` with `ProductionVersionNumber` and `TestingVersionNumber`.

```csharp
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

        // Removed: public int CurrentVersion { get; set; } = 1;

        // ADDED properties for specific version references
        public int ProductionVersionNumber { get; set; } = 1; // Default to 1
        public int TestingVersionNumber { get; set; } = 1; // Default to 1


        public DateTime LastModified { get; set; } = DateTime.Now;
        public ICollection<TemplateVersion> Versions { get; set; }
    }
}
```

**2. PDFGenerator.Infrastructure\DataAccess\Models\TemplateVersion.cs**

Modify `TemplateVersion.cs` to add the soft delete flag.

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

        // ADDED property for soft delete
        public bool IsDeleted { get; set; } = false;


        [ForeignKey("TemplateId")]
        public Template Template { get; set; }
    }
}
```

**3. Generate a New Migration**

Run `dotnet ef migrations add AddTestProdVersionsAndIsDeleted` in the project directory containing your DbContext (`PDFGenerator.Infrastructure`). This will generate a new migration file (e.g., `YYYYMMDDHHMMSS_AddTestProdVersionsAndIsDeleted.cs`) and a designer file. The generated migration should look something like this (the exact timestamp will vary, and default values might differ slightly based on EF Core version):

*   **YYYYMMDDHHMMSS_AddTestProdVersionsAndIsDeleted.cs**

```csharp
using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PDFGenerator.Web.Migrations // Note: Still the inconsistent namespace
{
    /// <inheritdoc />
    public partial class AddTestProdVersionsAndIsDeleted : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            // Drop the old CurrentVersion column
            migrationBuilder.DropColumn(
                name: "CurrentVersion",
                table: "Templates");

            // Add the new version number columns to Templates
            migrationBuilder.AddColumn<int>(
                name: "ProductionVersionNumber",
                table: "Templates",
                type: "int",
                nullable: false,
                defaultValue: 1); // Set default to 1

            migrationBuilder.AddColumn<int>(
                name: "TestingVersionNumber",
                table: "Templates",
                type: "int",
                nullable: false,
                defaultValue: 1); // Set default to 1

            // Add the IsDeleted column to TemplateVersions
            migrationBuilder.AddColumn<bool>(
                name: "IsDeleted",
                table: "TemplateVersions",
                type: "bit",
                nullable: false,
                defaultValue: false); // Set default to false
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            // Drop the new columns
            migrationBuilder.DropColumn(
                name: "ProductionVersionNumber",
                table: "Templates");

            migrationBuilder.DropColumn(
                name: "TestingVersionNumber",
                table: "Templates");

            migrationBuilder.DropColumn(
                name: "IsDeleted",
                table: "TemplateVersions");

            // Add the old CurrentVersion column back
            migrationBuilder.AddColumn<int>(
                name: "CurrentVersion",
                table: "Templates",
                type: "int",
                nullable: false,
                defaultValue: 0); // Or whatever the old default was, or requires data migration logic
        }
    }
}
```
*Run `dotnet ef database update` to apply this migration.*

**4. PDFGenerator.Infrastructure\DataAccess\Dtos\TemplateDataAccessDto.cs**

Modify `TemplateDataAccessDto` to reflect the new version number properties on the main template and include the `IsDeleted` flag from the version.

```csharp
// File: Infrastructure/Data/Dtos/TemplateDataAccessDto.cs
using PdfGeneratorApp.Models;
using System;
// Removed: using System.Text.Json.Serialization; // No longer needed here

namespace PDFGenerator.Infrastructure.DataAccess.Dtos
{
    // This DTO represents the Template entity combined with details of *one specific* version (e.g., the Test or Prod version)
    public class TemplateDataAccessDto
    {
        public int Id { get; set; }
        public string Name { get; set; }

        // Properties from the associated TemplateVersion
        public string HtmlContent { get; set; }
        public string? Description { get; set; } // Description is now on TemplateVersion
        public string? ExampleJsonData { get; set; }
        public string? InternalDataConfigJson { get; set; }
        public DateTime CreatedDate { get; set; } // Creation date of the version being represented

        // Properties from the main Template entity
        public int ProductionVersionNumber { get; set; }
        public int TestingVersionNumber { get; set; }
        public DateTime LastModified { get; set; } // Last modified date of the template record itself

        // Added property from TemplateVersion for soft delete status of *this specific version*
        public bool IsDeleted { get; set; }


        // Note: The Versions collection property is removed from this DTO
        // as this DTO is typically used to represent *one* template + *one* version's details.
        // The history view will use a list of TemplateVersionDataAccessDto.
        // Removed: public ICollection<TemplateVersionDataAccessDto> Versions { get; set; }
    }
}
```

**5. PDFGenerator.Infrastructure\DataAccess\Dtos\TemplatesDocDataAccessDto.cs**

Minor change: `Description` is now sourced from the Version, but the DTO structure doesn't strictly need to change. Ensure the repository query populates it correctly.

```csharp
﻿// File: Infrastructure/Data/Dtos/TemplateDataAccessDto.cs // Still incorrect comment
using System.ComponentModel.DataAnnotations;

namespace PDFGenerator.Infrastructure.DataAccess.Dtos
{
    public class TemplatesDocDataAccessDto
    {
        public int Id { get; set; }
        [Required]
        [StringLength(100, ErrorMessage = "Template Name cannot exceed 100 characters.")]
        public string Name { get; set; }

        // Description is now from the version, but the property name is the same
        public string? Description { get; set; }

        public string? ExampleJsonData { get; set; }
        public string? InternalDataConfigJson { get; set; }
    }
}
```

**6. PDFGenerator.Infrastructure\DataAccess\Dtos\TemplateSimpleDto.cs**

Modify `TemplateSimpleDto` to include both version numbers.

```csharp
﻿using System; // Added for DateTime

namespace PDFGenerator.Infrastructure.DataAccess.Dtos
{
    public class TemplateSimpleDto
    {
        public int Id { get; set; }
        public string Name { get; set; }

        // Removed: public int CurrentVersion { get; set; }

        // ADDED properties for specific version references
        public int ProductionVersionNumber { get; set; }
        public int TestingVersionNumber { get; set; }

        public DateTime LastModified { get; set; }
    }
}
```

**7. PDFGenerator.Infrastructure\DataAccess\Dtos\TemplateVersionDataAccessDto.cs**

Add the `IsDeleted` flag to `TemplateVersionDataAccessDto`.

```csharp
// File: Infrastructure/Data/Dtos/TemplateVersionDataAccessDto.cs

using System; // Added for DateTime

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

        // ADDED property for soft delete
        public bool IsDeleted { get; set; }
    }
}
```

**8. PDFGenerator.Web\Dtos\Template\TemplateVersionReferenceType.cs**

Create a new enum or class for version reference types. An enum is cleaner.

```csharp
namespace PDFGenerator.Web.Dtos.Template
{
    public enum TemplateVersionReferenceType
    {
        Testing,
        Production
    }
}
```

**9. PDFGenerator.Web\Dtos\Template\SetTemplateVersionRequestDto.cs**

Rename and modify `TemplateRevertRequestDto.cs` to include the version type.

```csharp
// Was TemplateRevertRequestDto.cs
using PDFGenerator.Web.Dtos.Template; // Added for TemplateVersionReferenceType

namespace PDFGenerator.Web.Dtos.Template
{
    public class SetTemplateVersionRequestDto
    {
        public string TemplateName { get; set; }
        public int VersionNumber { get; set; }
        public TemplateVersionReferenceType VersionType { get; set; } // ADDED: Which reference to set (Test or Prod)
    }
}
```

**10. PDFGenerator.Web\Dtos\Template\PublishTemplateRequestDto.cs**

Create a new DTO for the Publish action.

```csharp
namespace PDFGenerator.Web.Dtos.Template
{
    public class PublishTemplateRequestDto
    {
        // Only needs the template name to identify which template to publish
        public string TemplateName { get; set; }
    }
}
```

**11. PDFGenerator.Web\Dtos\TemplateVersion\SoftDeleteVersionRequestDto.cs**

Create a new DTO for the Soft Delete action.

```csharp
namespace PDFGenerator.Web.Dtos.TemplateVersion
{
    public class SoftDeleteVersionRequestDto
    {
        // Only needs the version ID to identify which version to delete
        public int VersionId { get; set; }
    }
}
```

**12. PDFGenerator.Web\Dtos\Template\TemplateListDto.cs**

Modify `TemplateListDto` to match `TemplateSimpleDto`.

```csharp
using System; // Added for DateTime

namespace PDFGenerator.Web.Dtos.Template
{
    public class TemplateListDto
    {
        public int Id { get; set; }
        public string Name { get; set; }
        // Removed: public string Description { get; set; } // Description is per version now
        // Removed: public int CurrentVersion { get; set; }

        // ADDED properties for specific version references
        public int ProductionVersionNumber { get; set; }
        public int TestingVersionNumber { get; set; }

        public DateTime LastModified { get; set; }
    }
}
```

**13. PDFGenerator.Web\Dtos\Template\TemplateDetailDto.cs**

Modify `TemplateDetailDto` to include both version numbers and version creation date/IsDeleted.

```csharp
using System.ComponentModel.DataAnnotations;
using System; // Added for DateTime

namespace PDFGenerator.Web.Dtos.Template
{
    // This DTO represents the Template entity combined with details of *one specific* version (e.g., the Test version for editing)
    public class TemplateDetailDto
    {
        public int Id { get; set; }

        [Required]
        [StringLength(100, ErrorMessage = "Template Name cannot exceed 100 characters.")]
        public string Name { get; set; }

        // Properties from the associated TemplateVersion (the one being viewed/edited)
        public string HtmlContent { get; set; }
        public string? Description { get; set; }
        public string? ExampleJsonData { get; set; }
        public string? InternalDataConfigJson { get; set; }
        public DateTime CreatedDate { get; set; } // Creation date of the version being represented
        public int VersionNumber { get; set; } // The version number of the version being represented
        public bool IsDeleted { get; set; } // Is this specific version deleted?


        // Properties from the main Template entity - provide context in the UI
        public int ProductionVersionNumber { get; set; }
        public int TestingVersionNumber { get; set; }
        public DateTime LastModified { get; set; } // Last modified date of the template record itself

    }
}
```

**14. PDFGenerator.Web\Dtos\TemplateVersion\TemplateVersionDto.cs**

Add the `IsDeleted` flag to `TemplateVersionDto`.

```csharp
using System;

namespace PDFGenerator.Web.Dtos.TemplateVersion
{
    public class TemplateVersionDto
    {
        public int Id { get; set; }
        public int TemplateId { get; set; }
        public int VersionNumber { get; set; }
        public string HtmlContent { get; set; }
        public string? Description { get; set; }
        public string? ExampleJsonData { get; set; }
        public string? InternalDataConfigJson { get; set; }
        public DateTime CreatedDate { get; set; }

        // ADDED property for soft delete
        public bool IsDeleted { get; set; }
    }
}
```

**15. PDFGenerator.Infrastructure\DataAccess\MappingProfile\DataAccessMappingProfile.cs**

Update mappings for the modified DTOs and models.

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
            // Mapping Template entity to TemplateDataAccessDto
            CreateMap<Template, TemplateDataAccessDto>()
                 // Ignore version-specific content properties when mapping FROM Template entity
                 // These must be populated from the relevant TemplateVersion
                .ForMember(dest => dest.HtmlContent, opt => opt.Ignore())
                .ForMember(dest => dest.Description, opt => opt.Ignore())
                .ForMember(dest => dest.ExampleJsonData, opt => opt.Ignore())
                .ForMember(dest => dest.InternalDataConfigJson, opt => opt.Ignore())
                .ForMember(dest => dest.CreatedDate, opt => opt.Ignore()) // Version creation date
                .ForMember(dest => dest.VersionNumber, opt => opt.Ignore()) // Specific version number
                .ForMember(dest => dest.IsDeleted, opt => opt.Ignore()); // Version deleted status

            // Mapping TemplateDataAccessDto to Template entity
            CreateMap<TemplateDataAccessDto, Template>()
                // Ignore version-specific content properties when mapping TO Template entity
                .ForMember(dest => dest.Versions, opt => opt.Ignore()); // Versions collection is managed separately


            // Bidirectional mapping between TemplateVersion entity and DTO
            CreateMap<TemplateVersion, TemplateVersionDataAccessDto>().ReverseMap();

            // Mapping from Template entity to TemplateSimpleDto (for lists)
            CreateMap<Template, TemplateSimpleDto>().ReverseMap();

            // Mapping from TemplateVersionDataAccessDto to TemplateDataAccessDto
            // This is used to populate the version-specific fields on TemplateDataAccessDto
            CreateMap<TemplateVersionDataAccessDto, TemplateDataAccessDto>(MemberList.Source) // Map only source properties
                .ForMember(dest => dest.Id, opt => opt.Ignore()) // Don't overwrite Template Id
                .ForMember(dest => dest.Name, opt => opt.Ignore()) // Don't overwrite Template Name
                 // Mapping version-specific properties
                .ForMember(dest => dest.HtmlContent, opt => opt.MapFrom(src => src.HtmlContent))
                .ForMember(dest => dest.Description, opt => opt.MapFrom(src => src.Description))
                .ForMember(dest => dest.ExampleJsonData, opt => opt.MapFrom(src => src.ExampleJsonData))
                .ForMember(dest => dest.InternalDataConfigJson, opt => opt.MapFrom(src => src.InternalDataConfigJson))
                .ForMember(dest => dest.CreatedDate, opt => opt.MapFrom(src => src.CreatedDate))
                .ForMember(dest => dest.VersionNumber, opt => opt.MapFrom(src => src.VersionNumber))
                .ForMember(dest => dest.IsDeleted, opt => opt.MapFrom(src => src.IsDeleted))
                // Ignore Template-specific properties
                .ForMember(dest => dest.ProductionVersionNumber, opt => opt.Ignore())
                .ForMember(dest => dest.TestingVersionNumber, opt => opt.Ignore())
                .ForMember(dest => dest.LastModified, opt => opt.Ignore());


            // Add mapping for TemplatesDocDataAccessDto
            CreateMap<Template, TemplatesDocDataAccessDto>()
                 // Map Description, ExampleJsonData, InternalDataConfigJson from the *related* TemplateVersion
                 // This mapping profile alone cannot do this automatically. The repository query must handle this.
                 // We still define the mapping for the properties that *are* on Template (Id, Name)
                 // The repository will select into TemplatesDocDataAccessDto directly.
                 .ForMember(dest => dest.Description, opt => opt.Ignore())
                 .ForMember(dest => dest.ExampleJsonData, opt => opt.Ignore())
                 .ForMember(dest => dest.InternalDataConfigJson, opt => opt.Ignore());
            // Add reverse map if needed
             CreateMap<TemplatesDocDataAccessDto, Template>()
                 .ForMember(dest => dest.ProductionVersionNumber, opt => opt.Ignore())
                 .ForMember(dest => dest.TestingVersionNumber, opt => opt.Ignore())
                 .ForMember(dest => dest.LastModified, opt => opt.Ignore())
                 .ForMember(dest => dest.Versions, opt => opt.Ignore());



            // Existing mappings (likely don't need modification unless source/dest DTOs changed)
            // CreateMap<TemplateVersion, TemplateDataAccessDto>().ReverseMap(); // This mapping still seems strange given the structure of TemplateDataAccessDto

        }
    }
}
```

**16. PDFGenerator.Web\MappingProfile\ApplicationLayerMappingProfile.cs**

Update mappings for modified web DTOs.

```csharp
using AutoMapper;
using PDFGenerator.Web.Dtos.Template;
using PDFGenerator.Web.Dtos.TemplateVersion;
using PDFGenerator.Infrastructure.DataAccess.Dtos;
using PDFGenerator.Web.Dtos.Auth;

namespace PdfGeneratorApp.Infrastructure.Mapping
{
    public class ApplicationLayerMappingProfile : Profile
    {
        public ApplicationLayerMappingProfile()
        {
            // Mapping TemplateSimpleDto <-> TemplateSimpleDto (Identity map, used when source and dest are the same)
            CreateMap<TemplateSimpleDto, TemplateSimpleDto>(); // Required for mapping lists when the source is already the correct DTO type

            // Mapping TemplateSimpleDto <-> TemplateDataAccessDto
            CreateMap<TemplateListDto, TemplateSimpleDto>().ReverseMap(); // TemplateListDto is the Application layer equivalent of TemplateSimpleDto

            // Mapping TemplateDetailDto <-> TemplateDataAccessDto
             CreateMap<TemplateDetailDto, TemplateDataAccessDto>().ReverseMap(); // Update to map new version number properties and version-specific properties


            // Mapping TemplateCreateDto -> TemplateDataAccessDto
            CreateMap<TemplateCreateDto, TemplateDataAccessDto>()
                 .ForMember(dest => dest.Id, opt => opt.Ignore()) // Id is generated by DB
                 .ForMember(dest => dest.CurrentVersion, opt => opt.Ignore()) // CurrentVersion is removed
                 .ForMember(dest => dest.LastModified, opt => opt.Ignore()) // Set by repo/UoW
                 .ForMember(dest => dest.Versions, opt => opt.Ignore()) // Versions managed by repo
                 .ForMember(dest => dest.ProductionVersionNumber, opt => opt.Ignore()) // Set by repo on create
                 .ForMember(dest => dest.TestingVersionNumber, opt => opt.Ignore()) // Set by repo on create
                 .ForMember(dest => dest.CreatedDate, opt => opt.Ignore()) // Set by repo/UoW for version
                 .ForMember(dest => dest.VersionNumber, opt => opt.Ignore()) // Set by repo for version
                 .ForMember(dest => dest.IsDeleted, opt => opt.Ignore()); // Set by repo for version


            // Mapping TemplateUpdateDto -> TemplateDataAccessDto
             CreateMap<TemplateUpdateDto, TemplateDataAccessDto>()
                 .ForMember(dest => dest.Name, opt => opt.Ignore()) // Name cannot be changed via update DTO
                 .ForMember(dest => dest.CurrentVersion, opt => opt.Ignore()) // CurrentVersion is removed
                 .ForMember(dest => dest.LastModified, opt => opt.Ignore()) // Set by repo/UoW
                 .ForMember(dest => dest.Versions, opt => opt.Ignore()) // Versions managed by repo
                 .ForMember(dest => dest.ProductionVersionNumber, opt => opt.Ignore()) // Not changed by update
                 .ForMember(dest => dest.TestingVersionNumber, opt => opt.Ignore()) // Not changed by update
                 .ForMember(dest => dest.CreatedDate, opt => opt.Ignore()) // Set by repo/UoW for version
                 .ForMember(dest => dest.VersionNumber, opt => opt.Ignore()) // Set by repo for version
                 .ForMember(dest => dest.IsDeleted, opt => opt.Ignore()); // Set by repo for version


            // Mapping TemplateVersionDto <-> TemplateVersionDataAccessDto
            CreateMap<TemplateVersionDto, TemplateVersionDataAccessDto>().ReverseMap();


            // Mapping TemplatesDocDto <-> TemplatesDocDataAccessDto
            CreateMap<TemplatesDocDto, TemplatesDocDataAccessDto>().ReverseMap();

            // Account DTOs
            CreateMap<AccountDto, AccountDataAccessDto>().ReverseMap();
            CreateMap<UserDto, UserDataAccessDto>().ReverseMap(); // Added mapping for UserDto if used from infrastructure

            // New request DTOs (typically no mapping needed if used directly by handler)
            // CreateMap<SetTemplateVersionRequestDto, ...>();
            // CreateMap<PublishTemplateRequestDto, ...>();
            // CreateMap<SoftDeleteVersionRequestDto, ...>();

        }
    }
}
```

**17. PDFGenerator.Infrastructure\DataAccess\Repositories\Interfaces\ITemplateRepository.cs**

Modify `ITemplateRepository` to define new methods and update existing ones.

```csharp
// File: Infrastructure/Data/Repositories/ITemplateRepository.cs
using PDFGenerator.Infrastructure.DataAccess.Dtos;
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Infrastructure.Data.Repositories.Base;
using PdfGeneratorApp.Models;
using PDFGenerator.Web.Dtos.Template; // Added for TemplateVersionReferenceType

namespace PdfGeneratorApp.Infrastructure.Data.Repositories
{
    public interface ITemplateRepository : IBaseRepository<Template, TemplateDataAccessDto>
    {
        // yoyo todo add pgaination and change this bad name
        // Updated to reflect TemplateSimpleDto changes
        Task<Result<List<TemplateSimpleDto>>> GetAllTemplateSimplAsync();

        // Updated to ensure it fetches from the PRODUCTION version
        Task<Result<List<TemplatesDocDataAccessDto>>> GetAllAsync();

        // Renamed - gets the template and its PRODUCTION version
        Task<Result<TemplateDataAccessDto>> GetProductionTemplateByNameAsync(string name);

        // NEW - gets the template and its TESTING version
        Task<Result<TemplateDataAccessDto>> GetTestingTemplateByNameAsync(string name);


        Task<Result<bool>> AnyByNameAsync(string name);

        // Updated - creates a new template and its first version, setting Test/Prod to 1
        Task<Result<TemplateDataAccessDto>> CreateNewTemplateAsync(TemplateDataAccessDto templateDataAccessDto);

        // Updated - creates a new version and sets the TESTING version number
        // Returns the new Testing version number
        Task<Result<int>> UpdateTemplateAsync(TemplateDataAccessDto templateDataAccessDto);

        // Renamed - sets either the Testing or Production version number
        // Returns the version number that was set
        Task<Result<int>> SetTemplateVersionReferenceAsync(int templateId, int versionNumber, TemplateVersionReferenceType versionType);

        // NEW - sets the Production version number to the Testing version number
        // Returns the new Production version number
        Task<Result<int>> PublishTemplateAsync(int templateId);

        // NEW - Get a template by ID (needed for checks in handlers)
        Task<Result<Template>> GetByIdAsync(int templateId); // Returning entity here for internal checks

        // NEW - Get a specific version by ID (needed for checks in handlers)
        Task<Result<TemplateVersion>> GetVersionByIdAsync(int versionId); // Returning entity here for internal checks
    }
}
```

**18. PDFGenerator.Infrastructure\DataAccess\Repositories\Implementation\TemplateRepository.cs**

Implement the changes in `TemplateRepository.cs`.

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
using PDFGenerator.Web.Dtos.Template; // Added for TemplateVersionReferenceType

namespace PdfGeneratorApp.Infrastructure.Data.Repositories
{
    // Inherit from BaseRepository<Template, TemplateDataAccessDto>
    public class TemplateRepository : BaseRepository<Template, TemplateDataAccessDto>, ITemplateRepository
    {
        // Removed redundant fields context and _mapper

        private readonly ApplicationDbContext _dbContext; // Use the base context field instead of a new one
        private readonly IMapper _mapper; // Use the base mapper field instead of a new one
        private readonly TemplateProcessingService _templateProcessingService;

        // Use the base class's context and mapper
        public TemplateRepository(ApplicationDbContext context, IMapper mapper, TemplateProcessingService templateProcessingService) : base(context, mapper)
        {
            // Assign to local fields if the base fields were private,
            // but it's better to use the protected DbSet directly or refactor BaseRepository.
            // For now, let's keep these local fields and align with the base.
            // Ideally, BaseRepository should expose protected _context and _mapper.
            // Assuming the base context and mapper are available or using the local ones.
            _dbContext = context; // Use the base context
            _mapper = mapper; // Use the base mapper
            _templateProcessingService = templateProcessingService;
        }


        public async Task<Result<List<TemplateSimpleDto>>> GetAllTemplateSimplAsync()
        {
            try
            {
                // Use _dbContext or DbSet from base
                List<TemplateSimpleDto> data = await _dbContext.Templates.Select(t => new TemplateSimpleDto()
                {
                    Id = t.Id,
                    Name = t.Name,
                    LastModified = t.LastModified, // CORRECTED the bug here
                    TestingVersionNumber = t.TestingVersionNumber, // ADDED
                    ProductionVersionNumber = t.ProductionVersionNumber // ADDED

                }).ToListAsync();

                return Result<List<TemplateSimpleDto>>.Success(data);

            }
            catch (Exception ex) // Catch specific or generic exception and log
            {
                // Log the exception
                Console.WriteLine($"Error in TemplateRepository.GetAllTemplateSimplAsync: {ex.Message}");
                return Result<List<TemplateSimpleDto>>.Failure(ErrorMessageUserConst.ServerErrorNoMsg); // Generic server error
            }
        }

        public async Task<Result<List<TemplatesDocDataAccessDto>>> GetAllAsync()
        {
             try // Added try-catch
             {
                // Join Template with TemplateVersions filtered by ProductionVersionNumber
                var templates = await (from t in _dbContext.Templates
                                   join tv in _dbContext.TemplateVersions
                                   on new { TemplateId = t.Id, Version = t.ProductionVersionNumber }
                                   equals new { tv.TemplateId, Version = tv.VersionNumber }
                                   where !tv.IsDeleted // Only include non-deleted production versions
                                   select new TemplatesDocDataAccessDto
                                   {
                                       Id = t.Id, // CORRECTED to use Template ID
                                       Name = t.Name,
                                       Description = tv.Description, // Get description from version
                                       ExampleJsonData = tv.ExampleJsonData,
                                       InternalDataConfigJson = tv.InternalDataConfigJson,
                                   }).ToListAsync();

                // If no templates are found, return an empty list, not an error
                // if (templates == null) return Result<List<TemplatesDocDataAccessDto>>.Failure(ErrorMessageUserConst.TemplateNameExists); // REMOVED incorrect null check and error

                return Result<List<TemplatesDocDataAccessDto>>.Success(templates ?? new List<TemplatesDocDataAccessDto>()); // Return empty list if query result is null (unlikely but safe)
             }
             catch(Exception ex) // Catch exception and log
             {
                 Console.WriteLine($"Error in TemplateRepository.GetAllAsync: {ex.Message}");
                 return Result<List<TemplatesDocDataAccessDto>>.Failure(ErrorMessageUserConst.ServerErrorNoMsg); // Generic server error
             }
        }

        // NEW - Gets template and its PRODUCTION version by name
        public async Task<Result<TemplateDataAccessDto>> GetProductionTemplateByNameAsync(string name)
        {
            return await GetTemplateWithVersionByNameAsync(name, TemplateVersionReferenceType.Production);
        }

        // NEW - Gets template and its TESTING version by name
         public async Task<Result<TemplateDataAccessDto>> GetTestingTemplateByNameAsync(string name)
        {
             return await GetTemplateWithVersionByNameAsync(name, TemplateVersionReferenceType.Testing);
        }


        // Helper method to get template with a specific version reference
        private async Task<Result<TemplateDataAccessDto>> GetTemplateWithVersionByNameAsync(string name, TemplateVersionReferenceType versionType)
        {
             try // Added try-catch
             {
                 // Use _dbContext or DbSet from base
                 var template = await _dbContext.Templates.SingleOrDefaultAsync(t => t.Name == name);

                 if (template == null)
                 {
                     return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.TemplateNotFound); // Correct error for not finding the template
                 }

                 int targetVersionNumber = versionType == TemplateVersionReferenceType.Production
                                             ? template.ProductionVersionNumber
                                             : template.TestingVersionNumber;

                 // Join Template with the specific Version based on the reference type
                 var templateWithVersion = await (from t in _dbContext.Templates
                                                 join tv in _dbContext.TemplateVersions
                                                 on new { TemplateId = t.Id, Version = targetVersionNumber } // Join condition uses targetVersionNumber
                                                 equals new { tv.TemplateId, Version = tv.VersionNumber }
                                                 where t.Id == template.Id // Ensure it's the template we found
                                                 && !tv.IsDeleted // Ensure the target version is not deleted
                                                 select new TemplateDataAccessDto() // Project into the DTO
                                                 {
                                                     // Properties from the Template entity
                                                     Id = t.Id,
                                                     Name = t.Name,
                                                     ProductionVersionNumber = t.ProductionVersionNumber,
                                                     TestingVersionNumber = t.TestingVersionNumber,
                                                     LastModified = t.LastModified,

                                                     // Properties from the joined TemplateVersion entity
                                                     HtmlContent = tv.HtmlContent,
                                                     Description = tv.Description,
                                                     ExampleJsonData = tv.ExampleJsonData,
                                                     InternalDataConfigJson = tv.InternalDataConfigJson,
                                                     CreatedDate = tv.CreatedDate,
                                                     VersionNumber = tv.VersionNumber, // The actual version number of the version data
                                                     IsDeleted = tv.IsDeleted // Soft delete status of this version
                                                 })
                                                .SingleOrDefaultAsync(); // Use SingleOrDefaultAsync as we expect one result

                 if (templateWithVersion == null)
                 {
                      // This case might occur if the referenced version (Test or Prod) doesn't exist or is deleted
                      return Result<TemplateDataAccessDto>.Failure(string.Format(ErrorMessageUserConst.VersionNotFound, targetVersionNumber, name));
                 }


                 return Result<TemplateDataAccessDto>.Success(templateWithVersion);
             }
             catch (InvalidOperationException ex) // Catch if SingleOrDefault finds multiple
             {
                 Console.WriteLine($"Error in TemplateRepository.GetTemplateWithVersionByNameAsync (Multiple results for name '{name}'): {ex.Message}");
                 return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.ServerErrorNoMsg); // Or a more specific error
             }
             catch (Exception ex) // Catch other exceptions
             {
                 Console.WriteLine($"Error in TemplateRepository.GetTemplateWithVersionByNameAsync for name '{name}': {ex.Message}");
                 return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
             }
        }


        public async Task<Result<bool>> AnyByNameAsync(string name)
        {
             try
             {
                // Use _dbContext or DbSet from base
                var exists = await _dbContext.Templates.AnyAsync(t => t.Name == name);
                return Result<bool>.Success(exists);
             }
             catch(Exception ex)
             {
                Console.WriteLine($"Error in TemplateRepository.AnyByNameAsync: {ex.Message}");
                return Result<bool>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
             }
        }

        public async Task<Result<TemplateDataAccessDto>> CreateNewTemplateAsync(TemplateDataAccessDto templateDto)
        {
             try // Added try-catch
             {
                templateDto.Name = templateDto.Name.Replace(" ", "_"); // Replace spaces with underscores

                // Use _dbContext or DbSet from base
                var nameExistsResult = await _dbContext.Templates.AnyAsync(t => t.Name == templateDto.Name);
                if (nameExistsResult) return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.TemplateNameExists);

                string generatedExampleJson; // Declare outside try for broader scope
                try
                {
                    generatedExampleJson = _templateProcessingService.GenerateExampleJson(templateDto.HtmlContent);
                }
                catch (Exception ex)
                {
                    // Correct error message
                    Console.WriteLine($"Error generating example JSON on create: {ex.Message}");
                    return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.ExampleJsonGenerationFailed);
                }


                if (!string.IsNullOrWhiteSpace(templateDto.InternalDataConfigJson))
                {
                    // Use the service for validation
                    if (!_templateProcessingService.IsValidJson(templateDto.InternalDataConfigJson))
                    {
                         return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.InternalDataConfigInvalidJson);
                    }
                     try // Added check for root element type
                     {
                         using JsonDocument doc = JsonDocument.Parse(templateDto.InternalDataConfigJson);
                         if (doc.RootElement.ValueKind != JsonValueKind.Object)
                         {
                             return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.InternalDataConfigNotObject);
                         }
                     }
                     catch (JsonException)
                     {
                          // This catch is actually redundant due to IsValidJson, but kept for safety
                          return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.InternalDataConfigInvalidJson);
                     }
                }


                // Create the main Template entity
                var template = _mapper.Map<Template>(templateDto);
                // Set initial version numbers
                template.ProductionVersionNumber = 1; // Initial version is 1
                template.TestingVersionNumber = 1;     // Initial version is 1
                template.LastModified = DateTime.Now;

                // Create the initial TemplateVersion entity (version 1)
                var initialVersion = new TemplateVersion
                {
                    VersionNumber = 1,
                    CreatedDate = DateTime.Now,
                    HtmlContent = templateDto.HtmlContent,
                    Description = templateDto.Description, // Description from input DTO
                    ExampleJsonData = generatedExampleJson, // Use generated JSON
                    InternalDataConfigJson = templateDto.InternalDataConfigJson,
                    IsDeleted = false // Initial version is not deleted
                };

                 // Add the version to the template's versions collection - EF will handle the relationship
                 template.Versions = new List<TemplateVersion> { initialVersion };

                // Add the template (and its linked version) to the context
                await _dbContext.Templates.AddAsync(template);

                // Map the created template entity (which now has an ID after AddAsync in some EF setups, but SaveChanges confirms it)
                // back to the DTO. The DTO needs version-specific data too.
                // Manually create the DTO or refine mapping. Let's manually populate version data.
                var createdTemplateDto = _mapper.Map<TemplateDataAccessDto>(template); // Maps Template entity parts
                _mapper.Map(initialVersion, createdTemplateDto); // Maps TemplateVersion parts onto the same DTO object


                // Save happens in UnitOfWork
                return Result<TemplateDataAccessDto>.Success(createdTemplateDto); // Return the combined DTO
             }
             catch(Exception ex) // Catch other errors during creation
             {
                 Console.WriteLine($"Error creating new template: {ex.Message}");
                 return Result<TemplateDataAccessDto>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
             }

        }

        // Updated - creates a new version and sets the TESTING version number
        // Returns the new Testing version number
        public async Task<Result<int>> UpdateTemplateAsync(TemplateDataAccessDto templateDto)
        {
             try // Added try-catch
             {
                 // Use _dbContext or DbSet from base
                 Template existingTemplate = await _dbContext.Templates
                                             .Include(t => t.Versions) // Include versions to find max version
                                             .FirstOrDefaultAsync(t => t.Id == templateDto.Id);

                 if (existingTemplate == null)
                 {
                     return Result<int>.Failure(string.Format(ErrorMessageUserConst.TemplateIdNotFound, templateDto.Id));
                 }

                // Validate Internal Data Config JSON using the service
                if (!string.IsNullOrWhiteSpace(templateDto.InternalDataConfigJson))
                {
                     if (!_templateProcessingService.IsValidJson(templateDto.InternalDataConfigJson))
                     {
                         return Result<int>.Failure(ErrorMessageUserConst.InternalDataConfigInvalidJson);
                     }
                     try
                     {
                         using JsonDocument doc = JsonDocument.Parse(templateDto.InternalDataConfigJson);
                         if (doc.RootElement.ValueKind != JsonValueKind.Object)
                         {
                              return Result<int>.Failure(ErrorMessageUserConst.InternalDataConfigNotObject);
                         }
                     }
                     catch (JsonException)
                     {
                         // Redundant due to IsValidJson, but safe
                         return Result<int>.Failure(ErrorMessageUserConst.InternalDataConfigInvalidJson);
                     }
                }


                int lastVersionNumber = 0;
                if (existingTemplate.Versions != null && existingTemplate.Versions.Any())
                {
                     lastVersionNumber = existingTemplate.Versions.Max(tv => tv.VersionNumber);
                }
                 // If no versions exist, the new version is 1. Otherwise, it's last + 1.
                 // The Create method already handles version 1. This path is for subsequent updates.
                 // Ensure lastVersionNumber calculation is correct if the template somehow has no versions but exists.
                 // Max() on an empty collection throws InvalidOperationException. Need a safer way.
                 lastVersionNumber = await _dbContext.TemplateVersions
                                                 .Where(tv => tv.TemplateId == templateDto.Id)
                                                 .Select(tv => tv.VersionNumber)
                                                 .DefaultIfEmpty(0) // Returns 0 if sequence is empty
                                                 .MaxAsync();


                int newVersionNumber = lastVersionNumber + 1;

                string generatedExampleJson;
                 try
                 {
                      generatedExampleJson = _templateProcessingService.GenerateExampleJson(templateDto.HtmlContent);
                 }
                 catch (Exception ex)
                 {
                      // Correct error message
                      Console.WriteLine($"Error generating example JSON on update: {ex.Message}");
                      return Result<int>.Failure(ErrorMessageUserConst.ExampleJsonGenerationFailed);
                 }


                // Create the new TemplateVersion entity
                TemplateVersion newVersion = new TemplateVersion()
                {
                    TemplateId = templateDto.Id,
                    VersionNumber = newVersionNumber,
                    HtmlContent = templateDto.HtmlContent,
                    Description = templateDto.Description, // Description from input DTO
                    ExampleJsonData = generatedExampleJson, // Use generated JSON
                    InternalDataConfigJson = templateDto.InternalDataConfigJson,
                    CreatedDate = DateTime.Now, // Use DateTime.Now for full timestamp
                    IsDeleted = false
                };

                // Add the new version to the context
                await _dbContext.TemplateVersions.AddAsync(newVersion);

                // Update the main template entity's TESTING version reference and LastModified date
                existingTemplate.TestingVersionNumber = newVersionNumber;
                existingTemplate.LastModified = DateTime.Now; // Use DateTime.Now for full timestamp
                // EF Core tracks changes to existingTemplate automatically

                // Save happens in UnitOfWork
                return Result<int>.Success(newVersionNumber); // Return the new testing version number
             }
             catch(Exception ex) // Catch other exceptions during update
             {
                 Console.WriteLine($"Error updating template ID {templateDto.Id}: {ex.Message}");
                 return Result<int>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
             }
        }


        // Renamed and modified - sets either the Testing or Production version number
        // Returns the version number that was set
        public async Task<Result<int>> SetTemplateVersionReferenceAsync(int templateId, int versionNumber, TemplateVersionReferenceType versionType)
        {
            try // Added try-catch
            {
                Template existingTemplate = await _dbContext.Templates
                                             .Include(t => t.Versions) // Include versions to check existence
                                             .FirstOrDefaultAsync(t => t.Id == templateId);

                if (existingTemplate == null)
                {
                    return Result<int>.Failure(string.Format(ErrorMessageUserConst.TemplateIdNotFound, templateId));
                }

                // Check if the target version exists for this template and is not deleted
                var targetVersion = await _dbContext.TemplateVersions
                                                .Where(tv => tv.TemplateId == templateId && tv.VersionNumber == versionNumber && !tv.IsDeleted)
                                                .FirstOrDefaultAsync();

                if (targetVersion == null)
                {
                     // Provide specific error if version not found or is deleted
                     return Result<int>.Failure(string.Format(ErrorMessageUserConst.VersionNotFound, versionNumber, existingTemplate.Name) + " (or is deleted)");
                }


                // Validation to prevent reverting Test/Prod to a future version (optional, but good practice)
                // Although the UI might prevent this, validation here is safer.
                int currentRefVersion = versionType == TemplateVersionReferenceType.Production
                                           ? existingTemplate.ProductionVersionNumber
                                           : existingTemplate.TestingVersionNumber;

                 // We need to know the highest version number *overall* for this template
                 int highestVersionNumber = await _dbContext.TemplateVersions
                                                 .Where(tv => tv.TemplateId == templateId)
                                                 .Select(tv => tv.VersionNumber)
                                                 .DefaultIfEmpty(0)
                                                 .MaxAsync();

                 // This check seems less relevant now with Test/Prod refs. A better check might be
                 // if the *target version* is somehow higher than the highest historical version.
                 // Let's check if the requested versionNumber is valid (i.e., <= highest).
                 if (versionNumber > highestVersionNumber)
                 {
                     return Result<int>.Failure(string.Format(ErrorMessageUserConst.VersionNotFound, versionNumber, existingTemplate.Name)); // Version number too high implies not found
                 }
                // The previous 'targetVersion == null' check already handles versions not found or deleted.
                // The check against 'highestVersionNumber' is somewhat redundant if targetVersion is found.


                // Update the appropriate version number property
                if (versionType == TemplateVersionReferenceType.Production)
                {
                    existingTemplate.ProductionVersionNumber = versionNumber;
                }
                else // TemplateVersionReferenceType.Testing
                {
                    existingTemplate.TestingVersionNumber = versionNumber;
                }

                existingTemplate.LastModified = DateTime.Now; // Update LastModified on the main template

                // Save happens in UnitOfWork
                return Result<int>.Success(versionNumber); // Return the version number that was set
            }
            catch(Exception ex) // Catch other exceptions
            {
                 Console.WriteLine($"Error setting version reference for template ID {templateId}: {ex.Message}");
                 return Result<int>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }


        // NEW - publishes the testing version to production
        // Returns the new Production version number
        public async Task<Result<int>> PublishTemplateAsync(int templateId)
        {
            try // Added try-catch
            {
                 Template existingTemplate = await _dbContext.Templates
                                             .FirstOrDefaultAsync(t => t.Id == templateId);

                 if (existingTemplate == null)
                 {
                     return Result<int>.Failure(string.Format(ErrorMessageUserConst.TemplateIdNotFound, templateId));
                 }

                 // Check if the testing version is valid (exists and is not deleted)
                 var testingVersion = await _dbContext.TemplateVersions
                                                .Where(tv => tv.TemplateId == templateId && tv.VersionNumber == existingTemplate.TestingVersionNumber && !tv.IsDeleted)
                                                .FirstOrDefaultAsync();

                 if (testingVersion == null)
                 {
                     // Cannot publish a testing version that doesn't exist or is deleted
                     return Result<int>.Failure($"Cannot publish. Testing version {existingTemplate.TestingVersionNumber} not found or is deleted for template ID {templateId}.");
                 }

                 // Set the Production version number to the Testing version number
                 existingTemplate.ProductionVersionNumber = existingTemplate.TestingVersionNumber;
                 existingTemplate.LastModified = DateTime.Now; // Update LastModified on the main template

                 // Save happens in UnitOfWork
                 return Result<int>.Success(existingTemplate.ProductionVersionNumber); // Return the new production version number
            }
            catch(Exception ex) // Catch other exceptions
            {
                 Console.WriteLine($"Error publishing template ID {templateId}: {ex.Message}");
                 return Result<int>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }

        // NEW - Get a template by ID
        public async Task<Result<Template>> GetByIdAsync(int templateId)
        {
            try
            {
                 // Use _dbContext or DbSet from base
                 var entity = await _dbContext.Templates.FindAsync(templateId);

                 if (entity == null)
                     return Result<Template>.Failure(string.Format(ErrorMessageUserConst.TemplateIdNotFound, templateId));

                 return Result<Template>.Success(entity);
            }
            catch (Exception ex)
            {
                 Console.WriteLine($"Error in TemplateRepository.GetByIdAsync({templateId}): {ex.Message}");
                 return Result<Template>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }

        // NEW - Get a specific version by ID
         public async Task<Result<TemplateVersion>> GetVersionByIdAsync(int versionId)
         {
             try
             {
                  // Use _dbContext or DbSet from base
                  var entity = await _dbContext.TemplateVersions.FindAsync(versionId);

                  if (entity == null)
                      return Result<TemplateVersion>.Failure($"Template Version with ID {versionId} not found."); // Specific error message

                  return Result<TemplateVersion>.Success(entity);
             }
             catch (Exception ex)
             {
                  Console.WriteLine($"Error in TemplateRepository.GetVersionByIdAsync({versionId}): {ex.Message}");
                  return Result<TemplateVersion>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
             }
         }

    }
}
```

**19. PDFGenerator.Infrastructure\DataAccess\Repositories\Interfaces\ITemplateVersionRepository.cs**

Modify `ITemplateVersionRepository` to include the Soft Delete method and uncomment/add the specific version getter.

```csharp
// File: Infrastructure/Data/Repositories/ITemplateVersionRepository.cs
using PdfGeneratorApp.Infrastructure.Data.Repositories.Base;
using PdfGeneratorApp.Models;
using PdfGeneratorApp.Common;
using PDFGenerator.Infrastructure.DataAccess.Dtos;

namespace PdfGeneratorApp.Infrastructure.Data.Repositories
{
    public interface ITemplateVersionRepository : IBaseRepository<TemplateVersion, TemplateVersionDataAccessDto>
    {
         // Updated to exclude deleted by default
         Task<Result<List<TemplateVersionDataAccessDto>>> GetByTemplateVersionsByTemplateIdAsync(int templateId);

         // Uncommented and defined - gets a specific version by template ID and version number
         Task<Result<TemplateVersionDataAccessDto>> GetByTemplateIdAndVersionNumberAsync(int templateId, int versionNumber);

         // NEW - Soft deletes a template version by ID
         // Does NOT check if it's a Test/Prod version - handler will do that.
         // Returns bool indicating if the version was found and marked as deleted.
         Task<Result<bool>> SoftDeleteVersionAsync(int versionId);
    }
}
```

**20. PDFGenerator.Infrastructure\DataAccess\Repositories\Implementation\TemplateVersionRepository.cs**

Implement the changes in `TemplateVersionRepository.cs`.

```csharp
// File: Infrastructure/Data/Repositories/TemplateVersionRepository.cs
using PdfGeneratorApp.Infrastructure.Data.Repositories.Base;
using PdfGeneratorApp.Data;
using AutoMapper;
using PdfGeneratorApp.Models;
using PdfGeneratorApp.Common;
using Microsoft.EntityFrameworkCore;
using PDFGenerator.Infrastructure.DataAccess.Dtos;

namespace PdfGeneratorApp.Infrastructure.Data.Repositories
{
    // Inherit from BaseRepository<TemplateVersion, TemplateVersionDataAccessDto>
    public class TemplateVersionRepository : BaseRepository<TemplateVersion, TemplateVersionDataAccessDto>, ITemplateVersionRepository
    {
        // Removed redundant fields context and mapper

        private readonly ApplicationDbContext _dbContext; // Use base context
        private readonly IMapper _mapper; // Use base mapper


        public TemplateVersionRepository(ApplicationDbContext context, IMapper mapper): base(context, mapper)
        {
             // Assign to local fields if base are private
            _dbContext = context; // Use base context
            _mapper = mapper; // Use base mapper
        }

        // Updated to exclude deleted versions by default
        public async Task<Result<List<TemplateVersionDataAccessDto>>> GetByTemplateVersionsByTemplateIdAsync(int templateId)
        {
             try // Added try-catch
             {
                // Use _dbContext or DbSet from base
                // Filter out deleted versions
                List<TemplateVersion> TemplateVersions = await _dbContext.TemplateVersions
                                                                .Where(tv => tv.TemplateId == templateId && !tv.IsDeleted)
                                                                .OrderByDescending(tv => tv.VersionNumber) // Optional: order by version
                                                                .ToListAsync();

                // If no non-deleted versions, return empty list, not an error
                return Result<List<TemplateVersionDataAccessDto>>.Success(_mapper.Map<List<TemplateVersionDataAccessDto>>(TemplateVersions) ?? new List<TemplateVersionDataAccessDto>());
             }
             catch(Exception ex) // Catch exceptions
             {
                 Console.WriteLine($"Error in TemplateVersionRepository.GetByTemplateVersionsByTemplateIdAsync({templateId}): {ex.Message}");
                 return Result<List<TemplateVersionDataAccessDto>>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
             }
        }

        // Uncommented and implemented - gets a specific version by template ID and version number
        public async Task<Result<TemplateVersionDataAccessDto>> GetByTemplateIdAndVersionNumberAsync(int templateId, int versionNumber)
        {
             try // Added try-catch
             {
                 // Use _dbContext or DbSet from base
                 var version = await _dbContext.TemplateVersions
                                         .Where(tv => tv.TemplateId == templateId && tv.VersionNumber == versionNumber)
                                         .SingleOrDefaultAsync(); // Use SingleOrDefault in case of data anomaly

                 if (version == null)
                 {
                     // Use a version-specific error message
                     return Result<TemplateVersionDataAccessDto>.Failure(string.Format(ErrorMessageUserConst.VersionNotFound, versionNumber, $"TemplateId {templateId}")); // Cannot easily get template name here
                 }

                 return Result<TemplateVersionDataAccessDto>.Success(_mapper.Map<TemplateVersionDataAccessDto>(version));
             }
             catch(InvalidOperationException ex) // Catch if SingleOrDefault finds multiple
             {
                 Console.WriteLine($"Error in TemplateVersionRepository.GetByTemplateIdAndVersionNumberAsync (Multiple results for template ID {templateId}, version {versionNumber}): {ex.Message}");
                 return Result<TemplateVersionDataAccessDto>.Failure(ErrorMessageUserConst.ServerErrorNoMsg); // Or a more specific error
             }
             catch(Exception ex) // Catch other exceptions
             {
                 Console.WriteLine($"Error in TemplateVersionRepository.GetByTemplateIdAndVersionNumberAsync({templateId}, {versionNumber}): {ex.Message}");
                 return Result<TemplateVersionDataAccessDto>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
             }
        }

        // NEW - Soft deletes a template version by ID
        // Returns bool indicating if the version was found and marked as deleted.
        public async Task<Result<bool>> SoftDeleteVersionAsync(int versionId)
        {
             try // Added try-catch
             {
                 // Use _dbContext or DbSet from base
                 var versionToDelete = await _dbContext.TemplateVersions.FindAsync(versionId);

                 if (versionToDelete == null)
                 {
                     // Return success(false) or failure depending on desired behavior. Success(false) indicates "not deleted because not found".
                     return Result<bool>.Success(false); // Version not found, nothing to delete
                 }

                 // Do not allow deleting if already deleted (idempotency)
                 if (versionToDelete.IsDeleted)
                 {
                     return Result<bool>.Success(true); // Already deleted, consider it successful
                 }

                 // Mark as deleted
                 versionToDelete.IsDeleted = true;
                 // EF Core tracks the change

                 // Save happens in UnitOfWork
                 return Result<bool>.Success(true); // Indicate successful marking for deletion
             }
             catch(Exception ex) // Catch exceptions
             {
                 Console.WriteLine($"Error in TemplateVersionRepository.SoftDeleteVersionAsync({versionId}): {ex.Message}");
                 return Result<bool>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
             }
        }
    }
}
```

**21. PDFGenerator.Infrastructure\DataAccess\UnitOfWork\IUnitOfWork.cs**

Add the new repository methods to the Unit of Work interface.

```csharp
// File: Infrastructure/Data/UnitOfWork/IUnitOfWork.cs
using PdfGeneratorApp.Infrastructure.Data.Repositories;
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Models; // Added for GetByIdAsync/GetVersionByIdAsync

namespace PdfGeneratorApp.Infrastructure.Data.UnitOfWork
{
    public interface IUnitOfWork : IDisposable
    {
        ITemplateRepository Templates { get; }
        ITemplateVersionRepository TemplateVersions { get; }
        IAccountRepository Accounts { get; }

        Task<Result<bool>> SaveAsync();
    }
}
```

**22. PDFGenerator.Infrastructure\DataAccess\UnitOfWork\UnitOfWork.cs**

Update the Unit of Work implementation to inject and expose the repositories. No logic changes needed for `SaveAsync`.

```csharp
// File: Infrastructure/Data/UnitOfWork/UnitOfWork.cs
using PdfGeneratorApp.Data;
using PdfGeneratorApp.Infrastructure.Data.Repositories;
using PdfGeneratorApp.Common;
using Microsoft.EntityFrameworkCore.Storage;
using PdfGeneratorApp.Models; // Added for repository properties

namespace PdfGeneratorApp.Infrastructure.Data.UnitOfWork
{
    public class UnitOfWork : IUnitOfWork
    {
        private readonly ApplicationDbContext _context; // Use the base context field
        public ITemplateRepository Templates { get; }
        public ITemplateVersionRepository TemplateVersions { get; }
        public IAccountRepository Accounts { get; }

        // Constructor injects repositories and context
        public UnitOfWork(ApplicationDbContext context,
                          ITemplateRepository templates,
                          ITemplateVersionRepository templateVersions,
                          IAccountRepository accounts)
        {
            _context = context;
            Templates = templates;
            TemplateVersions = templateVersions;
            Accounts = accounts;
        }

        public async Task<Result<bool>> SaveAsync()
        {
            IDbContextTransaction? transaction = null;

            try
            {
                // Only start a transaction if there are tracked changes to avoid unnecessary overhead
                // This is an optimization, optional but good practice.
                // var hasChanges = _context.ChangeTracker.HasChanges();
                // if (hasChanges) {
                //     transaction = await _context.Database.BeginTransactionAsync();
                // }
                 // Simplified: Always begin transaction if SaveAsync is called by handler
                 transaction = await _context.Database.BeginTransactionAsync();


                var affectedRows = await _context.SaveChangesAsync();

                 // Only commit if a transaction was started
                // if (transaction != null) {
                    await transaction.CommitAsync();
                // }


                return Result<bool>.Success(affectedRows > 0); // Indicate success if any rows were affected

            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error during UnitOfWork SaveAsync: {ex.Message}");

                if (transaction != null)
                {
                    await transaction.RollbackAsync();
                }

                // Provide more specific error if available, otherwise unexpected
                return Result<bool>.Failure($"Database Error: {ex.Message}"); // Include exception message for debug/logging, generic for user
            }
             finally
             {
                 if (transaction != null)
                 {
                      await transaction.DisposeAsync();
                 }
             }
        }

        public void Dispose()
        {
            _context.Dispose();
        }
    }
}
```

**23. PDFGenerator.Web\Services\IHandler.cs** (No Change)

**24. PDFGenerator.Web\Extensions\ServiceCollectionExtensions.cs**

Register the new/renamed handlers.

```csharp
﻿using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using PDFGenerator.Web.Handlers;
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Handlers;
using System.Text;
using PDFGenerator.Web.Dtos.Template; // Added for DTOs used in handlers
using PDFGenerator.Web.Dtos.TemplateVersion; // Added for DTOs used in handlers

// Note: Namespace is still inconsistent - EduCach.DataAccess.Extensions
namespace EduCach.DataAccess.Extensions // Should be PDFGenerator.Infrastructure.Extensions or PDFGenerator.Web.Extensions
{
    public static class ServiceCollectionExtensions
    {
        public static IServiceCollection AddDbContextServices(this IServiceCollection services, IConfiguration configuration)
        {
            services.AddIdentity<User, IdentityRole>().AddEntityFrameworkStores<ApplicationDbContext>().AddDefaultTokenProviders();

            services.AddDbContext<ApplicationDbContext>(optionBuilder =>
            {
                optionBuilder.UseSqlServer(configuration.GetConnectionString("cs"),
                    option =>
                    {
                        option.CommandTimeout(120);

                    });
            });

            return services;
        }


        public static IServiceCollection AddRepositories(this IServiceCollection services)
        {
            return services.AddScoped<TemplateProcessingService>()
                            .AddScoped<IMailServies, MailServies>()
                            .AddScoped<IAccountRepository, AccountRepository>()
                            // Use concrete implementations that match interfaces
                            .AddScoped<ITemplateRepository, TemplateRepository>()
                            .AddScoped<ITemplateVersionRepository, TemplateVersionRepository>()
                            .AddScoped<IUnitOfWork, UnitOfWork>();
        }

        // Note: This seems like a Web layer extension method, should probably be in PDFGenerator.Web.Extensions
        public static IServiceCollection AddServices(this IServiceCollection services)
        {
            return services
                // Renamed GetTemplateByNameHandler to GetProductionTemplateHandler (used by API)
                .AddScoped<IGetProductionTemplateHandler, GetProductionTemplateHandler>()
                // NEW - Gets template and its Testing version for design view
                .AddScoped<IGetTemplateForDesignHandler, GetTemplateForDesignHandler>()

                .AddScoped<IGetTemplatesDocHandler, GetTemplatesDocHandler>()
                .AddScoped<IGetTemplatesListHandler, GetTemplatesListHandler>()
                .AddScoped<IGeneratePdfHandler, GeneratePdfHandler>()

                // GetTemplateDesignHandler is replaced by GetTemplateForDesignHandler
                // .AddScoped<IGetTemplateDesignHandler, GetTemplateDesignHandler>()

                .AddScoped<IUpdateTemplateHandler, UpdateTemplateHandler>()
                .AddScoped<ICreateTemplateHandler, CreateTemplateHandler>()
                .AddScoped<IGetTemplateHistoryHandler, GetTemplateHistoryHandler>()

                // Renamed RevertTemplateHandler to SetTemplateVersionHandler
                .AddScoped<ISetTemplateVersionHandler, SetTemplateVersionHandler>()

                // NEW Handlers
                .AddScoped<IPublishTemplateHandler, PublishTemplateHandler>()
                .AddScoped<ISoftDeleteTemplateVersionHandler, SoftDeleteTemplateVersionHandler>();
        }

        // Note: This seems like a Web layer extension method, should probably be in PDFGenerator.Web.Extensions
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
                        context.Response.Redirect("/Account/Login");

                        return Task.CompletedTask;
                    }
                };
            });
        }

    }
}
```

**25. PDFGenerator.Infrastructure\DataSeeding\DataSeedingExtensions.cs**

Minor change to the seeding logic to reflect the new version number properties. Initial template insert data is gone anyway after migrations, but the *logic* for seeding a new template should set Test/Prod to 1. The current seed just creates users/roles, which is fine.

```csharp
// File: DataSeeding\DataSeedingExtensions.cs (No changes needed based on current content)
// The existing seed logic only creates users and roles, not templates.
// If template seeding were added, it would need to set Test/Prod versions.
```

**26. PDFGenerator.Web\Services\CreateTemplateHandler.cs**

Update `CreateTemplateHandler` to use the repository method which now sets Test/Prod to 1.

```csharp
// File: Handlers/CreateTemplateHandler.cs
using AutoMapper;
using PDFGenerator.Infrastructure.DataAccess.Dtos;
using PDFGenerator.Web.Dtos.Template;
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;

namespace PdfGeneratorApp.Handlers
{
    public interface ICreateTemplateHandler : IHandler<TemplateCreateDto, string>
    {
    }

    public class CreateTemplateHandler : ICreateTemplateHandler
    {
        private readonly IUnitOfWork _unitOfWork;
        private readonly IMapper _mapper;

        public CreateTemplateHandler(IUnitOfWork unitOfWork, IMapper mapper)
        {
            _unitOfWork = unitOfWork;
            _mapper = mapper;
        }

        public async Task<Result<string>> HandleAsync(TemplateCreateDto templateDto)
        {
            try
            {
                // Mapping DTO to DataAccessDto
                TemplateDataAccessDto templateDataAccessDto = _mapper.Map<TemplateDataAccessDto>(templateDto);

                // Use the repository method (which now sets Test/Prod versions to 1)
                Result<TemplateDataAccessDto> result = await _unitOfWork.Templates.CreateNewTemplateAsync(templateDataAccessDto);

                if (!result.IsCompleteSuccessfully)
                {
                     // Propagate specific error messages from repository
                    return Result<string>.Failure(result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                // Save changes to the database
                var saveResult = await _unitOfWork.SaveAsync();

                if (!saveResult.IsCompleteSuccessfully)
                {
                    // Propagate save error
                    return Result<string>.Failure(saveResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                // Return the name of the created template from the result data
                return Result<string>.Success(result.Data.Name);
            }
            catch (Exception ex)
            {
                // Catch unexpected errors during handler execution
                 Console.WriteLine($"Error in CreateTemplateHandler: {ex.Message}");
                return Result<string>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }
    }
}
```

**27. PDFGenerator.Web\Services\GeneratePdfHandler.cs**

Update `GeneratePdfHandler` to use the repository method that gets the *production* version.

```csharp
// File: Handlers/GeneratePdfHandler.cs
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Services;
using System.Text.Json;
using WkHtmlToPdfDotNet;
using WkHtmlToPdfDotNet.Contracts;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using PDFGenerator.Infrastructure.DataAccess.Dtos; // Added for DTO
using PDFGenerator.Web.Dtos.Template; // Added for DTO


namespace PdfGeneratorApp.Handlers
{
    // Request tuple: (template name, request body JSON, mode string)
    public interface IGeneratePdfHandler : IHandler<(string templateName, JsonElement requestBodyJson, string mode), byte[]>
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

        public async Task<Result<byte[]>> HandleAsync((string templateName, JsonElement requestBodyJson, string mode) request)
        {
            try
            {
                // Use the repository via Unit of Work to get the template + PRODUCTION version data access DTO
                var repoResult = await _unitOfWork.Templates.GetProductionTemplateByNameAsync(request.templateName);

                if (!repoResult.IsCompleteSuccessfully)
                {
                    // Propagate failure from repository (like Not Found, Version Not Found, Deleted Version)
                    // Check for specific errors from the repository method
                    if (repoResult.ErrorMessages == ErrorMessageUserConst.TemplateNotFound)
                        return Result<byte[]>.Failure(ErrorMessageUserConst.TemplateNotFound);
                    // Handle version not found/deleted error specifically
                    if (repoResult.ErrorMessages.Contains(ErrorMessageUserConst.VersionNotFound) || repoResult.ErrorMessages.Contains("(or is deleted)")) // Crude check, better to return specific error types
                         return Result<byte[]>.Failure($"Production version not found or is deleted for template '{request.templateName}'.");


                    // Generic server error for other issues
                    return Result<byte[]>.Failure(repoResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                var templateDataAccessDto = repoResult.Data; // Get the data access DTO

                 // The repository method now handles the template not found case,
                 // so templateDataAccessDto should not be null if repoResult.IsCompleteSuccessfully is true.
                 // This null check is belt-and-suspenders protection.
                if (templateDataAccessDto == null)
                {
                     return Result<byte[]>.Failure(ErrorMessageUserConst.TemplateNotFound);
                }


                JsonElement finalDataForHtmlProcessing;
                JsonElement insideParameters = default; // Initialize with default (null JsonElement)

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

                        // Attempt to get the 'parameters' property from the request body
                        if (request.requestBodyJson.TryGetProperty("parameters", out JsonElement parametersElement))
                        {
                             insideParameters = parametersElement; // Assign if found
                        }
                        // If 'parameters' property isn't found, insideParameters remains default (null), which ResolveInternalData handles

                        // Use data access DTO's InternalDataConfigJson property
                        finalDataForHtmlProcessing = _templateProcessingService.ResolveInternalData(templateDataAccessDto.InternalDataConfigJson, insideParameters);
                        break;

                    default:
                        return Result<byte[]>.Failure(ErrorMessageUserConst.InvalidMode);
                }

                // Use data access DTO's HtmlContent property (from the fetched Production version)
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
                    // More specific error message
                    return Result<byte[]>.Failure(ErrorMessageUserConst.PdfGenerationFailed + ". Check template content or wkhtmltopdf installation.");
                }

                return Result<byte[]>.Success(pdf);
            }
            catch (Exception ex)
            {
                // Log the unexpected exception
                Console.WriteLine($"Error in GeneratePdfHandler: {ex.Message}");
                return Result<byte[]>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }
    }
}
```

**28. PDFGenerator.Web\Services\GetTemplateByNameHandler.cs** (Rename)

Rename this file and class to `GetProductionTemplateHandler.cs` and `GetProductionTemplateHandler`. Update the interface name accordingly. This handler is now explicitly for getting the *production* version.

*   **GetProductionTemplateHandler.cs** (formerly GetTemplateByNameHandler.cs)

```csharp
// File: Handlers/GetProductionTemplateHandler.cs (Renamed)
using PdfGeneratorApp.Common;
using AutoMapper;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using PDFGenerator.Web.Dtos.Template;
using PdfGeneratorApp.Handlers; // Required for IHandler


namespace PDFGenerator.Web.Handlers // Using Web.Handlers namespace now
{
    // Renamed interface
    public interface IGetProductionTemplateHandler : IHandler<string, TemplateDetailDto>
    {
    }

    // Renamed class
    public class GetProductionTemplateHandler : IGetProductionTemplateHandler
    {
        private readonly IUnitOfWork _unitOfWork;
        private readonly IMapper _mapper;

        public GetProductionTemplateHandler(IUnitOfWork unitOfWork, IMapper mapper)
        {
            _unitOfWork = unitOfWork;
            _mapper = mapper;
        }

        public async Task<Result<TemplateDetailDto>> HandleAsync(string templateName)
        {
            try
            {
                // Use the repository method to get the template + PRODUCTION version
                var repoResult = await _unitOfWork.Templates.GetProductionTemplateByNameAsync(templateName);

                if (!repoResult.IsCompleteSuccessfully)
                {
                    // Propagate failure from repository (Not Found, Version Not Found/Deleted, Server Error)
                    return Result<TemplateDetailDto>.Failure(repoResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                // The repository method now handles the template not found case and version not found/deleted
                // so repoResult.Data should be null only if repoResult.IsCompleteSuccessfully is false.
                 if (repoResult.Data == null)
                 {
                     // Fallback check, should be covered by repoResult.IsCompleteSuccessfully
                     return Result<TemplateDetailDto>.Failure(ErrorMessageUserConst.TemplateNotFound);
                 }


                // Map the Data Access DTO to an Application DTO
                var templateDto = _mapper.Map<TemplateDetailDto>(repoResult.Data);

                return Result<TemplateDetailDto>.Success(templateDto);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in GetProductionTemplateHandler: {ex.Message}");
                return Result<TemplateDetailDto>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }
    }
}
```

**29. PDFGenerator.Web\Services\GetTemplateDesignHandler.cs** (Replace)

This handler is replaced by a new one that fetches the *testing* version.

*   **GetTemplateForDesignHandler.cs** (NEW)

```csharp
// File: Handlers/GetTemplateForDesignHandler.cs
using PdfGeneratorApp.Common;
using AutoMapper;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using PDFGenerator.Web.Dtos.Template;
using PdfGeneratorApp.Handlers; // Required for IHandler
using PDFGenerator.Infrastructure.DataAccess.Dtos; // Added for DTO

namespace PDFGenerator.Web.Handlers // Using Web.Handlers namespace now
{
    // NEW interface - gets the template and its TESTING version
    public interface IGetTemplateForDesignHandler : IHandler<string, TemplateDetailDto>
    {
    }

    // NEW class - gets the template and its TESTING version
    public class GetTemplateForDesignHandler : IGetTemplateForDesignHandler
    {
        private readonly IUnitOfWork _unitOfWork;
        private readonly IMapper _mapper;

        public GetTemplateForDesignHandler(IUnitOfWork unitOfWork, IMapper mapper)
        {
            _unitOfWork = unitOfWork;
            _mapper = mapper;
        }

        public async Task<Result<TemplateDetailDto>> HandleAsync(string templateName)
        {
            try
            {
                // Use the repository method to get the template + TESTING version
                var repoResult = await _unitOfWork.Templates.GetTestingTemplateByNameAsync(templateName);

                if (!repoResult.IsCompleteSuccessfully)
                {
                    // Propagate failure from repository (Not Found, Version Not Found/Deleted, Server Error)
                    return Result<TemplateDetailDto>.Failure(repoResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                 // The repository method now handles template/version not found/deleted
                 if (repoResult.Data == null)
                 {
                     // Fallback check, should be covered by repoResult.IsCompleteSuccessfully
                     return Result<TemplateDetailDto>.Failure(ErrorMessageUserConst.TemplateNotFound);
                 }


                // Map the Data Access DTO to an Application DTO
                var templateDto = _mapper.Map<TemplateDetailDto>(repoResult.Data);

                return Result<TemplateDetailDto>.Success(templateDto);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in GetTemplateForDesignHandler: {ex.Message}");
                return Result<TemplateDetailDto>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }
    }
}
```

**30. PDFGenerator.Web\Services\GetTemplateHistoryHandler.cs**

Update `GetTemplateHistoryHandler` to use the repository method that now excludes deleted versions by default.

```csharp
// File: Handlers/GetTemplateHistoryHandler.cs
using PdfGeneratorApp.Common;
using AutoMapper;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using PDFGenerator.Web.Dtos.TemplateVersion;
using PdfGeneratorApp.Handlers; // Required for IHandler


namespace PDFGenerator.Web.Handlers // Using Web.Handlers namespace now
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

        public async Task<Result<List<TemplateVersionDto>>> HandleAsync(int templateId)
        {
            try
            {
                // Use the repository method which now excludes deleted versions by default
                var getVersionsResult = await _unitOfWork.TemplateVersions.GetByTemplateVersionsByTemplateIdAsync(templateId);

                // getVersionsResult.Data will be an empty list if no versions found,
                // or null if a server error occurred in the repo.
                if (!getVersionsResult.IsCompleteSuccessfully)
                {
                     return Result<List<TemplateVersionDto>>.Failure(getVersionsResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }


                // Map the list of Data Access DTOs to Application DTOs
                var versionDtos = _mapper.Map<List<TemplateVersionDto>>(getVersionsResult.Data);

                return Result<List<TemplateVersionDto>>.Success(versionDtos);
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

**31. PDFGenerator.Web\Services\RevertTemplateHandler.cs** (Rename and Modify)

Rename this file and class to `SetTemplateVersionHandler.cs` and `SetTemplateVersionHandler`. Update the interface name. Modify to take `SetTemplateVersionRequestDto` and use the updated repository method.

*   **SetTemplateVersionHandler.cs** (formerly RevertTemplateHandler.cs)

```csharp
// File: Handlers/SetTemplateVersionHandler.cs (Renamed)
using PdfGeneratorApp.Common;
using AutoMapper; // Still needed for potential future mappings
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using PDFGenerator.Web.Dtos.Template;
using PdfGeneratorApp.Handlers; // Required for IHandler


namespace PDFGenerator.Web.Handlers // Using Web.Handlers namespace now
{
    // Renamed interface
    public interface ISetTemplateVersionHandler : IHandler<SetTemplateVersionRequestDto, int>
    {
    }

    // Renamed class
    public class SetTemplateVersionHandler : ISetTemplateVersionHandler
    {
        private readonly IUnitOfWork _unitOfWork;
        // private readonly IMapper _mapper; // Not used in this implementation, can remove if not used elsewhere

        public SetTemplateVersionHandler(IUnitOfWork unitOfWork) // Removed IMapper from constructor
        {
            _unitOfWork = unitOfWork;
            // _mapper = mapper;
        }

        public async Task<Result<int>> HandleAsync(SetTemplateVersionRequestDto request)
        {
            try
            {
                // The repository method includes checks for template and version existence, and if version is deleted.
                var repoResult = await _unitOfWork.Templates.SetTemplateVersionReferenceAsync(
                    templateId: 0, // Need template ID - need to fetch template by name first
                    versionNumber: request.VersionNumber,
                    versionType: request.VersionType
                );

                 // Need to get the template ID from the name first
                 var templateResult = await _unitOfWork.Templates.GetByIdAsync(0); // Need a GetTemplateByName on ITemplateRepository that returns Template entity

                 // Let's modify the flow: Get template by name first in the handler
                 var templateByNameResult = await _unitOfWork.Templates.GetProductionTemplateByNameAsync(request.TemplateName); // Can use any getter that returns TemplateDataAccessDto to get ID

                 if (!templateByNameResult.IsCompleteSuccessfully || templateByNameResult.Data == null)
                 {
                      // Propagate template not found error
                     return Result<int>.Failure(templateByNameResult.ErrorMessages ?? ErrorMessageUserConst.TemplateNotFound);
                 }

                 int templateId = templateByNameResult.Data.Id;


                // Now call the repository method with the actual template ID
                var setVersionResult = await _unitOfWork.Templates.SetTemplateVersionReferenceAsync(
                    templateId: templateId,
                    versionNumber: request.VersionNumber,
                    versionType: request.VersionType
                );


                if (!setVersionResult.IsCompleteSuccessfully)
                {
                    // Propagate specific error messages from repository (e.g., Version Not Found/Deleted)
                    return Result<int>.Failure(setVersionResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }


                // Save changes to the database after setting the version reference
                var saveResult = await _unitOfWork.SaveAsync();

                if (!saveResult.IsCompleteSuccessfully)
                {
                    // Propagate save error
                    return Result<int>.Failure(saveResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                // Return the version number that was set
                return Result<int>.Success(setVersionResult.Data);
            }
            catch (Exception ex)
            {
                // Catch unexpected errors during handler execution
                 Console.WriteLine($"Error in SetTemplateVersionHandler: {ex.Message}");
                return Result<int>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }
    }
}
```

**32. PDFGenerator.Web\Services\UpdateTemplateHandler.cs**

Update `UpdateTemplateHandler` to use the repository method which now sets the *testing* version number and returns it.

```csharp
// File: Handlers/UpdateTemplateHandler.cs
using AutoMapper;
using PDFGenerator.Infrastructure.DataAccess.Dtos;
using PDFGenerator.Web.Dtos.Template;
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using PdfGeneratorApp.Services;
using System.Text.Json;
using PdfGeneratorApp.Handlers; // Required for IHandler


namespace PDFGenerator.Web.Handlers // Using Web.Handlers namespace now
{
    public interface IUpdateTemplateHandler : IHandler<TemplateUpdateDto, int>
    {
    }

    public class UpdateTemplateHandler : IUpdateTemplateHandler
    {
        private readonly IUnitOfWork _unitOfWork;
        private readonly IMapper _mapper;

        public UpdateTemplateHandler(IUnitOfWork unitOfWork, IMapper mapper)
        {
            _unitOfWork = unitOfWork;
            _mapper = mapper;
        }

        public async Task<Result<int>> HandleAsync(TemplateUpdateDto templateDto)
        {
            try
            {
                 // Mapping DTO to DataAccessDto. This DTO contains the *new* content.
                var templateDataAccessDto = _mapper.Map<TemplateDataAccessDto>(templateDto);

                // Use the repository method which creates a new version and updates the TESTING reference
                var updateResult = await _unitOfWork.Templates.UpdateTemplateAsync(templateDataAccessDto);

                if (!updateResult.IsCompleteSuccessfully)
                {
                     // Propagate specific error messages from repository
                    return Result<int>.Failure(updateResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                // Save changes to the database (the new version and the updated template entity)
                var saveResult = await _unitOfWork.SaveAsync();

                if (!saveResult.IsCompleteSuccessfully)
                {
                    // Propagate save error
                    return Result<int>.Failure(saveResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                // Return the new testing version number (which the repository method now returns)
                return Result<int>.Success(updateResult.Data);
            }
            catch (Exception ex)
            {
                // Catch unexpected errors during handler execution
                 Console.WriteLine($"Error in UpdateTemplateHandler: {ex.Message}");
                return Result<int>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }
    }
}
```

**33. PDFGenerator.Web\Services\Auth\ForgotPasswordHandler.cs** (No Change)
**34. PDFGenerator.Web\Services\Auth\GetUserInfoByEmailHandler.cs** (No Change)
**35. PDFGenerator.Web\Services\Auth\LoginUserHandler.cs** (No Change)
**36. PDFGenerator.Web\Services\Auth\ResetPasswordHandler.cs** (No Change)

**37. PDFGenerator.Web\Services\PublishTemplateHandler.cs** (NEW)

Create a new handler for publishing the test version to production.

```csharp
// File: Handlers/PublishTemplateHandler.cs
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using PDFGenerator.Web.Dtos.Template;
using PdfGeneratorApp.Handlers; // Required for IHandler


namespace PDFGenerator.Web.Handlers // Using Web.Handlers namespace now
{
    // NEW interface
    public interface IPublishTemplateHandler : IHandler<PublishTemplateRequestDto, int>
    {
    }

    // NEW class
    public class PublishTemplateHandler : IPublishTemplateHandler
    {
        private readonly IUnitOfWork _unitOfWork;

        public PublishTemplateHandler(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }

        public async Task<Result<int>> HandleAsync(PublishTemplateRequestDto request)
        {
            try
            {
                // Need to get the template ID from the name first
                 var templateByNameResult = await _unitOfWork.Templates.GetProductionTemplateByNameAsync(request.TemplateName); // Use any getter that returns TemplateDataAccessDto to get ID

                 if (!templateByNameResult.IsCompleteSuccessfully || templateByNameResult.Data == null)
                 {
                      // Propagate template not found error
                     return Result<int>.Failure(templateByNameResult.ErrorMessages ?? ErrorMessageUserConst.TemplateNotFound);
                 }

                 int templateId = templateByNameResult.Data.Id;


                // Call the repository method to publish
                var publishResult = await _unitOfWork.Templates.PublishTemplateAsync(templateId);

                if (!publishResult.IsCompleteSuccessfully)
                {
                    // Propagate specific error messages from repository
                    return Result<int>.Failure(publishResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                // Save changes to the database
                var saveResult = await _unitOfWork.SaveAsync();

                if (!saveResult.IsCompleteSuccessfully)
                {
                    // Propagate save error
                    return Result<int>.Failure(saveResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                // Return the new production version number
                return Result<int>.Success(publishResult.Data);
            }
            catch (Exception ex)
            {
                // Catch unexpected errors during handler execution
                 Console.WriteLine($"Error in PublishTemplateHandler for template '{request.TemplateName}': {ex.Message}");
                return Result<int>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }
    }
}
```

**38. PDFGenerator.Web\Services\SoftDeleteTemplateVersionHandler.cs** (NEW)

Create a new handler for soft-deleting a template version.

```csharp
// File: Handlers/SoftDeleteTemplateVersionHandler.cs
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Infrastructure.Data.UnitOfWork;
using PDFGenerator.Web.Dtos.TemplateVersion;
using PdfGeneratorApp.Handlers; // Required for IHandler


namespace PDFGenerator.Web.Handlers // Using Web.Handlers namespace now
{
    // NEW interface
    public interface ISoftDeleteTemplateVersionHandler : IHandler<SoftDeleteVersionRequestDto, bool>
    {
    }

    // NEW class
    public class SoftDeleteTemplateVersionHandler : ISoftDeleteTemplateVersionHandler
    {
        private readonly IUnitOfWork _unitOfWork;

        public SoftDeleteTemplateVersionHandler(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }

        public async Task<Result<bool>> HandleAsync(SoftDeleteVersionRequestDto request)
        {
            try
            {
                // Before deleting the version, check if it's currently used as the Test or Prod version
                var versionResult = await _unitOfWork.Templates.GetVersionByIdAsync(request.VersionId);

                if (!versionResult.IsCompleteSuccessfully || versionResult.Data == null)
                {
                    // Version not found (or repository error), propagate
                     return Result<bool>.Failure(versionResult.ErrorMessages ?? $"Template Version with ID {request.VersionId} not found.");
                }

                var versionToDelete = versionResult.Data;

                 // Fetch the parent template to check Test/Prod version numbers
                 var templateResult = await _unitOfWork.Templates.GetByIdAsync(versionToDelete.TemplateId);

                 if (!templateResult.IsCompleteSuccessfully || templateResult.Data == null)
                 {
                     // Should not happen if version exists and has a valid TemplateId, but check defensively
                      return Result<bool>.Failure($"Could not find parent template for version ID {request.VersionId}.");
                 }

                 var parentTemplate = templateResult.Data;

                // Prevent deletion if it's the current Test or Production version
                if (versionToDelete.VersionNumber == parentTemplate.TestingVersionNumber)
                {
                    return Result<bool>.Failure($"Cannot delete version {versionToDelete.VersionNumber}. It is currently the Testing version.");
                }
                if (versionToDelete.VersionNumber == parentTemplate.ProductionVersionNumber)
                {
                     return Result<bool>.Failure($"Cannot delete version {versionToDelete.VersionNumber}. It is currently the Production version.");
                }


                // Call the repository method to soft delete
                var deleteResult = await _unitOfWork.TemplateVersions.SoftDeleteVersionAsync(request.VersionId);

                if (!deleteResult.IsCompleteSuccessfully)
                {
                    // Propagate specific error messages from repository
                    return Result<bool>.Failure(deleteResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                // Save changes to the database
                var saveResult = await _unitOfWork.SaveAsync();

                if (!saveResult.IsCompleteSuccessfully)
                {
                    // Propagate save error
                    return Result<bool>.Failure(saveResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
                }

                // Return the boolean result from the repository (indicating if it was found and marked deleted)
                return Result<bool>.Success(deleteResult.Data);
            }
            catch (Exception ex)
            {
                // Catch unexpected errors during handler execution
                 Console.WriteLine($"Error in SoftDeleteTemplateVersionHandler for version ID {request.VersionId}: {ex.Message}");
                return Result<bool>.Failure(ErrorMessageUserConst.ServerErrorNoMsg);
            }
        }
    }
}
```

**39. PDFGenerator.Web\Controllers\HomeController.cs**

Update `HomeController` to use the handler that gets the simple list with two versions.

```csharp
// File: Controllers/HomeController.cs
using Microsoft.AspNetCore.Mvc;
using PdfGeneratorApp.Handlers;
using PdfGeneratorApp.Common;
using Microsoft.AspNetCore.Authorization;
using PDFGenerator.Web.Dtos.Template; // Added for DTO

namespace PdfGeneratorApp.Controllers
{
    [Authorize]
    public class HomeController : Controller
    {
        // Use the handler that gets the simple list with both version numbers
        private readonly IGetTemplatesListHandler _getTemplatesListHandler;

        public HomeController(IGetTemplatesListHandler getTemplatesListHandler)
        {
            _getTemplatesListHandler = getTemplatesListHandler;
        }

        public async Task<IActionResult> Index()
        {
            // HandleAsync for IGetTemplatesListHandler takes object, pass null or a dummy object if no input is needed
            var result = await _getTemplatesListHandler.HandleAsync(null);

            if (!result.IsCompleteSuccessfully)
            {
                // Use TempData for user-friendly message and log the error
                 Console.WriteLine($"Error fetching template list: {result.ErrorMessages}");
                TempData["ErrorMessage"] = result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                // Return an empty list to the view on error, or redirect to an error page
                return View(new List<TemplateListDto>());
            }

            // Pass the list of TemplateListDto to the view
            return View(result.Data ?? new List<TemplateListDto>()); // Pass empty list if Data is null (unlikely)
        }
    }
}
```

**40. PDFGenerator.Web\Controllers\DocsController.cs**

Update `DocsController` to use the handler that gets templates for documentation (which now fetches based on the Production version).

```csharp
// File: Controllers/DocsController.cs
using Microsoft.AspNetCore.Mvc;
using PdfGeneratorApp.Handlers;
using PdfGeneratorApp.Common;
using Microsoft.AspNetCore.Authorization;
using PDFGenerator.Web.Dtos.Template; // Added for DTO

namespace PdfGeneratorApp.Controllers
{
    [Authorize]
    public class DocsController : Controller
    {
        private readonly IGetTemplatesDocHandler _getTemplatesDocHandler;

        public DocsController(IGetTemplatesDocHandler getTemplatesDocHandler)
        {
            _getTemplatesDocHandler = getTemplatesDocHandler;
        }

        // GET: /docs/templates
        public async Task<IActionResult> Templates()

        {
            // HandleAsync for IGetTemplatesDocHandler takes object, pass null
            var result = await _getTemplatesDocHandler.HandleAsync(null);

            if (!result.IsCompleteSuccessfully)
            {
                // Log the error detail
                Console.WriteLine($"Error fetching template docs: {result.ErrorMessages}");
                // Return a user-friendly message via TempData and show an empty list
                TempData["ErrorMessage"] = result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                return View(new List<TemplatesDocDto>());
            }

            // Pass the list of TemplatesDocDto to the view
            return View(result.Data ?? new List<TemplatesDocDto>()); // Pass empty list if Data is null (unlikely)
        }
    }
}
```

**41. PDFGenerator.Web\Controllers\PdfController.cs**

Update `PdfController` to use the handler for getting the *production* template (for the API endpoint) and the handler for getting the *testing* template (for the redirect to Design).

```csharp
// File: Controllers/PdfController.cs
using Microsoft.AspNetCore.Mvc;
using System.Text.Json;
using PdfGeneratorApp.Handlers;
using PdfGeneratorApp.Common;
using Microsoft.AspNetCore.Authorization;
using PDFGenerator.Web.Dtos.Template; // Added for DTOs
using PDFGenerator.Web.Handlers; // Added for new handler

namespace PdfGeneratorApp.Controllers
{
    // [Authorize] // API endpoint might not be authorized depending on use case, but Design is.
    // Let's keep [Authorize] at the controller level for simplicity based on other controllers.
    // If API is public, move [Authorize] to specific actions or remove.
    [Authorize]
    public class PdfController : Controller
    {
        // This handler gets the PRODUCTION version for the API POST endpoint
        private readonly IGetProductionTemplateHandler _getProductionTemplateHandler;

        // This handler gets the TESTING version for the GET redirect to Design
        private readonly IGetTemplateForDesignHandler _getTemplateForDesignHandler;


        private readonly IGeneratePdfHandler _generatePdfHandler;

        public PdfController(IGetProductionTemplateHandler getProductionTemplateHandler,
                             IGetTemplateForDesignHandler getTemplateForDesignHandler,
                             IGeneratePdfHandler generatePdfHandler)
        {
            _getProductionTemplateHandler = getProductionTemplateHandler;
            _getTemplateForDesignHandler = getTemplateForDesignHandler;
            _generatePdfHandler = generatePdfHandler;
        }

        // GET: /pdf/generate/{templateName} - Used to redirect to Design view
        [HttpGet("pdf/generate/{templateName}")]
        public async Task<IActionResult> Generate(string templateName)
        {
            // Use the handler that gets the TESTING version for the design view
            var result = await _getTemplateForDesignHandler.HandleAsync(templateName);

            if (!result.IsCompleteSuccessfully)
            {
                // Use TempData for user-friendly message and log the error
                Console.WriteLine($"Error getting template '{templateName}' for design: {result.ErrorMessages}");
                TempData["ErrorMessage"] = result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                 // Redirect to dashboard on failure
                return RedirectToAction("Index", "Home");
            }

            // Redirect to the Design action for the template, passing the template name
            // The Design action will fetch the details (specifically the TESTING version) again using its own handler.
            return RedirectToAction("Design", "Template", new { templateName = result.Data.Name });
        }

        // POST: /pdf/generate/{templateName} - API endpoint to generate PDF (uses PRODUCTION version)
        [HttpPost("pdf/generate/{templateName}")]
        [Consumes("application/json")]
        // Remove [Authorize] if API is public
        public async Task<IActionResult> Generate(string templateName, [FromBody] JsonElement requestBodyJson, [FromQuery] string mode = "outside")
        {
            var request = (templateName, requestBodyJson, mode);
            var result = await _generatePdfHandler.HandleAsync(request);

            if (!result.IsCompleteSuccessfully)
            {
                // Return appropriate HTTP status codes based on error type
                if (result.ErrorMessages == ErrorMessageUserConst.TemplateNotFound)
                {
                    return NotFound(result.ErrorMessages);
                }
                if (result.ErrorMessages == ErrorMessageUserConst.InvalidMode || result.ErrorMessages == ErrorMessageUserConst.InsideModeBodyNotObject)
                {
                    return BadRequest(result.ErrorMessages);
                }
                // Also handle version not found/deleted errors if they come up from the handler/repo
                 if (result.ErrorMessages != null && (result.ErrorMessages.Contains(ErrorMessageUserConst.VersionNotFound) || result.ErrorMessages.Contains("(or is deleted)")))
                 {
                     return BadRequest($"Production version not found or is deleted for template '{templateName}'."); // More specific error for API
                 }


                // Log the error for server-side visibility
                Console.WriteLine($"Error generating PDF for template '{templateName}' (Mode: {mode}): {result.ErrorMessages ?? "Unknown error"}");
                return StatusCode(500, result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);
            }

            // Return the PDF file
            // The filename convention might be improved, but keep existing for now.
            return File(result.Data, "application/pdf", $"{templateName}_{DateTime.Now:yyyyMMddHHmmss}.pdf");
        }
    }
}
```

**42. PDFGenerator.Web\Controllers\TemplateController.cs**

Modify `TemplateController` to handle the new Test/Prod versions, add actions for setting version references, publishing, and soft deleting versions.

```csharp
// File: Controllers/TemplateController.cs
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PDFGenerator.Web.Dtos.Template;
using PDFGenerator.Web.Dtos.TemplateVersion;
using PdfGeneratorApp.Common;
using PdfGeneratorApp.Data; // Keep DbContext dependency for GetDatabaseAliases
using PdfGeneratorApp.Handlers;
using PDFGenerator.Web.Handlers; // Added for new handlers

namespace PdfGeneratorApp.Controllers
{
    [Authorize]
    public class TemplateController : Controller
    {
        // Keep DbContext only if absolutely necessary (e.g., for non-entity-related access like config)
        // Getting DB aliases from config is fine here.
        private readonly ApplicationDbContext _context; // Used only for GetDatabaseAliases in this scope?
        private readonly IConfiguration _configuration; // Keep for getting database aliases

        // Renamed - gets template and its TESTING version for the Design GET view
        private readonly IGetTemplateForDesignHandler _getTemplateForDesignHandler;
        private readonly IUpdateTemplateHandler _updateTemplateHandler; // Updates the Testing version
        private readonly ICreateTemplateHandler _createTemplateHandler;
        private readonly IGetTemplateHistoryHandler _getTemplateHistoryHandler; // Gets history (excluding deleted)

        // Renamed - sets either Testing or Production version reference
        private readonly ISetTemplateVersionHandler _setTemplateVersionHandler;

        // NEW Handler - publishes Testing to Production
        private readonly IPublishTemplateHandler _publishTemplateHandler;

        // NEW Handler - soft deletes a version
        private readonly ISoftDeleteTemplateVersionHandler _softDeleteTemplateVersionHandler;


        public TemplateController(ApplicationDbContext context,
                                   IConfiguration configuration,
                                   IGetTemplateForDesignHandler getTemplateForDesignHandler, // Use new handler
                                   IUpdateTemplateHandler updateTemplateHandler,
                                   ICreateTemplateHandler createTemplateHandler,
                                   IGetTemplateHistoryHandler getTemplateHistoryHandler,
                                   ISetTemplateVersionHandler setTemplateVersionHandler, // Use new handler
                                   IPublishTemplateHandler publishTemplateHandler, // Inject new handler
                                   ISoftDeleteTemplateVersionHandler softDeleteTemplateVersionHandler) // Inject new handler
        {
            _context = context; // Keep for GetDatabaseAliases
            _configuration = configuration;
            _getTemplateForDesignHandler = getTemplateForDesignHandler;
            _updateTemplateHandler = updateTemplateHandler;
            _createTemplateHandler = createTemplateHandler;
            _getTemplateHistoryHandler = getTemplateHistoryHandler;
            _setTemplateVersionHandler = setTemplateVersionHandler;
            _publishTemplateHandler = publishTemplateHandler; // Assign new handler
            _softDeleteTemplateVersionHandler = softDeleteTemplateVersionHandler; // Assign new handler
        }

        // Helper to get database aliases from config
        private List<string> GetDatabaseAliases()
        {
            // Access config directly, not via DbContext
            return _configuration.GetSection("InternalDataConnections").GetChildren().Select(c => c.Key).ToList();
        }

        // GET: /templates/design/{templateName}
        [HttpGet("templates/design/{templateName}")]
        public async Task<IActionResult> Design(string templateName)
        {
            // Use the handler that gets the template + TESTING version for design
            Result<TemplateDetailDto> result = await _getTemplateForDesignHandler.HandleAsync(templateName);

            if (!result.IsCompleteSuccessfully)
            {
                // Use TempData for user message and log error
                Console.WriteLine($"Error getting template '{templateName}' for design: {result.ErrorMessages}");
                TempData["ErrorMessage"] = result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                // Redirect to dashboard on failure
                return RedirectToAction("Index", "Home");
            }

            var templateDto = result.Data;
            ViewBag.DatabaseAliases = GetDatabaseAliases(); // Pass aliases to view
            return View(templateDto);
        }

        // POST: /templates/design/{templateName} - Saves changes as a NEW version, sets it as TESTING
        [HttpPost("templates/design/{templateName}")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Design(string templateName, [Bind("Id,Description,HtmlContent,ExampleJsonData,InternalDataConfigJson")] TemplateUpdateDto templateDto)
        {
            // Re-fetch template details to pass to the view if validation fails
            // Use the handler that gets the TESTING version
            Result<TemplateDetailDto> detailDtoOnErrorResult = await _getTemplateForDesignHandler.HandleAsync(templateName);

            // Check if re-fetch for error view succeeded
            TemplateDetailDto detailDtoOnError = null;
            if (detailDtoOnErrorResult.IsCompleteSuccessfully && detailDtoOnErrorResult.Data != null)
            {
                 detailDtoOnError = detailDtoOnErrorResult.Data;
                 // Update the re-fetched DTO with the user's submitted (potentially invalid) data for display
                 detailDtoOnError.Description = templateDto.Description;
                 detailDtoOnError.HtmlContent = templateDto.HtmlContent;
                 detailDtoOnError.ExampleJsonData = templateDto.ExampleJsonData;
                 detailDtoOnError.InternalDataConfigJson = templateDto.InternalDataConfigJson;
            } else {
                 // If re-fetch failed (e.g. template deleted), cannot render the view with errors
                 // Log and redirect, or show a generic error page
                 Console.WriteLine($"Error re-fetching template '{templateName}' for update validation failure: {detailDtoOnErrorResult.ErrorMessages}");
                 TempData["ErrorMessage"] = detailDtoOnErrorResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                 return RedirectToAction("Index", "Home");
            }


            ViewBag.DatabaseAliases = GetDatabaseAliases(); // Pass aliases to view


            if (!ModelState.IsValid)
            {
                // Return the view with validation errors, using the re-fetched + updated DTO
                 return View(detailDtoOnError);
            }


            // Use the handler to update the template (creates new version, sets as TESTING)
            var updateResult = await _updateTemplateHandler.HandleAsync(templateDto);

            if (!updateResult.IsCompleteSuccessfully)
            {
                // Add handler error to model state for display
                ModelState.AddModelError("", updateResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);

                // Re-validate the specific fields that might have handler-level errors (like JSON format)
                // This is necessary because the handler might add errors not caught by ModelState.IsValid initially
                 if (updateResult.ErrorMessages == ErrorMessageUserConst.InternalDataConfigInvalidJson || updateResult.ErrorMessages == ErrorMessageUserConst.InternalDataConfigNotObject)
                 {
                     ModelState.AddModelError(nameof(TemplateUpdateDto.InternalDataConfigJson), updateResult.ErrorMessages);
                 }
                 else if (updateResult.ErrorMessages == ErrorMessageUserConst.ExampleJsonGenerationFailed)
                 {
                     // You might want a separate field for this error, or just add to model state summary
                     ModelState.AddModelError(nameof(TemplateUpdateDto.HtmlContent), updateResult.ErrorMessages); // Associate with HTML if JSON generation failed from it
                 }
                 // Add other handler errors as needed

                // Return the view with updated model state errors
                return View(detailDtoOnError); // Still use the re-fetched DTO
            }

            // On successful update, the handler returns the NEW Testing version number
            TempData["Message"] = $"Template '{templateName}' updated. New Testing Version is {updateResult.Data}!";

            // Redirect back to the design view to show the newly saved version
            return RedirectToAction(nameof(Design), new { templateName = templateName });
        }

        // GET: /templates/create
        public IActionResult Create()
        {
            ViewBag.DatabaseAliases = GetDatabaseAliases(); // Pass aliases to view
            // Provide an empty DTO for the view form
            return View(new TemplateCreateDto { HtmlContent = "" });
        }

        // POST: /templates/create - Creates a new template and its initial version (Test and Prod)
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create([Bind("Name,HtmlContent,Description,ExampleJsonData,InternalDataConfigJson")] TemplateCreateDto templateDto)
        {
            ViewBag.DatabaseAliases = GetDatabaseAliases(); // Pass aliases back to view on error

            if (!ModelState.IsValid)
            {
                return View(templateDto); // Return view with validation errors
            }

            // Use the handler to create the new template
            var result = await _createTemplateHandler.HandleAsync(templateDto);

            if (!result.IsCompleteSuccessfully)
            {
                // Add handler error to model state for display
                ModelState.AddModelError("", result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg);

                 // Add field-specific errors if they come from the handler
                if (result.ErrorMessages == ErrorMessageUserConst.TemplateNameExists)
                {
                    ModelState.AddModelError("Name", result.ErrorMessages);
                }
                else if (result.ErrorMessages == ErrorMessageUserConst.InternalDataConfigInvalidJson || result.ErrorMessages == ErrorMessageUserConst.InternalDataConfigNotObject)
                {
                    ModelState.AddModelError(nameof(TemplateCreateDto.InternalDataConfigJson), result.ErrorMessages);
                }
                 else if (result.ErrorMessages == ErrorMessageUserConst.ExampleJsonGenerationFailed)
                 {
                     ModelState.AddModelError(nameof(TemplateCreateDto.HtmlContent), result.ErrorMessages);
                 }
                 // Add other handler errors as needed


                return View(templateDto); // Return view with handler errors
            }

            // On successful creation, the handler returns the template name
            TempData["Message"] = $"Template '{result.Data}' created successfully!";
            // Redirect to the design view of the newly created template (which will show version 1)
            return RedirectToAction(nameof(Design), new { templateName = result.Data });
        }

        // GET: /templates/{templateName}/history
        [HttpGet("templates/{templateName}/history")]
        public async Task<IActionResult> History(string templateName)
        {
            // Fetch template details (including Test/Prod versions) to show in the header
            var templateDetailResult = await _getTemplateForDesignHandler.HandleAsync(templateName); // Can use either Test or Prod getter here, just need template details

            if (!templateDetailResult.IsCompleteSuccessfully || templateDetailResult.Data == null)
            {
                Console.WriteLine($"Error getting template '{templateName}' for history view: {templateDetailResult.ErrorMessages}");
                TempData["ErrorMessage"] = templateDetailResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                 // Redirect or show error view
                return RedirectToAction("Index", "Home");
            }

            var templateDetailDto = templateDetailResult.Data;

            // Fetch historical versions (excluding deleted by default) for the given template ID
            var versionsResult = await _getTemplateHistoryHandler.HandleAsync(templateDetailDto.Id);

            if (!versionsResult.IsCompleteSuccessfully)
            {
                Console.WriteLine($"Error fetching history for template '{templateName}' (ID: {templateDetailDto.Id}): {versionsResult.ErrorMessages}");
                TempData["ErrorMessage"] = versionsResult.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                ViewBag.TemplateVersions = new List<TemplateVersionDto>(); // Pass empty list on error
                return View(templateDetailDto); // Still show template header info
            }

            ViewBag.TemplateVersions = versionsResult.Data ?? new List<TemplateVersionDto>(); // Pass the list of versions to the view
            return View(templateDetailDto); // Pass template header info
        }


        // POST: /templates/{templateName}/set-version/{versionNumber}/{versionType} (renamed from revert)
        // Allows setting either Testing or Production version reference
        [HttpPost("templates/{TemplateName}/set-version/{VersionNumber}")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> SetVersion([FromRoute] string TemplateName, int VersionNumber, [FromForm] string VersionType) // Get VersionType from form data
        {
             // Validate VersionType string input before creating the DTO
            if (!Enum.TryParse<TemplateVersionReferenceType>(VersionType, true, out var parsedVersionType))
             {
                 TempData["Error"] = "Invalid version type specified. Must be 'Testing' or 'Production'.";
                 return RedirectToAction(nameof(History), new { templateName = TemplateName });
             }

            var request = new SetTemplateVersionRequestDto
            {
                TemplateName = TemplateName,
                VersionNumber = VersionNumber,
                VersionType = parsedVersionType // Use the parsed enum value
            };


            var result = await _setTemplateVersionHandler.HandleAsync(request);

            if (!result.IsCompleteSuccessfully)
            {
                 // Log error detail
                 Console.WriteLine($"Error setting {VersionType} version for template '{TemplateName}' to {VersionNumber}: {result.ErrorMessages}");
                 // Pass error message to history view
                TempData["ErrorMessage"] = result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                // Redirect back to history page
                return RedirectToAction(nameof(History), new { templateName = request.TemplateName });
            }

            // On success, the handler returns the version number that was set
            TempData["Message"] = $"{request.VersionType} version for template '{request.TemplateName}' successfully set to Version {result.Data}.";
            // Redirect back to history page
            return RedirectToAction(nameof(History), new { templateName = request.TemplateName });
        }

        // POST: /templates/{templateName}/publish (NEW ACTION)
        // Publishes the current Testing version to Production
        [HttpPost("templates/{templateName}/publish")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Publish([FromRoute] string templateName)
        {
            var request = new PublishTemplateRequestDto { TemplateName = templateName };

            var result = await _publishTemplateHandler.HandleAsync(request);

            if (!result.IsCompleteSuccessfully)
            {
                 // Log error detail
                 Console.WriteLine($"Error publishing template '{templateName}': {result.ErrorMessages}");
                 // Pass error message to design view
                TempData["ErrorMessage"] = result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                // Redirect back to the design page
                return RedirectToAction(nameof(Design), new { templateName = templateName });
            }

            // On success, the handler returns the new Production version number
            TempData["Message"] = $"Template '{templateName}' successfully published to Production. Production Version is now {result.Data}.";
            // Redirect back to the design page
            return RedirectToAction(nameof(Design), new { templateName = templateName });
        }

        // POST: /templates/versions/{versionId}/delete (NEW ACTION)
        // Soft deletes a specific template version
        [HttpPost("templates/versions/{versionId}/delete")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> SoftDeleteVersion([FromRoute] int versionId)
        {
            // Need to get the template name to redirect back to history
             var versionResult = await _unitOfWork.Templates.GetVersionByIdAsync(versionId);
             string templateName = null;
             if (versionResult.IsCompleteSuccessfully && versionResult.Data != null)
             {
                 // Get the parent template name via the version's TemplateId
                 var templateResult = await _unitOfWork.Templates.GetByIdAsync(versionResult.Data.TemplateId);
                 if (templateResult.IsCompleteSuccessfully && templateResult.Data != null)
                 {
                      templateName = templateResult.Data.Name;
                 }
             }

             // If we couldn't find the template name, redirect to dashboard with error
             if (string.IsNullOrEmpty(templateName))
             {
                  TempData["ErrorMessage"] = $"Could not find parent template for version ID {versionId}. Cannot soft delete.";
                  return RedirectToAction("Index", "Home");
             }


            var request = new SoftDeleteVersionRequestDto { VersionId = versionId };

            var result = await _softDeleteTemplateVersionHandler.HandleAsync(request);

            if (!result.IsCompleteSuccessfully)
            {
                 // Log error detail
                 Console.WriteLine($"Error soft deleting version ID {versionId} for template '{templateName}': {result.ErrorMessages}");
                 // Pass error message to history view
                TempData["ErrorMessage"] = result.ErrorMessages ?? ErrorMessageUserConst.ServerErrorNoMsg;
                // Redirect back to history page
                return RedirectToAction(nameof(History), new { templateName = templateName });
            }

            // On success, the handler returns true if deleted (or already deleted)
            TempData["Message"] = $"Template version {versionResult.Data.VersionNumber} for template '{templateName}' successfully soft deleted.";
            // Redirect back to history page
            return RedirectToAction(nameof(History), new { templateName = templateName });
        }
    }
}
```

**43. PDFGenerator.Web\Views\Home\Index.cshtml**

Update `Index.cshtml` to display Test and Prod version numbers.

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
            <div class="stat-number">N/A</div> @* Placeholder - update with real stats if available *@
            <div class="stat-label">Generated PDFs</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">N/A</div> @* Placeholder - update with real stats if available *@
            <div class="stat-label">Active Users</div>
        </div>
    </div>

    <div class="action-bar">
        <div class="search-box">
            <i class="fas fa-search search-icon"></i>
            <input type="text" id="searchInput" placeholder="Search templates by name..." class="form-control" /> @* Search only by name now *@
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
                @* Search only by name now, as description is per version *@
                <div class="template-card" data-name="@template.Name.ToLower()">
                    <div class="template-header">
                        <div class="template-icon">
                            <i class="fas fa-file-alt"></i>
                        </div>
                        <div class="version-badges"> @* Changed to display both versions *@
                             <span class="badge bg-primary me-1" title="Production Version"><i class="fas fa-cogs"></i> v @template.ProductionVersionNumber</span>
                             <span class="badge bg-secondary" title="Testing Version"><i class="fas fa-flask"></i> v @template.TestingVersionNumber</span>
                        </div>
                    </div>
                    <div class="template-info">
                        <h3 class="template-name">
                            <a asp-controller="Template" asp-action="Design" asp-route-templateName="@template.Name" title="Edit @template.Name">
                                @template.Name
                            </a>
                        </h3>
                        @* Description is per version, not easily displayed here without fetching version data * @
                        @* <p class="template-description" title="@template.Description">@(string.IsNullOrWhiteSpace(template.Description) ? "No description provided." : template.Description)</p> *@
                        <div class="template-meta">
                            <div class="meta-item">
                                <i class="fas fa-calendar-alt"></i>
                                <span>Modified: @template.LastModified.ToString("MMM dd, yyyy")</span>
                            </div>
                        </div>
                    </div>
                    <div class="template-actions">
                        <a asp-controller="Template" asp-action="Design" asp-route-templateName="@template.Name" class="btn btn-sm btn-design" title="Edit Testing Version"> @* Link to Design (Testing) * @
                            <i class="fas fa-paint-brush"></i>
                            Design
                        </a>
                        <a asp-controller="Template" asp-action="History" asp-route-templateName="@template.Name" class="btn btn-sm btn-info">
                            <i class="fas fa-history"></i>
                            History
                        </a>
                         @* Optional: Add a quick link to generate the Production PDF (opens in new tab?) *@
                         <a href="@Url.Action("Generate", "Pdf", new { templateName = template.Name })" target="_blank" class="btn btn-sm btn-success" title="Generate Production PDF">
                            <i class="fas fa-file-pdf"></i> PDF
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
            // const totalTemplatesStat = document.getElementById('totalTemplatesStat'); // No longer updated by JS

            function filterTemplates() {
                if (!searchInput || !templatesGrid) return;

                const searchTerm = searchInput.value.toLowerCase().trim();
                let visibleCount = 0;

                templateCards.forEach(card => {
                    const name = card.dataset.name.toLowerCase();
                    // Search only by name now
                    const isMatch = name.includes(searchTerm);

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
                    // If there are no cards initially, empty state is already shown
                    if(emptyState) emptyState.style.display = 'block';
                    templatesGrid.style.display = 'none';
                }


            }

            if (searchInput) {
                searchInput.addEventListener('input', filterTemplates);
            }

            // Add simple fade-in animation
            templateCards.forEach((card, index) => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)'; // Start slightly below
                setTimeout(() => {
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)'; // End at original position
                    card.style.transition = 'opacity 0.4s ease-out, transform 0.4s ease-out';
                }, index * 70); // Stagger the animation
            });
        });
    </script>
}
```

**44. PDFGenerator.Web\Views\Docs\Templates.cshtml**

No significant changes needed, as the handler will fetch based on the Production version, and the DTO structure didn't change properties. Update description text slightly.

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
            Test and understand the PDF generation API endpoints. Each template's <strong>Production Version</strong> is available here.
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
                        </button>
                    </h2>
                    <div id="@collapseId" class="accordion-collapse collapse" aria-labelledby="@headingId" data-bs-parent="#templateDocsAccordion">
                        <div class="accordion-body">
                            <h5>Endpoint Summary</h5>
                            <p>Generates a PDF document based on the <strong>Production Version</strong> of the <strong>@template.Name</strong> template and the provided JSON data (Outside mode) or internal configuration (Inside mode) using optional parameters.</p>

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
                                    <small class="form-text text-muted">This is the configuration stored for this template's Production Version. Data resolution happens on the server using this config.</small>
                                </div>

                                <!-- Parameters Input for INSIDE Mode -->
                                <div class="form-group mb-3 inside-parameters-section" style="display:none;">
                                    <label for="@insideParametersJsonTextareaId" class="form-label fw-semibold">Inside Parameters JSON for Inside Mode</label>
                                    <textarea class="form-control inside-parameters-json" id="@insideParametersJsonTextareaId" rows="5" style="font-family: monospace; font-size: 0.875em;">{}</textarea>
                                    <small class="form-text text-muted">Provide JSON parameters to be used in the Internal Data Configuration (e.g., <code>{ "userNID": "12345" }</code>). This JSON will be nested under a "parameters" key in the request body when using "Inside" mode.</small>
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
            <p>Create some templates first to see their API documentation here. The documentation is generated from the <strong>Production Version</strong> of each template.</p>
             <div class="mt-3">
                <a asp-controller="Template" asp-action="Create" class="btn btn-primary">
                    <i class="fas fa-plus"></i>
                    Create New Template
                </a>
            </div>
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
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script> @* Ensure jQuery is included if using $ *@
    <script>
        $(document).ready(function() {

            // --- Mode Selection Toggle ---
            $('.accordion-body').on('change', '.mode-radio', function() { // Delegate event handling
                var $tryItOutSection = $(this).closest('.try-it-out-section');
                var selectedMode = $(this).val();

                // Hide all mode-specific sections first
                $tryItOutSection.find('.data-config-section').hide();
                $tryItOutSection.find('.inside-parameters-section').hide();

                // Show sections based on selected mode
                if (selectedMode === 'outside') {
                     $tryItOutSection.find(`.data-config-section[data-mode="outside"]`).show();
                } else if (selectedMode === 'inside') {
                     $tryItOutSection.find(`.data-config-section[data-mode="inside"]`).show();
                     $tryItOutSection.find('.inside-parameters-section').show();
                }

                 // Clear previous response when switching mode
                 $tryItOutSection.find('.clear-response-btn').click();
            });


            // --- Execute Button Logic ---
             $('.accordion-body').on('click', '.execute-btn', function() { // Delegate event handling
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
                     var $jsonPayloadTextarea = $tryItOutSection.find('.data-config-section[data-mode="outside"] .json-payload');
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
                    var $insideParametersTextarea = $tryItOutSection.find('.inside-parameters-section .inside-parameters-json');
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

                // Include CSRF token if your site requires it on API POSTs
                // const antiForgeryToken = $('input[name="__RequestVerificationToken"]').val();
                const headers = {
                    'Content-Type': 'application/json'
                    // 'RequestVerificationToken': antiForgeryToken // Uncomment if needed
                };


                fetch(url, {
                    method: 'POST',
                    headers: headers,
                    body: JSON.stringify(requestBodyPayload)
                })
                .then(response => {
                    const contentType = response.headers.get('content-type');
                    if (!response.ok) {
                         return response.text().then(text => {
                             throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}\n\nResponse Body:\n${text}`);
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
                        const suggestedFilename = `${templateName}_${selectedMode}_API_Test_${new Date().toISOString().slice(0, 19).replace(/[-:T]/g, "")}.pdf`;
                        a.href = url;
                        a.download = suggestedFilename;
                        a.innerHTML = `<i class="fas fa-download me-1"></i> Download ${suggestedFilename}`;
                        a.className = 'btn btn-sm btn-success d-block mt-2';
                        $responseOutputDiv.html('PDF generated successfully.'); // Use html() to clear previous content
                        $responseOutputDiv.append(a);
                        $responseStatusDiv.addClass('alert alert-success');
                    } else {
                         // Display non-PDF responses (errors, warnings, etc.)
                        $responseOutputDiv.text(result.text);
                        if(result.ok){
                            $responseStatusDiv.addClass('alert alert-warning'); // E.g. 200 but not PDF
                        } else {
                             $responseStatusDiv.addClass('alert alert-danger'); // E.g. 4xx or 5xx
                        }
                    }
                })
                .catch(error => {
                    console.error('Fetch Error:', error);
                    $responseStatusDiv.html('<strong>Error:</strong> An API error occurred').addClass('alert alert-danger');
                    $responseOutputDiv.text(error.message).addClass('text-danger');
                })
                .finally(() => {
                    $button.prop('disabled', false).html('<i class="fas fa-play-circle"></i> Execute');
                    $responseSection.show();
                    $clearButton.show();
                });
            });

            // --- Clear Response Button ---
            $('.accordion-body').on('click', '.clear-response-btn', function() { // Delegate event handling
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


            // Format JSON textareas on load for all accordions
            $('.accordion-body .json-payload').each(function() {
                 formatJsonTextarea($(this));
            });
             $('.accordion-body .data-config-section[data-mode="inside"] textarea').each(function() {
                 formatJsonTextarea($(this)); // Format the read-only internal config display
            });
             $('.accordion-body .inside-parameters-json').each(function() {
                 formatJsonTextarea($(this)); // Format the new inside parameters input
            });

             // Initialize the UI visibility based on the default selected mode (outside) for each accordion item
             $('.accordion-body').each(function() {
                 var $body = $(this);
                 $body.find('.mode-radio:checked').trigger('change'); // Trigger change for initially checked radio
             });
        });
    </script>
}
```

**45. PDFGenerator.Web\Views\Template\Design.cshtml**

Update `Design.cshtml` to display Test/Prod version numbers and add the "Publish to Production" button.

```html
@using PDFGenerator.Web.Dtos.Template
@model TemplateDetailDto
@{
    ViewData["Title"] = $"Design Template: {Model.Name} (v{Model.VersionNumber})"; @* Include current version in title *@
    var dbAliases = ViewBag.DatabaseAliases as List<string> ?? new List<string>();
}

<div class="container">
    <div class="page-header">
        <h1>@ViewData["Title"]</h1>
        <p class="page-subtitle">You are editing <strong>Version @Model.VersionNumber</strong> (the current Testing version) of the <strong>@Model.Name</strong> template.</p>
    </div>

    <div class="row">
        <div class="col-md-12">
            <form asp-action="Design" asp-route-templateName="@Model.Name" method="post">
                <div asp-validation-summary="ModelOnly" class="text-danger"></div>
                <input type="hidden" asp-for="Id" /> @* Keep Template ID * @
                @* Hidden inputs for version-specific details that are part of the Model but not edited directly in these fields * @
                <input type="hidden" asp-for="VersionNumber" />
                <input type="hidden" asp-for="CreatedDate" />
                <input type="hidden" asp-for="IsDeleted" /> @* Soft delete status of THIS version * @

                <div class="row mb-3">
                    <div class="col-md-4">
                         <label class="control-label">Template Name:</label>
                         <input value="@Model.Name" class="form-control" readonly />
                    </div>
                     <div class="col-md-4">
                         <label class="control-label">Production Version:</label>
                         <input value="v @Model.ProductionVersionNumber" class="form-control" readonly />
                    </div>
                     <div class="col-md-4">
                         <label class="control-label">Testing Version:</label>
                         <input value="v @Model.TestingVersionNumber" class="form-control" readonly />
                    </div>
                </div>

                <div class="form-group mb-3">
                    <label class="control-label">Template Last Modified:</label>
                    <input value="@Model.LastModified.ToString("g")" class="form-control" readonly />
                </div>


                <div class="form-group mb-3">
                    <label asp-for="Description" class="control-label"></label>
                    <input asp-for="Description" class="form-control" />
                    <span asp-validation-for="Description" class="text-danger"></span>
                     <small class="form-text text-muted">Describe the changes in this specific version (v@Model.VersionNumber).</small>
                </div>

                <div class="form-group mb-3">
                    <label asp-for="HtmlContent" class="control-label"></label>
                    <textarea asp-for="HtmlContent" class="form-control" rows="15" id="htmlEditor"></textarea>
                    <span asp-validation-for="HtmlContent" class="text-danger"></span>
                    <small class="form-text text-muted">Use <code>&lt;&lt;FieldName&gt;&gt;</code> for dynamic data placeholders and <code>${{condition ? true_part : false_part}}</code> for conditionals.</small>
                </div>

                <hr class="my-4">

                <h5>Data Configuration:</h5>
                <p class="text-muted">Define how placeholders in the HTML content will be populated for "Outside" (API provided) and "Inside" (system sourced) data modes. Configurations below apply to <strong>Version @Model.VersionNumber</strong>.</p>

                 <!-- Placeholder list -->
                 <div class="card card-body mb-3">
                     <h6>Detected Placeholders (from HTML):</h6>
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

                <div class="form-group mt-4 button-group"> @* Use a class for layout *@
                    <input type="submit" value="Save Changes (New Testing Version)" class="btn btn-primary" /> @* Clarified button text *@
                    <a asp-action="Index" asp-controller="Home" class="btn btn-secondary">Back to Templates</a>
                    <a asp-controller="Template" asp-action="History" asp-route-templateName="@Model.Name" class="btn btn-info">View History</a>
                    <button type="button" id="downloadPdfBtn" class="btn btn-success" title="Generate PDF using Example JSON Data (Testing Version)">Download Test PDF</button>
                    @* NEW Button: Publish to Production *@
                    @if (Model.TestingVersionNumber != Model.ProductionVersionNumber) // Only show if Testing is different from Production
                    {
                        <form asp-action="Publish" asp-route-templateName="@Model.Name" method="post" class="d-inline publish-form needs-confirmation" data-confirmation-message="Are you sure you want to publish Testing Version @Model.TestingVersionNumber to Production?">
                             @Html.AntiForgeryToken()
                             <button type="submit" class="btn btn-warning ms-2" title="Set Production Version to Testing Version">
                                 <i class="fas fa-arrow-circle-up"></i> Publish to Production (v@Model.TestingVersionNumber)
                             </button>
                        </form>
                    }
                     @if (Model.TestingVersionNumber == Model.ProductionVersionNumber) // Indicate when Test == Prod
                     {
                          <span class="badge bg-success ms-2 p-2" title="Testing and Production versions are currently the same"><i class="fas fa-check-circle"></i> Testing Version is Production</span>
                     }
                </div>
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

            // Function to update the detected placeholders list
            function updatePlaceholdersList(html) {
                 // Use the same regex that matches Summernote's output
                 const placeholderRegex = /&lt;&lt;(\w+)&gt;&gt;/g;
                 let match;
                 const placeholders = new Set();

                 while ((match = placeholderRegex.exec(html)) !== null) {
                      placeholders.add(match[1]); // Add just the field name
                 }

                 placeholderListElement.empty();
                 if (placeholders.size === 0) {
                      placeholderListElement.html('<li class="list-inline-item"><em>(No data placeholders detected)</em></li>');
                 } else {
                      placeholders.forEach(placeholder => {
                           placeholderListElement.append(`<li class="list-inline-item"><code>&lt;&lt;${placeholder}&gt;&gt;</code></li>`); // Display using entities
                      });
                 }

                 // --- Future Enhancement: Dynamic UI connection here ---
            }

            // Auto-format JSON data for readability on load (for both fields)
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
                var mode = 'outside'; // For this test button, always use 'outside' mode

                // Validate JSON first
                try {
                    var payload = exampleJsonData.trim() === "" ? {} : JSON.parse(exampleJsonData);
                } catch (e) {
                    alert('Error: Invalid JSON in Example JSON Data field. Please correct it before testing.');
                    console.error('JSON Parse Error:', e);
                    return;
                }

                // Add mode as a query parameter
                 const url = new URL(endpoint, window.location.origin);
                 url.searchParams.append('mode', mode);


                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                         // Include CSRF token if your site requires it on this POST
                         // 'RequestVerificationToken': $('input[name="__RequestVerificationToken"]').val()
                    },
                    body: JSON.stringify(payload)
                })
                .then(response => {
                    if (!response.ok) {
                        return response.text().then(text => {
                            throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}\n\nResponse Body:\n${text}`);
                        });
                    }
                    return response.blob();
                })
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    // Suggest filename including version number and mode
                    const suggestedFilename = `${templateName}_v${@Model.VersionNumber}_${mode}_Test.pdf`;
                    a.href = url;
                    a.download = suggestedFilename;
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

            // Confirmation for publish form
            document.querySelectorAll('.publish-form.needs-confirmation').forEach(form => {
                form.addEventListener('submit', function (event) {
                    const message = this.dataset.confirmationMessage || 'Are you sure?';
                    if (!confirm(message)) {
                        event.preventDefault();
                    }
                });
            });


            // Initial placeholder detection on page load
             updatePlaceholdersList(htmlEditor.summernote('code'));

        });
    </script>

}
```

**46. PDFGenerator.Web\Views\Template\History.cshtml**

Update `History.cshtml` to display soft delete status, Test/Prod version numbers, and add buttons for setting versions and soft deleting.

```html
@using PDFGenerator.Web.Dtos.Template
@using PDFGenerator.Web.Dtos.TemplateVersion
@model TemplateDetailDto @* Use TemplateDetailDto to get current Test/Prod versions *@
@{
    var versions = ViewBag.TemplateVersions as List<TemplateVersionDto>;
    ViewData["Title"] = $"History for {Model.Name}";
}

<div class="container">
    <div class="page-header">
        <h1>@ViewData["Title"]</h1>
        <p class="page-subtitle">Review past versions of the template.
            Current Production Version: <strong>v@Model.ProductionVersionNumber</strong>.
            Current Testing Version: <strong>v@Model.TestingVersionNumber</strong>.
        </p>
    </div>

    @if (versions != null && versions.Any())
    {
        <div class="table-container">
            <table class="table table-striped table-hover"> @* Added styling *@
                <thead>
                    <tr>
                        <th>Version</th>
                        <th>Created Date</th>
                        <th>Status</th> @* Added Status column *@
                        <th>Description</th>
                        <th>Internal Data Config</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    @foreach (var version in versions)
                    {
                        // Highlight row if it's the current Test or Prod version
                        <tr class="@(version.VersionNumber == Model.TestingVersionNumber ? "table-info" : "") @(version.VersionNumber == Model.ProductionVersionNumber ? "table-success" : "") @(version.IsDeleted ? "table-danger text-muted" : "")">
                            <td class="version-number">
                                @version.VersionNumber
                                @if (version.VersionNumber == Model.ProductionVersionNumber)
                                {
                                    <span class="badge bg-success ms-2 p-1" title="Current Production Version"><i class="fas fa-cogs"></i> Prod</span>
                                }
                                @if (version.VersionNumber == Model.TestingVersionNumber)
                                {
                                     <span class="badge bg-secondary ms-2 p-1" title="Current Testing Version"><i class="fas fa-flask"></i> Test</span>
                                }
                            </td>
                             <td>@version.CreatedDate.ToString("yyyy-MM-dd HH:mm")</td> @* Standardize date format *@
                            <td> @* Status cell *@
                                @if (version.IsDeleted)
                                {
                                     <span class="badge bg-danger p-1"><i class="fas fa-trash-alt"></i> Deleted</span>
                                }
                                @* Add other statuses if needed, e.g., "Active" (default if not deleted) *@
                            </td>
                            <td style="max-width: 200px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="@version.Description">
                                @(string.IsNullOrWhiteSpace(version.Description) ? "N/A" : version.Description)
                            </td>
                            <td style="max-width: 250px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="@version.InternalDataConfigJson">
                                @(string.IsNullOrWhiteSpace(version.InternalDataConfigJson) ? "{}" : version.InternalDataConfigJson)
                            </td>
                            <td class="actions-column">
                                @* Action Buttons *@
                                @* View Details (Optional: Add button/modal to show HTML/JSON) *@
                                @* <button type="button" class="btn btn-sm btn-outline-secondary" title="View Full Content" data-bs-toggle="modal" data-bs-target="#versionDetailModal" data-version-id="@version.Id">
                                     <i class="fas fa-eye"></i> View
                                 </button> *@

                                @* Set as Testing Version Button *@
                                @if (!version.IsDeleted && version.VersionNumber != Model.TestingVersionNumber) // Cannot set deleted version or set to itself
                                {
                                    <form asp-action="SetVersion" asp-route-templateName="@Model.Name" asp-route-versionNumber="@version.VersionNumber" method="post" class="d-inline needs-confirmation" data-confirmation-message="Are you sure you want to set TESTING version for template '@Model.Name' to version @version.VersionNumber?">
                                        @Html.AntiForgeryToken()
                                        @* Pass VersionType as a hidden input or form value *@
                                        <input type="hidden" name="VersionType" value="@PDFGenerator.Web.Dtos.Template.TemplateVersionReferenceType.Testing" />
                                        <button type="submit" class="btn btn-sm btn-secondary" title="Set as Testing Version">
                                            <i class="fas fa-flask"></i> Set Test
                                        </button>
                                    </form>
                                }

                                @* Set as Production Version Button *@
                                @if (!version.IsDeleted && version.VersionNumber != Model.ProductionVersionNumber) // Cannot set deleted version or set to itself
                                {
                                    <form asp-action="SetVersion" asp-route-templateName="@Model.Name" asp-route-versionNumber="@version.VersionNumber" method="post" class="d-inline ms-1 needs-confirmation" data-confirmation-message="Are you sure you want to set PRODUCTION version for template '@Model.Name' to version @version.VersionNumber? This will become the version used by the API endpoint.">
                                        @Html.AntiForgeryToken()
                                         @* Pass VersionType as a hidden input or form value *@
                                        <input type="hidden" name="VersionType" value="@PDFGenerator.Web.Dtos.Template.TemplateVersionReferenceType.Production" />
                                        <button type="submit" class="btn btn-sm btn-success" title="Set as Production Version">
                                            <i class="fas fa-cogs"></i> Set Prod
                                        </button>
                                    </form>
                                }

                                 @* Soft Delete Button *@
                                @if (!version.IsDeleted && version.VersionNumber != Model.TestingVersionNumber && version.VersionNumber != Model.ProductionVersionNumber) // Can only delete if not already deleted AND not current Test/Prod
                                {
                                     <form asp-action="SoftDeleteVersion" asp-route-versionId="@version.Id" method="post" class="d-inline ms-1 needs-confirmation" data-confirmation-message="Are you sure you want to soft delete version @version.VersionNumber? It will no longer appear in the history list by default and cannot be set as Test or Prod. This action cannot be undone via UI.">
                                         @Html.AntiForgeryToken()
                                         <button type="submit" class="btn btn-sm btn-danger" title="Soft Delete This Version">
                                             <i class="fas fa-trash-alt"></i> Delete
                                         </button>
                                     </form>
                                }
                                 @if (version.IsDeleted)
                                 {
                                      <span class="text-danger small ms-1">Actions disabled</span> @* Indicate actions are disabled for deleted versions *@
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
            <p>This template does not have any previous versions recorded (or all have been soft deleted).</p>
        </div>
    }

    <div class="mt-4 text-center">
        <a asp-controller="Template" asp-action="Design" asp-route-templateName="@Model.Name" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Back to Design (v@Model.TestingVersionNumber)
        </a>
    </div>
</div>

@section Scripts {
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script> @* Ensure jQuery is included if using $ *@
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

             // Optional: Add modal logic here if implementing the "View Details" button
        });
    </script>
}
```

**47. PDFGenerator.Web\Views\Template\Create.cshtml** (No change, as the logic for setting versions to 1 is in the handler)
**48. PDFGenerator.Web\Views\Shared\_Layout.cshtml** (No change)
**49. PDFGenerator.Web\Views\Shared\_AccountLayout.cshtml** (No change)
**50. PDFGenerator.Web\Views\Shared\_ValidationScriptsPartial.cshtml** (No change)
**51. PDFGenerator.Web\Views\_ViewImports.cshtml** (No change)
**52. PDFGenerator.Web\Views\_ViewStart.cshtml** (No change)
**53. PDFGenerator.Web\Views\Auth\ForgotPassword.cshtml** (No change)
**54. PDFGenerator.Web\Views\Auth\Login.cshtml** (No change)
**55. PDFGenerator.Web\Views\Auth\Profile.cshtml** (No change)
**56. PDFGenerator.Web\Views\Auth\ResetPassword.cshtml** (No change)
**57. PDFGenerator.Infrastructure\Services\MailServies.cs** (No change related to this request)
**58. PDFGenerator.Infrastructure\Services\TemplateProcessingService.cs** (No change related to this request)
**59. PDFGenerator.Infrastructure\DataAccess\Models\ErrorViewModel.cs** (No change)

**Final Steps:**

1.  Apply the model changes.
2.  Generate and apply the new EF Core migration.
3.  Add the new DTO files (`SetTemplateVersionRequestDto.cs`, `TemplateVersionReferenceType.cs`, `PublishTemplateRequestDto.cs`, `SoftDeleteVersionRequestDto.cs`).
4.  Update existing DTO files.
5.  Update the two AutoMapper profile files.
6.  Update the repository interfaces and implementations (`TemplateRepository.cs`, `TemplateVersionRepository.cs`).
7.  Update the Unit of Work interface and implementation.
8.  Create the three new handler files (`SetTemplateVersionHandler.cs`, `PublishTemplateHandler.cs`, `SoftDeleteTemplateVersionHandler.cs`).
9.  Rename and update `GetTemplateByNameHandler.cs` to `GetProductionTemplateHandler.cs`.
10. Create `GetTemplateForDesignHandler.cs`.
11. Update existing handlers (`CreateTemplateHandler.cs`, `UpdateTemplateHandler.cs`, `GetTemplateHistoryHandler.cs`, `GeneratePdfHandler.cs`).
12. Update `ServiceCollectionExtensions.cs` (or `PDFGenerator.Web.Extensions\ServiceCollectionExtensions.cs` if you fix the namespace) to register all new/renamed handlers and repositories.
13. Update the Controller files (`HomeController.cs`, `DocsController.cs`, `PdfController.cs`, `TemplateController.cs`).
14. Update the View files (`Index.cshtml`, `Design.cshtml`, `History.cshtml`, `Templates.cshtml`).
15. Fix the inconsistent namespace (`EduCach.DataAccess.Extensions`). It should likely be `PDFGenerator.Infrastructure.Extensions`. If you fix this, ensure the `using` directives and namespace declarations throughout the relevant files are also updated. The handlers in `PDFGenerator.Web` should probably also be in a namespace like `PDFGenerator.Web.Handlers`.

This set of changes addresses the requirements by adding explicit version tracking for Test/Prod, soft deletion, and the necessary UI actions and backend logic to manage these versions.

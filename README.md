Okay, the problem you're describing is common when the UI state (especially a flag like `_isNew`) isn't managed correctly across operations like adding, saving, and navigating, or when the `BindingSource` isn't properly refreshed and rebound after data changes.

The `frmCategories.cs` you provided seems to have many of the fixes already incorporated. The key is that after saving a new record:
1.  The `_isNew` flag must be reset to `false`.
2.  The data source (e.g., `categoryBindingSource`) needs to be reloaded to include the new record.
3.  The UI (buttons, status messages) must be updated to reflect the new state (not adding anymore, potentially a new record selected).
4.  Navigation should then work on the reloaded dataset.

I will provide the complete set of files for `Categories`, `Suppliers`, `Products`, `Customers`, and `Employees`, ensuring this logic is consistently applied. I'll base the `Designer.cs` files on the `frmCategories.Designer.cs` structure and common fields for each entity.

Here are the files:

**Common Notes for all `*.cs` (code-behind) files:**

*   The `_isNew` flag is set to `true` on `tsbNew_Click`.
*   The `_isNew` flag is reset to `false` only *after* a successful save operation, specifically when a new item was being added.
*   `LoadDataAsync()` is called after save/delete operations to refresh the list.
    *   If a new item was added, `LoadDataAsync(null)` is called to show all items and clear any search.
    *   If an existing item was updated or deleted, `LoadDataAsync(txtSearch.Text)` is called to maintain the search context.
*   A `Select<Entity>ById(int id)` method is used to re-select the saved/updated item after `LoadDataAsync`.
*   `BindingSource_CurrentChanged` only updates UI elements if `!_isNew` to avoid conflicts during new item entry.
*   Error handling (`DbUpdateConcurrencyException`, `DbUpdateException`) is included.
*   Validation is present in `tsbSave_Click`.
*   Password handling for `frmEmployees` will clear the password field after save and require it for new employees.
*   `frmProducts` will include logic for loading `Category` and `Supplier` dropdowns.

---
**File 1: `frmCategories.Designer.cs`**
---
```csharp
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;
using Store.Data.Models; // Assuming Category model is here

namespace Store.Forms
{
    partial class frmCategories
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            components = new Container();
            ComponentResourceManager resources = new ComponentResourceManager(typeof(frmCategories));
            toolStrip1 = new ToolStrip();
            tsbNew = new ToolStripButton();
            tsbSave = new ToolStripButton();
            tsbDelete = new ToolStripButton();
            toolStripSeparator1 = new ToolStripSeparator();
            tsbFirst = new ToolStripButton();
            tsbPrevious = new ToolStripButton();
            tsbNext = new ToolStripButton();
            tsbLast = new ToolStripButton();
            toolStripSeparator2 = new ToolStripSeparator();
            txtSearch = new ToolStripTextBox();
            tsbSearch = new ToolStripButton();
            statusStrip1 = new StatusStrip();
            lblStatus = new ToolStripStatusLabel();
            categoryBindingSource = new BindingSource(components);
            groupBoxDetails = new GroupBox();
            tableLayoutPanelDetails = new TableLayoutPanel();
            lblCategoryID = new Label();
            txtCategoryID = new TextBox();
            lblCategoryName = new Label();
            txtCategoryName = new TextBox();
            toolStrip1.SuspendLayout();
            statusStrip1.SuspendLayout();
            ((ISupportInitialize)categoryBindingSource).BeginInit();
            groupBoxDetails.SuspendLayout();
            tableLayoutPanelDetails.SuspendLayout();
            SuspendLayout();
            // 
            // toolStrip1
            // 
            toolStrip1.Font = new Font("Segoe UI", 10F, FontStyle.Regular, GraphicsUnit.Point);
            toolStrip1.GripStyle = ToolStripGripStyle.Hidden;
            toolStrip1.ImageScalingSize = new Size(24, 24);
            toolStrip1.Items.AddRange(new ToolStripItem[] { tsbNew, tsbSave, tsbDelete, toolStripSeparator1, tsbFirst, tsbPrevious, tsbNext, tsbLast, toolStripSeparator2, txtSearch, tsbSearch });
            toolStrip1.Location = new Point(0, 0);
            toolStrip1.Name = "toolStrip1";
            toolStrip1.Padding = new Padding(8, 5, 8, 5);
            toolStrip1.RenderMode = ToolStripRenderMode.System;
            toolStrip1.Size = new Size(1118, 46);
            toolStrip1.TabIndex = 0;
            toolStrip1.Text = "toolStrip1";
            toolStrip1.BackColor = Color.FromArgb(240, 240, 240);
            // 
            // tsbNew
            // 
            tsbNew.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbNew.Image = (Image)resources.GetObject("tsbNew.Image");
            tsbNew.ImageTransparentColor = Color.Magenta;
            tsbNew.Margin = new Padding(4);
            tsbNew.Name = "tsbNew";
            tsbNew.Size = new Size(146, 28);
            tsbNew.Text = "New Category";
            tsbNew.ToolTipText = "Add New Category (Ctrl+N)";
            tsbNew.Font = new Font("Segoe UI", 10F, FontStyle.Regular, GraphicsUnit.Point);
            tsbNew.ForeColor = Color.FromArgb(64, 64, 64);
            tsbNew.Click += tsbNew_Click;
            // 
            // tsbSave
            // 
            tsbSave.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbSave.Image = (Image)resources.GetObject("tsbSave.Image");
            tsbSave.ImageTransparentColor = Color.Magenta;
            tsbSave.Margin = new Padding(4);
            tsbSave.Name = "tsbSave";
            tsbSave.Size = new Size(144, 28);
            tsbSave.Text = "Save Changes";
            tsbSave.ToolTipText = "Save Changes (Ctrl+S)";
            tsbSave.Font = new Font("Segoe UI", 10F, FontStyle.Regular, GraphicsUnit.Point);
            tsbSave.ForeColor = Color.FromArgb(64, 64, 64);
            tsbSave.Click += tsbSave_Click;
            // 
            // tsbDelete
            // 
            tsbDelete.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbDelete.Image = (Image)resources.GetObject("tsbDelete.Image");
            tsbDelete.ImageTransparentColor = Color.Magenta;
            tsbDelete.Margin = new Padding(4);
            tsbDelete.Name = "tsbDelete";
            tsbDelete.Size = new Size(161, 28);
            tsbDelete.Text = "Delete Category";
            tsbDelete.ToolTipText = "Delete Selected Category (Del)";
            tsbDelete.Font = new Font("Segoe UI", 10F, FontStyle.Regular, GraphicsUnit.Point);
            tsbDelete.ForeColor = Color.FromArgb(64, 64, 64);
            tsbDelete.Click += tsbDelete_Click;
            // 
            // toolStripSeparator1
            // 
            toolStripSeparator1.Margin = new Padding(10, 0, 10, 0);
            toolStripSeparator1.Name = "toolStripSeparator1";
            toolStripSeparator1.Size = new Size(6, 36);
            // 
            // tsbFirst
            // 
            tsbFirst.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbFirst.Image = (Image)resources.GetObject("tsbFirst.Image");
            tsbFirst.ImageTransparentColor = Color.Magenta;
            tsbFirst.Margin = new Padding(4);
            tsbFirst.Name = "tsbFirst";
            tsbFirst.Size = new Size(127, 28);
            tsbFirst.Text = "First Record";
            tsbFirst.ToolTipText = "Go to First Record (Ctrl+Home)";
            tsbFirst.Font = new Font("Segoe UI", 10F, FontStyle.Regular, GraphicsUnit.Point);
            tsbFirst.ForeColor = Color.FromArgb(64, 64, 64);
            tsbFirst.Click += tsbFirst_Click;
            // 
            // tsbPrevious
            // 
            tsbPrevious.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbPrevious.Image = (Image)resources.GetObject("tsbPrevious.Image");
            tsbPrevious.ImageTransparentColor = Color.Magenta;
            tsbPrevious.Margin = new Padding(4);
            tsbPrevious.Name = "tsbPrevious";
            tsbPrevious.Size = new Size(160, 28);
            tsbPrevious.Text = "Previous Record";
            tsbPrevious.ToolTipText = "Go to Previous Record (Ctrl+Left)";
            tsbPrevious.Font = new Font("Segoe UI", 10F, FontStyle.Regular, GraphicsUnit.Point);
            tsbPrevious.ForeColor = Color.FromArgb(64, 64, 64);
            tsbPrevious.Click += tsbPrevious_Click;
            // 
            // tsbNext
            // 
            tsbNext.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbNext.Image = (Image)resources.GetObject("tsbNext.Image");
            tsbNext.ImageTransparentColor = Color.Magenta;
            tsbNext.Margin = new Padding(4);
            tsbNext.Name = "tsbNext";
            tsbNext.Size = new Size(132, 28);
            tsbNext.Text = "Next Record";
            tsbNext.ToolTipText = "Go to Next Record (Ctrl+Right)";
            tsbNext.Font = new Font("Segoe UI", 10F, FontStyle.Regular, GraphicsUnit.Point);
            tsbNext.ForeColor = Color.FromArgb(64, 64, 64);
            tsbNext.Click += tsbNext_Click;
            // 
            // tsbLast
            // 
            tsbLast.DisplayStyle = ToolStripItemDisplayStyle.Text;
            tsbLast.ImageTransparentColor = Color.Magenta;
            tsbLast.Margin = new Padding(4);
            tsbLast.Name = "tsbLast";
            tsbLast.Size = new Size(102, 28);
            tsbLast.Text = "Last Record";
            tsbLast.ToolTipText = "Go to Last Record (Ctrl+End)";
            tsbLast.Font = new Font("Segoe UI", 10F, FontStyle.Regular, GraphicsUnit.Point);
            tsbLast.ForeColor = Color.FromArgb(64, 64, 64);
            tsbLast.Click += tsbLast_Click;
            // 
            // toolStripSeparator2
            // 
            toolStripSeparator2.Margin = new Padding(10, 0, 10, 0);
            toolStripSeparator2.Name = "toolStripSeparator2";
            toolStripSeparator2.Size = new Size(6, 36);
            // 
            // txtSearch
            // 
            txtSearch.Alignment = ToolStripItemAlignment.Right;
            txtSearch.BackColor = Color.White;
            txtSearch.BorderStyle = BorderStyle.FixedSingle;
            txtSearch.Font = new Font("Segoe UI", 10F, FontStyle.Regular, GraphicsUnit.Point);
            txtSearch.ForeColor = Color.FromArgb(64, 64, 64);
            txtSearch.Margin = new Padding(1, 2, 6, 2); 
            txtSearch.Name = "txtSearch";
            txtSearch.Size = new Size(200, 27);
            txtSearch.ToolTipText = "Enter search term and press Enter or click Search";
            txtSearch.KeyDown += txtSearch_KeyDown;
            // 
            // tsbSearch
            // 
            tsbSearch.Alignment = ToolStripItemAlignment.Right;
            tsbSearch.DisplayStyle = ToolStripItemDisplayStyle.Image;
            tsbSearch.Image = (Image)resources.GetObject("tsbSearch.Image"); 
            tsbSearch.ImageTransparentColor = Color.Magenta;
            tsbSearch.Margin = new Padding(1, 2, 1, 2); 
            tsbSearch.Name = "tsbSearch";
            tsbSearch.Size = new Size(28, 28); 
            tsbSearch.Text = "Search"; 
            tsbSearch.ToolTipText = "Search Categories (Enter)";
            tsbSearch.Click += tsbSearch_Click;
            // 
            // statusStrip1
            // 
            statusStrip1.ImageScalingSize = new Size(20, 20);
            statusStrip1.Items.AddRange(new ToolStripItem[] { lblStatus });
            statusStrip1.Location = new Point(0, 288);
            statusStrip1.Name = "statusStrip1";
            statusStrip1.Padding = new Padding(1, 0, 16, 0);
            statusStrip1.Size = new Size(1118, 22);
            statusStrip1.TabIndex = 2;
            statusStrip1.BackColor = Color.FromArgb(248, 248, 248);
            statusStrip1.Text = "statusStrip1";
            // 
            // lblStatus
            // 
            lblStatus.Name = "lblStatus";
            lblStatus.Size = new Size(1101, 16);
            lblStatus.Spring = true;
            lblStatus.TextAlign = ContentAlignment.MiddleLeft;
            lblStatus.Font = new Font("Segoe UI", 9F, FontStyle.Regular, GraphicsUnit.Point);
            lblStatus.ForeColor = Color.FromArgb(80, 80, 80);
            // 
            // categoryBindingSource
            // 
            categoryBindingSource.DataSource = typeof(Category);
            categoryBindingSource.CurrentChanged += categoryBindingSource_CurrentChanged;
            // 
            // groupBoxDetails
            // 
            groupBoxDetails.Controls.Add(tableLayoutPanelDetails);
            groupBoxDetails.Dock = DockStyle.Fill;
            groupBoxDetails.Location = new Point(0, 46);
            groupBoxDetails.Margin = new Padding(10);
            groupBoxDetails.Name = "groupBoxDetails";
            groupBoxDetails.Padding = new Padding(20);
            groupBoxDetails.Size = new Size(1118, 242);
            groupBoxDetails.TabIndex = 1;
            groupBoxDetails.TabStop = false;
            groupBoxDetails.Text = "Category Details";
            groupBoxDetails.Font = new Font("Segoe UI Semibold", 10F, FontStyle.Bold, GraphicsUnit.Point);
            groupBoxDetails.ForeColor = Color.FromArgb(55, 55, 55);
            // 
            // tableLayoutPanelDetails
            // 
            tableLayoutPanelDetails.ColumnCount = 2;
            tableLayoutPanelDetails.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 130F)); // Adjusted for longer label
            tableLayoutPanelDetails.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            tableLayoutPanelDetails.Controls.Add(lblCategoryID, 0, 0);
            tableLayoutPanelDetails.Controls.Add(txtCategoryID, 1, 0);
            tableLayoutPanelDetails.Controls.Add(lblCategoryName, 0, 1);
            tableLayoutPanelDetails.Controls.Add(txtCategoryName, 1, 1);
            tableLayoutPanelDetails.Dock = DockStyle.Fill;
            tableLayoutPanelDetails.Location = new Point(20, 43);
            tableLayoutPanelDetails.Margin = new Padding(0);
            tableLayoutPanelDetails.Name = "tableLayoutPanelDetails";
            tableLayoutPanelDetails.RowCount = 3; // 2 for fields, 1 for percent spacer
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F)); // Adjusted row height
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F)); // Adjusted row height
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableLayoutPanelDetails.Size = new Size(1078, 179);
            tableLayoutPanelDetails.TabIndex = 0;
            // 
            // lblCategoryID
            // 
            lblCategoryID.Anchor = AnchorStyles.Left;
            lblCategoryID.AutoSize = true;
            lblCategoryID.Location = new Point(3, 11); 
            lblCategoryID.Name = "lblCategoryID";
            lblCategoryID.Size = new Size(112, 23); 
            lblCategoryID.TabIndex = 0;
            lblCategoryID.Text = "Category ID:";
            lblCategoryID.TextAlign = ContentAlignment.MiddleLeft;
            lblCategoryID.Font = new Font("Segoe UI", 10F, FontStyle.Regular, GraphicsUnit.Point);
            lblCategoryID.ForeColor = Color.FromArgb(80, 80, 80);
            // 
            // txtCategoryID
            // 
            txtCategoryID.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            txtCategoryID.Location = new Point(133, 7); // Adjusted from 121 based on 130F col width
            txtCategoryID.Margin = new Padding(3, 4, 10, 4);
            txtCategoryID.Name = "txtCategoryID";
            txtCategoryID.ReadOnly = true;
            txtCategoryID.Size = new Size(935, 30); // Adjusted for Font
            txtCategoryID.TabIndex = 1;
            txtCategoryID.TabStop = false;
            txtCategoryID.Font = new Font("Segoe UI", 10F, FontStyle.Regular, GraphicsUnit.Point);
            txtCategoryID.ForeColor = Color.FromArgb(100, 100, 100);
            txtCategoryID.BackColor = Color.FromArgb(245, 245, 245);
            txtCategoryID.BorderStyle = BorderStyle.FixedSingle;
            // 
            // lblCategoryName
            // 
            lblCategoryName.Anchor = AnchorStyles.Left;
            lblCategoryName.AutoSize = true;
            lblCategoryName.Location = new Point(3, 56); 
            lblCategoryName.Name = "lblCategoryName";
            lblCategoryName.Size = new Size(116, 23); 
            lblCategoryName.TabIndex = 2;
            lblCategoryName.Text = "Category Name:";
            lblCategoryName.TextAlign = ContentAlignment.MiddleLeft;
            lblCategoryName.Font = new Font("Segoe UI", 10F, FontStyle.Regular, GraphicsUnit.Point);
            lblCategoryName.ForeColor = Color.FromArgb(80, 80, 80);
            // 
            // txtCategoryName
            // 
            txtCategoryName.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            txtCategoryName.Location = new Point(133, 52); // Adjusted from 121 based on 130F col width
            txtCategoryName.Margin = new Padding(3, 4, 10, 4);
            txtCategoryName.MaxLength = 50;
            txtCategoryName.Name = "txtCategoryName";
            txtCategoryName.Size = new Size(935, 30); // Adjusted
            txtCategoryName.TabIndex = 0; // This should be the first editable field
            txtCategoryName.Font = new Font("Segoe UI", 10F, FontStyle.Regular, GraphicsUnit.Point);
            txtCategoryName.ForeColor = Color.FromArgb(50, 50, 50);
            txtCategoryName.BorderStyle = BorderStyle.FixedSingle;
            // 
            // frmCategories
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.White;
            ClientSize = new Size(1118, 310);
            Controls.Add(groupBoxDetails);
            Controls.Add(statusStrip1);
            Controls.Add(toolStrip1);
            MinimumSize = new Size(550, 320);
            Name = "frmCategories";
            Text = "Manage Categories";
            Font = new Font("Segoe UI", 9F, FontStyle.Regular, GraphicsUnit.Point); 
            ForeColor = Color.FromArgb(64, 64, 64);
            Load += frmCategories_Load;
            toolStrip1.ResumeLayout(false);
            toolStrip1.PerformLayout();
            statusStrip1.ResumeLayout(false);
            statusStrip1.PerformLayout();
            ((ISupportInitialize)categoryBindingSource).EndInit();
            groupBoxDetails.ResumeLayout(false);
            tableLayoutPanelDetails.ResumeLayout(false);
            tableLayoutPanelDetails.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private System.Windows.Forms.ToolStrip toolStrip1;
        private System.Windows.Forms.ToolStripButton tsbNew;
        private System.Windows.Forms.ToolStripButton tsbSave;
        private System.Windows.Forms.ToolStripButton tsbDelete;
        private System.Windows.Forms.ToolStripSeparator toolStripSeparator1;
        private System.Windows.Forms.ToolStripButton tsbFirst;
        private System.Windows.Forms.ToolStripButton tsbPrevious;
        private System.Windows.Forms.ToolStripButton tsbNext;
        private System.Windows.Forms.ToolStripButton tsbLast;
        private System.Windows.Forms.ToolStripSeparator toolStripSeparator2;
        private System.Windows.Forms.ToolStripTextBox txtSearch;
        private System.Windows.Forms.ToolStripButton tsbSearch;
        private System.Windows.Forms.StatusStrip statusStrip1;
        private System.Windows.Forms.ToolStripStatusLabel lblStatus;
        private System.Windows.Forms.BindingSource categoryBindingSource;
        private System.Windows.Forms.GroupBox groupBoxDetails;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanelDetails;
        private System.Windows.Forms.Label lblCategoryID;
        private System.Windows.Forms.TextBox txtCategoryID;
        private System.Windows.Forms.Label lblCategoryName;
        private System.Windows.Forms.TextBox txtCategoryName;
    }
}
```

---
**File 2: `frmCategories.cs`**
---
```csharp
using Microsoft.EntityFrameworkCore;
using Store.Data.Models;
using Store.Services;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Store.Forms
{
    public partial class frmCategories : Form
    {
        private readonly CategoryService _categoryService;
        private bool _isNew = false;
        private bool _isLoading = false; // To prevent re-entrant calls during load

        public frmCategories(CategoryService categoryService)
        {
            InitializeComponent();
            _categoryService = categoryService;
        }

        private async void frmCategories_Load(object sender, EventArgs e)
        {
            _isLoading = true;
            await LoadDataAsync();
            SetupBindings();
            // UpdateButtonStates and UpdateNavigationState are called in LoadDataAsync's finally block
            _isLoading = false;
            // Call them once more after _isLoading is false to ensure correct initial state
            if (categoryBindingSource.Count > 0 && categoryBindingSource.Position < 0)
            {
                categoryBindingSource.MoveFirst();
            }
            UpdateButtonStates();
            UpdateNavigationState();
        }

        private async Task LoadDataAsync(string? searchTerm = null)
        {
            ToggleControls(false, true); // Keep toolbar enabled during load
            lblStatus.Text = "Loading categories...";
            try
            {
                List<Category> categories;
                if (string.IsNullOrWhiteSpace(searchTerm))
                {
                    categories = await _categoryService.GetAllCategoriesAsync();
                }
                else
                {
                    categories = await _categoryService.SearchCategoriesAsync(searchTerm);
                }
                
                var currentPosition = categoryBindingSource.Position;
                var currentId = (categoryBindingSource.Current as Category)?.CategoryID;

                categoryBindingSource.DataSource = categories;
                categoryBindingSource.ResetBindings(false);

                if (categories.Count == 0)
                {
                    lblStatus.Text = string.IsNullOrWhiteSpace(searchTerm) ? "No categories found. Click 'New' to add one." : $"No categories matching '{searchTerm}'.";
                    ClearForm(); // This will also clear bindings temporarily
                    SetupBindings(); // Re-setup bindings to empty source if needed
                }
                else
                {
                    lblStatus.Text = string.IsNullOrWhiteSpace(searchTerm) ? $"Displaying {categories.Count} categories." : $"Found {categories.Count} matching '{searchTerm}'.";
                     if (currentId.HasValue)
                    {
                        SelectCategoryById(currentId.Value, false); // Try to reselect, don't trigger CurrentChanged if not found
                    }
                    if (categoryBindingSource.Position < 0 && categories.Count > 0)
                    {
                        categoryBindingSource.MoveFirst();
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading categories: {ex.Message}", "Loading Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Error loading data.";
            }
            finally
            {
                if (!_isLoading) // Only update states if not in initial load sequence
                {
                    UpdateButtonStates();
                    UpdateNavigationState();
                }
                ToggleControls(true, true);
            }
        }

        private void SetupBindings()
        {
            // Clear existing bindings before adding new ones to prevent duplicates
            txtCategoryID.DataBindings.Clear();
            txtCategoryName.DataBindings.Clear();

            // Add new bindings
            txtCategoryID.DataBindings.Add("Text", categoryBindingSource, "CategoryID", true, DataSourceUpdateMode.Never);
            txtCategoryName.DataBindings.Add("Text", categoryBindingSource, "CategoryName", false, DataSourceUpdateMode.OnValidation);
        }

        private void ClearForm()
        {
            // Suspend binding before clearing, then resume after setting up for new or empty state
            categoryBindingSource.SuspendBinding();

            txtCategoryID.Clear();
            txtCategoryName.Clear();
            
            // If you intend for cleared form to be bindable (e.g. to a 'new' object not yet in source),
            // you might need to handle bindings differently or rely on _isNew state to manage fields directly.
            // For now, clearing textboxes is sufficient. Binding will re-engage on next current item.
            
            categoryBindingSource.ResumeBinding();
        }

        private void ToggleControls(bool enabled, bool keepToolbarEnabled = false)
        {
            groupBoxDetails.Enabled = enabled;
            if (!keepToolbarEnabled)
            {
                 toolStrip1.Enabled = enabled;
            }
            else
            {
                toolStrip1.Enabled = true; // Toolbar usually stays enabled, buttons managed by UpdateButtonStates
            }
           
            this.Cursor = enabled ? Cursors.Default : Cursors.WaitCursor;
        }

        private void UpdateButtonStates()
        {
            if (_isLoading) return;

            bool hasItems = categoryBindingSource.Count > 0;
            bool isItemSelected = categoryBindingSource.Current != null;

            tsbSave.Enabled = _isNew || (isItemSelected && !string.IsNullOrWhiteSpace(txtCategoryName.Text));
            tsbDelete.Enabled = isItemSelected && !_isNew;

            tsbFirst.Enabled = isItemSelected && !_isNew && categoryBindingSource.Position > 0;
            tsbPrevious.Enabled = isItemSelected && !_isNew && categoryBindingSource.Position > 0;
            tsbNext.Enabled = isItemSelected && !_isNew && categoryBindingSource.Position < categoryBindingSource.Count - 1;
            tsbLast.Enabled = isItemSelected && !_isNew && categoryBindingSource.Position < categoryBindingSource.Count - 1;

            // New, Search are always enabled unless the whole form is busy
            tsbNew.Enabled = toolStrip1.Enabled;
            txtSearch.Enabled = toolStrip1.Enabled;
            tsbSearch.Enabled = toolStrip1.Enabled;
        }

        private void UpdateNavigationState()
        {
            if (_isLoading) return;

            bool hasItems = categoryBindingSource.Count > 0;
            bool isItemSelected = categoryBindingSource.Current != null;

            if (_isNew)
            {
                lblStatus.Text = "Adding new category...";
                groupBoxDetails.Enabled = true; // Ensure details are enabled for new entry
            }
            else if (isItemSelected)
            {
                lblStatus.Text = $"Record {categoryBindingSource.Position + 1} of {categoryBindingSource.Count}";
                groupBoxDetails.Enabled = true; // Ensure details are enabled for editing
            }
            else // No items or no selection
            {
                lblStatus.Text = hasItems ? "No category selected." : (string.IsNullOrWhiteSpace(txtSearch.Text) ? "No categories found." : $"No categories matching '{txtSearch.Text}'.");
                groupBoxDetails.Enabled = false; // Disable details if no item is selected/available
                if (!hasItems) ClearForm(); // Clear form if no items exist
            }
            UpdateButtonStates(); // Call this to ensure button states are re-evaluated
        }

        private void tsbNew_Click(object sender, EventArgs e)
        {
            _isNew = true;
            categoryBindingSource.SuspendBinding(); 
            ClearForm(); 
            // Do not call categoryBindingSource.AddNew() here if you handle object creation manually on save.
            // SetupBindings(); // Re-establish bindings for a new, unbound state if desired, or handle manually
            
            txtCategoryName.Focus();
            UpdateNavigationState(); // This will set status text and call UpdateButtonStates
            // UpdateButtonStates(); // Called by UpdateNavigationState
        }

        private async void tsbSave_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtCategoryName.Text))
            {
                MessageBox.Show("Category Name cannot be empty.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                txtCategoryName.Focus();
                return;
            }

            // If not _isNew, ensure the current item's changes are pushed to the BindingSource
            if (!_isNew && categoryBindingSource.Current != null)
            {
                categoryBindingSource.EndEdit(); 
            }

            ToggleControls(false);
            lblStatus.Text = "Saving...";

            try
            {
                bool success = false;
                Category? categoryToSave = null;
                bool wasNewItemInitially = _isNew; // Store the state before trying to save

                if (_isNew)
                {
                    categoryToSave = new Category { CategoryName = txtCategoryName.Text.Trim() };
                    success = await _categoryService.AddCategoryAsync(categoryToSave);
                    if (success) lblStatus.Text = "Category added successfully.";
                    // else: _categoryService should throw an exception or return detailed error.
                }
                else
                {
                    if (categoryBindingSource.Current is Category currentCategory)
                    {
                        // Ensure text box value is applied if not using DataSourceUpdateMode.OnPropertyChanged for everything
                        currentCategory.CategoryName = txtCategoryName.Text.Trim(); 
                        categoryToSave = currentCategory;
                        success = await _categoryService.UpdateCategoryAsync(currentCategory);
                        if (success) lblStatus.Text = "Category updated successfully.";
                    }
                    else
                    {
                        MessageBox.Show("No category selected to update.", "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        lblStatus.Text = "No category selected."; // Update status
                    }
                }

                if (success)
                {
                    _isNew = false; // IMPORTANT: Reset _isNew flag AFTER successful save
                    int savedItemId = categoryToSave?.CategoryID ?? -1;
                    
                    // Reload data: clear search if new item was added
                    string? currentSearchTerm = wasNewItemInitially ? null : txtSearch.Text;
                    if (wasNewItemInitially) txtSearch.Clear();
                    
                    await LoadDataAsync(currentSearchTerm); // LoadDataAsync now handles re-selection if possible or MoveFirst
                    
                    if (savedItemId > 0)
                    {
                        SelectCategoryById(savedItemId); // Attempt to select the saved item
                    }
                    else if (categoryBindingSource.Count > 0)
                    {
                        categoryBindingSource.MoveFirst(); // Fallback to first if ID not found (should not happen for new)
                    }
                }
            }
            catch (DbUpdateConcurrencyException)
            {
                MessageBox.Show("The record you attempted to edit was modified by another user after you got the original value. The edit operation was canceled.", "Concurrency Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                lblStatus.Text = "Save failed due to concurrency.";
                await LoadDataAsync(txtSearch.Text); // Reload current search
            }
            catch (DbUpdateException dbEx)
            {
                // Check for unique constraint violation (example for SQL Server)
                string errorMessage = $"Database error saving category: {dbEx.InnerException?.Message ?? dbEx.Message}.";
                if (dbEx.InnerException?.Message.Contains("UNIQUE KEY constraint") == true || 
                    dbEx.InnerException?.Message.Contains("duplicate key value violates unique constraint") == true) // PostgreSQL
                {
                    errorMessage += "\nThe category name might already exist.";
                }
                MessageBox.Show(errorMessage, "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Database save error.";
            }
            catch (Exception ex)
            {
                MessageBox.Show($"An error occurred while saving: {ex.Message}", "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Save error.";
            }
            finally
            {
                // ToggleControls(true); // LoadDataAsync will call this in its finally block.
                // UpdateButtonStates and UpdateNavigationState are called by LoadDataAsync
                // If LoadDataAsync wasn't called (e.g. on failure before reload), ensure states are updated.
                if (!success) { // If save failed, re-enable controls and update UI state
                     ToggleControls(true);
                     UpdateButtonStates();
                     UpdateNavigationState();
                }
            }
        }

        private async void tsbDelete_Click(object sender, EventArgs e)
        {
            if (_isNew) // Should not be able to delete while in "new" mode
            {
                MessageBox.Show("Cannot delete an unsaved new category.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            if (categoryBindingSource.Current is Category currentCategory)
            {
                var confirmResult = MessageBox.Show($"Are you sure you want to delete category '{currentCategory.CategoryName}' (ID: {currentCategory.CategoryID})?\nThis action cannot be undone.",
                                                     "Confirm Delete", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);

                if (confirmResult == DialogResult.Yes)
                {
                    ToggleControls(false);
                    lblStatus.Text = "Deleting...";
                    try
                    {
                        bool success = await _categoryService.DeleteCategoryAsync(currentCategory.CategoryID);

                        if (success)
                        {
                            lblStatus.Text = "Category deleted successfully.";
                        }
                        // else: _categoryService should throw for errors
                        
                        await LoadDataAsync(txtSearch.Text.Trim()); // Reload data to reflect deletion
                    }
                    catch (DbUpdateException dbEx) // Catch specific exception for FK constraint
                    {
                        MessageBox.Show($"Database error deleting category: {dbEx.InnerException?.Message ?? dbEx.Message}.\nIt might be referenced by other records (e.g., products).", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        lblStatus.Text = "Database delete error.";
                        await LoadDataAsync(txtSearch.Text.Trim()); // Reload to show current state
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"An error occurred while deleting: {ex.Message}", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        lblStatus.Text = "Delete error.";
                        await LoadDataAsync(txtSearch.Text.Trim()); // Reload to show current state
                    }
                    // finally is handled by LoadDataAsync for ToggleControls and UI updates
                }
            }
            else
            {
                MessageBox.Show("No category selected to delete.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private async void PerformSearch()
        {
            _isNew = false; // Exit "new" mode if searching
            categoryBindingSource.ResumeBinding(); // Ensure binding is active
            await LoadDataAsync(txtSearch.Text.Trim());
        }

        private void tsbSearch_Click(object sender, EventArgs e)
        {
            PerformSearch();
        }

        private void txtSearch_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
            {
                PerformSearch();
                e.SuppressKeyPress = true; 
            }
        }

        private void tsbFirst_Click(object sender, EventArgs e)
        {
            if (_isNew) _isNew = false; categoryBindingSource.ResumeBinding(); categoryBindingSource.MoveFirst();
        }

        private void tsbPrevious_Click(object sender, EventArgs e)
        {
            if (_isNew) _isNew = false; categoryBindingSource.ResumeBinding(); categoryBindingSource.MovePrevious();
        }

        private void tsbNext_Click(object sender, EventArgs e)
        {
            if (_isNew) _isNew = false; categoryBindingSource.ResumeBinding(); categoryBindingSource.MoveNext();
        }

        private void tsbLast_Click(object sender, EventArgs e)
        {
            if (_isNew) _isNew = false; categoryBindingSource.ResumeBinding(); categoryBindingSource.MoveLast();
        }

        private void categoryBindingSource_CurrentChanged(object sender, EventArgs e)
        {
            if (_isLoading || _isNew) return; // Don't interfere if loading or in "new" mode

            if (categoryBindingSource.Current == null)
            {
                ClearForm();
                // Bindings should already be set up, or will be by LoadDataAsync if list is empty
            }
            // Data binding should automatically update textboxes if Current is not null.
            UpdateButtonStates();
            UpdateNavigationState();
        }

        private void SelectCategoryById(int categoryId, bool triggerCurrentChanged = true)
        {
            if (categoryId <= 0) return;

            if (categoryBindingSource.DataSource is List<Category> categories)
            {
                int index = -1;
                for(int i=0; i < categories.Count; i++)
                {
                    if (categories[i].CategoryID == categoryId)
                    {
                        index = i;
                        break;
                    }
                }

                if (index != -1)
                {
                    if (!triggerCurrentChanged)
                    {
                        // Temporarily detach event handler
                        this.categoryBindingSource.CurrentChanged -= categoryBindingSource_CurrentChanged;
                        categoryBindingSource.Position = index;
                        // Re-attach event handler
                        this.categoryBindingSource.CurrentChanged += categoryBindingSource_CurrentChanged;
                        // Manually update display if CurrentChanged was skipped
                        if(categoryBindingSource.Current is Category cat)
                        {
                            txtCategoryID.Text = cat.CategoryID.ToString();
                            txtCategoryName.Text = cat.CategoryName;
                        }
                    }
                    else
                    {
                         categoryBindingSource.Position = index;
                    }
                }
            }
        }
    }
}
```

---
**File 3: `frmSuppliers.Designer.cs`**
---
```csharp
using System;
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;
using Store.Data.Models;

namespace Store.Forms
{
    partial class frmSuppliers
    {
        private System.ComponentModel.IContainer components = null;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null)) { components.Dispose(); }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code
        private void InitializeComponent()
        {
            components = new Container();
            ComponentResourceManager resources = new ComponentResourceManager(typeof(frmSuppliers));
            toolStrip1 = new ToolStrip();
            tsbNew = new ToolStripButton();
            tsbSave = new ToolStripButton();
            tsbDelete = new ToolStripButton();
            toolStripSeparator1 = new ToolStripSeparator();
            tsbFirst = new ToolStripButton();
            tsbPrevious = new ToolStripButton();
            tsbNext = new ToolStripButton();
            tsbLast = new ToolStripButton();
            toolStripSeparator2 = new ToolStripSeparator();
            txtSearch = new ToolStripTextBox();
            tsbSearch = new ToolStripButton();
            statusStrip1 = new StatusStrip();
            lblStatus = new ToolStripStatusLabel();
            supplierBindingSource = new BindingSource(components);
            groupBoxDetails = new GroupBox();
            tableLayoutPanelDetails = new TableLayoutPanel();
            lblSupplierID = new Label();
            txtSupplierID = new TextBox();
            lblSupplierName = new Label();
            txtSupplierName = new TextBox();
            lblContactPerson = new Label();
            txtContactPerson = new TextBox();
            lblPhoneNumber = new Label();
            txtPhoneNumber = new TextBox();
            lblEmail = new Label();
            txtEmail = new TextBox();
            toolStrip1.SuspendLayout();
            statusStrip1.SuspendLayout();
            ((ISupportInitialize)supplierBindingSource).BeginInit();
            groupBoxDetails.SuspendLayout();
            tableLayoutPanelDetails.SuspendLayout();
            SuspendLayout();
            // 
            // toolStrip1
            // 
            toolStrip1.BackColor = Color.FromArgb(240, 240, 240);
            toolStrip1.Font = new Font("Segoe UI", 10F);
            toolStrip1.GripStyle = ToolStripGripStyle.Hidden;
            toolStrip1.ImageScalingSize = new Size(24, 24);
            toolStrip1.Items.AddRange(new ToolStripItem[] { tsbNew, tsbSave, tsbDelete, toolStripSeparator1, tsbFirst, tsbPrevious, tsbNext, tsbLast, toolStripSeparator2, txtSearch, tsbSearch });
            toolStrip1.Location = new Point(0, 0);
            toolStrip1.Name = "toolStrip1";
            toolStrip1.Padding = new Padding(8, 5, 8, 5);
            toolStrip1.RenderMode = ToolStripRenderMode.System;
            toolStrip1.Size = new Size(1118, 46);
            toolStrip1.TabIndex = 0;
            toolStrip1.Text = "toolStrip1";
            // 
            // tsbNew
            // 
            tsbNew.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbNew.Image = (Image)resources.GetObject("tsbNew.Image");
            tsbNew.ForeColor = Color.FromArgb(64, 64, 64);
            tsbNew.ImageTransparentColor = Color.Magenta;
            tsbNew.Margin = new Padding(4);
            tsbNew.Name = "tsbNew";
            tsbNew.Size = new Size(138, 28); 
            tsbNew.Text = "New Supplier";
            tsbNew.ToolTipText = "Add New Supplier (Ctrl+N)";
            tsbNew.Click += tsbNew_Click;
            // 
            // tsbSave
            // 
            tsbSave.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbSave.Image = (Image)resources.GetObject("tsbSave.Image");
            tsbSave.ForeColor = Color.FromArgb(64, 64, 64);
            tsbSave.ImageTransparentColor = Color.Magenta;
            tsbSave.Margin = new Padding(4);
            tsbSave.Name = "tsbSave";
            tsbSave.Size = new Size(144, 28);
            tsbSave.Text = "Save Changes";
            tsbSave.ToolTipText = "Save Changes (Ctrl+S)";
            tsbSave.Click += tsbSave_Click;
            // 
            // tsbDelete
            // 
            tsbDelete.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbDelete.Image = (Image)resources.GetObject("tsbDelete.Image");
            tsbDelete.ForeColor = Color.FromArgb(64, 64, 64);
            tsbDelete.ImageTransparentColor = Color.Magenta;
            tsbDelete.Margin = new Padding(4);
            tsbDelete.Name = "tsbDelete";
            tsbDelete.Size = new Size(153, 28); 
            tsbDelete.Text = "Delete Supplier";
            tsbDelete.ToolTipText = "Delete Selected Supplier (Del)";
            tsbDelete.Click += tsbDelete_Click;
            // 
            // toolStripSeparator1
            // 
            toolStripSeparator1.Margin = new Padding(10, 0, 10, 0);
            toolStripSeparator1.Name = "toolStripSeparator1";
            toolStripSeparator1.Size = new Size(6, 36);
            // 
            // tsbFirst
            // 
            tsbFirst.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbFirst.Image = (Image)resources.GetObject("tsbFirst.Image");
            tsbFirst.ForeColor = Color.FromArgb(64, 64, 64);
            tsbFirst.ImageTransparentColor = Color.Magenta;
            tsbFirst.Margin = new Padding(4);
            tsbFirst.Name = "tsbFirst";
            tsbFirst.Size = new Size(127, 28);
            tsbFirst.Text = "First Record";
            tsbFirst.ToolTipText = "Go to First Record (Ctrl+Home)";
            tsbFirst.Click += tsbFirst_Click;
            // 
            // tsbPrevious
            // 
            tsbPrevious.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbPrevious.Image = (Image)resources.GetObject("tsbPrevious.Image");
            tsbPrevious.ForeColor = Color.FromArgb(64, 64, 64);
            tsbPrevious.ImageTransparentColor = Color.Magenta;
            tsbPrevious.Margin = new Padding(4);
            tsbPrevious.Name = "tsbPrevious";
            tsbPrevious.Size = new Size(160, 28);
            tsbPrevious.Text = "Previous Record";
            tsbPrevious.ToolTipText = "Go to Previous Record (Ctrl+Left)";
            tsbPrevious.Click += tsbPrevious_Click;
            // 
            // tsbNext
            // 
            tsbNext.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbNext.Image = (Image)resources.GetObject("tsbNext.Image");
            tsbNext.ForeColor = Color.FromArgb(64, 64, 64);
            tsbNext.ImageTransparentColor = Color.Magenta;
            tsbNext.Margin = new Padding(4);
            tsbNext.Name = "tsbNext";
            tsbNext.Size = new Size(132, 28);
            tsbNext.Text = "Next Record";
            tsbNext.ToolTipText = "Go to Next Record (Ctrl+Right)";
            tsbNext.Click += tsbNext_Click;
            // 
            // tsbLast
            // 
            tsbLast.DisplayStyle = ToolStripItemDisplayStyle.Text;
            tsbLast.ForeColor = Color.FromArgb(64, 64, 64);
            tsbLast.ImageTransparentColor = Color.Magenta;
            tsbLast.Margin = new Padding(4);
            tsbLast.Name = "tsbLast";
            tsbLast.Size = new Size(102, 28);
            tsbLast.Text = "Last Record";
            tsbLast.ToolTipText = "Go to Last Record (Ctrl+End)";
            tsbLast.Click += tsbLast_Click;
            // 
            // toolStripSeparator2
            // 
            toolStripSeparator2.Margin = new Padding(10, 0, 10, 0);
            toolStripSeparator2.Name = "toolStripSeparator2";
            toolStripSeparator2.Size = new Size(6, 36);
            // 
            // txtSearch
            // 
            txtSearch.Alignment = ToolStripItemAlignment.Right;
            txtSearch.BackColor = Color.White;
            txtSearch.BorderStyle = BorderStyle.FixedSingle;
            txtSearch.Font = new Font("Segoe UI", 10F);
            txtSearch.ForeColor = Color.FromArgb(64, 64, 64);
            txtSearch.Margin = new Padding(1, 2, 6, 2);
            txtSearch.Name = "txtSearch";
            txtSearch.Size = new Size(200, 27);
            txtSearch.ToolTipText = "Enter search term and press Enter or click Search";
            txtSearch.KeyDown += txtSearch_KeyDown;
            // 
            // tsbSearch
            // 
            tsbSearch.Alignment = ToolStripItemAlignment.Right;
            tsbSearch.DisplayStyle = ToolStripItemDisplayStyle.Image;
            tsbSearch.Image = (Image)resources.GetObject("tsbSearch.Image");
            tsbSearch.ImageTransparentColor = Color.Magenta;
            tsbSearch.Margin = new Padding(1, 2, 1, 2);
            tsbSearch.Name = "tsbSearch";
            tsbSearch.Size = new Size(28, 28);
            tsbSearch.Text = "Search";
            tsbSearch.ToolTipText = "Search Suppliers";
            tsbSearch.Click += tsbSearch_Click;
            // 
            // statusStrip1
            // 
            statusStrip1.BackColor = Color.FromArgb(248, 248, 248);
            statusStrip1.ImageScalingSize = new Size(20, 20);
            statusStrip1.Items.AddRange(new ToolStripItem[] { lblStatus });
            statusStrip1.Location = new Point(0, 442);
            statusStrip1.Name = "statusStrip1";
            statusStrip1.Padding = new Padding(1, 0, 16, 0);
            statusStrip1.Size = new Size(1118, 22);
            statusStrip1.TabIndex = 2;
            statusStrip1.Text = "statusStrip1";
            // 
            // lblStatus
            // 
            lblStatus.Font = new Font("Segoe UI", 9F);
            lblStatus.ForeColor = Color.FromArgb(80, 80, 80);
            lblStatus.Name = "lblStatus";
            lblStatus.Size = new Size(1101, 16);
            lblStatus.Spring = true;
            lblStatus.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // supplierBindingSource
            // 
            supplierBindingSource.DataSource = typeof(Supplier);
            supplierBindingSource.CurrentChanged += supplierBindingSource_CurrentChanged;
            // 
            // groupBoxDetails
            // 
            groupBoxDetails.Controls.Add(tableLayoutPanelDetails);
            groupBoxDetails.Dock = DockStyle.Fill;
            groupBoxDetails.Font = new Font("Segoe UI Semibold", 10F, FontStyle.Bold);
            groupBoxDetails.ForeColor = Color.FromArgb(55, 55, 55);
            groupBoxDetails.Location = new Point(0, 46); 
            groupBoxDetails.Margin = new Padding(10);
            groupBoxDetails.Name = "groupBoxDetails";
            groupBoxDetails.Padding = new Padding(20);
            groupBoxDetails.Size = new Size(1118, 396); 
            groupBoxDetails.TabIndex = 1;
            groupBoxDetails.TabStop = false;
            groupBoxDetails.Text = "Supplier Details";
            // 
            // tableLayoutPanelDetails
            // 
            tableLayoutPanelDetails.ColumnCount = 2;
            tableLayoutPanelDetails.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 160F));
            tableLayoutPanelDetails.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            tableLayoutPanelDetails.Controls.Add(lblSupplierID, 0, 0);
            tableLayoutPanelDetails.Controls.Add(txtSupplierID, 1, 0);
            tableLayoutPanelDetails.Controls.Add(lblSupplierName, 0, 1);
            tableLayoutPanelDetails.Controls.Add(txtSupplierName, 1, 1);
            tableLayoutPanelDetails.Controls.Add(lblContactPerson, 0, 2);
            tableLayoutPanelDetails.Controls.Add(txtContactPerson, 1, 2);
            tableLayoutPanelDetails.Controls.Add(lblPhoneNumber, 0, 3);
            tableLayoutPanelDetails.Controls.Add(txtPhoneNumber, 1, 3);
            tableLayoutPanelDetails.Controls.Add(lblEmail, 0, 4);
            tableLayoutPanelDetails.Controls.Add(txtEmail, 1, 4);
            tableLayoutPanelDetails.Dock = DockStyle.Fill;
            tableLayoutPanelDetails.Location = new Point(20, 43);
            tableLayoutPanelDetails.Margin = new Padding(0);
            tableLayoutPanelDetails.Name = "tableLayoutPanelDetails";
            tableLayoutPanelDetails.RowCount = 6;
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableLayoutPanelDetails.Size = new Size(1078, 333); 
            tableLayoutPanelDetails.TabIndex = 0;
            // 
            // lblSupplierID
            // 
            lblSupplierID.Anchor = AnchorStyles.Left;
            lblSupplierID.AutoSize = true;
            lblSupplierID.Font = new Font("Segoe UI", 10F);
            lblSupplierID.ForeColor = Color.FromArgb(80, 80, 80);
            lblSupplierID.Location = new Point(3, 11);
            lblSupplierID.Name = "lblSupplierID";
            lblSupplierID.Size = new Size(98, 23);
            lblSupplierID.TabIndex = 0;
            lblSupplierID.Text = "Supplier ID:";
            // 
            // txtSupplierID
            // 
            txtSupplierID.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            txtSupplierID.BackColor = Color.FromArgb(245, 245, 245);
            txtSupplierID.BorderStyle = BorderStyle.FixedSingle;
            txtSupplierID.Font = new Font("Segoe UI", 10F);
            txtSupplierID.ForeColor = Color.FromArgb(100, 100, 100);
            txtSupplierID.Location = new Point(163, 7);
            txtSupplierID.Margin = new Padding(3, 4, 10, 4);
            txtSupplierID.Name = "txtSupplierID";
            txtSupplierID.ReadOnly = true;
            txtSupplierID.Size = new Size(905, 30);
            txtSupplierID.TabIndex = 99; // Non-focusable
            txtSupplierID.TabStop = false;
            // 
            // lblSupplierName
            // 
            lblSupplierName.Anchor = AnchorStyles.Left;
            lblSupplierName.AutoSize = true;
            lblSupplierName.Font = new Font("Segoe UI", 10F);
            lblSupplierName.ForeColor = Color.FromArgb(80, 80, 80);
            lblSupplierName.Location = new Point(3, 56);
            lblSupplierName.Name = "lblSupplierName";
            lblSupplierName.Size = new Size(127, 23);
            lblSupplierName.TabIndex = 2;
            lblSupplierName.Text = "Supplier Name:";
            // 
            // txtSupplierName
            // 
            txtSupplierName.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            txtSupplierName.BorderStyle = BorderStyle.FixedSingle;
            txtSupplierName.Font = new Font("Segoe UI", 10F);
            txtSupplierName.ForeColor = Color.FromArgb(50, 50, 50);
            txtSupplierName.Location = new Point(163, 52);
            txtSupplierName.Margin = new Padding(3, 4, 10, 4);
            txtSupplierName.MaxLength = 100;
            txtSupplierName.Name = "txtSupplierName";
            txtSupplierName.Size = new Size(905, 30);
            txtSupplierName.TabIndex = 0;
            // 
            // lblContactPerson
            // 
            lblContactPerson.Anchor = AnchorStyles.Left;
            lblContactPerson.AutoSize = true;
            lblContactPerson.Font = new Font("Segoe UI", 10F);
            lblContactPerson.ForeColor = Color.FromArgb(80, 80, 80);
            lblContactPerson.Location = new Point(3, 101);
            lblContactPerson.Name = "lblContactPerson";
            lblContactPerson.Size = new Size(130, 23);
            lblContactPerson.TabIndex = 4;
            lblContactPerson.Text = "Contact Person:";
            // 
            // txtContactPerson
            // 
            txtContactPerson.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            txtContactPerson.BorderStyle = BorderStyle.FixedSingle;
            txtContactPerson.Font = new Font("Segoe UI", 10F);
            txtContactPerson.ForeColor = Color.FromArgb(50, 50, 50);
            txtContactPerson.Location = new Point(163, 97);
            txtContactPerson.Margin = new Padding(3, 4, 10, 4);
            txtContactPerson.MaxLength = 100;
            txtContactPerson.Name = "txtContactPerson";
            txtContactPerson.Size = new Size(905, 30);
            txtContactPerson.TabIndex = 1;
            // 
            // lblPhoneNumber
            // 
            lblPhoneNumber.Anchor = AnchorStyles.Left;
            lblPhoneNumber.AutoSize = true;
            lblPhoneNumber.Font = new Font("Segoe UI", 10F);
            lblPhoneNumber.ForeColor = Color.FromArgb(80, 80, 80);
            lblPhoneNumber.Location = new Point(3, 146);
            lblPhoneNumber.Name = "lblPhoneNumber";
            lblPhoneNumber.Size = new Size(131, 23);
            lblPhoneNumber.TabIndex = 6;
            lblPhoneNumber.Text = "Phone Number:";
            // 
            // txtPhoneNumber
            // 
            txtPhoneNumber.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            txtPhoneNumber.BorderStyle = BorderStyle.FixedSingle;
            txtPhoneNumber.Font = new Font("Segoe UI", 10F);
            txtPhoneNumber.ForeColor = Color.FromArgb(50, 50, 50);
            txtPhoneNumber.Location = new Point(163, 142);
            txtPhoneNumber.Margin = new Padding(3, 4, 10, 4);
            txtPhoneNumber.MaxLength = 20;
            txtPhoneNumber.Name = "txtPhoneNumber";
            txtPhoneNumber.Size = new Size(905, 30);
            txtPhoneNumber.TabIndex = 2;
            // 
            // lblEmail
            // 
            lblEmail.Anchor = AnchorStyles.Left;
            lblEmail.AutoSize = true;
            lblEmail.Font = new Font("Segoe UI", 10F);
            lblEmail.ForeColor = Color.FromArgb(80, 80, 80);
            lblEmail.Location = new Point(3, 191);
            lblEmail.Name = "lblEmail";
            lblEmail.Size = new Size(55, 23);
            lblEmail.TabIndex = 8;
            lblEmail.Text = "Email:";
            // 
            // txtEmail
            // 
            txtEmail.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            txtEmail.BorderStyle = BorderStyle.FixedSingle;
            txtEmail.Font = new Font("Segoe UI", 10F);
            txtEmail.ForeColor = Color.FromArgb(50, 50, 50);
            txtEmail.Location = new Point(163, 187);
            txtEmail.Margin = new Padding(3, 4, 10, 4);
            txtEmail.MaxLength = 100;
            txtEmail.Name = "txtEmail";
            txtEmail.Size = new Size(905, 30);
            txtEmail.TabIndex = 3;
            // 
            // frmSuppliers
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.White;
            ClientSize = new Size(1118, 464);
            Controls.Add(groupBoxDetails);
            Controls.Add(statusStrip1);
            Controls.Add(toolStrip1);
            Font = new Font("Segoe UI", 9F);
            ForeColor = Color.FromArgb(64, 64, 64);
            MinimumSize = new Size(600, 450); // Adjusted min height
            Name = "frmSuppliers";
            Text = "Manage Suppliers";
            Load += frmSuppliers_Load;
            toolStrip1.ResumeLayout(false);
            toolStrip1.PerformLayout();
            statusStrip1.ResumeLayout(false);
            statusStrip1.PerformLayout();
            ((ISupportInitialize)supplierBindingSource).EndInit();
            groupBoxDetails.ResumeLayout(false);
            tableLayoutPanelDetails.ResumeLayout(false);
            tableLayoutPanelDetails.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }
        #endregion

        private ToolStrip toolStrip1;
        private ToolStripButton tsbNew;
        private ToolStripButton tsbSave;
        private ToolStripButton tsbDelete;
        private ToolStripSeparator toolStripSeparator1;
        private ToolStripButton tsbFirst;
        private ToolStripButton tsbPrevious;
        private ToolStripButton tsbNext;
        private ToolStripButton tsbLast;
        private ToolStripSeparator toolStripSeparator2;
        private ToolStripTextBox txtSearch;
        private ToolStripButton tsbSearch;
        private StatusStrip statusStrip1;
        private ToolStripStatusLabel lblStatus;
        private BindingSource supplierBindingSource;
        private GroupBox groupBoxDetails;
        private TableLayoutPanel tableLayoutPanelDetails;
        private Label lblSupplierID;
        private TextBox txtSupplierID;
        private Label lblSupplierName;
        private TextBox txtSupplierName;
        private Label lblContactPerson;
        private TextBox txtContactPerson;
        private Label lblPhoneNumber;
        private TextBox txtPhoneNumber;
        private Label lblEmail;
        private TextBox txtEmail;
    }
}
```

---
**File 4: `frmSuppliers.cs`**
---
```csharp
using Microsoft.EntityFrameworkCore;
using Store.Data.Models;
using Store.Services;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Store.Forms
{
    public partial class frmSuppliers : Form
    {
        private readonly SupplierService _supplierService;
        private bool _isNew = false;
        private bool _isLoading = false;

        public frmSuppliers(SupplierService supplierService)
        {
            InitializeComponent();
            _supplierService = supplierService;
        }

        private async void frmSuppliers_Load(object sender, EventArgs e)
        {
            _isLoading = true;
            await LoadDataAsync();
            SetupBindings();
            _isLoading = false;
            if (supplierBindingSource.Count > 0 && supplierBindingSource.Position < 0)
            {
                supplierBindingSource.MoveFirst();
            }
            UpdateButtonStates();
            UpdateNavigationState();
        }

        private async Task LoadDataAsync(string? searchTerm = null)
        {
            ToggleControls(false, true);
            lblStatus.Text = "Loading suppliers...";
            try
            {
                List<Supplier> suppliers;
                if (string.IsNullOrWhiteSpace(searchTerm))
                {
                    suppliers = await _supplierService.GetAllSuppliersAsync();
                }
                else
                {
                    suppliers = await _supplierService.SearchSuppliersAsync(searchTerm);
                }

                var currentId = (supplierBindingSource.Current as Supplier)?.SupplierID;

                supplierBindingSource.DataSource = suppliers;
                supplierBindingSource.ResetBindings(false);

                if (suppliers.Count == 0)
                {
                    lblStatus.Text = string.IsNullOrWhiteSpace(searchTerm) ? "No suppliers found. Click 'New' to add one." : $"No suppliers matching '{searchTerm}'.";
                    ClearForm();
                    SetupBindings(); 
                }
                else
                {
                    lblStatus.Text = string.IsNullOrWhiteSpace(searchTerm) ? $"Displaying {suppliers.Count} suppliers." : $"Found {suppliers.Count} matching '{searchTerm}'.";
                    if (currentId.HasValue)
                    {
                        SelectSupplierById(currentId.Value, false);
                    }
                     if (supplierBindingSource.Position < 0 && suppliers.Count > 0)
                    {
                        supplierBindingSource.MoveFirst();
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading suppliers: {ex.Message}", "Loading Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Error loading data.";
            }
            finally
            {
                if (!_isLoading)
                {
                    UpdateButtonStates();
                    UpdateNavigationState();
                }
                ToggleControls(true, true);
            }
        }

        private void SetupBindings()
        {
            txtSupplierID.DataBindings.Clear();
            txtSupplierName.DataBindings.Clear();
            txtContactPerson.DataBindings.Clear();
            txtPhoneNumber.DataBindings.Clear();
            txtEmail.DataBindings.Clear();

            txtSupplierID.DataBindings.Add("Text", supplierBindingSource, "SupplierID", true, DataSourceUpdateMode.Never);
            txtSupplierName.DataBindings.Add("Text", supplierBindingSource, "SupplierName", false, DataSourceUpdateMode.OnValidation);
            txtContactPerson.DataBindings.Add("Text", supplierBindingSource, "ContactPerson", true, DataSourceUpdateMode.OnValidation, string.Empty);
            txtPhoneNumber.DataBindings.Add("Text", supplierBindingSource, "PhoneNumber", true, DataSourceUpdateMode.OnValidation, string.Empty);
            txtEmail.DataBindings.Add("Text", supplierBindingSource, "Email", true, DataSourceUpdateMode.OnValidation, string.Empty);
        }

        private void ClearForm()
        {
            supplierBindingSource.SuspendBinding();
            txtSupplierID.Clear();
            txtSupplierName.Clear();
            txtContactPerson.Clear();
            txtPhoneNumber.Clear();
            txtEmail.Clear();
            supplierBindingSource.ResumeBinding();
        }
        
        private void ToggleControls(bool enabled, bool keepToolbarEnabled = false)
        {
            groupBoxDetails.Enabled = enabled;
            if (!keepToolbarEnabled) toolStrip1.Enabled = enabled;
            else toolStrip1.Enabled = true;
            this.Cursor = enabled ? Cursors.Default : Cursors.WaitCursor;
        }

        private void UpdateButtonStates()
        {
            if (_isLoading) return;
            bool hasItems = supplierBindingSource.Count > 0;
            bool isItemSelected = supplierBindingSource.Current != null;

            tsbSave.Enabled = _isNew || (isItemSelected && !string.IsNullOrWhiteSpace(txtSupplierName.Text));
            tsbDelete.Enabled = isItemSelected && !_isNew;
            tsbFirst.Enabled = isItemSelected && !_isNew && supplierBindingSource.Position > 0;
            tsbPrevious.Enabled = isItemSelected && !_isNew && supplierBindingSource.Position > 0;
            tsbNext.Enabled = isItemSelected && !_isNew && supplierBindingSource.Position < supplierBindingSource.Count - 1;
            tsbLast.Enabled = isItemSelected && !_isNew && supplierBindingSource.Position < supplierBindingSource.Count - 1;
            tsbNew.Enabled = toolStrip1.Enabled;
            txtSearch.Enabled = toolStrip1.Enabled;
            tsbSearch.Enabled = toolStrip1.Enabled;
        }

        private void UpdateNavigationState()
        {
            if (_isLoading) return;
            bool hasItems = supplierBindingSource.Count > 0;
            bool isItemSelected = supplierBindingSource.Current != null;

            if (_isNew)
            {
                lblStatus.Text = "Adding new supplier...";
                groupBoxDetails.Enabled = true;
            }
            else if (isItemSelected)
            {
                lblStatus.Text = $"Record {supplierBindingSource.Position + 1} of {supplierBindingSource.Count}";
                groupBoxDetails.Enabled = true;
            }
            else
            {
                lblStatus.Text = hasItems ? "No supplier selected." : (string.IsNullOrWhiteSpace(txtSearch.Text) ? "No suppliers found." : $"No suppliers matching '{txtSearch.Text}'.");
                groupBoxDetails.Enabled = false;
                if (!hasItems) ClearForm();
            }
             UpdateButtonStates();
        }

        private void tsbNew_Click(object sender, EventArgs e)
        {
            _isNew = true;
            supplierBindingSource.SuspendBinding();
            ClearForm();
            txtSupplierName.Focus();
            UpdateNavigationState();
        }

        private async void tsbSave_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtSupplierName.Text))
            {
                MessageBox.Show("Supplier Name cannot be empty.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                txtSupplierName.Focus();
                return;
            }
            // Basic email validation (optional, enhance as needed)
            if (!string.IsNullOrWhiteSpace(txtEmail.Text) && !txtEmail.Text.Contains("@"))
            {
                MessageBox.Show("Please enter a valid email address or leave it empty.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                txtEmail.Focus();
                return;
            }

            if (!_isNew && supplierBindingSource.Current != null)
            {
                supplierBindingSource.EndEdit();
            }

            ToggleControls(false);
            lblStatus.Text = "Saving...";

            try
            {
                bool success = false;
                Supplier? supplierToSave = null;
                bool wasNewItemInitially = _isNew;

                if (_isNew)
                {
                    supplierToSave = new Supplier
                    {
                        SupplierName = txtSupplierName.Text.Trim(),
                        ContactPerson = string.IsNullOrWhiteSpace(txtContactPerson.Text) ? null : txtContactPerson.Text.Trim(),
                        PhoneNumber = string.IsNullOrWhiteSpace(txtPhoneNumber.Text) ? null : txtPhoneNumber.Text.Trim(),
                        Email = string.IsNullOrWhiteSpace(txtEmail.Text) ? null : txtEmail.Text.Trim()
                    };
                    success = await _supplierService.AddSupplierAsync(supplierToSave);
                     if (success) lblStatus.Text = "Supplier added successfully.";
                }
                else
                {
                    if (supplierBindingSource.Current is Supplier currentSupplier)
                    {
                        currentSupplier.SupplierName = txtSupplierName.Text.Trim();
                        currentSupplier.ContactPerson = string.IsNullOrWhiteSpace(txtContactPerson.Text) ? null : txtContactPerson.Text.Trim();
                        currentSupplier.PhoneNumber = string.IsNullOrWhiteSpace(txtPhoneNumber.Text) ? null : txtPhoneNumber.Text.Trim();
                        currentSupplier.Email = string.IsNullOrWhiteSpace(txtEmail.Text) ? null : txtEmail.Text.Trim();
                        supplierToSave = currentSupplier;
                        success = await _supplierService.UpdateSupplierAsync(currentSupplier);
                        if (success) lblStatus.Text = "Supplier updated successfully.";
                    }
                    else
                    {
                         MessageBox.Show("No supplier selected to update.", "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                         lblStatus.Text = "No supplier selected.";
                    }
                }

                if (success)
                {
                    _isNew = false;
                    int savedItemId = supplierToSave?.SupplierID ?? -1;
                    string? currentSearchTerm = wasNewItemInitially ? null : txtSearch.Text;
                    if (wasNewItemInitially) txtSearch.Clear();
                    
                    await LoadDataAsync(currentSearchTerm);
                    
                    if (savedItemId > 0) SelectSupplierById(savedItemId);
                    else if(supplierBindingSource.Count > 0) supplierBindingSource.MoveFirst();
                }
            }
            catch (DbUpdateConcurrencyException)
            {
                MessageBox.Show("The record was modified. Please reload and try again.", "Concurrency Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                lblStatus.Text = "Save failed due to concurrency.";
                await LoadDataAsync(txtSearch.Text);
            }
            catch (DbUpdateException dbEx)
            {
                string errorMessage = $"Database error: {dbEx.InnerException?.Message ?? dbEx.Message}.";
                 if (dbEx.InnerException?.Message.Contains("UNIQUE KEY constraint") == true || 
                    dbEx.InnerException?.Message.Contains("duplicate key value violates unique constraint") == true)
                {
                    errorMessage += "\nA supplier with the same name or email might already exist if they are unique.";
                }
                MessageBox.Show(errorMessage, "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Database save error.";
            }
            catch (Exception ex)
            {
                MessageBox.Show($"An error occurred: {ex.Message}", "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Save error.";
            }
            finally
            {
                 if (!success) { 
                     ToggleControls(true);
                     UpdateButtonStates();
                     UpdateNavigationState();
                }
            }
        }

        private async void tsbDelete_Click(object sender, EventArgs e)
        {
             if (_isNew) {
                MessageBox.Show("Cannot delete an unsaved new supplier.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }
            if (supplierBindingSource.Current is Supplier currentSupplier)
            {
                var confirmResult = MessageBox.Show($"Delete supplier '{currentSupplier.SupplierName}' (ID: {currentSupplier.SupplierID})?", "Confirm Delete", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                if (confirmResult == DialogResult.Yes)
                {
                    ToggleControls(false);
                    lblStatus.Text = "Deleting...";
                    try
                    {
                        bool success = await _supplierService.DeleteSupplierAsync(currentSupplier.SupplierID);
                        if (success) lblStatus.Text = "Supplier deleted.";
                        await LoadDataAsync(txtSearch.Text.Trim());
                    }
                    catch (DbUpdateException dbEx)
                    {
                        MessageBox.Show($"Database error: {dbEx.InnerException?.Message ?? dbEx.Message}.\nSupplier might have related products.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        lblStatus.Text = "Database delete error.";
                        await LoadDataAsync(txtSearch.Text.Trim());
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"An error occurred: {ex.Message}", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        lblStatus.Text = "Delete error.";
                        await LoadDataAsync(txtSearch.Text.Trim());
                    }
                }
            }
            else
            {
                MessageBox.Show("No supplier selected.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private async void PerformSearch()
        {
            _isNew = false; supplierBindingSource.ResumeBinding();
            await LoadDataAsync(txtSearch.Text.Trim());
        }
        private void tsbSearch_Click(object sender, EventArgs e) => PerformSearch();
        private void txtSearch_KeyDown(object sender, KeyEventArgs e) { if (e.KeyCode == Keys.Enter) { PerformSearch(); e.SuppressKeyPress = true; } }
        private void tsbFirst_Click(object sender, EventArgs e) { if (_isNew) _isNew = false; supplierBindingSource.ResumeBinding(); supplierBindingSource.MoveFirst(); }
        private void tsbPrevious_Click(object sender, EventArgs e) { if (_isNew) _isNew = false; supplierBindingSource.ResumeBinding(); supplierBindingSource.MovePrevious(); }
        private void tsbNext_Click(object sender, EventArgs e) { if (_isNew) _isNew = false; supplierBindingSource.ResumeBinding(); supplierBindingSource.MoveNext(); }
        private void tsbLast_Click(object sender, EventArgs e) { if (_isNew) _isNew = false; supplierBindingSource.ResumeBinding(); supplierBindingSource.MoveLast(); }

        private void supplierBindingSource_CurrentChanged(object sender, EventArgs e)
        {
            if (_isLoading || _isNew) return;
            if (supplierBindingSource.Current == null) ClearForm();
            UpdateButtonStates();
            UpdateNavigationState();
        }

        private void SelectSupplierById(int supplierId, bool triggerCurrentChanged = true)
        {
            if (supplierId <= 0) return;
            if (supplierBindingSource.DataSource is List<Supplier> suppliers)
            {
                int index = suppliers.FindIndex(s => s.SupplierID == supplierId);
                if (index != -1)
                {
                    if(!triggerCurrentChanged)
                    {
                        this.supplierBindingSource.CurrentChanged -= supplierBindingSource_CurrentChanged;
                        supplierBindingSource.Position = index;
                        this.supplierBindingSource.CurrentChanged += supplierBindingSource_CurrentChanged;
                        if(supplierBindingSource.Current is Supplier sup)
                        {
                            txtSupplierID.Text = sup.SupplierID.ToString();
                            txtSupplierName.Text = sup.SupplierName;
                            txtContactPerson.Text = sup.ContactPerson;
                            txtPhoneNumber.Text = sup.PhoneNumber;
                            txtEmail.Text = sup.Email;
                        }
                    }
                    else
                    {
                         supplierBindingSource.Position = index;
                    }
                }
            }
        }
    }
}
```

---
**File 5: `frmProducts.Designer.cs`**
---
```csharp
using System;
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;
using Store.Data.Models;

namespace Store.Forms
{
    partial class frmProducts
    {
        private System.ComponentModel.IContainer components = null;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null)) { components.Dispose(); }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code
        private void InitializeComponent()
        {
            components = new Container();
            ComponentResourceManager resources = new ComponentResourceManager(typeof(frmProducts));
            toolStrip1 = new ToolStrip();
            tsbNew = new ToolStripButton();
            tsbSave = new ToolStripButton();
            tsbDelete = new ToolStripButton();
            toolStripSeparator1 = new ToolStripSeparator();
            tsbFirst = new ToolStripButton();
            tsbPrevious = new ToolStripButton();
            tsbNext = new ToolStripButton();
            tsbLast = new ToolStripButton();
            toolStripSeparator2 = new ToolStripSeparator();
            txtSearch = new ToolStripTextBox();
            tsbSearch = new ToolStripButton();
            statusStrip1 = new StatusStrip();
            lblStatus = new ToolStripStatusLabel();
            productBindingSource = new BindingSource(components);
            groupBoxDetails = new GroupBox();
            tableLayoutPanelDetails = new TableLayoutPanel();
            lblProductID = new Label();
            txtProductID = new TextBox();
            lblProductName = new Label();
            txtProductName = new TextBox();
            lblDescription = new Label();
            txtDescription = new TextBox();
            lblCategory = new Label();
            cmbCategory = new ComboBox();
            categoryBindingSource = new BindingSource(components); // For cmbCategory
            lblSupplier = new Label();
            cmbSupplier = new ComboBox();
            supplierBindingSource = new BindingSource(components); // For cmbSupplier
            lblPurchasePrice = new Label();
            txtPurchasePrice = new TextBox();
            lblSellingPrice = new Label();
            txtSellingPrice = new TextBox();
            lblStockQuantity = new Label();
            txtStockQuantity = new TextBox();
            toolStrip1.SuspendLayout();
            statusStrip1.SuspendLayout();
            ((ISupportInitialize)productBindingSource).BeginInit();
            ((ISupportInitialize)categoryBindingSource).BeginInit();
            ((ISupportInitialize)supplierBindingSource).BeginInit();
            groupBoxDetails.SuspendLayout();
            tableLayoutPanelDetails.SuspendLayout();
            SuspendLayout();
            // 
            // toolStrip1
            // 
            toolStrip1.BackColor = Color.FromArgb(240, 240, 240);
            toolStrip1.Font = new Font("Segoe UI", 10F);
            toolStrip1.GripStyle = ToolStripGripStyle.Hidden;
            toolStrip1.ImageScalingSize = new Size(24, 24);
            toolStrip1.Items.AddRange(new ToolStripItem[] { tsbNew, tsbSave, tsbDelete, toolStripSeparator1, tsbFirst, tsbPrevious, tsbNext, tsbLast, toolStripSeparator2, txtSearch, tsbSearch });
            toolStrip1.Location = new Point(0, 0);
            toolStrip1.Name = "toolStrip1";
            toolStrip1.Padding = new Padding(8, 5, 8, 5);
            toolStrip1.RenderMode = ToolStripRenderMode.System;
            toolStrip1.Size = new Size(1118, 46);
            toolStrip1.TabIndex = 0;
            toolStrip1.Text = "toolStrip1";
            // 
            // tsbNew
            // 
            tsbNew.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbNew.Image = (Image)resources.GetObject("tsbNew.Image");
            tsbNew.ForeColor = Color.FromArgb(64, 64, 64);
            tsbNew.ImageTransparentColor = Color.Magenta;
            tsbNew.Margin = new Padding(4);
            tsbNew.Name = "tsbNew";
            tsbNew.Size = new Size(136, 28); 
            tsbNew.Text = "New Product";
            tsbNew.ToolTipText = "Add New Product (Ctrl+N)";
            tsbNew.Click += tsbNew_Click;
            // 
            // tsbSave
            // 
            tsbSave.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbSave.Image = (Image)resources.GetObject("tsbSave.Image");
            tsbSave.ForeColor = Color.FromArgb(64, 64, 64);
            tsbSave.ImageTransparentColor = Color.Magenta;
            tsbSave.Margin = new Padding(4);
            tsbSave.Name = "tsbSave";
            tsbSave.Size = new Size(144, 28);
            tsbSave.Text = "Save Changes";
            tsbSave.ToolTipText = "Save Changes (Ctrl+S)";
            tsbSave.Click += tsbSave_Click;
            // 
            // tsbDelete
            // 
            tsbDelete.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbDelete.Image = (Image)resources.GetObject("tsbDelete.Image");
            tsbDelete.ForeColor = Color.FromArgb(64, 64, 64);
            tsbDelete.ImageTransparentColor = Color.Magenta;
            tsbDelete.Margin = new Padding(4);
            tsbDelete.Name = "tsbDelete";
            tsbDelete.Size = new Size(151, 28); 
            tsbDelete.Text = "Delete Product";
            tsbDelete.ToolTipText = "Delete Selected Product (Del)";
            tsbDelete.Click += tsbDelete_Click;
            // 
            // toolStripSeparator1
            // 
            toolStripSeparator1.Margin = new Padding(10, 0, 10, 0);
            toolStripSeparator1.Name = "toolStripSeparator1";
            toolStripSeparator1.Size = new Size(6, 36);
            // 
            // tsbFirst
            // 
            tsbFirst.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbFirst.Image = (Image)resources.GetObject("tsbFirst.Image");
            tsbFirst.ForeColor = Color.FromArgb(64, 64, 64);
            tsbFirst.ImageTransparentColor = Color.Magenta;
            tsbFirst.Margin = new Padding(4);
            tsbFirst.Name = "tsbFirst";
            tsbFirst.Size = new Size(127, 28);
            tsbFirst.Text = "First Record";
            tsbFirst.ToolTipText = "Go to First Record (Ctrl+Home)";
            tsbFirst.Click += tsbFirst_Click;
            // 
            // tsbPrevious
            // 
            tsbPrevious.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbPrevious.Image = (Image)resources.GetObject("tsbPrevious.Image");
            tsbPrevious.ForeColor = Color.FromArgb(64, 64, 64);
            tsbPrevious.ImageTransparentColor = Color.Magenta;
            tsbPrevious.Margin = new Padding(4);
            tsbPrevious.Name = "tsbPrevious";
            tsbPrevious.Size = new Size(160, 28);
            tsbPrevious.Text = "Previous Record";
            tsbPrevious.ToolTipText = "Go to Previous Record (Ctrl+Left)";
            tsbPrevious.Click += tsbPrevious_Click;
            // 
            // tsbNext
            // 
            tsbNext.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbNext.Image = (Image)resources.GetObject("tsbNext.Image");
            tsbNext.ForeColor = Color.FromArgb(64, 64, 64);
            tsbNext.ImageTransparentColor = Color.Magenta;
            tsbNext.Margin = new Padding(4);
            tsbNext.Name = "tsbNext";
            tsbNext.Size = new Size(132, 28);
            tsbNext.Text = "Next Record";
            tsbNext.ToolTipText = "Go to Next Record (Ctrl+Right)";
            tsbNext.Click += tsbNext_Click;
            // 
            // tsbLast
            // 
            tsbLast.DisplayStyle = ToolStripItemDisplayStyle.Text;
            tsbLast.ForeColor = Color.FromArgb(64, 64, 64);
            tsbLast.ImageTransparentColor = Color.Magenta;
            tsbLast.Margin = new Padding(4);
            tsbLast.Name = "tsbLast";
            tsbLast.Size = new Size(102, 28);
            tsbLast.Text = "Last Record";
            tsbLast.ToolTipText = "Go to Last Record (Ctrl+End)";
            tsbLast.Click += tsbLast_Click;
            // 
            // toolStripSeparator2
            // 
            toolStripSeparator2.Margin = new Padding(10, 0, 10, 0);
            toolStripSeparator2.Name = "toolStripSeparator2";
            toolStripSeparator2.Size = new Size(6, 36);
            // 
            // txtSearch
            // 
            txtSearch.Alignment = ToolStripItemAlignment.Right;
            txtSearch.BackColor = Color.White;
            txtSearch.BorderStyle = BorderStyle.FixedSingle;
            txtSearch.Font = new Font("Segoe UI", 10F);
            txtSearch.ForeColor = Color.FromArgb(64, 64, 64);
            txtSearch.Margin = new Padding(1, 2, 6, 2);
            txtSearch.Name = "txtSearch";
            txtSearch.Size = new Size(200, 27);
            txtSearch.ToolTipText = "Enter search term and press Enter or click Search";
            txtSearch.KeyDown += txtSearch_KeyDown;
            // 
            // tsbSearch
            // 
            tsbSearch.Alignment = ToolStripItemAlignment.Right;
            tsbSearch.DisplayStyle = ToolStripItemDisplayStyle.Image;
            tsbSearch.Image = (Image)resources.GetObject("tsbSearch.Image");
            tsbSearch.ImageTransparentColor = Color.Magenta;
            tsbSearch.Margin = new Padding(1, 2, 1, 2);
            tsbSearch.Name = "tsbSearch";
            tsbSearch.Size = new Size(28, 28);
            tsbSearch.Text = "Search";
            tsbSearch.ToolTipText = "Search Products";
            tsbSearch.Click += tsbSearch_Click;
            // 
            // statusStrip1
            // 
            statusStrip1.BackColor = Color.FromArgb(248, 248, 248);
            statusStrip1.ImageScalingSize = new Size(20, 20);
            statusStrip1.Items.AddRange(new ToolStripItem[] { lblStatus });
            statusStrip1.Location = new Point(0, 592);
            statusStrip1.Name = "statusStrip1";
            statusStrip1.Padding = new Padding(1, 0, 16, 0);
            statusStrip1.Size = new Size(1118, 22);
            statusStrip1.TabIndex = 2;
            statusStrip1.Text = "statusStrip1";
            // 
            // lblStatus
            // 
            lblStatus.Font = new Font("Segoe UI", 9F);
            lblStatus.ForeColor = Color.FromArgb(80, 80, 80);
            lblStatus.Name = "lblStatus";
            lblStatus.Size = new Size(1101, 16);
            lblStatus.Spring = true;
            lblStatus.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // productBindingSource
            // 
            productBindingSource.DataSource = typeof(Product);
            productBindingSource.CurrentChanged += productBindingSource_CurrentChanged;
            // 
            // categoryBindingSource
            //
            categoryBindingSource.DataSource = typeof(Category);
            //
            // supplierBindingSource
            //
            supplierBindingSource.DataSource = typeof(Supplier);
            // 
            // groupBoxDetails
            // 
            groupBoxDetails.Controls.Add(tableLayoutPanelDetails);
            groupBoxDetails.Dock = DockStyle.Fill;
            groupBoxDetails.Font = new Font("Segoe UI Semibold", 10F, FontStyle.Bold);
            groupBoxDetails.ForeColor = Color.FromArgb(55, 55, 55);
            groupBoxDetails.Location = new Point(0, 46); 
            groupBoxDetails.Margin = new Padding(10);
            groupBoxDetails.Name = "groupBoxDetails";
            groupBoxDetails.Padding = new Padding(20);
            groupBoxDetails.Size = new Size(1118, 546); 
            groupBoxDetails.TabIndex = 1;
            groupBoxDetails.TabStop = false;
            groupBoxDetails.Text = "Product Details";
            // 
            // tableLayoutPanelDetails
            // 
            tableLayoutPanelDetails.ColumnCount = 2;
            tableLayoutPanelDetails.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 150F));
            tableLayoutPanelDetails.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            tableLayoutPanelDetails.Controls.Add(lblProductID, 0, 0);
            tableLayoutPanelDetails.Controls.Add(txtProductID, 1, 0);
            tableLayoutPanelDetails.Controls.Add(lblProductName, 0, 1);
            tableLayoutPanelDetails.Controls.Add(txtProductName, 1, 1);
            tableLayoutPanelDetails.Controls.Add(lblDescription, 0, 2);
            tableLayoutPanelDetails.Controls.Add(txtDescription, 1, 2);
            tableLayoutPanelDetails.Controls.Add(lblCategory, 0, 3);
            tableLayoutPanelDetails.Controls.Add(cmbCategory, 1, 3);
            tableLayoutPanelDetails.Controls.Add(lblSupplier, 0, 4);
            tableLayoutPanelDetails.Controls.Add(cmbSupplier, 1, 4);
            tableLayoutPanelDetails.Controls.Add(lblPurchasePrice, 0, 5);
            tableLayoutPanelDetails.Controls.Add(txtPurchasePrice, 1, 5);
            tableLayoutPanelDetails.Controls.Add(lblSellingPrice, 0, 6);
            tableLayoutPanelDetails.Controls.Add(txtSellingPrice, 1, 6);
            tableLayoutPanelDetails.Controls.Add(lblStockQuantity, 0, 7);
            tableLayoutPanelDetails.Controls.Add(txtStockQuantity, 1, 7);
            tableLayoutPanelDetails.Dock = DockStyle.Fill;
            tableLayoutPanelDetails.Location = new Point(20, 43);
            tableLayoutPanelDetails.Margin = new Padding(0);
            tableLayoutPanelDetails.Name = "tableLayoutPanelDetails";
            tableLayoutPanelDetails.RowCount = 9; // 8 for fields, 1 for spacer
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 80F)); // Description
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F)); // Category
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F)); // Supplier
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F)); // Purchase Price
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F)); // Selling Price
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F)); // Stock
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableLayoutPanelDetails.Size = new Size(1078, 483); 
            tableLayoutPanelDetails.TabIndex = 0;
            // 
            // lblProductID
            // 
            lblProductID.Anchor = AnchorStyles.Left; lblProductID.AutoSize = true;
            lblProductID.Font = new Font("Segoe UI", 10F); lblProductID.ForeColor = Color.FromArgb(80, 80, 80);
            lblProductID.Location = new Point(3, 11); lblProductID.Name = "lblProductID";
            lblProductID.Size = new Size(96, 23); lblProductID.TabIndex = 0; lblProductID.Text = "Product ID:";
            // 
            // txtProductID
            // 
            txtProductID.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            txtProductID.BackColor = Color.FromArgb(245, 245, 245); txtProductID.BorderStyle = BorderStyle.FixedSingle;
            txtProductID.Font = new Font("Segoe UI", 10F); txtProductID.ForeColor = Color.FromArgb(100, 100, 100);
            txtProductID.Location = new Point(153, 7); txtProductID.Margin = new Padding(3, 4, 10, 4);
            txtProductID.Name = "txtProductID"; txtProductID.ReadOnly = true;
            txtProductID.Size = new Size(915, 30); txtProductID.TabIndex = 99; txtProductID.TabStop = false;
            // 
            // lblProductName
            // 
            lblProductName.Anchor = AnchorStyles.Left; lblProductName.AutoSize = true;
            lblProductName.Font = new Font("Segoe UI", 10F); lblProductName.ForeColor = Color.FromArgb(80, 80, 80);
            lblProductName.Location = new Point(3, 56); lblProductName.Name = "lblProductName";
            lblProductName.Size = new Size(125, 23); lblProductName.TabIndex = 2; lblProductName.Text = "Product Name:";
            // 
            // txtProductName
            // 
            txtProductName.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            txtProductName.BorderStyle = BorderStyle.FixedSingle; txtProductName.Font = new Font("Segoe UI", 10F);
            txtProductName.ForeColor = Color.FromArgb(50, 50, 50);
            txtProductName.Location = new Point(153, 52); txtProductName.Margin = new Padding(3, 4, 10, 4);
            txtProductName.MaxLength = 100; txtProductName.Name = "txtProductName";
            txtProductName.Size = new Size(915, 30); txtProductName.TabIndex = 0;
            // 
            // lblDescription
            // 
            lblDescription.AutoSize = true; lblDescription.Font = new Font("Segoe UI", 10F);
            lblDescription.ForeColor = Color.FromArgb(80, 80, 80);
            lblDescription.Location = new Point(3, 98); 
            lblDescription.Margin = new Padding(3, 8, 3, 0); lblDescription.Name = "lblDescription";
            lblDescription.Size = new Size(100, 23); lblDescription.TabIndex = 4; lblDescription.Text = "Description:";
            // 
            // txtDescription
            // 
            txtDescription.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
            txtDescription.BorderStyle = BorderStyle.FixedSingle; txtDescription.Font = new Font("Segoe UI", 10F);
            txtDescription.ForeColor = Color.FromArgb(50, 50, 50);
            txtDescription.Location = new Point(153, 94); txtDescription.Margin = new Padding(3, 4, 10, 4);
            txtDescription.MaxLength = 1000; txtDescription.Multiline = true; txtDescription.Name = "txtDescription";
            txtDescription.ScrollBars = ScrollBars.Vertical; txtDescription.Size = new Size(915, 72);
            txtDescription.TabIndex = 1;
            // 
            // lblCategory
            // 
            lblCategory.Anchor = AnchorStyles.Left; lblCategory.AutoSize = true;
            lblCategory.Font = new Font("Segoe UI", 10F); lblCategory.ForeColor = Color.FromArgb(80, 80, 80);
            lblCategory.Location = new Point(3, 181); lblCategory.Name = "lblCategory";
            lblCategory.Size = new Size(83, 23); lblCategory.TabIndex = 6; lblCategory.Text = "Category:";
            // 
            // cmbCategory
            // 
            cmbCategory.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            cmbCategory.DataSource = categoryBindingSource; // Bind to its own source
            cmbCategory.DisplayMember = "CategoryName";
            cmbCategory.ValueMember = "CategoryID";
            cmbCategory.DropDownStyle = ComboBoxStyle.DropDownList;
            cmbCategory.Font = new Font("Segoe UI", 10F); cmbCategory.ForeColor = Color.FromArgb(50, 50, 50);
            cmbCategory.FormattingEnabled = true; cmbCategory.Location = new Point(153, 178);
            cmbCategory.Margin = new Padding(3, 4, 10, 4); cmbCategory.Name = "cmbCategory";
            cmbCategory.Size = new Size(915, 31); cmbCategory.TabIndex = 2;
            // 
            // lblSupplier
            // 
            lblSupplier.Anchor = AnchorStyles.Left; lblSupplier.AutoSize = true;
            lblSupplier.Font = new Font("Segoe UI", 10F); lblSupplier.ForeColor = Color.FromArgb(80, 80, 80);
            lblSupplier.Location = new Point(3, 226); lblSupplier.Name = "lblSupplier";
            lblSupplier.Size = new Size(76, 23); lblSupplier.TabIndex = 8; lblSupplier.Text = "Supplier:";
            // 
            // cmbSupplier
            // 
            cmbSupplier.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            cmbSupplier.DataSource = supplierBindingSource; // Bind to its own source
            cmbSupplier.DisplayMember = "SupplierName";
            cmbSupplier.ValueMember = "SupplierID";
            cmbSupplier.DropDownStyle = ComboBoxStyle.DropDownList;
            cmbSupplier.Font = new Font("Segoe UI", 10F); cmbSupplier.ForeColor = Color.FromArgb(50, 50, 50);
            cmbSupplier.FormattingEnabled = true; cmbSupplier.Location = new Point(153, 223);
            cmbSupplier.Margin = new Padding(3, 4, 10, 4); cmbSupplier.Name = "cmbSupplier";
            cmbSupplier.Size = new Size(915, 31); cmbSupplier.TabIndex = 3;
            // 
            // lblPurchasePrice
            // 
            lblPurchasePrice.Anchor = AnchorStyles.Left; lblPurchasePrice.AutoSize = true;
            lblPurchasePrice.Font = new Font("Segoe UI", 10F); lblPurchasePrice.ForeColor = Color.FromArgb(80, 80, 80);
            lblPurchasePrice.Location = new Point(3, 271); lblPurchasePrice.Name = "lblPurchasePrice";
            lblPurchasePrice.Size = new Size(125, 23); lblPurchasePrice.TabIndex = 10; lblPurchasePrice.Text = "Purchase Price:";
            // 
            // txtPurchasePrice
            // 
            txtPurchasePrice.Anchor = AnchorStyles.Left; 
            txtPurchasePrice.BorderStyle = BorderStyle.FixedSingle; txtPurchasePrice.Font = new Font("Segoe UI", 10F);
            txtPurchasePrice.ForeColor = Color.FromArgb(50, 50, 50);
            txtPurchasePrice.Location = new Point(153, 267); txtPurchasePrice.Margin = new Padding(3, 4, 10, 4);
            txtPurchasePrice.MaxLength = 15; txtPurchasePrice.Name = "txtPurchasePrice";
            txtPurchasePrice.Size = new Size(200, 30); txtPurchasePrice.TabIndex = 4;
            txtPurchasePrice.TextAlign = HorizontalAlignment.Right;
            // 
            // lblSellingPrice
            // 
            lblSellingPrice.Anchor = AnchorStyles.Left; lblSellingPrice.AutoSize = true;
            lblSellingPrice.Font = new Font("Segoe UI", 10F); lblSellingPrice.ForeColor = Color.FromArgb(80, 80, 80);
            lblSellingPrice.Location = new Point(3, 316); lblSellingPrice.Name = "lblSellingPrice";
            lblSellingPrice.Size = new Size(106, 23); lblSellingPrice.TabIndex = 12; lblSellingPrice.Text = "Selling Price:";
            // 
            // txtSellingPrice
            // 
            txtSellingPrice.Anchor = AnchorStyles.Left; 
            txtSellingPrice.BorderStyle = BorderStyle.FixedSingle; txtSellingPrice.Font = new Font("Segoe UI", 10F);
            txtSellingPrice.ForeColor = Color.FromArgb(50, 50, 50);
            txtSellingPrice.Location = new Point(153, 312); txtSellingPrice.Margin = new Padding(3, 4, 10, 4);
            txtSellingPrice.MaxLength = 15; txtSellingPrice.Name = "txtSellingPrice";
            txtSellingPrice.Size = new Size(200, 30); txtSellingPrice.TabIndex = 5;
            txtSellingPrice.TextAlign = HorizontalAlignment.Right;
            // 
            // lblStockQuantity
            // 
            lblStockQuantity.Anchor = AnchorStyles.Left; lblStockQuantity.AutoSize = true;
            lblStockQuantity.Font = new Font("Segoe UI", 10F); lblStockQuantity.ForeColor = Color.FromArgb(80, 80, 80);
            lblStockQuantity.Location = new Point(3, 361); lblStockQuantity.Name = "lblStockQuantity";
            lblStockQuantity.Size = new Size(125, 23); lblStockQuantity.TabIndex = 14; lblStockQuantity.Text = "Stock Quantity:";
            // 
            // txtStockQuantity
            // 
            txtStockQuantity.Anchor = AnchorStyles.Left;
            txtStockQuantity.BorderStyle = BorderStyle.FixedSingle; txtStockQuantity.Font = new Font("Segoe UI", 10F);
            txtStockQuantity.ForeColor = Color.FromArgb(50, 50, 50);
            txtStockQuantity.Location = new Point(153, 357); txtStockQuantity.Margin = new Padding(3, 4, 10, 4);
            txtStockQuantity.MaxLength = 10; txtStockQuantity.Name = "txtStockQuantity";
            txtStockQuantity.Size = new Size(150, 30); txtStockQuantity.TabIndex = 6;
            txtStockQuantity.TextAlign = HorizontalAlignment.Right;
            // 
            // frmProducts
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.White;
            ClientSize = new Size(1118, 614);
            Controls.Add(groupBoxDetails);
            Controls.Add(statusStrip1);
            Controls.Add(toolStrip1);
            Font = new Font("Segoe UI", 9F);
            ForeColor = Color.FromArgb(64, 64, 64);
            MinimumSize = new Size(700, 600); // Adjusted min height
            Name = "frmProducts";
            Text = "Manage Products";
            Load += frmProducts_Load;
            toolStrip1.ResumeLayout(false);
            toolStrip1.PerformLayout();
            statusStrip1.ResumeLayout(false);
            statusStrip1.PerformLayout();
            ((ISupportInitialize)productBindingSource).EndInit();
            ((ISupportInitialize)categoryBindingSource).EndInit();
            ((ISupportInitialize)supplierBindingSource).EndInit();
            groupBoxDetails.ResumeLayout(false);
            tableLayoutPanelDetails.ResumeLayout(false);
            tableLayoutPanelDetails.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }
        #endregion

        private ToolStrip toolStrip1;
        private ToolStripButton tsbNew;
        private ToolStripButton tsbSave;
        private ToolStripButton tsbDelete;
        private ToolStripSeparator toolStripSeparator1;
        private ToolStripButton tsbFirst;
        private ToolStripButton tsbPrevious;
        private ToolStripButton tsbNext;
        private ToolStripButton tsbLast;
        private ToolStripSeparator toolStripSeparator2;
        private ToolStripTextBox txtSearch;
        private ToolStripButton tsbSearch;
        private StatusStrip statusStrip1;
        private ToolStripStatusLabel lblStatus;
        private BindingSource productBindingSource;
        private BindingSource categoryBindingSource;
        private BindingSource supplierBindingSource;
        private GroupBox groupBoxDetails;
        private TableLayoutPanel tableLayoutPanelDetails;
        private Label lblProductID;
        private TextBox txtProductID;
        private Label lblProductName;
        private TextBox txtProductName;
        private Label lblDescription;
        private TextBox txtDescription;
        private Label lblCategory;
        private ComboBox cmbCategory;
        private Label lblSupplier;
        private ComboBox cmbSupplier;
        private Label lblPurchasePrice;
        private TextBox txtPurchasePrice;
        private Label lblSellingPrice;
        private TextBox txtSellingPrice;
        private Label lblStockQuantity;
        private TextBox txtStockQuantity;
    }
}
```

---
**File 6: `frmProducts.cs`**
---
```csharp
using Microsoft.EntityFrameworkCore;
using Store.Data.Models;
using Store.Services;
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Store.Forms
{
    public partial class frmProducts : Form
    {
        private readonly ProductService _productService;
        // Assuming ProductService can provide lists for dropdowns, 
        // or inject CategoryService and SupplierService if they handle that.
        // For this example, ProductService will have methods GetCategoriesForDropdownAsync and GetSuppliersForDropdownAsync
        private bool _isNew = false;
        private bool _isLoading = false;
        private bool _isLoadingComboBoxes = false;

        public frmProducts(ProductService productService)
        {
            InitializeComponent();
            _productService = productService;
        }

        private async void frmProducts_Load(object sender, EventArgs e)
        {
            _isLoading = true;
            _isLoadingComboBoxes = true;
            await LoadComboBoxesAsync();
            _isLoadingComboBoxes = false;
            await LoadDataAsync();
            SetupBindings(); // Bindings for main product data
            _isLoading = false;
            if (productBindingSource.Count > 0 && productBindingSource.Position < 0)
            {
                productBindingSource.MoveFirst();
            }
            UpdateButtonStates();
            UpdateNavigationState();
        }

        private async Task LoadComboBoxesAsync()
        {
            try
            {
                var categories = await _productService.GetCategoriesForDropdownAsync();
                var suppliers = await _productService.GetSuppliersForDropdownAsync();

                // Add placeholder for "None" or "Select"
                categories.Insert(0, new Category { CategoryID = 0, CategoryName = "(Select Category)" });
                suppliers.Insert(0, new Supplier { SupplierID = 0, SupplierName = "(Select Supplier)" });
                
                categoryBindingSource.DataSource = categories; // Use the dedicated BindingSource
                supplierBindingSource.DataSource = suppliers;   // Use the dedicated BindingSource

                // cmbCategory.DataSource already set via designer to categoryBindingSource
                // cmbSupplier.DataSource already set via designer to supplierBindingSource

                if (cmbCategory.Items.Count > 0) cmbCategory.SelectedIndex = 0;
                if (cmbSupplier.Items.Count > 0) cmbSupplier.SelectedIndex = 0;

            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading dropdown data: {ex.Message}", "Dropdown Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                cmbCategory.Enabled = false;
                cmbSupplier.Enabled = false;
            }
        }
        
        private async Task LoadDataAsync(string? searchTerm = null)
        {
            ToggleControls(false, true);
            lblStatus.Text = "Loading products...";
            try
            {
                List<Product> products;
                if (string.IsNullOrWhiteSpace(searchTerm))
                {
                    products = await _productService.GetAllProductsAsync();
                }
                else
                {
                    products = await _productService.SearchProductsAsync(searchTerm);
                }
                
                var currentId = (productBindingSource.Current as Product)?.ProductID;

                productBindingSource.DataSource = products;
                productBindingSource.ResetBindings(false);

                if (products.Count == 0)
                {
                    lblStatus.Text = string.IsNullOrWhiteSpace(searchTerm) ? "No products found. Click 'New' to add one." : $"No products matching '{searchTerm}'.";
                    ClearForm();
                    SetupBindings(); 
                }
                else
                {
                    lblStatus.Text = string.IsNullOrWhiteSpace(searchTerm) ? $"Displaying {products.Count} products." : $"Found {products.Count} matching '{searchTerm}'.";
                    if (currentId.HasValue)
                    {
                        SelectProductById(currentId.Value, false);
                    }
                    if (productBindingSource.Position < 0 && products.Count > 0)
                    {
                        productBindingSource.MoveFirst();
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading products: {ex.Message}", "Loading Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Error loading data.";
            }
            finally
            {
                 if (!_isLoading)
                {
                    UpdateButtonStates();
                    UpdateNavigationState();
                }
                ToggleControls(true, true);
            }
        }

        private void SetupBindings()
        {
            txtProductID.DataBindings.Clear();
            txtProductName.DataBindings.Clear();
            txtDescription.DataBindings.Clear();
            cmbCategory.DataBindings.Clear(); // For Product.CategoryID
            cmbSupplier.DataBindings.Clear(); // For Product.SupplierID
            txtPurchasePrice.DataBindings.Clear();
            txtSellingPrice.DataBindings.Clear();
            txtStockQuantity.DataBindings.Clear();

            txtProductID.DataBindings.Add("Text", productBindingSource, "ProductID", true, DataSourceUpdateMode.Never);
            txtProductName.DataBindings.Add("Text", productBindingSource, "ProductName", false, DataSourceUpdateMode.OnValidation);
            txtDescription.DataBindings.Add("Text", productBindingSource, "Description", true, DataSourceUpdateMode.OnValidation, string.Empty, "");
            
            // Bind the SelectedValue of ComboBoxes to the Product's foreign key properties
            cmbCategory.DataBindings.Add("SelectedValue", productBindingSource, "CategoryID", true, DataSourceUpdateMode.OnValidation, DBNull.Value);
            cmbSupplier.DataBindings.Add("SelectedValue", productBindingSource, "SupplierID", true, DataSourceUpdateMode.OnValidation, DBNull.Value);

            txtPurchasePrice.DataBindings.Add("Text", productBindingSource, "PurchasePrice", true, DataSourceUpdateMode.OnValidation, DBNull.Value, "N2");
            txtSellingPrice.DataBindings.Add("Text", productBindingSource, "SellingPrice", true, DataSourceUpdateMode.OnValidation, DBNull.Value, "N2");
            txtStockQuantity.DataBindings.Add("Text", productBindingSource, "StockQuantity", true, DataSourceUpdateMode.OnValidation, 0);
        }

        private void ClearForm()
        {
            productBindingSource.SuspendBinding();
            txtProductID.Clear();
            txtProductName.Clear();
            txtDescription.Clear();
            if (cmbCategory.Items.Count > 0) cmbCategory.SelectedIndex = 0;
            if (cmbSupplier.Items.Count > 0) cmbSupplier.SelectedIndex = 0;
            txtPurchasePrice.Clear();
            txtSellingPrice.Clear();
            txtStockQuantity.Text = "0";
            productBindingSource.ResumeBinding();
        }

        private void ToggleControls(bool enabled, bool keepToolbarEnabled = false)
        {
            groupBoxDetails.Enabled = enabled;
            if (!keepToolbarEnabled) toolStrip1.Enabled = enabled;
            else toolStrip1.Enabled = true;
            this.Cursor = enabled ? Cursors.Default : Cursors.WaitCursor;
        }
        
        private void UpdateButtonStates()
        {
            if (_isLoading) return;
            bool hasItems = productBindingSource.Count > 0;
            bool isItemSelected = productBindingSource.Current != null;

            tsbSave.Enabled = _isNew || (isItemSelected && !string.IsNullOrWhiteSpace(txtProductName.Text));
            tsbDelete.Enabled = isItemSelected && !_isNew;
            tsbFirst.Enabled = isItemSelected && !_isNew && productBindingSource.Position > 0;
            tsbPrevious.Enabled = isItemSelected && !_isNew && productBindingSource.Position > 0;
            tsbNext.Enabled = isItemSelected && !_isNew && productBindingSource.Position < productBindingSource.Count - 1;
            tsbLast.Enabled = isItemSelected && !_isNew && productBindingSource.Position < productBindingSource.Count - 1;
            tsbNew.Enabled = toolStrip1.Enabled;
            txtSearch.Enabled = toolStrip1.Enabled;
            tsbSearch.Enabled = toolStrip1.Enabled;
        }

        private void UpdateNavigationState()
        {
             if (_isLoading) return;
            bool hasItems = productBindingSource.Count > 0;
            bool isItemSelected = productBindingSource.Current != null;

            if (_isNew)
            {
                lblStatus.Text = "Adding new product...";
                groupBoxDetails.Enabled = true;
            }
            else if (isItemSelected)
            {
                lblStatus.Text = $"Record {productBindingSource.Position + 1} of {productBindingSource.Count}";
                 groupBoxDetails.Enabled = true;
            }
            else
            {
                lblStatus.Text = hasItems ? "No product selected." : (string.IsNullOrWhiteSpace(txtSearch.Text) ? "No products found." : $"No products matching '{txtSearch.Text}'.");
                groupBoxDetails.Enabled = false;
                if (!hasItems) ClearForm();
            }
            UpdateButtonStates();
        }

        private void tsbNew_Click(object sender, EventArgs e)
        {
            _isNew = true;
            productBindingSource.SuspendBinding();
            ClearForm();
            txtProductName.Focus();
            UpdateNavigationState();
        }

        private async void tsbSave_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtProductName.Text))
            {
                MessageBox.Show("Product Name cannot be empty.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                txtProductName.Focus(); return;
            }
            if (!decimal.TryParse(txtSellingPrice.Text, NumberStyles.Any, CultureInfo.CurrentCulture, out decimal sellingPrice) || sellingPrice < 0)
            {
                MessageBox.Show("Selling Price must be a valid non-negative number.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                txtSellingPrice.Focus(); return;
            }
            if (!int.TryParse(txtStockQuantity.Text, out int stockQuantity) || stockQuantity < 0)
            {
                MessageBox.Show("Stock Quantity must be a valid non-negative integer.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                txtStockQuantity.Focus(); return;
            }
            decimal? purchasePrice = null;
            if (!string.IsNullOrWhiteSpace(txtPurchasePrice.Text))
            {
                if (!decimal.TryParse(txtPurchasePrice.Text, NumberStyles.Any, CultureInfo.CurrentCulture, out decimal pp) || pp < 0)
                {
                    MessageBox.Show("Purchase Price must be valid non-negative or empty.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    txtPurchasePrice.Focus(); return;
                }
                purchasePrice = pp;
            }

             if (!_isNew && productBindingSource.Current != null)
            {
                productBindingSource.EndEdit();
            }

            ToggleControls(false);
            lblStatus.Text = "Saving...";

            try
            {
                bool success = false;
                Product? productToSave = null;
                bool wasNewItemInitially = _isNew;

                int? categoryId = (cmbCategory.SelectedValue != null && (int)cmbCategory.SelectedValue != 0) ? (int)cmbCategory.SelectedValue : (int?)null;
                int? supplierId = (cmbSupplier.SelectedValue != null && (int)cmbSupplier.SelectedValue != 0) ? (int)cmbSupplier.SelectedValue : (int?)null;
                
                if (_isNew)
                {
                    productToSave = new Product
                    {
                        ProductName = txtProductName.Text.Trim(),
                        Description = string.IsNullOrWhiteSpace(txtDescription.Text) ? null : txtDescription.Text.Trim(),
                        CategoryID = categoryId,
                        SupplierID = supplierId,
                        PurchasePrice = purchasePrice,
                        SellingPrice = sellingPrice,
                        StockQuantity = stockQuantity
                    };
                    success = await _productService.AddProductAsync(productToSave);
                    if (success) lblStatus.Text = "Product added successfully.";
                }
                else
                {
                    if (productBindingSource.Current is Product currentProduct)
                    {
                        currentProduct.ProductName = txtProductName.Text.Trim();
                        currentProduct.Description = string.IsNullOrWhiteSpace(txtDescription.Text) ? null : txtDescription.Text.Trim();
                        currentProduct.CategoryID = categoryId;
                        currentProduct.SupplierID = supplierId;
                        currentProduct.PurchasePrice = purchasePrice;
                        currentProduct.SellingPrice = sellingPrice;
                        currentProduct.StockQuantity = stockQuantity;
                        productToSave = currentProduct;
                        success = await _productService.UpdateProductAsync(currentProduct);
                        if (success) lblStatus.Text = "Product updated successfully.";
                    }
                     else
                    {
                         MessageBox.Show("No product selected to update.", "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                         lblStatus.Text = "No product selected.";
                    }
                }

                if (success)
                {
                    _isNew = false;
                    int savedItemId = productToSave?.ProductID ?? -1;
                    string? currentSearchTerm = wasNewItemInitially ? null : txtSearch.Text;
                    if (wasNewItemInitially) txtSearch.Clear();
                    
                    await LoadDataAsync(currentSearchTerm);
                    
                    if (savedItemId > 0) SelectProductById(savedItemId);
                    else if(productBindingSource.Count > 0) productBindingSource.MoveFirst();
                }
            }
            catch (DbUpdateConcurrencyException)
            {
                MessageBox.Show("Record modified. Reload and try again.", "Concurrency Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                lblStatus.Text = "Save failed due to concurrency.";
                await LoadDataAsync(txtSearch.Text);
            }
            catch (DbUpdateException dbEx)
            {
                 string errorMessage = $"Database error: {dbEx.InnerException?.Message ?? dbEx.Message}.";
                 if (dbEx.InnerException?.Message.Contains("UNIQUE KEY constraint") == true || 
                    dbEx.InnerException?.Message.Contains("duplicate key value violates unique constraint") == true)
                {
                    errorMessage += "\nA product with the same name might already exist if it's unique.";
                }
                MessageBox.Show(errorMessage, "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Database save error.";
            }
            catch (Exception ex)
            {
                MessageBox.Show($"An error occurred: {ex.Message}", "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Save error.";
            }
            finally
            {
                if (!success) { 
                     ToggleControls(true);
                     UpdateButtonStates();
                     UpdateNavigationState();
                }
            }
        }

        private async void tsbDelete_Click(object sender, EventArgs e)
        {
            if (_isNew) {
                MessageBox.Show("Cannot delete an unsaved new product.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }
            if (productBindingSource.Current is Product currentProduct)
            {
                var confirmResult = MessageBox.Show($"Delete product '{currentProduct.ProductName}' (ID: {currentProduct.ProductID})?", "Confirm Delete", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                if (confirmResult == DialogResult.Yes)
                {
                    ToggleControls(false);
                    lblStatus.Text = "Deleting...";
                    try
                    {
                        bool success = await _productService.DeleteProductAsync(currentProduct.ProductID);
                        if (success) lblStatus.Text = "Product deleted.";
                        await LoadDataAsync(txtSearch.Text.Trim());
                    }
                    catch (DbUpdateException dbEx)
                    {
                        MessageBox.Show($"Database error: {dbEx.InnerException?.Message ?? dbEx.Message}.\nProduct might be in an order.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        lblStatus.Text = "Database delete error.";
                         await LoadDataAsync(txtSearch.Text.Trim());
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"An error occurred: {ex.Message}", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        lblStatus.Text = "Delete error.";
                         await LoadDataAsync(txtSearch.Text.Trim());
                    }
                }
            }
            else
            {
                MessageBox.Show("No product selected.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private async void PerformSearch()
        {
            _isNew = false; productBindingSource.ResumeBinding();
            await LoadDataAsync(txtSearch.Text.Trim());
        }
        private void tsbSearch_Click(object sender, EventArgs e) => PerformSearch();
        private void txtSearch_KeyDown(object sender, KeyEventArgs e) { if (e.KeyCode == Keys.Enter) { PerformSearch(); e.SuppressKeyPress = true; } }
        private void tsbFirst_Click(object sender, EventArgs e) { if (_isNew) _isNew = false; productBindingSource.ResumeBinding(); productBindingSource.MoveFirst(); }
        private void tsbPrevious_Click(object sender, EventArgs e) { if (_isNew) _isNew = false; productBindingSource.ResumeBinding(); productBindingSource.MovePrevious(); }
        private void tsbNext_Click(object sender, EventArgs e) { if (_isNew) _isNew = false; productBindingSource.ResumeBinding(); productBindingSource.MoveNext(); }
        private void tsbLast_Click(object sender, EventArgs e) { if (_isNew) _isNew = false; productBindingSource.ResumeBinding(); productBindingSource.MoveLast(); }

        private void productBindingSource_CurrentChanged(object sender, EventArgs e)
        {
            if (_isLoading || _isNew || _isLoadingComboBoxes) return;
            if (productBindingSource.Current == null) ClearForm();
            UpdateButtonStates();
            UpdateNavigationState();
        }

        private void SelectProductById(int productId, bool triggerCurrentChanged = true)
        {
            if (productId <= 0) return;
            if (productBindingSource.DataSource is List<Product> products)
            {
                int index = products.FindIndex(p => p.ProductID == productId);
                if (index != -1)
                {
                     if(!triggerCurrentChanged)
                    {
                        this.productBindingSource.CurrentChanged -= productBindingSource_CurrentChanged;
                        productBindingSource.Position = index;
                        this.productBindingSource.CurrentChanged += productBindingSource_CurrentChanged;

                        if(productBindingSource.Current is Product prod)
                        {
                             txtProductID.Text = prod.ProductID.ToString();
                             txtProductName.Text = prod.ProductName;
                             txtDescription.Text = prod.Description;
                             cmbCategory.SelectedValue = prod.CategoryID ?? 0;
                             cmbSupplier.SelectedValue = prod.SupplierID ?? 0;
                             txtPurchasePrice.Text = prod.PurchasePrice?.ToString("N2") ?? "";
                             txtSellingPrice.Text = prod.SellingPrice.ToString("N2");
                             txtStockQuantity.Text = prod.StockQuantity.ToString();
                        }
                    }
                    else
                    {
                        productBindingSource.Position = index;
                    }
                }
            }
        }
    }
}
```

---
**File 7: `frmCustomers.Designer.cs`**
---
```csharp
using System;
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;
using Store.Data.Models; 

namespace Store.Forms
{
    partial class frmCustomers
    {
        private System.ComponentModel.IContainer components = null;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        private void InitializeComponent()
        {
            components = new Container();
            ComponentResourceManager resources = new ComponentResourceManager(typeof(frmCustomers));
            toolStrip1 = new ToolStrip();
            tsbNew = new ToolStripButton();
            tsbSave = new ToolStripButton();
            tsbDelete = new ToolStripButton();
            toolStripSeparator1 = new ToolStripSeparator();
            tsbFirst = new ToolStripButton();
            tsbPrevious = new ToolStripButton();
            tsbNext = new ToolStripButton();
            tsbLast = new ToolStripButton();
            toolStripSeparator2 = new ToolStripSeparator();
            txtSearch = new ToolStripTextBox();
            tsbSearch = new ToolStripButton();
            statusStrip1 = new StatusStrip();
            lblStatus = new ToolStripStatusLabel();
            customerBindingSource = new BindingSource(components);
            groupBoxDetails = new GroupBox();
            tableLayoutPanelDetails = new TableLayoutPanel();
            lblCustomerID = new Label();
            txtCustomerID = new TextBox();
            lblFirstName = new Label();
            txtFirstName = new TextBox();
            lblLastName = new Label();
            txtLastName = new TextBox();
            lblPhoneNumber = new Label();
            txtPhoneNumber = new TextBox();
            lblEmail = new Label();
            txtEmail = new TextBox();
            lblAddress = new Label();
            txtAddress = new TextBox();
            toolStrip1.SuspendLayout();
            statusStrip1.SuspendLayout();
            ((ISupportInitialize)customerBindingSource).BeginInit();
            groupBoxDetails.SuspendLayout();
            tableLayoutPanelDetails.SuspendLayout();
            SuspendLayout();
            //
            // toolStrip1
            //
            toolStrip1.Font = new Font("Segoe UI", 10F);
            toolStrip1.GripStyle = ToolStripGripStyle.Hidden;
            toolStrip1.ImageScalingSize = new Size(24, 24);
            toolStrip1.Items.AddRange(new ToolStripItem[] { tsbNew, tsbSave, tsbDelete, toolStripSeparator1, tsbFirst, tsbPrevious, tsbNext, tsbLast, toolStripSeparator2, txtSearch, tsbSearch });
            toolStrip1.Location = new Point(0, 0);
            toolStrip1.Name = "toolStrip1";
            toolStrip1.Padding = new Padding(8, 5, 8, 5);
            toolStrip1.RenderMode = ToolStripRenderMode.System;
            toolStrip1.Size = new Size(1118, 46);
            toolStrip1.TabIndex = 0;
            toolStrip1.Text = "toolStrip1";
            toolStrip1.BackColor = Color.FromArgb(240, 240, 240);
            //
            // tsbNew
            //
            tsbNew.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbNew.Image = (Image)resources.GetObject("tsbNew.Image");
            tsbNew.ImageTransparentColor = Color.Magenta;
            tsbNew.Margin = new Padding(4);
            tsbNew.Name = "tsbNew";
            tsbNew.Size = new Size(158, 28); 
            tsbNew.Text = "New Customer";
            tsbNew.ToolTipText = "Add New Customer (Ctrl+N)";
            tsbNew.ForeColor = Color.FromArgb(64, 64, 64);
            tsbNew.Click += tsbNew_Click;
            //
            // tsbSave
            //
            tsbSave.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbSave.Image = (Image)resources.GetObject("tsbSave.Image");
            tsbSave.ImageTransparentColor = Color.Magenta;
            tsbSave.Margin = new Padding(4);
            tsbSave.Name = "tsbSave";
            tsbSave.Size = new Size(144, 28);
            tsbSave.Text = "Save Changes";
            tsbSave.ToolTipText = "Save Changes (Ctrl+S)";
            tsbSave.ForeColor = Color.FromArgb(64, 64, 64);
            tsbSave.Click += tsbSave_Click;
            //
            // tsbDelete
            //
            tsbDelete.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbDelete.Image = (Image)resources.GetObject("tsbDelete.Image");
            tsbDelete.ImageTransparentColor = Color.Magenta;
            tsbDelete.Margin = new Padding(4);
            tsbDelete.Name = "tsbDelete";
            tsbDelete.Size = new Size(173, 28); 
            tsbDelete.Text = "Delete Customer";
            tsbDelete.ToolTipText = "Delete Selected Customer (Del)";
            tsbDelete.ForeColor = Color.FromArgb(64, 64, 64);
            tsbDelete.Click += tsbDelete_Click;
            //
            // toolStripSeparator1
            //
            toolStripSeparator1.Margin = new Padding(10, 0, 10, 0);
            toolStripSeparator1.Name = "toolStripSeparator1";
            toolStripSeparator1.Size = new Size(6, 36);
            //
            // tsbFirst
            //
            tsbFirst.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbFirst.Image = (Image)resources.GetObject("tsbFirst.Image");
            tsbFirst.ImageTransparentColor = Color.Magenta;
            tsbFirst.Margin = new Padding(4);
            tsbFirst.Name = "tsbFirst";
            tsbFirst.Size = new Size(127, 28);
            tsbFirst.Text = "First Record";
            tsbFirst.ToolTipText = "Go to First Record (Ctrl+Home)";
            tsbFirst.ForeColor = Color.FromArgb(64, 64, 64);
            tsbFirst.Click += tsbFirst_Click;
            //
            // tsbPrevious
            //
            tsbPrevious.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbPrevious.Image = (Image)resources.GetObject("tsbPrevious.Image");
            tsbPrevious.ImageTransparentColor = Color.Magenta;
            tsbPrevious.Margin = new Padding(4);
            tsbPrevious.Name = "tsbPrevious";
            tsbPrevious.Size = new Size(160, 28);
            tsbPrevious.Text = "Previous Record";
            tsbPrevious.ToolTipText = "Go to Previous Record (Ctrl+Left)";
            tsbPrevious.ForeColor = Color.FromArgb(64, 64, 64);
            tsbPrevious.Click += tsbPrevious_Click;
            //
            // tsbNext
            //
            tsbNext.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbNext.Image = (Image)resources.GetObject("tsbNext.Image");
            tsbNext.ImageTransparentColor = Color.Magenta;
            tsbNext.Margin = new Padding(4);
            tsbNext.Name = "tsbNext";
            tsbNext.Size = new Size(132, 28);
            tsbNext.Text = "Next Record";
            tsbNext.ToolTipText = "Go to Next Record (Ctrl+Right)";
            tsbNext.ForeColor = Color.FromArgb(64, 64, 64);
            tsbNext.Click += tsbNext_Click;
            //
            // tsbLast
            //
            tsbLast.DisplayStyle = ToolStripItemDisplayStyle.Text;
            tsbLast.ImageTransparentColor = Color.Magenta;
            tsbLast.Margin = new Padding(4);
            tsbLast.Name = "tsbLast";
            tsbLast.Size = new Size(102, 28);
            tsbLast.Text = "Last Record";
            tsbLast.ToolTipText = "Go to Last Record (Ctrl+End)";
            tsbLast.ForeColor = Color.FromArgb(64, 64, 64);
            tsbLast.Click += tsbLast_Click;
            //
            // toolStripSeparator2
            //
            toolStripSeparator2.Margin = new Padding(10, 0, 10, 0);
            toolStripSeparator2.Name = "toolStripSeparator2";
            toolStripSeparator2.Size = new Size(6, 36);
            //
            // txtSearch
            //
            txtSearch.Alignment = ToolStripItemAlignment.Right;
            txtSearch.BackColor = Color.White;
            txtSearch.BorderStyle = BorderStyle.FixedSingle;
            txtSearch.Font = new Font("Segoe UI", 10F);
            txtSearch.ForeColor = Color.FromArgb(64, 64, 64);
            txtSearch.Margin = new Padding(1, 2, 6, 2);
            txtSearch.Name = "txtSearch";
            txtSearch.Size = new Size(200, 27); 
            txtSearch.ToolTipText = "Enter search term and press Enter or click Search";
            txtSearch.KeyDown += txtSearch_KeyDown;
            //
            // tsbSearch
            //
            tsbSearch.Alignment = ToolStripItemAlignment.Right;
            tsbSearch.DisplayStyle = ToolStripItemDisplayStyle.Image;
            tsbSearch.Image = (Image)resources.GetObject("tsbSearch.Image");
            tsbSearch.ImageTransparentColor = Color.Magenta;
            tsbSearch.Margin = new Padding(1, 2, 1, 2);
            tsbSearch.Name = "tsbSearch";
            tsbSearch.Size = new Size(28, 28); 
            tsbSearch.Text = "Search";
            tsbSearch.ToolTipText = "Search Customers (Enter)";
            tsbSearch.Click += tsbSearch_Click;
            //
            // statusStrip1
            //
            statusStrip1.ImageScalingSize = new Size(20, 20);
            statusStrip1.Items.AddRange(new ToolStripItem[] { lblStatus });
            statusStrip1.Location = new Point(0, 488);
            statusStrip1.Name = "statusStrip1";
            statusStrip1.Padding = new Padding(1, 0, 16, 0);
            statusStrip1.Size = new Size(1118, 22); 
            statusStrip1.TabIndex = 2;
            statusStrip1.BackColor = Color.FromArgb(248, 248, 248);
            statusStrip1.Text = "statusStrip1";
            //
            // lblStatus
            //
            lblStatus.Name = "lblStatus";
            lblStatus.Size = new Size(1101, 16); 
            lblStatus.Spring = true;
            lblStatus.TextAlign = ContentAlignment.MiddleLeft;
            lblStatus.Font = new Font("Segoe UI", 9F);
            lblStatus.ForeColor = Color.FromArgb(80, 80, 80);
            //
            // customerBindingSource
            //
            customerBindingSource.DataSource = typeof(Customer);
            customerBindingSource.CurrentChanged += customerBindingSource_CurrentChanged;
            //
            // groupBoxDetails
            //
            groupBoxDetails.Controls.Add(tableLayoutPanelDetails);
            groupBoxDetails.Dock = DockStyle.Fill;
            groupBoxDetails.Location = new Point(0, 46);
            groupBoxDetails.Margin = new Padding(10);
            groupBoxDetails.Name = "groupBoxDetails";
            groupBoxDetails.Padding = new Padding(20);
            groupBoxDetails.Size = new Size(1118, 442);
            groupBoxDetails.TabIndex = 1;
            groupBoxDetails.TabStop = false;
            groupBoxDetails.Text = "Customer Details";
            groupBoxDetails.Font = new Font("Segoe UI Semibold", 10F, FontStyle.Bold);
            groupBoxDetails.ForeColor = Color.FromArgb(55, 55, 55);
            //
            // tableLayoutPanelDetails
            //
            tableLayoutPanelDetails.ColumnCount = 2;
            tableLayoutPanelDetails.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 150F));
            tableLayoutPanelDetails.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            tableLayoutPanelDetails.Controls.Add(lblCustomerID, 0, 0);
            tableLayoutPanelDetails.Controls.Add(txtCustomerID, 1, 0);
            tableLayoutPanelDetails.Controls.Add(lblFirstName, 0, 1);
            tableLayoutPanelDetails.Controls.Add(txtFirstName, 1, 1);
            tableLayoutPanelDetails.Controls.Add(lblLastName, 0, 2);
            tableLayoutPanelDetails.Controls.Add(txtLastName, 1, 2);
            tableLayoutPanelDetails.Controls.Add(lblPhoneNumber, 0, 3);
            tableLayoutPanelDetails.Controls.Add(txtPhoneNumber, 1, 3);
            tableLayoutPanelDetails.Controls.Add(lblEmail, 0, 4);
            tableLayoutPanelDetails.Controls.Add(txtEmail, 1, 4);
            tableLayoutPanelDetails.Controls.Add(lblAddress, 0, 5);
            tableLayoutPanelDetails.Controls.Add(txtAddress, 1, 5);
            tableLayoutPanelDetails.Dock = DockStyle.Fill;
            tableLayoutPanelDetails.Location = new Point(20, 43);
            tableLayoutPanelDetails.Margin = new Padding(0);
            tableLayoutPanelDetails.Name = "tableLayoutPanelDetails";
            tableLayoutPanelDetails.RowCount = 7;
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 80F)); // Address
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableLayoutPanelDetails.Size = new Size(1078, 379);
            tableLayoutPanelDetails.TabIndex = 0;
            //
            // lblCustomerID 
            //
            lblCustomerID.Anchor = AnchorStyles.Left; lblCustomerID.AutoSize = true;
            lblCustomerID.Location = new Point(3, 11); lblCustomerID.Name = "lblCustomerID";
            lblCustomerID.Size = new Size(115, 23); 
            lblCustomerID.TabIndex = 0; lblCustomerID.Text = "Customer ID:";
            lblCustomerID.Font = new Font("Segoe UI", 10F); 
            lblCustomerID.ForeColor = Color.FromArgb(80, 80, 80);

            txtCustomerID.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            txtCustomerID.Location = new Point(153, 7); txtCustomerID.Margin = new Padding(3, 4, 10, 4);
            txtCustomerID.Name = "txtCustomerID"; txtCustomerID.ReadOnly = true;
            txtCustomerID.Size = new Size(915, 30); txtCustomerID.TabIndex = 99; // Non-focusable
            txtCustomerID.TabStop = false; txtCustomerID.Font = new Font("Segoe UI", 10F);
            txtCustomerID.ForeColor = Color.FromArgb(100, 100, 100);
            txtCustomerID.BackColor = Color.FromArgb(245, 245, 245); txtCustomerID.BorderStyle = BorderStyle.FixedSingle;
            //
            // lblFirstName 
            //
            lblFirstName.Anchor = AnchorStyles.Left; lblFirstName.AutoSize = true;
            lblFirstName.Location = new Point(3, 56); lblFirstName.Name = "lblFirstName";
            lblFirstName.Size = new Size(97, 23); lblFirstName.TabIndex = 2; lblFirstName.Text = "First Name:";
            lblFirstName.Font = new Font("Segoe UI", 10F); lblFirstName.ForeColor = Color.FromArgb(80, 80, 80);

            txtFirstName.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            txtFirstName.Location = new Point(153, 52); txtFirstName.Margin = new Padding(3, 4, 10, 4);
            txtFirstName.MaxLength = 50; txtFirstName.Name = "txtFirstName";
            txtFirstName.Size = new Size(915, 30); txtFirstName.TabIndex = 0;
            txtFirstName.Font = new Font("Segoe UI", 10F); txtFirstName.ForeColor = Color.FromArgb(50, 50, 50);
            txtFirstName.BorderStyle = BorderStyle.FixedSingle;
            //
            // lblLastName 
            //
            lblLastName.Anchor = AnchorStyles.Left; lblLastName.AutoSize = true;
            lblLastName.Location = new Point(3, 101); lblLastName.Name = "lblLastName";
            lblLastName.Size = new Size(95, 23); lblLastName.TabIndex = 4; lblLastName.Text = "Last Name:";
            lblLastName.Font = new Font("Segoe UI", 10F); lblLastName.ForeColor = Color.FromArgb(80, 80, 80);

            txtLastName.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            txtLastName.Location = new Point(153, 97); txtLastName.Margin = new Padding(3, 4, 10, 4);
            txtLastName.MaxLength = 50; txtLastName.Name = "txtLastName";
            txtLastName.Size = new Size(915, 30); txtLastName.TabIndex = 1;
            txtLastName.Font = new Font("Segoe UI", 10F); txtLastName.ForeColor = Color.FromArgb(50, 50, 50);
            txtLastName.BorderStyle = BorderStyle.FixedSingle;
            //
            // lblPhoneNumber 
            //
            lblPhoneNumber.Anchor = AnchorStyles.Left; lblPhoneNumber.AutoSize = true;
            lblPhoneNumber.Location = new Point(3, 146); lblPhoneNumber.Name = "lblPhoneNumber";
            lblPhoneNumber.Size = new Size(128, 23); lblPhoneNumber.TabIndex = 6; lblPhoneNumber.Text = "Phone Number:";
            lblPhoneNumber.Font = new Font("Segoe UI", 10F); lblPhoneNumber.ForeColor = Color.FromArgb(80, 80, 80);

            txtPhoneNumber.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            txtPhoneNumber.Location = new Point(153, 142); txtPhoneNumber.Margin = new Padding(3, 4, 10, 4);
            txtPhoneNumber.MaxLength = 20; txtPhoneNumber.Name = "txtPhoneNumber";
            txtPhoneNumber.Size = new Size(915, 30); txtPhoneNumber.TabIndex = 2;
            txtPhoneNumber.Font = new Font("Segoe UI", 10F); txtPhoneNumber.ForeColor = Color.FromArgb(50, 50, 50);
            txtPhoneNumber.BorderStyle = BorderStyle.FixedSingle;
            //
            // lblEmail 
            //
            lblEmail.Anchor = AnchorStyles.Left; lblEmail.AutoSize = true;
            lblEmail.Location = new Point(3, 191); lblEmail.Name = "lblEmail";
            lblEmail.Size = new Size(55, 23); lblEmail.TabIndex = 8; lblEmail.Text = "Email:";
            lblEmail.Font = new Font("Segoe UI", 10F); lblEmail.ForeColor = Color.FromArgb(80, 80, 80);

            txtEmail.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            txtEmail.Location = new Point(153, 187); txtEmail.Margin = new Padding(3, 4, 10, 4);
            txtEmail.MaxLength = 100; txtEmail.Name = "txtEmail";
            txtEmail.Size = new Size(915, 30); txtEmail.TabIndex = 3;
            txtEmail.Font = new Font("Segoe UI", 10F); txtEmail.ForeColor = Color.FromArgb(50, 50, 50);
            txtEmail.BorderStyle = BorderStyle.FixedSingle;
            //
            // lblAddress 
            //
            lblAddress.Anchor = AnchorStyles.Left | AnchorStyles.Top; lblAddress.AutoSize = true;
            lblAddress.Location = new Point(3, 228); lblAddress.Margin = new Padding(3, 8, 3, 0);
            lblAddress.Name = "lblAddress"; lblAddress.Size = new Size(74, 23);
            lblAddress.TabIndex = 10; lblAddress.Text = "Address:";
            lblAddress.Font = new Font("Segoe UI", 10F); lblAddress.ForeColor = Color.FromArgb(80, 80, 80);

            txtAddress.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
            txtAddress.Location = new Point(153, 224); txtAddress.Margin = new Padding(3, 4, 10, 4);
            txtAddress.MaxLength = 255; txtAddress.Multiline = true; txtAddress.Name = "txtAddress";
            txtAddress.ScrollBars = ScrollBars.Vertical; txtAddress.Size = new Size(915, 72);
            txtAddress.TabIndex = 4; txtAddress.Font = new Font("Segoe UI", 10F);
            txtAddress.ForeColor = Color.FromArgb(50, 50, 50); txtAddress.BorderStyle = BorderStyle.FixedSingle;
            //
            // frmCustomers
            //
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.White;
            ClientSize = new Size(1118, 510); 
            Controls.Add(groupBoxDetails);
            Controls.Add(statusStrip1);
            Controls.Add(toolStrip1);
            MinimumSize = new Size(650, 500); // Adjusted min height
            Name = "frmCustomers";
            Text = "Manage Customers";
            Font = new Font("Segoe UI", 9F);
            ForeColor = Color.FromArgb(64, 64, 64);
            Load += frmCustomers_Load;
            toolStrip1.ResumeLayout(false);
            toolStrip1.PerformLayout();
            statusStrip1.ResumeLayout(false);
            statusStrip1.PerformLayout();
            ((ISupportInitialize)customerBindingSource).EndInit();
            groupBoxDetails.ResumeLayout(false);
            tableLayoutPanelDetails.ResumeLayout(false);
            tableLayoutPanelDetails.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private ToolStrip toolStrip1;
        private ToolStripButton tsbNew;
        private ToolStripButton tsbSave;
        private ToolStripButton tsbDelete;
        private ToolStripSeparator toolStripSeparator1;
        private ToolStripButton tsbFirst;
        private ToolStripButton tsbPrevious;
        private ToolStripButton tsbNext;
        private ToolStripButton tsbLast;
        private ToolStripSeparator toolStripSeparator2;
        private ToolStripTextBox txtSearch;
        private ToolStripButton tsbSearch;
        private StatusStrip statusStrip1;
        private ToolStripStatusLabel lblStatus;
        private BindingSource customerBindingSource;
        private GroupBox groupBoxDetails;
        private TableLayoutPanel tableLayoutPanelDetails;
        private Label lblCustomerID;
        private TextBox txtCustomerID;
        private Label lblFirstName;
        private TextBox txtFirstName;
        private Label lblLastName;
        private TextBox txtLastName;
        private Label lblPhoneNumber;
        private TextBox txtPhoneNumber;
        private Label lblEmail;
        private TextBox txtEmail;
        private Label lblAddress;
        private TextBox txtAddress;
    }
}
```

---
**File 8: `frmCustomers.cs`**
---
```csharp
using Microsoft.EntityFrameworkCore;
using Store.Data.Models;
using Store.Services;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Store.Forms
{
    public partial class frmCustomers : Form
    {
        private readonly CustomerService _customerService;
        private bool _isNew = false;
        private bool _isLoading = false;

        public frmCustomers(CustomerService customerService)
        {
            InitializeComponent();
            _customerService = customerService;
        }

        private async void frmCustomers_Load(object sender, EventArgs e)
        {
            _isLoading = true;
            await LoadDataAsync();
            SetupBindings();
            _isLoading = false;
             if (customerBindingSource.Count > 0 && customerBindingSource.Position < 0)
            {
                customerBindingSource.MoveFirst();
            }
            UpdateButtonStates();
            UpdateNavigationState();
        }

        private async Task LoadDataAsync(string? searchTerm = null)
        {
            ToggleControls(false, true);
            lblStatus.Text = "Loading customers...";
            try
            {
                List<Customer> customers;
                if (string.IsNullOrWhiteSpace(searchTerm))
                {
                    customers = await _customerService.GetAllCustomersAsync();
                }
                else
                {
                    customers = await _customerService.SearchCustomersAsync(searchTerm);
                }

                var currentId = (customerBindingSource.Current as Customer)?.CustomerID;
                
                customerBindingSource.DataSource = customers;
                customerBindingSource.ResetBindings(false);

                if (customers.Count == 0)
                {
                     lblStatus.Text = string.IsNullOrWhiteSpace(searchTerm) ? "No customers found. Click 'New' to add one." : $"No customers matching '{searchTerm}'.";
                    ClearForm();
                    SetupBindings();
                }
                else
                {
                    lblStatus.Text = string.IsNullOrWhiteSpace(searchTerm) ? $"Displaying {customers.Count} customers." : $"Found {customers.Count} matching '{searchTerm}'.";
                    if(currentId.HasValue)
                    {
                        SelectCustomerById(currentId.Value, false);
                    }
                     if (customerBindingSource.Position < 0 && customers.Count > 0)
                    {
                        customerBindingSource.MoveFirst();
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading customers: {ex.Message}", "Loading Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Error loading data.";
            }
            finally
            {
                if (!_isLoading)
                {
                    UpdateButtonStates();
                    UpdateNavigationState();
                }
                ToggleControls(true, true);
            }
        }

        private void SetupBindings()
        {
            txtCustomerID.DataBindings.Clear();
            txtFirstName.DataBindings.Clear();
            txtLastName.DataBindings.Clear();
            txtPhoneNumber.DataBindings.Clear();
            txtEmail.DataBindings.Clear();
            txtAddress.DataBindings.Clear();

            txtCustomerID.DataBindings.Add("Text", customerBindingSource, "CustomerID", true, DataSourceUpdateMode.Never);
            txtFirstName.DataBindings.Add("Text", customerBindingSource, "FirstName", false, DataSourceUpdateMode.OnValidation);
            txtLastName.DataBindings.Add("Text", customerBindingSource, "LastName", false, DataSourceUpdateMode.OnValidation);
            txtPhoneNumber.DataBindings.Add("Text", customerBindingSource, "PhoneNumber", true, DataSourceUpdateMode.OnValidation, string.Empty, "");
            txtEmail.DataBindings.Add("Text", customerBindingSource, "Email", true, DataSourceUpdateMode.OnValidation, string.Empty, "");
            txtAddress.DataBindings.Add("Text", customerBindingSource, "Address", true, DataSourceUpdateMode.OnValidation, string.Empty, "");
        }

        private void ClearForm()
        {
            customerBindingSource.SuspendBinding();
            txtCustomerID.Clear();
            txtFirstName.Clear();
            txtLastName.Clear();
            txtPhoneNumber.Clear();
            txtEmail.Clear();
            txtAddress.Clear();
            customerBindingSource.ResumeBinding();
        }

        private void ToggleControls(bool enabled, bool keepToolbarEnabled = false)
        {
            groupBoxDetails.Enabled = enabled;
            if (!keepToolbarEnabled) toolStrip1.Enabled = enabled;
            else toolStrip1.Enabled = true;
            this.Cursor = enabled ? Cursors.Default : Cursors.WaitCursor;
        }

        private void UpdateButtonStates()
        {
            if (_isLoading) return;
            bool hasItems = customerBindingSource.Count > 0;
            bool isItemSelected = customerBindingSource.Current != null;

            tsbSave.Enabled = _isNew || (isItemSelected && (!string.IsNullOrWhiteSpace(txtFirstName.Text) || !string.IsNullOrWhiteSpace(txtLastName.Text)));
            tsbDelete.Enabled = isItemSelected && !_isNew;
            tsbFirst.Enabled = isItemSelected && !_isNew && customerBindingSource.Position > 0;
            tsbPrevious.Enabled = isItemSelected && !_isNew && customerBindingSource.Position > 0;
            tsbNext.Enabled = isItemSelected && !_isNew && customerBindingSource.Position < customerBindingSource.Count - 1;
            tsbLast.Enabled = isItemSelected && !_isNew && customerBindingSource.Position < customerBindingSource.Count - 1;
            tsbNew.Enabled = toolStrip1.Enabled;
            txtSearch.Enabled = toolStrip1.Enabled;
            tsbSearch.Enabled = toolStrip1.Enabled;
        }

        private void UpdateNavigationState()
        {
            if (_isLoading) return;
            bool hasItems = customerBindingSource.Count > 0;
            bool isItemSelected = customerBindingSource.Current != null;

            if (_isNew)
            {
                lblStatus.Text = "Adding new customer...";
                groupBoxDetails.Enabled = true;
            }
            else if (isItemSelected)
            {
                lblStatus.Text = $"Record {customerBindingSource.Position + 1} of {customerBindingSource.Count}";
                 groupBoxDetails.Enabled = true;
            }
            else
            {
                lblStatus.Text = hasItems ? "No customer selected." : (string.IsNullOrWhiteSpace(txtSearch.Text) ? "No customers found." : $"No customers matching '{txtSearch.Text}'.");
                groupBoxDetails.Enabled = false;
                if (!hasItems) ClearForm();
            }
            UpdateButtonStates();
        }

        private void tsbNew_Click(object sender, EventArgs e)
        {
            _isNew = true;
            customerBindingSource.SuspendBinding();
            ClearForm();
            txtFirstName.Focus();
            UpdateNavigationState();
        }

        private async void tsbSave_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtFirstName.Text) || string.IsNullOrWhiteSpace(txtLastName.Text))
            {
                MessageBox.Show("First Name and Last Name cannot be empty.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                txtFirstName.Focus(); return;
            }
             if (!string.IsNullOrWhiteSpace(txtEmail.Text) && !txtEmail.Text.Contains("@"))
            {
                MessageBox.Show("Please enter a valid email address or leave it empty.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                txtEmail.Focus();
                return;
            }

            if (!_isNew && customerBindingSource.Current != null)
            {
                customerBindingSource.EndEdit();
            }

            ToggleControls(false);
            lblStatus.Text = "Saving...";

            try
            {
                bool success = false;
                Customer? customerToSave = null;
                bool wasNewItemInitially = _isNew;

                if (_isNew)
                {
                    customerToSave = new Customer
                    {
                        FirstName = txtFirstName.Text.Trim(),
                        LastName = txtLastName.Text.Trim(),
                        PhoneNumber = string.IsNullOrWhiteSpace(txtPhoneNumber.Text) ? null : txtPhoneNumber.Text.Trim(),
                        Email = string.IsNullOrWhiteSpace(txtEmail.Text) ? null : txtEmail.Text.Trim(),
                        Address = string.IsNullOrWhiteSpace(txtAddress.Text) ? null : txtAddress.Text.Trim()
                    };
                    success = await _customerService.AddCustomerAsync(customerToSave);
                    if (success) lblStatus.Text = "Customer added successfully.";
                }
                else
                {
                    if (customerBindingSource.Current is Customer currentCustomer)
                    {
                        currentCustomer.FirstName = txtFirstName.Text.Trim();
                        currentCustomer.LastName = txtLastName.Text.Trim();
                        currentCustomer.PhoneNumber = string.IsNullOrWhiteSpace(txtPhoneNumber.Text) ? null : txtPhoneNumber.Text.Trim();
                        currentCustomer.Email = string.IsNullOrWhiteSpace(txtEmail.Text) ? null : txtEmail.Text.Trim();
                        currentCustomer.Address = string.IsNullOrWhiteSpace(txtAddress.Text) ? null : txtAddress.Text.Trim();
                        customerToSave = currentCustomer;
                        success = await _customerService.UpdateCustomerAsync(currentCustomer);
                        if (success) lblStatus.Text = "Customer updated successfully.";
                    }
                    else
                    {
                         MessageBox.Show("No customer selected to update.", "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                         lblStatus.Text = "No customer selected.";
                    }
                }

                if (success)
                {
                    _isNew = false;
                    int savedItemId = customerToSave?.CustomerID ?? -1;
                    string? currentSearchTerm = wasNewItemInitially ? null : txtSearch.Text;
                    if (wasNewItemInitially) txtSearch.Clear();
                    
                    await LoadDataAsync(currentSearchTerm);
                    
                    if (savedItemId > 0) SelectCustomerById(savedItemId);
                    else if(customerBindingSource.Count > 0) customerBindingSource.MoveFirst();
                }
            }
            catch (DbUpdateConcurrencyException)
            {
                MessageBox.Show("Record modified. Reload and try again.", "Concurrency Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                lblStatus.Text = "Save failed due to concurrency.";
                await LoadDataAsync(txtSearch.Text);
            }
            catch (DbUpdateException dbEx)
            {
                string errorMessage = $"Database error: {dbEx.InnerException?.Message ?? dbEx.Message}.";
                 if (dbEx.InnerException?.Message.Contains("UNIQUE KEY constraint") == true || 
                    dbEx.InnerException?.Message.Contains("duplicate key value violates unique constraint") == true) // For PostgreSQL
                {
                    errorMessage += "\nA customer with the same Phone Number or Email might already exist if they are unique.";
                }
                MessageBox.Show(errorMessage, "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Database save error.";
            }
            catch (Exception ex)
            {
                MessageBox.Show($"An error occurred: {ex.Message}", "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Save error.";
            }
            finally
            {
                if (!success) { 
                     ToggleControls(true);
                     UpdateButtonStates();
                     UpdateNavigationState();
                }
            }
        }

        private async void tsbDelete_Click(object sender, EventArgs e)
        {
            if (_isNew) {
                MessageBox.Show("Cannot delete an unsaved new customer.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }
            if (customerBindingSource.Current is Customer currentCustomer)
            {
                var confirmResult = MessageBox.Show($"Delete customer '{currentCustomer.FullName}' (ID: {currentCustomer.CustomerID})?", "Confirm Delete", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                if (confirmResult == DialogResult.Yes)
                {
                    ToggleControls(false);
                    lblStatus.Text = "Deleting...";
                    try
                    {
                        bool success = await _customerService.DeleteCustomerAsync(currentCustomer.CustomerID);
                        if (success) lblStatus.Text = "Customer deleted.";
                        await LoadDataAsync(txtSearch.Text.Trim());
                    }
                    catch (DbUpdateException dbEx)
                    {
                        MessageBox.Show($"Database error: {dbEx.InnerException?.Message ?? dbEx.Message}.\nCustomer might have related orders.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        lblStatus.Text = "Database delete error.";
                        await LoadDataAsync(txtSearch.Text.Trim());
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"An error occurred: {ex.Message}", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        lblStatus.Text = "Delete error.";
                        await LoadDataAsync(txtSearch.Text.Trim());
                    }
                }
            }
            else
            {
                MessageBox.Show("No customer selected.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private async void PerformSearch()
        {
            _isNew = false; customerBindingSource.ResumeBinding();
            await LoadDataAsync(txtSearch.Text.Trim());
        }
        private void tsbSearch_Click(object sender, EventArgs e) => PerformSearch();
        private void txtSearch_KeyDown(object sender, KeyEventArgs e) { if (e.KeyCode == Keys.Enter) { PerformSearch(); e.SuppressKeyPress = true; } }
        private void tsbFirst_Click(object sender, EventArgs e) { if (_isNew) _isNew = false; customerBindingSource.ResumeBinding(); customerBindingSource.MoveFirst(); }
        private void tsbPrevious_Click(object sender, EventArgs e) { if (_isNew) _isNew = false; customerBindingSource.ResumeBinding(); customerBindingSource.MovePrevious(); }
        private void tsbNext_Click(object sender, EventArgs e) { if (_isNew) _isNew = false; customerBindingSource.ResumeBinding(); customerBindingSource.MoveNext(); }
        private void tsbLast_Click(object sender, EventArgs e) { if (_isNew) _isNew = false; customerBindingSource.ResumeBinding(); customerBindingSource.MoveLast(); }

        private void customerBindingSource_CurrentChanged(object sender, EventArgs e)
        {
            if (_isLoading || _isNew) return;
            if (customerBindingSource.Current == null) ClearForm();
            UpdateButtonStates();
            UpdateNavigationState();
        }

        private void SelectCustomerById(int customerId, bool triggerCurrentChanged = true)
        {
            if (customerId <= 0) return;
            if (customerBindingSource.DataSource is List<Customer> customers)
            {
                int index = customers.FindIndex(c => c.CustomerID == customerId);
                if (index != -1)
                {
                     if(!triggerCurrentChanged)
                    {
                        this.customerBindingSource.CurrentChanged -= customerBindingSource_CurrentChanged;
                        customerBindingSource.Position = index;
                        this.customerBindingSource.CurrentChanged += customerBindingSource_CurrentChanged;
                        if(customerBindingSource.Current is Customer cust)
                        {
                            txtCustomerID.Text = cust.CustomerID.ToString();
                            txtFirstName.Text = cust.FirstName;
                            txtLastName.Text = cust.LastName;
                            txtPhoneNumber.Text = cust.PhoneNumber;
                            txtEmail.Text = cust.Email;
                            txtAddress.Text = cust.Address;
                        }
                    }
                    else
                    {
                        customerBindingSource.Position = index;
                    }
                }
            }
        }
    }
}
```

---
**File 9: `frmEmployees.Designer.cs`**
---
```csharp
using System;
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;
using Store.Data.Models;

namespace Store.Forms
{
    partial class frmEmployees
    {
        private System.ComponentModel.IContainer components = null;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null)) { components.Dispose(); }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code
        private void InitializeComponent()
        {
            components = new Container();
            ComponentResourceManager resources = new ComponentResourceManager(typeof(frmEmployees));
            toolStrip1 = new ToolStrip();
            tsbNew = new ToolStripButton();
            tsbSave = new ToolStripButton();
            tsbDelete = new ToolStripButton();
            toolStripSeparator1 = new ToolStripSeparator();
            tsbFirst = new ToolStripButton();
            tsbPrevious = new ToolStripButton();
            tsbNext = new ToolStripButton();
            tsbLast = new ToolStripButton();
            toolStripSeparator2 = new ToolStripSeparator();
            txtSearch = new ToolStripTextBox();
            tsbSearch = new ToolStripButton();
            statusStrip1 = new StatusStrip();
            lblStatus = new ToolStripStatusLabel();
            employeeBindingSource = new BindingSource(components);
            groupBoxDetails = new GroupBox();
            tableLayoutPanelDetails = new TableLayoutPanel();
            lblEmployeeID = new Label();
            txtEmployeeID = new TextBox();
            lblFirstName = new Label();
            txtFirstName = new TextBox();
            lblLastName = new Label();
            txtLastName = new TextBox();
            lblPosition = new Label();
            txtPosition = new TextBox();
            lblUsername = new Label();
            txtUsername = new TextBox();
            lblPassword = new Label();
            txtPassword = new TextBox();
            lblPasswordInfo = new Label();
            toolStrip1.SuspendLayout();
            statusStrip1.SuspendLayout();
            ((ISupportInitialize)employeeBindingSource).BeginInit();
            groupBoxDetails.SuspendLayout();
            tableLayoutPanelDetails.SuspendLayout();
            SuspendLayout();
            //
            // toolStrip1
            //
            toolStrip1.Font = new Font("Segoe UI", 10F);
            toolStrip1.GripStyle = ToolStripGripStyle.Hidden;
            toolStrip1.ImageScalingSize = new Size(24, 24);
            toolStrip1.Items.AddRange(new ToolStripItem[] { tsbNew, tsbSave, tsbDelete, toolStripSeparator1, tsbFirst, tsbPrevious, tsbNext, tsbLast, toolStripSeparator2, txtSearch, tsbSearch });
            toolStrip1.Location = new Point(0, 0);
            toolStrip1.Name = "toolStrip1";
            toolStrip1.Padding = new Padding(8, 5, 8, 5);
            toolStrip1.RenderMode = ToolStripRenderMode.System;
            toolStrip1.Size = new Size(1118, 46);
            toolStrip1.TabIndex = 0;
            toolStrip1.Text = "toolStrip1";
            toolStrip1.BackColor = Color.FromArgb(240, 240, 240);
            //
            // tsbNew
            //
            tsbNew.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbNew.Image = (Image)resources.GetObject("tsbNew.Image");
            tsbNew.ImageTransparentColor = Color.Magenta;
            tsbNew.Margin = new Padding(4);
            tsbNew.Name = "tsbNew";
            tsbNew.Size = new Size(152, 28);
            tsbNew.Text = "New Employee";
            tsbNew.ToolTipText = "Add New Employee (Ctrl+N)";
            tsbNew.ForeColor = Color.FromArgb(64, 64, 64);
            tsbNew.Click += tsbNew_Click;
            //
            // tsbSave
            //
            tsbSave.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbSave.Image = (Image)resources.GetObject("tsbSave.Image");
            tsbSave.ImageTransparentColor = Color.Magenta;
            tsbSave.Margin = new Padding(4);
            tsbSave.Name = "tsbSave";
            tsbSave.Size = new Size(144, 28);
            tsbSave.Text = "Save Changes";
            tsbSave.ToolTipText = "Save Changes (Ctrl+S)";
            tsbSave.ForeColor = Color.FromArgb(64, 64, 64);
            tsbSave.Click += tsbSave_Click;
            //
            // tsbDelete
            //
            tsbDelete.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbDelete.Image = (Image)resources.GetObject("tsbDelete.Image");
            tsbDelete.ImageTransparentColor = Color.Magenta;
            tsbDelete.Margin = new Padding(4);
            tsbDelete.Name = "tsbDelete";
            tsbDelete.Size = new Size(167, 28);
            tsbDelete.Text = "Delete Employee";
            tsbDelete.ToolTipText = "Delete Selected Employee (Del)";
            tsbDelete.ForeColor = Color.FromArgb(64, 64, 64);
            tsbDelete.Click += tsbDelete_Click;
            //
            // toolStripSeparator1
            //
            toolStripSeparator1.Margin = new Padding(10, 0, 10, 0);
            toolStripSeparator1.Name = "toolStripSeparator1";
            toolStripSeparator1.Size = new Size(6, 36);
            //
            // tsbFirst
            //
            tsbFirst.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbFirst.Image = (Image)resources.GetObject("tsbFirst.Image");
            tsbFirst.ImageTransparentColor = Color.Magenta;
            tsbFirst.Margin = new Padding(4);
            tsbFirst.Name = "tsbFirst";
            tsbFirst.Size = new Size(127, 28);
            tsbFirst.Text = "First Record";
            tsbFirst.ToolTipText = "Go to First Record (Ctrl+Home)";
            tsbFirst.ForeColor = Color.FromArgb(64, 64, 64);
            tsbFirst.Click += tsbFirst_Click;
            //
            // tsbPrevious
            //
            tsbPrevious.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbPrevious.Image = (Image)resources.GetObject("tsbPrevious.Image");
            tsbPrevious.ImageTransparentColor = Color.Magenta;
            tsbPrevious.Margin = new Padding(4);
            tsbPrevious.Name = "tsbPrevious";
            tsbPrevious.Size = new Size(160, 28);
            tsbPrevious.Text = "Previous Record";
            tsbPrevious.ToolTipText = "Go to Previous Record (Ctrl+Left)";
            tsbPrevious.ForeColor = Color.FromArgb(64, 64, 64);
            tsbPrevious.Click += tsbPrevious_Click;
            //
            // tsbNext
            //
            tsbNext.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            tsbNext.Image = (Image)resources.GetObject("tsbNext.Image");
            tsbNext.ImageTransparentColor = Color.Magenta;
            tsbNext.Margin = new Padding(4);
            tsbNext.Name = "tsbNext";
            tsbNext.Size = new Size(132, 28);
            tsbNext.Text = "Next Record";
            tsbNext.ToolTipText = "Go to Next Record (Ctrl+Right)";
            tsbNext.ForeColor = Color.FromArgb(64, 64, 64);
            tsbNext.Click += tsbNext_Click;
            //
            // tsbLast
            //
            tsbLast.DisplayStyle = ToolStripItemDisplayStyle.Text;
            tsbLast.ImageTransparentColor = Color.Magenta;
            tsbLast.Margin = new Padding(4);
            tsbLast.Name = "tsbLast";
            tsbLast.Size = new Size(102, 28);
            tsbLast.Text = "Last Record";
            tsbLast.ToolTipText = "Go to Last Record (Ctrl+End)";
            tsbLast.ForeColor = Color.FromArgb(64, 64, 64);
            tsbLast.Click += tsbLast_Click;
            //
            // toolStripSeparator2
            //
            toolStripSeparator2.Margin = new Padding(10, 0, 10, 0);
            toolStripSeparator2.Name = "toolStripSeparator2";
            toolStripSeparator2.Size = new Size(6, 36);
            //
            // txtSearch
            //
            txtSearch.Alignment = ToolStripItemAlignment.Right;
            txtSearch.BackColor = Color.White;
            txtSearch.BorderStyle = BorderStyle.FixedSingle;
            txtSearch.Font = new Font("Segoe UI", 10F);
            txtSearch.ForeColor = Color.FromArgb(64, 64, 64);
            txtSearch.Margin = new Padding(1, 2, 6, 2);
            txtSearch.Name = "txtSearch";
            txtSearch.Size = new Size(200, 27);
            txtSearch.ToolTipText = "Enter search term and press Enter or click Search";
            txtSearch.KeyDown += txtSearch_KeyDown;
            //
            // tsbSearch
            //
            tsbSearch.Alignment = ToolStripItemAlignment.Right;
            tsbSearch.DisplayStyle = ToolStripItemDisplayStyle.Image;
            tsbSearch.Image = (Image)resources.GetObject("tsbSearch.Image");
            tsbSearch.ImageTransparentColor = Color.Magenta;
            tsbSearch.Margin = new Padding(1, 2, 1, 2);
            tsbSearch.Name = "tsbSearch";
            tsbSearch.Size = new Size(28, 28);
            tsbSearch.Text = "Search";
            tsbSearch.ToolTipText = "Search Employees (Enter)";
            tsbSearch.Click += tsbSearch_Click;
            // 
            // statusStrip1
            // 
            statusStrip1.ImageScalingSize = new Size(20, 20);
            statusStrip1.Items.AddRange(new ToolStripItem[] { lblStatus });
            statusStrip1.Location = new Point(0, 488);
            statusStrip1.Name = "statusStrip1";
            statusStrip1.Padding = new Padding(1, 0, 16, 0);
            statusStrip1.Size = new Size(1118, 22);
            statusStrip1.TabIndex = 2;
            statusStrip1.BackColor = Color.FromArgb(248, 248, 248);
            statusStrip1.Text = "statusStrip1";
            // 
            // lblStatus
            // 
            lblStatus.Name = "lblStatus";
            lblStatus.Size = new Size(1101, 16);
            lblStatus.Spring = true;
            lblStatus.TextAlign = ContentAlignment.MiddleLeft;
            lblStatus.Font = new Font("Segoe UI", 9F);
            lblStatus.ForeColor = Color.FromArgb(80, 80, 80);
            // 
            // employeeBindingSource
            // 
            employeeBindingSource.DataSource = typeof(Employee);
            employeeBindingSource.CurrentChanged += employeeBindingSource_CurrentChanged;
            // 
            // groupBoxDetails
            // 
            groupBoxDetails.Controls.Add(tableLayoutPanelDetails);
            groupBoxDetails.Dock = DockStyle.Fill;
            groupBoxDetails.Location = new Point(0, 46);
            groupBoxDetails.Margin = new Padding(10);
            groupBoxDetails.Name = "groupBoxDetails";
            groupBoxDetails.Padding = new Padding(20);
            groupBoxDetails.Size = new Size(1118, 442);
            groupBoxDetails.TabIndex = 1;
            groupBoxDetails.TabStop = false;
            groupBoxDetails.Text = "Employee Details";
            groupBoxDetails.Font = new Font("Segoe UI Semibold", 10F, FontStyle.Bold);
            groupBoxDetails.ForeColor = Color.FromArgb(55, 55, 55);
            // 
            // tableLayoutPanelDetails
            // 
            tableLayoutPanelDetails.ColumnCount = 2;
            tableLayoutPanelDetails.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 150F));
            tableLayoutPanelDetails.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            tableLayoutPanelDetails.Controls.Add(lblEmployeeID, 0, 0);
            tableLayoutPanelDetails.Controls.Add(txtEmployeeID, 1, 0);
            tableLayoutPanelDetails.Controls.Add(lblFirstName, 0, 1);
            tableLayoutPanelDetails.Controls.Add(txtFirstName, 1, 1);
            tableLayoutPanelDetails.Controls.Add(lblLastName, 0, 2);
            tableLayoutPanelDetails.Controls.Add(txtLastName, 1, 2);
            tableLayoutPanelDetails.Controls.Add(lblPosition, 0, 3);
            tableLayoutPanelDetails.Controls.Add(txtPosition, 1, 3);
            tableLayoutPanelDetails.Controls.Add(lblUsername, 0, 4);
            tableLayoutPanelDetails.Controls.Add(txtUsername, 1, 4);
            tableLayoutPanelDetails.Controls.Add(lblPassword, 0, 5);
            tableLayoutPanelDetails.Controls.Add(txtPassword, 1, 5);
            tableLayoutPanelDetails.Controls.Add(lblPasswordInfo, 1, 6); // Span if needed or just in second column
            tableLayoutPanelDetails.Dock = DockStyle.Fill;
            tableLayoutPanelDetails.Location = new Point(20, 43);
            tableLayoutPanelDetails.Margin = new Padding(0);
            tableLayoutPanelDetails.Name = "tableLayoutPanelDetails";
            tableLayoutPanelDetails.RowCount = 8; // 6 fields, 1 info label, 1 spacer
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F)); // Password
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F)); // Password Info
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableLayoutPanelDetails.Size = new Size(1078, 379);
            tableLayoutPanelDetails.TabIndex = 0;
            // 
            // lblEmployeeID 
            // 
            lblEmployeeID.Anchor = AnchorStyles.Left; lblEmployeeID.AutoSize = true;
            lblEmployeeID.Location = new Point(3, 11); lblEmployeeID.Name = "lblEmployeeID";
            lblEmployeeID.Size = new Size(119, 23); lblEmployeeID.TabIndex = 0; lblEmployeeID.Text = "Employee ID:";
            lblEmployeeID.Font = new Font("Segoe UI", 10F); lblEmployeeID.ForeColor = Color.FromArgb(80, 80, 80);

            txtEmployeeID.Anchor = AnchorStyles.Left | AnchorStyles.Right; txtEmployeeID.Location = new Point(153, 7);
            txtEmployeeID.Margin = new Padding(3, 4, 10, 4); txtEmployeeID.Name = "txtEmployeeID"; txtEmployeeID.ReadOnly = true;
            txtEmployeeID.Size = new Size(915, 30); txtEmployeeID.TabIndex = 99; txtEmployeeID.TabStop = false; // Non-focusable
            txtEmployeeID.Font = new Font("Segoe UI", 10F); txtEmployeeID.ForeColor = Color.FromArgb(100, 100, 100);
            txtEmployeeID.BackColor = Color.FromArgb(245, 245, 245); txtEmployeeID.BorderStyle = BorderStyle.FixedSingle;
            // 
            // lblFirstName 
            // 
            lblFirstName.Anchor = AnchorStyles.Left; lblFirstName.AutoSize = true;
            lblFirstName.Location = new Point(3, 56); lblFirstName.Name = "lblFirstName";
            lblFirstName.Size = new Size(97, 23); lblFirstName.TabIndex = 2; lblFirstName.Text = "First Name:";
            lblFirstName.Font = new Font("Segoe UI", 10F); lblFirstName.ForeColor = Color.FromArgb(80, 80, 80);

            txtFirstName.Anchor = AnchorStyles.Left | AnchorStyles.Right; txtFirstName.Location = new Point(153, 52);
            txtFirstName.Margin = new Padding(3, 4, 10, 4); txtFirstName.MaxLength = 50; txtFirstName.Name = "txtFirstName";
            txtFirstName.Size = new Size(915, 30); txtFirstName.TabIndex = 0;
            txtFirstName.Font = new Font("Segoe UI", 10F); txtFirstName.ForeColor = Color.FromArgb(50, 50, 50); txtFirstName.BorderStyle = BorderStyle.FixedSingle;
            // 
            // lblLastName 
            // 
            lblLastName.Anchor = AnchorStyles.Left; lblLastName.AutoSize = true;
            lblLastName.Location = new Point(3, 101); lblLastName.Name = "lblLastName";
            lblLastName.Size = new Size(95, 23); lblLastName.TabIndex = 4; lblLastName.Text = "Last Name:";
            lblLastName.Font = new Font("Segoe UI", 10F); lblLastName.ForeColor = Color.FromArgb(80, 80, 80);

            txtLastName.Anchor = AnchorStyles.Left | AnchorStyles.Right; txtLastName.Location = new Point(153, 97);
            txtLastName.Margin = new Padding(3, 4, 10, 4); txtLastName.MaxLength = 50; txtLastName.Name = "txtLastName";
            txtLastName.Size = new Size(915, 30); txtLastName.TabIndex = 1;
            txtLastName.Font = new Font("Segoe UI", 10F); txtLastName.ForeColor = Color.FromArgb(50, 50, 50); txtLastName.BorderStyle = BorderStyle.FixedSingle;
            // 
            // lblPosition 
            // 
            lblPosition.Anchor = AnchorStyles.Left; lblPosition.AutoSize = true;
            lblPosition.Location = new Point(3, 146); lblPosition.Name = "lblPosition";
            lblPosition.Size = new Size(73, 23); lblPosition.TabIndex = 6; lblPosition.Text = "Position:";
            lblPosition.Font = new Font("Segoe UI", 10F); lblPosition.ForeColor = Color.FromArgb(80, 80, 80);

            txtPosition.Anchor = AnchorStyles.Left | AnchorStyles.Right; txtPosition.Location = new Point(153, 142);
            txtPosition.Margin = new Padding(3, 4, 10, 4); txtPosition.MaxLength = 50; txtPosition.Name = "txtPosition";
            txtPosition.Size = new Size(915, 30); txtPosition.TabIndex = 2;
            txtPosition.Font = new Font("Segoe UI", 10F); txtPosition.ForeColor = Color.FromArgb(50, 50, 50); txtPosition.BorderStyle = BorderStyle.FixedSingle;
            // 
            // lblUsername 
            // 
            lblUsername.Anchor = AnchorStyles.Left; lblUsername.AutoSize = true;
            lblUsername.Location = new Point(3, 191); lblUsername.Name = "lblUsername";
            lblUsername.Size = new Size(91, 23); lblUsername.TabIndex = 8; lblUsername.Text = "Username:";
            lblUsername.Font = new Font("Segoe UI", 10F); lblUsername.ForeColor = Color.FromArgb(80, 80, 80);

            txtUsername.Anchor = AnchorStyles.Left | AnchorStyles.Right; txtUsername.Location = new Point(153, 187);
            txtUsername.Margin = new Padding(3, 4, 10, 4); txtUsername.MaxLength = 50; txtUsername.Name = "txtUsername";
            txtUsername.Size = new Size(915, 30); txtUsername.TabIndex = 3;
            txtUsername.Font = new Font("Segoe UI", 10F); txtUsername.ForeColor = Color.FromArgb(50, 50, 50); txtUsername.BorderStyle = BorderStyle.FixedSingle;
            // 
            // lblPassword 
            // 
            lblPassword.Anchor = AnchorStyles.Left; lblPassword.AutoSize = true;
            lblPassword.Location = new Point(3, 236); lblPassword.Name = "lblPassword";
            lblPassword.Size = new Size(84, 23); lblPassword.TabIndex = 10; lblPassword.Text = "Password:";
            lblPassword.Font = new Font("Segoe UI", 10F); lblPassword.ForeColor = Color.FromArgb(80, 80, 80);

            txtPassword.Anchor = AnchorStyles.Left | AnchorStyles.Right; txtPassword.Location = new Point(153, 232);
            txtPassword.Margin = new Padding(3, 4, 10, 4); txtPassword.MaxLength = 100; // Hashed passwords can be long
            txtPassword.Name = "txtPassword"; txtPassword.PasswordChar = '*';
            txtPassword.Size = new Size(915, 30); txtPassword.TabIndex = 4;
            txtPassword.Font = new Font("Segoe UI", 10F); txtPassword.ForeColor = Color.FromArgb(50, 50, 50); txtPassword.BorderStyle = BorderStyle.FixedSingle;
            // 
            // lblPasswordInfo
            // 
            lblPasswordInfo.Anchor = AnchorStyles.Left | AnchorStyles.Right | AnchorStyles.Top;
            lblPasswordInfo.AutoSize = false; // Set to false to allow manual sizing and text alignment
            lblPasswordInfo.Location = new Point(153, 270); // Position in the second column, below password
            lblPasswordInfo.Margin = new Padding(3, 0, 10, 0); // Adjust margins as needed
            lblPasswordInfo.Name = "lblPasswordInfo";
            lblPasswordInfo.Size = new Size(915, 30); // Span the width of the second column
            lblPasswordInfo.TabIndex = 12;
            lblPasswordInfo.Text = "Enter password only for new employee or to change existing.";
            lblPasswordInfo.TextAlign = ContentAlignment.MiddleLeft;
            lblPasswordInfo.Font = new Font("Segoe UI", 8F, FontStyle.Italic); 
            lblPasswordInfo.ForeColor = Color.FromArgb(120, 120, 120);
            // 
            // frmEmployees
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.White;
            ClientSize = new Size(1118, 510);
            Controls.Add(groupBoxDetails);
            Controls.Add(statusStrip1);
            Controls.Add(toolStrip1);
            MinimumSize = new Size(650, 520); // Adjusted min height
            Name = "frmEmployees";
            Text = "Manage Employees";
            Font = new Font("Segoe UI", 9F);
            ForeColor = Color.FromArgb(64, 64, 64);
            Load += frmEmployees_Load;
            toolStrip1.ResumeLayout(false);
            toolStrip1.PerformLayout();
            statusStrip1.ResumeLayout(false);
            statusStrip1.PerformLayout();
            ((ISupportInitialize)employeeBindingSource).EndInit();
            groupBoxDetails.ResumeLayout(false);
            tableLayoutPanelDetails.ResumeLayout(false);
            tableLayoutPanelDetails.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }
        #endregion

        private ToolStrip toolStrip1;
        private ToolStripButton tsbNew;
        private ToolStripButton tsbSave;
        private ToolStripButton tsbDelete;
        private ToolStripSeparator toolStripSeparator1;
        private ToolStripButton tsbFirst;
        private ToolStripButton tsbPrevious;
        private ToolStripButton tsbNext;
        private ToolStripButton tsbLast;
        private ToolStripSeparator toolStripSeparator2;
        private ToolStripTextBox txtSearch;
        private ToolStripButton tsbSearch;
        private StatusStrip statusStrip1;
        private ToolStripStatusLabel lblStatus;
        private BindingSource employeeBindingSource;
        private GroupBox groupBoxDetails;
        private TableLayoutPanel tableLayoutPanelDetails;
        private Label lblEmployeeID;
        private TextBox txtEmployeeID;
        private Label lblFirstName;
        private TextBox txtFirstName;
        private Label lblLastName;
        private TextBox txtLastName;
        private Label lblPosition;
        private TextBox txtPosition;
        private Label lblUsername;
        private TextBox txtUsername;
        private Label lblPassword;
        private TextBox txtPassword;
        private Label lblPasswordInfo;
    }
}
```

---
**File 10: `frmEmployees.cs`**
---
```csharp
using Microsoft.EntityFrameworkCore;
using Store.Data.Models;
using Store.Services;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Store.Forms
{
    public partial class frmEmployees : Form
    {
        private readonly EmployeeService _employeeService;
        private bool _isNew = false;
        private bool _isLoading = false;

        public frmEmployees(EmployeeService employeeService)
        {
            InitializeComponent();
            _employeeService = employeeService;
        }

        private async void frmEmployees_Load(object sender, EventArgs e)
        {
            _isLoading = true;
            await LoadDataAsync();
            SetupBindings();
            _isLoading = false;
             if (employeeBindingSource.Count > 0 && employeeBindingSource.Position < 0)
            {
                employeeBindingSource.MoveFirst();
            }
            UpdateButtonStates();
            UpdateNavigationState();
        }

        private async Task LoadDataAsync(string? searchTerm = null)
        {
            ToggleControls(false, true);
            lblStatus.Text = "Loading employees...";
            try
            {
                List<Employee> employees;
                if (string.IsNullOrWhiteSpace(searchTerm))
                {
                    employees = await _employeeService.GetAllEmployeesAsync();
                }
                else
                {
                    employees = await _employeeService.SearchEmployeesAsync(searchTerm);
                }
                
                var currentId = (employeeBindingSource.Current as Employee)?.EmployeeID;

                employeeBindingSource.DataSource = employees;
                employeeBindingSource.ResetBindings(false);

                if (employees.Count == 0)
                {
                    lblStatus.Text = string.IsNullOrWhiteSpace(searchTerm) ? "No employees found. Click 'New' to add one." : $"No employees matching '{searchTerm}'.";
                    ClearForm();
                    SetupBindings();
                }
                else
                {
                     lblStatus.Text = string.IsNullOrWhiteSpace(searchTerm) ? $"Displaying {employees.Count} employees." : $"Found {employees.Count} matching '{searchTerm}'.";
                     if(currentId.HasValue)
                     {
                        SelectEmployeeById(currentId.Value, false);
                     }
                     if (employeeBindingSource.Position < 0 && employees.Count > 0)
                    {
                        employeeBindingSource.MoveFirst();
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading employees: {ex.Message}", "Loading Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Error loading data.";
            }
            finally
            {
                 if (!_isLoading)
                {
                    UpdateButtonStates();
                    UpdateNavigationState();
                }
                ToggleControls(true, true);
            }
        }

        private void SetupBindings()
        {
            txtEmployeeID.DataBindings.Clear();
            txtFirstName.DataBindings.Clear();
            txtLastName.DataBindings.Clear();
            txtPosition.DataBindings.Clear();
            txtUsername.DataBindings.Clear();
            // Password field (txtPassword) is NOT bound directly for security.

            txtEmployeeID.DataBindings.Add("Text", employeeBindingSource, "EmployeeID", true, DataSourceUpdateMode.Never);
            txtFirstName.DataBindings.Add("Text", employeeBindingSource, "FirstName", false, DataSourceUpdateMode.OnValidation);
            txtLastName.DataBindings.Add("Text", employeeBindingSource, "LastName", false, DataSourceUpdateMode.OnValidation);
            txtPosition.DataBindings.Add("Text", employeeBindingSource, "Position", true, DataSourceUpdateMode.OnValidation, string.Empty, "");
            txtUsername.DataBindings.Add("Text", employeeBindingSource, "Username", false, DataSourceUpdateMode.OnValidation);
        }

        private void ClearForm()
        {
            employeeBindingSource.SuspendBinding();
            txtEmployeeID.Clear();
            txtFirstName.Clear();
            txtLastName.Clear();
            txtPosition.Clear();
            txtUsername.Clear();
            txtPassword.Clear(); // Always clear password field
            employeeBindingSource.ResumeBinding();
        }

        private void ToggleControls(bool enabled, bool keepToolbarEnabled = false)
        {
            groupBoxDetails.Enabled = enabled;
            if (!keepToolbarEnabled) toolStrip1.Enabled = enabled;
            else toolStrip1.Enabled = true;
            this.Cursor = enabled ? Cursors.Default : Cursors.WaitCursor;
        }
        
        private void UpdateButtonStates()
        {
            if (_isLoading) return;
            bool hasItems = employeeBindingSource.Count > 0;
            bool isItemSelected = employeeBindingSource.Current != null;

            bool requiredFieldsFilled = !string.IsNullOrWhiteSpace(txtFirstName.Text) &&
                                        !string.IsNullOrWhiteSpace(txtLastName.Text) &&
                                        !string.IsNullOrWhiteSpace(txtUsername.Text);
            if (_isNew)
            {
                requiredFieldsFilled = requiredFieldsFilled && !string.IsNullOrWhiteSpace(txtPassword.Text);
            }


            tsbSave.Enabled = _isNew ? requiredFieldsFilled : (isItemSelected && requiredFieldsFilled);
            tsbDelete.Enabled = isItemSelected && !_isNew;
            tsbFirst.Enabled = isItemSelected && !_isNew && employeeBindingSource.Position > 0;
            tsbPrevious.Enabled = isItemSelected && !_isNew && employeeBindingSource.Position > 0;
            tsbNext.Enabled = isItemSelected && !_isNew && employeeBindingSource.Position < employeeBindingSource.Count - 1;
            tsbLast.Enabled = isItemSelected && !_isNew && employeeBindingSource.Position < employeeBindingSource.Count - 1;
            tsbNew.Enabled = toolStrip1.Enabled;
            txtSearch.Enabled = toolStrip1.Enabled;
            tsbSearch.Enabled = toolStrip1.Enabled;
        }

        private void UpdateNavigationState()
        {
             if (_isLoading) return;
            bool hasItems = employeeBindingSource.Count > 0;
            bool isItemSelected = employeeBindingSource.Current != null;

            if (_isNew)
            {
                lblStatus.Text = "Adding new employee...";
                groupBoxDetails.Enabled = true;
                lblPasswordInfo.Text = "Password is required for new employee.";
                txtPassword.Enabled = true;
            }
            else if (isItemSelected)
            {
                lblStatus.Text = $"Record {employeeBindingSource.Position + 1} of {employeeBindingSource.Count}";
                groupBoxDetails.Enabled = true;
                lblPasswordInfo.Text = "Enter password only to change existing.";
                txtPassword.Enabled = true;
                txtPassword.Clear(); // Clear password when navigating to existing records
            }
            else
            {
                lblStatus.Text = hasItems ? "No employee selected." : (string.IsNullOrWhiteSpace(txtSearch.Text) ? "No employees found." : $"No employees matching '{txtSearch.Text}'.");
                groupBoxDetails.Enabled = false;
                txtPassword.Enabled = false;
                if (!hasItems) ClearForm();
            }
            UpdateButtonStates();
        }

        private void tsbNew_Click(object sender, EventArgs e)
        {
            _isNew = true;
            employeeBindingSource.SuspendBinding();
            ClearForm();
            txtFirstName.Focus();
            UpdateNavigationState();
        }

        private async void tsbSave_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtFirstName.Text) || string.IsNullOrWhiteSpace(txtLastName.Text))
            {
                MessageBox.Show("First Name and Last Name cannot be empty.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                txtFirstName.Focus(); return;
            }
            if (string.IsNullOrWhiteSpace(txtUsername.Text))
            {
                MessageBox.Show("Username cannot be empty.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                txtUsername.Focus(); return;
            }
            string? plainPassword = txtPassword.Text; // Can be empty if updating without changing password
            if (_isNew && string.IsNullOrWhiteSpace(plainPassword))
            {
                MessageBox.Show("Password is required for a new employee.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                txtPassword.Focus(); return;
            }

            if (!_isNew && employeeBindingSource.Current != null)
            {
                employeeBindingSource.EndEdit();
            }

            ToggleControls(false);
            lblStatus.Text = "Saving...";

            try
            {
                bool success = false;
                Employee? employeeToSave = null;
                bool wasNewItemInitially = _isNew;

                if (_isNew)
                {
                    employeeToSave = new Employee
                    {
                        FirstName = txtFirstName.Text.Trim(),
                        LastName = txtLastName.Text.Trim(),
                        Position = string.IsNullOrWhiteSpace(txtPosition.Text) ? null : txtPosition.Text.Trim(),
                        Username = txtUsername.Text.Trim(),
                        // PasswordHash will be set by the service
                    };
                    success = await _employeeService.AddEmployeeAsync(employeeToSave, plainPassword!); // plainPassword must not be null here
                     if (success) lblStatus.Text = "Employee added successfully.";
                }
                else
                {
                    if (employeeBindingSource.Current is Employee currentEmployee)
                    {
                        currentEmployee.FirstName = txtFirstName.Text.Trim();
                        currentEmployee.LastName = txtLastName.Text.Trim();
                        currentEmployee.Position = string.IsNullOrWhiteSpace(txtPosition.Text) ? null : txtPosition.Text.Trim();
                        currentEmployee.Username = txtUsername.Text.Trim();
                        employeeToSave = currentEmployee;
                        // Pass null if password field is empty, meaning don't change password
                        string? passwordToUpdate = string.IsNullOrWhiteSpace(plainPassword) ? null : plainPassword;
                        success = await _employeeService.UpdateEmployeeAsync(currentEmployee, passwordToUpdate);
                         if (success) lblStatus.Text = "Employee updated successfully.";
                    }
                     else
                    {
                         MessageBox.Show("No employee selected to update.", "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                         lblStatus.Text = "No employee selected.";
                    }
                }

                if (success)
                {
                    _isNew = false;
                    txtPassword.Clear(); // Clear password field after successful save
                    int savedItemId = employeeToSave?.EmployeeID ?? -1;
                    string? currentSearchTerm = wasNewItemInitially ? null : txtSearch.Text;
                    if (wasNewItemInitially) txtSearch.Clear();
                    
                    await LoadDataAsync(currentSearchTerm);
                    
                    if (savedItemId > 0) SelectEmployeeById(savedItemId);
                    else if(employeeBindingSource.Count > 0) employeeBindingSource.MoveFirst();
                }
            }
            catch (DbUpdateConcurrencyException)
            {
                MessageBox.Show("Record modified. Reload and try again.", "Concurrency Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                lblStatus.Text = "Save failed due to concurrency.";
                await LoadDataAsync(txtSearch.Text);
            }
            catch (DbUpdateException dbEx)
            {
                 string errorMessage = $"Database error: {dbEx.InnerException?.Message ?? dbEx.Message}.";
                 if (dbEx.InnerException?.Message.Contains("UNIQUE KEY constraint") == true || 
                    dbEx.InnerException?.Message.Contains("duplicate key value violates unique constraint") == true)
                {
                    errorMessage += "\nThe username might already exist.";
                }
                MessageBox.Show(errorMessage, "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Database save error.";
            }
            catch (Exception ex)
            {
                MessageBox.Show($"An error occurred: {ex.Message}", "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Save error.";
            }
            finally
            {
                if (!success) { 
                     ToggleControls(true);
                     UpdateButtonStates();
                     UpdateNavigationState();
                }
            }
        }

        private async void tsbDelete_Click(object sender, EventArgs e)
        {
            if (_isNew) {
                MessageBox.Show("Cannot delete an unsaved new employee.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }
            if (employeeBindingSource.Current is Employee currentEmployee)
            {
                var confirmResult = MessageBox.Show($"Delete employee '{currentEmployee.FullName}' (Username: {currentEmployee.Username})?", "Confirm Delete", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                if (confirmResult == DialogResult.Yes)
                {
                    ToggleControls(false);
                    lblStatus.Text = "Deleting...";
                    try
                    {
                        bool success = await _employeeService.DeleteEmployeeAsync(currentEmployee.EmployeeID);
                        if (success) lblStatus.Text = "Employee deleted.";
                        await LoadDataAsync(txtSearch.Text.Trim());
                    }
                    catch (DbUpdateException dbEx) // Catch specific for FK, etc.
                    {
                        MessageBox.Show($"Database error: {dbEx.InnerException?.Message ?? dbEx.Message}.\nEmployee might have related records.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        lblStatus.Text = "Database delete error.";
                         await LoadDataAsync(txtSearch.Text.Trim());
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"An error occurred: {ex.Message}", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        lblStatus.Text = "Delete error.";
                         await LoadDataAsync(txtSearch.Text.Trim());
                    }
                }
            }
            else
            {
                MessageBox.Show("No employee selected.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private async void PerformSearch()
        {
             _isNew = false; employeeBindingSource.ResumeBinding();
            await LoadDataAsync(txtSearch.Text.Trim());
        }
        private void tsbSearch_Click(object sender, EventArgs e) => PerformSearch();
        private void txtSearch_KeyDown(object sender, KeyEventArgs e) { if (e.KeyCode == Keys.Enter) { PerformSearch(); e.SuppressKeyPress = true; } }
        private void tsbFirst_Click(object sender, EventArgs e) { if (_isNew) _isNew = false; employeeBindingSource.ResumeBinding(); employeeBindingSource.MoveFirst(); }
        private void tsbPrevious_Click(object sender, EventArgs e) { if (_isNew) _isNew = false; employeeBindingSource.ResumeBinding(); employeeBindingSource.MovePrevious(); }
        private void tsbNext_Click(object sender, EventArgs e) { if (_isNew) _isNew = false; employeeBindingSource.ResumeBinding(); employeeBindingSource.MoveNext(); }
        private void tsbLast_Click(object sender, EventArgs e) { if (_isNew) _isNew = false; employeeBindingSource.ResumeBinding(); employeeBindingSource.MoveLast(); }

        private void employeeBindingSource_CurrentChanged(object sender, EventArgs e)
        {
            if (_isLoading || _isNew) return;
            if (employeeBindingSource.Current == null) ClearForm();
            else txtPassword.Clear(); // Clear password on navigation to existing employee
            UpdateButtonStates();
            UpdateNavigationState();
        }

        private void SelectEmployeeById(int employeeId, bool triggerCurrentChanged = true)
        {
            if (employeeId <= 0) return;
            if (employeeBindingSource.DataSource is List<Employee> employees)
            {
                int index = employees.FindIndex(emp => emp.EmployeeID == employeeId);
                if (index != -1)
                {
                     if(!triggerCurrentChanged)
                    {
                        this.employeeBindingSource.CurrentChanged -= employeeBindingSource_CurrentChanged;
                        employeeBindingSource.Position = index;
                        this.employeeBindingSource.CurrentChanged += employeeBindingSource_CurrentChanged;
                        if(employeeBindingSource.Current is Employee emp)
                        {
                            txtEmployeeID.Text = emp.EmployeeID.ToString();
                            txtFirstName.Text = emp.FirstName;
                            txtLastName.Text = emp.LastName;
                            txtPosition.Text = emp.Position;
                            txtUsername.Text = emp.Username;
                            txtPassword.Clear(); // Password is not displayed
                        }
                    }
                    else
                    {
                         employeeBindingSource.Position = index;
                    }
                }
            }
        }
    }
}
```

**To Use These Files:**

1.  **Replace existing files:** If you have `frmCategories.Designer.cs`, `frmCategories.cs`, etc., in your project, replace their content with the code provided above.
2.  **Add New Files:** If these forms are new, add new Windows Forms to your project with these names (e.g., `frmSuppliers`) and then paste the `Designer.cs` content into the `*.Designer.cs` file and the `cs` content into the `*.cs` file.
3.  **Ensure Services Exist:** Make sure you have `CategoryService.cs`, `SupplierService.cs`, `ProductService.cs`, `CustomerService.cs`, and `EmployeeService.cs` in your `Store.Services` namespace, and that they have the methods being called (e.g., `GetAllAsync`, `SearchAsync`, `AddAsync`, `UpdateAsync`, `DeleteAsync`).
    *   `ProductService` will also need `GetCategoriesForDropdownAsync()` and `GetSuppliersForDropdownAsync()`.
    *   `EmployeeService` methods `AddEmployeeAsync` and `UpdateEmployeeAsync` will need to handle password hashing.
4.  **Ensure Models Exist:** Your `Store.Data.Models` namespace should contain `Category.cs`, `Supplier.cs`, `Product.cs`, `Customer.cs`, and `Employee.cs` with the properties being accessed.
5.  **Resource Files:** The `Designer.cs` files reference images like `(Image)resources.GetObject("tsbNew.Image")`. Ensure these image resources are correctly set up in your project's resource file (usually `Resources.resx`). If not, the designer might show errors or buttons might not have icons.
6.  **Dependency Injection:** You'll need to instantiate these forms and pass the required services to their constructors (e.g., using a dependency injection framework or manual instantiation).

This comprehensive set of files should address the issue of navigation buttons not working after adding and saving a new record by correctly managing the UI state and data binding.

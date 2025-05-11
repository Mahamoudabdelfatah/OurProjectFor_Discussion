Okay, let's proceed with `frmSuppliers` and then `frmProducts`.

**`frmSuppliers.Designer.cs` (Updated)**
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
            tsbNew.Size = new Size(138, 28); // Adjusted
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
            tsbDelete.Size = new Size(153, 28); // Adjusted
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
            groupBoxDetails.Location = new Point(0, 46); // Adjusted
            groupBoxDetails.Margin = new Padding(10);
            groupBoxDetails.Name = "groupBoxDetails";
            groupBoxDetails.Padding = new Padding(20);
            groupBoxDetails.Size = new Size(1118, 396); // Adjusted
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
            tableLayoutPanelDetails.Size = new Size(1078, 333); // Adjusted
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
            txtSupplierID.TabIndex = 1;
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
            MinimumSize = new Size(600, 400);
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

**`frmSuppliers.cs` (Updated)**
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

        public frmSuppliers(SupplierService supplierService)
        {
            InitializeComponent();
            _supplierService = supplierService;
        }

        private async void frmSuppliers_Load(object sender, EventArgs e)
        {
            await LoadDataAsync();
            SetupBindings();
            UpdateButtonStates();
            UpdateNavigationState();
        }

        private async Task LoadDataAsync(string? searchTerm = null)
        {
            ToggleControls(false);
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
                    lblStatus.Text = $"Found {suppliers.Count} matching '{searchTerm}'.";
                }

                supplierBindingSource.DataSource = suppliers;
                supplierBindingSource.ResetBindings(false);

                if (suppliers.Count == 0 && string.IsNullOrWhiteSpace(searchTerm))
                {
                    lblStatus.Text = "No suppliers found. Click 'New' to add one.";
                    ClearForm();
                }
                else if (suppliers.Count > 0)
                {
                    lblStatus.Text = $"Displaying {suppliers.Count} suppliers.";
                    if (supplierBindingSource.Position < 0) supplierBindingSource.MoveFirst();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading suppliers: {ex.Message}", "Loading Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Error loading data.";
            }
            finally
            {
                // _isNew = false; // Moved to tsbSave_Click success path
                UpdateButtonStates();
                UpdateNavigationState();
                ToggleControls(true);
            }
        }

        private void SetupBindings()
        {
            txtSupplierID.DataBindings.Clear();
            txtSupplierName.DataBindings.Clear();
            txtContactPerson.DataBindings.Clear();
            txtPhoneNumber.DataBindings.Clear();
            txtEmail.DataBindings.Clear();

            txtSupplierID.DataBindings.Add("Text", supplierBindingSource, "SupplierID", true, DataSourceUpdateMode.OnPropertyChanged);
            txtSupplierName.DataBindings.Add("Text", supplierBindingSource, "SupplierName", false, DataSourceUpdateMode.OnValidation);
            txtContactPerson.DataBindings.Add("Text", supplierBindingSource, "ContactPerson", true, DataSourceUpdateMode.OnValidation, string.Empty); 
            txtPhoneNumber.DataBindings.Add("Text", supplierBindingSource, "PhoneNumber", true, DataSourceUpdateMode.OnValidation, string.Empty);   
            txtEmail.DataBindings.Add("Text", supplierBindingSource, "Email", true, DataSourceUpdateMode.OnValidation, string.Empty);           
        }

        private void ClearForm()
        {
            txtSupplierID.DataBindings.Clear();
            txtSupplierName.DataBindings.Clear();
            txtContactPerson.DataBindings.Clear();
            txtPhoneNumber.DataBindings.Clear();
            txtEmail.DataBindings.Clear();

            txtSupplierID.Clear();
            txtSupplierName.Clear();
            txtContactPerson.Clear();
            txtPhoneNumber.Clear();
            txtEmail.Clear();
        }

        private void ToggleControls(bool enabled)
        {
            Control? detailsContainer = this.Controls.Find("groupBoxDetails", true).FirstOrDefault();
            Control? toolStrip = this.Controls.Find("toolStrip1", true).FirstOrDefault();

            if (detailsContainer != null) detailsContainer.Enabled = enabled;
            if (toolStrip != null) toolStrip.Enabled = true;
            this.Cursor = enabled ? Cursors.Default : Cursors.WaitCursor;
        }

        private void UpdateButtonStates()
        {
            bool hasItems = supplierBindingSource.Count > 0;
            bool isItemSelected = supplierBindingSource.Position >= 0;

            tsbSave.Enabled = _isNew || (hasItems && isItemSelected);
            tsbDelete.Enabled = hasItems && isItemSelected && !_isNew;
            tsbFirst.Enabled = hasItems && isItemSelected && !_isNew && supplierBindingSource.Position > 0;
            tsbPrevious.Enabled = hasItems && isItemSelected && !_isNew && supplierBindingSource.Position > 0;
            tsbNext.Enabled = hasItems && isItemSelected && !_isNew && supplierBindingSource.Position < supplierBindingSource.Count - 1;
            tsbLast.Enabled = hasItems && isItemSelected && !_isNew && supplierBindingSource.Position < supplierBindingSource.Count - 1;
            tsbNew.Enabled = true;
            txtSearch.Enabled = true;
            tsbSearch.Enabled = true;
        }

        private void UpdateNavigationState()
        {
            bool hasItems = supplierBindingSource.Count > 0;
            bool isItemSelected = supplierBindingSource.Position >= 0;

            if (_isNew)
            {
                lblStatus.Text = "Adding new supplier...";
                groupBoxDetails.Enabled = true;
                tsbFirst.Enabled = false; tsbPrevious.Enabled = false; tsbNext.Enabled = false; tsbLast.Enabled = false;
            }
            else if (hasItems && isItemSelected)
            {
                lblStatus.Text = $"Record {supplierBindingSource.Position + 1} of {supplierBindingSource.Count}";
                groupBoxDetails.Enabled = true;
                tsbFirst.Enabled = supplierBindingSource.Position > 0;
                tsbPrevious.Enabled = supplierBindingSource.Position > 0;
                tsbNext.Enabled = supplierBindingSource.Position < supplierBindingSource.Count - 1;
                tsbLast.Enabled = supplierBindingSource.Position < supplierBindingSource.Count - 1;
            }
            else
            {
                lblStatus.Text = hasItems ? "No supplier selected." : "No suppliers found.";
                groupBoxDetails.Enabled = false;
                tsbFirst.Enabled = false; tsbPrevious.Enabled = false; tsbNext.Enabled = false; tsbLast.Enabled = false;
                 if (!hasItems) ClearForm();
            }
            tsbSave.Enabled = _isNew || (hasItems && isItemSelected);
            tsbDelete.Enabled = hasItems && isItemSelected && !_isNew;
        }

        private void tsbNew_Click(object sender, EventArgs e)
        {
            _isNew = true;
            supplierBindingSource.SuspendBinding();
            ClearForm();
            groupBoxDetails.Enabled = true;
            txtSupplierName.Focus();
            UpdateNavigationState();
            UpdateButtonStates();
        }

        private async void tsbSave_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtSupplierName.Text))
            {
                MessageBox.Show("Supplier Name cannot be empty.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                txtSupplierName.Focus();
                return;
            }

            if(!_isNew)
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
                    lblStatus.Text = success ? "Supplier added successfully." : "Failed to add supplier.";
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
                        lblStatus.Text = success ? "Supplier updated successfully." : "Failed to update supplier.";
                    }
                    else
                    {
                        MessageBox.Show("No supplier selected to update.", "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }

                if (success)
                {
                    _isNew = false;
                    int savedItemId = supplierToSave?.SupplierID ?? -1;

                    if(wasNewItemInitially)
                    {
                        txtSearch.Clear();
                        await LoadDataAsync(null);
                    }
                    else
                    {
                        await LoadDataAsync(txtSearch.Text);
                    }
                    
                    if (savedItemId > 0) SelectSupplierById(savedItemId);
                }
            }
            catch (DbUpdateConcurrencyException)
            {
                MessageBox.Show("Record modified by another user. Reload and try again.", "Concurrency Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                lblStatus.Text = "Save failed due to concurrency.";
                await LoadDataAsync(txtSearch.Text);
            }
            catch (DbUpdateException dbEx)
            {
                MessageBox.Show($"Database error: {dbEx.InnerException?.Message ?? dbEx.Message}.", "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Database save error.";
            }
            catch (Exception ex)
            {
                MessageBox.Show($"An error occurred: {ex.Message}", "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Save error.";
            }
            finally
            {
                ToggleControls(true);
                // UpdateButtonStates(); // Called by LoadDataAsync
                // UpdateNavigationState(); // Called by LoadDataAsync
            }
        }

        private async void tsbDelete_Click(object sender, EventArgs e)
        {
            if (supplierBindingSource.Current is Supplier currentSupplier)
            {
                var confirmResult = MessageBox.Show($"Delete supplier '{currentSupplier.SupplierName}' (ID: {currentSupplier.SupplierID})?",
                                                     "Confirm Delete", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);

                if (confirmResult == DialogResult.Yes)
                {
                    ToggleControls(false);
                    lblStatus.Text = "Deleting...";
                    try
                    {
                        bool success = await _supplierService.DeleteSupplierAsync(currentSupplier.SupplierID);
                        
                        if (success)
                        {
                            lblStatus.Text = "Supplier deleted.";
                            await LoadDataAsync(txtSearch.Text.Trim()); 
                        }
                        else
                        {
                            MessageBox.Show("Failed to delete supplier. It might have related products.", "Delete Failed", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                            lblStatus.Text = "Delete failed.";
                            await LoadDataAsync(txtSearch.Text.Trim());
                        }
                    }
                    catch (DbUpdateException dbEx)
                    {
                        MessageBox.Show($"Database error: {dbEx.InnerException?.Message ?? dbEx.Message}. Cannot delete supplier with related products.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        lblStatus.Text = "Database delete error.";
                        await LoadDataAsync(txtSearch.Text.Trim());
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"An error occurred: {ex.Message}", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        lblStatus.Text = "Delete error.";
                        await LoadDataAsync(txtSearch.Text.Trim());
                    }
                    finally
                    {
                        ToggleControls(true);
                    }
                }
            }
            else
            {
                MessageBox.Show("No supplier selected.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private async void PerformSearch() => await LoadDataAsync(txtSearch.Text.Trim());
        private void tsbSearch_Click(object sender, EventArgs e) => PerformSearch();
        private void txtSearch_KeyDown(object sender, KeyEventArgs e) { if (e.KeyCode == Keys.Enter) { PerformSearch(); e.SuppressKeyPress = true; } }
        private void tsbFirst_Click(object sender, EventArgs e) => supplierBindingSource.MoveFirst();
        private void tsbPrevious_Click(object sender, EventArgs e) => supplierBindingSource.MovePrevious();
        private void tsbNext_Click(object sender, EventArgs e) => supplierBindingSource.MoveNext();
        private void tsbLast_Click(object sender, EventArgs e) => supplierBindingSource.MoveLast();

        private void supplierBindingSource_CurrentChanged(object sender, EventArgs e)
        {
            if (!_isNew) 
            { 
                if(supplierBindingSource.Current == null)
                {
                    ClearForm();
                }
                UpdateButtonStates(); 
                UpdateNavigationState(); 
            }
        }

        private void SelectSupplierById(int supplierId)
        {
            if (supplierId <= 0) return;
             if (supplierBindingSource.DataSource is List<Supplier> suppliers)
            {
                int index = suppliers.FindIndex(sup => sup.SupplierID == supplierId);
                if (index != -1)
                {
                    supplierBindingSource.Position = index;
                }
            }
        }
    }
}
```

---
And now for `frmProducts`.

**`frmProducts.Designer.cs` (Updated)**
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
            lblSupplier = new Label();
            cmbSupplier = new ComboBox();
            lblPurchasePrice = new Label();
            txtPurchasePrice = new TextBox();
            lblSellingPrice = new Label();
            txtSellingPrice = new TextBox();
            lblStockQuantity = new Label();
            txtStockQuantity = new TextBox();
            toolStrip1.SuspendLayout();
            statusStrip1.SuspendLayout();
            ((ISupportInitialize)productBindingSource).BeginInit();
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
            tsbNew.Size = new Size(136, 28); // Adjusted
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
            tsbDelete.Size = new Size(151, 28); // Adjusted
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
            // groupBoxDetails
            // 
            groupBoxDetails.Controls.Add(tableLayoutPanelDetails);
            groupBoxDetails.Dock = DockStyle.Fill;
            groupBoxDetails.Font = new Font("Segoe UI Semibold", 10F, FontStyle.Bold);
            groupBoxDetails.ForeColor = Color.FromArgb(55, 55, 55);
            groupBoxDetails.Location = new Point(0, 46); // Adjusted
            groupBoxDetails.Margin = new Padding(10);
            groupBoxDetails.Name = "groupBoxDetails";
            groupBoxDetails.Padding = new Padding(20);
            groupBoxDetails.Size = new Size(1118, 546); // Adjusted
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
            tableLayoutPanelDetails.RowCount = 9;
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 80F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 45F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableLayoutPanelDetails.Size = new Size(1078, 483); // Adjusted
            tableLayoutPanelDetails.TabIndex = 0;
            // 
            // lblProductID
            // 
            lblProductID.Anchor = AnchorStyles.Left;
            lblProductID.AutoSize = true;
            lblProductID.Font = new Font("Segoe UI", 10F);
            lblProductID.ForeColor = Color.FromArgb(80, 80, 80);
            lblProductID.Location = new Point(3, 11);
            lblProductID.Name = "lblProductID";
            lblProductID.Size = new Size(96, 23);
            lblProductID.TabIndex = 0;
            lblProductID.Text = "Product ID:";
            // 
            // txtProductID
            // 
            txtProductID.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            txtProductID.BackColor = Color.FromArgb(245, 245, 245);
            txtProductID.BorderStyle = BorderStyle.FixedSingle;
            txtProductID.Font = new Font("Segoe UI", 10F);
            txtProductID.ForeColor = Color.FromArgb(100, 100, 100);
            txtProductID.Location = new Point(153, 7);
            txtProductID.Margin = new Padding(3, 4, 10, 4);
            txtProductID.Name = "txtProductID";
            txtProductID.ReadOnly = true;
            txtProductID.Size = new Size(915, 30);
            txtProductID.TabIndex = 1;
            txtProductID.TabStop = false;
            // 
            // lblProductName
            // 
            lblProductName.Anchor = AnchorStyles.Left;
            lblProductName.AutoSize = true;
            lblProductName.Font = new Font("Segoe UI", 10F);
            lblProductName.ForeColor = Color.FromArgb(80, 80, 80);
            lblProductName.Location = new Point(3, 56);
            lblProductName.Name = "lblProductName";
            lblProductName.Size = new Size(125, 23);
            lblProductName.TabIndex = 2;
            lblProductName.Text = "Product Name:";
            // 
            // txtProductName
            // 
            txtProductName.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            txtProductName.BorderStyle = BorderStyle.FixedSingle;
            txtProductName.Font = new Font("Segoe UI", 10F);
            txtProductName.ForeColor = Color.FromArgb(50, 50, 50);
            txtProductName.Location = new Point(153, 52);
            txtProductName.Margin = new Padding(3, 4, 10, 4);
            txtProductName.MaxLength = 100;
            txtProductName.Name = "txtProductName";
            txtProductName.Size = new Size(915, 30);
            txtProductName.TabIndex = 0;
            // 
            // lblDescription
            // 
            lblDescription.AutoSize = true;
            lblDescription.Font = new Font("Segoe UI", 10F);
            lblDescription.ForeColor = Color.FromArgb(80, 80, 80);
            lblDescription.Location = new Point(3, 98); // Top align for multiline
            lblDescription.Margin = new Padding(3, 8, 3, 0);
            lblDescription.Name = "lblDescription";
            lblDescription.Size = new Size(100, 23);
            lblDescription.TabIndex = 4;
            lblDescription.Text = "Description:";
            // 
            // txtDescription
            // 
            txtDescription.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
            txtDescription.BorderStyle = BorderStyle.FixedSingle;
            txtDescription.Font = new Font("Segoe UI", 10F);
            txtDescription.ForeColor = Color.FromArgb(50, 50, 50);
            txtDescription.Location = new Point(153, 94);
            txtDescription.Margin = new Padding(3, 4, 10, 4);
            txtDescription.MaxLength = 1000;
            txtDescription.Multiline = true;
            txtDescription.Name = "txtDescription";
            txtDescription.ScrollBars = ScrollBars.Vertical;
            txtDescription.Size = new Size(915, 72);
            txtDescription.TabIndex = 1;
            // 
            // lblCategory
            // 
            lblCategory.Anchor = AnchorStyles.Left;
            lblCategory.AutoSize = true;
            lblCategory.Font = new Font("Segoe UI", 10F);
            lblCategory.ForeColor = Color.FromArgb(80, 80, 80);
            lblCategory.Location = new Point(3, 181);
            lblCategory.Name = "lblCategory";
            lblCategory.Size = new Size(83, 23);
            lblCategory.TabIndex = 6;
            lblCategory.Text = "Category:";
            // 
            // cmbCategory
            // 
            cmbCategory.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            cmbCategory.DropDownStyle = ComboBoxStyle.DropDownList;
            cmbCategory.Font = new Font("Segoe UI", 10F);
            cmbCategory.ForeColor = Color.FromArgb(50, 50, 50);
            cmbCategory.FormattingEnabled = true;
            cmbCategory.Location = new Point(153, 178);
            cmbCategory.Margin = new Padding(3, 4, 10, 4);
            cmbCategory.Name = "cmbCategory";
            cmbCategory.Size = new Size(915, 31);
            cmbCategory.TabIndex = 2;
            // 
            // lblSupplier
            // 
            lblSupplier.Anchor = AnchorStyles.Left;
            lblSupplier.AutoSize = true;
            lblSupplier.Font = new Font("Segoe UI", 10F);
            lblSupplier.ForeColor = Color.FromArgb(80, 80, 80);
            lblSupplier.Location = new Point(3, 226);
            lblSupplier.Name = "lblSupplier";
            lblSupplier.Size = new Size(76, 23);
            lblSupplier.TabIndex = 8;
            lblSupplier.Text = "Supplier:";
            // 
            // cmbSupplier
            // 
            cmbSupplier.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            cmbSupplier.DropDownStyle = ComboBoxStyle.DropDownList;
            cmbSupplier.Font = new Font("Segoe UI", 10F);
            cmbSupplier.ForeColor = Color.FromArgb(50, 50, 50);
            cmbSupplier.FormattingEnabled = true;
            cmbSupplier.Location = new Point(153, 223);
            cmbSupplier.Margin = new Padding(3, 4, 10, 4);
            cmbSupplier.Name = "cmbSupplier";
            cmbSupplier.Size = new Size(915, 31);
            cmbSupplier.TabIndex = 3;
            // 
            // lblPurchasePrice
            // 
            lblPurchasePrice.Anchor = AnchorStyles.Left;
            lblPurchasePrice.AutoSize = true;
            lblPurchasePrice.Font = new Font("Segoe UI", 10F);
            lblPurchasePrice.ForeColor = Color.FromArgb(80, 80, 80);
            lblPurchasePrice.Location = new Point(3, 271);
            lblPurchasePrice.Name = "lblPurchasePrice";
            lblPurchasePrice.Size = new Size(125, 23);
            lblPurchasePrice.TabIndex = 10;
            lblPurchasePrice.Text = "Purchase Price:";
            // 
            // txtPurchasePrice
            // 
            txtPurchasePrice.Anchor = AnchorStyles.Left; // Removed Right Anchor
            txtPurchasePrice.BorderStyle = BorderStyle.FixedSingle;
            txtPurchasePrice.Font = new Font("Segoe UI", 10F);
            txtPurchasePrice.ForeColor = Color.FromArgb(50, 50, 50);
            txtPurchasePrice.Location = new Point(153, 267);
            txtPurchasePrice.Margin = new Padding(3, 4, 10, 4);
            txtPurchasePrice.MaxLength = 15;
            txtPurchasePrice.Name = "txtPurchasePrice";
            txtPurchasePrice.Size = new Size(200, 30); // Fixed width
            txtPurchasePrice.TabIndex = 4;
            txtPurchasePrice.TextAlign = HorizontalAlignment.Right;
            // 
            // lblSellingPrice
            // 
            lblSellingPrice.Anchor = AnchorStyles.Left;
            lblSellingPrice.AutoSize = true;
            lblSellingPrice.Font = new Font("Segoe UI", 10F);
            lblSellingPrice.ForeColor = Color.FromArgb(80, 80, 80);
            lblSellingPrice.Location = new Point(3, 316);
            lblSellingPrice.Name = "lblSellingPrice";
            lblSellingPrice.Size = new Size(106, 23);
            lblSellingPrice.TabIndex = 12;
            lblSellingPrice.Text = "Selling Price:";
            // 
            // txtSellingPrice
            // 
            txtSellingPrice.Anchor = AnchorStyles.Left; // Removed Right Anchor
            txtSellingPrice.BorderStyle = BorderStyle.FixedSingle;
            txtSellingPrice.Font = new Font("Segoe UI", 10F);
            txtSellingPrice.ForeColor = Color.FromArgb(50, 50, 50);
            txtSellingPrice.Location = new Point(153, 312);
            txtSellingPrice.Margin = new Padding(3, 4, 10, 4);
            txtSellingPrice.MaxLength = 15;
            txtSellingPrice.Name = "txtSellingPrice";
            txtSellingPrice.Size = new Size(200, 30); // Fixed width
            txtSellingPrice.TabIndex = 5;
            txtSellingPrice.TextAlign = HorizontalAlignment.Right;
            // 
            // lblStockQuantity
            // 
            lblStockQuantity.Anchor = AnchorStyles.Left;
            lblStockQuantity.AutoSize = true;
            lblStockQuantity.Font = new Font("Segoe UI", 10F);
            lblStockQuantity.ForeColor = Color.FromArgb(80, 80, 80);
            lblStockQuantity.Location = new Point(3, 361);
            lblStockQuantity.Name = "lblStockQuantity";
            lblStockQuantity.Size = new Size(125, 23);
            lblStockQuantity.TabIndex = 14;
            lblStockQuantity.Text = "Stock Quantity:";
            // 
            // txtStockQuantity
            // 
            txtStockQuantity.Anchor = AnchorStyles.Left; // Removed Right Anchor
            txtStockQuantity.BorderStyle = BorderStyle.FixedSingle;
            txtStockQuantity.Font = new Font("Segoe UI", 10F);
            txtStockQuantity.ForeColor = Color.FromArgb(50, 50, 50);
            txtStockQuantity.Location = new Point(153, 357);
            txtStockQuantity.Margin = new Padding(3, 4, 10, 4);
            txtStockQuantity.MaxLength = 10;
            txtStockQuantity.Name = "txtStockQuantity";
            txtStockQuantity.Size = new Size(150, 30); // Fixed width
            txtStockQuantity.TabIndex = 6;
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
            MinimumSize = new Size(700, 550);
            Name = "frmProducts";
            Text = "Manage Products";
            Load += frmProducts_Load;
            toolStrip1.ResumeLayout(false);
            toolStrip1.PerformLayout();
            statusStrip1.ResumeLayout(false);
            statusStrip1.PerformLayout();
            ((ISupportInitialize)productBindingSource).EndInit();
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

**`frmProducts.cs` (Updated)**
```csharp
using Microsoft.EntityFrameworkCore;
using Store.Data.Models;
using Store.Services; 
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Globalization; // For NumberStyles

namespace Store.Forms
{
    public partial class frmProducts : Form
    {
        private readonly ProductService _productService;
        // If CategoryService and SupplierService are separate and ProductService doesn't provide dropdown data:
        // private readonly CategoryService _categoryService; 
        // private readonly SupplierService _supplierService;
        private bool _isNew = false;
        
        public frmProducts(ProductService productService /*, CategoryService categoryService, SupplierService supplierService */)
        {
            InitializeComponent();
            _productService = productService;
            // _categoryService = categoryService;
            // _supplierService = supplierService;
        }

        private async void frmProducts_Load(object sender, EventArgs e)
        {
            await LoadComboBoxesAsync();
            await LoadDataAsync();
            SetupBindings(); 
            UpdateButtonStates();
            UpdateNavigationState();
        }

        private async Task LoadComboBoxesAsync()
        {
            try
            {
                // Assuming ProductService provides these lists or use dedicated services
                var categories = await _productService.GetCategoriesForDropdownAsync(); 
                var suppliers = await _productService.GetSuppliersForDropdownAsync();

                if (categories.All(c => c.CategoryID != 0)) { // Add placeholder if not present
                    categories.Insert(0, new Category { CategoryID = 0, CategoryName = "(Select Category)" });
                }
                if (suppliers.All(s => s.SupplierID != 0)) { // Add placeholder if not present
                     suppliers.Insert(0, new Supplier { SupplierID = 0, SupplierName = "(Select Supplier)" });
                }
               
                cmbCategory.DataSource = categories;
                cmbCategory.DisplayMember = "CategoryName";
                cmbCategory.ValueMember = "CategoryID";
                if(cmbCategory.Items.Count > 0) cmbCategory.SelectedIndex = 0; 

                cmbSupplier.DataSource = suppliers;
                cmbSupplier.DisplayMember = "SupplierName";
                cmbSupplier.ValueMember = "SupplierID";
                if(cmbSupplier.Items.Count > 0) cmbSupplier.SelectedIndex = 0;
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading categories/suppliers for dropdowns: {ex.Message}", "Dropdown Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                cmbCategory.Enabled = false;
                cmbSupplier.Enabled = false;
            }
        }

        private async Task LoadDataAsync(string? searchTerm = null)
        {
            ToggleControls(false);
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
                    lblStatus.Text = $"Found {products.Count} matching '{searchTerm}'.";
                }

                productBindingSource.DataSource = products;
                productBindingSource.ResetBindings(false);

                if (products.Count == 0 && string.IsNullOrWhiteSpace(searchTerm))
                {
                    lblStatus.Text = "No products found. Click 'New' to add one.";
                    ClearForm();
                }
                else if (products.Count > 0)
                {
                    lblStatus.Text = $"Displaying {products.Count} products.";
                    if (productBindingSource.Position < 0) productBindingSource.MoveFirst();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading products: {ex.Message}", "Loading Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Error loading data.";
            }
            finally
            {
                // _isNew = false; // Moved to tsbSave_Click success path
                UpdateButtonStates();
                UpdateNavigationState();
                ToggleControls(true);
            }
        }

        private void SetupBindings()
        {
            txtProductID.DataBindings.Clear();
            txtProductName.DataBindings.Clear();
            txtDescription.DataBindings.Clear();
            cmbCategory.DataBindings.Clear(); 
            cmbSupplier.DataBindings.Clear(); 
            txtPurchasePrice.DataBindings.Clear();
            txtSellingPrice.DataBindings.Clear();
            txtStockQuantity.DataBindings.Clear();

            txtProductID.DataBindings.Add("Text", productBindingSource, "ProductID", true, DataSourceUpdateMode.OnPropertyChanged);
            txtProductName.DataBindings.Add("Text", productBindingSource, "ProductName", false, DataSourceUpdateMode.OnValidation);
            txtDescription.DataBindings.Add("Text", productBindingSource, "Description", true, DataSourceUpdateMode.OnValidation, string.Empty); 

            cmbCategory.DataBindings.Add("SelectedValue", productBindingSource, "CategoryID", true, DataSourceUpdateMode.OnValidation, 0); 
            cmbSupplier.DataBindings.Add("SelectedValue", productBindingSource, "SupplierID", true, DataSourceUpdateMode.OnValidation, 0); 
            
            txtPurchasePrice.DataBindings.Add("Text", productBindingSource, "PurchasePrice", true, DataSourceUpdateMode.OnValidation, DBNull.Value, "N2"); 
            txtSellingPrice.DataBindings.Add("Text", productBindingSource, "SellingPrice", true, DataSourceUpdateMode.OnValidation, DBNull.Value, "N2"); 
            txtStockQuantity.DataBindings.Add("Text", productBindingSource, "StockQuantity", true, DataSourceUpdateMode.OnValidation); 
        }

        private void ClearForm()
        {
            txtProductID.DataBindings.Clear();
            txtProductName.DataBindings.Clear();
            txtDescription.DataBindings.Clear();
            cmbCategory.DataBindings.Clear();
            cmbSupplier.DataBindings.Clear();
            txtPurchasePrice.DataBindings.Clear();
            txtSellingPrice.DataBindings.Clear();
            txtStockQuantity.DataBindings.Clear();

            txtProductID.Clear();
            txtProductName.Clear();
            txtDescription.Clear();
            if (cmbCategory.Items.Count > 0) cmbCategory.SelectedIndex = 0; // Select "(Select Category)"
            if (cmbSupplier.Items.Count > 0) cmbSupplier.SelectedIndex = 0; // Select "(Select Supplier)"
            txtPurchasePrice.Clear();
            txtSellingPrice.Clear();
            txtStockQuantity.Text = "0"; 
        }

        private void ToggleControls(bool enabled)
        {
            Control? detailsContainer = this.Controls.Find("groupBoxDetails", true).FirstOrDefault();
            Control? toolStrip = this.Controls.Find("toolStrip1", true).FirstOrDefault();

            if (detailsContainer != null) detailsContainer.Enabled = enabled;
             if (toolStrip != null) toolStrip.Enabled = true;
            
            this.Cursor = enabled ? Cursors.Default : Cursors.WaitCursor;
            
            if (enabled) {
                if (!cmbCategory.Enabled && cmbCategory.Items.Count > 0) cmbCategory.Enabled = true;
                if (!cmbSupplier.Enabled && cmbSupplier.Items.Count > 0) cmbSupplier.Enabled = true;
            }
        }

        private void UpdateButtonStates()
        {
            bool hasItems = productBindingSource.Count > 0;
            bool isItemSelected = productBindingSource.Position >= 0;

            tsbSave.Enabled = _isNew || (hasItems && isItemSelected);
            tsbDelete.Enabled = hasItems && isItemSelected && !_isNew;
            tsbFirst.Enabled = hasItems && isItemSelected && !_isNew && productBindingSource.Position > 0;
            tsbPrevious.Enabled = hasItems && isItemSelected && !_isNew && productBindingSource.Position > 0;
            tsbNext.Enabled = hasItems && isItemSelected && !_isNew && productBindingSource.Position < productBindingSource.Count - 1;
            tsbLast.Enabled = hasItems && isItemSelected && !_isNew && productBindingSource.Position < productBindingSource.Count - 1;
            tsbNew.Enabled = true;
            txtSearch.Enabled = true;
            tsbSearch.Enabled = true;
        }

        private void UpdateNavigationState()
        {
            bool hasItems = productBindingSource.Count > 0;
            bool isItemSelected = productBindingSource.Position >= 0;

            if (_isNew)
            {
                lblStatus.Text = "Adding new product...";
                groupBoxDetails.Enabled = true;
                tsbFirst.Enabled = false; tsbPrevious.Enabled = false; tsbNext.Enabled = false; tsbLast.Enabled = false;
            }
            else if (hasItems && isItemSelected)
            {
                lblStatus.Text = $"Record {productBindingSource.Position + 1} of {productBindingSource.Count}";
                groupBoxDetails.Enabled = true;
                tsbFirst.Enabled = productBindingSource.Position > 0;
                tsbPrevious.Enabled = productBindingSource.Position > 0;
                tsbNext.Enabled = productBindingSource.Position < productBindingSource.Count - 1;
                tsbLast.Enabled = productBindingSource.Position < productBindingSource.Count - 1;
            }
            else
            {
                lblStatus.Text = hasItems ? "No product selected." : "No products found.";
                groupBoxDetails.Enabled = false;
                tsbFirst.Enabled = false; tsbPrevious.Enabled = false; tsbNext.Enabled = false; tsbLast.Enabled = false;
                 if (!hasItems) ClearForm();
            }
            tsbSave.Enabled = _isNew || (hasItems && isItemSelected);
            tsbDelete.Enabled = hasItems && isItemSelected && !_isNew;
        }

        private void tsbNew_Click(object sender, EventArgs e)
        {
            _isNew = true;
            productBindingSource.SuspendBinding();
            ClearForm();
            groupBoxDetails.Enabled = true;
            txtProductName.Focus();
            UpdateNavigationState();
            UpdateButtonStates();
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
                    MessageBox.Show("Purchase Price must be a valid non-negative number or empty.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    txtPurchasePrice.Focus(); return;
                }
                purchasePrice = pp;
            }

            if(!_isNew)
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

                int? categoryId = (cmbCategory.SelectedValue != null && (int)cmbCategory.SelectedValue > 0) ? (int)cmbCategory.SelectedValue : (int?)null;
                int? supplierId = (cmbSupplier.SelectedValue != null && (int)cmbSupplier.SelectedValue > 0) ? (int)cmbSupplier.SelectedValue : (int?)null;

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
                    lblStatus.Text = success ? "Product added successfully." : "Failed to add product.";
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
                        lblStatus.Text = success ? "Product updated successfully." : "Failed to update product.";
                    }
                    else
                    {
                        MessageBox.Show("No product selected to update.", "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }

                if (success)
                {
                    _isNew = false;
                    int savedItemId = productToSave?.ProductID ?? -1;

                    if(wasNewItemInitially)
                    {
                        txtSearch.Clear();
                        await LoadDataAsync(null); 
                    }
                    else
                    {
                        await LoadDataAsync(txtSearch.Text);
                    }
                                        
                    if (savedItemId > 0) SelectProductById(savedItemId);
                }
            }
            catch (DbUpdateConcurrencyException)
            {
                MessageBox.Show("Record modified by another user. Reload and try again.", "Concurrency Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                lblStatus.Text = "Save failed due to concurrency.";
                await LoadDataAsync(txtSearch.Text);
            }
            catch (DbUpdateException dbEx)
            {
                MessageBox.Show($"Database error: {dbEx.InnerException?.Message ?? dbEx.Message}.", "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Database save error.";
            }
            catch (Exception ex)
            {
                MessageBox.Show($"An error occurred: {ex.Message}", "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Save error.";
            }
            finally
            {
                ToggleControls(true);
                // UpdateButtonStates(); // Called by LoadDataAsync
                // UpdateNavigationState(); // Called by LoadDataAsync
            }
        }

        private async void tsbDelete_Click(object sender, EventArgs e)
        {
            if (productBindingSource.Current is Product currentProduct)
            {
                var confirmResult = MessageBox.Show($"Delete product '{currentProduct.ProductName}' (ID: {currentProduct.ProductID})?",
                                                     "Confirm Delete", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);

                if (confirmResult == DialogResult.Yes)
                {
                    ToggleControls(false);
                    lblStatus.Text = "Deleting...";
                    try
                    {
                        bool success = await _productService.DeleteProductAsync(currentProduct.ProductID);
                        
                        if (success)
                        {
                             lblStatus.Text = "Product deleted.";
                            await LoadDataAsync(txtSearch.Text.Trim());
                        }
                        else
                        {
                            MessageBox.Show("Failed to delete product. It might be part of an order.", "Delete Failed", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                            lblStatus.Text = "Delete failed.";
                            await LoadDataAsync(txtSearch.Text.Trim());
                        }
                    }
                    catch (DbUpdateException dbEx)
                    {
                        MessageBox.Show($"Database error: {dbEx.InnerException?.Message ?? dbEx.Message}. Cannot delete product in use.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        lblStatus.Text = "Database delete error.";
                        await LoadDataAsync(txtSearch.Text.Trim());
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"An error occurred: {ex.Message}", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        lblStatus.Text = "Delete error.";
                        await LoadDataAsync(txtSearch.Text.Trim());
                    }
                    finally
                    {
                        ToggleControls(true);
                    }
                }
            }
            else
            {
                MessageBox.Show("No product selected.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private async void PerformSearch() => await LoadDataAsync(txtSearch.Text.Trim());
        private void tsbSearch_Click(object sender, EventArgs e) => PerformSearch();
        private void txtSearch_KeyDown(object sender, KeyEventArgs e) { if (e.KeyCode == Keys.Enter) { PerformSearch(); e.SuppressKeyPress = true; } }
        private void tsbFirst_Click(object sender, EventArgs e) => productBindingSource.MoveFirst();
        private void tsbPrevious_Click(object sender, EventArgs e) => productBindingSource.MovePrevious();
        private void tsbNext_Click(object sender, EventArgs e) => productBindingSource.MoveNext();
        private void tsbLast_Click(object sender, EventArgs e) => productBindingSource.MoveLast();

        private void productBindingSource_CurrentChanged(object sender, EventArgs e)
        {
            if (!_isNew) 
            { 
                if(productBindingSource.Current == null)
                {
                    ClearForm();
                }
                UpdateButtonStates(); 
                UpdateNavigationState(); 
            }
        }

        private void SelectProductById(int productId)
        {
            if (productId <= 0) return;
            if (productBindingSource.DataSource is List<Product> products)
            {
                int index = products.FindIndex(prod => prod.ProductID == productId);
                if (index != -1)
                {
                    productBindingSource.Position = index;
                }
            }
        }
    }
}
```
Finally, `frmOrders`.

**`frmOrders.Designer.cs` (Updated)**
```csharp
using System;
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;
using Store.Data.Models; 

namespace Store.Forms
{
    partial class frmOrders
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
            ComponentResourceManager resources = new ComponentResourceManager(typeof(frmOrders));
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
            orderBindingSource = new BindingSource(components);
            groupBoxDetails = new GroupBox();
            tableLayoutPanelDetails = new TableLayoutPanel();
            lblOrderID = new Label();
            txtOrderID = new TextBox();
            lblCustomer = new Label();
            cmbCustomer = new ComboBox();
            lblEmployee = new Label();
            cmbEmployee = new ComboBox();
            lblOrderDate = new Label();
            dtpOrderDate = new DateTimePicker();
            lblTotalAmount = new Label();
            txtTotalAmount = new TextBox();
            btnViewDetails = new Button();
            toolStrip1.SuspendLayout();
            statusStrip1.SuspendLayout();
            ((ISupportInitialize)orderBindingSource).BeginInit();
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
            tsbNew.Size = new Size(120, 28); // Adjusted
            tsbNew.Text = "New Order";
            tsbNew.ToolTipText = "Add New Order (Ctrl+N)";
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
            tsbDelete.Size = new Size(135, 28); // Adjusted
            tsbDelete.Text = "Delete Order";
            tsbDelete.ToolTipText = "Delete Selected Order (Del)";
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
            txtSearch.ToolTipText = "Search by Order ID or Customer Name";
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
            tsbSearch.ToolTipText = "Search Orders";
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
            // orderBindingSource
            // 
            orderBindingSource.DataSource = typeof(Order);
            orderBindingSource.CurrentChanged += orderBindingSource_CurrentChanged;
            // 
            // groupBoxDetails
            // 
            groupBoxDetails.Controls.Add(tableLayoutPanelDetails);
            groupBoxDetails.Dock = DockStyle.Fill;
            groupBoxDetails.Font = new Font("Segoe UI Semibold", 10F, FontStyle.Bold);
            groupBoxDetails.ForeColor = Color.FromArgb(55, 55, 55);
            groupBoxDetails.Location = new Point(0, 46); // Adjusted
            groupBoxDetails.Margin = new Padding(10);
            groupBoxDetails.Name = "groupBoxDetails";
            groupBoxDetails.Padding = new Padding(20);
            groupBoxDetails.Size = new Size(1118, 396); // Adjusted
            groupBoxDetails.TabIndex = 1;
            groupBoxDetails.TabStop = false;
            groupBoxDetails.Text = "Order Header"; // Changed from "Order Details" to avoid confusion with line items
            // 
            // tableLayoutPanelDetails
            // 
            tableLayoutPanelDetails.ColumnCount = 2;
            tableLayoutPanelDetails.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 150F));
            tableLayoutPanelDetails.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            tableLayoutPanelDetails.Controls.Add(lblOrderID, 0, 0);
            tableLayoutPanelDetails.Controls.Add(txtOrderID, 1, 0);
            tableLayoutPanelDetails.Controls.Add(lblCustomer, 0, 1);
            tableLayoutPanelDetails.Controls.Add(cmbCustomer, 1, 1);
            tableLayoutPanelDetails.Controls.Add(lblEmployee, 0, 2);
            tableLayoutPanelDetails.Controls.Add(cmbEmployee, 1, 2);
            tableLayoutPanelDetails.Controls.Add(lblOrderDate, 0, 3);
            tableLayoutPanelDetails.Controls.Add(dtpOrderDate, 1, 3);
            tableLayoutPanelDetails.Controls.Add(lblTotalAmount, 0, 4);
            tableLayoutPanelDetails.Controls.Add(txtTotalAmount, 1, 4);
            tableLayoutPanelDetails.Controls.Add(btnViewDetails, 1, 5);
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
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Absolute, 55F));
            tableLayoutPanelDetails.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableLayoutPanelDetails.Size = new Size(1078, 333); // Adjusted
            tableLayoutPanelDetails.TabIndex = 0;
            // 
            // lblOrderID
            // 
            lblOrderID.Anchor = AnchorStyles.Left;
            lblOrderID.AutoSize = true;
            lblOrderID.Font = new Font("Segoe UI", 10F);
            lblOrderID.ForeColor = Color.FromArgb(80, 80, 80);
            lblOrderID.Location = new Point(3, 11);
            lblOrderID.Name = "lblOrderID";
            lblOrderID.Size = new Size(80, 23);
            lblOrderID.TabIndex = 0;
            lblOrderID.Text = "Order ID:";
            // 
            // txtOrderID
            // 
            txtOrderID.Anchor = AnchorStyles.Left; // Removed Right Anchor
            txtOrderID.BackColor = Color.FromArgb(245, 245, 245);
            txtOrderID.BorderStyle = BorderStyle.FixedSingle;
            txtOrderID.Font = new Font("Segoe UI", 10F);
            txtOrderID.ForeColor = Color.FromArgb(100, 100, 100);
            txtOrderID.Location = new Point(153, 7);
            txtOrderID.Margin = new Padding(3, 4, 10, 4);
            txtOrderID.Name = "txtOrderID";
            txtOrderID.ReadOnly = true;
            txtOrderID.Size = new Size(200, 30); // Fixed width
            txtOrderID.TabIndex = 1;
            txtOrderID.TabStop = false;
            // 
            // lblCustomer
            // 
            lblCustomer.Anchor = AnchorStyles.Left;
            lblCustomer.AutoSize = true;
            lblCustomer.Font = new Font("Segoe UI", 10F);
            lblCustomer.ForeColor = Color.FromArgb(80, 80, 80);
            lblCustomer.Location = new Point(3, 56);
            lblCustomer.Name = "lblCustomer";
            lblCustomer.Size = new Size(88, 23);
            lblCustomer.TabIndex = 2;
            lblCustomer.Text = "Customer:";
            // 
            // cmbCustomer
            // 
            cmbCustomer.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            cmbCustomer.DropDownStyle = ComboBoxStyle.DropDownList;
            cmbCustomer.Font = new Font("Segoe UI", 10F);
            cmbCustomer.ForeColor = Color.FromArgb(50, 50, 50);
            cmbCustomer.FormattingEnabled = true;
            cmbCustomer.Location = new Point(153, 53);
            cmbCustomer.Margin = new Padding(3, 4, 10, 4);
            cmbCustomer.Name = "cmbCustomer";
            cmbCustomer.Size = new Size(915, 31);
            cmbCustomer.TabIndex = 0;
            // 
            // lblEmployee
            // 
            lblEmployee.Anchor = AnchorStyles.Left;
            lblEmployee.AutoSize = true;
            lblEmployee.Font = new Font("Segoe UI", 10F);
            lblEmployee.ForeColor = Color.FromArgb(80, 80, 80);
            lblEmployee.Location = new Point(3, 101);
            lblEmployee.Name = "lblEmployee";
            lblEmployee.Size = new Size(88, 23);
            lblEmployee.TabIndex = 4;
            lblEmployee.Text = "Employee:";
            // 
            // cmbEmployee
            // 
            cmbEmployee.Anchor = AnchorStyles.Left | AnchorStyles.Right;
            cmbEmployee.DropDownStyle = ComboBoxStyle.DropDownList;
            cmbEmployee.Font = new Font("Segoe UI", 10F);
            cmbEmployee.ForeColor = Color.FromArgb(50, 50, 50);
            cmbEmployee.FormattingEnabled = true;
            cmbEmployee.Location = new Point(153, 98);
            cmbEmployee.Margin = new Padding(3, 4, 10, 4);
            cmbEmployee.Name = "cmbEmployee";
            cmbEmployee.Size = new Size(915, 31);
            cmbEmployee.TabIndex = 1;
            // 
            // lblOrderDate
            // 
            lblOrderDate.Anchor = AnchorStyles.Left;
            lblOrderDate.AutoSize = true;
            lblOrderDate.Font = new Font("Segoe UI", 10F);
            lblOrderDate.ForeColor = Color.FromArgb(80, 80, 80);
            lblOrderDate.Location = new Point(3, 146);
            lblOrderDate.Name = "lblOrderDate";
            lblOrderDate.Size = new Size(99, 23);
            lblOrderDate.TabIndex = 6;
            lblOrderDate.Text = "Order Date:";
            // 
            // dtpOrderDate
            // 
            dtpOrderDate.Anchor = AnchorStyles.Left;
            dtpOrderDate.CustomFormat = "yyyy-MM-dd HH:mm";
            dtpOrderDate.Font = new Font("Segoe UI", 10F);
            dtpOrderDate.Format = DateTimePickerFormat.Custom;
            dtpOrderDate.Location = new Point(153, 142);
            dtpOrderDate.Margin = new Padding(3, 4, 10, 4);
            dtpOrderDate.Name = "dtpOrderDate";
            dtpOrderDate.Size = new Size(250, 30);
            dtpOrderDate.TabIndex = 2;
            // 
            // lblTotalAmount
            // 
            lblTotalAmount.Anchor = AnchorStyles.Left;
            lblTotalAmount.AutoSize = true;
            lblTotalAmount.Font = new Font("Segoe UI", 10F);
            lblTotalAmount.ForeColor = Color.FromArgb(80, 80, 80);
            lblTotalAmount.Location = new Point(3, 191);
            lblTotalAmount.Name = "lblTotalAmount";
            lblTotalAmount.Size = new Size(117, 23);
            lblTotalAmount.TabIndex = 8;
            lblTotalAmount.Text = "Total Amount:";
            // 
            // txtTotalAmount
            // 
            txtTotalAmount.Anchor = AnchorStyles.Left; // Removed Right Anchor
            txtTotalAmount.BackColor = Color.FromArgb(245, 245, 245);
            txtTotalAmount.BorderStyle = BorderStyle.FixedSingle;
            txtTotalAmount.Font = new Font("Segoe UI", 10F, FontStyle.Bold);
            txtTotalAmount.ForeColor = Color.FromArgb(0, 100, 0);
            txtTotalAmount.Location = new Point(153, 187);
            txtTotalAmount.Margin = new Padding(3, 4, 10, 4);
            txtTotalAmount.Name = "txtTotalAmount";
            txtTotalAmount.ReadOnly = true;
            txtTotalAmount.Size = new Size(200, 30); // Fixed width
            txtTotalAmount.TabIndex = 9;
            txtTotalAmount.TabStop = false;
            txtTotalAmount.TextAlign = HorizontalAlignment.Right;
            // 
            // btnViewDetails
            // 
            btnViewDetails.Anchor = AnchorStyles.Left;
            btnViewDetails.Font = new Font("Segoe UI", 10F);
            btnViewDetails.Location = new Point(153, 233);
            btnViewDetails.Margin = new Padding(3, 8, 3, 8);
            btnViewDetails.Name = "btnViewDetails";
            btnViewDetails.Size = new Size(200, 39);
            btnViewDetails.TabIndex = 3;
            btnViewDetails.Text = "&View/Edit Details...";
            btnViewDetails.UseVisualStyleBackColor = true;
            btnViewDetails.Click += btnViewDetails_Click;
            // 
            // frmOrders
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
            MinimumSize = new Size(700, 450);
            Name = "frmOrders";
            Text = "Manage Orders";
            Load += frmOrders_Load;
            toolStrip1.ResumeLayout(false);
            toolStrip1.PerformLayout();
            statusStrip1.ResumeLayout(false);
            statusStrip1.PerformLayout();
            ((ISupportInitialize)orderBindingSource).EndInit();
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
        private BindingSource orderBindingSource;
        private GroupBox groupBoxDetails;
        private TableLayoutPanel tableLayoutPanelDetails;
        private Label lblOrderID;
        private TextBox txtOrderID;
        private Label lblCustomer;
        private ComboBox cmbCustomer;
        private Label lblEmployee;
        private ComboBox cmbEmployee;
        private Label lblOrderDate;
        private DateTimePicker dtpOrderDate;
        private Label lblTotalAmount;
        private TextBox txtTotalAmount;
        private Button btnViewDetails;
    }
}
```

**`frmOrders.cs` (Updated)**
```csharp
using Microsoft.EntityFrameworkCore;
using Store.Data.Models;
using Store.Services; 
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using Microsoft.Extensions.DependencyInjection; // For DI to open frmOrderDetails

namespace Store.Forms
{
    public partial class frmOrders : Form
    {
        private readonly OrderService _orderService;
        private readonly CustomerService _customerService;
        private readonly EmployeeService _employeeService;
        private readonly IServiceProvider _serviceProvider; // For DI
        private bool _isNew = false;

        public frmOrders(OrderService orderService, CustomerService customerService, EmployeeService employeeService, IServiceProvider serviceProvider)
        {
            InitializeComponent();
            _orderService = orderService;
            _customerService = customerService; 
            _employeeService = employeeService; 
            _serviceProvider = serviceProvider;
        }

        private async void frmOrders_Load(object sender, EventArgs e)
        {
            await LoadComboBoxesAsync();
            await LoadDataAsync();
            SetupBindings();
            UpdateButtonStates();
            UpdateNavigationState();
        }

        private async Task LoadComboBoxesAsync()
        {
            try
            {
                var customers = await _customerService.GetAllCustomersAsync();
                var employees = await _employeeService.GetAllEmployeesAsync();

                // Add "(None)" option if not already present
                if (customers.All(c => c.CustomerID != 0)) {
                    customers.Insert(0, new Customer { CustomerID = 0, FirstName = "(Select", LastName = "Customer)" });
                }
                if (employees.All(e => e.EmployeeID != 0)) {
                     employees.Insert(0, new Employee { EmployeeID = 0, FirstName = "(Select", LastName = "Employee)" });
                }
               
                cmbCustomer.DataSource = customers;
                cmbCustomer.ValueMember = "CustomerID";
                cmbCustomer.Format += (s, e) => 
                {
                    if (e.ListItem is Customer c)
                    {
                        e.Value = (c.CustomerID == 0) ? "(Select Customer)" : $"{c.FirstName} {c.LastName}";
                    }
                };
                if(cmbCustomer.Items.Count > 0) cmbCustomer.SelectedIndex = 0;


                cmbEmployee.DataSource = employees;
                cmbEmployee.ValueMember = "EmployeeID";
                cmbEmployee.Format += (s, e) => 
                {
                    if (e.ListItem is Employee emp)
                    {
                        e.Value = (emp.EmployeeID == 0) ? "(Select Employee)" : $"{emp.FirstName} {emp.LastName}";
                    }
                };
                if(cmbEmployee.Items.Count > 0) cmbEmployee.SelectedIndex = 0;
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading customers/employees for dropdowns: {ex.Message}", "Dropdown Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                cmbCustomer.Enabled = false;
                cmbEmployee.Enabled = false;
            }
        }


        private async Task LoadDataAsync(string? searchTerm = null) 
        {
            ToggleControls(false);
            lblStatus.Text = "Loading orders...";
            try
            {
                List<Order> orders;
                if (string.IsNullOrWhiteSpace(searchTerm))
                {
                    orders = await _orderService.GetAllOrdersAsync();
                }
                else
                {
                    // Assuming OrderService.SearchOrdersAsync handles various search criteria
                    orders = await _orderService.SearchOrdersAsync(searchTerm);
                    lblStatus.Text = $"Found {orders.Count} matching '{searchTerm}'.";
                }

                orderBindingSource.DataSource = orders;
                orderBindingSource.ResetBindings(false);

                if (orders.Count == 0 && string.IsNullOrWhiteSpace(searchTerm))
                {
                    lblStatus.Text = "No orders found. Click 'New' to add one.";
                    ClearForm();
                }
                else if (orders.Count > 0)
                {
                    lblStatus.Text = $"Displaying {orders.Count} orders.";
                    if (orderBindingSource.Position < 0) orderBindingSource.MoveFirst();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading orders: {ex.Message}", "Loading Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Error loading data.";
            }
            finally
            {
                // _isNew = false; // Moved to tsbSave_Click success path
                UpdateButtonStates();
                UpdateNavigationState();
                ToggleControls(true);
            }
        }

        private void SetupBindings()
        {
            txtOrderID.DataBindings.Clear();
            cmbCustomer.DataBindings.Clear();
            cmbEmployee.DataBindings.Clear();
            dtpOrderDate.DataBindings.Clear();
            txtTotalAmount.DataBindings.Clear();

            txtOrderID.DataBindings.Add("Text", orderBindingSource, "OrderID", true, DataSourceUpdateMode.OnPropertyChanged);
            cmbCustomer.DataBindings.Add("SelectedValue", orderBindingSource, "CustomerID", true, DataSourceUpdateMode.OnValidation, 0); 
            cmbEmployee.DataBindings.Add("SelectedValue", orderBindingSource, "EmployeeID", true, DataSourceUpdateMode.OnValidation, 0); 
            dtpOrderDate.DataBindings.Add("Value", orderBindingSource, "OrderDate", true, DataSourceUpdateMode.OnPropertyChanged);
            txtTotalAmount.DataBindings.Add("Text", orderBindingSource, "TotalAmount", true, DataSourceUpdateMode.OnPropertyChanged, DBNull.Value, "C2"); 
        }

        private void ClearForm()
        {
            txtOrderID.DataBindings.Clear();
            cmbCustomer.DataBindings.Clear();
            cmbEmployee.DataBindings.Clear();
            dtpOrderDate.DataBindings.Clear();
            txtTotalAmount.DataBindings.Clear();

            txtOrderID.Clear();
            if (cmbCustomer.Items.Count > 0) cmbCustomer.SelectedIndex = 0; // Select "(Select Customer)"
            if (cmbEmployee.Items.Count > 0) cmbEmployee.SelectedIndex = 0; // Select "(Select Employee)"
            dtpOrderDate.Value = DateTime.Now; 
            txtTotalAmount.Clear();
        }

        private void ToggleControls(bool enabled)
        {
            Control? detailsContainer = this.Controls.Find("groupBoxDetails", true).FirstOrDefault();
            Control? toolStrip = this.Controls.Find("toolStrip1", true).FirstOrDefault();

            if (detailsContainer != null) detailsContainer.Enabled = enabled;
             if (toolStrip != null) toolStrip.Enabled = true;
            
            this.Cursor = enabled ? Cursors.Default : Cursors.WaitCursor;
            
            if (enabled) {
                if (!cmbCustomer.Enabled && cmbCustomer.Items.Count > 0) cmbCustomer.Enabled = true;
                if (!cmbEmployee.Enabled && cmbEmployee.Items.Count > 0) cmbEmployee.Enabled = true;
            }
        }

        private void UpdateButtonStates()
        {
            bool hasItems = orderBindingSource.Count > 0;
            bool isItemSelected = orderBindingSource.Position >= 0;

            tsbSave.Enabled = _isNew || (hasItems && isItemSelected);
            tsbDelete.Enabled = hasItems && isItemSelected && !_isNew;
            
            tsbFirst.Enabled = hasItems && isItemSelected && !_isNew && orderBindingSource.Position > 0;
            tsbPrevious.Enabled = hasItems && isItemSelected && !_isNew && orderBindingSource.Position > 0;
            tsbNext.Enabled = hasItems && isItemSelected && !_isNew && orderBindingSource.Position < orderBindingSource.Count - 1;
            tsbLast.Enabled = hasItems && isItemSelected && !_isNew && orderBindingSource.Position < orderBindingSource.Count - 1;
            
            tsbNew.Enabled = true;
            txtSearch.Enabled = true;
            tsbSearch.Enabled = true;
            btnViewDetails.Enabled = hasItems && isItemSelected && !_isNew; // Enable if an existing order is selected
        }

        private void UpdateNavigationState()
        {
            bool hasItems = orderBindingSource.Count > 0;
            bool isItemSelected = orderBindingSource.Position >= 0;

            if (_isNew)
            {
                lblStatus.Text = "Adding new order...";
                groupBoxDetails.Enabled = true;
                tsbFirst.Enabled = false; tsbPrevious.Enabled = false; tsbNext.Enabled = false; tsbLast.Enabled = false;
                cmbCustomer.Enabled = true;
                cmbEmployee.Enabled = true;
                dtpOrderDate.Enabled = true;
                txtTotalAmount.ReadOnly = true; 
                btnViewDetails.Enabled = false; // Cannot view details for an unsaved new order
            }
            else if (hasItems && isItemSelected)
            {
                lblStatus.Text = $"Record {orderBindingSource.Position + 1} of {orderBindingSource.Count}";
                groupBoxDetails.Enabled = true;
                tsbFirst.Enabled = orderBindingSource.Position > 0;
                tsbPrevious.Enabled = orderBindingSource.Position > 0;
                tsbNext.Enabled = orderBindingSource.Position < orderBindingSource.Count - 1;
                tsbLast.Enabled = orderBindingSource.Position < orderBindingSource.Count - 1;
                cmbCustomer.Enabled = true;
                cmbEmployee.Enabled = true;
                dtpOrderDate.Enabled = true;
                txtTotalAmount.ReadOnly = true;
                btnViewDetails.Enabled = true;
            }
            else
            {
                lblStatus.Text = hasItems ? "No order selected." : "No orders found.";
                groupBoxDetails.Enabled = false;
                tsbFirst.Enabled = false; tsbPrevious.Enabled = false; tsbNext.Enabled = false; tsbLast.Enabled = false;
                btnViewDetails.Enabled = false;
                if (!hasItems) ClearForm();
            }
            tsbSave.Enabled = _isNew || (hasItems && isItemSelected);
            tsbDelete.Enabled = hasItems && isItemSelected && !_isNew;
        }

        private void tsbNew_Click(object sender, EventArgs e)
        {
            _isNew = true;
            orderBindingSource.SuspendBinding();
            ClearForm();
            groupBoxDetails.Enabled = true;
            cmbCustomer.Focus(); 
            UpdateNavigationState();
            UpdateButtonStates();
        }

        private async void tsbSave_Click(object sender, EventArgs e)
        {
            if (dtpOrderDate.Value > DateTime.Now.AddDays(1)) 
            {
                MessageBox.Show("Order Date cannot be in the future.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                dtpOrderDate.Focus(); return;
            }

            if(!_isNew)
            {
                 orderBindingSource.EndEdit();
            }

            ToggleControls(false);
            lblStatus.Text = "Saving...";

            try
            {
                bool success = false;
                Order? orderToSave = null;
                bool wasNewItemInitially = _isNew;

                int? customerId = (cmbCustomer.SelectedValue != null && (int)cmbCustomer.SelectedValue > 0) ? (int)cmbCustomer.SelectedValue : (int?)null;
                int? employeeId = (cmbEmployee.SelectedValue != null && (int)cmbEmployee.SelectedValue > 0) ? (int)cmbEmployee.SelectedValue : (int?)null;

                if (_isNew)
                {
                    orderToSave = new Order
                    {
                        CustomerID = customerId,
                        EmployeeID = employeeId,
                        OrderDate = dtpOrderDate.Value,
                        // TotalAmount will be calculated based on OrderDetails later or by a trigger/service logic
                    };
                    success = await _orderService.AddOrderAsync(orderToSave);
                    lblStatus.Text = success ? "Order added successfully." : "Failed to add order.";
                }
                else 
                {
                    if (orderBindingSource.Current is Order currentOrder)
                    {
                        currentOrder.CustomerID = customerId;
                        currentOrder.EmployeeID = employeeId;
                        currentOrder.OrderDate = dtpOrderDate.Value;
                        
                        orderToSave = currentOrder;
                        success = await _orderService.UpdateOrderAsync(currentOrder);
                        lblStatus.Text = success ? "Order updated successfully." : "Failed to update order.";
                    }
                    else
                    {
                        MessageBox.Show("No order selected to update.", "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }

                if (success)
                {
                    _isNew = false;
                    int savedItemId = orderToSave?.OrderID ?? -1;

                    if(wasNewItemInitially)
                    {
                        txtSearch.Clear();
                        await LoadDataAsync(null);
                    }
                    else
                    {
                         await LoadDataAsync(txtSearch.Text);
                    }
                                       
                    if (savedItemId > 0) SelectOrderById(savedItemId);

                    // If it was a new order and successfully saved, prompt to add details
                    if (wasNewItemInitially && savedItemId > 0)
                    {
                        var result = MessageBox.Show("Order created. Do you want to add items (details) to this order now?", 
                                                     "Add Order Details", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
                        if (result == DialogResult.Yes)
                        {
                            OpenOrderDetailsForm(savedItemId);
                        }
                    }
                }
            }
            catch (DbUpdateConcurrencyException)
            {
                MessageBox.Show("Record modified by another user. Reload and try again.", "Concurrency Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                lblStatus.Text = "Save failed due to concurrency.";
                await LoadDataAsync(txtSearch.Text);
            }
            catch (DbUpdateException dbEx)
            {
                MessageBox.Show($"Database error: {dbEx.InnerException?.Message ?? dbEx.Message}.", "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Database save error.";
            }
            catch (Exception ex)
            {
                MessageBox.Show($"An error occurred: {ex.Message}", "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                lblStatus.Text = "Save error.";
            }
            finally
            {
                ToggleControls(true);
                // UpdateButtonStates(); // Called by LoadDataAsync
                // UpdateNavigationState(); // Called by LoadDataAsync
            }
        }

        private async void tsbDelete_Click(object sender, EventArgs e)
        {
            if (orderBindingSource.Current is Order currentOrder)
            {
                var confirmResult = MessageBox.Show($"Delete Order ID: {currentOrder.OrderID} (Date: {currentOrder.OrderDate:d})?\nThis will also delete all associated Order Details!",
                                                     "Confirm Delete", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);

                if (confirmResult == DialogResult.Yes)
                {
                    ToggleControls(false);
                    lblStatus.Text = "Deleting...";
                    try
                    {
                        bool success = await _orderService.DeleteOrderAsync(currentOrder.OrderID);
                        
                        if (success)
                        {
                            lblStatus.Text = "Order deleted.";
                            await LoadDataAsync(txtSearch.Text.Trim()); 
                        }
                        else
                        {
                            MessageBox.Show("Failed to delete order. Ensure all related data (like payments if any) is handled.", "Delete Failed", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                            lblStatus.Text = "Delete failed.";
                             await LoadDataAsync(txtSearch.Text.Trim());
                        }
                    }
                    catch (DbUpdateException dbEx) 
                    {
                        MessageBox.Show($"Database error: {dbEx.InnerException?.Message ?? dbEx.Message}. Ensure order is not referenced elsewhere.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        lblStatus.Text = "Database delete error.";
                        await LoadDataAsync(txtSearch.Text.Trim());
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"An error occurred: {ex.Message}", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        lblStatus.Text = "Delete error.";
                        await LoadDataAsync(txtSearch.Text.Trim());
                    }
                    finally
                    {
                        ToggleControls(true);
                    }
                }
            }
            else
            {
                MessageBox.Show("No order selected.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private async void PerformSearch() => await LoadDataAsync(txtSearch.Text.Trim());
        private void tsbSearch_Click(object sender, EventArgs e) => PerformSearch();
        private void txtSearch_KeyDown(object sender, KeyEventArgs e) { if (e.KeyCode == Keys.Enter) { PerformSearch(); e.SuppressKeyPress = true; } }
        private void tsbFirst_Click(object sender, EventArgs e) => orderBindingSource.MoveFirst();
        private void tsbPrevious_Click(object sender, EventArgs e) => orderBindingSource.MovePrevious();
        private void tsbNext_Click(object sender, EventArgs e) => orderBindingSource.MoveNext();
        private void tsbLast_Click(object sender, EventArgs e) => orderBindingSource.MoveLast();

        private async void orderBindingSource_CurrentChanged(object sender, EventArgs e) // Made async
        {
            if (!_isNew) 
            { 
                 if(orderBindingSource.Current == null)
                {
                    ClearForm();
                }
                else
                {
                    // When current order changes, refresh its total amount from the database
                    // as details might have been changed from frmOrderDetails
                    if (orderBindingSource.Current is Order currentOrder && currentOrder.OrderID > 0)
                    {
                        decimal newTotal = await _orderService.GetOrderTotalAmountAsync(currentOrder.OrderID);
                        currentOrder.TotalAmount = newTotal; // Update the model object
                        // txtTotalAmount.Text = newTotal.ToString("C2"); // Update bound control
                        // ResetBindings is safer if other properties might have changed via other means
                        orderBindingSource.ResetBindings(false); 
                    }
                }
                UpdateButtonStates(); 
                UpdateNavigationState(); 
            }
        }

        private void SelectOrderById(int orderId)
        {
            if (orderId <= 0) return;
            if (orderBindingSource.DataSource is List<Order> orders)
            {
                int index = orders.FindIndex(ord => ord.OrderID == orderId);
                if (index != -1)
                {
                    orderBindingSource.Position = index;
                }
            }
        }
        
        private void btnViewDetails_Click(object sender, EventArgs e)
        {
            if (orderBindingSource.Current is Order currentOrder && currentOrder.OrderID > 0)
            {
                OpenOrderDetailsForm(currentOrder.OrderID);
            }
            else if (_isNew)
            {
                 MessageBox.Show("Please save the new order first before adding details.", "Save Order", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            else
            {
                MessageBox.Show("No order selected to view details.", "View Details", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        private async void OpenOrderDetailsForm(int orderId)
        {
            // Use DI to create frmOrderDetails if it's registered
            var orderDetailService = _serviceProvider.GetRequiredService<OrderDetailService>();
            var productService = _serviceProvider.GetRequiredService<ProductService>();
            // The OrderService is already available via _orderService

            using (var frmDetails = new frmOrderDetails(orderDetailService, _orderService, productService, orderId))
            {
                frmDetails.ShowDialog(this); // Show as a dialog, modal to this form
            }

            // After frmOrderDetails closes, the order total might have changed.
            // Refresh the current order's total amount.
            if (orderBindingSource.Current is Order currentOrderAfterDetails && currentOrderAfterDetails.OrderID == orderId)
            {
                decimal newTotal = await _orderService.GetOrderTotalAmountAsync(orderId);
                currentOrderAfterDetails.TotalAmount = newTotal;
                orderBindingSource.ResetCurrentItem(); // This should refresh bound controls for the current item
            }
        }
    }
}
```

This completes all the forms you provided. Remember to:
1.  **Add Image Resources:** Crucial for the icons on `ToolStripButton`s.
2.  **Dependency Injection for `frmOrderDetails`:** The `frmOrders.cs` now includes a placeholder for using `IServiceProvider` to open `frmOrderDetails`. You'll need to ensure your `Program.cs` or startup logic correctly registers `frmOrderDetails` and its dependencies if you want to use this DI approach. Otherwise, you'll revert to direct instantiation (`new frmOrderDetails(...)`).
3.  **`FullName` Properties:** Check if `Customer` and `Employee` models have `FullName` or adjust combobox display.
4.  **`SearchOrdersAsync` and `SearchOrderDetailsByProductNameAsync`:** These methods in `OrderService` and `OrderDetailService` respectively were assumed to exist. You'll need to implement them if you want the search functionality in `frmOrders` and `frmOrderDetails` to work beyond very basic ID search.
5.  **`GetOrderTotalAmountAsync`:** The `frmOrders` form now calls this method on `OrderService` to refresh the total when the current order changes. Ensure this method exists and correctly calculates the total from `OrderDetails`.

Test thoroughly after integrating these changes!

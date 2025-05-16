using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ArcGIS.Core.CIM;
using ArcGIS.Core.Data;
using ArcGIS.Core.Geometry;
using ArcGIS.Desktop.Catalog;
using ArcGIS.Desktop.Core;
using ArcGIS.Desktop.Editing;
using ArcGIS.Desktop.Extensions;
using ArcGIS.Desktop.Framework;
using ArcGIS.Desktop.Framework.Contracts;
using ArcGIS.Desktop.Framework.Dialogs;
using ArcGIS.Desktop.Framework.Threading.Tasks;
using ArcGIS.Desktop.Layouts;
using ArcGIS.Desktop.Mapping;
using ArcGIS.Desktop.KnowledgeGraph;
using ArcGIS.Desktop.Core.Geoprocessing;

namespace MiningSites
{
    internal class OpenIntersectTool : Button
    {
        protected override void OnClick()
        {
            try
            {
                // launch the Intersect tool UI dialog
                QueuedTask.Run(() =>
                {
                    // name of the tool
                    string toolName = "analysis.Intersect";
                    Geoprocessing.OpenToolDialog(toolName, null);
                });
            }
            catch (Exception ex)
            {
                // handle any unexpected errors
                MessageBox.Show($"Error: {ex.Message}\n{ex.StackTrace}");
            }
        }
    }
}
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
using System.Diagnostics;
using ActiproSoftware.Windows.Extensions;
using ArcGIS.Desktop.Core.Geoprocessing;
using System.Windows;

namespace MiningSites
{
    internal class BufferSelectedFeatures : Button
    {
        protected override async void OnClick()
        {
            // run buffer process when the button is clicked
            bool bufferSuccessful = await QueuedTask.Run(() => BufferSelectedFeaturesAsync());
        }

        private async Task<bool> BufferSelectedFeaturesAsync()
        {
            var mapView = MapView.Active;
            if (mapView == null)
                return false;

            // Get selected features in the active FeatureLayer
            var layers = mapView.Map.Layers;
            var selectedFeatures = new List<Geometry>();
            string selectedFeatureLayer = null;

            foreach (var layer in layers)
            {
                if (layer is FeatureLayer featureLayer)
                {
                    // Get selected features from the layer
                    var selected = await QueuedTask.Run(() => featureLayer.GetSelection());
                    var objectIds = await QueuedTask.Run(() => selected.GetObjectIDs());

                    if (objectIds.Count == 0)
                        continue;

                    // Ensure the feature layer is selected
                    selectedFeatureLayer = featureLayer.Name;

                    // Retrieve the BUFF_DIST value for the selected features
                    var fieldIndex = featureLayer.GetTable().GetDefinition().FindField("BUFF_DIST");
                    if (fieldIndex == -1)
                        continue;

                    // Get the BUFF_DIST value for each selected feature
                    foreach (var objectId in objectIds)
                    {
                        using (var rowCursor = featureLayer.GetTable().Search(new QueryFilter
                        {
                            ObjectIDs = new List<long> { objectId }
                        }))
                        {
                            while (rowCursor.MoveNext())
                            {
                                var row = rowCursor.Current;
                                var bufferDistance = row[fieldIndex] as short?;

                                // convert from short to double
                                double bufferDistanceValue = Convert.ToDouble(bufferDistance.Value);

                                // use the buffer distance in the Geoprocessing tool
                                await PerformBufferOperation(featureLayer, bufferDistanceValue);
                            }
                        }
                    }
                    return true;
                }
            }

            ArcGIS.Desktop.Framework.Dialogs.MessageBox.Show("No selected features found.", "Error", MessageBoxButton.OK, MessageBoxImage.Information);
            return false;
        }

        private async Task PerformBufferOperation(FeatureLayer featureLayer, double bufferDistance)
        {
            var mapView = MapView.Active;
            if (mapView == null)
                return;

            try
            {
                // use Geoprocessing tool to create the buffer
                var toolName = "analysis.Buffer";

                // set the input parameters for the tool
                var inputLayer = featureLayer.Name;
                var outputFeatureClass = @"C:\Documents\COGS\WIN2025\GISY6048\AddinsTesting\AddinsTesting.gdb\AreaOfInterest";
                var bufferDistanceStr = $"{bufferDistance} Meters";

                // prepare the parameters for the GP tool
                var values = Geoprocessing.MakeValueArray(inputLayer, outputFeatureClass, bufferDistanceStr,
                                                        "FULL", "ROUND", "NONE", null, "PLANAR");

                // execute the tool asynchronously
                var gpResult = await Geoprocessing.ExecuteToolAsync(toolName, values);
            }
            catch (Exception)
            {
                // error message if buffer fails
                ArcGIS.Desktop.Framework.Dialogs.MessageBox.Show("Buffer process has failed.", "Error", MessageBoxButton.OK, MessageBoxImage.Information);
            }
        }
    }
}
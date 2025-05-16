using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
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

namespace MiningSites
{
    internal class MiningSitesComboBox : ComboBox 
    {

        private bool _isInitialized;

        // store mapping between comboboxitem and featurelayer
        private Dictionary<string, FeatureLayer> _layerMap;

        public MiningSitesComboBox() 
        {
            _layerMap = new Dictionary<string, FeatureLayer>();
            UpdateCombo();
        }
 
        private void UpdateCombo()
        {
            if (_isInitialized)
            {
                SelectedItem = ItemCollection.FirstOrDefault();
                return;
            }

            Clear();

            // get all feature layers in the current map view
            var featureLayers = MapView.Active.Map.Layers.OfType<FeatureLayer>();

            if (!featureLayers.Any())
            {
                Add(new ComboBoxItem("No feature layers available"));
            }
            else
            {
                // add each feature layer to the combobox
                foreach (var featureLayer in featureLayers)
                {
                    var comboBoxItem = new ComboBoxItem(featureLayer.Name);
                    Add(new ComboBoxItem(featureLayer.Name, featureLayer));
                    _layerMap[featureLayer.Name] = featureLayer;
                }
            }

            _isInitialized = true;
            Enabled = true;
            SelectedItem = ItemCollection.FirstOrDefault();
          }
       
        protected override void OnSelectionChange(ComboBoxItem item) 
        {
            if (item == null)
                return;

            // check if selected item corresponds to a valid feature layer
            if (_layerMap.TryGetValue(item.Text, out var featureLayer))
            {
                SelectAllFeaturesInLayer(featureLayer);
            }
        }

        private void SelectAllFeaturesInLayer(FeatureLayer featureLayer)
        {
            QueuedTask.Run(() =>
            {
                // clear any existing selection
                featureLayer.ClearSelection();

                // create queryfilter to select all features in the layer
                var queryFilter = new QueryFilter
                {
                    WhereClause = ""
                };

                // select all feature in layer using the queryfilter
                featureLayer.Select(queryFilter);
            });
        }
    }
}

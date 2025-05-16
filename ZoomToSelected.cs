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
using ArcGIS.Core.Internal.Geometry;

namespace MiningSites
{
    internal class ZoomToSelected : Button
    {
        protected override async void OnClick()
        {
            // call the ZoomToSelectedAsync method when the button is clicked
            bool zoomSuccessful = await ZoomToSelectedAsync();
        }

        // method to zoom to the selected features in the map
        public async Task<bool> ZoomToSelectedAsync()
        {
            // get the active map view
            var mapView = MapView.Active;
            if (mapView == null)
                return false;

            // zoom to the map's selected features
            return await QueuedTask.Run(() => mapView.ZoomToSelectedAsync(TimeSpan.FromSeconds(2)));
        }
    }
}

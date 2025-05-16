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

namespace MiningSites
{
    internal class IdentifyTool : MapTool
    {
        public IdentifyTool()
        {
            IsSketchTool = true;
            SketchType = SketchGeometryType.Rectangle;
            SketchOutputMode = SketchOutputMode.Map;
        }

        protected override Task OnToolActivateAsync(bool active)
        {
            return base.OnToolActivateAsync(active);
        }

        protected override async Task<bool> OnSketchCompleteAsync(Geometry geometry)
        {
            var mv = MapView.Active;
            var identifyResult = await QueuedTask.Run(() =>
            {
                var sb = new StringBuilder();

                // get the features that intersect the sketch geometry
                var features = mv.GetFeatures(geometry);

                // get all layer definitions
                var lyrs = mv.Map.GetLayersAsFlattenedList().OfType<FeatureLayer>();
                foreach (var lyr in lyrs)
                {
                    var fCnt = features.ToDictionary().ContainsKey(lyr) ? features[lyr].Count : 0;
                    sb.AppendLine($@"{fCnt} {(fCnt == 1 ? "record" : "records")} for {lyr.Name}");
                }
                return sb.ToString();
            });
            MessageBox.Show(identifyResult);
            return true;
        }
    }
}
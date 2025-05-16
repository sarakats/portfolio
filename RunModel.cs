using ArcGIS.Core.CIM;
using ArcGIS.Core.Data;
using ArcGIS.Core.Geometry;
using ArcGIS.Desktop.Catalog;
using ArcGIS.Desktop.Core;
using ArcGIS.Desktop.Core.Geoprocessing;
using ArcGIS.Desktop.Editing;
using ArcGIS.Desktop.Extensions;
using ArcGIS.Desktop.Framework;
using ArcGIS.Desktop.Framework.Contracts;
using ArcGIS.Desktop.Framework.Dialogs;
using ArcGIS.Desktop.Framework.Threading.Tasks;
using ArcGIS.Desktop.Layouts;
using ArcGIS.Desktop.Mapping;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;

namespace MiningSites
{
    internal class RunModel : Button
    {
        protected override async void OnClick()
        {
            try
            {
                CancelableProgressorSource cps = new("Running Model", "Canceled");

                // set tool name 
                string modelToolName = "AddinsTestingatbx.CrTbl";

                // No input parameters required
                var args = Geoprocessing.MakeValueArray();

                // set environment options
                var env = Geoprocessing.MakeEnvironmentArray(overwriteoutput: true);

                // run the tool
                await RunGPTool(modelToolName, args, cps.Progressor, env, GPExecuteToolFlags.AddOutputsToMap);
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        public async Task RunGPTool(string GPTool,
                                    IReadOnlyList<string> parameters,
                                    CancelableProgressor prog,
                                    IEnumerable<KeyValuePair<string, string>> env = null,
                                    GPExecuteToolFlags flag = GPExecuteToolFlags.Default)
        {
            try
            {
                var gp_result = await Geoprocessing.ExecuteToolAsync(GPTool, parameters, env, prog, flag);
                if (gp_result != null) Geoprocessing.ShowMessageBox(gp_result.Messages, "Geoprocessing Result",
                  gp_result.IsFailed ? GPMessageBoxStyle.Error :
                    GPMessageBoxStyle.Default);
            }
            catch
            {
                var gp_result = await Geoprocessing.OpenToolDialogAsync(GPTool, parameters, env);
                if (gp_result != null) Geoprocessing.ShowMessageBox(gp_result.Messages, "Geoprocessing Result",
                  gp_result.IsFailed ? GPMessageBoxStyle.Error :
                    GPMessageBoxStyle.Default);
            }
        }
    }
}
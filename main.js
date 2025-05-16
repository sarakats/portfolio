/*
Author : Sara Katsabas
Date   : April 14, 2025
Purpose: To create and initialize a 3D web scene using ArcGIS SDK for JavaScript
*/

"use strict";

require(["esri/config",
    "esri/core/Collection",
    "esri/Map",
    "esri/views/SceneView",
    "esri/layers/FeatureLayer",
    "esri/symbols/WebStyleSymbol",
    "esri/webmap/Bookmark",
    // Add widget modules
    "esri/widgets/Expand",
    "esri/widgets/Home",
    "esri/widgets/BasemapToggle",
    "esri/widgets/Legend",
    "esri/widgets/LineOfSight",
    "esri/widgets/ElevationProfile",
    "esri/widgets/Bookmarks"],
    function (esriConfig, Collection, Map, SceneView, FeatureLayer, WebStyleSymbol, Bookmark,
        Expand, Home, BasemapToggle, Legend, LineOfSight, ElevationProfile, Bookmarks) {
        /*
        Function: init
        Purpose : To initialize API key and set map and view properties
        */
        function init() {
            // Give access via API token (all access)
            esriConfig.apiKey = "AAPTxy8BH1VEsoebNVZXo8HurFETYEN-oxKTcZ-OJ47G5_IDbL40zlC2mhJCjTxmJjPbcHibQ9v7Ab4rZR69j12uJZXw6e0Af1kFcUEu37DGydnw8JnM6FEf01GnGXM8MrSNIMFci77ePZQcj1dqLQkznt03DdNforcmjkn76aE17RrhOS_3bTqWxlR93S98bvTJdIGgMxWRMCDji1YGu0R5enQxkk6tHEn6M068ERySOL8.AT1_SI2CN7Z7"

            // Define map and set basemap
            const mainMap = new Map({
                basemap: "topo-vector",
                ground: "world-topobathymetry"
            });

            // Define scene view and camera properties
            const view = new SceneView({
                map: mainMap,
                container: "sceneDiv",
                camera: {
                    position: [
                        -125.7281,
                        49.164345,
                        10000
                    ],
                    heading: -105,
                    tilt: 45
                }
            });

            // Call mapLayers and mapWidgets functions
            mapLayers(mainMap);
            mapWidgets(view);
        };

        /*
        Function: mapLayers
        Purpose : To style, define, and add layers to map from existing feature service layers
        */
        // Define and add new layers from feature service layers 
        function mapLayers(mainMap) {

            // SurveyAreas
            // Define a renderer for SurveyAreas
            let surveyAreasRenderer = {
                type: "simple",
                symbol: {
                    type: "simple-fill",
                    color: [283, 141, 208, 0.3],
                    outline: {
                        width: 1,
                        color: [77, 38, 101, 0.8]
                    }
                }
            };

            // Define a popup template for surveyAreas units
            let surveyAreasPopup = {
                title: "Survey Areas",
                content: [{
                    type: "fields",
                    fieldInfos: [{
                        fieldName: "SITE_NAME",
                        label: "Site Name"
                    }, {
                        fieldName: "Shape__Area",
                        label: "Area (square km)",
                        format: {
                            digitSeparator: true,
                            places: 2
                        }
                    }]
                }]
            };

            // Define layer SurveyAreas
            let surveyAreas = new FeatureLayer({
                url: "https://services6.arcgis.com/FdqeyoRFp9Q4CC1T/arcgis/rest/services/SurveyAreas/FeatureServer"
                , elevationInfo: "relative-to-ground"
                , renderer: surveyAreasRenderer
                , popupTemplate: surveyAreasPopup
                , maxScale: 0
                , copyright: "Government of Canada; Environment and Climate Change Canada"
            });

            // SurveyTransects
            // Define a renderer for surveyTransects that includes unique styling for different transect types
            let surveyTransectsRenderer = {
                type: "unique-value",
                field: "Type",
                uniqueValueInfos: [
                    {
                        value: "Boat",
                        symbol: {
                            type: "simple-line",
                            color: "blue",
                            width: 1,
                            style: "solid"
                        },
                        label: "Boat Transects"
                    },
                    {
                        value: "Walking",
                        symbol: {
                            type: "simple-line",
                            color: "green",
                            width: 2,
                            style: "dash"
                        },
                        label: "Walking Transects"
                    },
                    {
                        value: "Point",
                        symbol: {
                            type: "simple-line",
                            color: "purple",
                            width: 2,
                            style: "dot"
                        },
                        label: "Point Transects"
                    }
                ]
            };

            // Define layer SurveyTransects
            let surveyTransects = new FeatureLayer({
                url: "https://services6.arcgis.com/FdqeyoRFp9Q4CC1T/arcgis/rest/services/SurveyTransects/FeatureServer"
                , elevationInfo: "on-the-ground"
                , renderer: surveyTransectsRenderer
                , copyright: "Government of Canada; Environment and Climate Change Canada"
            });

            // SurveyPoints
            // Define 3D symbol for surveyPoints
            let pointSymbol = new WebStyleSymbol({
                name: "Standing Diamond",
                styleName: "EsriThematicShapesStyle"
            });

            let pointSymbolRenderer = {
                type: "simple",
                symbol: pointSymbol
            };

            // Define layer surveyPoints
            let surveyPoints = new FeatureLayer({
                url: "https://services6.arcgis.com/FdqeyoRFp9Q4CC1T/arcgis/rest/services/SurveyPoints/FeatureServer"
                , renderer: pointSymbolRenderer
                , elevationInfo: "relative-to-ground"
                , copyright: "Government of Canada; Environment and Climate Change Canada"
            });

            // Resize and colour surveyPoints symbols
            pointSymbol.fetchSymbol()
                .then(function (ptSymb) {
                    let objectSymbolLayer = ptSymb.symbolLayers.getItemAt(0);
                    objectSymbolLayer.material = { color: "blue" };
                    objectSymbolLayer.height *= 35;
                    objectSymbolLayer.width *= 35;
                    objectSymbolLayer.depth *= 35;

                    let NEWrenderer = surveyPoints.renderer.clone();
                    NEWrenderer.symbol = ptSymb;
                    surveyPoints.renderer = NEWrenderer;
                });

            // Add layers to map
            mainMap.addMany([surveyAreas, surveyTransects, surveyPoints]);
        };

        /*
        Function: mapWidgets
        Purpose : To define and add widgets to map
        */
        function mapWidgets(view) {
            // Define and add home widget to top left corner of the view
            let homeWidget = new Home({
                view: view
            });
            view.ui.add(homeWidget, "top-left");

            // Define and add basemap toggle widget to top right
            let basemapToggle = new BasemapToggle({
                view: view,
                nextBasemap: "dark-gray-3d"
            });
            view.ui.add(basemapToggle, "top-right");

            // Define and add legend widget to bottom right corner of the view
            let legend = new Legend({
                view: view
            });
            // Add ability to collapse the widget
            let legendExpand = new Expand({
                view: view,
                content: legend
            });
            view.ui.add(legendExpand, "bottom-right");

            // Define and add elevation profile to bottom left corner of the view
            let elevationProfile = new ElevationProfile({
                view: view
            });
            // Add ability to collapse the widget
            let profileExpand = new Expand({
                view: view,
                content: elevationProfile
            });
            view.ui.add(profileExpand, "bottom-left");

            // Create an event listener which will clear elevation profile when widget is collapsed
            profileExpand.watch("expanded", function (isExpanded) {
                if (isExpanded) {
                    elevationProfile.activeTool = "direct-line";
                }
                else {
                    elevationProfile.activeTool = null;
                    elevationProfile.input = null;
                    elevationProfile.viewModel.clear();
                }
            });

            // Define and add line of sight widget to bottom left corner of the view
            let lineOfSight = new LineOfSight({
                view: view
            });
            // Add ability to collapse the widget
            let lineOfSightExpand = new Expand({
                view: view,
                content: lineOfSight
            });
            view.ui.add(lineOfSightExpand, "bottom-left");

            // Define bookmarks for bookmarks widget
            let surveyBookmarks = new Collection([
                new Bookmark({
                    name: "Arakan Flats",
                    viewpoint: {
                        camera: {
                            position: [
                                -125.871506,
                                49.126766,
                                5000
                            ],
                            heading: 0,
                            tilt: 45
                        }
                    }
                }),
                new Bookmark({
                    name: "Ducking Flats",
                    viewpoint: {
                        targetGeometry: {
                            type: "extent",
                            xmin: -125.874880105,
                            ymin: 49.134896781,
                            xmax: -125.85345366,
                            ymax: 49.15244634,
                            spatialReference: { wkid: 4326 }
                        }
                    }
                }),
                new Bookmark({
                    name: "South Bay",
                    viewpoint: {
                        targetGeometry: {
                            type: "extent",
                            xmin: -125.843069941,
                            ymin: 49.098014617,
                            xmax: -125.816038182,
                            ymax: 49.123952843,
                            spatialReference: { wkid: 4326 }
                        }
                    }
                }),
                new Bookmark({
                    name: "Maltby Slough",
                    viewpoint: {
                        targetGeometry: {
                            type: "extent",
                            xmin: -125.863194673,
                            ymin: 49.094457407,
                            xmax: -125.841436206,
                            ymax: 49.127721837,
                            spatialReference: { wkid: 4326 }
                        }
                    }
                }),
                new Bookmark({
                    name: "Doug Banks' Flats",
                    viewpoint: {
                        targetGeometry: {
                            type: "extent",
                            xmin: -125.890120078,
                            ymin: 49.112226664,
                            xmax: -125.851251712,
                            ymax: 49.145900522,
                            spatialReference: { wkid: 4326 }
                        }
                    }
                }),
                new Bookmark({
                    name: "Chesterman Beach",
                    viewpoint: {
                        targetGeometry: {
                            type: "extent",
                            xmin: -125.9052751,
                            ymin: 49.10654995,
                            xmax: -125.878974357,
                            ymax: 49.124218988,
                            spatialReference: { wkid: 4326 }
                        }
                    }
                }),
                new Bookmark({
                    name: "Grice Bay",
                    viewpoint: {
                        targetGeometry: {
                            type: "extent",
                            xmin: -125.769362753,
                            ymin: 49.072403999,
                            xmax: -125.7253022,
                            ymax: 49.106131483,
                            spatialReference: { wkid: 4326 }
                        }
                    }
                })
            ]);

            // Define and add bookmarks widget to top right corner of the view
            let bookmarks = new Bookmarks({
                view: view,
                bookmarks: surveyBookmarks,
                editingEnabled: false
            });
            // Add ability to collapse the widget
            let bookmarksExpand = new Expand({
                view: view,
                content: bookmarks
            });
            view.ui.add(bookmarksExpand, "top-right");
        };

        // Run init function
        init();
    });
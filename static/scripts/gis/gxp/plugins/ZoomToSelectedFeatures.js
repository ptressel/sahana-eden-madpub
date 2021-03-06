/**
 * Copyright (c) 2008-2011 The Open Planning Project
 * 
 * Published under the BSD license.
 * See https://github.com/opengeo/gxp/raw/master/license.txt for the full text
 * of the license.
 */

/**
 * @requires plugins/ZoomToExtent.js
 */

/** api: (define)
 *  module = gxp.plugins
 *  class = ZoomToSelectedFeatures
 */

/** api: (extends)
 *  plugins/ZoomToExtent.js
 */
Ext.namespace("gxp.plugins");

/** api: constructor
 *  .. class:: ZoomToSelectedFeatures(config)
 *
 *    Plugin for zooming to the extent of selected features
 */
gxp.plugins.ZoomToSelectedFeatures = Ext.extend(gxp.plugins.ZoomToExtent, {
    
    /** api: ptype = gxp_zoomtoselectedfeatures */
    ptype: "gxp_zoomtoselectedfeatures",
    
    /** api: config[menuText]
     *  ``String``
     *  Text for zoom menu item (i18n).
     */
    menuText: "Zoom to selected features",

    /** api: config[tooltip]
     *  ``String``
     *  Text for zoom action tooltip (i18n).
     */
    tooltip: "Zoom to selected features",
    
    /** api: config[featureManager]
     *  ``String`` id of the :class:`gxp.plugins.FeatureManager` to look for
     *  selected features
     */
    
    /** api: config[closest]
     *  ``Boolean`` Find the zoom level that most closely fits the specified
     *  extent. Note that this may result in a zoom that does not exactly
     *  contain the entire extent.  Default is false.
     */
    closest: false,

    /** private: property[iconCls]
     */
    iconCls: "gxp-icon-zoom-to",
    
    /** private: method[extent]
     */
    extent: function() {
        var layer = this.target.tools[this.featureManager].featureLayer;
        var bounds, geom, extent, features = layer.selectedFeatures;
        for (var i=features.length-1; i>=0; --i) {
            geom = features[i].geometry;
            if (geom) {
                extent = geom.getBounds();
                if (bounds) {
                    bounds.extend(extent);
                } else {
                    bounds = extent.clone();
                }
            }
        };
        return bounds;
     },
    
    /** api: method[addActions]
     */
    addActions: function() {
        var actions = gxp.plugins.ZoomToSelectedFeatures.superclass.addActions.apply(this, arguments);
        actions[0].disable();

        var layer = this.target.tools[this.featureManager].featureLayer;
        layer.events.on({
            "featureselected": function() {
                actions[0].isDisabled() && actions[0].enable();
            },
            "featureunselected": function() {
                layer.selectedFeatures.length == 0 && actions[0].disable();
            }
        });
        
        return actions;
    }
        
});

Ext.preg(gxp.plugins.ZoomToSelectedFeatures.prototype.ptype, gxp.plugins.ZoomToSelectedFeatures);

// src/router/navigation.js

export const NAV_ROOT = "/dashboard";

export const NAV_ITEMS = {
  dashboard: {
    label: "Dashboard",
    path: "/dashboard"
  },

  layers: [
    { label: "Layer 1", path: "/layer1" },
    { label: "Layer 2", path: "/layer2" },
    { label: "Layer 3", path: "/layer3" }
  ],

  extruders: [
    { label: "Extruder 1", path: "/extruder1" },
    { label: "Extruder 2", path: "/extruder2" },
    { label: "Extruder 3", path: "/extruder3" }
  ],

  winders: [
    { label: "Winder 1", path: "/winder1" },
    { label: "Winder 2", path: "/winder2" }
  ],

  utilities: [
    { label: "Reports", path: "/reports" },
    { label: "Material Utilization", path: "/material-utilization" }
  ]
};

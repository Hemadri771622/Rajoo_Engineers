import { createRouter, createWebHistory } from "vue-router";

import Login from "../views/Login.vue";
import DashboardMain from "../views/dashboard_main.vue";

import Layer1 from "../views/Layer1.vue";
import Layer2 from "../views/Layer2.vue";
import Layer3 from "../views/Layer3.vue";

// ================= NEW PAGES =================
import Extruder1 from "../views/Extruder1.vue";
import Extruder2 from "../views/Extruder2.vue";
import Extruder3 from "../views/Extruder3.vue";

import Winder1 from "../views/Winder1.vue";
import Winder2 from "../views/Winder2.vue";

import Reports from "../views/Reports.vue";
import MaterialUtilization from "../views/MaterialUtilization.vue";

// ================= ROUTES =================
const routes = [
  { path: "/", component: Login },

  {
    path: "/dashboard",
    component: DashboardMain,
    meta: { requiresAuth: true }
  },

  // -------- LAYERS --------
  { path: "/layer1", component: Layer1, meta: { requiresAuth: true } },
  { path: "/layer2", component: Layer2, meta: { requiresAuth: true } },
  { path: "/layer3", component: Layer3, meta: { requiresAuth: true } },

  // -------- EXTRUDERS --------
  { path: "/extruder1", component: Extruder1, meta: { requiresAuth: true } },
  { path: "/extruder2", component: Extruder2, meta: { requiresAuth: true } },
  { path: "/extruder3", component: Extruder3, meta: { requiresAuth: true } },

  // -------- WINDERS --------
  { path: "/winder1", component: Winder1, meta: { requiresAuth: true } },
  { path: "/winder2", component: Winder2, meta: { requiresAuth: true } },

  // -------- UTILITIES --------
  { path: "/reports", component: Reports, meta: { requiresAuth: true } },
  {
    path: "/material-utilization",
    component: MaterialUtilization,
    meta: { requiresAuth: true }
  }
];

// ================= ROUTER =================
const router = createRouter({
  history: createWebHistory(),
  routes
});

// ================= GLOBAL GUARD =================
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");

  // -------- AUTH --------
  if (to.meta.requiresAuth && !token) {
    next("/");
    return;
  }

  if (to.path === "/" && token) {
    next("/dashboard");
    return;
  }

  // -------- TRANSITIONS --------
  // default animation for all routes
  to.meta.transition = "fade";

 
  const isReturningToDashboard =
    to.path === "/dashboard" &&
    from.path !== "/" &&
    from.path !== "/dashboard";

  if (isReturningToDashboard) {
    to.meta.transition = "slide-back";
  }

  next();
});

export default router;


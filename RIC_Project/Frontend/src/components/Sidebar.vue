<template>
  <aside class="sidebar">
    <div class="avatar">
      <img src="/VirtualEX_logo.png" alt="User Avatar" />
    </div>

    <div v-for="section in menuSections" :key="section.title" class="menu-section">
      <div class="menu-title">{{ section.title }}</div>
      <button
        v-for="item in section.items"
        :key="item.label"
        :class="['menu-item', { active: isActive(item) }]"
        @click="navigate(item.path)"
      >
        {{ item.label }}
      </button>
    </div>
  </aside>
</template>

<script>
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";

export default {
  name: "Sidebar",
  setup() {
    const router = useRouter();
    const route = useRoute();

    const menuSections = [
      {
        title: "LAYERS",
        items: [
          { label: "Layer 1", path: "/layer1" },
          { label: "Layer 2", path: "/layer2" },
          { label: "Layer 3", path: "/layer3" },
        ],
      },
      {
        title: "EXTRUDER",
        items: [
          { label: "Extruder A", path: "/extruder1" },
          { label: "Extruder B", path: "/extruder2" },
          { label: "Extruder C", path: "/extruder3" },
        ],
      },
      {
        title: "WINDER",
        items: [
          { label: "Winder 1", path: "/winder1" },
          { label: "Winder 2", path: "/winder2" },
        ],
      },
      {
        title: "",
        items: [
          { label: "Die Zone Temperature", path: "/die-zone-temperature" },
        ],
      },

      {
        title: "UTILITIES",
        items: [
          { label: "Reports", path: "/reports" },
          { label: "Material Utilization", path: "/material-utilization" },
        ],
      },
    ];

    const navigate = (path) => router.push(path);
    const isActive = (item) => route.path.startsWith(item.path);

    return { menuSections, navigate, isActive };
  },
};
</script>
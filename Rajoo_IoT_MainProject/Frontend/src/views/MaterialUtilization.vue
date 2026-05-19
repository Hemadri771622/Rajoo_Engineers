<template>
  <div class="app">
    <!-- ================= SIDEBAR ================= -->
    <aside class="sidebar">
      <div class="avatar">
        <img src="/user-icon.png" />
      </div>

      <div class="menu-section">
        <div class="menu-title">LAYERS</div>
        <button class="menu-item" :class="{ active: isActive('/layer1') }" @click="navigate('/layer1')">Layer 1</button>
        <button class="menu-item" :class="{ active: isActive('/layer2') }" @click="navigate('/layer2')">Layer 2</button>
        <button class="menu-item" :class="{ active: isActive('/layer3') }" @click="navigate('/layer3')">Layer 3</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">EXTRUDER</div>
        <button class="menu-item" @click="navigate('/extruder1')">Extruder A</button>
        <button class="menu-item" @click="navigate('/extruder2')">Extruder B</button>
        <button class="menu-item" @click="navigate('/extruder3')">Extruder C</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">WINDER</div>
        <button class="menu-item" @click="navigate('/winder1')">Winder 1</button>
        <button class="menu-item" @click="navigate('/winder2')">Winder 2</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">UTILITIES</div>
        <button class="menu-item" @click="navigate('/reports')">Reports</button>
        <button class="menu-item" @click="navigate('/material-utilization')">
          Material Utilization
        </button>
      </div>
    </aside>

    <!-- ================= MAIN ================= -->
    <main class="main">

      <!-- ================= TOPBAR ================= -->
      <header class="topbar">
        <div class="top-left">
          <img src="/back-arrow.png" class="back-icon" @click="goBack" />
          <h1>THREE LAYER BLOWN FILM LINE</h1>
        </div>

        <div class="top-right">
          <span class="pill dark">
            {{ currentDate }}<br />
            {{ currentTime }}
          </span>
          <img src="/notification.png" class="notification-icon" />
          <!-- <img src="/power-button.png" class="power-icon" /> -->
        </div>
      </header>

      <!-- ================= CONTENT ================= -->
      <div class="content">
        <section class="panel left-panel">
          <h2>MATERIAL UTILIZATION</h2>

          <!--  LIVE CHART GRID -->
          <div class="chart-grid">

            <!-- Extruder A -->
            <div class="chart-card">
              <div class="chart-title">EXTRUDER A - TOTAL KG</div>
              <Line :key="'A'" :data="chartA" :options="commonOptions()" />
            </div>

            <!-- Extruder B -->
            <div class="chart-card">
              <div class="chart-title">EXTRUDER B - TOTAL KG</div>
              <Line :key="'B'" :data="chartA" :options="commonOptions()" />
            </div>

            <!-- Extruder C -->
            <div class="chart-card">
              <div class="chart-title">EXTRUDER C - TOTAL KG</div>
             <Line :key="'C'" :data="chartA" :options="commonOptions()" />
            </div>

          </div>

        </section>
      </div>

      <!-- ================= FOOTER ================= -->
      <footer class="footer">
        MODEL : RFC-2550-40-1800
      </footer>

    </main>
  </div>
</template>




<!-- <script>
import { io } from "socket.io-client";
import { Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
);

const MATERIAL_COLORS = {
  F18010: "#4dd0e1",
  LD: "#ff7043",
  F19010: "#81c784",
  PPA705: "#ffd54f",
  MLLD: "#ba68c8"
};

export default {
  name: "MaterialUtilization",
  components: { Line },

  data() {
    return {
      socket: null,
      currentDate: "",
      currentTime: "",
      extruderData: {
        A: {},
        B: {},
        C: {}
      }
    };
  },

  mounted() {
    this.updateClock();
    setInterval(this.updateClock, 1000);
    this.initSocket();
  },

  beforeUnmount() {
    if (this.socket) {
      this.socket.disconnect();
    }
  },

  methods: {

    // ===== NAVIGATION =====
    navigate(path) {
      if (this.$route.path !== path) {
        this.$router.push(path);
      }
    },

    goBack() {
      this.$router.push("/dashboard");
    },

    isActive(path) {
      return this.$route.path === path;
    },

    updateClock() {
      const d = new Date();
      this.currentDate = d.toLocaleDateString("en-GB");
      this.currentTime = d.toLocaleTimeString("en-US");
    },

    // ===== SOCKET =====
    initSocket() {
      this.socket = io("http://localhost:5000");

      this.socket.on("telemetry_update", (data) => {
        if (!data || !data.material_utilisation) return;

        this.extruderData = {
          A: data.material_utilisation.A?.materials ?? {},
          B: data.material_utilisation.B?.materials ?? {},
          C: data.material_utilisation.C?.materials ?? {}
        };
      });
    },

    // ===== CHART DATA BUILDER =====
    buildChart(materials) {

      if (!materials || typeof materials !== "object") {
        return { labels: [], datasets: [] };
      }

      const keys = Object.keys(materials);
      if (keys.length === 0) {
        return { labels: [], datasets: [] };
      }

      const firstSeries = materials[keys[0]];
      if (!Array.isArray(firstSeries) || firstSeries.length === 0) {
        return { labels: [], datasets: [] };
      }

      const labels = firstSeries.map(point =>
        new Date(point.x).toLocaleTimeString("en-GB")
      );

      const datasets = keys.map(key => ({
        label: key,
        data: materials[key].map(p => p.y ?? 0),
        borderColor: MATERIAL_COLORS[key] ?? "#ffffff",
        backgroundColor: MATERIAL_COLORS[key] ?? "#ffffff",
        tension: 0.3,
        pointRadius: 2,
        borderWidth: 2
      }));

      return { labels, datasets };
    },

    // ===== CHART OPTIONS =====
    commonOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,

        plugins: {
          legend: {
            position: "top",
            labels: {
              color: "#e6f7fb",
              boxWidth: 15
            }
          },

          // 🔥 REMOVE CENTER TITLE
          title: {
            display: false
          }
        },

        scales: {
          x: {
            title: {
              display: true,
              text: "Timestamp",
              color: "#7fdcff",
              font: {
                size: 12,
                weight: "bold"
              }
            },
            ticks: {
              color: "#e6f7fb",
              maxRotation: 45,
              minRotation: 45
            },
            grid: {
              color: "rgba(255,255,255,0.05)"
            }
          },

          y: {
            title: {
              display: true,
              text: "Kg",
              color: "#7fdcff",
              font: {
                size: 12,
                weight: "bold"
              }
            },
            ticks: {
              color: "#e6f7fb"
            },
            grid: {
              color: "rgba(255,255,255,0.05)"
            }
          }
        }
      };
    }
  },

  computed: {
    chartA() {
      return this.buildChart(this.extruderData.A);
    },
    chartB() {
      return this.buildChart(this.extruderData.B);
    },
    chartC() {
      return this.buildChart(this.extruderData.C);
    }
  }
};
</script> -->

<script>
import socket from "@/services/socket";
import { Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
);

const MATERIAL_COLORS = {
  F18010: "#4dd0e1",
  LD: "#ff7043",
  F19010: "#81c784",
  PPA705: "#ffd54f",
  MLLD: "#ba68c8"
};

export default {
  name: "MaterialUtilization",
  components: { Line },

  data() {
    return {
      currentDate: "",
      currentTime: "",
      extruderData: {
        A: {},
        B: {},
        C: {}
      },
      _clockTimer: null,
      _telemetryHandler: null
    };
  },

  mounted() {
    // ===== CLOCK =====
    this.updateClock();
    this._clockTimer = setInterval(this.updateClock, 1000);

    // ===== SOCKET LISTENER (GLOBAL SOCKET USED) =====
    this._telemetryHandler = (data) => {
      if (!data || !data.material_utilisation) return;

      this.extruderData = {
        A: data.material_utilisation.A?.materials ?? {},
        B: data.material_utilisation.B?.materials ?? {},
        C: data.material_utilisation.C?.materials ?? {}
      };
    };

    socket.off("telemetry_update", this._telemetryHandler);
    socket.on("telemetry_update", this._telemetryHandler);
  },

  beforeUnmount() {
    clearInterval(this._clockTimer);
    socket.off("telemetry_update", this._telemetryHandler);
  },

  methods: {

    navigate(path) {
      if (this.$route.path !== path) {
        this.$router.push(path);
      }
    },

    goBack() {
      this.$router.push("/dashboard");
    },

    isActive(path) {
      return this.$route.path === path;
    },

    updateClock() {
      const d = new Date();
      this.currentDate = d.toLocaleDateString("en-GB");
      this.currentTime = d.toLocaleTimeString("en-US");
    },

    // ===== BUILD CHART DATA =====
    buildChart(materials) {

      if (!materials || typeof materials !== "object") {
        return { labels: [], datasets: [] };
      }

      const keys = Object.keys(materials);
      if (!keys.length) {
        return { labels: [], datasets: [] };
      }

      const firstSeries = materials[keys[0]];
      if (!Array.isArray(firstSeries) || !firstSeries.length) {
        return { labels: [], datasets: [] };
      }

      const labels = firstSeries.map(point =>
        new Date(point.x).toLocaleTimeString("en-GB")
      );

      const datasets = keys.map(key => ({
        label: key,
        data: materials[key].map(p => p.y ?? 0),
        borderColor: MATERIAL_COLORS[key] ?? "#ffffff",
        backgroundColor: MATERIAL_COLORS[key] ?? "#ffffff",
        tension: 0.3,
        pointRadius: 2,
        borderWidth: 2
      }));

      return { labels, datasets };
    },

    // ===== CHART OPTIONS =====
    commonOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        plugins: {
          legend: {
            position: "top",
            labels: {
              color: "#e6f7fb",
              boxWidth: 15
            }
          }
        },
        scales: {
          x: {
            title: {
              display: true,
              text: "Timestamp",
              color: "#7fdcff",
              font: { size: 12, weight: "bold" }
            },
            ticks: {
              color: "#e6f7fb",
              maxRotation: 45,
              minRotation: 45
            },
            grid: {
              color: "rgba(255,255,255,0.05)"
            }
          },
          y: {
            title: {
              display: true,
              text: "Kg",
              color: "#7fdcff",
              font: { size: 12, weight: "bold" }
            },
            ticks: {
              color: "#e6f7fb"
            },
            grid: {
              color: "rgba(255,255,255,0.05)"
            }
          }
        }
      };
    }
  },

  computed: {
    chartA() {
      return this.buildChart(this.extruderData.A);
    },
    chartB() {
      return this.buildChart(this.extruderData.B);
    },
    chartC() {
      return this.buildChart(this.extruderData.C);
    }
  }
};
</script>

<style scoped>

/* ================= MAIN LAYOUT FIX ================= */

.main {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.content {
  flex: 1;
  overflow: hidden;
  display: flex;
}

.left-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* ================= BACK BUTTON ================= */

.top-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.back-icon {
  width: 42px;
  height: 42px;
  cursor: pointer;
  border-radius: 50%;
  padding: 6px;
  background: rgba(0, 255, 160, 0.12);
  backdrop-filter: blur(6px);
  transition:
    transform 0.2s ease,
    box-shadow 0.25s ease,
    background-color 0.25s ease;
}

.back-icon:hover {
  transform: scale(1.08);
  background: rgba(0, 255, 160, 0.22);
  box-shadow:
    0 0 14px rgba(0, 255, 160, 0.45),
    inset 0 0 0 1px rgba(255,255,255,0.35);
}

.back-icon:active {
  transform: scale(0.96);
}

/* ================= CHART GRID ================= */

.chart-grid {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 15px;
  min-height: 0;
}

/* ================= CHART CARD ================= */

.chart-card {
  flex: 1;                 
  min-height: 0;           
  padding: 15px;
  border-radius: 18px;
  background: rgba(255,255,255,0.08);
  backdrop-filter: blur(6px);
  display: flex;
  flex-direction: column;
}

/* ================= CHART TITLE ================= */

.chart-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #7fdcff;
  letter-spacing: 0.5px;
}

/* ================= CHART WRAPPER ================= */

.chart-wrapper {
  flex: 1;
  position: relative;
}

/* Make Chart.js canvas fill properly */

.chart-card canvas {
  height: 100% !important;
  width: 100% !important;
}

</style>
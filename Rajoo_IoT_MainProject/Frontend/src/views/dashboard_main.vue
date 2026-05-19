<template>
  <div class="app">
    <!-- LEFT SIDEBAR -->
    <aside class="sidebar">
      <div class="avatar">
        <img src="/user-icon.png" />
      </div>

      <div class="menu-section">
        <div class="menu-title">LAYERS</div>
        <button class="menu-item" :class="{ active: isActive('/layer1') }" @click="goToLayer('/layer1')">Layer 1</button>
        <button class="menu-item" :class="{ active: isActive('/layer2') }" @click="goToLayer('/layer2')">Layer 2</button>
        <button class="menu-item" :class="{ active: isActive('/layer3') }" @click="goToLayer('/layer3')">Layer 3</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">EXTRUDER</div>
        <button class="menu-item" :class="{ active: isActive('/extruder1') }" @click="goTo('/extruder1')">Extruder A</button>
        <button class="menu-item" :class="{ active: isActive('/extruder2') }" @click="goTo('/extruder2')">Extruder B</button>
        <button class="menu-item" :class="{ active: isActive('/extruder3') }" @click="goTo('/extruder3')">Extruder C</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">WINDER</div>
        <button class="menu-item" :class="{ active: isActive('/winder1') }" @click="goTo('/winder1')">Winder 1</button>
        <button class="menu-item" :class="{ active: isActive('/winder2') }" @click="goTo('/winder2')">Winder 2</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">UTILITIES</div>
        <button class="menu-item" :class="{ active: isActive('/reports') }" @click="goTo('/reports')">Reports</button>
        <button class="menu-item" :class="{ active: isActive('/material-utilization') }" @click="goTo('/material-utilization')">Material Utilization</button>
      </div>
    </aside>

    <!-- MAIN -->
    <main class="main">
      <!-- TOP BAR -->
      <header class="topbar">

  <!-- LEFT TITLE -->
  <div class="top-left">
    <h1>THREE LAYER BLOWN FILM LINE</h1>
  </div>

  <!-- CENTER KPI BOXES -->
  <div class="top-kpi-wrapper">
    <div class="top-kpi-box">
      <div class="kpi-title">OEE</div>
      <div class="kpi-value">{{ oee ?? 'N/A' }}</div>
    </div>

    <div class="top-kpi-box">
      <div class="kpi-title">Availability</div>
      <div class="kpi-value">{{ availability ?? 'N/A' }}</div>
    </div>

    <div class="top-kpi-box">
      <div class="kpi-title">Performance</div>
      <div class="kpi-value">{{ performance ?? 'N/A' }}</div>
    </div>

    <div class="top-kpi-box">
      <div class="kpi-title">Quality</div>
      <div class="kpi-value">{{ quality ?? 'N/A' }}</div>
    </div>
  </div>

  <!-- RIGHT DATE + ICONS -->
  <div class="top-right">
    <span class="pill dark">
      {{ currentDate }}<br />
      {{ currentTime }}
    </span>
    <img src="/notification.png" class="notification-icon" />
    <img src="/power-button.png" class="power-icon" @click="handleLogout" />
  </div>

</header>

      <!-- CONTENT -->
      <div class="content">
        <!-- MACHINE OVERVIEW -->
        <section class="panel left-panel">
          <h2>MACHINE OVERVIEW PANEL</h2>

          <div class="stats">
            <div class="stat">Total Set Output<span>{{ total_set_output.toFixed(2) }} kg/hr</span></div>
            <div class="stat">Total Actual Output<span>{{ total_actual_output.toFixed(2) }} kg/hr</span></div>
            <div class="stat">Density<span>{{ density.toFixed(2) }} g/cm³</span></div>
            <div class="stat">GSM<span>{{ gsm.toFixed(2) }}</span></div>
            <div class="stat">Lay Flat<span>{{ lay_flat.toFixed(2) }} mm</span></div>
          </div>

          <div class="dual-graph-row">
            <div class="row graph-row">
              <div class="row-title">LIP PROFILE</div>
              <Line :data="lipChartData" :options="lipChartOptions" />
            </div>
            <div class="row graph-row">
              <div class="row-title">MAP PROFILE</div>
              <Line :data="mapChartData" :options="mapChartOptions" />
            </div>
          </div>

          <div class="dual-graph-row">
            <div class="row graph-row">
              <div class="row-title">IBC TEMP IN / OUT</div>
              <Bar :data="ibcChartData" :options="ibcChartOptions" />
            </div>
            <div class="row graph-row">
              <div class="row-title">SET vs ACT SPEED</div>
              <Line :data="speedChartData" :options="speedChartOptions" />
            </div>
          </div>

          <!-- DIE TEMP -->
          <div class="row die-zone-card">
            <div class="row-title">DIE TEMPERATURE ZONE WISE</div>
            <div class="die-zone-grid">
              <div v-for="zone in die_temp_zones" :key="zone.zone" class="die-zone" :class="zoneStatus(zone)">
                <div class="zone-name">{{ zone.zone }}</div>
                <div class="zone-values">
                  <div>SET {{ zone.set.toFixed(1) }}°C</div>
                  <div>ACT {{ zone.actual.toFixed(1) }}°C</div>
                  <div class="delta">Δ {{ (zone.actual - zone.set).toFixed(1) }}°C</div>
                </div>
              </div>
            </div>
          </div>

          <!-- THICKNESS -->
          <div class="row thickness-card-full">
            <div class="row-title">THICKNESS</div>
            <div class="thickness-content-full">
              <div class="thickness-graph-full">
                <Line :data="thicknessChartData" :options="thicknessChartOptions" />
              </div>
              <div class="thickness-info-full">
                <div><b>Set Thickness</b> : {{ thickness_stats.set }}</div>
                <div><b>Average</b> : {{ thickness_stats.avg }}</div>
                <div><b>Nominal</b> : {{ thickness_stats.nominal }}</div>
                <div><b>Maximum</b> : {{ thickness_stats.max }}</div>
                <div><b>Minimum</b> : {{ thickness_stats.min }}</div>
                <div><b>GBR Position</b> : {{ thickness_stats.gbr }}</div>
              </div>
            </div>
          </div>
        </section>

      </div>

      <footer class="footer">MODEL : RFC-2550-40-1800</footer>
    </main>
  </div>
</template>



<script>
import socket from "@/services/socket";   
import { Line, Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  LineElement,
  BarElement,
  BarController,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  LineElement,
  BarElement,
  BarController,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
);

ChartJS.defaults.responsive = true;
ChartJS.defaults.maintainAspectRatio = false;

export default {
  name: "DashboardMain",
  components: { Line, Bar },

  data() {
    return {
      chartKey: 0,

      currentDate: "",
      currentTime: "",

      oee: null,
      availability: null,
      performance: null,
      quality: null,

      total_set_output: 0,
      total_actual_output: 0,
      density: 0,
      gsm: 0,
      lay_flat: 0,

      lip_labels: [],
      lip_values: [],
      map_labels: [],
      map_values: [],

      ibc_labels: [],
      ibc_in: [],
      ibc_out: [],

      speed_labels: [],
      speed_set: [],
      speed_actual: [],

      thickness_labels: [],
      thickness_actual: [],
      thickness_stats: {
        set: 0,
        avg: 0,
        nominal: 0,
        max: 0,
        min: 0,
        gbr: 0
      },

      die_temp_zones: [],

      clockInterval: null,
      refreshInterval: null,
      telemetryHandler: null
    };
  },

  mounted() {
    // ================= CLOCK =================
    this.updateClock();
    this.clockInterval = setInterval(this.updateClock, 1000);

    // ================= TELEMETRY =================
    this.telemetryHandler = (data) => {

      if (data.machine_overview) {
        Object.assign(this, data.machine_overview);
      }

      this.lip_labels = data.lip_profile?.map(p => String(p.x)) ?? [];
      this.lip_values = data.lip_profile?.map(p => p.y) ?? [];

      this.map_labels = data.map_profile?.map(p => String(p.x)) ?? [];
      this.map_values = data.map_profile?.map(p => p.y) ?? [];

      const makeTime = (len) =>
        Array.from({ length: len }, (_, i) =>
          new Date(Date.now() - (len - i - 1) * 10000)
            .toLocaleTimeString("en-GB")
        );

      this.ibc_labels = makeTime(data.ibc_temp?.in?.length || 0);
      this.ibc_in = data.ibc_temp?.in ?? [];
      this.ibc_out = data.ibc_temp?.out ?? [];

      this.speed_labels = makeTime(data.speed_trend?.set?.length || 0);
      this.speed_set = data.speed_trend?.set ?? [];
      this.speed_actual = data.speed_trend?.actual ?? [];

      if (data.thickness) {
        this.thickness_labels = makeTime(data.thickness.trend.length);
        this.thickness_actual = data.thickness.trend;
        this.thickness_stats = data.thickness.stats;
      }

      this.die_temp_zones = data.die_temp_zones ?? [];

      // keep your redraw logic
      this.chartKey++;
    };

    socket.on("telemetry_update", this.telemetryHandler);

    // ================= SAFETY REFRESH =================
    this.refreshInterval = setInterval(() => {
      this.chartKey++;
    }, 10000);
  },

  beforeUnmount() {
    socket.off("telemetry_update", this.telemetryHandler);

    if (this.clockInterval) clearInterval(this.clockInterval);
    if (this.refreshInterval) clearInterval(this.refreshInterval);
  },

  methods: {
    updateClock() {
      const now = new Date();
      this.currentDate = now.toLocaleDateString("en-GB");
      this.currentTime = now.toLocaleTimeString("en-GB");
    },

    goToLayer(path) {
      if (this.$route.path !== path) this.$router.push(path);
    },

    goTo(path) {
      if (this.$route.path !== path) this.$router.push(path);
    },

    isActive(path) {
      return this.$route.path === path;
    },

    zoneStatus(zone) {
      const diff = Math.abs(zone.actual - zone.set);
      if (diff <= 2) return "ok";
      if (diff <= 5) return "warn";
      return "alert";
    },

    handleLogout() {
      socket.disconnect();
      localStorage.removeItem("token");
      this.$router.replace("/");
    },

    commonOptions(xLabel, yLabel, legend = false, isTimeChart = false) {
      return {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,

        plugins: {
          legend: legend
            ? {
                labels: {
                  color: "#e6f7fb",
                  font: { size: 13 }
                }
              }
            : { display: false }
        },

        scales: {
          x: {
            type: "category",
            title: {
              display: true,
              text: xLabel,
              color: "#ffffff"
            },
            ticks: {
              color: "#dff6ff",
              autoSkip: true,
              maxTicksLimit: isTimeChart ? 8 : undefined,
              maxRotation: 0,
              minRotation: 0,
              font: {
                size: isTimeChart ? 9 : 11
              }
            }
          },
          y: {
            title: {
              display: true,
              text: yLabel,
              color: "#ffffff"
            },
            ticks: {
              color: "#dff6ff",
              font: { size: 10 }
            }
          }
        }
      };
    }
  },

  computed: {
    lipChartData() {
      return {
        labels: this.lip_labels,
        datasets: [{
          data: this.lip_values,
          borderColor: "#7fdcff",
          borderWidth: 2.5,
          tension: 0.35,
          pointRadius: 3
        }]
      };
    },

    mapChartData() {
      return {
        labels: this.map_labels,
        datasets: [{
          data: this.map_values,
          borderColor: "#81c784",
          borderWidth: 2.5,
          tension: 0.35,
          pointRadius: 3
        }]
      };
    },

    ibcChartData() {
      return {
        labels: this.ibc_labels,
        datasets: [
          {
            label: "IBC IN",
            data: this.ibc_in,
            backgroundColor: "rgba(79,195,247,0.9)"
          },
          {
            label: "IBC OUT",
            data: this.ibc_out,
            backgroundColor: "rgba(255,138,101,0.9)"
          }
        ]
      };
    },

    speedChartData() {
      return {
        labels: this.speed_labels,
        datasets: [
          { label: "SET", data: this.speed_set, borderColor: "#4dd0e1" },
          { label: "ACT", data: this.speed_actual, borderColor: "#ff7043" }
        ]
      };
    },

    thicknessChartData() {
      return {
        labels: this.thickness_labels,
        datasets: [
          {
            label: "Actual",
            data: this.thickness_actual,
            borderColor: "#ff7043",
            borderWidth: 3
          },
          {
            label: "Set",
            data: this.thickness_labels.map(() => this.thickness_stats.set),
            borderColor: "#4dd0e1",
            borderDash: [6, 4]
          }
        ]
      };
    },

    lipChartOptions() {
      return this.commonOptions("Die Width", "Thickness (µm)");
    },

    mapChartOptions() {
      return this.commonOptions("Die Width", "Thickness (µm)");
    },

    ibcChartOptions() {
      return this.commonOptions("Time", "Temperature (°C)", true, true);
    },

    speedChartOptions() {
      return this.commonOptions("Time", "Speed", true, true);
    },

    thicknessChartOptions() {
      return this.commonOptions("Time", "Thickness (µm)", false, true);
    }
  }
};
</script>



<style>

/* ================= BASE ================= */
* {
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  margin: 0;
  background: radial-gradient(circle at top, #0c2c3d, #061621);
  font-family: "Inter", sans-serif;
  color: #e6f7fb;
  overflow: hidden;
}

/* ================= APP LAYOUT ================= */
.app {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

/* ================= SIDEBAR ================= */
.sidebar {
  width: 190px;
  min-width: 190px;
  max-width: 190px;
  height: 100vh;
  padding: 12px 12px 16px 12px;
  background: linear-gradient(180deg, #051c2a, #04121b);
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  overflow-x: hidden;
}

/* ================= AVATAR ================= */
.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: radial-gradient(circle, #7fdcff, #3f51b5);
  display: flex;
  align-items: center;
  justify-content: center;
  align-self: center;
  margin-bottom: 18px;
}

.avatar img {
  width: 26px;
  height: 26px;
}

/* ================= MENU ================= */
.menu-section {
  margin-bottom: 14px;
}

.menu-title {
  font-size: 10px;
  letter-spacing: 1.2px;
  color: #4dd0e1;
  margin: 8px 0 6px;
}

.menu-item {
  width: 100%;
  background: rgba(255,255,255,0.06);
  border: none;
  color: #e6f7fb;
  padding: 10px 12px;
  border-radius: 10px;
  margin-bottom: 8px;
  text-align: left;
  font-size: 13px;
  cursor: pointer;
}

.menu-item.active {
  background: rgba(127,220,255,0.25);
}

/* ================= MAIN ================= */
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
}

/* ================= TOP BAR ================= */
.topbar {
  height: 60px;
  min-height: 60px;
  max-height: 60px;
  flex-shrink: 0;
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(180deg, #0e2f43, #081c28);
  overflow: hidden;
}

.topbar h1 {
  font-size: 22px;
  font-weight: 700;
  margin: 0;
  text-transform: uppercase;
  line-height: 1;
  background: linear-gradient(
    90deg,
    #e6f7fb 0%,
    #7fdcff 40%,
    #4dd0e1 70%,
    #e6f7fb 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.top-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.notification-icon,
.power-icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
  cursor: pointer;
}

/* ================= CONTENT ================= */
.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 14px 20px 10px 20px;
  overflow: hidden;
}

/* ================= PANEL ================= */
.panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: rgba(255,255,255,0.08);
  border-radius: 20px;
  padding: 14px 16px;
  overflow: hidden;
}

/* ================= PANEL TITLE ================= */
.panel > h2 {
  margin: -4px 0 10px 0;
  font-size: 20px;   
  font-weight: 600;
}

/* ================= STATS ================= */
.stats {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
  margin-bottom: 12px;
}

.stat {
  background: rgba(255,255,255,0.14);
  border-radius: 12px;
  padding: 14px 10px;
  text-align: center;
}

.stat span {
  display: block;
  margin-top: 4px;
  font-size: 16px;
  font-weight: 700;
}

/* ================= ROW ================= */
.row {
  background: rgba(255,255,255,0.1);
  border-radius: 14px;
  padding: 10px 12px;
  margin-bottom: 12px;
  display: flex;
  flex-direction: column;
}

.row-title {
  font-size: 13px;
  font-weight: 700;
  margin-bottom: 4px;
}

/* ================= GRAPH ROWS ================= */
.dual-graph-row {
  display: flex;
  gap: 14px;
}

.dual-graph-row .row {
  flex: 1;
}

.graph-row {
  height: 195px;
  padding: 18px 8px 12px 8px;
  background: rgba(0,0,0,0.18);
  border-radius: 12px;
  position: relative;
  overflow: hidden;
}

.graph-row canvas {
  width: 100% !important;
  height: 100% !important;
}

/* ================= DIE ZONE ================= */
.die-zone-card {
  margin: 4px 0 8px 0;
  padding: 6px 10px;
}

.die-zone-grid {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.die-zone {
  flex: 1 1 105px;
  min-height: 65px;
  padding: 8px 6px;
  border-radius: 10px;
  text-align: center;
  font-size: 12px;
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(127,220,255,0.3);
}

/* ================= THICKNESS (Balanced Compact) ================= */
.thickness-content-full {
  display: flex;
  gap: 18px;
  align-items: stretch;
}

.thickness-graph-full {
  flex: 1;
  height: 175px;              /* 🔥 perfectly balanced */
  padding: 4px 8px 10px 8px;  /* tighter */
  overflow: hidden;
}

.thickness-graph-full canvas {
  width: 100% !important;
  height: 100% !important;
}

.thickness-info-full {
  width: 220px;
  font-size: 13px;
  line-height: 1.6;
}

/* ================= FOOTER ================= */
.footer {
  height: 45px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  background: linear-gradient(180deg, #123a52, #081c28);
}


/* ================= TOP KPI BOXES ================= */

.top-kpi-wrapper {
  display: flex;
  gap: 14px;
  align-items: center;
}

.top-kpi-box {
  min-width: 110px;
  padding: 6px 12px;
  border-radius: 12px;
  background: rgba(255,255,255,0.12);
  text-align: center;
}

.top-kpi-box .kpi-title {
  font-size: 11px;
  opacity: 0.8;
}

.top-kpi-box .kpi-value {
  font-size: 16px;
  font-weight: 700;
}

</style>

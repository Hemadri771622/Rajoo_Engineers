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
        <button class="menu-item" @click="navigate('/material-utilization')">Material Utilization</button>
      </div>
    </aside>

    <!-- ================= MAIN ================= -->
    <main class="main">
      <header class="topbar">
        <div class="top-left">
          <img src="/back-arrow.png" class="back-icon" @click="goBack" />
          <h1>THREE LAYER BLOWN FILM LINE</h1>
        </div>

        <div class="top-right">
          <span class="pill dark">{{ currentDate }}<br />{{ currentTime }}</span>
          <img src="/notification.png" class="notification-icon" />
          <!-- <img src="/power-button.png" class="power-icon" /> -->
        </div>
      </header>

      <div class="content">
        <!-- ================= LEFT PANEL ================= -->
        <section class="panel left-panel">
          <h2>LAYER 1</h2>

          <!-- ===== METRIC CARDS ===== -->
          <div class="stats">
            <div class="stat">SPEED <span>{{ speed.toFixed(1) }} RPM</span></div>
            <div class="stat">YIELD <span>{{ yieldVal.toFixed(1) }} kg/hr</span></div>
            <div class="stat">AMPERE <span>{{ ampere }} A</span></div>
          </div>

          <!-- ===== LIVE GRAPHS ===== -->
          <div class="dual-graph-row">

            <!-- MELT PRESSURE -->
            <div class="row graph-row tall-graph">
              <div class="graph-header">
                <div class="graph-title">MELT PRESSURE</div>
                <div class="inline-value pressure">
                  {{
                    meltPressureTrend.length
                      ? meltPressureTrend[meltPressureTrend.length - 1].y.toFixed(2)
                      : "0.00"
                  }} Bar
                </div>
              </div>

              <div class="graph-placeholder">
                <Line :data="meltPressureChartData" :options="chartOptions" />
              </div>
            </div>

            <!-- SET vs ACT THICKNESS -->
            <div class="row graph-row tall-graph">
              <div class="row-title">SET vs ACT THICKNESS</div>

              <div class="graph-placeholder large">
                <Line :data="thicknessChartData" :options="chartOptions" />
              </div>
            </div>

            <!-- MELT TEMPERATURE -->
            <div class="row graph-row tall-graph">
              <div class="graph-header">
                <div class="graph-title">MELT TEMPERATURE</div>
                <div class="inline-value temperature">
                  {{
                    meltTemperatureTrend.length
                      ? meltTemperatureTrend[meltTemperatureTrend.length - 1].y.toFixed(1)
                      : "0"
                  }} °C
                </div>
              </div>

              <div class="graph-placeholder">
                <Line :data="meltTemperatureChartData" :options="chartOptions" />
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
import ChartDataLabels from "chartjs-plugin-datalabels";

ChartJS.register(
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend,
  ChartDataLabels
);

const MAX_POINTS = 30;

export default {
  name: "Layer1",
  components: { Line },

  data() {
    return {
      currentDate: "",
      currentTime: "",

      speed: 0,
      yieldVal: 0,
      ampere: 0,

      meltPressureTrend: [],
      meltTemperatureTrend: [],
      thicknessSetTrend: [],
      thicknessActualTrend: [],

      graphSeeded: false,
      _telemetryHandler: null
    };
  },

  mounted() {
    this.updateClock();
    setInterval(this.updateClock, 1000);

    this._telemetryHandler = this.onTelemetry;
    socket.on("telemetry_update", this._telemetryHandler);
  },

  beforeUnmount() {
    if (this._telemetryHandler) {
      socket.off("telemetry_update", this._telemetryHandler);
    }
  },

  methods: {

    /* ================= SOCKET ================= */
    onTelemetry(data) {
      const layer = data.layer_data?.layer1;
      const trends = data.layer_trends?.layer1;
      if (!layer || !trends) return;

      // ===== KPIs =====
      this.speed = layer.speed ?? this.speed;
      this.yieldVal = layer.yield ?? this.yieldVal;
      this.ampere = layer.ampere ?? this.ampere;

      const now = Date.now();
      const intervalSeconds = 10;

      /* ================= INITIAL SEED ================= */
      if (!this.graphSeeded) {

        const buildSeries = (values) => {
          if (!values || values.length === 0) return [];

          const start = now - (values.length - 1) * intervalSeconds * 1000;

          return values.slice(-MAX_POINTS).map((v, i) => {
            const t = new Date(start + i * intervalSeconds * 1000);
            return {
              x: t.toLocaleTimeString("en-GB", {
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit"
              }),
              y: v
            };
          });
        };

        this.meltPressureTrend = buildSeries(trends.melt_pressure);
        this.meltTemperatureTrend = buildSeries(trends.melt_temperature);
        this.thicknessSetTrend = buildSeries(trends.thickness_set);
        this.thicknessActualTrend = buildSeries(trends.thickness_actual);

        this.graphSeeded = true;
        return;  // important
      }

      /* ================= LIVE UPDATE ================= */

      const timeLabel = new Date().toLocaleTimeString("en-GB", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
      });

      const pushPoint = (arr, value) => {
        arr.push({ x: timeLabel, y: value });
        if (arr.length > MAX_POINTS) arr.shift();
      };

      pushPoint(this.meltPressureTrend, trends.melt_pressure?.at(-1));
      pushPoint(this.meltTemperatureTrend, trends.melt_temperature?.at(-1));
      pushPoint(this.thicknessSetTrend, trends.thickness_set?.at(-1));
      pushPoint(this.thicknessActualTrend, trends.thickness_actual?.at(-1));
    },

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
      this.currentTime = d.toLocaleTimeString("en-GB", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
      });
    }
  },

  computed: {
    meltPressureChartData() {
      return {
        labels: this.meltPressureTrend.map(p => p.x),
        datasets: [{
          label: "Melt Pressure (Bar)",
          data: this.meltPressureTrend.map(p => p.y),
          borderColor: "#7fdcff",
          tension: 0.35,
          pointRadius: 3
        }]
      };
    },

    meltTemperatureChartData() {
      return {
        labels: this.meltTemperatureTrend.map(p => p.x),
        datasets: [{
          label: "Melt Temperature (°C)",
          data: this.meltTemperatureTrend.map(p => p.y),
          borderColor: "#ffb74d",
          tension: 0.35,
          pointRadius: 3
        }]
      };
    },

    thicknessChartData() {
      const labels = this.thicknessActualTrend.map(p => p.x);
      const setValue = this.thicknessSetTrend.length
        ? this.thicknessSetTrend[this.thicknessSetTrend.length - 1].y
        : 0;

      return {
        labels,
        datasets: [
          {
            label: "Actual Thickness",
            data: this.thicknessActualTrend.map(p => p.y),
            borderColor: "#ff7043",
            tension: 0.3,
            pointRadius: 3
          },
          {
            label: "Set Thickness",
            data: labels.map(() => setValue),
            borderColor: "#4dd0e1",
            borderDash: [6, 4],
            pointRadius: 0
          }
        ]
      };
    },

    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        plugins: {
          legend: {
            labels: { color: "#e6f7fb", font: { size: 11 } }
          },
          datalabels: {
            color: "#ffffff",
            align: "top",
            anchor: "end",
            font: { weight: "bold", size: 10 },
            formatter: (value, context) => {
              const dataset = context.chart.data.datasets[0].data;
              return context.dataIndex === dataset.length - 1
                ? Number(value).toFixed(1)
                : "";
            }
          }
        },
        scales: {
          x: {
            title: { display: true, text: "Time", color: "#e6f7fb" },
            ticks: { color: "#cfefff" }
          },
          y: {
            title: { display: true, text: "Value", color: "#e6f7fb" },
            ticks: { color: "#cfefff" }
          }
        }
      };
    }
  }
};
</script>



<style scoped>

/* ================= HEADER ================= */

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
  transition: transform 0.2s ease, box-shadow 0.25s ease, background-color 0.25s ease;
}

.back-icon:hover {
  transform: scale(1.08);
  background: rgba(0, 255, 160, 0.22);
  box-shadow: 0 0 14px rgba(0, 255, 160, 0.45),
              inset 0 0 0 1px rgba(255,255,255,0.35);
}

.back-icon:active {
  transform: scale(0.96);
}

/* ================= CONTENT STRUCTURE FIX ================= */

.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;            /* 🔴 critical */
  overflow: hidden;
}

.panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;            /* 🔴 critical */
  overflow: hidden;
}

/* ================= METRIC CARDS ================= */

.stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(180px, 220px));
  justify-content: center;
  gap: 18px;
  margin-bottom: 20px;
}

.stat {
  position: relative;
  padding: 14px 14px;
  min-height: 72px;
  border-radius: 14px;

  background: linear-gradient(
    180deg,
    rgba(255,255,255,0.16),
    rgba(255,255,255,0.07)
  );

  text-align: center;
  font-size: 17px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  color: #d9f2f8;

  backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.14);

  box-shadow:
    0 8px 18px rgba(0,0,0,0.30),
    inset 0 1px 0 rgba(255,255,255,0.22);

  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.stat::before {
  content: "";
  position: absolute;
  inset: -6px;
  border-radius: 18px;
  border: 1px solid rgba(255,255,255,0.14);
  background: rgba(255,255,255,0.02);
  pointer-events: none;
}

.stat span {
  display: block;
  margin-top: 6px;
  font-size: 18px;
  font-weight: 800;
}

.stats .stat:nth-child(1) span { color: #7fdcff; }
.stats .stat:nth-child(2) span { color: #6ee7b7; }
.stats .stat:nth-child(3) span { color: #eaec6e; }

/* ================= GRAPH LAYOUT FIX ================= */

/* Stack vertically but prevent overflow */
.dual-graph-row {
  display: flex;
  flex-direction: column;
  gap: 16px;
  flex: 1;
  min-height: 0;         
}

/* Each graph card */
.graph-row {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;         
}

/* Header section */
.graph-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
  flex: 0 0 auto;
}

.graph-title {
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.6px;
  color: #e6f7fb;
}

/* Graph container */
.graph-placeholder {
  flex: 1;
  min-height: 0;            
  width: 100%;
  border-radius: 14px;
  background: rgba(255,255,255,0.14);
  padding: 8px 12px 12px;
  overflow: hidden;
}

/* Remove forced height */
.graph-placeholder.large {
  height: auto !important;
}

/* Force canvas containment */
.graph-placeholder canvas {
  width: 100% !important;
  height: 100% !important;
}

/* ================= INLINE LIVE VALUE ================= */

.inline-value {   
  padding: 3px 10px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.3px;
  backdrop-filter: blur(6px);
  border: 1px solid rgba(255,255,255,0.22);
  box-shadow:
    inset 0 0 0 1px rgba(255,255,255,0.18),
    0 2px 6px rgba(0,0,0,0.25);
  flex-shrink: 0;
}

.inline-value.pressure {
  color: #7fdcff;
  background: rgba(127, 220, 255, 0.16);
}

.inline-value.temperature {
  color: #ffb74d;
  background: rgba(255, 183, 77, 0.16);
}

</style>

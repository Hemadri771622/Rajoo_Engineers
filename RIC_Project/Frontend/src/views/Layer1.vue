<template>
  <div class="app">

    <Sidebar />

    <main class="main">

      <Header />

      <div class="content">

        <section class="panel left-panel">

          <h2>LAYER 1</h2>

          <!-- ================= KPI CARDS ================= -->

          <div class="stats">

            <div class="stat">

              SPEED

              <span>
                {{ layer.speed?.toFixed(3) || "0.000" }} RPM
              </span>

            </div>

            <div class="stat">

              YIELD

              <span>
                {{ layer.yield?.toFixed(3) || "0.000" }} kg/hr
              </span>

            </div>

            <div class="stat">

              AMPERE

              <span>
                {{ layer.ampere?.toFixed(1) || "0.0" }} A
              </span>

            </div>

            <div class="stat">

              MELT PRESSURE

              <span>
                {{ layer.melt_pressure?.toFixed(1) || "0.0" }} BAR
              </span>

            </div>

            <div class="stat">

              MELT TEMP

              <span>
                {{ layer.melt_temperature?.toFixed(1) || "0.0" }} °C
              </span>

            </div>

          </div>

          <!-- ================= GRAPHS ================= -->

          <div class="dual-graph-row">

            <!-- ================= FLOW RATE ================= -->

            <div class="graph-row tall-graph">

              <div class="graph-header">

                <div class="graph-title">
                  FLOW RATE
                </div>

              </div>

              <div class="graph-placeholder">

                <Line
                  :data="flowRateChartData"
                  :options="flowOptions"
                />

              </div>

            </div>

            <!-- ================= YIELD ================= -->

            <div class="graph-row tall-graph">

              <div class="graph-header">

                <div class="graph-title">
                  YIELD
                </div>

              </div>

              <div class="graph-placeholder">

                <Line
                  :data="yieldChartData"
                  :options="yieldOptions"
                />

              </div>

            </div>

            <!-- ================= THICKNESS ================= -->

            <div class="graph-row tall-graph">

              <div class="row-title">
                THICKNESS
              </div>

              <div class="graph-placeholder large">

                <Line
                  :data="thicknessChartData"
                  :options="thicknessOptions"
                />

              </div>

            </div>

          </div>

        </section>

      </div>

    </main>

  </div>
</template>

<script>
import { telemetry } from "@/stores/telemetryStore";
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
import Sidebar from "../components/Sidebar.vue";
import Header from "../components/Header.vue";

ChartJS.register(
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
);

export default {
  name: "Layer1",
  components: { Line, Sidebar, Header },

  data() {
    return {
      telemetry,
      currentDate: "",
      currentTime: ""
    };
  },

  mounted() {
    this.updateClock();
    setInterval(this.updateClock, 1000);
  },

  methods: {
    updateClock() {
      const d = new Date();
      this.currentDate = d.toLocaleDateString("en-GB");
      this.currentTime = d.toLocaleTimeString("en-GB");
    },

    makeTime(len) {
      return Array.from({ length: len }, (_, i) =>
        new Date(Date.now() - (len - i - 1) * 5000)
          .toLocaleTimeString("en-GB")
      );
    }
  },

  computed: {
    layer() {
      return this.telemetry.layers.layer1 || {};
    },

    trends() {
      return this.telemetry.layerTrends.layer1 || {};
    },

    /* ===== LABELS ===== */
    flow_labels() {
      return this.makeTime(this.trends.flow_rate?.length || 0);
    },

    yield_labels() {
      return this.makeTime(this.trends.yield?.length || 0);
    },

    thickness_labels() {
      return this.makeTime(this.trends.thickness?.length || 0);
    },

    /* ===== DATA ===== */
    flowRateChartData() {
      return {
        labels: this.flow_labels,
        datasets: [
          {
            label: "Flow Rate",
            data: this.trends.flow_rate || [],
            borderColor: "#64ffda",
            tension: 0.35
          }
        ]
      };
    },

    yieldChartData() {
      return {
        labels: this.yield_labels,
        datasets: [
          {
            label: "Yield",
            data: this.trends.yield || [],
            borderColor: "#6ee7b7",
            tension: 0.35
          }
        ]
      };
    },

    thicknessChartData() {
      return {
        labels: this.thickness_labels,
        datasets: [
          {
            label: "Thickness",
            data: this.trends.thickness || [],
            borderColor: "#ff7043",
            tension: 0.35
          }
        ]
      };
    },

    /* ===== BASE OPTIONS ===== */
    baseOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,

        layout: {
          padding: {
            left: 5,
            right: 10
          }
        },

        plugins: {
          legend: {
            labels: {
              color: "#e6f7fb",
              font: { size: 10 }
            }
          }
        },

        scales: {
          x: {
            ticks: {
              color: "#cfefff",
              font: { size: 9 },
              maxRotation: 0,
              autoSkip: true,
              maxTicksLimit: 6
            },
            title: {
              display: true,
              text: "Time",
              color: "#9fdfff",
              font: { size: 10 }
            }
          },

          y: {
            ticks: {
              color: "#cfefff",
              font: { size: 10 },
              maxTicksLimit: 5
            },
            title: {
              display: true,
              text: "",   
              color: "#9fdfff",
              font: { size: 9 }
            }
          }
        }
      };
    },

    /* ===== CUSTOM OPTIONS (ONLY UNITS) ===== */
    flowOptions() {
      return {
        ...this.baseOptions,
        scales: {
          ...this.baseOptions.scales,
          y: {
            ...this.baseOptions.scales.y,
            title: {
              display: true,
              text: " kg/hr ",
              color: "#9fdfff",
              font: { size: 9 }
            }
          }
        }
      };
    },

    yieldOptions() {
      return {
        ...this.baseOptions,
        scales: {
          ...this.baseOptions.scales,
          y: {
            ...this.baseOptions.scales.y,
            title: {
              display: true,
              text: " kg/hr ",
              color: "#9fdfff",
              font: { size: 9 }
            }
          }
        }
      };
    },

    thicknessOptions() {
      return {
        ...this.baseOptions,
        scales: {
          ...this.baseOptions.scales,
          y: {
            ...this.baseOptions.scales.y,
            title: {
              display: true,
              text: " µm ",
              color: "#9fdfff",
              font: { size: 9 }
            }
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

/* .back-icon {
  width: 42px;
  height: 42px;
  cursor: pointer;
  border-radius: 50%;
  padding: 6px;
  background: rgba(0, 255, 160, 0.12);
  backdrop-filter: blur(6px);
  transition: transform 0.2s ease, box-shadow 0.25s ease, background-color 0.25s ease;
} */

/* .back-icon:hover {
  transform: scale(1.08);
  background: rgba(0, 255, 160, 0.22);
  box-shadow: 0 0 14px rgba(0, 255, 160, 0.45),
              inset 0 0 0 1px rgba(255,255,255,0.35);
}

.back-icon:active {
  transform: scale(0.96);
} */

/* ================= CONTENT STRUCTURE FIX ================= */

.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

/* ================= METRIC CARDS ================= */

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); 
  justify-content: center;
  gap: 10px;  
  margin-bottom: 14px;
}

.stat {
  position: relative;
  padding: 8px 10px;  
  min-height: 55px;    
  border-radius: 10px;

  background: linear-gradient(
    180deg,
    rgba(255,255,255,0.14),
    rgba(255,255,255,0.05)
  );

  text-align: center;
  font-size: 13px;  
  font-weight: 600;
  letter-spacing: 0.4px;
  text-transform: uppercase;
  color: #d9f2f8;

  backdrop-filter: blur(5px);
  border: 1px solid rgba(255,255,255,0.10);

  box-shadow:
    0 4px 10px rgba(0,0,0,0.25),
    inset 0 1px 0 rgba(255,255,255,0.15);

  transition: transform 0.2s ease;
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
  margin-top: 3px;
  font-size: 14px;   
  font-weight: 700;
}

.stats .stat:nth-child(1) span { color: #6ee7b7;  }
.stats .stat:nth-child(2) span { color: #6ee7b7; }
.stats .stat:nth-child(3) span { color: #6ee7b7; }
.stats .stat:nth-child(4) span { color: #6ee7b7; }
.stats .stat:nth-child(5) span { color: #6ee7b7; }

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
  /* background: rgba(255,255,255,0.14); */
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

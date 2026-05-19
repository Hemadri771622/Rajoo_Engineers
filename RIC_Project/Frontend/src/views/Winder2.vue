<template>
  <div class="app">
    <Sidebar />

    <main class="main">
      <Header />

      <div class="content">
        <section class="panel left-panel">

          <h2>WINDER 1</h2>

          <!-- KPI SECTION -->
          <div class="stats centered">

            <!-- TOTALIZER -->
            <div class="stat">
              <div class="kpi-title">TOTALIZER</div>

              <div class="kpi-value">
                {{ (telemetry.winders.winder1.totalizer ?? 0).toFixed(3) }}

                <span class="kpi-unit-inline">m</span>
              </div>
            </div>

            <!-- NUMBER OF ROLLS -->
            <div class="stat">
              <div class="kpi-title">NUMBER OF ROLLS</div>

              <div class="kpi-value">
                {{ telemetry.winders.winder1.number_of_rolls ?? 0 }}
              </div>
            </div>

          </div>

          <!-- ROLL LENGTH -->
          <div class="graph-section graph-row">

            <div class="graph-header">

              <div class="graph-title">
                ROLL LENGTH
              </div>

              <div class="graph-value">
                {{
                  (telemetry.winderTrends.winder1.roll_length?.slice(-1)[0] ?? 0).toFixed(3)
                }} m
              </div>

            </div>

            <div class="graph-card">
              <Line :data="rollLengthChartData" :options="getChartOptions('Length')" />
            </div>

          </div>

          <!-- ROLL DIAMETER -->
          <div class="graph-section graph-row">

            <div class="graph-header">

              <div class="graph-title">
                ROLL DIAMETER
              </div>

              <div class="graph-value">
                {{
                  (telemetry.winderTrends.winder1.roll_dia?.slice(-1)[0] ?? 0).toFixed(3)
                }} mm
              </div>

            </div>

            <div class="graph-card">
              <Line :data="rollDiaChartData" :options="getChartOptions('Diameter')" />
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
  name: "Winder2",

  components: {
    Sidebar,
    Header,
    Line
  },

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

  computed: {

    trends() {
      return this.telemetry.winderTrends.winder2 || {};
    },

    rollLengthChartData() {

      const data = this.trends.roll_length || [];

      const visibleData = data.slice(-30);

      return {

        labels: this.generateTimeLabels(visibleData.length),

        datasets: [
          {
            label: "Roll Length",

            data: visibleData,

            borderColor: "#7fdcff",

            backgroundColor: "rgba(127,220,255,0.12)",

            tension: 0.35,

            fill: true,

            pointRadius: 1.2,

            borderWidth: 3
          }
        ]
      };
    },

    rollDiaChartData() {

      const data = this.trends.roll_dia || [];

      const visibleData = data.slice(-30);

      return {

        labels: this.generateTimeLabels(visibleData.length),

        datasets: [
          {
            label: "Roll Diameter",

            data: visibleData,

            borderColor: "#4dd0e1",

            backgroundColor: "rgba(77,208,225,0.12)",

            tension: 0.35,

            fill: true,

            pointRadius: 1.2,

            borderWidth: 3
          }
        ]
      };
    }
  },

  methods: {

    updateClock() {

      const d = new Date();

      this.currentDate = d.toLocaleDateString("en-GB");

      this.currentTime = d.toLocaleTimeString("en-GB");
    },

    generateTimeLabels(length) {

      const labels = [];

      const now = new Date();

      for (let i = length - 1; i >= 0; i--) {

        const t = new Date(now.getTime() - (i * 5000));

        labels.push(
          t.toLocaleTimeString("en-GB", {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit"
          })
        );
      }

      return labels;
    },

    getChartOptions(yAxisLabel) {

      return {

        responsive: true,

        maintainAspectRatio: false,

        animation: false,

        interaction: {
          mode: "index",
          intersect: false
        },

        plugins: {

          legend: {

            labels: {
              color: "#e6f7fb",

              font: {
                size: 12
              }
            }
          },

          tooltip: {
            enabled: true
          }
        },

        elements: {

          point: {
            radius: 1.2,
            hoverRadius: 4
          },

          line: {
            borderWidth: 3
          }
        },

        scales: {

          x: {

            title: {
              display: true,

              text: "Timestamp",

              color: "#e6f7fb",

              font: {
                size: 14,
                weight: "bold"
              }
            },

            ticks: {
              color: "#cfefff",

              autoSkip: true,

              maxTicksLimit: 10,

              maxRotation: 0,

              minRotation: 0
            },

            grid: {
              color: "rgba(255,255,255,0.06)"
            }
          },

          y: {

            title: {
              display: true,

              text: yAxisLabel,

              color: "#e6f7fb",

              font: {
                size: 14,
                weight: "bold"
              }
            },

            ticks: {
              color: "#cfefff"
            },

            grid: {
              color: "rgba(255,255,255,0.06)"
            }
          }

        }
      };
    }
  }
};
</script>


<style scoped>

/* ================= CONTENT STRUCTURE ================= */

.content {
  flex: 1;
  display: flex;
  flex-direction: column;

  min-height: 0;

  overflow: hidden;

  padding: 12px;
}

.panel {
  flex: 1;

  display: flex;
  flex-direction: column;

  min-height: 0;

  overflow: hidden;
}

h2 {
  color: #e6f7fb;

  font-size: 24px;
  font-weight: 800;

  margin-bottom: 12px;

  letter-spacing: 1px;
}

/* ================= KPI SECTION ================= */

.stats.centered {
  display: flex;

  justify-content: center;

  align-items: stretch;

  gap: 28px;

  margin: 2px 0 12px 0;
}

.stat {
  width: 20%;

  min-height: 64px;

  padding: 8px 20px;

  border-radius: 18px;

  background: linear-gradient(
    180deg,
    #4a5f6b,
    #3a4d57
  );

  text-align: center;

  box-shadow:
    0 4px 14px rgba(0, 0, 0, 0.25);
}

.kpi-title {
  font-size: 11px;

  opacity: 0.82;

  color: #dff9ff;

  margin-bottom: 2px;

  letter-spacing: 0.5px;
}

.kpi-value {
  display: flex;

  justify-content: center;

  align-items: baseline;

  gap: 6px;

  font-size: 22px;

  font-weight: 900;

  color: #7fffd4;

  line-height: 1;
}

.kpi-unit-inline {
  font-size: 14px;

  color: #7fffd4;

  font-weight: 700;
}

/* ================= GRAPH SECTION ================= */

.graph-section {
  display: flex;

  flex-direction: column;

  gap: 12px;

  margin-top: 14px;

  padding: 14px;

  border-radius: 22px;

  background: linear-gradient(
    90deg,
    rgba(7, 28, 42, 0.92),
    rgba(11, 35, 48, 0.92)
  );
}

.graph-header {
  display: flex;

  justify-content: space-between;

  align-items: center;

  padding: 0 6px;
}

.graph-title {
  color: #e6f7fb;

  font-size: 16px;

  font-weight: 800;

  letter-spacing: 0.6px;
}

.graph-value {
  background: rgba(255, 255, 255, 0.10);

  padding: 8px 18px;

  border-radius: 12px;

  color: #7fffd4;

  font-size: 16px;

  font-weight: 800;

  min-width: 120px;

  text-align: center;

  box-shadow:
    inset 0 0 0 1px rgba(255,255,255,0.05);
}

.graph-card {
  height: 560px;

  background: rgba(255, 255, 255, 0.10);

  border-radius: 22px;

  padding: 18px;

  backdrop-filter: blur(6px);
}

.graph-card canvas {
  width: 100% !important;

  height: 100% !important;
}

/* ================= RESPONSIVE ================= */

@media (max-width: 900px) {

  .stats.centered {
    flex-direction: column;

    align-items: center;
  }

  .stat {
    width: 90%;
  }

  .graph-card {
    height: 320px;
  }
}

@media (max-height: 800px) {

  .graph-card {
    height: 340px;
  }
}

</style>
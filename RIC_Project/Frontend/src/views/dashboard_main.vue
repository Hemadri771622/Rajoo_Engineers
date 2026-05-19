<template>
  <div class="app">
    <Sidebar />

    <main class="main">
      <header class="topbar">

        <div class="top-left">
          <h3>THREE LAYER BLOWN FILM LINE</h3>
        </div>

        <div class="top-kpi-wrapper">
          <div class="top-kpi-box stat">
            <div class="kpi-title">OEE</div>
            <div class="kpi-value">{{ oee ?? 'N/A' }}</div>
          </div>

          <div class="top-kpi-box stat">
            <div class="kpi-title">Availability</div>
            <div class="kpi-value">{{ availability ?? 'N/A' }}</div>
          </div>

          <div class="top-kpi-box stat">
            <div class="kpi-title">Performance</div>
            <div class="kpi-value">{{ performance ?? 'N/A' }}</div>
          </div>

          <div class="top-kpi-box stat">
            <div class="kpi-title">Quality</div>
            <div class="kpi-value">{{ quality ?? 'N/A' }}</div>
          </div>
        </div>

        <div class="top-right">

          <!-- RAJOO LOGO -->
          <div class="rajoo-logo-box">
            <img src="/rajoo_logo.png" alt="Rajoo Logo" />
          </div>

          <span class="pill dark">
            {{ currentDate }}<br />
            {{ currentTime }}
          </span>
          
          

          <div class="notification-icon">
            <span class="material-icons">notifications</span>
          </div>

          <div class="power-icon" @click="handleLogout">
            <span class="material-icons">power_settings_new</span>
          </div>
        </div>
      </header>

      <div class="content">
        <section class="panel left-panel">
          <h2>MACHINE OVERVIEW PANEL</h2>

          <!-- STATS -->
          <div class="stats">
            <div class="stat">
              Total Set Output
              <span>{{ telemetry.machine.total_set_output.toFixed(3) }} kg/hr</span>
            </div>

            <div class="stat">
              Total Actual Output
              <span>{{ telemetry.machine.total_actual_output.toFixed(3) }} kg/hr</span>
            </div>

            <div class="stat">
              Density
              <span>{{ telemetry.machine.density.toFixed(3) }} g/cm³</span>
            </div>

            <div class="stat">
              GSM
              <span>{{ telemetry.machine.gsm.toFixed(3) }}</span>
            </div>

            <div class="stat">
              Lay Flat
              <span>{{ telemetry.machine.lay_flat.toFixed(3) }} mm</span>
            </div>

            <div class="stat">
              Valve Position
              <span>{{ (telemetry.machine.valve_position ?? 0).toFixed(3) }} %</span>
            </div>
          </div>

          <!-- THICKNESS GRAPH MOVED TO TOP -->
          <div class="graph-section graph-row">
            <div class="graph-title">THICKNESS</div>

            <div class="thickness-content-full">
              <div class="thickness-graph-full">
                <Line :data="thicknessChartData" :options="thicknessOptions" />
              </div>

              <div class="thickness-info-full">
                <div><b>Set Thickness</b> : {{ telemetry.thickness?.set || 0 }}</div>
                <div><b>Average</b> : {{ telemetry.thickness?.avg || 0 }}</div>
                <div><b>Nominal</b> : {{ telemetry.thickness?.nominal || 0 }}</div>
                <div><b>Maximum</b> : {{ telemetry.thickness?.max || 0 }}</div>
                <div><b>Minimum</b> : {{ telemetry.thickness?.min || 0 }}</div>
              </div>
            </div>
          </div>

          <!-- FIXED CARDS -->
          <div class="control-cards">

            <div class="zone-card small">
              <h3>Tower Nip</h3>

              <div class="zone-row">
                <span>SET</span>
                <span>{{ telemetry.tower_nip?.set?.toFixed(3) || '0.000' }}</span>
              </div>

              <div class="zone-row">
                <span>ACT</span>
                <span>{{ telemetry.tower_nip?.actual?.toFixed(3) || '0.000' }}</span>
              </div>

              <div
                class="zone-row diff"
                :class="{ high: Math.abs((telemetry.tower_nip?.actual || 0) - (telemetry.tower_nip?.set || 0)) > 5 }"
              >
                <span>DIFF</span>
                <span>
                  {{
                    (
                      (telemetry.tower_nip?.actual || 0) -
                      (telemetry.tower_nip?.set || 0)
                    ).toFixed(3)
                  }}
                </span>
              </div>
            </div>

            <div class="zone-card small">
              <h3>Air Ring</h3>

              <div class="zone-row">
                <span>SET</span>
                <span>{{ telemetry.air_ring?.set?.toFixed(3) || '0.000' }}</span>
              </div>

              <div class="zone-row">
                <span>ACT</span>
                <span>{{ telemetry.air_ring?.actual?.toFixed(3) || '0.000' }}</span>
              </div>

              <div
                class="zone-row diff"
                :class="{ high: Math.abs((telemetry.air_ring?.actual || 0) - (telemetry.air_ring?.set || 0)) > 5 }"
              >
                <span>DIFF</span>
                <span>
                  {{
                    (
                      (telemetry.air_ring?.actual || 0) -
                      (telemetry.air_ring?.set || 0)
                    ).toFixed(3)
                  }}
                </span>
              </div>
            </div>

            <div class="zone-card small">
              <h3>Regeneration</h3>

              <div class="zone-row">
                <span>SET</span>
                <span>{{ telemetry.regeneration?.set?.toFixed(3) || '0.000' }}</span>
              </div>

              <div class="zone-row">
                <span>ACT</span>
                <span>{{ telemetry.regeneration?.actual?.toFixed(3) || '0.000' }}</span>
              </div>

              <div
                class="zone-row diff"
                :class="{ high: Math.abs((telemetry.regeneration?.actual || 0) - (telemetry.regeneration?.set || 0)) > 5 }"
              >
                <span>DIFF</span>
                <span>
                  {{
                    (
                      (telemetry.regeneration?.actual || 0) -
                      (telemetry.regeneration?.set || 0)
                    ).toFixed(3)
                  }}
                </span>
              </div>
            </div>

            <div class="zone-card small">
              <h3>Reverse Haul-Off</h3>

              <div class="zone-row">
                <span>SET</span>
                <span>{{ telemetry.reverse_hauloff?.set?.toFixed(3) || '0.000' }}</span>
              </div>

              <div class="zone-row">
                <span>ACT</span>
                <span>{{ telemetry.reverse_hauloff?.actual?.toFixed(3) || '0.000' }}</span>
              </div>

              <div
                class="zone-row diff"
                :class="{ high: Math.abs((telemetry.reverse_hauloff?.actual || 0) - (telemetry.reverse_hauloff?.set || 0)) > 5 }"
              >
                <span>DIFF</span>
                <span>
                  {{
                    (
                      (telemetry.reverse_hauloff?.actual || 0) -
                      (telemetry.reverse_hauloff?.set || 0)
                    ).toFixed(3)
                  }}
                </span>
              </div>
            </div>

          </div>

          <!-- IBC + SPEED MOVED TO BOTTOM -->
          <div class="dual-graph-row">

            <div class="graph-section graph-row">
              <div class="graph-title">IBC TEMP IN / OUT</div>

              <div class="graph-card">
                <Line :data="ibcChartData" :options="ibcOptions" />
              </div>
            </div>

            <div class="graph-section graph-row">
              <div class="graph-title">SET vs ACT SPEED</div>

              <div class="graph-card">
                <Line :data="speedChartData" :options="speedOptions" />
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
import Sidebar from "../components/Sidebar.vue";


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

export default {
  name: "DashboardMain",
  components: { Line, Bar, Sidebar },

  data() {
    return {
      telemetry,

      currentDate: "",
      currentTime: "",

      oee: null,
      availability: null,
      performance: null,
      quality: null,

      clockInterval: null
    };
  },

  mounted() {
    this.updateClock();
    this.clockInterval = setInterval(this.updateClock, 1000);
  },

  beforeUnmount() {
    if (this.clockInterval) clearInterval(this.clockInterval);
  },

  methods: {
    updateClock() {
      const now = new Date();
      this.currentDate = now.toLocaleDateString("en-GB");
      this.currentTime = now.toLocaleTimeString("en-GB");
    },

    handleLogout() {
      localStorage.removeItem("token");
      this.$router.replace("/");
    },

    makeTime(len) {
      return Array.from({ length: len }, (_, i) =>
        new Date(Date.now() - (len - i - 1) * 10000)
          .toLocaleTimeString("en-GB")
      );
    }
  },

  computed: {
    /* ================= LABELS ================= */
    ibc_labels() {
      return this.makeTime(this.telemetry.ibc.in.length);
    },

    speed_labels() {
      return this.makeTime(this.telemetry.speed.set.length);
    },

    thickness_labels() {
      return this.makeTime(this.telemetry.thickness.trend.length);
    },

    /* ================= DATA ================= */
    ibcChartData() {
      return {
        labels: this.ibc_labels,
        datasets: [
          {
            label: "IBC IN",
            data: this.telemetry.ibc.in,
            borderColor: "#4dd0e1",
            tension: 0.35
          },
          {
            label: "IBC OUT",
            data: this.telemetry.ibc.out,
            borderColor: "#ff7043",
            tension: 0.35
          }
        ]
      };
    },

    speedChartData() {
      return {
        labels: this.speed_labels,
        datasets: [
          {
            label: "SET",
            data: this.telemetry.speed.set,
            borderColor: "#4dd0e1",
            tension: 0.35
          },
          {
            label: "ACT",
            data: this.telemetry.speed.actual,
            borderColor: "#ff7043",
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
            label: "Actual",
            data: this.telemetry.thickness.trend,
            borderColor: "#ff7043",
            tension: 0.35
          }
        ]
      };
    },

    /* ================= COMMON OPTIONS ================= */
    commonOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: { color: "#e6f7fb" }
          }
        },
        scales: {
          x: {
            ticks: { color: "#dff6ff" },
            title: {
              display: true,
              text: "Time",
              color: "#9fdfff",
              font: { size: 12, weight: "600" }
            }
          },
          y: {
            ticks: { color: "#dff6ff" },
            title: {
              display: true,
              text: "Value",
              color: "#9fdfff",
              font: { size: 12, weight: "600" }
            }
          }
        }
      };
    },

    /* ================= CUSTOM GRAPH OPTIONS ================= */

    ibcOptions() {
      return {
        ...this.commonOptions,
        scales: {
          ...this.commonOptions.scales,
          y: {
            ...this.commonOptions.scales.y,
            title: {
              display: true,
              text: "Temperature (°C)",
              color: "#9fdfff"
            }
          }
        }
      };
    },

    speedOptions() {
      return {
        ...this.commonOptions,
        scales: {
          ...this.commonOptions.scales,
          y: {
            ...this.commonOptions.scales.y,
            title: {
              display: true,
              text: "Speed",
              color: "#9fdfff"
            }
          }
        }
      };
    },

    thicknessOptions() {
      return {
        ...this.commonOptions,
        scales: {
          ...this.commonOptions.scales,
          y: {
            ...this.commonOptions.scales.y,
            title: {
              display: true,
              text: "µm",
              color: "#9fdfff"
            }
          }
        }
      };
    }
  }
};
</script>



<style scoped>

.stat {
  padding: 5px !important;
  min-height: max-content !important;
  font-size: 14px !important;
}

/* ================= TOP BAR ================= */
.topbar {
  height: max-content;
  min-height: 60px;
  flex-shrink: 0;
  padding: 10px 16px;
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

/* ================= STATS ================= */
.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(90px, 1fr));
  gap: 18px;
  margin-bottom: 10px;
  justify-content: center;
}

.stat {
  background: rgba(255,255,255,0.12);
  border-radius: 10px;
  padding: 8px 6px;        
  text-align: center;
  font-size: 12px;         
  min-height: 50px;
}

.stat span {
  display: block;
  margin-top: 2px;        
  font-size: 14px;        
  font-weight: 500;       
}

.stats .stat:nth-child(1) span { color: #6ee7b7;  }
.stats .stat:nth-child(2) span { color: #6ee7b7; }
.stats .stat:nth-child(3) span { color: #6ee7b7; }
.stats .stat:nth-child(4) span { color: #6ee7b7; }
.stats .stat:nth-child(5) span { color: #6ee7b7; }
.stats .stat:nth-child(6) span { color: #6ee7b7;  }


/* ================= ROW ================= */ 
.row {
  /* background: rgba(255,255,255,0.1); */
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
  height: 175px;              
  padding: 4px 8px 10px 8px;  
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




/* ================= TOP KPI BOXES ================= */

.top-kpi-wrapper {
  display: flex;
  gap: 20px;
  align-items: center;

  margin-left: -100px;
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

.control-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr); 
  gap: 15px;
  margin: 10px 0 15px 0;
}


.zone-card.small {
  padding: 14px;
  border-radius: 12px;
  text-align: center;

  background: linear-gradient(
    180deg,
    rgba(255,255,255,0.14),
    rgba(255,255,255,0.06)
  );

  border: 1px solid rgba(255,255,255,0.15);
  backdrop-filter: blur(6px);

  color: #e6f7fb;
}

.zone-card.small h3 {
  font-size: 14px;
  margin-bottom: 8px;
  color: #cfefff;
}

.zone-card.small .row {
  display: flex;
  justify-content: space-between;
  margin-top: 6px;
  font-size: 13px;


  background: transparent !important;
  padding: 0 !important;
}

.zone-card.small .diff {
  font-weight: 700;
  color: #6ee7b7;
}

.zone-card.small .diff.high {
  color: #ff5252;
}

.zone-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 6px;
  font-size: 13px;

  flex-direction: row !important;
  padding: 0 !important;
  background: transparent !important;
}

/* RAJOO LOGO BOX */
.rajoo-logo-box {
  display: flex;
  align-items: center;
  justify-content: center;

  height: 52px;

  padding: 0 14px;

  border-radius: 14px;

  background: rgba(255,255,255,0.07);

  border: 1px solid rgba(255,255,255,0.10);

  backdrop-filter: blur(8px);

  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.06),
    0 0 10px rgba(77,208,225,0.08);
}

/* LOGO IMAGE */
.rajoo-logo-box img {
  height: 34px;
  width: auto;

  object-fit: contain;

  display: block;
}
</style>

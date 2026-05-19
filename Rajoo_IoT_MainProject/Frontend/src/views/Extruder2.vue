<template>
  <div class="app">

    <!-- ================= SIDEBAR ================= -->
    <aside class="sidebar">
      <div class="avatar">
        <img src="/user-icon.png" />
      </div>

      <div class="menu-section">
        <div class="menu-title">LAYERS</div>
        <button class="menu-item" @click="navigate('/layer1')">Layer 1</button>
        <button class="menu-item" @click="navigate('/layer2')">Layer 2</button>
        <button class="menu-item" @click="navigate('/layer3')">Layer 3</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">EXTRUDER</div>
        <button class="menu-item" @click="navigate('/extruder1')">Extruder A</button>
        <button class="menu-item active">Extruder B</button>
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

      <!-- ===== HEADER ===== -->
      <header class="topbar">
        <div class="top-left">
          <img src="/back-arrow.png" class="back-icon" @click="goBack" />
          <span class="page-title">THREE LAYER BLOWN FILM LINE</span>
        </div>

        <div class="top-right">
          <span class="pill dark">
            {{ currentDate }}<br />
            {{ currentTime }}
          </span>
          <img src="/notification.png" class="notification-icon" />
        </div>
      </header>

      <!-- ===== CONTENT ===== -->
      <div class="content">
        <section class="panel extruder-panel">
          <h2>EXTRUDER B</h2>

          <div class="material-visuals">

            <!-- KPI -->
            <div class="kpi-wrapper" v-if="materials.length">
              <div
                v-for="m in materials"
                :key="m.name"
                class="kpi-glass"
              >
                <div class="kpi-inner-glass">

                  <div class="kpi-title">
                    {{ m.name }}
                  </div>

                  <div class="kpi-set">
                    {{ m.setKg.toFixed(2) }} kg
                  </div>

                  <div
                    class="kpi-actual"
                    :class="{ high: m.actKg > m.setKg, low: m.actKg < m.setKg }"
                  >
                    {{ m.actKg.toFixed(2) }} kg
                  </div>

                </div>
              </div>
            </div>

            <!-- ================= COMPOSITION ================= -->
            <div class="visual-card">

              <div class="card-header-left">
                ACTUAL COMPOSITION (%)
              </div>

              <div class="chart-wrapper">
                <canvas ref="compositionChart"></canvas>
              </div>

            </div>

            <!-- ================= TEMPERATURE ================= -->
            <div class="visual-card">

              <div class="card-header-left">
                EXTRUDER TEMPERATURE COMPARISON
              </div>

              <div class="chart-wrapper">
                <canvas ref="tempBarChart"></canvas>
              </div>

            </div>

          </div>
        </section>
      </div>

      <!-- ===== FOOTER ===== -->
      <footer class="footer">
        MODEL : RFC-2550-40-1800
      </footer>

    </main>
  </div>
</template>




<!-- <script>
import Chart from "chart.js/auto";
import socket from "@/services/socket";

export default {
  name: "Extruder2",

  data() {
    return {
      currentDate: "",
      currentTime: "",
      clockInterval: null,

      materials: [],
      tempZones: [],

      compositionChart: null,
      tempBarChart: null,

      socketHandler: null
    };
  },

  mounted() {
    this.startClock();
    this.attachSocket();
  },

  activated() {
    this.attachSocket();
  },

  deactivated() {
    this.detachSocket();
  },

  beforeUnmount() {
    this.stopClock();
    this.detachSocket();
    this.destroyCharts();
  },

  methods: {

    /* ================= NAVIGATION ================= */

    navigate(path) {
      this.$router.push(path);
    },

    goBack() {
      this.$router.back();
    },

    /* ================= CLOCK ================= */

    startClock() {
      this.updateClock();
      this.clockInterval = setInterval(this.updateClock, 1000);
    },

    stopClock() {
      if (this.clockInterval) {
        clearInterval(this.clockInterval);
        this.clockInterval = null;
      }
    },

    updateClock() {
      const d = new Date();
      this.currentDate = d.toLocaleDateString("en-GB");
      this.currentTime = d.toLocaleTimeString("en-US");
    },

    /* ================= SOCKET ================= */

    attachSocket() {
      if (this.socketHandler) return;

      this.socketHandler = (payload) => {

        const safePayload = JSON.parse(JSON.stringify(payload));
        const extruder = safePayload?.extruders?.B;
        if (!extruder) return;

        this.materials = Object.entries(extruder.materials || {}).map(
          ([name, m]) => ({
            name,
            act: Number(m.act) || 0,
            setKg: Number(m.setKg) || 0,
            actKg: Number(m.actKg) || 0,
            color: m.color || "#00e5ff"
          })
        );

        this.tempZones = extruder.temperature || [];

        this.renderCharts();
      };

      socket.on("telemetry_update", this.socketHandler);
    },

    detachSocket() {
      if (!this.socketHandler) return;
      socket.off("telemetry_update", this.socketHandler);
      this.socketHandler = null;
    },

    /* ================= CHART MANAGEMENT ================= */

    destroyCharts() {
      if (this.compositionChart) {
        this.compositionChart.destroy();
        this.compositionChart = null;
      }

      if (this.tempBarChart) {
        this.tempBarChart.destroy();
        this.tempBarChart = null;
      }
    },

    renderCharts() {
      this.$nextTick(() => {

        this.destroyCharts();

        /* ===== COMPOSITION ===== */

        if (this.$refs.compositionChart) {
          this.compositionChart = new Chart(
            this.$refs.compositionChart,
            {
              type: "bar",
              data: {
                labels: ["Blend"],
                datasets: this.materials.map(m => ({
                  label: m.name,
                  data: [m.act],
                  backgroundColor: m.color
                }))
              },
              options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                animation: false,
                scales: {
                  x: { stacked: true, min: 0, max: 100 },
                  y: { stacked: true }
                }
              }
            }
          );
        }

        /* ===== TEMPERATURE ===== */

        if (this.$refs.tempBarChart) {
          this.tempBarChart = new Chart(
            this.$refs.tempBarChart,
            {
              type: "bar",
              data: {
                labels: this.tempZones.map(z => z.zone),
                datasets: [
                  {
                    label: "Set (°C)",
                    data: this.tempZones.map(z => z.set),
                    backgroundColor: "#00e5ff"
                  },
                  {
                    label: "Actual (°C)",
                    data: this.tempZones.map(z => z.act),
                    backgroundColor: "#ffb300"
                  }
                ]
              },
              options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: false
              }
            }
          );
        }

      });
    }

  }
};
</script> -->

<script>
import Chart from "chart.js/auto";
import socket from "@/services/socket";

export default {
  name: "Extruder2",

  data() {
    return {
      currentDate: "",
      currentTime: "",
      clockInterval: null,

      materials: [],
      tempZones: [],

      compositionChart: null,
      tempBarChart: null,

      socketHandler: null
    };
  },

  mounted() {
    this.startClock();
    this.attachSocket();
  },

  activated() {
    this.attachSocket();
  },

  deactivated() {
    this.detachSocket();
  },

  beforeUnmount() {
    this.stopClock();
    this.detachSocket();
    this.destroyCharts();
  },

  methods: {

    /* ================= NAVIGATION ================= */

    navigate(path) {
      this.$router.push(path);
    },

    goBack() {
      this.$router.back();
    },

    /* ================= CLOCK ================= */

    startClock() {
      this.updateClock();
      this.clockInterval = setInterval(this.updateClock, 1000);
    },

    stopClock() {
      if (this.clockInterval) {
        clearInterval(this.clockInterval);
        this.clockInterval = null;
      }
    },

    updateClock() {
      const d = new Date();
      this.currentDate = d.toLocaleDateString("en-GB");
      this.currentTime = d.toLocaleTimeString("en-US");
    },

    /* ================= SOCKET ================= */

    attachSocket() {
      if (this.socketHandler) return;

      this.socketHandler = (payload) => {

        const safePayload = JSON.parse(JSON.stringify(payload));
        const extruder = safePayload?.extruders?.B;
        if (!extruder) return;

        this.materials = Object.entries(extruder.materials || {}).map(
          ([name, m]) => ({
            name,
            act: Number(m.act) || 0,
            setKg: Number(m.setKg) || 0,
            actKg: Number(m.actKg) || 0,
            color: m.color || "#00e5ff"
          })
        );

        this.tempZones = extruder.temperature || [];

        this.renderCharts();
      };

      socket.on("telemetry_update", this.socketHandler);
    },

    detachSocket() {
      if (!this.socketHandler) return;
      socket.off("telemetry_update", this.socketHandler);
      this.socketHandler = null;
    },

    /* ================= CHART MANAGEMENT ================= */

    destroyCharts() {
      if (this.compositionChart) {
        this.compositionChart.destroy();
        this.compositionChart = null;
      }

      if (this.tempBarChart) {
        this.tempBarChart.destroy();
        this.tempBarChart = null;
      }
    },

    renderCharts() {
      this.$nextTick(() => {

        this.destroyCharts();

        /* ===== COMPOSITION ===== */

        if (this.$refs.compositionChart) {
          this.compositionChart = new Chart(
            this.$refs.compositionChart,
            {
              type: "bar",
              data: {
                labels: ["Blend"],
                datasets: this.materials.map(m => ({
                  label: m.name,
                  data: [m.act],
                  backgroundColor: m.color
                }))
              },
              options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                animation: false,

                scales: {
                  x: {
                    stacked: true,
                    min: 0,
                    max: 100,
                    ticks: {
                      color: "#bfe9ff",
                      font: {
                        size: 12,
                        weight: "600"
                      }
                    },
                    grid: {
                      color: "rgba(255,255,255,0.08)"
                    }
                  },
                  y: {
                    stacked: true,
                    ticks: {
                      color: "#bfe9ff",
                      font: {
                        size: 12,
                        weight: "600"
                      }
                    },
                    grid: {
                      display: false
                    }
                  }
                },

                plugins: {
                  legend: {
                    labels: {
                      color: "#9ecfff",
                      font: {
                        size: 12,
                        weight: "600"
                      }
                    }
                  }
                }
              }
            }
          );
        }

        /* ===== TEMPERATURE ===== */

        if (this.$refs.tempBarChart) {
          this.tempBarChart = new Chart(
            this.$refs.tempBarChart,
            {
              type: "bar",
              data: {
                labels: this.tempZones.map(z => z.zone),
                datasets: [
                  {
                    label: "Set (°C)",
                    data: this.tempZones.map(z => z.set),
                    backgroundColor: "#00e5ff"
                  },
                  {
                    label: "Actual (°C)",
                    data: this.tempZones.map(z => z.act),
                    backgroundColor: "#ffb300"
                  }
                ]
              },
              options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: false,

                scales: {
                  x: {
                    ticks: {
                      color: "#bfe9ff",
                      font: {
                        size: 12,
                        weight: "600"
                      }
                    },
                    grid: {
                      display: false
                    }
                  },
                  y: {
                    ticks: {
                      color: "#bfe9ff",
                      font: {
                        size: 12,
                        weight: "600"
                      }
                    },
                    grid: {
                      color: "rgba(255,255,255,0.08)"
                    }
                  }
                },

                plugins: {
                  legend: {
                    labels: {
                      color: "#9ecfff",
                      font: {
                        size: 12,
                        weight: "600"
                      }
                    }
                  }
                }
              }
            }
          );
        }

      });
    }

  }
};
</script>

<style scoped>

/* ================= HEADER ================= */

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
}

.top-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #9ecfff;
}

.back-icon {
  width: 36px;
  height: 36px;
  cursor: pointer;
  border-radius: 50%;
  padding: 6px;
  background: rgba(0, 255, 160, 0.12);
  transition: 0.2s ease;
}

.back-icon:hover {
  transform: scale(1.05);
  background: rgba(0, 255, 160, 0.18);
}


/* ================= DOUBLE GLASS KPI ================= */

.kpi-wrapper {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 28px;
  margin-bottom: 28px;
}

.kpi-glass {
  width: 190px;
  padding: 6px;
  border-radius: 18px;

  background: linear-gradient(
    145deg,
    rgba(255,255,255,0.08),
    rgba(255,255,255,0.02)
  );

  backdrop-filter: blur(12px);

  box-shadow:
    0 10px 28px rgba(0,0,0,0.45),
    inset 0 1px 1px rgba(255,255,255,0.18);

  transition: 0.25s ease;
}

.kpi-glass:hover {
  transform: translateY(-4px);
}

.kpi-inner-glass {
  border-radius: 14px;
  padding: 18px;
  text-align: center;

  background: linear-gradient(
    145deg,
    rgba(255,255,255,0.06),
    rgba(255,255,255,0.02)
  );

  box-shadow:
    inset 0 1px 2px rgba(255,255,255,0.15),
    inset 0 -2px 6px rgba(0,0,0,0.45);
}

.kpi-title {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.6px;
  color: #cfe9ff;
  margin-bottom: 6px;
}

.kpi-set {
  font-size: 15px;
  font-weight: 500;
  color: #7ed6ff;
}

.kpi-actual {
  font-size: 16px;
  font-weight: 700;
  margin-top: 6px;
}

.kpi-actual.high {
  color: #ff5c5c;
}

.kpi-actual.low {
  color: #3bffb3;
}


/* ================= CARDS ================= */

.visual-card {
  background: #081c2f;
  border-radius: 16px;
  padding: 14px 18px 18px 18px;
  margin-bottom: 24px;

  box-shadow:
    0 8px 25px rgba(0,0,0,0.4),
    inset 0 1px 1px rgba(255,255,255,0.05);
}


/* ================= LEFT ALIGNED GRAPH TITLE ================= */

.card-title,
.card-header-left {
  text-align: left;         
  font-size: 14px;
  font-weight: 600;
  color: #9ecfff;
  letter-spacing: 0.6px;
  margin-bottom: 8px;
  padding-left: 4px;
}


/* ================= GRAPH AREA (UNCHANGED HEIGHT) ================= */

.chart-wrapper {
  position: relative;
  height: 260px;   
}

.chart-wrapper canvas {
  position: absolute !important;
  width: 100% !important;
  height: 100% !important;
}

</style>
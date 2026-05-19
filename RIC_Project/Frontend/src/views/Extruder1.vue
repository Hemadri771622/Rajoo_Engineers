<template>
  <div class="app">

    <!-- ================= SIDEBAR ================= -->
    <Sidebar />

    <!-- ================= MAIN ================= -->
    <main class="main">

      <!-- ================= HEADER ================= -->
      <Header />

      <!-- ================= CONTENT ================= -->
      <div class="content">

        <section class="panel extruder-panel">

          <h2>EXTRUDER A</h2>

          <!-- ================= BLENDER + MIXER ================= -->

          <div class="summary-row">

            <div class="summary-card">

              <div class="summary-title">
                BLENDER WEIGHT
              </div>

              <div class="summary-value">
                {{ extruderBlender.toFixed(2) }} kg
              </div>

            </div>

            <div class="summary-card">

              <div class="summary-title">
                MIXER WEIGHT
              </div>

              <div class="summary-value">
                {{ extruderMixer.toFixed(2) }} kg
              </div>

            </div>

          </div>

          <!-- ================= COMPONENT TABLE ================= -->

          <div class="component-table-wrapper">

            <table class="component-table">

              <thead>

                <tr>

                  <th>Comp</th>
                  <th>Material</th>
                  <th>Density</th>
                  <th>SP%</th>
                  <th>PV%</th>
                  <th>Set KG</th>
                  <th>Act KG</th>
                  <th>Total KG</th>
                  <th>Dev</th>

                </tr>

              </thead>

              <tbody>

                <tr
                  v-for="m in materials"
                  :key="m.component"
                >

                  <td>
                    C{{ m.component }}
                  </td>

                  <td>

                    <span class="material-pill">
                      {{ m.name }}
                    </span>

                  </td>

                  <td>
                    {{ m.density.toFixed(3) }}
                  </td>

                  <td>
                    {{ m.setPct.toFixed(1) }}
                  </td>

                  <td>
                    {{ m.actPct.toFixed(1) }}
                  </td>

                  <td>
                    {{ m.setKg.toFixed(1) }}
                  </td>

                  <td>
                    {{ m.actKg.toFixed(1) }}
                  </td>

                  <td>
                    {{ m.totalKg.toFixed(1) }}
                  </td>

                  <td
                    :class="{
                      devHigh: m.deviation > 5,
                      devLow: m.deviation < -5
                    }"
                  >
                    {{ m.deviation.toFixed(1) }}
                  </td>

                </tr>

              </tbody>

            </table>

          </div>

          <!-- ================= KPI CARDS ================= -->

          <div class="stats" v-if="materials.length">

            <div
              v-for="m in materials"
              :key="m.name"
              class="stat"
            >

              <div class="kpi-title">
                {{ m.name }}
              </div>

              <div class="kpi-set">
                SET : {{ m.setKg.toFixed(2) }} kg
              </div>

              <div
                class="kpi-actual"
                :class="{
                  high: m.actKg > m.setKg,
                  low: m.actKg < m.setKg
                }"
              >
                ACT : {{ m.actKg.toFixed(2) }} kg
              </div>

            </div>

          </div>

          <!-- ================= TEMPERATURE KPI CARDS ================= -->

          <div class="graph-section graph-row">

            <div class="graph-title">
              EXTRUDER TEMPERATURE COMPARISON
            </div>

            <div class="control-cards">

              <div
                class="zone-card small"
                v-for="zone in tempZones"
                :key="zone.zone"
              >

                <h3>{{ zone.zone }}</h3>

                <div class="zone-row">
                  <span>SET</span>

                  <span>
                    {{ Number(zone.set).toFixed(1) }} °C
                  </span>
                </div>

                <div class="zone-row">
                  <span>ACT</span>

                  <span>
                    {{ Number(zone.act).toFixed(1) }} °C
                  </span>
                </div>

                <div
                  class="zone-row diff"
                  :class="{
                    high:
                      Math.abs(
                        Number(zone.act) -
                        Number(zone.set)
                      ) > 5
                  }"
                >

                  <span>DIFF</span>

                  <span>
                    {{
                      (
                        Number(zone.act) -
                        Number(zone.set)
                      ).toFixed(1)
                    }} °C
                  </span>

                </div>

              </div>

            </div>

          </div>

        </section>

      </div>

    </main>

  </div>
</template>

<script>

import socket from "@/services/socket";

import Sidebar from "../components/Sidebar.vue";
import Header from "../components/Header.vue";

export default {

  name: "Extruder1",

  components: {
    Sidebar,
    Header
  },

  data() {

    return {

      currentDate: "",
      currentTime: "",

      clockInterval: null,

      materials: [],

      tempZones: [],

      extruderBlender: 0,

      extruderMixer: 0,

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

      this.clockInterval = setInterval(
        this.updateClock,
        1000
      );
    },

    stopClock() {

      if (this.clockInterval) {

        clearInterval(this.clockInterval);

        this.clockInterval = null;
      }
    },

    updateClock() {

      const d = new Date();

      this.currentDate =
        d.toLocaleDateString("en-GB");

      this.currentTime =
        d.toLocaleTimeString("en-US");
    },

    /* ================= SOCKET ================= */

    attachSocket() {

      if (this.socketHandler) return;

      this.socketHandler = (payload) => {

        const extruder =
          payload?.extruders?.A;

        if (!extruder) return;

        /* ================= BLENDER + MIXER ================= */

        const blender =
          Number(extruder.blender_weight);

        if (
          !isNaN(blender) &&
          blender > 0
        ) {

          this.extruderBlender = blender;
        }

        const mixer =
          Number(extruder.mixer_weight);

        if (
          !isNaN(mixer) &&
          mixer > 0
        ) {

          this.extruderMixer = mixer;
        }

        /* ================= COMPONENTS ================= */

        (extruder.components || []).forEach((m, index) => {

          // ==========================================
          // CREATE OBJECT IF NOT EXISTS
          // ==========================================

          if (!this.materials[index]) {

            this.materials[index] = {

              component: index + 1,

              name: "UNKNOWN",

              density: 0,

              setPct: 0,

              actPct: 0,

              setKg: 0,

              actKg: 0,

              totalKg: 0,

              deviation: 0,

              color: "#00e5ff"
            };
          }

          // ==========================================
          // UPDATE EXISTING OBJECT
          // ==========================================

          const existing =
            this.materials[index];

          existing.component =
            m.component || index + 1;

          // ==========================================
          // STABLE MATERIAL NAME
          // ==========================================

          if (
            m.material_name !== null &&
            m.material_name !== undefined &&
            m.material_name !== "" &&
            m.material_name !== "UNKNOWN"
          ) {

            existing.name =
              m.material_name;
          }

          // ==========================================
          // STABLE DENSITY
          // ==========================================

          if (
            m.density !== null &&
            m.density !== undefined
          ) {

            existing.density =
              Number(m.density);
          }

          existing.setPct =
            Number(m.set_pct) || 0;

          existing.actPct =
            Number(m.act_pct) || 0;

          existing.setKg =
            Number(m.set_kg) || 0;

          existing.actKg =
            Number(m.act_kg) || 0;

          existing.totalKg =
            Number(m.total_kg) || 0;

          existing.deviation =
            Number(m.deviation) || 0;

          existing.color =
            Number(m.deviation) > 5
              ? "#ff5252"
              : Number(m.deviation) > 2
              ? "#ffc107"
              : "#00e5ff";
        });

        // ==========================================
        // FORCE REACTIVE UPDATE
        // ==========================================

        this.materials = [...this.materials];

        /* ================= TEMPERATURE ================= */

        (extruder.temperature || []).forEach((zone, index) => {

          // ==========================================
          // CREATE OBJECT IF NOT EXISTS
          // ==========================================

          if (!this.tempZones[index]) {

            this.tempZones[index] = {

              zone: zone.zone || `Z${index + 1}`,

              set: 0,

              act: 0
            };
          }

          // ==========================================
          // EXISTING OBJECT
          // ==========================================

          const existing =
            this.tempZones[index];

          // ==========================================
          // STABLE ZONE NAME
          // ==========================================

          if (
            zone.zone !== null &&
            zone.zone !== undefined &&
            zone.zone !== ""
          ) {

            existing.zone = zone.zone;
          }

          // ==========================================
          // STABLE SET TEMPERATURE
          // ==========================================

          const setTemp =
            Number(zone.set);

          if (!isNaN(setTemp)) {

            existing.set = setTemp;
          }

          // ==========================================
          // STABLE ACT TEMPERATURE
          // ==========================================

          const actTemp =
            Number(zone.act);

          if (!isNaN(actTemp)) {

            existing.act = actTemp;
          }
        });

        // ==========================================
        // FORCE REACTIVE UPDATE
        // ==========================================

        this.tempZones = [...this.tempZones];
      };

      socket.on(
        "telemetry_update",
        this.socketHandler
      );
    },

    detachSocket() {

      if (!this.socketHandler) return;

      socket.off(
        "telemetry_update",
        this.socketHandler
      );

      this.socketHandler = null;
    }
  }
};

</script>

<style scoped>

/* ================= SUMMARY ================= */

.summary-row {

  display: flex;

  gap: 20px;

  margin-bottom: 24px;
}

.summary-card {

  flex: 1;

  padding: 18px;

  border-radius: 18px;

  background: rgba(255,255,255,0.05);

  backdrop-filter: blur(12px);

  box-shadow:
    0 8px 24px rgba(0,0,0,0.35);

  text-align: center;
}

.summary-title {

  color: #9ecfff;

  font-size: 14px;

  margin-bottom: 10px;

  font-weight: 600;
}

.summary-value {

  color: #ffffff;

  font-size: 28px;

  font-weight: 700;
}

/* ================= TABLE ================= */

.component-table-wrapper {

  overflow-x: auto;

  margin-bottom: 28px;

  border-radius: 18px;

  background: rgba(255,255,255,0.04);

  backdrop-filter: blur(10px);

  padding: 14px;

  box-shadow:
    0 8px 24px rgba(0,0,0,0.35);
}

.component-table {

  width: 100%;

  border-collapse: collapse;

  color: #ffffff;
}

.component-table th {

  color: #9ecfff;

  font-size: 13px;

  font-weight: 700;

  padding: 14px;

  border-bottom:
    1px solid rgba(255,255,255,0.1);
}

.component-table td {

  padding: 14px;

  text-align: center;

  border-bottom:
    1px solid rgba(255,255,255,0.06);

  font-size: 14px;
}

.material-pill {

  background: rgba(0,229,255,0.12);

  color: #00e5ff;

  padding: 6px 12px;

  border-radius: 999px;

  font-size: 13px;

  font-weight: 700;
}

.devHigh {

  color: #ff5252;

  font-weight: 700;
}

.devLow {

  color: #00e676;

  font-weight: 700;
}

.stats {

  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(160px, 1fr));

  gap: 18px;

  margin-bottom: 28px;
}

.stat {

  padding: 14px;

  border-radius: 18px;

  background: linear-gradient(
    145deg,
    rgba(255,255,255,0.08),
    rgba(255,255,255,0.03)
  );

  backdrop-filter: blur(10px);

  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.06),
    0 6px 20px rgba(0,0,0,0.22);

  text-align: center;

  transition: 0.25s ease;
}

.stat:hover {

  transform: translateY(-3px);
}

.kpi-title {

  font-size: 14px;

  font-weight: 700;

  letter-spacing: 0.5px;

  color: #cfe9ff;

  margin-bottom: 8px;
}

.kpi-set {

  font-size: 14px;

  font-weight: 500;

  color: #7ed6ff;
}

.kpi-actual {

  font-size: 16px;

  font-weight: 700;

  margin-top: 8px;
}

.kpi-actual.high {

  color: #ff5c5c;
}

.kpi-actual.low {

  color: #3bffb3;
}

.graph-title {

  font-size: 15px;

  font-weight: 700;

  color: #9ecfff;

  letter-spacing: 0.6px;

  margin-bottom: 14px;

  padding-left: 4px;
}

.control-cards {

  display: grid;

  grid-template-columns: repeat(4, 1fr);

  gap: 18px;

  margin-top: 12px;
}

.zone-card.small {

  padding: 16px;

  border-radius: 18px;

  text-align: center;

  background: linear-gradient(
    180deg,
    rgba(255,255,255,0.14),
    rgba(255,255,255,0.06)
  );

  border: 1px solid rgba(255,255,255,0.14);

  backdrop-filter: blur(10px);

  color: #e6f7fb;

  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.08),
    0 6px 20px rgba(0,0,0,0.22);

  transition: 0.25s ease;
}

.zone-card.small:hover {

  transform: translateY(-3px);
}

.zone-card.small h3 {

  font-size: 16px;

  margin-bottom: 14px;

  color: #cfefff;

  font-weight: 700;
}

.zone-row {

  display: flex;

  justify-content: space-between;

  align-items: center;

  margin-top: 10px;

  font-size: 14px;

  color: #e6f7fb;
}

.zone-row.diff {

  margin-top: 14px;

  font-weight: 700;

  color: #6ee7b7;
}

.zone-row.diff.high {

  color: #ff5252;
}

</style>
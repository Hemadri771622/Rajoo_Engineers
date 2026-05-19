<template>
  <div class="layout">
    <Sidebar />

    <div class="main">
      <Header />

      <div class="content">
        <h2>Die Zone Temperature</h2>

        <!-- ✅ CORRECT LOOP -->
        <div class="zones">
          <div
            v-for="(zone, index) in telemetry.die || []"
            :key="index"
            class="zone-card"
          >
            <h3>Zone {{ index + 1 }}</h3>

            <!-- SET -->
            <div class="row">
              <span>SET</span>
              <span>{{ (zone.set ?? 0).toFixed(3) }} °C</span>
            </div>

            <!-- ACT -->
            <div class="row">
              <span>ACT</span>
              <span>{{ (zone.actual ?? 0).toFixed(3) }} °C</span>
            </div>

            <!-- DIFF -->
            <div
              class="row diff"
              :class="{
                high: Math.abs((zone.actual ?? 0) - (zone.set ?? 0)) > 5
              }"
            >
              <span>DIFF</span>
              <span>
                {{
                  ((zone.actual ?? 0) - (zone.set ?? 0)).toFixed(3)
                }} °C
              </span>
            </div>
          </div>
        </div>

      </div>

      <footer class="footer">
        MODEL :- RFCF-2550-40-1800
      </footer>
    </div>
  </div>
</template>

<script>
import { telemetry } from "@/stores/telemetryStore";
import Sidebar from "@/components/Sidebar.vue";
import Header from "@/components/Header.vue";

export default {
  name: "DieZoneTemperature",

  components: {
    Sidebar,
    Header,
  },

  setup() {
    return { telemetry };
  },
};
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
}

.main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.content {
  padding: 20px;
}

/* GRID */
.zones {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 15px;
}

/* CARD */
.zone-card {
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

/* TITLE */
.zone-card h3 {
  font-size: 14px;
  margin-bottom: 8px;
  color: #cfefff;
}

/* ROWS */
.row {
  display: flex;
  justify-content: space-between;
  margin-top: 6px;
  font-size: 13px;
}

/* DIFF NORMAL */
.diff {
  font-weight: 700;
  color: #6ee7b7;
}

/* DIFF ALERT */
.diff.high {
  color: #ff5252;
}

/* FOOTER */
.footer {
  margin-top: auto;
  text-align: center;
  padding: 10px;
  font-size: 16px;
  color: #c6f2ff;
}
</style>
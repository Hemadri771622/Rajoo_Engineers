import { reactive } from "vue";
import socket from "@/services/socket";

export const telemetry = reactive({

  // ================= DASHBOARD =================

  machine: {

    total_set_output: 0,

    total_actual_output: 0,

    density: 0,

    gsm: 0,

    lay_flat: 0,

    valve_position: 0
  },

  // ================= CONTROL KPIs =================

  tower_nip: {

    set: 0,

    actual: 0
  },

  air_ring: {

    set: 0,

    actual: 0
  },

  regeneration: {

    set: 0,

    actual: 0
  },

  reverse_hauloff: {

    set: 0,

    actual: 0
  },

  // ================= KPI CACHE =================

  kpis: {

    tower_set: 0,

    tower_act: 0,

    air_set: 0,

    air_act: 0,

    regen_set: 0,

    regen_act: 0,

    hauloff_set: 0,

    hauloff_act: 0,

    valve_act: 0
  },

  // ================= SPEED =================

  speed: {

    set: [],

    actual: []
  },

  // ================= IBC =================

  ibc: {

    in: [],

    out: []
  },

  // ================= THICKNESS =================

  thickness: {

    trend: []
  },

  // ================= DIE =================

  die: [],

  // ================= LAYERS =================

  layers: {

  layer1: {

    speed: 0,

    yield: 0,

    ampere: 0,

    melt_pressure: 0,

    melt_temperature: 0
  },

  layer2: {

    speed: 0,

    yield: 0,

    ampere: 0,

    melt_pressure: 0,

    melt_temperature: 0
  },

  layer3: {

    speed: 0,

    yield: 0,

    ampere: 0,

    melt_pressure: 0,

    melt_temperature: 0
  }
},

  layerTrends: {

    layer1: {

      thickness: [],

      melt_temperature: [],

      melt_pressure: []
    },

    layer2: {

      thickness: [],

      melt_temperature: [],

      melt_pressure: []
    },

    layer3: {

      thickness: [],

      melt_temperature: [],

      melt_pressure: []
    }
  },

  

 // ================= WINDERS =================

winders: {

  winder1: {

    totalizer: 0,

    number_of_rolls: 0,

    roll_dia: 0,

    roll_length: 0
  },

  winder2: {

    totalizer: 0,

    number_of_rolls: 0,

    roll_dia: 0,

    roll_length: 0
  }
},
  winderTrends: {

    winder1: {

      roll_length: [],

      roll_dia: []
    },

    winder2: {

      roll_length: [],

      roll_dia: []
    }
  },

  // ================= EXTRUDERS =================

  extruders: {

    A: {

      components: [],

      temperature: []
    },

    B: {

      components: [],

      temperature: []
    },

    C: {

      components: [],

      temperature: []
    }
  },

  // ================= MATERIAL =================

  material: {

    efficiency: 0,

    waste: 0
  }
});


// ================= SOCKET LISTENER =================

// socket.on("telemetry_update", (data) => {

//   console.log(
//     "GLOBAL TELEMETRY:",
//     data
//   );

//   // =================================================
//   // MACHINE
//   // =================================================

//   telemetry.machine =
//     data.machine_overview ||
//     telemetry.machine;

//   // =================================================
//   // CONTROL KPIs
//   // =================================================

//   telemetry.tower_nip = {

//     set:
//       Number(
//         data.machine_overview?.set_tower_nip
//       ) || 0,

//     actual:
//       Number(
//         data.machine_overview?.actual_tower_nip
//       ) || 0
//   };

//   telemetry.air_ring = {

//     set:
//       Number(
//         data.machine_overview?.set_air_ring
//       ) || 0,

//     actual:
//       Number(
//         data.machine_overview?.actual_air_ring
//       ) || 0
//   };

//   telemetry.regeneration = {

//     set:
//       Number(
//         data.machine_overview?.set_regeneration
//       ) || 0,

//     actual:
//       Number(
//         data.machine_overview?.actual_regeneration
//       ) || 0
//   };

//   telemetry.reverse_hauloff = {

//     set:
//       Number(
//         data.machine_overview?.set_reverse_hauloff
//       ) || 0,

//     actual:
//       Number(
//         data.machine_overview?.actual_reverse_hauloff
//       ) || 0
//   };

//   // =================================================
//   // KPI CACHE
//   // =================================================

//   telemetry.kpis = {

//     tower_set:
//       telemetry.tower_nip.set,

//     tower_act:
//       telemetry.tower_nip.actual,

//     air_set:
//       telemetry.air_ring.set,

//     air_act:
//       telemetry.air_ring.actual,

//     regen_set:
//       telemetry.regeneration.set,

//     regen_act:
//       telemetry.regeneration.actual,

//     hauloff_set:
//       telemetry.reverse_hauloff.set,

//     hauloff_act:
//       telemetry.reverse_hauloff.actual,

//     valve_act:
//       Number(
//         data.machine_overview?.valve_position
//       ) || 0
//   };

//   // =================================================
//   // SPEED
//   // =================================================

//   telemetry.speed.set =
//     data.speed_trend?.set || [];

//   telemetry.speed.actual =
//     data.speed_trend?.actual || [];

//   // =================================================
//   // IBC
//   // =================================================

//   telemetry.ibc.in =
//     data.ibc_temp?.in || [];

//   telemetry.ibc.out =
//     data.ibc_temp?.out || [];

//   // =================================================
//   // THICKNESS
//   // =================================================

//   telemetry.thickness.trend =
//     data.thickness?.trend || [];

//   // =================================================
//   // DIE
//   // =================================================

//   telemetry.die =
//     data.die_temp_zones || [];

//   // =================================================
//   // LAYERS
//   // =================================================

//   telemetry.layers =
//     data.layer_data ||
//     telemetry.layers;

//   telemetry.layerTrends =
//     data.layer_trends ||
//     telemetry.layerTrends;

//   // =================================================
//   // WINDERS
//   // =================================================

//   telemetry.winders =
//     data.winder_data ||
//     telemetry.winders;

//   telemetry.winderTrends =
//     data.winder_trends ||
//     telemetry.winderTrends;

//   // =================================================
//   // EXTRUDERS
//   // =================================================

//   telemetry.extruders =
//     data.extruders ||
//     telemetry.extruders;

//   // =================================================
//   // MATERIAL CALCULATION
//   // =================================================

//   const set =
//     telemetry.machine.total_set_output || 0;

//   const act =
//     telemetry.machine.total_actual_output || 0;

//   if (set > 0) {

//     const efficiency =
//       (act / set) * 100;

//     telemetry.material.efficiency =
//       efficiency.toFixed(1);

//     telemetry.material.waste =
//       (100 - efficiency).toFixed(1);
//   }
// });
socket.on("telemetry_update", (data) => {

  console.log(
    "GLOBAL TELEMETRY:",
    data
  );

  // =================================================
  // MACHINE
  // =================================================

  Object.assign(
    telemetry.machine,
    data.machine_overview || {}
  );

  // =================================================
  // CONTROL KPIs
  // =================================================

  telemetry.tower_nip = {

    set:
      Number(
        data.machine_overview?.set_tower_nip
      ) || 0,

    actual:
      Number(
        data.machine_overview?.actual_tower_nip
      ) || 0
  };

  telemetry.air_ring = {

    set:
      Number(
        data.machine_overview?.set_air_ring
      ) || 0,

    actual:
      Number(
        data.machine_overview?.actual_air_ring
      ) || 0
  };

  telemetry.regeneration = {

    set:
      Number(
        data.machine_overview?.set_regeneration
      ) || 0,

    actual:
      Number(
        data.machine_overview?.actual_regeneration
      ) || 0
  };

  telemetry.reverse_hauloff = {

    set:
      Number(
        data.machine_overview?.set_reverse_hauloff
      ) || 0,

    actual:
      Number(
        data.machine_overview?.actual_reverse_hauloff
      ) || 0
  };

  // =================================================
  // KPI CACHE
  // =================================================

  telemetry.kpis = {

    tower_set:
      telemetry.tower_nip.set,

    tower_act:
      telemetry.tower_nip.actual,

    air_set:
      telemetry.air_ring.set,

    air_act:
      telemetry.air_ring.actual,

    regen_set:
      telemetry.regeneration.set,

    regen_act:
      telemetry.regeneration.actual,

    hauloff_set:
      telemetry.reverse_hauloff.set,

    hauloff_act:
      telemetry.reverse_hauloff.actual,

    valve_act:
      Number(
        data.machine_overview?.valve_position
      ) || 0
  };

  // =================================================
  // SPEED
  // =================================================

  telemetry.speed.set =
    data.speed_trend?.set || [];

  telemetry.speed.actual =
    data.speed_trend?.actual || [];

  // =================================================
  // IBC
  // =================================================

  telemetry.ibc.in =
    data.ibc_temp?.in || [];

  telemetry.ibc.out =
    data.ibc_temp?.out || [];

  // =================================================
  // THICKNESS
  // =================================================

  telemetry.thickness.trend =
    data.thickness?.trend || [];

  // =================================================
  // DIE
  // =================================================

  telemetry.die =
    data.die_temp_zones || [];

  // =================================================
  // LAYERS
  // =================================================

  Object.assign(
    telemetry.layers,
    data.layer_data || {}
  );

  Object.assign(
    telemetry.layerTrends,
    data.layer_trends || {}
  );

  // =================================================
  // WINDERS
  // =================================================

  Object.assign(
    telemetry.winders,
    data.winder_data || {}
  );

  Object.assign(
    telemetry.winderTrends,
    data.winder_trends || {}
  );

  // =================================================
  // EXTRUDERS
  // =================================================

  Object.assign(
    telemetry.extruders,
    data.extruders || {}
  );

  // =================================================
  // MATERIAL CALCULATION
  // =================================================

  const set =
    telemetry.machine.total_set_output || 0;

  const act =
    telemetry.machine.total_actual_output || 0;

  if (set > 0) {

    const efficiency =
      (act / set) * 100;

    telemetry.material.efficiency =
      efficiency.toFixed(1);

    telemetry.material.waste =
      (100 - efficiency).toFixed(1);
  }

});
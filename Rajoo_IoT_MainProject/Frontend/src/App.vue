 <template>
  <router-view v-slot="{ Component }">
    <transition :name="transitionName">
      <keep-alive>
        <component :is="Component" />
      </keep-alive>
    </transition>
  </router-view>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";
import socket from "./services/socket";

export default {
  setup() {
    const transitionName = ref("fade");
    const router = useRouter();

    // ------------------------------
    // Route transition logic
    // ------------------------------
    router.beforeEach((to, from, next) => {
      if (from.path.startsWith("/layer") && to.path === "/dashboard") {
        transitionName.value = "slide-back";
      } else {
        transitionName.value = "fade";
      }
      next();
    });

    // ------------------------------
    // Telemetry listener (unchanged)
    // ------------------------------
    const onTelemetry = (data) => {
      console.log("LIVE TELEMETRY RECEIVED:", data);
    };

    onMounted(() => {
      console.log("App mounted → attaching telemetry listener");
      socket.on("telemetry_update", onTelemetry);
    });

    onBeforeUnmount(() => {
      socket.off("telemetry_update", onTelemetry);
    });

    return { transitionName };
  }
};
</script>
// import { createApp } from "vue";
// import App from "./App.vue";
// import router from "./router";

// createApp(App).use(router).mount("#app");

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";


import socket from "./services/socket";

const app = createApp(App);

// make socket globally available
app.config.globalProperties.$socket = socket;

app.use(router);
app.mount("#app");


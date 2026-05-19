// import { defineConfig } from "vite";
// import vue from "@vitejs/plugin-vue";

// export default defineConfig({
//   plugins: [vue()],
//   server: {
//     host: "127.0.0.1",
//     port: 5173,
//     strictPort: true,
//     open: false
//   }
// });



import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { fileURLToPath, URL } from "node:url";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    host: "127.0.0.1",
    port: 5173,
    strictPort: true,
    open: false,
  },
});

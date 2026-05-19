import { io } from "socket.io-client";

const socket = io("http://localhost:5000", {
  transports: ["polling"],
  upgrade: false,
  rememberUpgrade: false,
  autoConnect: true,
  reconnection: true,
  reconnectionAttempts: Infinity,
  reconnectionDelay: 1000,
  timeout: 20000
});

socket.on("connect", () => {
  console.log("[SOCKET] connected:", socket.id);
});

socket.on("disconnect", (reason) => {
  console.log("[SOCKET] disconnected:", reason);
});

socket.on("connect_error", (err) => {
  console.error("[SOCKET] error:", err.message);
});

export default socket;

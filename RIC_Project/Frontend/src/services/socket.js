


// import { io } from "socket.io-client";

// const socket = io(
//   "https://api.appvirtualex.com",
//   {
//     transports: ["websocket", "polling"],
//     autoConnect: true,
//     reconnection: true,
//     reconnectionAttempts: Infinity,
//     reconnectionDelay: 1000,
//     timeout: 20000
//   }
// );

// socket.on("connect", () => {
//   console.log("[SOCKET] connected:", socket.id);
// });

// socket.on("disconnect", (reason) => {
//   console.log("[SOCKET] disconnected:", reason);
// });

// socket.on("connect_error", (err) => {
//   console.error("[SOCKET] error:", err.message);
// });

// export default socket;




import { io } from "socket.io-client";

const socket = io(
  "https://api.appvirtualex.com",
  {
    transports: ["polling", "websocket"],

    autoConnect: true,

    reconnection: true,
    reconnectionAttempts: Infinity,
    reconnectionDelay: 1000,

    timeout: 20000,

    forceNew: true
  }
);

socket.on("connect", () => {

  console.log(
    "[SOCKET] connected:",
    socket.id
  );

});

socket.on("disconnect", (reason) => {

  console.log(
    "[SOCKET] disconnected:",
    reason
  );

});

socket.on("connect_error", (err) => {

  console.error(
    "[SOCKET] error:",
    err
  );

});

socket.onAny((event, ...args) => {

  console.log(
    "[SOCKET EVENT]",
    event,
    args
  );

});

export default socket;
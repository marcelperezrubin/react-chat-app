import express from "express";
import http from "http";
import morgan from "morgan";
import { Server as SocketServer } from "socket.io";
import {dirname, join} from "path";
import { fileURLToPath } from "url";

import { PORT } from "./config.js";
import cors from "cors";

// Inicialización de Express y configuración de middlewares
const app = express();
const __dirname = dirname(fileURLToPath(import.meta.url));
app.use(cors());
app.use(morgan("dev"));
app.use(express.urlencoded({ extended: false }));
app.use(express.static(resolve("frontend/dist")));

// Creación del servidor HTTP y configuración de Socket.IO
const server = http.createServer(app);
const io = setupSocketIO(server);

// Manejo de conexiones de Socket.IO
io.on("connection", (socket) => {
  console.log(socket.id);
  socket.on("message", (body) => {
    socket.broadcast.emit("message", {
      body,
      from: socket.id.slice(8),
    });
  });
});


app.use(express.static(join(__dirname, '../frontend/dist')))

// Inicio del servidor
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

// Función para configurar Socket.IO
function setupSocketIO(httpServer) {
  return new SocketServer(httpServer, {
    cors: {
      origin: "*",
    },
  });
}

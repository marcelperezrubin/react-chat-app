// frontend/vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/socket.io': {
        target: 'ws://localhost:3000',
        ws: true,
      },
    },
  },
  build: {
    rollupOptions: {
      external: ['react', 'react-dom'],
    },
  },
  base: '/react-chat-app/frontend/dist/',
});

// preload.js (Renderer Process Communication)
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
    // Note: Expose any functions or values needed in the renderer process
});

// main.js (Main Process)
const { app, BrowserWindow } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: true,  
            webSecurity: true,
        },
        
    });

    mainWindow.loadFile('index.html');

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

app.whenReady().then(createWindow); 

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();  // Note: For macOS
});

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow();
    }
});

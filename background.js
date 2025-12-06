const { app, BrowserWindow, ipcMain, dialog } = require('electron')
const path = require('path')

function createWindow () {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    
    // 👇👇👇【新增】设置窗口图标 👇👇👇
    // 注意：如果在开发环境，路径通常是 public/logo.png
    // 如果打包后图标丢失，可能需要指向 dist/logo.png，取决于打包配置
    icon: path.join(__dirname, 'public/logo.png'), 
    // 👆👆👆【新增】结束 👆👆👆

    // 隐藏顶部 File/Edit 菜单栏，让软件更干净
    autoHideMenuBar: true, 
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      webSecurity: false // 允许加载本地图片
    }
  })
  
  // 彻底移除菜单栏（某些Windows版本需要这行）
  win.setMenuBarVisibility(false)

 if (!app.isPackaged) {
   win.loadURL('http://localhost:5173')
 } else {
   win.loadFile(path.join(__dirname, 'dist/index.html'))
 }
}

app.whenReady().then(() => {
  // 🟢 监听：前端 App.vue 请求打开文件夹选择框
  ipcMain.handle('dialog:openDirectory', async () => {
    const { canceled, filePaths } = await dialog.showOpenDialog({
      properties: ['openDirectory']
    })
    if (canceled) return null
    return filePaths[0]
  })

  createWindow()
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})
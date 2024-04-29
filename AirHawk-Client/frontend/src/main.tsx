import React from 'react'
import ReactDOM from 'react-dom/client'
import "./global.scss"
import App from './App'
import { ThemeProvider } from './components/theme-provider'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ThemeProvider defaultTheme='dark' storageKey='theme'>
      <App></App>
    </ThemeProvider>
  </React.StrictMode>
)

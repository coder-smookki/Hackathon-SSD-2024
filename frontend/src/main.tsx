import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles/global.css'
import App from './App.tsx'
import { BrowserRouter } from "react-router";

createRoot(document.getElementById('root')!).render(
  <StrictMode>
      <BrowserRouter basename="/Hackathon-SSD-2024">
          <App />
      </BrowserRouter>
  </StrictMode>,
)

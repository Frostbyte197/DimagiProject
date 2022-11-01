import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import LocationForm from '@/views/LocationForm.vue'
import LocationGrid from '@/views/LocationGrid.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/location-form',
    name: 'LocationForm',
    component: LocationForm
  },
  {
    path: '/location-grid',
    name: 'LocationGrid',
    component: LocationGrid
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

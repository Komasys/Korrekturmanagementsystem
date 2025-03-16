import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import SignUp from '@/components/SignUp.vue'
import DashboardView from '@/views/DashboardView.vue'
import API_URL from '@/api'
import LoginView from '@/views/LoginView.vue'
import TicketCreate from '@/components/TicketCreate.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUp,
    },
    {
      path: '/signout',
      name: 'signout',
      beforeEnter: (to, from, next) => {
        localStorage.removeItem('access_token')
        next({ name: 'signin' })
      },
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true },
    },
    {
      path: '/ticket-erstellen',
      name: 'TicketCreate',
      component: TicketCreate,
      meta: { requiresAuth: true },
    },
  ],
})

// Navigation Guard
router.beforeEach(async (to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    const token = localStorage.getItem('access_token')

    if (!token) {
      next({ name: 'login' })
      return
    }

    try {
      const response = await fetch(`${API_URL}/auth/user-info`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
      })

      if (response.ok) {
        const userInfo = await response.json()
        const userStore = useUserStore()
        userStore.setEmail(userInfo.email)
        userStore.setName(userInfo.name)
        userStore.setBenutzerId(userInfo.id)
        next()
      } else {
        console.error('Unauthorized. Redirecting to sign-in.')
        localStorage.removeItem('access_token')
        next({ name: 'login' })
      }
    } catch (error) {
      console.error('Invalid token:', error)
      localStorage.removeItem('access_token')
      next({ name: 'login' })
    }
  } else {
    next()
  }
})

export default router

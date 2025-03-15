import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import HomeView from '@/views/HomeView.vue'
import SignUp from '@/components/SignUp.vue'
import SignIn from '@/components/SignIn.vue'
import DashboardView from '@/views/DashboardView.vue'
import API_URL from '@/api'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUp,
    },
    {
      path: '/signin',
      name: 'signin',
      component: SignIn,
    },
    {
      path: '/signout',
      name: 'signout',
      beforeEnter: (to, from, next) => {
        localStorage.removeItem('access_token')
        next({ name: 'home' })
      },
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true },
    },
  ],
})

// Navigation Guard
router.beforeEach(async (to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    const token = localStorage.getItem('access_token')

    if (!token) {
      next({ name: 'signin' })
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
        next()
      } else {
        console.error('Unauthorized. Redirecting to sign-in.')
        localStorage.removeItem('access_token')
        next({ name: 'signin' })
      }
    } catch (error) {
      console.error('Invalid token:', error)
      localStorage.removeItem('access_token')
      next({ name: 'signin' })
    }
  } else {
    next()
  }
})

export default router

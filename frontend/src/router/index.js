import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import SignUp from '@/components/SignUp.vue'
import DashboardView from '@/views/DashboardView.vue'
import API_URL from '@/api'
import LoginView from '@/views/LoginView.vue'
import TicketDetails from '@/components/TicketDetails.vue'
import TicketCreate from '@/components/TicketCreate.vue'
import MyTickets from '@/components/MyTickets.vue'
import AllTickets from '@/components/AllTickets.vue'
import BearbeiteteTickets from '@/components/EditTickets.vue'

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
        next({ name: 'login' })
      },
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true },
      children: [
        {
          path: 'create-ticket',
          name: 'create-ticket',
          component: TicketCreate,
        },
        {
          path: 'my-tickets',
          name: 'my-tickets',
          component: MyTickets,
        },
        {
          path: 'all-tickets',
          name: 'all-tickets',
          component: AllTickets,
        },
        {
          path: 'ticket/:id',
          name: 'ticket-details',
          component: TicketDetails,
          props: (route) => ({ ticketId: route.params.id }),
        },
        {
          path: 'bearbeitete-tickets',
          name: 'bearbeitete-tickets',
          component: BearbeiteteTickets,
        },
      ],
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
        userStore.setBenutzerRolle(userInfo.rolle)

        if (to.name === 'dashboard' || to.name === 'login') {
          next(
            userStore.benutzer_rolle === 'student'
              ? { name: 'my-tickets' }
              : { name: 'all-tickets' },
          )
        } else {
          next()
        }
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

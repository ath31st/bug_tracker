import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import LoginView from '@/views/LoginView.vue';
import { useAuthStore } from '@/stores/authStore';
import RegisterView from '@/views/RegisterView.vue';
import IssueView from '@/views/IssueView.vue';
import AboutView from '@/views/AboutView.vue';
import CreateIssue from '@/views/CreateIssue.vue';
import NotFoundView from '@/views/NotFoundView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true },
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,
      meta: { requiresAuth: true },
    },
    {
      path: '/new-issue',
      name: 'New Issue',
      component: CreateIssue,
      meta: { requiresAuth: true },
    },
    {
      path: '/issue/:id',
      name: 'Issue',
      component: IssueView,
      props: true,
      meta: { requiresAuth: true },
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/not-found',
      name: 'not-found',
      component: NotFoundView,
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/not-found',
    },
  ],
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.user) {
    next('/login');
  } else {
    next();
  }
});

export default router;

import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";
import LoginPage from "../pages/LoginPage.vue";
import RegisterPage from "../pages/RegisterPage.vue";
import TablesPage from "../pages/TablesPage.vue";
import TableDetailPage from "../pages/TableDetailPage.vue";
import OrderDetailPage from "../pages/OrderDetailPage.vue";

const routes = [
  { path: "/login", component: LoginPage },
  { path: "/register", component: RegisterPage },
  { path: "/", component: TablesPage, meta: { auth: true } },
  { path: "/tables/:id", component: TableDetailPage, meta: { auth: true } },
  { path: "/orders/:id", component: OrderDetailPage, meta: { auth: true } },
];

const router = createRouter({ history: createWebHistory(), routes });

router.beforeEach((to, _from, next) => {
  const a = useAuthStore();
  if (to.meta.auth && !a.isLoggedIn) next("/login");
  else next();
});

export default router;

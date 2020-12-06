import { createRouter, createWebHistory } from "vue-router";
// import Home from "../views/Home.vue";
import Index from "@/views/Index.vue";
import SignIn from "@/components/SignIn.vue";
import SignUp from "@/components/SignUp.vue";
import Dashboard from "@/views/Dashboard";

const routes = [
  {
    path: "/",
    component: Index,
    children: [
      {
        name: "sign-in",
        path: "/sign-in",
        component: SignIn,
        fallback: false
      },
      {
        name: "sign-up",
        path: "/sign-up",
        component: SignUp,
        fallback: false
      }
    ]
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue")
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: Dashboard
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;

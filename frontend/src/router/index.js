import { createRouter, createWebHistory } from "vue-router";
// import Home from "../views/Home.vue";
import Index from "@/views/Index.vue";
import SignIn from "@/components/SignIn.vue";
import SignUp from "@/components/SignUp.vue";

const routes = [
  // {
  //   path: "/",
  //   name: "Home",
  //   component: Home
  // },
  // {
  //   path: "/",
  //   name: "Index",
  //   component: Index
  // },
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
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;

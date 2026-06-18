import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../components/home/HomeView.vue'
import RecipeView from '../components/recipe/RecipeView.vue'
import FavoritesView from '../components/favorites/FavoritesView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/recipe/:id', name: 'recipe', component: RecipeView, props: true },
    { path: '/favorites', name: 'favorites', component: FavoritesView },
  ],
  scrollBehavior(_, __, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0 }
  },
})

export default router

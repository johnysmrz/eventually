import { createRouter, createWebHistory } from 'vue-router'

import EventSelectorPage from './pages/EventSelectorPage.vue'
import EventEditorPage from './pages/EventEditorPage.vue'

const routes = [
  { path: '/event-selector', name: 'EventSelector', component: EventSelectorPage },
  { path: '/event-editor/:id', name: 'EventEditor', component: EventEditorPage, children:
    [
      { path: '', name: 'EventEditorProgram', component: () => import('./pages/EventEditor/ProgramOverview.vue') },
    ] 
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

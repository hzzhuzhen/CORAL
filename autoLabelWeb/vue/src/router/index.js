import {createRouter, createWebHistory} from 'vue-router'
import NotFoundView from '../views/NotFoundView.vue'
import TrackBoard from '../views/TrackBoard.vue'
import CorrectionView from '../views/CorrectionView.vue'
import HomeView from '../views/HomeView.vue'
import LLMView from '../views/LLMView.vue'
import SLMView from '../views/SLMView.vue'
import ResultDisplay from '../views/ResultDisplay.vue'
import LLMView2 from '../views/LLMView2.vue'
import TestView from "@/views/TestView.vue";
import TaskForm from "@/views/TaskForm.vue";
import LoginView from "@/views/LoginView.vue"
import RegisterView from "@/views/RegisterView.vue";

const routes = [
    {
        path: '/',
        name: 'login',
        component: () => import('../views/CreateTask.vue')
    },
    {
        path: '/register',
        name: 'register',
        component: () => import('../views/RegisterView.vue')
    },
    {
        path: '/createtask',
        name: 'createtask',
        component: () => import('../views/CreateTask.vue')
    },
    {
        path: '/listtask',
        name: 'listtask',
        component: () => import('../views/TaskListView.vue')
    },
    {
        path: '/model_setting',
        name: 'model_setting',
        component: () => import('../views/ModelSetting.vue')
    },
    {
        path: '/recommend',
        name: 'recommend',
        component: () => import('../views/RecommendationView.vue')
    },
    {
        path: '/',
        name: 'home',
        component: HomeView
    },
    {
        path: '/trackboard/',
        name: 'trackboard',
        component: TrackBoard
    },
    {
        path: '/welcome',
        name: 'welcome',
        component: () => import('../views/WelcomeView.vue')
    },
    {
        path: '/correctionView/',
        name: 'correction',
        component: CorrectionView
    },
    {
        path: '/LLMView/',
        name: 'LLMView',
        component: LLMView
    },
    {
        path: '/LLMView2/',
        name: 'LLMView2',
        component: LLMView2
    },
    {
        path: '/SLMView/',
        name: 'SLMView',
        component: SLMView
    },
    {
        path: '/ResultDisplay/',
        name: 'ResultDisplay',
        component: ResultDisplay
    },
    {
        path: '/404/',
        name: '404',
        component: NotFoundView
    },
    {
        path: '/:catchAll(.*)',
        redirect: '/404/',
    },
    {
        path: '/TestView',
        name: 'TestView',
        component: TestView
    },
    {
        path: '/TaskForm',
        name: 'TaskForm',
        component: TaskForm
    },
    {
        path: '/LoginView',
        name: 'LoginView',
        component: LoginView
    },
    {
        path: '/RegisterView',
        name: 'RegisterView',
        component: RegisterView
    },
    {
        path: '/HomeView',
        name: 'HomeView',
        component: HomeView
    }
]

export default createRouter({
    history: createWebHistory(),
    routes
})

// export default router

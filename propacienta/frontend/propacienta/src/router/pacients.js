import MyPacients from '@/views/doctors/MyPacients';
import { ifAuthenticated, isDoctor } from './utils';


export default [
    {
        path: '/my-pacients',
        component: MyPacients,
        name: 'my-pacients',
        // beforeEnter: ifAuthenticated,
        beforeEnter: async (to, from, next) => { await ifAuthenticated(to, from, next), await isDoctor(to, from, next) },
    },
]

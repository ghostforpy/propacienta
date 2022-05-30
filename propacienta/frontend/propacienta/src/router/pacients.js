import MyPacientCalendar from '@/views/pacients/MyPacientCalendar';
import MyPacients from '@/views/pacients/MyPacients';
import { ifAuthenticated, isDoctor } from './utils';


export default [
    {
        path: '/my-pacients',
        component: MyPacients,
        name: 'my-pacients',
        // beforeEnter: ifAuthenticated,
        beforeEnter: async (to, from, next) => { await ifAuthenticated(to, from, next), await isDoctor(to, from, next) },
    },
    {
        path: '/my-pacient-calendar',
        component: MyPacientCalendar,
        name: 'my-pacient-calendar',
        beforeEnter: ifAuthenticated,
    },
]

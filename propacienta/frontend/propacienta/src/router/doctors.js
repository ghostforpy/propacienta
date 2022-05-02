import DoctorProfile from '@/views/doctors/DoctorProfile';
import DoctorsList from '@/views/doctors/DoctorsList';
import MyDoctorProfile from '@/views/doctors/MyDoctorProfile';
import { ifAuthenticated, isDoctorModeAvailable } from './utils';


export default [
    {
        path: '/my-doctor-profile',
        component: MyDoctorProfile,
        name: 'my-doctor-profile',
        // beforeEnter: ifAuthenticated,
        beforeEnter: async (to, from, next) => { await ifAuthenticated(to, from, next), await isDoctorModeAvailable(to, from, next) },
    },
    {
        path: '/doctors',
        component: DoctorsList,
        name: 'doctors',
        // beforeEnter: ifAuthenticated,
        // beforeEnter: async (to, from, next) => { await ifAuthenticated(to, from, next), await isDoctor(to, from, next) },
    },
    {
        path: '/doctors/:doctorId',
        component: DoctorProfile,
        name: 'doctor',
        // beforeEnter: ifAuthenticated,
        // beforeEnter: async (to, from, next) => { await ifAuthenticated(to, from, next), await isDoctor(to, from, next) },
    },
]

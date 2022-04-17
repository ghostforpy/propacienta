import AboutUs from '@/views/pages/AboutUs';
import ContacUs from '@/views/pages/ContacUs';
import PrivacyPolicy from '@/views/pages/PrivacyPolicy';
import TeamPage from '@/views/pages/TeamPage';

export default [
    {
        path: '/about-us',
        component: AboutUs,
        name: 'about-us',
        // beforeEnter: ifAuthenticated,
    },
    {
        path: '/privacy',
        component: PrivacyPolicy,
        name: 'privacy',
        // beforeEnter: ifAuthenticated,
    },
    {
        path: '/team',
        component: TeamPage,
        name: 'team',
        // beforeEnter: ifAuthenticated,
    },
    {
        path: '/contacts',
        component: ContacUs,
        name: 'contacts',
        // beforeEnter: ifAuthenticated,
    },
]

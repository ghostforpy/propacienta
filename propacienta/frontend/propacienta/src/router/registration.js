import RegistrationView from '@/views/registration/Registration';
import ActivateRegistrationView from '@/views/registration/ActivateRegistration';
import { ifNotAuthenticated } from './utils'
export default [
    {
        path: '/registration',
        name: 'registration',
        component: RegistrationView,
        beforeEnter: ifNotAuthenticated,
    },
    {
        path: '/accounts/activate/:uid/:token',
        name: 'accounts-activate',
        component: ActivateRegistrationView,
        beforeEnter: ifNotAuthenticated,
    },
]

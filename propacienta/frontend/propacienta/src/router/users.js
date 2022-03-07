import ProfileOwnerPacient from '@/views/users/ProfileOwnerPacient';
import { ifAuthenticated } from './utils'

export default [
    {
        path: '/users',
        // name: 'registration',
        component: ProfileOwnerPacient,
        children: [
            {
                // UserProfile will be rendered inside User's <router-view>
                // when /user/:id/profile is matched
                path: 'me',
                name: 'users-me',
                component: ProfileOwnerPacient
            },
            // {
            //     // UserPosts will be rendered inside User's <router-view>
            //     // when /user/:id/posts is matched
            //     // добавить beforeEnter ifDoctor
            //     path: ':id',
            //     component: ProfilePacient
            // }
        ],
        beforeEnter: ifAuthenticated,
    },
    // {
    //     path: '/accounts/activate/:uid/:token',
    //     name: 'accounts-activate',
    //     component: ActivateRegistrationView,
    //     beforeEnter: ifNotAuthenticated,
    // },
]

import OwnerMedicineCardView from '@/views/medicinecard/OwnerMedicineCard';
import { ifAuthenticated, isDoctor } from './utils';

export default [
    {
        path: '/my-medicine-card',
        component: OwnerMedicineCardView,
        name: 'my-medicine-card',
        beforeEnter: ifAuthenticated,
    },
    {
        path: '/medicine-card/:id',
        component: OwnerMedicineCardView,
        name: 'pacient-medicine-card',
        beforeEnter: async (to, from, next) => { await ifAuthenticated(to, from, next), await isDoctor(to, from, next) },
    },
]

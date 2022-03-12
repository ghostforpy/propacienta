import OwnerMedicineCardView from '@/views/medicinecard/OwnerMedicineCard';
import { ifAuthenticated } from './utils'

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
        beforeEnter: ifAuthenticated,
    },
]

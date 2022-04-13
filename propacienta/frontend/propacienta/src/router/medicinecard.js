import OwnerMedicineCardView from '@/views/medicinecard/OwnerMedicineCard';
import PacientMedicineCard from '@/views/medicinecard/PacientMedicineCard';
import { ifAuthenticated } from './utils';


export default [
    {
        path: '/my-medicine-card',
        component: OwnerMedicineCardView,
        name: 'my-medicine-card',
        beforeEnter: ifAuthenticated,
    },
    {
        path: '/pacient-medicine-card/:pacientId',
        component: PacientMedicineCard,
        name: 'pacient-medicine-card',
        beforeEnter: ifAuthenticated,
        // beforeEnter: async (to, from, next) => { await ifAuthenticated(to, from, next), await isDoctor(to, from, next) },
    },
]

import store from '@/store';
import { AUTH_PING } from "@/store/actions/auth";

export const ifAuthenticated = async (to, from, next) => {
    if (store.getters.isAuthenticated === '') {
        const isAuth = await store.dispatch(AUTH_PING)
        if (isAuth) {
            next()
            return
        }
        next({ name: 'login', query: { redirect: to.fullPath } })
        return
    }

    if (store.getters.isAuthenticated) {
        next()
        return
    }
    next({ name: 'login', query: { redirect: to.fullPath } })
}

export const ifNotAuthenticated = async (to, from, next) => {
    if (store.getters.isAuthenticated === '') {
        const isAuth = await store.dispatch(AUTH_PING)
        if (isAuth) {
            next({ name: 'logout' })
            return
        }
        next()
        return
    }
    if (store.getters.isAuthenticated) {
        next({ name: 'logout' })
        return
    }
    next()
}


export const isDoctor = async (to, from, next) => {
    if (store.getters.docMode) {
        next()
        return
    }
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
}
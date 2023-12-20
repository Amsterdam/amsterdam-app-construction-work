const domain = import.meta.env.VITE_DOMAIN ?? ''
const basePath = import.meta.env.VITE_BASE_PATH ?? '/api/v1'

const prependDomain = (relativeUrl: string) => `${domain}${basePath}${relativeUrl}`

export const getTokenUrl = prependDomain('/get-token/')
export const refreshTokenUrl = prependDomain('/refresh-token/')
export const userPasswordUrl = prependDomain('/user/password')
export const projectManagerUrl = prependDomain('/project/manager')
export const projectsUrl = prependDomain('/projects_jwt')
export const projectWarningUrl = prependDomain('/project/warning')

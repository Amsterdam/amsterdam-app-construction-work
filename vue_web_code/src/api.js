const domain = ''

const prependDomain = relativeUrl => `${domain}/api/v1/${relativeUrl}`

export const getTokenUrl = prependDomain('get-token/')
export const refreshTokenUrl = prependDomain('refresh-token/')
export const userPasswordUrl = prependDomain('user/password')
export const projectManagerUrl = prependDomain('project/manager')
export const projectsUrl = prependDomain('projects_jwt')
export const projectWarningUrl = prependDomain('/project/warning')
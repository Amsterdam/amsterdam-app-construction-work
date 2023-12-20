const domain = 'https://api-test-backend.app-amsterdam.nl'

const prependDomain = relativeUrl => `${domain}/api/v1/${relativeUrl}`

export const getTokenUrl = prependDomain('get-token/')
export const userPasswordUrl = prependDomain('user/password')
export const projectManagerUrl = prependDomain('project/manager')
export const projectsUrl = prependDomain('projects')
export const projectWarningUrl = prependDomain('/project/warning')
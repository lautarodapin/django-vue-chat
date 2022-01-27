import dayjs from 'dayjs'
export const fromNow = (date?: string) => !date ? '' : dayjs(date).fromNow()
export const formatDate = (date?: string) => !date ? '' : dayjs(date).format('MMM DD, YYYY')
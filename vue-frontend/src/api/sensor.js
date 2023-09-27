import request from '@/utils/request'

export function getSensorData() {
  return request({
    url: 'http://localhost:5392/data',
    method: 'get',
  })
}

export function getSensorData() {

}
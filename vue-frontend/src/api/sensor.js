import request from '@/utils/request'

export function getcurrentSensorData() {
  return request({
    url: 'http://localhost:7777/current-data',
    method: 'get',
  })
}

export function getSensorData() {
  return request({
    url: 'http://localhost:7777/data',
    method: 'get',
  })
}

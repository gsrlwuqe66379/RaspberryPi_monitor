import request from '@/utils/request'

export function getcurrentSensorData() {
  return request({
    url: 'http://192.168.31.138:8888/current-data',
    method: 'get',
  })
}

export function getSensorData() {
  return request({
    url: 'http://192.168.31.138:8888/data',
    method: 'get',
  })
}

export function getweatherforecast() {
  return request({
    url: 'http://192.168.31.138:8888/forecast',
  })
}
import request from '@/utils/request'

export function getcurrentSensorData() {
  return request({
    url: 'http://localhost:7779/current-data',
    method: 'get',
  })
}

export function getSensorData() {
  return request({
    url: 'http://localhost:7779/data',
    method: 'get',
  })
}

export function getstreamVideo() {
  return request({
    url: 'http://localhost:7779/video_feed',
    method: 'get',
  })
}

import axios from "axios";
import mockFetch from './mockData'

// Колхозное переключение между запросами к серверу и взятием локальных данных
// Это такие заглушечные обращения к серверу
// TODO: сделать так, чтобы этот параметр можно было передавать в консоли
const turnOnMock = true

const realFetch = axios.create({
    baseURL: "https://randomuser.me/api/",
    responseType: "json"
});

const fetchFunc = turnOnMock ? mockFetch : realFetch

export default fetchFunc
import { call, put, takeLatest } from 'redux-saga/effects';
import API from '../../utils/API'

function* test( dataFromComponent ) { // В аргумент приходит экшн. Если тип экшена, затрагивающего сагу, совпадает с типом, используемым в редьюсере, то в этом редьюсере запишуться данные поля "payload" первого вызывнного экшена, и без разницы, сколько было вызвано похожих экшенов из саги
    yield put({ type: "TEST_ITEM", payload: 123 });
    dataFromComponent.payload('/testRoute')
    const data = yield call(API.get, '/', {
        params: {
          results: 1,
          inc: 'name,email,picture'
        }
    })

    console.log('data from API', data)

}

export default function* testWatcher() {
    yield takeLatest('TEST', test)
}
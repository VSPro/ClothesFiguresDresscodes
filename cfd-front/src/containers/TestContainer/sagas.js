import { put, takeLatest } from 'redux-saga/effects';

function* test( dataFromComponent ) { // В аргумент приходит экшн. Если тип экшена, затрагивающего сагу, совпадает с типом, используемым в редьюсере, то в этом редьюсере запишуться данные поля "payload" первого вызывнного экшена, и без разницы, сколько было вызвано похожих экшенов из саги
    yield put({ type: "TEST_ITEM", payload: 123 });
    console.log('i\'m called from saga', dataFromComponent)
}

export default function* testWatcher() {
    yield takeLatest('TEST', test)
}
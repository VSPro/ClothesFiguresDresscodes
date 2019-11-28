import { call, put, takeLatest } from 'redux-saga/effects';
import API from '../../utils/API'

function* findTypeOfShape( shapeMetrics: any ) { // В аргумент приходит экшн. Если тип экшена, затрагивающего сагу, совпадает с типом, используемым в редьюсере, то в этом редьюсере запишуться данные поля "payload" первого вызывнного экшена, и без разницы, сколько было вызвано похожих экшенов из саги
console.log('shapeMetrics', shapeMetrics)
    const paramsOfUser = yield call(API.get as any, '/find-type-of-shape', { ...shapeMetrics })

    yield put({ type: "TYPE_OF_SHAPE", payload: paramsOfUser });

}

export default function* appWatcher() {
    yield takeLatest('SHAPE_METRICS', findTypeOfShape)
}
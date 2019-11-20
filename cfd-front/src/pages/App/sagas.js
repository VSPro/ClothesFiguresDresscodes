import { call, put, takeLatest } from 'redux-saga/effects';
import API from '../../utils/API'

function* findTypeOfShape( shapeMetrics ) { // В аргумент приходит экшн. Если тип экшена, затрагивающего сагу, совпадает с типом, используемым в редьюсере, то в этом редьюсере запишуться данные поля "payload" первого вызывнного экшена, и без разницы, сколько было вызвано похожих экшенов из саги

    const typeOfShape = yield call(API.get, '/find-type-of-shape', {
        params: {
            chest: shapeMetrics.chest,
            waist: shapeMetrics.waist,
            hips: shapeMetrics.hips
        }
    })

    console.log('data from API', typeOfShape)
    yield put({ type: "TYPE_OF_SHAPE", payload: typeOfShape });

}

export default function* appWatcher() {
    yield takeLatest('SHAPE_METRICS', findTypeOfShape)
}
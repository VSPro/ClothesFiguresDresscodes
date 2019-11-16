import { put, takeLatest, all } from 'redux-saga/effects';

function* test() {
    yield put({ type: "TEST", payload: 123 });
}

function* actionWatcher() {
    yield takeLatest('GET_NEWS', test)
}

export default function* rootSaga() {
    yield all([
        actionWatcher(),
    ]);
 }
import { all } from 'redux-saga/effects';

import testWatcher from '../pages/TestContainer/sagas'

export default function* rootSaga() {
    yield all([
        testWatcher(),
    ]);
 }
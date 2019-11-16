import { all } from 'redux-saga/effects';

import testWatcher from '../containers/TestContainer/sagas'

export default function* rootSaga() {
    yield all([
        testWatcher(),
    ]);
 }
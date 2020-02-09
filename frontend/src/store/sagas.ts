import { all } from "redux-saga/effects";

import testWatcher from "../pages/TestContainer/sagas";
import appWatcher from "../pages/FirstPage/sagas";

export default function* rootSaga() {
  yield all([testWatcher(), appWatcher()]);
}

import { all } from "redux-saga/effects";

import figureCalculationPageWatcher from "../pages/FigureCalculationPage/sagas";
import aboutPageWatcher from "../pages/AboutPage/sagas";

export default function* rootSaga() {
  yield all([
    figureCalculationPageWatcher(),
    aboutPageWatcher(),
  ]);
}

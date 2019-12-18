import { call, put, select, takeLatest } from "redux-saga/effects";
import API from "../../utils/API";

function* findTypeOfShape(shapeMetrics: any) {
  // В аргумент приходит экшн. Если тип экшена, затрагивающего сагу, совпадает с типом, используемым в редьюсере, то в этом редьюсере запишуться данные поля "payload" первого вызывнного экшена, и без разницы, сколько было вызвано похожих экшенов из саги
  console.log("shapeMetrics", shapeMetrics);
  // TODO: переделать так, чтобы в запрос передавалось не { ...shapeMetrics }, а { ...shapeMetrics.payload }
  const paramsOfUser = yield call(API.get as any, "/find-type-of-shape", {
    ...shapeMetrics
  });

  yield put({ type: "PARAMS_OF_USER", payload: paramsOfUser });
}

function* sendAppearanceFeatures(appearanceFeatures: any) {
  const paramsOfUser = yield select((state: any) => state.app.paramsOfUser);
  const photosURLs = yield call(API.get as any, "/relevant-photos", {
    appearanceFeatures: { ...appearanceFeatures.payload },
    paramsOfUser: paramsOfUser
  });
  yield put({ type: "RELEVANT_PHOTOS", payload: photosURLs });
}

export default function* appWatcher() {
  yield takeLatest("SHAPE_METRICS", findTypeOfShape);
  yield takeLatest("APPEARANCE_FEATURES", sendAppearanceFeatures);
}

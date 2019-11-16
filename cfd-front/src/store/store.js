import { createStore, applyMiddleware, compose } from 'redux'
import rootReducer from './rootReducer'

import createSagaMiddleware from 'redux-saga';
import rootSaga from './sagas';
const sagaMiddleware = createSagaMiddleware();

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

export default createStore(rootReducer, /* preloadedState, */ composeEnhancers(
    applyMiddleware(sagaMiddleware)
));

sagaMiddleware.run(rootSaga)
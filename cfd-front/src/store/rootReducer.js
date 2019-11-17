import { combineReducers } from 'redux'
import testReducer from '../pages/TestContainer/reducer'

export default combineReducers({
    test: testReducer
})
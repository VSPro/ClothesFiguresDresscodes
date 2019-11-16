import { combineReducers } from 'redux'
import testReducer from '../containers/TestContainer/reducer'

export default combineReducers({
    test: testReducer
})
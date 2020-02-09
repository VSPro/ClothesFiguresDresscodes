import { combineReducers } from "redux";
import testReducer from "../pages/TestContainer/reducer";
import appReducer from "../pages/FirstPage/reducer";

export default combineReducers({
  test: testReducer,
  app: appReducer
});

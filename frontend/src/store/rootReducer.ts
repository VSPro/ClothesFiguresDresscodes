import { combineReducers } from "redux";
import figureCalculationPageReducer from "../pages/FigureCalculationPage/reducer";
import aboutPageReducer from "../pages/AboutPage/reducer";
import filterPageReducer from "../pages/FiltersPage/reducer";


export default combineReducers({
  figureCalculationPage: figureCalculationPageReducer,
  aboutPage: aboutPageReducer,
  filterPage: filterPageReducer,
});

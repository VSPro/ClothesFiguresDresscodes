import React from "react";
import ReactDOM from "react-dom";
import { Route, BrowserRouter as Router, Switch } from "react-router-dom";
import FirstPage from "./pages/AboutPage/FirstPage";
import FigureCalculationPage from "./pages/FigureCalculationPage";
import { Provider } from "react-redux";
import store from "./store/store";
import FiltersPage from "./pages/FiltersPage";
import NotFoundPage from "./pages/NotFoundPage";

ReactDOM.render(
  <Provider store={store}>
    <Router>
      <Switch>
        <Route exact path="/" component={FirstPage} />
        <Route path="/calculation" component={FigureCalculationPage} />
        <Route path="/filters" component={FiltersPage} />
        <Route component={NotFoundPage} />
      </Switch>
    </Router>
  </Provider>,
  document.getElementById("root")
);

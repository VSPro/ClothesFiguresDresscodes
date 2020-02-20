import React from 'react';
import ReactDOM from 'react-dom';
import { Route, BrowserRouter as Router, Switch } from 'react-router-dom';
import { Provider } from 'react-redux';
import store from './store/store';
import MainLayout, { PageConfig } from './modules/MainLayout';
import urlScheme from './urlScheme';

ReactDOM.render(
  <Provider store={store}>
    <Router>
      <MainLayout urlScheme={urlScheme}/>
    
      {/* <Switch>
        <Route exact path="/" component={FrontPage} />
        <Route exact path="/firstPage" component={FirstPage} />
        <Route path="/calculation" component={FigureCalculationPage} />
        <Route path="/filters" component={FiltersPage} />
        <Route component={NotFoundPage} />
      </Switch> */}
      
    </Router>
  </Provider>,
  document.getElementById('root'),
);

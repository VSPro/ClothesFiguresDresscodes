import React from 'react';
import ReactDOM from 'react-dom';
import { Route, BrowserRouter as Router, Switch } from 'react-router-dom'
import './index.css';
import App from './pages/App/';

import { Provider } from 'react-redux';
import store from './store/store'
import SecondTestContainer from './pages/SecondTestContainer/';
import NotFoundPage from './pages/NotFoundPage/';

ReactDOM.render(
    <Provider store={ store }>
        <Router>
            <Switch>
                <Route exact path='/' component={ App } />
                <Route path='/filters' component={ SecondTestContainer } />
                <Route component={ NotFoundPage } />
            </Switch>
        </Router>
    </Provider>,
    document.getElementById('root')
);

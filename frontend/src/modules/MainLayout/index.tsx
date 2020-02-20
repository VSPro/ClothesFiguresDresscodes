import React, { Fragment } from 'react';
import { CssBaseline, Container } from '@material-ui/core';
import Footer from '../../components/Footer';
import Header from '../../components/Header';
import { Switch, Route } from 'react-router-dom';

interface Props {
  urlScheme?: PageConfig[];
}

export interface PageConfig {
  pageTitle: string;
  pageUrl: string;
  component: any;
}

const MainLayout: React.FC<Props> = ({
    urlScheme,
}) => {
  const headerItems = urlScheme?.map(item => ({pageTitle: item.pageTitle, pageUrl: item.pageUrl}))
  const components = urlScheme?.map(item => ({component: item.component, pageUrl: item.pageUrl}))
  
  return (
    <Fragment>
      <CssBaseline />
      <Header headerItems={headerItems}/>
        <Container>
        <Switch>
          {
            components?.map((item) => (
              <Route exact path={item.pageUrl} component={item.component} />
            ))
          }
        </Switch>
        </Container>
      <Footer />
    </Fragment>
  );
}

export default MainLayout

import React, { Fragment } from 'react';
import { CssBaseline, Container } from '@material-ui/core';
import Footer from '../../components/Footer';
import Header from '../../components/Header';

interface Props {

}

const MainLayout: React.FC<Props> = ({
    children
}) => {
  return (
    <Fragment>
      <CssBaseline />
      <Header />
        <Container>
            { children }
        </Container>
      <Footer />
    </Fragment>
  );
}

export default MainLayout

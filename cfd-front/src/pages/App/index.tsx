import React from 'react';
import Container from '@material-ui/core/Container';
import { makeStyles } from '@material-ui/core/styles';

import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';

import FirstInputsForm from './FirstInputsForm'
import SecondInputsForm from './SecondInputsForm'

const useStyles = makeStyles(theme => ({
  paper: {
    marginTop: theme.spacing(8),
    marginBottom: theme.spacing(5),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  }
}));

function App( props: any ) {
  const { title1, title2 } = props
  const classes = useStyles();

  return (
    <>
      <Typography variant="h6" gutterBottom>
        { title1 }
      </Typography>
      <Divider />
      <Container component="main" maxWidth="xs">        
        <div className={classes.paper}>
          <FirstInputsForm />
        </div>
      </Container>
      <Typography variant="h6" gutterBottom>
        { title2 }
      </Typography>
      <Divider />
      <Container component="main" maxWidth="xs">        
        <div className={classes.paper}>
          {/* <SecondInputsForm /> */}
        </div>
      </Container>
    </>
    
  );
}

export default App;

import React from 'react';
// import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';

import App from '../App/'

// const useStyles = makeStyles(theme => ({

// }));

export default function Main(props: any) {
  // const classes = useStyles();
  const { title1, title2 } = props;

  return (
    <Grid item xs={12} md={8}>
      {/* <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      <Divider /> */}

      <App title1={ title1 } title2={ title2 } />

    </Grid>
  );
}

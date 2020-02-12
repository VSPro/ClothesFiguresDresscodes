import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(theme => ({
  footer: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(6, 0),
  },
}));

export default function Footer() {
  const { footer } = useStyles();

  return <footer className={footer}>Footer</footer>;
}

import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';

interface MainFeaturedPost {
  title: string;
  description: string;
  img1: string;
  img2: string;
  firstBtnText: string;
  secondBtnText: string;
}

interface Props {
  mainFeaturedPost: MainFeaturedPost;
}

const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1,
  },
  mainContainerContent: {},
  imgClass: {},
  mainTitle: {},
  buttons: {
    '& > *': {
      margin: theme.spacing(4),
    },
  },
}));

export default function MainFeaturedPost({ mainFeaturedPost }: Props) {
  const { title, description, img1, img2, firstBtnText, secondBtnText } = mainFeaturedPost;
  const { root, imgClass, mainTitle, mainContainerContent, buttons } = useStyles();
  return (
    <Grid container className={root} spacing={2}>
      <Grid item xs={12} md={6} className={mainContainerContent}>
        <Typography variant="h3" color="inherit" gutterBottom className={mainTitle}>
          {title}
        </Typography>
        <Typography variant="h5" color="inherit" paragraph>
          {description}
        </Typography>
        <div className={buttons}>
          <Button variant="contained">{firstBtnText}</Button>
          <Button variant="contained">{secondBtnText}</Button>
        </div>
      </Grid>
      <Grid item xs={12} md={3}>
        <Paper className={imgClass} style={{ backgroundImage: `url(${img1})` }} />
      </Grid>
      <Grid item xs={12} md={3}>
        <Paper className={imgClass} style={{ backgroundImage: `url(${img2})` }} />
      </Grid>
    </Grid>
  );
}

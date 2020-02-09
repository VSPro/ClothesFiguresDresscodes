import React from "react";
import { useSelector } from "react-redux";
import { oc } from 'ts-optchain';

import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardActions from "@material-ui/core/CardActions";
import CardMedia from "@material-ui/core/CardMedia";

const useStyles = makeStyles(theme => ({
  form: {
    width: "100%", // Fix IE 11 issue.
    marginTop: theme.spacing(3)
  },
  submit: {
    margin: theme.spacing(3, 0, 2)
  },
  colorPickerButton: {
    margin: theme.spacing(3, 0, 2),
    height: 50,
    backgroundColor: "red"
  },
  titleForToggle: {
    marginTop: theme.spacing(1)
  },
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120
  },
  cardMedia: {
    paddingTop: "56.25%" // 16:9
  },
  card: {
    height: "100%",
    display: "flex",
    flexDirection: "column"
  }
}));

const PhotoViewer = (props: any) => {
  const classes = useStyles();
  const cards = oc(useSelector((state: any) => state.app.relevantPhotos))([]);

  return (
    <Grid container spacing={2}>
      {cards.map((card: any) => (
          <Grid item key={card} xs={12} sm={6}>
            <Card className={classes.card}>
              <CardMedia
                className={classes.cardMedia}
                image={card}
                title="Image title"
              />
              <CardActions>
                <Button size="small" color="primary">
                  посмотреть
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
    </Grid>
  );
};

export default PhotoViewer;

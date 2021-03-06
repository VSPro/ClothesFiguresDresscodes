import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import ToggleButton from "@material-ui/lab/ToggleButton";
import ToggleButtonGroup from "@material-ui/lab/ToggleButtonGroup";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(theme => ({
  form: {
    width: "100%", // Fix IE 11 issue.
    marginTop: theme.spacing(3)
  },
  submit: {
    margin: theme.spacing(3, 0, 2)
  },
  titleForToggle: {
    marginTop: theme.spacing(1)
  }
}));

export default function FirstInputsForm(props: any) {
  const setSecondFotmIsDisable = props.setSecondFotmIsDisable;
  const classes = useStyles();

  const [inputs, setInputs] = useState<any>({
    first: "",
    second: "",
    third: "",
    fourth: "",
    fifth: "m",
    sixth: "",
    seventh: ""
  });

  const typeOfShape = useSelector(
    (state: any): Array<number | string> => state.aboutPage.paramsOfUser.shape
  );
  const size = useSelector(
    (state: any): { sizeOfChest: string; sizeOfHips: string } =>
      state.aboutPage.paramsOfUser.sizeParams
  );

  const inputValidationFunc = (field: string) => {
    return (e: any, newAlignment: any) => {
      const value = e.target.value;
      if (isNaN(+value)) {
        setInputs((state: any) => {
          return { ...state, [field]: newAlignment };
        });
      }
      setInputs((state: any) => {
        return { ...state, [field]: value };
      });
    };
  };

  const dispatch = useDispatch();

  return (
    <form className={classes.form} noValidate>
      {/* TODO: Move all Grids to flex */}
      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}>
          <Typography
            variant="subtitle1"
            noWrap
            className={classes.titleForToggle}
          >
            Выберете пол:
          </Typography>
        </Grid>
        <Grid item xs={12} sm={6}>
          <ToggleButtonGroup
            value={inputs.fifth}
            exclusive
            onChange={inputValidationFunc("fifth")}
            aria-label="text alignment"
          >
            <ToggleButton value="m" aria-label="left aligned">
              {" "}
              М{" "}
            </ToggleButton>
            <ToggleButton value="f" aria-label="centered">
              {" "}
              Ж{" "}
            </ToggleButton>
          </ToggleButtonGroup>
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            id="chest-girth"
            label="Ширина плеч"
            // fullWidth
            // variant="outlined"
            margin="normal"
            type="number"
            value={inputs.first}
            onChange={inputValidationFunc("first") as any}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            id="chest-girth"
            label="Обхват груди"
            margin="normal"
            type="number"
            value={inputs.sixth}
            onChange={inputValidationFunc("sixth") as any}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            id="waist-circumference"
            label="Обхват талии"
            margin="normal"
            type="number"
            value={inputs.second}
            onChange={inputValidationFunc("second") as any}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            id="hip-girth"
            label="Обхват бёдер"
            margin="normal"
            type="number"
            value={inputs.third}
            onChange={inputValidationFunc("third") as any}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            id="height"
            label="Рост"
            margin="normal"
            type="number"
            value={inputs.fourth}
            onChange={inputValidationFunc("fourth") as any}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            id="height"
            label="Размер обуви"
            margin="normal"
            type="number"
            value={inputs.seventh}
            onChange={inputValidationFunc("seventh") as any}
          />
        </Grid>
        <Button
          fullWidth
          variant="outlined"
          color="secondary"
          className={classes.submit}
          disabled={
            !(
              inputs.first &&
              inputs.second &&
              inputs.third &&
              inputs.fourth &&
              inputs.fifth &&
              inputs.sixth &&
              inputs.seventh
            )
          }
          onClick={() => {
            setSecondFotmIsDisable(false);
            dispatch({
              type: "SHAPE_METRICS",
              payload: {
                shoulders: inputs.first,
                chest: inputs.sixth,
                waist: inputs.second,
                hips: inputs.third,
                height: inputs.fourth,
                sex: inputs.fifth,
                shoes: inputs.seventh
              }
            });
          }}
        >
          Определить тип фигуры
        </Button>
        <Grid item xs={12} sm={6}>
          <Typography variant="subtitle1" noWrap>
            Ваш тип фигуры:
          </Typography>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Typography variant="subtitle1" noWrap>
            {typeOfShape ? typeOfShape : "~"}
          </Typography>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Typography variant="subtitle1" noWrap>
            Ваш размер по плечам:
          </Typography>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Typography variant="subtitle1" noWrap>
            {size.sizeOfChest ? size.sizeOfChest : "~"}
          </Typography>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Typography variant="subtitle1" noWrap>
            Ваш размер по бёдрам:
          </Typography>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Typography variant="subtitle1" noWrap>
            {size.sizeOfHips ? size.sizeOfHips : "~"}
          </Typography>
        </Grid>
      </Grid>
    </form>
  );
}
